"""
WORLD CUP 2026 — SCORELINE DISTRIBUTION EVALUATION (Fase 4K). READ-ONLY · NO API · NO scraping · NO web
· NO market/odds/betting · NO fabrication · NO secrets. Pure football. MEASURE ONLY — nothing changed.

Scores the Fase-4K scoreline distribution against REAL settled results: exact-score top-1/3/5 hit rates,
the rank and probability mass of the ACTUAL scoreline, the 1X2 implied by the distribution (vs the
existing 1X2), and goal MAE from the λ. Recomputes each fixture's Poisson grid from the stored λ
(shared functions from build_worldcup_scoreline_distribution) so the actual-score rank/mass are exact.

Inputs:
  * worldcup_scoreline_distribution.json (per-fixture λ + top-5)
  * worldcup_predictions_log.csv         (result_final_gh/ga, result_1x2, settled)

Outputs:
  * worldcup_scoreline_evaluation.csv          (one row per evaluated fixture)
  * worldcup_scoreline_evaluation_summary.json
  * worldcup_scoreline_evaluation_report.txt

Run:  python analysis/worldcup/evaluate_worldcup_scoreline_distribution.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_worldcup_scoreline_distribution as sd  # noqa: E402  (shared Poisson functions)

DIST_JSON = HERE / "worldcup_scoreline_distribution.json"
PRED_LOG = HERE / "worldcup_predictions_log.csv"
OUT_CSV = HERE / "worldcup_scoreline_evaluation.csv"
OUT_JSON = HERE / "worldcup_scoreline_evaluation_summary.json"
OUT_TXT = HERE / "worldcup_scoreline_evaluation_report.txt"

MIN_SAMPLE = 30
EPS = 1e-12
CLASSES = ["H", "D", "A"]

CSV_COLUMNS = [
    "fixture_id", "home", "away", "lambda_home", "lambda_away", "source_lambda",
    "actual_score", "in_top1", "in_top3", "in_top5", "actual_score_probability",
    "rank_actual_score", "pred_top1_scoreline", "result_1x2", "derived_1x2_pred",
    "data_quality", "confidence",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _r(v, nd=4):
    return None if v is None else round(float(v), nd)


def _read_csv(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df if len(df) else None


def _load_distribution(path=DIST_JSON):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for f in payload.get("scoreline_distribution", []):
        fid = f.get("fixture_id")
        if fid is not None and f.get("lambda_home") is not None:
            out[int(fid)] = f
    return out


def _rank_of(grid, score):
    """1-based rank of `score` (i,j) in the grid sorted by prob desc; None if outside the grid."""
    if score not in grid:
        return None
    order = sorted(grid.items(), key=lambda kv: (-kv[1], kv[0][0] + kv[0][1], kv[0][0]))
    for idx, (k, _) in enumerate(order, 1):
        if k == score:
            return idx
    return None


# ============================================================ evaluation (pure-ish)
def build_rows(dist_by_fixture, pred_df):
    """Pair each fixture distribution with its real result. Returns eval-row dicts for SETTLED fixtures."""
    rows = []
    if pred_df is None:
        return rows
    s = pred_df[pred_df.get("settled") == 1] if "settled" in pred_df.columns else pred_df
    for _, r in s.iterrows():
        try:
            fid = int(r["fixture_id"])
        except Exception:
            continue
        fx = dist_by_fixture.get(fid)
        if not fx:
            continue
        gh, ga = sd.safe_num(r.get("result_final_gh")), sd.safe_num(r.get("result_final_ga"))
        if gh is None or ga is None:
            continue
        gh, ga = int(round(gh)), int(round(ga))
        lh, la = sd.safe_num(fx.get("lambda_home")), sd.safe_num(fx.get("lambda_away"))
        if lh is None or la is None:
            continue
        grid, _ = sd.scoreline_distribution(lh, la)
        top5 = sd.top_scorelines(grid, 5)
        top_scores = [(t["score_home"], t["score_away"]) for t in top5]
        actual = (gh, ga)
        d1x2 = sd.distribution_1x2(grid)
        derived_pred = max(zip(CLASSES, (d1x2["home_win"], d1x2["draw"], d1x2["away_win"])),
                           key=lambda kv: kv[1])[0]
        rows.append({
            "fixture_id": fid, "home": fx.get("home"), "away": fx.get("away"),
            "lambda_home": _r(lh, 3), "lambda_away": _r(la, 3), "source_lambda": fx.get("source_lambda"),
            "actual_score": f"{gh}-{ga}",
            "in_top1": int(actual == top_scores[0]) if top_scores else 0,
            "in_top3": int(actual in top_scores[:3]),
            "in_top5": int(actual in top_scores[:5]),
            "actual_score_probability": _r(grid.get(actual, 0.0)),
            "rank_actual_score": _rank_of(grid, actual),
            "pred_top1_scoreline": top5[0]["scoreline"] if top5 else None,
            "result_1x2": str(r.get("result_1x2") or "").strip().upper(),
            "derived_1x2_pred": derived_pred,
            "_d1x2": d1x2, "_actual_goals": (gh, ga), "_lambdas": (lh, la),
            "data_quality": "media", "confidence": "media",
        })
    return rows


def summarize(rows):
    n = len(rows)
    if n == 0:
        return {"n_matches": 0, "status": "NO_EVALUABLE",
                "reason": "sin fixtures liquidados con distribución y resultado"}
    top1 = sum(r["in_top1"] for r in rows) / n
    top3 = sum(r["in_top3"] for r in rows) / n
    top5 = sum(r["in_top5"] for r in rows) / n
    avg_p = sum(r["actual_score_probability"] for r in rows) / n
    ranks = [r["rank_actual_score"] for r in rows if r["rank_actual_score"] is not None]
    mean_rank = sum(ranks) / len(ranks) if ranks else None
    # derived 1X2 metrics (multiclass)
    correct = 0
    mbrier = mll = 0.0
    for r in rows:
        d = r["_d1x2"]
        p = {"H": d["home_win"], "D": d["draw"], "A": d["away_win"]}
        tot = sum(p.values()) or 1.0
        p = {k: v / tot for k, v in p.items()}
        actual = r["result_1x2"] if r["result_1x2"] in CLASSES else None
        if actual is None:
            continue
        correct += int(max(p, key=p.get) == actual)
        mbrier += sum((p[k] - (1.0 if actual == k else 0.0)) ** 2 for k in CLASSES)
        mll += -math.log(min(max(p[actual], EPS), 1 - EPS))
    n1x2 = sum(1 for r in rows if r["result_1x2"] in CLASSES)
    # goal MAE from lambdas
    mae_h = sum(abs(r["_lambdas"][0] - r["_actual_goals"][0]) for r in rows) / n
    mae_a = sum(abs(r["_lambdas"][1] - r["_actual_goals"][1]) for r in rows) / n
    mae_t = sum(abs((r["_lambdas"][0] + r["_lambdas"][1]) - (r["_actual_goals"][0] + r["_actual_goals"][1]))
                for r in rows) / n
    bias_t = sum((r["_lambdas"][0] + r["_lambdas"][1]) - (r["_actual_goals"][0] + r["_actual_goals"][1])
                 for r in rows) / n
    status = "ACTIVO" if n >= MIN_SAMPLE else "INSUFFICIENT_SAMPLE"
    return {
        "n_matches": n, "status": status,
        "exact_score_top1_hit_rate": _r(top1), "exact_score_top3_hit_rate": _r(top3),
        "exact_score_top5_hit_rate": _r(top5),
        "actual_score_avg_probability": _r(avg_p), "probability_mass_actual_score": _r(avg_p),
        "mean_rank_actual_score": _r(mean_rank, 2),
        "n_actual_in_grid": len(ranks),
        "derived_1x2_accuracy": _r(correct / n1x2) if n1x2 else None,
        "derived_1x2_brier_multiclass": _r(mbrier / n1x2) if n1x2 else None,
        "derived_1x2_logloss_multiclass": _r(mll / n1x2) if n1x2 else None,
        "goals_mae_home": _r(mae_h), "goals_mae_away": _r(mae_a), "goals_mae_total": _r(mae_t),
        "goals_bias_total": _r(bias_t),
        "confidence": "media" if status == "ACTIVO" else "baja",
        "reason": f"{n} partidos liquidados con distribución de marcadores y resultado",
    }


def build(dist_json=DIST_JSON, pred_log=PRED_LOG, write=True):
    dist = _load_distribution(dist_json)
    pred = _read_csv(pred_log)
    rows = build_rows(dist, pred)
    summary = summarize(rows)
    payload = {"meta": {"min_sample": MIN_SAMPLE,
                        "method": "marcador real vs distribución Poisson derivada del xG existente; "
                                  "modelo base NO modificado; solo medición."},
               "summary": summary,
               "rows": [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]}
    if write:
        pd.DataFrame([{c: r.get(c) for c in CSV_COLUMNS} for r in rows],
                     columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
        Path(OUT_JSON).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(OUT_TXT).write_text(render_txt(payload) + "\n", encoding="utf-8")
    return payload


def render_txt(payload) -> str:
    s = payload["summary"]
    L = ["===== WORLD CUP — EVALUACIÓN DE DISTRIBUCIÓN DE MARCADORES (Fase 4K) =====", ""]
    if s.get("n_matches", 0) == 0:
        L.append(f"Estado: {s.get('status')} — {s.get('reason')}")
        return "\n".join(L)
    L += [f"Estado: {s['status']} · partidos: {s['n_matches']}", "",
          "-- ACIERTO DE MARCADOR EXACTO --",
          f"  top-1: {s['exact_score_top1_hit_rate']} · top-3: {s['exact_score_top3_hit_rate']} · "
          f"top-5: {s['exact_score_top5_hit_rate']}",
          f"  prob. media del marcador real: {s['actual_score_avg_probability']} · "
          f"rank medio del real: {s['mean_rank_actual_score']} "
          f"(en grid: {s['n_actual_in_grid']}/{s['n_matches']})", "",
          "-- 1X2 DERIVADO DE LA DISTRIBUCIÓN --",
          f"  accuracy: {s['derived_1x2_accuracy']} · Brier: {s['derived_1x2_brier_multiclass']} · "
          f"LogLoss: {s['derived_1x2_logloss_multiclass']}", "",
          "-- GOLES (MAE desde λ) --",
          f"  home: {s['goals_mae_home']} · away: {s['goals_mae_away']} · total: {s['goals_mae_total']} "
          f"· bias total: {s['goals_bias_total']}", "",
          "Predicción futbolística pura, sin terminología de juego. Solo medición; el modelo base NO se "
          "modifica. NO toca data/external."]
    return "\n".join(L)


def main():
    p = build()
    s = p["summary"]
    if s.get("n_matches", 0) == 0:
        print(f"scoreline eval: {s.get('status')} — {s.get('reason')}")
        return 0
    print(f"scoreline eval: n={s['n_matches']} | top1={s['exact_score_top1_hit_rate']} "
          f"top3={s['exact_score_top3_hit_rate']} top5={s['exact_score_top5_hit_rate']} | "
          f"mean_rank={s['mean_rank_actual_score']} | derived 1X2 acc={s['derived_1x2_accuracy']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
