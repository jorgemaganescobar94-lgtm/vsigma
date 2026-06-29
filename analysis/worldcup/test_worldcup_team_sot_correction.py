"""
Offline tests for the Fase-4M team-SOT level-correction evaluator (shadow / display-only). Read-only,
no network, no model, no API, no market/odds/betting. Cover:
  * global ratio cancels the cumulative bias (and shrinks |bias|);
  * subtractive global bias cancels the cumulative bias;
  * pre_fixture uses ONLY strictly-earlier fixtures (not the current one, not future ones);
  * leave_one_fixture_out excludes the evaluated fixture's own rows;
  * with no prior history the original value is kept;
  * no corrected value goes below 0;
  * SHADOW_ONLY when an improvement exists but the sample is below the activation threshold;
  * CONSIDER_DISPLAY_CORRECTION when pre_fixture improves materially with a sufficient sample;
  * Fase 4J surfaces the correction as a SHADOW module (never ACTIVO here);
  * the report carries no betting language;
  * the module touches no market/API endpoint.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import evaluate_worldcup_team_sot_level_correction as lc  # noqa: E402
import evaluate_worldcup_prediction_accuracy as pa  # noqa: E402


# ------------------------------------------------------------------ helpers
def _ev(rows):
    """Build an evaluable DataFrame shaped like load_evaluable() output (sorted, with pred/act)."""
    df = pd.DataFrame(rows)
    for c, d in (("team_name", "T"), ("opponent_id", ""), ("opponent_name", "O"), ("side", "home")):
        if c not in df.columns:
            df[c] = d
    df["pred"] = df["predicted_sot"].astype(float)
    df["act"] = df["actual_sot"].astype(float)
    df["kickoff_utc"] = df["kickoff_utc"].fillna("")
    return df.sort_values(["kickoff_utc", "fixture_id", "team_id"]).reset_index(drop=True)


def _fixtures(n_fix, pred, act, start_day=1):
    """n_fix fixtures, 2 teams each, chronological. pred/act constant -> known ratio act/pred."""
    rows = []
    for f in range(n_fix):
        ko = f"2026-06-{start_day + f:02d} 18:00"
        for t in (0, 1):
            rows.append({"fixture_id": 1000 + f, "kickoff_utc": ko, "team_id": 10 * f + t,
                         "side": "home" if t == 0 else "away",
                         "predicted_sot": pred, "actual_sot": act})
    return rows


# ------------------------------------------------------------------ cumulative corrections cancel bias
def test_global_ratio_cancels_cumulative_bias():
    ev = _ev(_fixtures(6, pred=4.0, act=2.0))      # strong over-prediction, ratio 0.5
    summary, _ = lc.build_summary_and_rows(ev)
    orig_b = summary["original"]["bias"]
    corr_b = summary["cumulative"]["global_ratio"]["bias"]
    assert orig_b > 1.0                            # original over-predicts
    assert abs(corr_b) < abs(orig_b)               # ratio shrinks |bias|
    assert abs(corr_b) < 1e-6                       # and cancels it on the fit sample
    assert summary["cumulative"]["global_ratio"]["ratio"] == pytest.approx(0.5)


def test_global_bias_subtraction_cancels_cumulative_bias():
    ev = _ev(_fixtures(6, pred=4.0, act=2.0))
    summary, _ = lc.build_summary_and_rows(ev)
    assert summary["cumulative"]["global_bias"]["bias_subtracted"] == pytest.approx(2.0)
    assert abs(summary["cumulative"]["global_bias"]["bias"]) < 1e-6


# ------------------------------------------------------------------ pre_fixture anti-look-ahead
def test_pre_fixture_uses_only_earlier_fixtures():
    # 3 history fixtures pred=2 act=1 (ratio 0.5), then a 4th fixture whose OWN actual is extreme.
    rows = _fixtures(3, pred=2.0, act=1.0, start_day=1)
    rows += [{"fixture_id": 2000, "kickoff_utc": "2026-06-10 18:00", "team_id": 99, "side": "home",
              "predicted_sot": 4.0, "actual_sot": 99.0},      # extreme own/future-looking value
             {"fixture_id": 2000, "kickoff_utc": "2026-06-10 18:00", "team_id": 98, "side": "away",
              "predicted_sot": 4.0, "actual_sot": 99.0}]
    ev = _ev(rows)
    corrected, modes, _ = lc.pre_fixture_correction(ev)
    pos = ev.index[ev["fixture_id"] == 2000].tolist()
    # ratio fit from history (pred2/act1 -> 0.5) only -> 4*0.5 = 2.0, regardless of the 99 actual
    for i in pos:
        assert modes[i] == "pre_fixture_applied"
        assert corrected[i] == pytest.approx(2.0)


def test_pre_fixture_keeps_original_without_history():
    ev = _ev(_fixtures(6, pred=4.0, act=2.0))
    corrected, modes, confs = lc.pre_fixture_correction(ev)
    first_fix = ev["fixture_id"].iloc[0]
    pos = ev.index[ev["fixture_id"] == first_fix].tolist()
    for i in pos:                                   # first fixture has no earlier history
        assert modes[i] == "pre_fixture_kept_original"
        assert confs[i] == "baja"
        assert corrected[i] == pytest.approx(float(ev.at[i, "pred"]))


def test_leave_one_out_excludes_evaluated_fixture():
    ev = _ev(_fixtures(5, pred=4.0, act=2.0))
    # make ONE fixture an outlier so excluding it changes the ratio detectably
    ev.loc[ev["fixture_id"] == 1000, "act"] = 8.0
    corrected = lc.leave_one_fixture_out_correction(ev)
    rest = ev[ev["fixture_id"] != 1000]
    ratio_excl = rest["act"].mean() / rest["pred"].mean()
    for i in ev.index[ev["fixture_id"] == 1000].tolist():
        assert corrected[i] == pytest.approx(float(ev.at[i, "pred"]) * ratio_excl)


# ------------------------------------------------------------------ clip >= 0
def test_corrected_never_below_zero():
    # tiny predictions with a large global bias would push subtractive correction negative -> clip 0
    rows = _fixtures(4, pred=1.0, act=0.0)          # global_bias = 1.0 > pred -> would be negative
    ev = _ev(rows)
    _summary, out = lc.build_summary_and_rows(ev)
    for r in out:
        assert r["corrected_sot_global_ratio"] >= 0
        assert r["corrected_sot_global_bias"] >= 0
        assert r["corrected_sot_home_away_ratio"] >= 0
        assert r["corrected_sot_pre_fixture"] >= 0
        assert r["corrected_sot_leave_one_out"] >= 0


# ------------------------------------------------------------------ recommendation
def test_recommendation_shadow_only_when_sample_below_threshold():
    ev = _ev(_fixtures(10, pred=4.0, act=2.0))      # n=20 < 50 but pre_fixture improves
    summary, _ = lc.build_summary_and_rows(ev)
    assert summary["n_team_rows"] < lc.N_MIN_ACTIVATE
    assert summary["recommendation"] == "SHADOW_ONLY"


def test_recommendation_consider_when_material_and_enough_sample():
    ev = _ev(_fixtures(30, pred=4.0, act=2.0))      # n=60 >= 50, strong consistent over-prediction
    summary, _ = lc.build_summary_and_rows(ev)
    assert summary["n_team_rows"] >= lc.N_MIN_ACTIVATE
    pf = summary["anti_look_ahead"]["pre_fixture"]
    assert pf["delta_mae_on_corrected"] >= lc.DELTA_MAE_MATERIAL
    assert summary["recommendation"] == "CONSIDER_DISPLAY_CORRECTION"


def test_no_change_when_empty():
    summary, rows = lc.build_summary_and_rows(_ev_empty())
    assert summary["recommendation"] == "NO_CHANGE" and summary["n_team_rows"] == 0 and rows == []


def _ev_empty():
    return pd.DataFrame()


# ------------------------------------------------------------------ Fase 4J integration (SHADOW)
def test_phase4j_shows_correction_as_shadow(tmp_path):
    ev = _ev(_fixtures(10, pred=4.0, act=2.0))
    summary, _ = lc.build_summary_and_rows(ev)
    p = tmp_path / "sum.json"
    p.write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")
    m = pa.team_sot_correction_module(p)
    assert m["module"] == "Team SOT level correction" and m["status"] == "SHADOW"
    assert m["primary_metric"] == "delta_mae_pre_fixture" and m["primary_value"] is not None
    assert "shadow" in m["recommendation"].lower()


def test_phase4j_correction_no_evaluable_when_missing(tmp_path):
    m = pa.team_sot_correction_module(tmp_path / "absent.json")
    assert m["status"] == "NO_EVALUABLE" and m["n"] == 0


# ------------------------------------------------------------------ report honesty + isolation
def test_report_has_no_betting_language():
    ev = _ev(_fixtures(10, pred=4.0, act=2.0))
    summary, _ = lc.build_summary_and_rows(ev)
    text = lc.render_txt(summary).lower()
    for bad in ["apuesta", "cuota", "stake", "odds", "edge", "pick", "roi", " bet", "mercado de"]:
        assert bad not in text
    assert "shadow" in text and "no se aplica" in text


def test_empty_report_soft():
    summary, _ = lc.build_summary_and_rows(_ev_empty())
    assert "sin filas evaluables" in lc.render_txt(summary)


def test_no_market_or_api_calls_in_module():
    src = (HERE / "evaluate_worldcup_team_sot_level_correction.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient",
                "requests.get", "http://", "https://"):
        assert bad not in src
