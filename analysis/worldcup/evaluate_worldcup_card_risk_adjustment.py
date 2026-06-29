"""
WORLD CUP 2026 — CARD-RISK ADJUSTMENT EVALUATION (Fase 4G). READ-ONLY · NO API · NO scraping · NO web ·
NO market/odds/betting · NO fabrication · NO secrets. Pure football. MEASURE FIRST, do NOT change weights.

Evaluates the Fase-4F card-risk adjustment by comparing, on REAL settled World Cup outcomes:
  * probability_card_original  (the props model's frozen-at-KO p_card)
  * probability_card_adjusted  (reconstructed by applying card_risk_adjuster to that same p_card with the
                                CURRENT auto profiles + referee context — the SAME transform the product
                                applies live in build_worldcup_player_events.apply_card_adjustment)
  * the REAL card event         (act_card from the settled props log: 1 if booked, else 0)

Labelled set = settled rows of worldcup_player_props_log.csv (full per-player denominator, not only the
players who happened to have an event). The current worldcup_player_events.json holds only UPCOMING
fixtures (no results yet); it is read to confirm the live adjuster config and for a consistency note.

METHODOLOGICAL CAVEAT (stated honestly in the report): the auto profiles are CUMULATIVE — they include
the very fixtures being scored — so the reconstructed `adjusted` carries a mild look-ahead advantage.
With a small positive count the result is therefore indicative, NOT a verdict. No victory on a thin sample.

Outputs (generated artifacts; report/JSON are gitignored — regenerable — the CSV may be auto-committed):
  * analysis/worldcup/worldcup_card_risk_evaluation.csv          (one row per evaluated prediction)
  * analysis/worldcup/worldcup_card_risk_evaluation_summary.json (overall + segments + recommendation)
  * analysis/worldcup/worldcup_card_risk_evaluation_report.txt   (human-readable conclusion)

Run:  python analysis/worldcup/evaluate_worldcup_card_risk_adjustment.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import card_risk_adjuster as cadj  # noqa: E402
import referee_context as refctx  # noqa: E402
import player_data_adapters as adapters  # noqa: E402

PROPS_LOG = HERE / "worldcup_player_props_log.csv"
PLAYER_EVENTS_JSON = HERE / "worldcup_player_events.json"
FIXTURE_REFEREES = ROOT / "data" / "external" / "fixture_referees.csv"
OUT_CSV = HERE / "worldcup_card_risk_evaluation.csv"
OUT_JSON = HERE / "worldcup_card_risk_evaluation_summary.json"
OUT_TXT = HERE / "worldcup_card_risk_evaluation_report.txt"

MIN_SAMPLE = 30           # spec §2: below this -> low sample, do not conclude
SEG_MIN = 5               # min n to report a segment with any confidence
REF_MIN_MATCHES = 2       # spec §3D
TEAM_MIN_PREDS = 3        # spec §3E
EPS = 1e-12

CSV_COLUMNS = [
    "fixture_id", "player_id", "player_name", "team", "team_id", "position", "referee_name",
    "probability_card_original", "probability_card_adjusted", "adjustment_direction",
    "abs_adjustment", "label_card", "confidence", "data_quality",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ pure metric helpers (testable)
def brier_score(probs, labels):
    """Mean squared error of probabilistic forecasts. None if empty."""
    pairs = [(float(p), int(y)) for p, y in zip(probs, labels) if p is not None]
    if not pairs:
        return None
    return sum((p - y) ** 2 for p, y in pairs) / len(pairs)


def log_loss(probs, labels):
    """Binary cross-entropy with clipping. None if empty."""
    pairs = [(min(max(float(p), EPS), 1 - EPS), int(y)) for p, y in zip(probs, labels) if p is not None]
    if not pairs:
        return None
    return -sum(y * math.log(p) + (1 - y) * math.log(1 - p) for p, y in pairs) / len(pairs)


def calibration_bins(probs, labels, n_bins=10):
    """Reliability table: per bin {bin_lo, bin_hi, n, avg_pred, real_rate}. Empty bins omitted."""
    pairs = [(float(p), int(y)) for p, y in zip(probs, labels) if p is not None]
    out = []
    for i in range(n_bins):
        lo, hi = i / n_bins, (i + 1) / n_bins
        sel = [(p, y) for p, y in pairs if (p >= lo and (p < hi or (i == n_bins - 1 and p <= hi)))]
        if not sel:
            continue
        out.append({"bin_lo": round(lo, 2), "bin_hi": round(hi, 2), "n": len(sel),
                    "avg_pred": round(sum(p for p, _ in sel) / len(sel), 4),
                    "real_rate": round(sum(y for _, y in sel) / len(sel), 4)})
    return out


def _r(v, nd=5):
    return None if v is None else round(float(v), nd)


def metric_block(rows):
    """Brier/LogLoss for original & adjusted over a list of eval rows + deltas + sizes."""
    o = [r["probability_card_original"] for r in rows]
    a = [r["probability_card_adjusted"] for r in rows]
    y = [r["label_card"] for r in rows]
    bo, ba = brier_score(o, y), brier_score(a, y)
    lo, la = log_loss(o, y), log_loss(a, y)
    n_pos = sum(1 for v in y if v == 1)
    return {
        "n": len(rows),
        "n_positive": n_pos,
        "real_card_rate": _r(n_pos / len(rows) if rows else None, 4),
        "avg_probability_original": _r(sum(o) / len(o) if o else None, 4),
        "avg_probability_adjusted": _r(sum(a) / len(a) if a else None, 4),
        "brier_original": _r(bo), "brier_adjusted": _r(ba),
        "delta_brier": _r((ba - bo) if (bo is not None and ba is not None) else None),
        "logloss_original": _r(lo), "logloss_adjusted": _r(la),
        "delta_logloss": _r((la - lo) if (lo is not None and la is not None) else None),
        "avg_abs_adjustment": _r(sum(r["abs_adjustment"] for r in rows) / len(rows) if rows else None, 4),
    }


# ============================================================ evaluation-row construction
class RefereeResolver:
    """Resolves a per-fixture referee_context (manual>auto>none), cached. Loaded once."""
    def __init__(self, fixture_referees=None, manual=None, manual_reason=None, auto=None, auto_reason=None):
        self.fix_ref = fixture_referees or {}
        self.manual, self.manual_reason = (manual, manual_reason)
        self.auto, self.auto_reason = (auto, auto_reason)
        self._cache = {}

    def ctx_for(self, fixture_id):
        if fixture_id not in self._cache:
            name = self.fix_ref.get(fixture_id)
            self._cache[fixture_id] = refctx.build_referee_context(
                name, self.manual, self.manual_reason, self.auto, self.auto_reason)
        return self._cache[fixture_id]


def _position_for(pid, player_prof, pos_map):
    if player_prof and player_prof.get("position"):
        return str(player_prof["position"]).strip().upper() or None
    if pid is not None and pos_map.get(pid):
        return str((pos_map[pid] or {}).get("position") or "").strip().upper() or None
    return None


def build_evaluation_rows(settled_df, card_profiles, pos_map, referee_resolver):
    """For each settled per-player prediction, reconstruct the adjusted probability (same transform as
    the product) and pair it with the real card label. Returns a list of eval-row dicts. NO fabrication:
    a row without a numeric p_card or without a settled result is skipped."""
    players = (card_profiles or {}).get("players", {})
    teams = (card_profiles or {}).get("teams", {})
    positions = (card_profiles or {}).get("positions", {})
    rows = []
    for _, r in settled_df.iterrows():
        p_card = r.get("p_card")
        if p_card is None or (isinstance(p_card, float) and pd.isna(p_card)):
            continue
        try:
            label = 1 if float(r.get("act_card") or 0) >= 1 else 0
        except Exception:
            continue
        try:
            pid = int(r.get("player_id")) if pd.notna(r.get("player_id")) else None
        except Exception:
            pid = None
        try:
            tid = int(r.get("team_id")) if pd.notna(r.get("team_id")) else None
        except Exception:
            tid = None
        try:
            fid = int(r.get("fixture_id"))
        except Exception:
            continue

        player_prof = players.get(pid) if pid is not None else None
        pos_label = _position_for(pid, player_prof, pos_map)
        position_prof = positions.get(pos_label) if pos_label else None
        team_prof = teams.get(tid) if tid is not None else None
        ref_ctx = referee_resolver.ctx_for(fid)

        adj = cadj.adjust_card_risk(p_card, player_profile=player_prof, position_profile=position_prof,
                                    team_profile=team_prof, referee_context=ref_ctx)
        orig = adj["probability_card_original"]
        adjusted = adj["probability_card_adjusted"]
        if orig is None or adjusted is None:
            continue
        rows.append({
            "fixture_id": fid, "player_id": pid, "player_name": r.get("player"),
            "team": r.get("team"), "team_id": tid, "position": pos_label,
            "referee_name": ref_ctx.get("referee_name"),
            "probability_card_original": round(float(orig), 4),
            "probability_card_adjusted": round(float(adjusted), 4),
            "adjustment_direction": adj["adjustment_direction"],
            "abs_adjustment": round(abs(float(adjusted) - float(orig)), 4),
            "label_card": label,
            "confidence": adj["confidence"], "data_quality": adj["data_quality"],
        })
    return rows


# ============================================================ segmentation
def segment(rows, key_fn, min_n=SEG_MIN):
    """Group eval rows by key_fn(row) and compute a metric_block per group (n>=min_n flagged usable)."""
    groups = {}
    for r in rows:
        k = key_fn(r)
        if k is None or (isinstance(k, float) and pd.isna(k)):
            k = "no determinado"
        groups.setdefault(str(k), []).append(r)
    out = {}
    for k, grp in groups.items():
        mb = metric_block(grp)
        mb["usable"] = mb["n"] >= min_n
        mb["confidence"] = "baja" if mb["n"] < min_n else ("media-baja" if mb["n"] < MIN_SAMPLE else "media")
        out[k] = mb
    return out


def _referee_segment(rows):
    """Referees with >=REF_MIN_MATCHES distinct evaluated fixtures; 1-fixture refs flagged low-sample."""
    by_ref = {}
    for r in rows:
        by_ref.setdefault(r.get("referee_name") or "no determinado", []).append(r)
    out = {}
    for name, grp in by_ref.items():
        n_fix = len({r["fixture_id"] for r in grp})
        mb = metric_block(grp)
        mb["n_fixtures"] = n_fix
        mb["usable"] = n_fix >= REF_MIN_MATCHES and mb["n"] >= SEG_MIN
        mb["confidence"] = "baja" if n_fix < REF_MIN_MATCHES else ("media-baja" if mb["n"] < MIN_SAMPLE else "media")
        mb["reason"] = (f"{n_fix} partido(s) evaluados — muestra baja, no extrapolar"
                        if n_fix < REF_MIN_MATCHES else f"{n_fix} partidos evaluados")
        out[name] = mb
    return out


def _team_segment(rows):
    by_team = {}
    for r in rows:
        by_team.setdefault(r.get("team") or "no determinado", []).append(r)
    out = {}
    for name, grp in by_team.items():
        mb = metric_block(grp)
        mb["usable"] = mb["n"] >= TEAM_MIN_PREDS
        mb["confidence"] = "baja" if mb["n"] < TEAM_MIN_PREDS else ("media-baja" if mb["n"] < MIN_SAMPLE else "media")
        out[name] = mb
    return out


# ============================================================ recommendation (conservative)
def recommend(overall, segments):
    """Translate the measured deltas into a CONSERVATIVE recommendation. Never declares victory on a
    thin sample. Returns {verdict, weights, factor_referee, factor_position, factor_team, notes, ...}."""
    n = overall["n"]
    npos = overall["n_positive"]
    db, dl = overall["delta_brier"], overall["delta_logloss"]
    low_sample = n < MIN_SAMPLE
    few_positives = npos < 50

    if low_sample or db is None or dl is None:
        verdict = "muestra baja"
        weights = "no tocar nada — muestra insuficiente para concluir"
        result_word = "no concluyente"
    elif abs(db) < 1e-9 and abs(dl) < 1e-9:
        # exact no-op (e.g. card profiles not generated -> adjuster inert). NOT a worsening.
        verdict = "sin cambio (ajuste inerte: perfiles no disponibles o sin señal)"
        weights = "no tocar nada — el ajuste no se aplicó (revisar que existan los perfiles auto)"
        result_word = "sin cambio"
    else:
        improves_brier = db < 0
        improves_logloss = dl < 0
        if improves_brier and improves_logloss:
            verdict = "adjusted mejora ambas"
            weights = "mantener pesos actuales"
            result_word = "mejora marginal" if (abs(db) < 0.005 and abs(dl) < 0.02) else "mejora"
        elif (not improves_brier) and (not improves_logloss):
            verdict = "adjusted empeora ambas"
            weights = "bajar pesos (ajuste demasiado agresivo)"
            result_word = "empeora"
        else:
            verdict = "mixto (mejora una, empeora otra)"
            weights = "mantener pesos y vigilar; no subir agresividad"
            result_word = "mixto"

    # per-factor hints from the directional segments (subir/bajar). A direction that worsens Brier on a
    # usable sample suggests softening the factors that push that way. Conservative wording only.
    dirseg = segments.get("by_direction", {})
    factor_referee = factor_position = factor_team = "mantener (sin señal clara)"
    subir = dirseg.get("subir"); bajar = dirseg.get("bajar")
    if not low_sample:
        if subir and subir.get("usable") and (subir.get("delta_brier") or 0) > 0.002:
            factor_referee = "considerar bajar ligeramente (las subidas no mejoran)"
            factor_position = factor_team = "considerar bajar ligeramente (las subidas no mejoran)"
        elif subir and subir.get("usable") and (subir.get("delta_brier") or 0) < -0.002:
            factor_position = factor_team = "adecuados (las subidas ayudan)"
        if bajar and bajar.get("usable") and (bajar.get("delta_brier") or 0) > 0.002:
            factor_team = "revisar (las bajadas no mejoran)"

    # referee factor currently inert? (no populated referee profiles -> every fixture 'no determinado')
    refseg = segments.get("by_referee", {})
    ref_inactive = bool(refseg) and all(str(k).strip().lower() in ("no determinado", "none", "")
                                        for k in refseg)
    if ref_inactive:
        factor_referee = "inactivo — aún no hay perfiles de árbitro poblados (no aporta al ajuste)"

    notes = []
    if ref_inactive:
        notes.append("factor árbitro INACTIVO: worldcup_referee_profiles_auto sin perfiles utilizables "
                     "todavía; su contribución al ajuste es ~0 (no es un fallo, es falta de muestra).")
    if low_sample:
        notes.append(f"n_with_result={n} < {MIN_SAMPLE}: por debajo del umbral de muestra.")
    if few_positives:
        notes.append(f"solo {npos} eventos de tarjeta reales: la calibración de un evento poco frecuente "
                     "es ruidosa.")
    notes.append("perfiles auto acumulativos -> el adjusted tiene una ligera ventaja de look-ahead; "
                 "trata las mejoras como indicativas, no como veredicto.")
    return {
        "verdict": verdict, "result_word": result_word, "weights": weights,
        "factor_referee": factor_referee, "factor_position": factor_position, "factor_team": factor_team,
        "low_sample": low_sample, "few_positives": few_positives, "notes": notes,
    }


def _over_adjustment(rows):
    """Honest 'over-adjustment' signal: share of rows where the adjustment moved the probability FARTHER
    from the realised outcome than the original (per-row hindsight check)."""
    worse = same = 0
    for r in rows:
        do = abs(r["probability_card_original"] - r["label_card"])
        da = abs(r["probability_card_adjusted"] - r["label_card"])
        if da > do + 1e-9:
            worse += 1
        elif abs(da - do) <= 1e-9:
            same += 1
    moved = len(rows) - same
    return {"rows_moved": moved, "rows_worse_after_adjust": worse,
            "share_worse_of_moved": round(worse / moved, 4) if moved else None}


# ============================================================ build / I/O
def _confidence_for(n, npos):
    if n < MIN_SAMPLE:
        return "baja", "baja"
    if npos < 50:
        return "media-baja", "media-baja"
    return "media", "media"


def build(props_path=PROPS_LOG, card_profiles=None, write=True):
    if not Path(props_path).exists():
        payload = {"meta": {"error": "no props log"}, "overall": metric_block([]), "rows": 0}
        if write:
            pd.DataFrame(columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
            Path(OUT_JSON).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            Path(OUT_TXT).write_text("Sin props log; nada que evaluar.\n", encoding="utf-8")
        return payload

    props = pd.read_csv(props_path)
    settled = props[props.get("settled") == 1].copy() if "settled" in props.columns else props.iloc[0:0]

    if card_profiles is None:
        card_profiles, _ = cadj.load_card_profiles()
    pos_map, _ = adapters.load_positional_profiles()
    manual, manual_r = adapters.load_referee_profiles()
    auto, auto_r = refctx.load_auto_referee_profiles()
    fix_ref = {}
    if Path(FIXTURE_REFEREES).exists():
        try:
            rf = pd.read_csv(FIXTURE_REFEREES)
            fix_ref = {int(a): b for a, b in zip(rf["fixture_id"], rf["referee_name"])
                       if pd.notna(a) and isinstance(b, str)}
        except Exception:
            fix_ref = {}
    resolver = RefereeResolver(fix_ref, manual, manual_r, auto, auto_r)

    rows = build_evaluation_rows(settled, card_profiles, pos_map, resolver)
    overall = metric_block(rows)
    overall["over_adjustment"] = _over_adjustment(rows)
    conf, dq = _confidence_for(overall["n"], overall["n_positive"])
    overall["confidence"], overall["data_quality"] = conf, dq

    segments = {
        "by_position": segment(rows, lambda r: r.get("position")),
        "by_direction": segment(rows, lambda r: r.get("adjustment_direction")),
        "by_confidence": segment(rows, lambda r: r.get("confidence")),
        "by_referee": _referee_segment(rows),
        "by_team": _team_segment(rows),
    }
    rec = recommend(overall, segments)

    # consistency note: does the live JSON (upcoming fixtures) carry the adjuster fields? (no labels)
    live_note = _live_consistency_note()

    payload = {
        "meta": {
            "n_predictions": len(rows),
            "n_with_result": overall["n"],
            "min_sample": MIN_SAMPLE,
            "method": "adjusted reconstruido aplicando card_risk_adjuster a la p_card congelada (props "
                      "log settled) con los perfiles auto actuales — mismo transform que el producto.",
            "caveat_lookahead": "perfiles auto acumulativos: incluyen el partido evaluado (ligero "
                                "look-ahead); mejoras = indicativas, no veredicto.",
            "live_json": live_note,
        },
        "overall": overall,
        "calibration_original": calibration_bins(
            [r["probability_card_original"] for r in rows], [r["label_card"] for r in rows]),
        "calibration_adjusted": calibration_bins(
            [r["probability_card_adjusted"] for r in rows], [r["label_card"] for r in rows]),
        "segments": segments,
        "recommendation": rec,
    }
    if write:
        pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
        Path(OUT_JSON).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(OUT_TXT).write_text(render_txt(payload) + "\n", encoding="utf-8")
    return payload


def _live_consistency_note():
    p = Path(PLAYER_EVENTS_JSON)
    if not p.exists():
        return "worldcup_player_events.json no presente"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return "worldcup_player_events.json ilegible"
    n_fix = len(data)
    n_adj = sum(1 for o in data for c in o.get("player_predictions", {}).get("card_risk", [])
                if "probability_card_adjusted" in c)
    return (f"{n_fix} fixtures próximos (sin resultado todavía); {n_adj} entradas card_risk ya llevan "
            f"probability_card_adjusted (ajuste activo en producto)")


def render_txt(p) -> str:
    o = p["overall"]
    rec = p["recommendation"]
    L = ["===== WORLD CUP — EVALUACIÓN DEL AJUSTE DE RIESGO DE TARJETA (Fase 4G) =====", "",
         f"Predicciones evaluadas (con resultado): {o['n']}  ·  eventos de tarjeta reales: {o['n_positive']}"
         f"  ·  tasa real: {o['real_card_rate']}",
         f"Prob. media: original {o['avg_probability_original']} · ajustada {o['avg_probability_adjusted']}"
         f"  (ajuste medio |Δ| = {o['avg_abs_adjustment']})",
         "",
         "-- MÉTRICAS GLOBALES (menor = mejor) --",
         f"  Brier:    original {o['brier_original']} -> ajustada {o['brier_adjusted']}  (Δ {o['delta_brier']})",
         f"  LogLoss:  original {o['logloss_original']} -> ajustada {o['logloss_adjusted']}  (Δ {o['delta_logloss']})",
         f"  Sobre-ajuste: {o['over_adjustment']['rows_worse_after_adjust']} de "
         f"{o['over_adjustment']['rows_moved']} filas movidas empeoran "
         f"(share {o['over_adjustment']['share_worse_of_moved']})",
         f"  Confianza de la evaluación: {o['confidence']} (dq {o['data_quality']})", ""]

    def seg_lines(title, seg, extra=None):
        out = [f"-- {title} --"]
        for k, m in sorted(seg.items(), key=lambda kv: -kv[1]["n"]):
            tag = "" if m.get("usable") else "  [muestra baja]"
            out.append(f"  {k:>14}: n={m['n']:3d} real={m['real_card_rate']} "
                       f"ΔBrier={m['delta_brier']} ΔLogLoss={m['delta_logloss']}{tag}")
        return out

    L += seg_lines("POR POSICIÓN", p["segments"]["by_position"])
    L.append("")
    L += seg_lines("POR DIRECCIÓN DE AJUSTE", p["segments"]["by_direction"])
    L.append("")
    L += seg_lines("POR CONFIANZA", p["segments"]["by_confidence"])
    L.append("")
    L += seg_lines("POR ÁRBITRO (>=2 partidos usable)", p["segments"]["by_referee"])
    L.append("")
    # only show teams with enough preds, to avoid noise
    teams_usable = {k: m for k, m in p["segments"]["by_team"].items() if m.get("usable")}
    L += seg_lines("POR EQUIPO (>=3 predicciones)", teams_usable)
    L.append("")
    L += ["-- RECOMENDACIÓN (conservadora; MEDIR antes de tocar pesos) --",
          f"  Resultado: el ajuste {rec['result_word']} ({rec['verdict']}).",
          f"  Pesos: {rec['weights']}.",
          f"  Factor árbitro: {rec['factor_referee']}.",
          f"  Factor posición: {rec['factor_position']}.",
          f"  Factor equipo: {rec['factor_team']}."]
    for n in rec["notes"]:
        L.append(f"  · {n}")
    L.append("")
    L.append("Predicción futbolística pura, sin terminología de juego. NO se modifican pesos en esta fase "
             "(Fase 4G = medición). NO toca data/external.")
    return "\n".join(L)


def main():
    p = build()
    o = p["overall"]
    rec = p["recommendation"]
    print(f"card-risk eval: n={o['n']} pos={o['n_positive']} | "
          f"Brier {o['brier_original']}->{o['brier_adjusted']} (Δ{o['delta_brier']}) | "
          f"LogLoss {o['logloss_original']}->{o['logloss_adjusted']} (Δ{o['delta_logloss']})")
    print(f"  recomendación: {rec['weights']} ({rec['verdict']}; {rec['result_word']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
