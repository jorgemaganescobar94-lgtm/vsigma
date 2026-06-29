"""
WORLD CUP 2026 — CARD-RISK ADJUSTMENT NO-LOOK-AHEAD EVALUATION (Fase 4H). READ-ONLY · NO API · NO
scraping · NO web · NO market/odds/betting · NO fabrication · NO secrets. Pure football. MEASURE ONLY —
weights are NOT changed.

Re-runs the Fase-4G evaluation of the card-risk adjustment but REBUILDS the auto discipline profiles
WITHOUT future information, to test whether the marginal improvement seen in 4G survives once the
cumulative-profile look-ahead is removed.

Three modes, identical adjuster/lookup, differing ONLY in which events feed the profiles per fixture:
  * cumulative          — ALL events (= Fase-4G regime; carries look-ahead). Baseline for comparison.
  * pre_fixture         — only events from STRICTLY EARLIER match-days (date < the fixture's date).
                          The clean, anti-look-ahead estimate (small sample early in the tournament).
  * leave_one_fixture_out — all events EXCEPT the evaluated fixture's own (still uses later fixtures,
                          so LESS strict than pre_fixture; an auxiliary diagnostic).

Labelled set = settled rows of worldcup_player_props_log.csv (frozen p_card + act_card). Profiles are
rebuilt per cutoff from worldcup_fixture_events.csv with the SAME derivation as
build_worldcup_card_profiles_auto + build_worldcup_referee_profiles_auto (NO new sources, NO scraping).

Honest sample handling: pre_fixture is the strictest but thinnest; if its sample is below threshold the
report says so and does NOT declare a real improvement. A direction is neutral when there is no usable
prior history. We never claim a gain that only exists with look-ahead.

Outputs (CSV may be auto-committed; json+report gitignored — regenerable):
  * analysis/worldcup/worldcup_card_risk_no_lookahead_evaluation.csv   (one row per evaluated prediction)
  * analysis/worldcup/worldcup_card_risk_no_lookahead_summary.json
  * analysis/worldcup/worldcup_card_risk_no_lookahead_report.txt

Run:  python analysis/worldcup/evaluate_worldcup_card_risk_adjustment_no_lookahead.py
"""
from __future__ import annotations

import json
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
import build_worldcup_card_profiles_auto as cpa  # noqa: E402
import build_worldcup_referee_profiles_auto as refauto  # noqa: E402
import evaluate_worldcup_card_risk_adjustment as ev  # noqa: E402  (reuse metric/segment helpers)

PROPS_LOG = HERE / "worldcup_player_props_log.csv"
FIXTURE_EVENTS = HERE / "worldcup_fixture_events.csv"
FIXTURE_REFEREES = ROOT / "data" / "external" / "fixture_referees.csv"
OUT_CSV = HERE / "worldcup_card_risk_no_lookahead_evaluation.csv"
OUT_JSON = HERE / "worldcup_card_risk_no_lookahead_summary.json"
OUT_TXT = HERE / "worldcup_card_risk_no_lookahead_report.txt"

MIN_SAMPLE = ev.MIN_SAMPLE

