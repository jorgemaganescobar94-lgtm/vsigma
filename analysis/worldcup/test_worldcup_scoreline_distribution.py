"""
Fase 4K offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the Poisson scoreline distribution, the top-5 ordering, safe_float, the no-λ no_evaluable case,
the scoreline evaluation (top-1/3/5 hit, rank of actual, derived 1X2) and the Fase-4J integration.
Measurement only — base model never modified.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_worldcup_scoreline_distribution as sd  # noqa: E402
import evaluate_worldcup_scoreline_distribution as se  # noqa: E402
import evaluate_worldcup_prediction_accuracy as pa  # noqa: E402

FORBIDDEN = ["apuesta", "apostar", "cuota", "odds", "edge", "pick", "stake", "roi", "mercado"]


# ---------------------------------------------------------------- Poisson core
def test_poisson_distribution_sums_to_one():
    grid, _ = sd.scoreline_distribution(1.4, 1.1)
    assert abs(sum(grid.values()) - 1.0) < 1e-9          # normalised
    assert all(p >= 0 for p in grid.values())


def test_top5_ordered_by_probability():
    grid, _ = sd.scoreline_distribution(1.5, 1.0)
    top5 = sd.top_scorelines(grid, 5)
    probs = [t["probability"] for t in top5]
    assert probs == sorted(probs, reverse=True) and len(top5) == 5
    assert all("-" in t["scoreline"] for t in top5)


def test_distribution_1x2_sums_to_one_and_matches_lambda_skew():
    grid, _ = sd.scoreline_distribution(2.5, 0.4)        # strong home favourite
    d = sd.distribution_1x2(grid)
    assert abs(d["home_win"] + d["draw"] + d["away_win"] - 1.0) < 1e-9
    assert d["home_win"] > d["away_win"]                 # higher home λ -> more home wins


def test_safe_num_ignores_strings():
    assert sd.safe_num("Pedri; Gavi") is None and sd.safe_num("") is None
    assert sd.safe_num("1.8") == 1.8 and sd.safe_num(None) is None
    assert sd.safe_prob(1.5) is None and sd.safe_prob(0.4) == 0.4


def test_resolve_lambdas_priority_and_missing():
    row = {"l3_xg_home": 1.2, "l3_xg_away": 0.9, "mx_xg_home": 2.0, "mx_xg_away": 0.5}
    lh, la, src = sd.resolve_lambdas(row)
    assert src == "mx" and lh == 2.0                      # mx outranks l3
    assert sd.resolve_lambdas({"l3_xg_home": "x", "l3_xg_away": "y"}) == (None, None, None)


def test_fixture_without_lambdas_is_no_evaluable():
    fx = sd.build_fixture_distribution({"fixture_id": 1, "home": "A", "away": "B"})
    assert fx["top_5_scorelines"] == [] and fx["confidence"] == "baja"
    assert "sin goles esperados" in fx["reason"]


# ---------------------------------------------------------------- evaluation
def _pred(rows):
    cols = ["fixture_id", "settled", "result_final_gh", "result_final_ga", "result_1x2"]
    return pd.DataFrame([{c: r.get(c) for c in cols} for r in rows], columns=cols)


def _dist(fid, lh, la, home="A", away="B"):
    fx = sd.build_fixture_distribution({"fixture_id": fid, "home": home, "away": away,
                                        "l3_xg_home": lh, "l3_xg_away": la})
    return fx


def test_evaluation_top_hits_and_rank():
    # build a distribution dict + matching results; one match lands on the most likely score
    dist = {1: _dist(1, 1.2, 0.8)}                         # top score likely 1-0 or 1-1
    top1 = dist[1]["top_5_scorelines"][0]["scoreline"]
    gh, ga = map(int, top1.split("-"))
    pred = _pred([{"fixture_id": 1, "settled": 1, "result_final_gh": gh, "result_final_ga": ga,
                   "result_1x2": sd.implied_result(gh, ga)}])
    rows = se.build_rows(dist, pred)
    assert len(rows) == 1
    r = rows[0]
    assert r["in_top1"] == 1 and r["in_top3"] == 1 and r["in_top5"] == 1
    assert r["rank_actual_score"] == 1
    assert r["actual_score_probability"] > 0


def test_evaluation_summary_metrics():
    dist, preds = {}, []
    for i in range(35):
        dist[i] = _dist(i, 1.3, 1.0)
        preds.append({"fixture_id": i, "settled": 1, "result_final_gh": 1, "result_final_ga": 1,
                      "result_1x2": "D"})
    summary = se.summarize(se.build_rows(dist, _pred(preds)))
    assert summary["n_matches"] == 35 and summary["status"] == "ACTIVO"
    for k in ("exact_score_top1_hit_rate", "exact_score_top3_hit_rate", "exact_score_top5_hit_rate",
              "mean_rank_actual_score", "derived_1x2_accuracy", "goals_mae_total"):
        assert summary[k] is not None


def test_evaluation_no_matches_no_evaluable():
    summary = se.summarize([])
    assert summary["status"] == "NO_EVALUABLE" and summary["n_matches"] == 0


# ---------------------------------------------------------------- Fase 4J integration
def test_fase4j_scoreline_module_no_evaluable_when_absent(tmp_path):
    m = pa.evaluate_scoreline_module(tmp_path / "nope.json")
    assert m["status"] == "NO_EVALUABLE" and m["module"] == "Marcadores top-3/5"


def test_fase4j_scoreline_module_active_from_summary(tmp_path):
    import json
    payload = {"summary": {"n_matches": 44, "status": "ACTIVO", "exact_score_top1_hit_rate": 0.11,
                           "exact_score_top3_hit_rate": 0.36, "exact_score_top5_hit_rate": 0.52,
                           "mean_rank_actual_score": 6.98, "derived_1x2_accuracy": 0.68,
                           "actual_score_avg_probability": 0.078, "reason": "44 partidos"}}
    f = tmp_path / "scoreline_eval.json"; f.write_text(json.dumps(payload), encoding="utf-8")
    m = pa.evaluate_scoreline_module(f)
    assert m["status"] == "ACTIVO" and m["n"] == 44
    assert m["primary_value"] == 0.36
    assert m["secondary"]["top5"] == 0.52


# ---------------------------------------------------------------- report wording
def test_reports_no_betting_language():
    dist = {1: _dist(1, 1.4, 1.0)}
    pred = _pred([{"fixture_id": 1, "settled": 1, "result_final_gh": 1, "result_final_ga": 1,
                   "result_1x2": "D"}])
    summ = {"summary": se.summarize(se.build_rows(dist, pred)), "meta": {}}
    txt = se.render_txt(summ).lower()
    assert "marcador" in txt and not any(w in txt for w in FORBIDDEN)
    btxt = sd.render_txt(sd.build(write=False)).lower() if False else ""  # build() reads real file; skip
    # build distribution report from a tiny synthetic payload
    payload = {"meta": {"fixtures_total": 1, "fixtures_with_distribution": 1, "maxg": 10, "top_n": 5},
               "scoreline_distribution": [dist[1]]}
    assert not any(w in sd.render_txt(payload).lower() for w in FORBIDDEN)
