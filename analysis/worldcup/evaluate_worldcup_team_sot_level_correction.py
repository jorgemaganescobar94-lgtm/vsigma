"""
WORLD CUP 2026 — TEAM SOT LEVEL-CORRECTION EVALUATOR (Fase 4M). SHADOW / DISPLAY-ONLY · READ-ONLY ·
NO API · NO scraping · NO web · NO market/odds/betting · NO fabrication · NO secrets · NO external
sources. Pure football. EVALUATE ONLY — NOTHING is applied: the base model, lam_shot_on, the player
model, the predictions and Telegram are NOT touched. No weights change. No base prediction is replaced.

CONTEXT (Fase 4L finding): the team SOT prediction (Σ player λ_sot) OVER-predicts the real team SOT
(bias +1.75; mean pred 4.40 vs real 2.66). This module *measures* whether a simple level correction
applied to the SHOWN/predicted SOT would reduce that bias/MAE — and, critically, whether the gain
survives an ANTI-LOOK-AHEAD (online) test. It recommends only; it never activates a correction.

CANDIDATE CORRECTIONS (all shadow):
  A) global_ratio   : corrected = pred * (mean_actual / mean_pred)
  B) global_bias    : corrected = max(0, pred - mean(pred - actual))
  C) home_away_ratio: corrected = pred * ratio_side  (per side; global-ratio fallback if side sample < MIN_SIDE_ROWS)
  D) team_ratio     : corrected = pred * ratio_team  (only teams with >= MIN_TEAM_FIXTURES; else global-ratio fallback)
  E) clip           : every corrected value clamped to >= 0 (corrections shrink the over-prediction, so no
                      upper cap is invented; outliers are not fabricated).

ANTI-LOOK-AHEAD (decisive over cumulative):
  pre_fixture       : chronological. For each fixture, the global ratio is fit from STRICTLY EARLIER
                      fixtures only and applied to the current one. With < MIN_HISTORY_ROWS of history
                      the original value is kept (confidence baja). This is the honest "would it have
                      helped live?" test.
  leave_one_fixture_out : diagnostic only (less strict — it peeks at later fixtures): fit the ratio
                      excluding the evaluated fixture's own rows, apply to it.

RECOMMENDATION (conservative thresholds; pre_fixture overrides cumulative):
  CONSIDER_DISPLAY_CORRECTION : pre_fixture improves MAE >= DELTA_MAE_MATERIAL and RMSE, moves |bias|
                                toward 0 without strong inversion, AND n_team_rows >= N_MIN_ACTIVATE.
  SHADOW_ONLY                 : a real improvement exists (cumulative and/or pre_fixture) but the sample
                                is below N_MIN_ACTIVATE -> keep measuring, do not activate.
  REDUCE_AGGRESSIVENESS       : the correction WORSENS MAE (over-correction).
  NO_CHANGE                   : no material improvement / insufficient sample and no signal.

OUTPUT (read-only; explicit git-add only):
  * worldcup_team_sot_level_correction.csv        (per team/fixture: original + each corrected value)
  * worldcup_team_sot_level_correction_summary.json (metrics + recommendation; regenerable -> gitignored)
  * worldcup_team_sot_level_correction_report.txt   (human report, no betting language; regenerable -> gitignored)

Run:  python analysis/worldcup/evaluate_worldcup_team_sot_level_correction.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent

SOT_SCORECARD = HERE / "worldcup_team_sot_scorecard.csv"
OUT_CSV = HERE / "worldcup_team_sot_level_correction.csv"
OUT_JSON = HERE / "worldcup_team_sot_level_correction_summary.json"
OUT_TXT = HERE / "worldcup_team_sot_level_correction_report.txt"

# ---- conservative thresholds (governance) ----
N_MIN_ACTIVATE = 50          # below this no correction may even be CONSIDERED for activation
DELTA_MAE_MATERIAL = 0.15    # a MAE drop must be at least this to count as material
MIN_SIDE_ROWS = 10           # per-side ratio needs this many rows, else global fallback
MIN_TEAM_FIXTURES = 3        # per-team ratio needs this many rows, else global fallback
MIN_HISTORY_ROWS = 6         # pre_fixture needs this many earlier rows to fit a ratio, else keep original

CSV_COLUMNS = [
    "fixture_id", "kickoff_utc", "team_id", "team_name", "opponent_id", "opponent_name", "side",
    "predicted_sot_original", "actual_sot",
    "corrected_sot_global_ratio", "corrected_sot_global_bias", "corrected_sot_home_away_ratio",
    "corrected_sot_pre_fixture", "corrected_sot_leave_one_out",
    "error_original", "error_corrected_pre_fixture",
    "abs_error_original", "abs_error_corrected_pre_fixture",
    "correction_mode", "data_quality", "confidence", "reason",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _num(v):
    try:
        if v is None or v == "":
            return None
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if (f == f and f not in (float("inf"), float("-inf"))) else None


# ===================================================================== load evaluable rows
def load_evaluable(scorecard_path=SOT_SCORECARD):
    """Read the Fase-4L scorecard and return the chronologically sorted evaluable rows (both
    predicted_sot and actual_sot present) as a DataFrame with float pred/act columns. Empty -> empty
    DataFrame. Pure read; no fabrication."""
    p = Path(scorecard_path)
    if not p.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(p)
    except Exception:
        return pd.DataFrame()
    if not {"predicted_sot", "actual_sot"} <= set(df.columns):
        return pd.DataFrame()
    df = df.copy()
    df["pred"] = df["predicted_sot"].map(_num)
    df["act"] = df["actual_sot"].map(_num)
    ev = df[df["pred"].notna() & df["act"].notna()].copy()
    if not len(ev):
        return ev
    # stable chronological order; empty kickoff sorts first but evaluable rows always carry one
    ev["kickoff_utc"] = ev["kickoff_utc"].fillna("")
    ev = ev.sort_values(["kickoff_utc", "fixture_id", "team_id"]).reset_index(drop=True)
    return ev


# ===================================================================== metric helpers (pure)
def _metrics(pred, act):
    pred = np.asarray(pred, dtype=float)
    act = np.asarray(act, dtype=float)
    if len(pred) == 0:
        return {"n": 0, "mae": None, "rmse": None, "bias": None,
                "overprediction_rows": 0, "underprediction_rows": 0, "correlation": None}
    err = pred - act
    corr = None
    if len(pred) >= 3 and np.std(pred) > 1e-12 and np.std(act) > 1e-12:
        corr = round(float(np.corrcoef(pred, act)[0, 1]), 4)
    return {
        "n": int(len(pred)),
        "mae": round(float(np.mean(np.abs(err))), 4),
        "rmse": round(float(np.sqrt(np.mean(err ** 2))), 4),
        "bias": round(float(np.mean(err)), 4),
        "overprediction_rows": int(np.sum(err > 0)),
        "underprediction_rows": int(np.sum(err < 0)),
        "correlation": corr,
    }


def _clip0(arr):
    """Clip E): corrected SOT cannot be negative. No upper cap invented (corrections shrink)."""
    return np.maximum(0.0, np.asarray(arr, dtype=float))


# ===================================================================== fit corrections
def fit_global_ratio(pred, act):
    mp = float(np.mean(pred))
    return (float(np.mean(act)) / mp) if mp > 1e-12 else 1.0


def fit_global_bias(pred, act):
    return float(np.mean(np.asarray(pred, float) - np.asarray(act, float)))


def fit_side_ratios(ev, global_ratio):
    """{side: ratio}. A side with fewer than MIN_SIDE_ROWS falls back to the global ratio."""
    out = {}
    for side, g in ev.groupby("side"):
        if len(g) >= MIN_SIDE_ROWS:
            out[side] = fit_global_ratio(g["pred"].values, g["act"].values)
        else:
            out[side] = global_ratio
    return out


def fit_team_ratios(ev, global_ratio):
    """{team_id: ratio}. A team with fewer than MIN_TEAM_FIXTURES rows falls back to the global ratio."""
    out = {}
    for tid, g in ev.groupby("team_id"):
        if len(g) >= MIN_TEAM_FIXTURES:
            out[int(tid)] = fit_global_ratio(g["pred"].values, g["act"].values)
        else:
            out[int(tid)] = global_ratio
    return out


# ===================================================================== anti-look-ahead
def pre_fixture_correction(ev):
    """ONLINE global-ratio correction: for each fixture in chronological order, fit the ratio from
    STRICTLY EARLIER fixtures and apply it to the current fixture. < MIN_HISTORY_ROWS earlier rows ->
    keep the original (no fabrication). Returns (corrected_array_aligned_to_ev_index, modes, confs).
    Never uses the current or any future fixture."""
    corrected = np.array(ev["pred"].values, dtype=float)   # default = original (kept)
    modes = ["pre_fixture_kept_original"] * len(ev)
    confs = ["baja"] * len(ev)
    # fixtures in time order
    fix_order = (ev.drop_duplicates("fixture_id")
                   .sort_values(["kickoff_utc", "fixture_id"])["fixture_id"].tolist())
    for fid in fix_order:
        hist = ev[ev["fixture_id"].isin(fix_order[:fix_order.index(fid)])]
        cur_idx = ev.index[ev["fixture_id"] == fid].tolist()
        if len(hist) >= MIN_HISTORY_ROWS and float(np.sum(hist["pred"].values)) > 1e-12:
            ratio = fit_global_ratio(hist["pred"].values, hist["act"].values)
            for i in cur_idx:
                corrected[i] = max(0.0, float(ev.at[i, "pred"]) * ratio)
                modes[i] = "pre_fixture_applied"
                confs[i] = "media"
    return corrected, modes, confs


def leave_one_fixture_out_correction(ev):
    """DIAGNOSTIC (less strict): for each fixture, fit the global ratio EXCLUDING that fixture's own
    rows (but using every other fixture, incl. later ones) and apply it. Returns corrected array."""
    corrected = np.array(ev["pred"].values, dtype=float)
    for fid in ev["fixture_id"].unique():
        rest = ev[ev["fixture_id"] != fid]
        if len(rest) and float(np.sum(rest["pred"].values)) > 1e-12:
            ratio = fit_global_ratio(rest["pred"].values, rest["act"].values)
            for i in ev.index[ev["fixture_id"] == fid].tolist():
                corrected[i] = max(0.0, float(ev.at[i, "pred"]) * ratio)
    return corrected


# ===================================================================== recommendation
def recommend(summary):
    """Conservative recommendation. pre_fixture overrides cumulative. Returns (rec, reason)."""
    n = summary["n_team_rows"]
    orig = summary["original"]
    if n == 0 or orig["mae"] is None:
        return "NO_CHANGE", "sin filas evaluables todavía."
    pf = summary["anti_look_ahead"]["pre_fixture"]
    # matched-subset deltas (only rows pre_fixture actually corrected) — the honest online comparison
    d_mae = pf.get("delta_mae_on_corrected")
    d_rmse = pf.get("delta_rmse_on_corrected")
    bias_o = pf.get("bias_original_on_corrected")
    bias_c = pf.get("bias_corrected_on_corrected")
    # cumulative best improvement (any method) — used only to detect "signal exists but online fails"
    cum_best = max((m["delta_mae"] for m in summary["cumulative"].values()
                    if m["delta_mae"] is not None), default=0.0)

    # worsening guard: pre_fixture (or every cumulative method) increases MAE
    if d_mae is not None and d_mae < -1e-9 and cum_best <= 1e-9:
        return ("REDUCE_AGGRESSIVENESS",
                "la corrección EMPEORA el MAE (sobre-corrección); reducir agresividad o no aplicar.")

    bias_better = (bias_o is not None and bias_c is not None and abs(bias_c) < abs(bias_o) - 1e-9)
    strong_inversion = (bias_o is not None and bias_c is not None
                        and (bias_o == 0 or (bias_c * bias_o < 0)) and abs(bias_c) > 0.5 * abs(bias_o or 0) + 1e-9)
    pf_material = (d_mae is not None and d_mae >= DELTA_MAE_MATERIAL
                   and d_rmse is not None and d_rmse > 0 and bias_better and not strong_inversion)

    if pf_material and n >= N_MIN_ACTIVATE:
        return ("CONSIDER_DISPLAY_CORRECTION",
                f"pre_fixture mejora MAE {d_mae:+.2f} y RMSE {d_rmse:+.2f}, acerca el sesgo a 0 "
                f"({bias_o:+.2f}->{bias_c:+.2f}) y n={n}>= {N_MIN_ACTIVATE}: candidata a corrección "
                f"de display en una fase posterior (requiere aprobación explícita).")
    if pf_material or cum_best >= DELTA_MAE_MATERIAL:
        return ("SHADOW_ONLY",
                f"hay mejora real (pre_fixture ΔMAE {('%.2f' % d_mae) if d_mae is not None else 'n/a'}, "
                f"mejor cumulative ΔMAE {cum_best:.2f}) pero n={n} < {N_MIN_ACTIVATE}: seguir SOLO en "
                f"shadow y acumular muestra antes de plantear activación.")
    return ("NO_CHANGE",
            f"sin mejora material en pre_fixture (ΔMAE {('%.2f' % d_mae) if d_mae is not None else 'n/a'}) "
            f"ni muestra suficiente (n={n}): no cambiar nada.")


# ===================================================================== build summary + rows
def build_summary_and_rows(ev):
    if not len(ev):
        summary = {"generated_at_utc": now_iso(), "n_team_rows": 0, "n_fixtures": 0,
                   "reason": "sin filas evaluables en el scorecard de SOT todavía.",
                   "recommendation": "NO_CHANGE",
                   "recommendation_reason": "sin datos.",
                   "thresholds": {"n_min_activate": N_MIN_ACTIVATE, "delta_mae_material": DELTA_MAE_MATERIAL,
                                  "min_side_rows": MIN_SIDE_ROWS, "min_team_fixtures": MIN_TEAM_FIXTURES,
                                  "min_history_rows": MIN_HISTORY_ROWS}}
        return summary, []

    pred = ev["pred"].values.astype(float)
    act = ev["act"].values.astype(float)
    orig = _metrics(pred, act)

    # ---- cumulative corrections ----
    g_ratio = fit_global_ratio(pred, act)
    g_bias = fit_global_bias(pred, act)
    side_ratios = fit_side_ratios(ev, g_ratio)
    team_ratios = fit_team_ratios(ev, g_ratio)

    c_ratio = _clip0(pred * g_ratio)
    c_bias = _clip0(pred - g_bias)
    c_side = _clip0(np.array([float(p) * side_ratios.get(s, g_ratio)
                              for p, s in zip(pred, ev["side"].values)]))
    c_team = _clip0(np.array([float(p) * team_ratios.get(int(t), g_ratio)
                              for p, t in zip(pred, ev["team_id"].values)]))

    def _method(name, corrected):
        m = _metrics(corrected, act)
        m["delta_mae"] = round(orig["mae"] - m["mae"], 4) if m["mae"] is not None else None
        m["delta_rmse"] = round(orig["rmse"] - m["rmse"], 4) if m["rmse"] is not None else None
        return m

    cumulative = {
        "global_ratio": {**_method("global_ratio", c_ratio), "ratio": round(g_ratio, 4)},
        "global_bias": {**_method("global_bias", c_bias), "bias_subtracted": round(g_bias, 4)},
        "home_away_ratio": {**_method("home_away_ratio", c_side),
                            "ratios": {k: round(v, 4) for k, v in side_ratios.items()}},
        "team_ratio": {**_method("team_ratio", c_team),
                       "n_teams_own_ratio": int(sum(1 for tid, g in ev.groupby("team_id")
                                                    if len(g) >= MIN_TEAM_FIXTURES))},
    }

    # ---- anti-look-ahead ----
    c_pre, modes, confs = pre_fixture_correction(ev)
    c_loo = leave_one_fixture_out_correction(ev)

    pre_all = _metrics(c_pre, act)        # over ALL rows (kept-original rows contribute original error)
    pre_all["delta_mae"] = round(orig["mae"] - pre_all["mae"], 4) if pre_all["mae"] is not None else None
    pre_all["delta_rmse"] = round(orig["rmse"] - pre_all["rmse"], 4) if pre_all["rmse"] is not None else None
    # matched subset (rows actually corrected) — the honest online comparison vs their own original
    mask = np.array([m == "pre_fixture_applied" for m in modes])
    n_corr = int(mask.sum())
    if n_corr:
        o_sub = _metrics(pred[mask], act[mask])
        c_sub = _metrics(c_pre[mask], act[mask])
        pre = {"n_corrected": n_corr, "n_kept_original": int(len(ev) - n_corr),
               "mae_all_rows": pre_all["mae"], "rmse_all_rows": pre_all["rmse"], "bias_all_rows": pre_all["bias"],
               "delta_mae_all_rows": pre_all["delta_mae"], "delta_rmse_all_rows": pre_all["delta_rmse"],
               "mae_original_on_corrected": o_sub["mae"], "mae_corrected_on_corrected": c_sub["mae"],
               "rmse_original_on_corrected": o_sub["rmse"], "rmse_corrected_on_corrected": c_sub["rmse"],
               "bias_original_on_corrected": o_sub["bias"], "bias_corrected_on_corrected": c_sub["bias"],
               "delta_mae_on_corrected": round(o_sub["mae"] - c_sub["mae"], 4),
               "delta_rmse_on_corrected": round(o_sub["rmse"] - c_sub["rmse"], 4)}
    else:
        pre = {"n_corrected": 0, "n_kept_original": int(len(ev)),
               "mae_all_rows": pre_all["mae"], "rmse_all_rows": pre_all["rmse"], "bias_all_rows": pre_all["bias"],
               "delta_mae_all_rows": pre_all["delta_mae"], "delta_rmse_all_rows": pre_all["delta_rmse"],
               "delta_mae_on_corrected": None, "delta_rmse_on_corrected": None,
               "bias_original_on_corrected": None, "bias_corrected_on_corrected": None,
               "reason": "sin historial previo suficiente en ningún fixture -> todo se mantiene original."}

    loo = _metrics(c_loo, act)
    loo["delta_mae"] = round(orig["mae"] - loo["mae"], 4) if loo["mae"] is not None else None
    loo["delta_rmse"] = round(orig["rmse"] - loo["rmse"], 4) if loo["rmse"] is not None else None

    summary = {
        "generated_at_utc": now_iso(),
        "n_team_rows": int(len(ev)),
        "n_fixtures": int(ev["fixture_id"].nunique()),
        "original": orig,
        "cumulative": cumulative,
        "anti_look_ahead": {"pre_fixture": pre, "leave_one_fixture_out": loo},
        "thresholds": {"n_min_activate": N_MIN_ACTIVATE, "delta_mae_material": DELTA_MAE_MATERIAL,
                       "min_side_rows": MIN_SIDE_ROWS, "min_team_fixtures": MIN_TEAM_FIXTURES,
                       "min_history_rows": MIN_HISTORY_ROWS},
    }
    rec, reason = recommend(summary)
    summary["recommendation"] = rec
    summary["recommendation_reason"] = reason

    # ---- per-row CSV ----
    rows = []
    for pos, (_idx, r) in enumerate(ev.iterrows()):
        err_o = float(r["pred"]) - float(r["act"])
        err_pf = float(c_pre[pos]) - float(r["act"])
        applied = modes[pos] == "pre_fixture_applied"
        rows.append({
            "fixture_id": r["fixture_id"], "kickoff_utc": r["kickoff_utc"],
            "team_id": r["team_id"], "team_name": r.get("team_name", ""),
            "opponent_id": ("" if pd.isna(r.get("opponent_id")) else r.get("opponent_id")),
            "opponent_name": r.get("opponent_name", ""), "side": r.get("side", ""),
            "predicted_sot_original": round(float(r["pred"]), 3),
            "actual_sot": round(float(r["act"]), 3),
            "corrected_sot_global_ratio": round(float(c_ratio[pos]), 3),
            "corrected_sot_global_bias": round(float(c_bias[pos]), 3),
            "corrected_sot_home_away_ratio": round(float(c_side[pos]), 3),
            "corrected_sot_pre_fixture": round(float(c_pre[pos]), 3),
            "corrected_sot_leave_one_out": round(float(c_loo[pos]), 3),
            "error_original": round(err_o, 3), "error_corrected_pre_fixture": round(err_pf, 3),
            "abs_error_original": round(abs(err_o), 3),
            "abs_error_corrected_pre_fixture": round(abs(err_pf), 3),
            "correction_mode": modes[pos],
            "data_quality": "evaluable",
            "confidence": confs[pos],
            "reason": ("pre_fixture: ratio de fixtures anteriores aplicado (shadow)" if applied
                       else "pre_fixture: sin historial previo suficiente -> original (shadow)"),
        })
    return summary, rows


# ===================================================================== report
def _bias_es(b):
    if b is None:
        return "—"
    if abs(b) < 0.25:
        return "≈ neutral"
    return "infraestima" if b < 0 else "sobrestima"


def render_txt(summary):
    L = []
    n = summary["n_team_rows"]
    if n == 0:
        L.append(f"⚽ Corrección de nivel SOT de equipo (SHADOW): sin filas evaluables ({now_iso()[:10]}).")
        L.append("")
        L.append(summary.get("reason", ""))
        L.append("")
        L.append(f"recomendación: {summary['recommendation']} — {summary['recommendation_reason']}")
        L.append(f"generated_at_utc: {summary['generated_at_utc']}")
        return "\n".join(L)

    o = summary["original"]
    pf = summary["anti_look_ahead"]["pre_fixture"]
    loo = summary["anti_look_ahead"]["leave_one_fixture_out"]
    L.append(f"⚽ Corrección de nivel SOT de equipo — SHADOW / display-only (N={n}, "
             f"{summary['n_fixtures']} partidos). NO se aplica nada; solo medición.")
    L.append("")
    L.append("===== original (sin corrección) =====")
    L.append(f"  MAE {o['mae']:.2f} · RMSE {o['rmse']:.2f} · sesgo {o['bias']:+.2f} ({_bias_es(o['bias'])})")
    L.append("")
    L.append("===== correcciones CUMULATIVE (ajustadas sobre TODA la muestra -> optimistas) =====")
    L.append(f"  {'método':18} {'ratio/bias':>11} {'MAE':>6} {'ΔMAE':>7} {'RMSE':>6} {'ΔRMSE':>7} {'sesgo':>7}")
    for name, m in summary["cumulative"].items():
        pv = m.get("ratio", m.get("bias_subtracted", ""))
        pv = f"{pv:.3f}" if isinstance(pv, (int, float)) else str(pv)
        L.append(f"  {name:18} {pv:>11} {m['mae']:>6.2f} {m['delta_mae']:>+7.2f} "
                 f"{m['rmse']:>6.2f} {m['delta_rmse']:>+7.2f} {m['bias']:>+7.2f}")
    if "ratios" in summary["cumulative"]["home_away_ratio"]:
        L.append(f"    home/away ratios: {summary['cumulative']['home_away_ratio']['ratios']}")
    L.append("")
    L.append("===== ANTI-LOOK-AHEAD (decisivo) =====")
    L.append(f"  pre_fixture (online; ratio de fixtures ANTERIORES): corregidos {pf['n_corrected']}/"
             f"{n}, mantenidos {pf['n_kept_original']}")
    if pf.get("delta_mae_on_corrected") is not None:
        L.append(f"    sobre filas corregidas: MAE {pf['mae_original_on_corrected']:.2f}->"
                 f"{pf['mae_corrected_on_corrected']:.2f} (Δ {pf['delta_mae_on_corrected']:+.2f}) · "
                 f"RMSE Δ {pf['delta_rmse_on_corrected']:+.2f} · "
                 f"sesgo {pf['bias_original_on_corrected']:+.2f}->{pf['bias_corrected_on_corrected']:+.2f}")
    L.append(f"    sobre TODAS las filas: MAE {pf['mae_all_rows']:.2f} (Δ {pf['delta_mae_all_rows']:+.2f}) · "
             f"RMSE {pf['rmse_all_rows']:.2f} (Δ {pf['delta_rmse_all_rows']:+.2f})")
    L.append(f"  leave_one_fixture_out (diagnóstico, menos estricto): MAE {loo['mae']:.2f} "
             f"(Δ {loo['delta_mae']:+.2f}) · sesgo {loo['bias']:+.2f}")
    L.append("")
    th = summary["thresholds"]
    L.append("===== RECOMENDACIÓN =====")
    L.append(f"  >>> {summary['recommendation']}")
    L.append(f"  {summary['recommendation_reason']}")
    L.append(f"  umbrales: n_min_activate={th['n_min_activate']} · ΔMAE_material={th['delta_mae_material']} · "
             f"pre_fixture manda sobre cumulative.")
    L.append("")
    L.append("HONESTIDAD: las métricas CUMULATIVE están ajustadas sobre la misma muestra (optimistas); "
             "manda el pre_fixture (online, sin mirar el propio partido ni los futuros). NADA se aplica: "
             "ni pesos, ni lam_shot_on, ni modelo de jugador, ni predicción base, ni Telegram. Solo shadow.")
    L.append("")
    L.append(f"generated_at_utc: {summary['generated_at_utc']}")
    return "\n".join(L)


# ===================================================================== I/O
def write_csv(rows, path=OUT_CSV):
    pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(path, index=False)


def build(scorecard_path=SOT_SCORECARD, write=True,
          csv_path=OUT_CSV, json_path=OUT_JSON, txt_path=OUT_TXT):
    ev = load_evaluable(scorecard_path)
    summary, rows = build_summary_and_rows(ev)
    if write:
        write_csv(rows, csv_path)
        Path(json_path).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(txt_path).write_text(render_txt(summary) + "\n", encoding="utf-8")
    return summary, rows


def main(scorecard_path=SOT_SCORECARD):
    summary, _rows = build(scorecard_path)
    n = summary["n_team_rows"]
    if n:
        pf = summary["anti_look_ahead"]["pre_fixture"]
        print(f"team-SOT level correction [SHADOW] N={n}: original MAE={summary['original']['mae']} "
              f"bias={summary['original']['bias']} | pre_fixture ΔMAE(corr)="
              f"{pf.get('delta_mae_on_corrected')} -> {summary['recommendation']}")
    else:
        print(f"team-SOT level correction [SHADOW]: 0 evaluable rows -> {summary['recommendation']}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup team SOT level-correction evaluator (shadow, Fase 4M).")
    ap.add_argument("--scorecard", default=str(SOT_SCORECARD))
    a = ap.parse_args()
    sys.exit(main(a.scorecard))
