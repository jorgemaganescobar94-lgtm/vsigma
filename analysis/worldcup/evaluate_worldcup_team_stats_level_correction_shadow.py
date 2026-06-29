"""
WORLD CUP 2026 — TEAM STATS (shots / corners) LEVEL-CORRECTION SHADOW EVALUATOR (Fase 4N). SHADOW /
DISPLAY-ONLY · READ-ONLY · NO API · NO scraping · NO web · NO market/odds/betting · NO fabrication · NO
secrets · NO external sources. Pure football. EVALUATE ONLY — NOTHING is applied: base model, the stats
model, predictions, the existing stats-level correction and Telegram are NOT touched. No weights change.

CONTEXT (Fase 4J finding): the team-stats model UNDER-predicts shots (bias ≈ −6.05 on the per-fixture
total) and corners (bias ≈ −1.39). This module extends the SOT shadow pattern (Fase 4M) to shots and
corners: it measures whether a simple level correction reduces MAE/bias AND survives an anti-look-ahead
(pre_fixture, online) test. It recommends only; it never activates anything.

DATA: the per-FIXTURE totals (both teams) live in worldcup_predictions_log.csv — st_shots_total vs
result_shots and st_corners_total vs result_corners — frozen pre-KO, filled at settle, WITH kickoff for
chronology. That is per-fixture (not per-team), enough for the full pattern (cumulative + pre_fixture +
leave_one_out). If the per-fixture log is unavailable for a stat but the aggregated scorecard has it,
the stat is reported at AGGREGATE level only and marked NEEDS_PER_FIXTURE_DATA — no fake anti-look-ahead.

HOME/AWAY ratio is NOT evaluated here: the log persists only per-fixture TOTALS (no per-side split), so a
side ratio would be fabricated. Cards are EXCLUDED (separate card-risk line; not interfered with).

The pure correction/metric helpers are reused from the Fase-4M SOT evaluator (single source of truth).

OUTPUT (read-only; explicit git-add only):
  * worldcup_team_stats_level_correction_shadow.csv        (one row per stat × correction_type)
  * worldcup_team_stats_level_correction_shadow_summary.json (regenerable -> gitignored)
  * worldcup_team_stats_level_correction_shadow_report.txt   (no betting language; regenerable -> gitignored)

Run:  python analysis/worldcup/evaluate_worldcup_team_stats_level_correction_shadow.py
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
sys.path.insert(0, str(HERE))
# Reuse the SOT shadow evaluator's pure helpers (metrics, ratio/bias fit, clip, anti-look-ahead).
import evaluate_worldcup_team_sot_level_correction as lc  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PRED_LOG = HERE / "worldcup_predictions_log.csv"
TEAM_STATS_SCORECARD = HERE / "worldcup_team_stats_scorecard.csv"
OUT_CSV = HERE / "worldcup_team_stats_level_correction_shadow.csv"
OUT_JSON = HERE / "worldcup_team_stats_level_correction_shadow_summary.json"
OUT_TXT = HERE / "worldcup_team_stats_level_correction_shadow_report.txt"

# (stat key, per-fixture predicted total col, per-fixture real total col) — cards excluded on purpose.
STATS = [
    ("shots", "st_shots_total", "result_shots"),
    ("corners", "st_corners_total", "result_corners"),
]

# thresholds reused from the SOT evaluator (single source of truth)
N_MIN_ACTIVATE = lc.N_MIN_ACTIVATE
DELTA_MAE_MATERIAL = lc.DELTA_MAE_MATERIAL

CSV_COLUMNS = ["stat", "n", "original_mae", "original_rmse", "original_bias", "correction_type",
               "corrected_mae", "corrected_rmse", "corrected_bias", "delta_mae", "recommendation",
               "data_quality", "confidence", "reason"]


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


# ===================================================================== per-fixture data
def load_stat_ev(pred_df, pred_col, real_col):
    """Per-fixture evaluable rows (fixture_id, kickoff_utc, pred, act) for one stat, settled only,
    chronologically sorted. Empty DataFrame if the columns/rows are unavailable. No fabrication."""
    if pred_df is None or pred_col not in pred_df.columns or real_col not in pred_df.columns:
        return pd.DataFrame()
    df = pred_df
    if "settled" in df.columns:
        df = df[df["settled"].fillna(0).astype(int) == 1]
    sub = df.dropna(subset=[pred_col, real_col])
    if not len(sub):
        return pd.DataFrame()
    ev = pd.DataFrame({
        "fixture_id": sub["fixture_id"].values if "fixture_id" in sub.columns else range(len(sub)),
        "kickoff_utc": (sub["kickoff_utc"].fillna("").values if "kickoff_utc" in sub.columns
                        else [""] * len(sub)),
        "pred": sub[pred_col].astype(float).values,
        "act": sub[real_col].astype(float).values,
    })
    return ev.sort_values(["kickoff_utc", "fixture_id"]).reset_index(drop=True)


def load_aggregate(scorecard_df, stat):
    """{mae, rmse, bias, n} for a stat from the aggregated team-stats scorecard, or None."""
    if scorecard_df is None or "stat" not in scorecard_df.columns:
        return None
    row = scorecard_df[scorecard_df["stat"].astype(str).str.lower() == stat]
    if not len(row):
        return None
    r = row.iloc[0]
    def g(c):
        try:
            v = float(r[c]); return v if v == v else None
        except (KeyError, TypeError, ValueError):
            return None
    return {"n": int(g("n") or 0), "mae": g("mae"), "rmse": g("rmse"), "bias": g("bias")}


# ===================================================================== per-stat recommendation
def _recommend_stat(n, pre_dmae, pre_drmse, bias_o, bias_c, cum_best):
    """Allowed set: SHADOW_ONLY / NO_CHANGE / CONSIDER_DISPLAY_CORRECTION_LATER (NEEDS_PER_FIXTURE_DATA
    is decided upstream when there is no per-fixture data). pre_fixture overrides cumulative."""
    if pre_dmae is None:
        return "NO_CHANGE"
    bias_better = (bias_o is not None and bias_c is not None and abs(bias_c) < abs(bias_o) - 1e-9)
    strong_inversion = (bias_o is not None and bias_c is not None and (bias_c * bias_o < 0)
                        and abs(bias_c) > 0.5 * abs(bias_o) + 1e-9)
    pf_material = (pre_dmae >= DELTA_MAE_MATERIAL and (pre_drmse or 0) > 0
                   and bias_better and not strong_inversion)
    if pf_material and n >= N_MIN_ACTIVATE:
        return "CONSIDER_DISPLAY_CORRECTION_LATER"
    if pf_material or (cum_best is not None and cum_best >= DELTA_MAE_MATERIAL):
        return "SHADOW_ONLY"
    return "NO_CHANGE"


# ===================================================================== evaluate one stat
def evaluate_stat(stat, ev, agg):
    """Full pattern when per-fixture rows exist; else AGGREGATE-ONLY -> NEEDS_PER_FIXTURE_DATA. Returns
    a result dict with 'rows' (one per correction_type) and per-stat metrics/recommendation."""
    # AGGREGATE-ONLY fallback (no per-fixture chronology -> never fake anti-look-ahead)
    if ev is None or not len(ev):
        if agg is None:
            return {"stat": stat, "mode": "no_data", "n": 0, "recommendation": "NO_CHANGE",
                    "reason": "sin datos por fixture ni scorecard agregado para esta stat.",
                    "rows": [{"stat": stat, "n": 0, "original_mae": None, "original_rmse": None,
                              "original_bias": None, "correction_type": "(none)", "corrected_mae": None,
                              "corrected_rmse": None, "corrected_bias": None, "delta_mae": None,
                              "recommendation": "NO_CHANGE", "data_quality": "no_data",
                              "confidence": "baja", "reason": "sin datos."}]}
        return {"stat": stat, "mode": "aggregate_only", "n": agg["n"],
                "original": {"mae": agg["mae"], "rmse": agg["rmse"], "bias": agg["bias"]},
                "recommendation": "NEEDS_PER_FIXTURE_DATA",
                "reason": ("solo hay scorecard AGREGADO (sin filas por fixture): no se puede hacer "
                           "anti-look-ahead honesto -> NEEDS_PER_FIXTURE_DATA."),
                "rows": [{"stat": stat, "n": agg["n"], "original_mae": agg["mae"],
                          "original_rmse": agg["rmse"], "original_bias": agg["bias"],
                          "correction_type": "aggregate_only", "corrected_mae": None,
                          "corrected_rmse": None, "corrected_bias": None, "delta_mae": None,
                          "recommendation": "NEEDS_PER_FIXTURE_DATA", "data_quality": "aggregate_only",
                          "confidence": "baja",
                          "reason": "scorecard agregado; faltan filas por fixture para corrección honesta."}]}

    pred = ev["pred"].values.astype(float)
    act = ev["act"].values.astype(float)
    orig = lc._metrics(pred, act)
    n = orig["n"]

    g_ratio = lc.fit_global_ratio(pred, act)
    g_bias = lc.fit_global_bias(pred, act)
    c_ratio = lc._metrics(lc._clip0(pred * g_ratio), act)
    c_bias = lc._metrics(lc._clip0(pred - g_bias), act)

    c_pre_arr, modes, _confs = lc.pre_fixture_correction(ev)
    c_loo_arr = lc.leave_one_fixture_out_correction(ev)
    mask = np.array([m == "pre_fixture_applied" for m in modes])
    n_corr = int(mask.sum())
    if n_corr:
        o_sub = lc._metrics(pred[mask], act[mask])
        c_sub = lc._metrics(c_pre_arr[mask], act[mask])
        pre = {"corrected_mae": c_sub["mae"], "corrected_rmse": c_sub["rmse"],
               "corrected_bias": c_sub["bias"], "bias_original_on_corrected": o_sub["bias"],
               "delta_mae": round(o_sub["mae"] - c_sub["mae"], 4),
               "delta_rmse": round(o_sub["rmse"] - c_sub["rmse"], 4), "n_corrected": n_corr}
    else:
        pre = {"corrected_mae": None, "corrected_rmse": None, "corrected_bias": None,
               "bias_original_on_corrected": None, "delta_mae": None, "delta_rmse": None, "n_corrected": 0}
    loo = lc._metrics(c_loo_arr, act)

    cum_best = max([d for d in (round(orig["mae"] - c_ratio["mae"], 4),
                                round(orig["mae"] - c_bias["mae"], 4)) if d is not None], default=0.0)
    rec = _recommend_stat(n, pre["delta_mae"], pre["delta_rmse"],
                          pre["bias_original_on_corrected"], pre["corrected_bias"], cum_best)

    def _row(ctype, m, dmae, conf="baja", note=""):
        return {"stat": stat, "n": n, "original_mae": orig["mae"], "original_rmse": orig["rmse"],
                "original_bias": orig["bias"], "correction_type": ctype,
                "corrected_mae": m.get("mae"), "corrected_rmse": m.get("rmse"),
                "corrected_bias": m.get("bias"), "delta_mae": dmae, "recommendation": rec,
                "data_quality": "per_fixture_total", "confidence": conf, "reason": note}

    rows = [
        _row("global_ratio", c_ratio, round(orig["mae"] - c_ratio["mae"], 4),
             note=f"cumulative ratio={round(g_ratio, 4)} (optimista, ajustado sobre toda la muestra)"),
        _row("global_bias", c_bias, round(orig["mae"] - c_bias["mae"], 4),
             note=f"cumulative bias_subtracted={round(g_bias, 4)} (optimista)"),
        _row("pre_fixture",
             {"mae": pre["corrected_mae"], "rmse": pre["corrected_rmse"], "bias": pre["corrected_bias"]},
             pre["delta_mae"], conf=("media" if n_corr else "baja"),
             note=f"anti-look-ahead online sobre {n_corr} filas corregidas (decisivo)"),
        _row("leave_one_out", loo, round(orig["mae"] - loo["mae"], 4),
             note="diagnóstico (menos estricto: excluye el propio fixture pero ve futuros)"),
    ]
    return {"stat": stat, "mode": "per_fixture", "n": n,
            "original": {"mae": orig["mae"], "rmse": orig["rmse"], "bias": orig["bias"]},
            "global_ratio": round(g_ratio, 4), "global_bias_subtracted": round(g_bias, 4),
            "pre_fixture": pre, "leave_one_out": {"mae": loo["mae"], "bias": loo["bias"],
                                                  "delta_mae": round(orig["mae"] - loo["mae"], 4)},
            "cumulative_best_delta_mae": cum_best, "recommendation": rec, "rows": rows}


# ===================================================================== build
def build(pred_log=PRED_LOG, scorecard=TEAM_STATS_SCORECARD, write=True,
          csv_path=OUT_CSV, json_path=OUT_JSON, txt_path=OUT_TXT):
    pred = _read_csv(pred_log)
    sc = _read_csv(scorecard)
    results = {}
    all_rows = []
    for stat, pc, rc in STATS:
        ev = load_stat_ev(pred, pc, rc)
        agg = load_aggregate(sc, stat)
        res = evaluate_stat(stat, ev, agg)
        results[stat] = res
        all_rows.extend(res["rows"])
    summary = {
        "generated_at_utc": now_iso(),
        "stats": {k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in results.items()},
        "thresholds": {"n_min_activate": N_MIN_ACTIVATE, "delta_mae_material": DELTA_MAE_MATERIAL},
        "notes": ("home/away ratio NO evaluado (el log solo persiste totales por partido, no por equipo); "
                  "cards EXCLUIDAS (línea de tarjetas separada). Nada se aplica: solo shadow."),
    }
    if write:
        pd.DataFrame(all_rows, columns=CSV_COLUMNS).to_csv(csv_path, index=False)
        Path(json_path).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(txt_path).write_text(render_txt(results, summary) + "\n", encoding="utf-8")
    return summary, all_rows, results


# ===================================================================== report
def _fmt(v, nd=2):
    return "—" if v is None else f"{v:.{nd}f}"


def render_txt(results, summary):
    L = ["⚽ Corrección de nivel de stats de equipo (tiros/córners) — SHADOW / display-only. "
         f"NO se aplica nada; solo medición ({now_iso()[:10]}).", ""]
    for stat, res in results.items():
        if res["mode"] == "aggregate_only":
            o = res["original"]
            L.append(f"== {stat} == [NEEDS_PER_FIXTURE_DATA] n={res['n']} "
                     f"MAE {_fmt(o['mae'])} sesgo {_fmt(o['bias'])} (solo agregado; sin cronología)")
            L.append(f"   {res['reason']}")
            L.append("")
            continue
        if res["mode"] == "no_data":
            L.append(f"== {stat} == sin datos.")
            L.append("")
            continue
        o = res["original"]; pre = res["pre_fixture"]
        L.append(f"== {stat} == n={res['n']} · original MAE {_fmt(o['mae'])} RMSE {_fmt(o['rmse'])} "
                 f"sesgo {_fmt(o['bias'], 2)}")
        L.append(f"   cumulative: ratio={res['global_ratio']} bias_sub={res['global_bias_subtracted']} "
                 f"(optimista) · mejor ΔMAE {_fmt(res['cumulative_best_delta_mae'])}")
        if pre["n_corrected"]:
            L.append(f"   pre_fixture (online, {pre['n_corrected']} filas): MAE "
                     f"{_fmt(pre['corrected_mae'])} (ΔMAE {_fmt(pre['delta_mae'])}) · "
                     f"sesgo {_fmt(pre['bias_original_on_corrected'])}->{_fmt(pre['corrected_bias'])}")
        else:
            L.append("   pre_fixture: sin historial previo suficiente -> sin corrección online.")
        L.append(f"   leave_one_out (diagnóstico): MAE {_fmt(res['leave_one_out']['mae'])} "
                 f"(ΔMAE {_fmt(res['leave_one_out']['delta_mae'])})")
        L.append(f"   >>> {res['recommendation']}")
        L.append("")
    L.append(summary["notes"])
    L.append("")
    L.append("HONESTIDAD: las métricas CUMULATIVE están ajustadas sobre la misma muestra (optimistas); "
             "manda el pre_fixture (online). NADA se aplica: ni pesos, ni modelo de stats, ni la "
             "corrección de stats existente, ni predicción base, ni Telegram. Solo shadow.")
    L.append("")
    L.append(f"generated_at_utc: {summary['generated_at_utc']}")
    return "\n".join(L)


def main(pred_log=PRED_LOG, scorecard=TEAM_STATS_SCORECARD):
    summary, _rows, results = build(pred_log, scorecard)
    for stat, res in results.items():
        n = res.get("n", 0)
        rec = res.get("recommendation")
        if res["mode"] == "per_fixture":
            print(f"  {stat:8} n={n:>3} pre_fixture ΔMAE={res['pre_fixture']['delta_mae']} -> {rec}")
        else:
            print(f"  {stat:8} n={n:>3} -> {rec}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup team stats (shots/corners) level-correction shadow (Fase 4N).")
    ap.add_argument("--pred", default=str(PRED_LOG))
    ap.add_argument("--scorecard", default=str(TEAM_STATS_SCORECARD))
    a = ap.parse_args()
    sys.exit(main(a.pred, a.scorecard))