CSV_COLUMNS = [
    "fixture_id", "player_id", "player_name", "team", "position", "referee_name",
    "p_original", "p_adjusted_pre_fixture", "p_adjusted_leave_one_out", "act_card",
    "adjustment_direction_pre_fixture", "adjustment_direction_leave_one_out", "confidence", "reason",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ profile indexing (in-memory, per cutoff)
def _index_profiles(player_list, team_list, position_list):
    players = {}
    for p in player_list:
        if p.get("player_id") is not None:
            players[int(p["player_id"])] = p
    teams = {}
    for t in team_list:
        if t.get("team_id") is not None:
            teams[int(t["team_id"])] = t
    positions = {(p.get("position") or "").strip().upper(): p for p in position_list
                 if (p.get("position") or "").strip()}
    return {"players": players, "teams": teams, "positions": positions}


def _referee_auto_dict(ref_profiles_list):
    """{referee_name_lower: profile} from derive_referee_profiles output (anti-look-ahead subset)."""
    out = {}
    for p in ref_profiles_list:
        name = str(p.get("referee_name") or "").strip()
        if name:
            out[name.lower()] = p
    return out


def build_profiles_from_events(events_subset, pos_map, referees_map):
    """Rebuild player/team/position/referee profiles from a SUBSET of events (the anti-look-ahead core).
    Returns (card_profiles_index, referee_auto_dict). Pure derivation — NO new sources, NO fabrication."""
    players = cpa.derive_player_profiles(events_subset, pos_map)
    teams = cpa.derive_team_profiles(events_subset)
    positions = cpa.derive_position_profiles(events_subset, pos_map)
    ref_list = refauto.derive_referee_profiles(referees_map, events_subset)
    return _index_profiles(players, teams, positions), _referee_auto_dict(ref_list)


# ============================================================ adjustment for one row given profiles
def _position_for(pid, player_prof, pos_map):
    """pos_map here is {player_id: position_str} (cpa.load_positions). Position is identity, not an
    outcome -> safe to use; no look-ahead."""
    if player_prof and player_prof.get("position"):
        return str(player_prof["position"]).strip().upper() or None
    if pid is not None and pos_map.get(pid):
        return str(pos_map[pid]).strip().upper() or None
    return None


def _adjust_with(cp_index, ref_auto_dict, p_card, pid, tid, ref_name, pos_map):
    players, teams, positions = cp_index["players"], cp_index["teams"], cp_index["positions"]
    player_prof = players.get(pid) if pid is not None else None
    pos_label = _position_for(pid, player_prof, pos_map)
    position_prof = positions.get(pos_label) if pos_label else None
    team_prof = teams.get(tid) if tid is not None else None
    ref_ctx = refctx.build_referee_context(ref_name, {}, "", ref_auto_dict, "")
    adj = cadj.adjust_card_risk(p_card, player_profile=player_prof, position_profile=position_prof,
                                team_profile=team_prof, referee_context=ref_ctx)
    return adj, pos_label, ref_ctx.get("referee_name")


# ============================================================ evaluation builder
def build_rows(settled_df, events_df, pos_map, referees_map):
    """For each settled prediction build original + adjusted under cumulative / pre_fixture /
    leave_one_out profile regimes. Profiles cached per fixture (all rows of a fixture share a cutoff)."""
    # fixture -> date (day). evaluated fixtures from props kickoff; event fixtures from events.date
    fix_date = {}
    if events_df is not None and len(events_df):
        for fid, grp in events_df.groupby("fixture_id"):
            d = str(grp["date"].iloc[0])[:10] if "date" in grp.columns and len(grp) else None
            try:
                fix_date[int(fid)] = d
            except Exception:
                pass
    for _, r in settled_df.iterrows():
        try:
            fid = int(r["fixture_id"])
        except Exception:
            continue
        ko = str(r.get("kickoff_utc") or "")[:10]
        if ko:
            fix_date[fid] = ko  # prefer the props kickoff day for evaluated fixtures

    # per-fixture profile caches (built once per fixture)
    cum_index, cum_ref = build_profiles_from_events(events_df, pos_map, referees_map)
    pre_cache, loo_cache = {}, {}

    def pre_profiles(fid):
        if fid not in pre_cache:
            d = fix_date.get(fid)
            if d and "date" in events_df.columns:
                sub = events_df[events_df["date"].astype(str).str[:10] < d]
            else:
                sub = events_df.iloc[0:0]
            pre_cache[fid] = build_profiles_from_events(sub, pos_map, referees_map)
        return pre_cache[fid]

    def loo_profiles(fid):
        if fid not in loo_cache:
            sub = events_df[events_df["fixture_id"].astype("Int64") != fid] if events_df is not None \
                else events_df
            loo_cache[fid] = build_profiles_from_events(sub, pos_map, referees_map)
        return loo_cache[fid]

    rows = []
    for _, r in settled_df.iterrows():
        p_card = r.get("p_card")
        if p_card is None or (isinstance(p_card, float) and pd.isna(p_card)):
            continue
        try:
            label = 1 if float(r.get("act_card") or 0) >= 1 else 0
            fid = int(r["fixture_id"])
        except Exception:
            continue
        pid = int(r["player_id"]) if pd.notna(r.get("player_id")) else None
        tid = int(r["team_id"]) if pd.notna(r.get("team_id")) else None
        ref_name = referees_map.get(fid)

        a_cum, pos_label, ref_disp = _adjust_with(cum_index, cum_ref, p_card, pid, tid, ref_name, pos_map)
        pre_idx, pre_ref = pre_profiles(fid)
        a_pre, _, _ = _adjust_with(pre_idx, pre_ref, p_card, pid, tid, ref_name, pos_map)
        loo_idx, loo_ref = loo_profiles(fid)
        a_loo, _, _ = _adjust_with(loo_idx, loo_ref, p_card, pid, tid, ref_name, pos_map)

        # pre_fixture history availability -> confidence/reason for the row
        has_pre_hist = bool(pre_idx["players"] or pre_idx["teams"])
        if not has_pre_hist:
            conf, reason = "baja", "sin historial previo al fixture (primeras jornadas) — ajuste neutro"
        else:
            conf, reason = a_pre["confidence"], "perfiles reconstruidos solo con jornadas anteriores"

        rows.append({
            "fixture_id": fid, "player_id": pid, "player_name": r.get("player"),
            "team": r.get("team"), "team_id": tid, "position": pos_label, "referee_name": ref_disp,
            "p_original": a_cum["probability_card_original"],
            "p_adjusted_cumulative": a_cum["probability_card_adjusted"],
            "p_adjusted_pre_fixture": a_pre["probability_card_adjusted"],
            "p_adjusted_leave_one_out": a_loo["probability_card_adjusted"],
            "act_card": label,
            "adjustment_direction_cumulative": a_cum["adjustment_direction"],
            "adjustment_direction_pre_fixture": a_pre["adjustment_direction"],
            "adjustment_direction_leave_one_out": a_loo["adjustment_direction"],
            "confidence": conf, "reason": reason,
        })
    return rows


# ============================================================ per-mode metrics / segments
def _mode_rows(rows, adj_key, dir_key):
    """Map eval rows to the shape ev.metric_block / ev.segment expect, for one mode."""
    return [{
        "fixture_id": r["fixture_id"], "player_id": r["player_id"], "player_name": r["player_name"],
        "team": r["team"], "team_id": r["team_id"], "position": r["position"],
        "referee_name": r["referee_name"],
        "probability_card_original": r["p_original"],
        "probability_card_adjusted": r[adj_key],
        "adjustment_direction": r[dir_key],
        "abs_adjustment": round(abs((r[adj_key] or 0) - (r["p_original"] or 0)), 4),
        "label_card": r["act_card"], "confidence": r["confidence"], "data_quality": r["confidence"],
    } for r in rows if r["p_original"] is not None and r[adj_key] is not None]


def _real_rate_by_direction(mrows):
    out = {}
    for d in ("subir", "bajar", "neutro"):
        grp = [r for r in mrows if r["adjustment_direction"] == d]
        pos = sum(1 for r in grp if r["label_card"] == 1)
        out[d] = {"n": len(grp), "n_positive": pos,
                  "real_card_rate": round(pos / len(grp), 4) if grp else None}
    return out


def _mode_summary(mrows):
    mb = ev.metric_block(mrows)
    mb["over_adjustment"] = ev._over_adjustment(mrows)
    mb["direction_counts"] = {d: sum(1 for r in mrows if r["adjustment_direction"] == d)
                              for d in ("subir", "bajar", "neutro")}
    mb["real_rate_by_direction"] = _real_rate_by_direction(mrows)
    mb["calibration_original"] = ev.calibration_bins(
        [r["probability_card_original"] for r in mrows], [r["label_card"] for r in mrows])
    mb["calibration_adjusted"] = ev.calibration_bins(
        [r["probability_card_adjusted"] for r in mrows], [r["label_card"] for r in mrows])
    mb["segments"] = {
        "by_direction": ev.segment(mrows, lambda r: r["adjustment_direction"]),
        "by_position": ev.segment(mrows, lambda r: r["position"]),
        "by_confidence": ev.segment(mrows, lambda r: r["confidence"]),
        "by_team": ev._team_segment(mrows),
        "by_referee": ev._referee_segment(mrows),
    }
    return mb


# ============================================================ comparison + recommendation
def _improves(mb):
    db, dl = mb.get("delta_brier"), mb.get("delta_logloss")
    if db is None or dl is None:
        return None
    if db < 0 and dl < 0:
        return "both"
    if db > 0 and dl > 0:
        return "neither"
    return "mixed"


# a Brier gain smaller than this (≈0.5% of the ~0.09 base rate) is noise, not a real improvement —
# even if its sign is negative. We do NOT declare a win on a negligible magnitude.
NEGLIGIBLE_BRIER = 0.0005


def recommend(cumulative, pre, loo):
    """Conservative recommendation comparing the 3 regimes (spec §6). NEVER claims a gain that only
    survives with look-ahead or whose magnitude collapses to noise; never concludes on a thin sample."""
    pre_n, loo_n = pre["n"], loo["n"]
    pre_imp, loo_imp, cum_imp = _improves(pre), _improves(loo), _improves(cumulative)
    pre_db = pre.get("delta_brier")
    cum_db = cumulative.get("delta_brier")
    notes, survives = [], None

    low_pre = pre_n < MIN_SAMPLE
    low_loo = loo_n < MIN_SAMPLE
    negligible = (pre_db is None) or abs(pre_db) < NEGLIGIBLE_BRIER
    # how much of the cumulative (4G) Brier gain survives without look-ahead
    shrink = None
    if cum_db is not None and pre_db is not None and cum_db < 0:
        shrink = round(max(0.0, pre_db) if pre_db >= 0 else (pre_db / cum_db), 3)  # fraction surviving

    if low_pre and low_loo:
        verdict = "muestra baja en ambos modos"
        weights = "no tocar nada — muestra insuficiente sin look-ahead"
    elif pre_imp == "both" and not negligible:
        verdict = "la mejora SE MANTIENE sin look-ahead (pre_fixture)"
        weights = "mantener pesos actuales"
        survives = True
    elif negligible and pre_imp != "neither":
        verdict = "la mejora se DESVANECE sin look-ahead (magnitud negligible)"
        weights = "congelar el ajuste como SHADOW y tratarlo como neutral; NO subir pesos"
        survives = False
    elif pre_imp == "neither":
        verdict = "el ajuste EMPEORA sin look-ahead (pre_fixture)"
        weights = "bajar pesos del ajuste (o congelar como shadow)"
        survives = False
    else:
        verdict = "señal no concluyente sin look-ahead"
        weights = "congelar como shadow; mantener medición"
        survives = False

    if cum_imp == "both" and survives is not True:
        pct = f" (sobrevive ≈{int((shrink or 0)*100)}%)" if shrink is not None else ""
        notes.append(f"la mejora de Fase 4G (acumulativo) era, en su mayor parte, look-ahead{pct}: "
                     "desaparece o se vuelve negligible al reconstruir perfiles sin información futura.")
    if negligible and not (low_pre and low_loo):
        notes.append(f"|ΔBrier| pre_fixture < {NEGLIGIBLE_BRIER} -> indistinguible de ruido; no se "
                     "declara mejora real.")
    if low_pre:
        notes.append(f"pre_fixture n={pre_n}: las jornadas evaluadas son las más recientes, así que "
                     "muchas filas tienen poco/ningún historial previo y quedan neutras.")
    notes.append("leave_one_out ≈ pre_fixture aquí: los fixtures evaluados son los más recientes del "
                 "dataset (apenas hay eventos posteriores), así que excluir-uno coincide casi con solo-previos.")
    return {"verdict": verdict, "weights": weights, "improvement_survives_no_lookahead": survives,
            "pre_fixture_improves": pre_imp, "leave_one_out_improves": loo_imp,
            "cumulative_improves": cum_imp, "negligible_pre_fixture": negligible,
            "fraction_of_4g_gain_surviving": shrink, "low_sample_pre_fixture": low_pre, "notes": notes}


# ============================================================ build / I/O
def build(props_path=PROPS_LOG, events_path=FIXTURE_EVENTS, write=True):
    if not Path(props_path).exists() or not Path(events_path).exists():
        payload = {"meta": {"error": "missing props log or events"}}
        if write:
            pd.DataFrame(columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
            Path(OUT_JSON).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            Path(OUT_TXT).write_text("Sin props log o eventos; nada que evaluar.\n", encoding="utf-8")
        return payload

    props = pd.read_csv(props_path)
    settled = props[props.get("settled") == 1].copy() if "settled" in props.columns else props.iloc[0:0]
    events = pd.read_csv(events_path)
    pos_map = cpa.load_positions()
    referees_map = refauto.load_fixture_referees(FIXTURE_REFEREES)

    rows = build_rows(settled, events, pos_map, referees_map)

    cum = _mode_summary(_mode_rows(rows, "p_adjusted_cumulative", "adjustment_direction_cumulative"))
    pre = _mode_summary(_mode_rows(rows, "p_adjusted_pre_fixture", "adjustment_direction_pre_fixture"))
    loo = _mode_summary(_mode_rows(rows, "p_adjusted_leave_one_out", "adjustment_direction_leave_one_out"))
    rec = recommend(cum, pre, loo)

    payload = {
        "meta": {
            "n_predictions": len(rows),
            "min_sample": MIN_SAMPLE,
            "method": "perfiles reconstruidos por fixture: cumulative=todos los eventos (4G, con "
                      "look-ahead); pre_fixture=solo jornadas anteriores (date < fixture); "
                      "leave_one_out=todos menos el propio fixture (menos estricto).",
        },
        "cumulative": cum, "pre_fixture": pre, "leave_one_fixture_out": loo,
        "recommendation": rec,
    }
    if write:
        pd.DataFrame([{c: r.get(c) for c in CSV_COLUMNS} for r in rows],
                     columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
        Path(OUT_JSON).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(OUT_TXT).write_text(render_txt(payload) + "\n", encoding="utf-8")
    return payload


def _mode_line(name, mb):
    return (f"  {name:18} n={mb['n']:3d} pos={mb['n_positive']:2d} | "
            f"Brier {mb['brier_original']}->{mb['brier_adjusted']} (Δ {mb['delta_brier']}) | "
            f"LogLoss {mb['logloss_original']}->{mb['logloss_adjusted']} (Δ {mb['delta_logloss']})")


def render_txt(p) -> str:
    rec = p["recommendation"]
    L = ["===== WORLD CUP — EVALUACIÓN ANTI-LOOK-AHEAD DEL AJUSTE DE TARJETA (Fase 4H) =====", "",
         f"Predicciones evaluadas: {p['meta']['n_predictions']}", "",
         "-- MÉTRICAS POR MODO (menor = mejor) --",
         _mode_line("cumulative (4G)", p["cumulative"]),
         _mode_line("pre_fixture", p["pre_fixture"]),
         _mode_line("leave_one_out", p["leave_one_fixture_out"]), ""]

    for label, key in (("PRE_FIXTURE", "pre_fixture"), ("LEAVE_ONE_OUT", "leave_one_fixture_out")):
        mb = p[key]
        rd = mb["real_rate_by_direction"]
        L.append(f"-- {label}: tasa real por dirección --")
        for d in ("subir", "bajar", "neutro"):
            L.append(f"    {d:7}: n={rd[d]['n']:3d} real={rd[d]['real_card_rate']}")
        # position segment deltas
        L.append(f"-- {label}: ΔBrier por posición --")
        for k, m in sorted(mb["segments"]["by_position"].items(), key=lambda kv: -kv[1]["n"]):
            tag = "" if m.get("usable") else "  [muestra baja]"
            L.append(f"    {k:>6}: n={m['n']:3d} ΔBrier={m['delta_brier']}{tag}")
        L.append("")

    L += ["-- COMPARACIÓN Y RECOMENDACIÓN (conservadora; pesos NO modificados) --",
          f"  4G acumulativo mejora: {rec['cumulative_improves']}",
          f"  4H pre_fixture mejora: {rec['pre_fixture_improves']}",
          f"  4H leave_one_out mejora: {rec['leave_one_out_improves']}",
          f"  Veredicto: {rec['verdict']}.",
          f"  ¿La mejora sobrevive sin look-ahead?: {rec['improvement_survives_no_lookahead']}",
          f"  Pesos: {rec['weights']}."]
    for n in rec["notes"]:
        L.append(f"  · {n}")
    L.append("")
    L.append("Predicción futbolística pura, sin terminología de juego. Fase 4H = medición anti-look-ahead; "
             "NO se modifican pesos. NO toca data/external.")
    return "\n".join(L)


def main():
    p = build()
    if "recommendation" not in p:
        print("no-lookahead eval: sin datos suficientes.")
        return 0
    pre, loo, rec = p["pre_fixture"], p["leave_one_fixture_out"], p["recommendation"]
    print(f"no-lookahead eval: pre_fixture n={pre['n']} ΔBrier={pre['delta_brier']} "
          f"ΔLogLoss={pre['delta_logloss']} | leave_one_out n={loo['n']} ΔBrier={loo['delta_brier']}")
    print(f"  veredicto: {rec['verdict']}")
    print(f"  pesos: {rec['weights']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
