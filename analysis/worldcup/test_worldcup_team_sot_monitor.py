"""
Offline tests for Fase 4N: the team-SOT correction ACTIVATION MONITOR and the team-stats (shots/corners)
level-correction SHADOW evaluator. Read-only, no network, no model, no API, no market/odds/betting.
Cover:
  * monitor returns False if n<50 even when the signal improves;
  * monitor returns True if n>=50 and the improvement is material;
  * monitor returns False if the improvement is not material;
  * monitor blocks activation on a strong bias inversion;
  * team-stats shadow marks NEEDS_PER_FIXTURE_DATA when only the aggregated scorecard exists;
  * team-stats shadow evaluates ratio/bias/pre_fixture when per-fixture rows exist;
  * Fase 4J surfaces all the new shadow modules;
  * the reports carry no betting language;
  * the modules touch no market/API endpoint.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import monitor_worldcup_team_sot_correction_shadow as mon  # noqa: E402
import evaluate_worldcup_team_stats_level_correction_shadow as ss  # noqa: E402
import evaluate_worldcup_prediction_accuracy as pa  # noqa: E402


# ------------------------------------------------------------------ activation gate (pure)
def _metrics(n, dmae, drmse=0.5, bias_o=1.75, bias_c=0.1, n_corr=40):
    return {"n_team_rows": n, "delta_mae_pre_fixture": dmae, "delta_rmse_pre_fixture": drmse,
            "original_bias": bias_o, "pre_fixture_bias": bias_c, "n_corrected": n_corr}


def test_monitor_false_when_sample_below_50_even_if_improves():
    should, reason, gates = mon.decide_activation(_metrics(38, 0.9))
    assert should is False
    assert gates["sample_ge_min"] is False
    assert gates["delta_mae_material"] is True          # the signal IS positive
    assert "38" in reason


def test_monitor_true_when_sample_and_material():
    should, _r, gates = mon.decide_activation(_metrics(60, 0.5))
    assert should is True and all(gates.values())


def test_monitor_false_when_improvement_not_material():
    should, _r, gates = mon.decide_activation(_metrics(60, 0.05))
    assert should is False and gates["delta_mae_material"] is False


def test_monitor_false_on_strong_bias_inversion():
    # bias flips +1.0 -> -0.9 and |−0.9| > 0.5*1.0 -> strong inversion blocks activation
    should, _r, gates = mon.decide_activation(_metrics(60, 0.5, bias_o=1.0, bias_c=-0.9))
    assert should is False and gates["no_strong_inversion"] is False


def test_monitor_false_when_too_few_corrected_rows():
    should, _r, gates = mon.decide_activation(_metrics(60, 0.5, n_corr=5))
    assert should is False and gates["data_quality_ok"] is False


def test_monitor_extract_metrics_from_summary():
    summary = {"n_team_rows": 38, "n_fixtures": 19, "original": {"mae": 2.34, "rmse": 2.66, "bias": 1.75},
               "anti_look_ahead": {"pre_fixture": {"mae_corrected_on_corrected": 1.45,
                                                   "rmse_corrected_on_corrected": 1.94,
                                                   "bias_corrected_on_corrected": 0.09,
                                                   "delta_mae_on_corrected": 0.89,
                                                   "delta_rmse_on_corrected": 0.72,
                                                   "n_corrected": 32, "n_kept_original": 6}},
               "recommendation": "SHADOW_ONLY"}
    m = mon.extract_metrics(summary)
    assert m["original_bias"] == 1.75 and m["pre_fixture_bias"] == 0.09
    assert m["bias_reduction"] == pytest.approx(abs(1.75) - abs(0.09))
    should, _r, _g = mon.decide_activation(m)
    assert should is False                              # n=38 < 50


# ------------------------------------------------------------------ team-stats shadow
def _ev(n_fix, pred, act):
    rows = []
    for f in range(n_fix):
        rows.append({"fixture_id": 500 + f, "kickoff_utc": f"2026-06-{f + 1:02d} 18:00",
                     "pred": float(pred), "act": float(act)})
    return pd.DataFrame(rows)


def test_stats_shadow_needs_per_fixture_when_only_aggregate():
    agg = {"n": 39, "mae": 7.42, "rmse": 8.9, "bias": -6.05}
    res = ss.evaluate_stat("shots", pd.DataFrame(), agg)       # empty per-fixture ev
    assert res["mode"] == "aggregate_only" and res["recommendation"] == "NEEDS_PER_FIXTURE_DATA"
    assert res["rows"][0]["correction_type"] == "aggregate_only"


def test_stats_shadow_evaluates_ratio_and_bias_with_per_fixture():
    ev = _ev(12, pred=18.0, act=24.0)                  # under-prediction -> ratio > 1
    res = ss.evaluate_stat("shots", ev, None)
    assert res["mode"] == "per_fixture" and res["n"] == 12
    assert res["global_ratio"] == pytest.approx(24.0 / 18.0, abs=1e-3)
    types = {r["correction_type"] for r in res["rows"]}
    assert {"global_ratio", "global_bias", "pre_fixture", "leave_one_out"} <= types
    gr = next(r for r in res["rows"] if r["correction_type"] == "global_ratio")
    assert gr["corrected_mae"] is not None and gr["delta_mae"] is not None


def test_stats_shadow_loads_real_stats_have_per_fixture_data():
    """The live predictions log DOES carry per-fixture totals -> shots/corners must be per_fixture."""
    summary, _rows, results = ss.build(write=False)
    for stat in ("shots", "corners"):
        if stat in results and results[stat]["n"]:
            assert results[stat]["mode"] == "per_fixture"


# ------------------------------------------------------------------ Fase 4J integration
def test_phase4j_shows_sot_monitor_shadow(tmp_path):
    out = {"n_team_rows": 38, "should_activate_display_correction": False,
           "delta_mae_pre_fixture": 0.89, "delta_rmse_pre_fixture": 0.72, "bias_reduction": 1.65,
           "original_bias": 1.75, "pre_fixture_bias": 0.09, "activation_gates": {"sample_ge_min": False},
           "thresholds": {"n_min_activate": 50}, "decision_reason": "n=38 < 50."}
    p = tmp_path / "mon.json"; p.write_text(json.dumps(out), encoding="utf-8")
    m = pa.team_sot_monitor_module(p)
    assert m["module"] == "Team SOT correction monitor" and m["status"] == "SHADOW"
    assert m["primary_value"] is False


def test_phase4j_sot_monitor_no_evaluable_when_missing(tmp_path):
    assert pa.team_sot_monitor_module(tmp_path / "absent.json")["status"] == "NO_EVALUABLE"


def test_phase4j_stats_shadow_modules(tmp_path):
    summary = {"stats": {"shots": {"mode": "per_fixture", "n": 39,
                                   "original": {"mae": 7.42, "rmse": 8.9, "bias": -6.05},
                                   "global_ratio": 1.33, "cumulative_best_delta_mae": 2.36,
                                   "pre_fixture": {"delta_mae": 2.02, "delta_rmse": 0.7,
                                                   "corrected_bias": 0.57, "n_corrected": 33},
                                   "recommendation": "SHADOW_ONLY"},
                         "corners": {"mode": "aggregate_only", "n": 39,
                                     "original": {"mae": 2.53, "rmse": 3.0, "bias": -1.39},
                                     "recommendation": "NEEDS_PER_FIXTURE_DATA",
                                     "reason": "solo agregado"}}}
    p = tmp_path / "stats.json"; p.write_text(json.dumps(summary), encoding="utf-8")
    ms = pa.team_stats_correction_shadow_module("shots", "Team shots level correction", p)
    mc = pa.team_stats_correction_shadow_module("corners", "Team corners level correction", p)
    assert ms["status"] == "SHADOW" and ms["primary_value"] == 2.02
    assert mc["status"] == "NEEDS_PER_FIXTURE_DATA"


def test_phase4j_stats_shadow_no_evaluable_when_missing(tmp_path):
    m = pa.team_stats_correction_shadow_module("shots", "Team shots level correction", tmp_path / "x.json")
    assert m["status"] == "NO_EVALUABLE"


# ------------------------------------------------------------------ report honesty + isolation
def test_monitor_report_no_betting_language():
    out = mon.build(json_path=Path("does_not_exist.json"), write=False)
    text = mon.render_txt(out).lower()
    for bad in ["apuesta", "cuota", "stake", "odds", "edge", "pick", "roi", " bet", "mercado de"]:
        assert bad not in text


def test_stats_report_no_betting_language():
    ev = _ev(12, 18.0, 24.0)
    summary, _rows, results = ss.build(write=False)
    text = ss.render_txt(results, summary).lower()
    for bad in ["apuesta", "cuota", "stake", "odds", "edge", "pick", "roi", " bet", "mercado de"]:
        assert bad not in text


def test_no_market_or_api_calls_in_modules():
    for fn in ("monitor_worldcup_team_sot_correction_shadow.py",
               "evaluate_worldcup_team_stats_level_correction_shadow.py"):
        src = (HERE / fn).read_text(encoding="utf-8")
        for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                    "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient",
                    "requests.get", "http://", "https://"):
            assert bad not in src
