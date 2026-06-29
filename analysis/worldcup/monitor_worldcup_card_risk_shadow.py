"""
WORLD CUP 2026 — CARD-RISK SHADOW MONITOR (Fase 4I). READ-ONLY inputs · NO API · NO scraping · NO web ·
NO market/odds/betting · NO fabrication · NO secrets. Pure football. WEIGHTS ARE NEVER CHANGED.

Turns the Fase-4F card-risk adjustment into a STABLE SHADOW MONITOR: it re-reads the 4G (cumulative) and
4H (anti-look-ahead) evaluations every run, classifies the adjustment into a clear state, and persists a
one-row-per-day time series so we can watch — automatically — whether the adjustment ever starts to add
REAL signal once there are more fixtures and more positive card events.

It does NOT touch weights and does NOT promote the adjustment. The only gate that could ever justify a
future weight change, `should_adjust_weights`, returns False unless STRICT conditions are met (and they
are not, today).

Inputs (read-only; each optional -> degrades to low confidence + reason, never fabricated):
  * analysis/worldcup/worldcup_card_risk_evaluation.csv            (4G: original + cumulative-adjusted)
  * analysis/worldcup/worldcup_card_risk_no_lookahead_evaluation.csv (4H: original + pre_fixture-adjusted)
  * analysis/worldcup/worldcup_card_risk_no_lookahead_summary.json  (4H summary; fraction surviving)
  * analysis/worldcup/worldcup_player_props_log.csv                 (cross-check of evaluated count)

Outputs:
  * analysis/worldcup/worldcup_card_risk_shadow_monitor.csv   (time series: one row per UTC day)
  * analysis/worldcup/worldcup_card_risk_shadow_monitor.json  (current snapshot + state + gate)
  * analysis/worldcup/worldcup_card_risk_shadow_monitor_report.txt

Run:  python analysis/worldcup/monitor_worldcup_card_risk_shadow.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import evaluate_worldcup_card_risk_adjustment as ev  # noqa: E402  (reuse brier/logloss helpers)

EVAL_4G_CSV = HERE / "worldcup_card_risk_evaluation.csv"
EVAL_4H_CSV = HERE / "worldcup_card_risk_no_lookahead_evaluation.csv"
SUMMARY_4H_JSON = HERE / "worldcup_card_risk_no_lookahead_summary.json"
PROPS_LOG = HERE / "worldcup_player_props_log.csv"
OUT_CSV = HERE / "worldcup_card_risk_shadow_monitor.csv"
OUT_JSON = HERE / "worldcup_card_risk_shadow_monitor.json"
OUT_TXT = HERE / "worldcup_card_risk_shadow_monitor_report.txt"

# ----- thresholds for the state machine (spec §3) and the safety gate (§4). Conservative on purpose. -----
MIN_POSITIVES_SAMPLE = 30        # below -> INSUFFICIENT_SAMPLE
MIN_N_SAMPLE = 100               # below -> INSUFFICIENT_SAMPLE
KEEP_WEAK_POSITIVES = 75         # KEEP_WEAK needs at least this many positives
RECAL_POSITIVES = 100            # CONSIDER_RECALIBRATION / weight-change gate need this many
NEGLIGIBLE_BRIER = 0.0005        # |ΔBrier| below this is noise (same as Fase 4H)
MATERIAL_BRIER = 0.0020          # a "material" Brier gain (≈2% of the ~0.09 base)
MATERIAL_LOGLOSS = 0.0050        # a "material" LogLoss gain
DIRECTION_SEP_MIN = 0.05         # real_rate(subir) - real_rate(bajar) needed for a "clear" separation
MIN_FRACTION_SURVIVING = 0.50    # fraction of the 4G gain that must survive without look-ahead

CSV_COLUMNS = [
    "date_utc", "logged_at_utc", "state", "recommended_mode", "should_adjust_weights",
    "evaluated_predictions", "positive_cards", "card_rate_real",
    "brier_original", "brier_adjusted_cumulative", "brier_adjusted_pre_fixture",
    "delta_brier_cumulative", "delta_brier_pre_fixture",
    "logloss_original", "logloss_adjusted_cumulative", "logloss_adjusted_pre_fixture",
    "delta_logloss_cumulative", "delta_logloss_pre_fixture",
    "fraction_of_4g_gain_surviving", "average_adjustment_size",
    "count_subir", "count_bajar", "count_neutro",
    "real_rate_subir", "real_rate_bajar", "real_rate_neutro", "verdict",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_csv(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df if len(df) else None


def _real_rates_by_direction(df, dir_col, label_col):
    out = {}
    for d in ("subir", "bajar", "neutro"):
        grp = df[df[dir_col].astype(str) == d]
        pos = int((pd.to_numeric(grp[label_col], errors="coerce").fillna(0) >= 1).sum())
        out[d] = {"n": len(grp), "real": round(pos / len(grp), 4) if len(grp) else None}
    return out


def _round(v, nd=5):
    return None if v is None else round(float(v), nd)


# ============================================================ metric collection (read-only)
def collect_metrics(eval_4g=EVAL_4G_CSV, eval_4h=EVAL_4H_CSV, summary_4h=SUMMARY_4H_JSON,
                    props=PROPS_LOG):
    """Build the monitored metrics dict from the 4G + 4H evaluation artifacts. Missing source -> the
    affected fields are None and a reason is recorded; NEVER fabricated."""
    reasons = []
    g = _read_csv(eval_4g)
    h = _read_csv(eval_4h)

    m = {k: None for k in (
        "evaluated_predictions", "positive_cards", "card_rate_real",
        "brier_original", "brier_adjusted_cumulative", "brier_adjusted_pre_fixture",
        "delta_brier_cumulative", "delta_brier_pre_fixture",
        "logloss_original", "logloss_adjusted_cumulative", "logloss_adjusted_pre_fixture",
        "delta_logloss_cumulative", "delta_logloss_pre_fixture",
        "fraction_of_4g_gain_surviving", "average_adjustment_size",
        "count_subir", "count_bajar", "count_neutro",
        "real_rate_subir", "real_rate_bajar", "real_rate_neutro")}

    # ----- cumulative (4G) -----
    if g is not None and {"probability_card_original", "probability_card_adjusted",
                          "label_card"} <= set(g.columns):
        y = g["label_card"].tolist()
        m["evaluated_predictions"] = len(g)
        m["positive_cards"] = int((pd.to_numeric(g["label_card"], errors="coerce").fillna(0) >= 1).sum())
        m["card_rate_real"] = _round(m["positive_cards"] / len(g) if len(g) else None, 4)
        bo = ev.brier_score(g["probability_card_original"], y)
        bc = ev.brier_score(g["probability_card_adjusted"], y)
        lo = ev.log_loss(g["probability_card_original"], y)
        lc = ev.log_loss(g["probability_card_adjusted"], y)
        m["brier_original"] = _round(bo)
        m["brier_adjusted_cumulative"] = _round(bc)
        m["delta_brier_cumulative"] = _round((bc - bo) if (bo is not None and bc is not None) else None)
        m["logloss_original"] = _round(lo)
        m["logloss_adjusted_cumulative"] = _round(lc)
        m["delta_logloss_cumulative"] = _round((lc - lo) if (lo is not None and lc is not None) else None)
    else:
        reasons.append("evaluación 4G (acumulativa) ausente o sin columnas esperadas")

    # ----- pre_fixture (4H) -----
    if h is not None and {"p_original", "p_adjusted_pre_fixture", "act_card",
                          "adjustment_direction_pre_fixture"} <= set(h.columns):
        y = (pd.to_numeric(h["act_card"], errors="coerce").fillna(0) >= 1).astype(int).tolist()
        if m["evaluated_predictions"] is None:
            m["evaluated_predictions"] = len(h)
            m["positive_cards"] = int(sum(y))
            m["card_rate_real"] = _round(sum(y) / len(y) if y else None, 4)
        bo = ev.brier_score(h["p_original"], y)
        bp = ev.brier_score(h["p_adjusted_pre_fixture"], y)
        lo = ev.log_loss(h["p_original"], y)
        lp = ev.log_loss(h["p_adjusted_pre_fixture"], y)
        if m["brier_original"] is None:
            m["brier_original"] = _round(bo)
            m["logloss_original"] = _round(lo)
        m["brier_adjusted_pre_fixture"] = _round(bp)
        m["delta_brier_pre_fixture"] = _round((bp - bo) if (bo is not None and bp is not None) else None)
        m["logloss_adjusted_pre_fixture"] = _round(lp)
        m["delta_logloss_pre_fixture"] = _round((lp - lo) if (lo is not None and lp is not None) else None)
        m["average_adjustment_size"] = _round(
            (h["p_adjusted_pre_fixture"] - h["p_original"]).abs().mean(), 4)
        dc = h["adjustment_direction_pre_fixture"].astype(str).value_counts().to_dict()
        m["count_subir"] = int(dc.get("subir", 0))
        m["count_bajar"] = int(dc.get("bajar", 0))
        m["count_neutro"] = int(dc.get("neutro", 0))
        rr = _real_rates_by_direction(h, "adjustment_direction_pre_fixture", "act_card")
        m["real_rate_subir"] = rr["subir"]["real"]
        m["real_rate_bajar"] = rr["bajar"]["real"]
        m["real_rate_neutro"] = rr["neutro"]["real"]
    else:
        reasons.append("evaluación 4H (pre_fixture) ausente o sin columnas esperadas")

    # ----- fraction of 4G gain surviving: prefer the 4H summary, else compute from deltas -----
    frac = None
    sp = Path(summary_4h)
    if sp.exists():
        try:
            s = json.loads(sp.read_text(encoding="utf-8"))
            frac = s.get("recommendation", {}).get("fraction_of_4g_gain_surviving")
        except Exception:
            frac = None
    if frac is None:
        dbc, dbp = m["delta_brier_cumulative"], m["delta_brier_pre_fixture"]
        if dbc is not None and dbp is not None and dbc < 0:
            frac = round(max(0.0, dbp) if dbp >= 0 else dbp / dbc, 3)
    m["fraction_of_4g_gain_surviving"] = frac

    # ----- cross-check evaluated count vs props settled (diagnostic only) -----
    pl = _read_csv(props)
    if pl is not None and "settled" in pl.columns:
        settled = int((pd.to_numeric(pl["settled"], errors="coerce").fillna(0) == 1).sum())
        m["props_settled_rows"] = settled
    return m, reasons


# ============================================================ state machine (spec §3)
def _improves_both(db, dl):
    return db is not None and dl is not None and db < 0 and dl < 0


def _worsens_both(db, dl):
    return db is not None and dl is not None and db > 0 and dl > 0


def _negligible(db):
    return db is None or abs(db) < NEGLIGIBLE_BRIER


def _material(db, dl):
    return (db is not None and dl is not None and db <= -MATERIAL_BRIER and dl <= -MATERIAL_LOGLOSS)


def _direction_separation_clear(m):
    rs, rb = m.get("real_rate_subir"), m.get("real_rate_bajar")
    if rs is None or rb is None:
        return False
    return (rs - rb) >= DIRECTION_SEP_MIN


def _direction_contrary(m):
    """Adjustment points the WRONG way: players pushed UP get cards LESS than players pushed DOWN."""
    rs, rb = m.get("real_rate_subir"), m.get("real_rate_bajar")
    if rs is None or rb is None or m.get("count_subir", 0) < 10 or m.get("count_bajar", 0) < 10:
        return False
    return rs < rb


def classify_state(m):
    """Return (state, recommended_mode, verdict, reason). Conservative; never promotes on a thin sample
    or a negligible/look-ahead-only gain. recommended_mode == state (one of the 5 labels)."""
    n = m.get("evaluated_predictions") or 0
    pos = m.get("positive_cards") or 0
    dbp, dlp = m.get("delta_brier_pre_fixture"), m.get("delta_logloss_pre_fixture")
    frac = m.get("fraction_of_4g_gain_surviving")

    if pos < MIN_POSITIVES_SAMPLE or n < MIN_N_SAMPLE:
        state = "INSUFFICIENT_SAMPLE"
        verdict = "muestra insuficiente para evaluar el ajuste sin look-ahead"
        reason = f"positivos={pos} (<{MIN_POSITIVES_SAMPLE}) o n={n} (<{MIN_N_SAMPLE})"
    elif _worsens_both(dbp, dlp) or _direction_contrary(m):
        state = "REDUCE_OR_DISABLE"
        verdict = "el ajuste empeora o va en dirección contraria sin look-ahead"
        reason = (f"pre_fixture ΔBrier={dbp} ΔLogLoss={dlp}; "
                  f"real subir={m.get('real_rate_subir')} vs bajar={m.get('real_rate_bajar')}")
    elif (_improves_both(dbp, dlp) and pos >= RECAL_POSITIVES and _material(dbp, dlp)
          and _direction_separation_clear(m)
          and frac is not None and frac >= MIN_FRACTION_SURVIVING):
        state = "CONSIDER_RECALIBRATION"
        verdict = "mejora material y estable sin look-ahead — candidata a recalibración (con revisión)"
        reason = (f"positivos={pos}, pre_fixture ΔBrier={dbp} ΔLogLoss={dlp}, "
                  f"separación subir-bajar clara, sobrevive {frac}")
    elif (_improves_both(dbp, dlp) and pos >= KEEP_WEAK_POSITIVES and not _negligible(dbp)
          and not _direction_contrary(m)):
        state = "KEEP_WEAK"
        verdict = "mejora leve pero consistente sin look-ahead — mantener como señal débil"
        reason = f"positivos={pos}, pre_fixture ΔBrier={dbp} ΔLogLoss={dlp} (no negligible)"
    else:
        state = "SHADOW_NEUTRAL"
        if _negligible(dbp):
            why = "la mejora pre_fixture es negligible (indistinguible de ruido)"
        elif pos < KEEP_WEAK_POSITIVES:
            why = f"solo {pos} positivos (<{KEEP_WEAK_POSITIVES})"
        else:
            why = "la mejora no es consistente/material sin look-ahead"
        verdict = "ajuste como shadow neutral — no aporta señal real todavía"
        reason = why + (f"; sobrevive {frac} de la ganancia 4G" if frac is not None else "")
    return state, state, verdict, reason


# ============================================================ safety gate (spec §4)
def should_adjust_weights(summary) -> bool:
    """Returns True ONLY under STRICT conditions: enough positives, a material AND surviving improvement
    without look-ahead, and a stable direction signal. False in every other case (and today)."""
    m = summary.get("metrics", summary) if isinstance(summary, dict) else {}
    pos = m.get("positive_cards") or 0
    dbp, dlp = m.get("delta_brier_pre_fixture"), m.get("delta_logloss_pre_fixture")
    frac = m.get("fraction_of_4g_gain_surviving")
    return bool(
        pos >= RECAL_POSITIVES
        and _improves_both(dbp, dlp)
        and _material(dbp, dlp)
        and _direction_separation_clear(m)
        and frac is not None and frac >= MIN_FRACTION_SURVIVING
    )


# ============================================================ persistence (time series) + report
def _append_timeseries(row, path=OUT_CSV):
    """Upsert one row per UTC day (keeps a clean stability time series). Existing same-day row replaced."""
    existing = _read_csv(path)
    rows = []
    if existing is not None:
        for c in CSV_COLUMNS:
            if c not in existing.columns:
                existing[c] = None
        rows = [r for r in existing[CSV_COLUMNS].to_dict("records")
                if str(r.get("date_utc")) != row["date_utc"]]
    rows.append({c: row.get(c) for c in CSV_COLUMNS})
    pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(path, index=False)


def render_txt(snapshot) -> str:
    m = snapshot["metrics"]
    L = ["🟨 Card Risk Shadow Monitor (Fase 4I — predicción futbolística pura)", "",
         f"Estado: {snapshot['state']}",
         f"Motivo: {snapshot['reason']}",
         f"Acción: {snapshot['action']}", "",
         "-- Métricas (menor Brier/LogLoss = mejor) --",
         f"  Evaluadas: {m['evaluated_predictions']} · positivos: {m['positive_cards']} · "
         f"tasa real: {m['card_rate_real']}",
         f"  Brier: original {m['brier_original']} · acumulado {m['brier_adjusted_cumulative']} "
         f"(Δ {m['delta_brier_cumulative']}) · pre_fixture {m['brier_adjusted_pre_fixture']} "
         f"(Δ {m['delta_brier_pre_fixture']})",
         f"  LogLoss: original {m['logloss_original']} · acumulado {m['logloss_adjusted_cumulative']} "
         f"(Δ {m['delta_logloss_cumulative']}) · pre_fixture {m['logloss_adjusted_pre_fixture']} "
         f"(Δ {m['delta_logloss_pre_fixture']})",
         f"  Ganancia 4G que sobrevive sin look-ahead: {m['fraction_of_4g_gain_surviving']}",
         f"  Ajuste medio: {m['average_adjustment_size']} · "
         f"subir={m['count_subir']} bajar={m['count_bajar']} neutro={m['count_neutro']}",
         f"  Tasa real por dirección: subir={m['real_rate_subir']} bajar={m['real_rate_bajar']} "
         f"neutro={m['real_rate_neutro']}", "",
         f"¿Recalibrar pesos? -> should_adjust_weights = {snapshot['should_adjust_weights']}",
         f"Confianza: {snapshot['confidence']}", "",
         "Predicción futbolística pura, sin terminología de juego. Pesos NO modificados; ajuste en modo "
         "shadow. NO toca data/external."]
    return "\n".join(L)


_ACTION = {
    "SHADOW_NEUTRAL": "mantener pesos, no recalibrar (seguir midiendo en shadow)",
    "KEEP_WEAK": "mantener pesos; el ajuste se conserva como señal débil (sin promover)",
    "CONSIDER_RECALIBRATION": "NO recalibrar automáticamente; abrir revisión manual de pesos (gate humano)",
    "REDUCE_OR_DISABLE": "revisar/reducir el ajuste (propuesta manual; pesos NO se tocan aquí)",
    "INSUFFICIENT_SAMPLE": "mantener pesos, seguir acumulando muestra",
}


def build(write=True):
    m, reasons = collect_metrics()
    state, mode, verdict, reason = classify_state(m)
    pos = m.get("positive_cards") or 0
    n = m.get("evaluated_predictions") or 0
    confidence = "baja" if (pos < KEEP_WEAK_POSITIVES or n < MIN_N_SAMPLE) else "media"
    gate = should_adjust_weights({"metrics": m})
    snapshot = {
        "logged_at_utc": now_iso(),
        "date_utc": now_iso()[:10],
        "state": state, "recommended_mode": mode, "verdict": verdict, "reason": reason,
        "action": _ACTION.get(state, "mantener pesos"),
        "should_adjust_weights": gate, "confidence": confidence,
        "source_reasons": reasons, "metrics": m,
    }
    if write:
        row = {"date_utc": snapshot["date_utc"], "logged_at_utc": snapshot["logged_at_utc"],
               "state": state, "recommended_mode": mode, "should_adjust_weights": gate,
               "verdict": verdict, **{k: m.get(k) for k in CSV_COLUMNS if k in m}}
        _append_timeseries(row, OUT_CSV)
        Path(OUT_JSON).write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(OUT_TXT).write_text(render_txt(snapshot) + "\n", encoding="utf-8")
    return snapshot


def main():
    s = build()
    print(f"card-risk shadow monitor: state={s['state']} | should_adjust_weights={s['should_adjust_weights']}")
    print(f"  motivo: {s['reason']}")
    print(f"  acción: {s['action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
