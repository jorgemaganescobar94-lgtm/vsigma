"""
Fase 4J offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the GLOBAL prediction-accuracy evaluator: safe_prob, 1X2 Brier/LogLoss, goals MAE, per-player
binary modules, module statuses (NO_EVALUABLE / INSUFFICIENT_SAMPLE / ACTIVO), and report wording.
Measurement only — nothing is modified.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import evaluate_worldcup_prediction_accuracy as pa  # noqa: E402

FORBIDDEN = ["apuesta", "apostar", "cuota", "odds", "edge", "pick", "stake", "roi", "mercado"]


# ---------------------------------------------------------------- safe coercion
def test_safe_prob_ignores_strings_and_out_of_range():
    assert pa.safe_prob("Pedri; Gavi") is None and pa.safe_prob("") is None
    assert pa.safe_prob(1.5) is None and pa.safe_prob(-0.1) is None
    assert pa.safe_prob(0.4) == 0.4
    assert pa.safe_num("1.8") == 1.8 and pa.safe_num("x") is None


def test_binary_metrics():
    assert pa.brier_binary([1.0, 0.0], [1, 0]) == 0.0
    assert pa.brier_binary([0.5, 0.5], [1, 0]) == 0.25
    assert pa.mae([1.0, 2.0], [1.0, 4.0]) == 1.0
    assert round(pa.bias([2.0, 2.0], [1.0, 1.0]), 3) == 1.0


# ---------------------------------------------------------------- 1X2
def _pred(rows):
    cols = ["fixture_id", "settled", "result_1x2", "result_final_gh", "result_final_ga",
            "l3_home", "l3_draw", "l3_away", "l3_xg_home", "l3_xg_away", "l3_top_score",
            "mx_home", "mx_draw", "mx_away"]
    return pd.DataFrame([{c: r.get(c) for c in cols} for r in rows], columns=cols)


def test_evaluate_1x2_brier_logloss_accuracy():
    rows = [{"fixture_id": i, "settled": 1, "result_1x2": "H",
             "l3_home": 0.6, "l3_draw": 0.25, "l3_away": 0.15} for i in range(40)]
    m = pa.evaluate_1x2(_pred(rows))
    assert m["status"] == "ACTIVO" and m["n"] == 40
    assert m["primary_value"] == 1.0                       # always predicts H, all H
    assert m["secondary"]["brier_multiclass"] is not None
    assert m["secondary"]["logloss_multiclass"] is not None


def test_evaluate_1x2_ignores_non_numeric_probs():
    # a row with a non-numeric prob (the old inj_home string bug) must be skipped, not crash
    rows = [{"fixture_id": 1, "settled": 1, "result_1x2": "H",
             "l3_home": "Pedri", "l3_draw": "x", "l3_away": "y"}]
    m = pa.evaluate_1x2(_pred(rows))
    assert m["status"] == "NO_EVALUABLE" and m["n"] == 0


def test_evaluate_1x2_no_source():
    assert pa.evaluate_1x2(None)["status"] == "NO_EVALUABLE"


# ---------------------------------------------------------------- goals
def test_evaluate_goals_mae_and_exact():
    rows = [{"fixture_id": i, "settled": 1, "result_final_gh": 1, "result_final_ga": 0,
             "l3_xg_home": 1.2, "l3_xg_away": 0.7, "l3_top_score": "1-0"} for i in range(35)]
    m = pa.evaluate_goals(_pred(rows))
    assert m["status"] == "ACTIVO" and m["n"] == 35
    assert m["primary_metric"] == "mae_total_goals" and m["primary_value"] is not None
    assert m["secondary"]["exact_scoreline_hit"] == 1.0    # top_score 1-0 == real 1-0
    assert "NO_DISPONIBLE" in m["secondary"]["top3_top5_scoreline"]


# ---------------------------------------------------------------- player modules
def _props(rows):
    cols = ["fixture_id", "settled", "player_id", "team", "p_goal", "act_goal", "p_card", "act_card",
            "p_assist", "act_assist", "p_shot_on", "act_shots_on", "exp_shots", "act_shots"]
    return pd.DataFrame([{c: r.get(c) for c in cols} for r in rows], columns=cols)


def test_evaluate_player_card_binary():
    rows = [{"fixture_id": i, "settled": 1, "player_id": i, "p_card": 0.2,
             "act_card": 1 if i % 5 == 0 else 0} for i in range(40)]
    m = pa.evaluate_player_binary(_props(rows), "Jugadores: tarjetas", "p_card", "act_card")
    assert m["status"] == "ACTIVO" and m["n"] == 40
    assert m["primary_metric"] == "brier" and m["primary_value"] is not None
    assert m["secondary"]["positive_rate_real"] == 0.2


def test_evaluate_player_goal_overprediction_flagged():
    # avg_p 0.30 but real rate 0.0 -> overprediction
    rows = [{"fixture_id": i, "settled": 1, "player_id": i, "p_goal": 0.30, "act_goal": 0}
            for i in range(40)]
    m = pa.evaluate_player_binary(_props(rows), "Jugadores: gol", "p_goal", "act_goal")
    assert "sobre" in m["bias"]
    assert "sobrepredicci" in m["recommendation"].lower()


def test_module_no_evaluable_when_columns_missing():
    df = _props([{"fixture_id": 1, "settled": 1, "player_id": 1}])
    m = pa.evaluate_player_binary(df.drop(columns=["p_card"]), "Jugadores: tarjetas", "p_card", "act_card")
    assert m["status"] == "NO_EVALUABLE"


def test_panel_marks_insufficient_sample():
    rows = [{"fixture_id": i, "settled": 1, "player_id": i, "p_card": 0.2, "act_card": 0}
            for i in range(10)]                            # n=10 < MIN_SAMPLE
    m = pa.evaluate_player_binary(_props(rows), "Jugadores: tarjetas", "p_card", "act_card")
    assert m["status"] == "INSUFFICIENT_SAMPLE"


def test_team_stats_marks_sot_no_evaluable():
    sc = pd.DataFrame([{"stat": "shots", "n": 39, "mae": 7.4, "rmse": 8.9, "bias": -6.0,
                        "mean_pred": 18.3, "mean_real": 24.3, "line_acc": None}])
    mods = pa.evaluate_team_stats(sc)
    names = {m["module"]: m for m in mods}
    assert names["Team stats: tiros"]["status"] == "ACTIVO"
    assert names["Team stats: SOT"]["status"] == "NO_EVALUABLE"


# ---------------------------------------------------------------- report + round trip
def test_report_no_betting_language(tmp_path, monkeypatch):
    pred = _pred([{"fixture_id": i, "settled": 1, "result_1x2": "H", "result_final_gh": 1,
                   "result_final_ga": 0, "l3_home": 0.5, "l3_draw": 0.3, "l3_away": 0.2,
                   "l3_xg_home": 1.3, "l3_xg_away": 0.8, "l3_top_score": "1-0"} for i in range(35)])
    props = _props([{"fixture_id": i, "settled": 1, "player_id": i, "p_card": 0.2,
                     "act_card": 1 if i % 5 == 0 else 0, "p_goal": 0.1, "act_goal": 0,
                     "p_assist": 0.08, "act_assist": 0, "p_shot_on": 0.3, "act_shots_on": 0,
                     "exp_shots": 1.5, "act_shots": 1} for i in range(40)])
    pf = tmp_path / "pred.csv"; pred.to_csv(pf, index=False)
    prf = tmp_path / "props.csv"; props.to_csv(prf, index=False)
    monkeypatch.setattr(pa, "OUT_CSV", tmp_path / "acc.csv")
    monkeypatch.setattr(pa, "OUT_JSON", tmp_path / "acc.json")
    monkeypatch.setattr(pa, "OUT_TXT", tmp_path / "acc.txt")
    monkeypatch.setattr(pa, "SHADOW_MONITOR_JSON", tmp_path / "nope.json")
    summary = pa.build(pred_log=pf, props_log=prf, team_stats=tmp_path / "none.csv", write=True)
    assert (tmp_path / "acc.csv").exists() and (tmp_path / "acc.json").exists()
    txt = pa.render_txt(summary).lower()
    assert "panel de módulos" in txt and "conclusión ejecutiva" in txt
    assert not any(w in txt for w in FORBIDDEN)
    # executive summary should classify modules
    ex = summary["executive_summary"]
    assert "Resultado 1X2" in ex["active_modules"]
