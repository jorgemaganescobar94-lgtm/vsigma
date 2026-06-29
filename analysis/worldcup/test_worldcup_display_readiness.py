"""
Offline tests for the Fase-4O display-correction readiness gate. Read-only, no network, no model, no
API, no market/odds/betting. Cover:
  * NOT_READY_SAMPLE when n<50 even if the correction improves;
  * READY_FOR_PROPOSAL when n>=50 and every gate passes;
  * NOT_READY_NO_SIGNAL when the improvement is not material;
  * NOT_READY_BIAS_INVERSION when the bias strongly inverts;
  * should_propose_activation_any False in the current (live) state;
  * should_propose_activation_any True when a module is ready;
  * Fase 4J surfaces readiness as a SHADOW module;
  * the report carries no betting language;
  * the module touches no market/API endpoint.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import monitor_worldcup_display_correction_readiness as rg  # noqa: E402
import evaluate_worldcup_prediction_accuracy as pa  # noqa: E402


def _m(n, dmae, drmse=0.5, bias_o=1.75, bias_c=0.1, n_corr=40, anti=True):
    return {"n": n, "delta_mae": dmae, "delta_rmse": drmse, "original_bias": bias_o,
            "corrected_bias": bias_c, "n_corrected": n_corr, "anti_available": anti}


# ------------------------------------------------------------------ pure readiness gate
def test_not_ready_sample_when_below_50_even_if_improves():
    g = rg.decide_readiness(_m(38, 0.9))
    assert g["readiness_status"] == "NOT_READY_SAMPLE"
    assert g["sample_gate"] is False and g["improvement_gate"] is True   # signal IS positive


def test_ready_for_proposal_when_all_gates_pass():
    g = rg.decide_readiness(_m(60, 0.5))
    assert g["readiness_status"] == "READY_FOR_PROPOSAL"
    assert all(g[k] for k in ("sample_gate", "improvement_gate", "bias_gate",
                              "no_strong_bias_inversion_gate", "anti_lookahead_available",
                              "data_quality_ok"))


def test_not_ready_no_signal_when_not_material():
    g = rg.decide_readiness(_m(60, 0.05))
    assert g["readiness_status"] == "NOT_READY_NO_SIGNAL" and g["improvement_gate"] is False


def test_not_ready_no_signal_when_no_anti_lookahead():
    g = rg.decide_readiness(_m(60, 0.9, anti=False))
    assert g["readiness_status"] == "NOT_READY_NO_SIGNAL"
    assert g["anti_lookahead_available"] is False


def test_not_ready_bias_inversion_when_strong_flip():
    # bias +1.0 -> -0.9, |−0.9| > 0.5*1.0 -> strong inversion
    g = rg.decide_readiness(_m(60, 0.5, bias_o=1.0, bias_c=-0.9))
    assert g["readiness_status"] == "NOT_READY_BIAS_INVERSION"
    assert g["no_strong_bias_inversion_gate"] is False


def test_watch_when_minor_gate_fails():
    # all good but too few corrected rows -> data quality fails -> WATCH (not NOT_READY)
    g = rg.decide_readiness(_m(60, 0.5, n_corr=5))
    assert g["readiness_status"] == "WATCH" and g["data_quality_ok"] is False


def test_direction_stable_flag():
    assert rg.decide_readiness(_m(60, 0.5))["direction_stable"] is True
    assert rg.decide_readiness(_m(60, 0.5, bias_o=1.0, bias_c=-0.9))["direction_stable"] is False


# ------------------------------------------------------------------ build / global gate
def test_live_state_should_not_propose():
    summary, rows = rg.build(write=False)
    assert summary["should_propose_activation_any"] is False
    assert all(r["readiness_status"] == "NOT_READY_SAMPLE" for r in rows if r["n"])
    # first candidate is the best-signal near-ready module (shots, highest ΔMAE)
    assert summary["first_candidate"] == "team_shots_display_correction"


def test_should_propose_true_when_a_module_ready(monkeypatch):
    monkeypatch.setattr(rg, "load_sot_metrics", lambda: _m(60, 0.5))          # ready
    monkeypatch.setattr(rg, "load_stat_metrics", lambda stat: _m(40, 0.9))    # not enough sample
    # rebuild MODULES table so it uses the patched loaders
    monkeypatch.setattr(rg, "MODULES", [
        ("team_sot_display_correction", "SOT", rg.load_sot_metrics),
        ("team_shots_display_correction", "tiros", lambda: rg.load_stat_metrics("shots")),
    ])
    summary, _rows = rg.build(write=False)
    assert summary["should_propose_activation_any"] is True
    assert "team_sot_display_correction" in summary["ready_modules"]
    assert summary["first_candidate"] == "team_sot_display_correction"


# ------------------------------------------------------------------ Fase 4J integration
def test_phase4j_shows_readiness_shadow(tmp_path):
    summary, _rows = rg.build(write=False)
    p = tmp_path / "ready.json"
    p.write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")
    m = pa.display_readiness_module(p)
    assert m["module"] == "Display correction readiness" and m["status"] == "SHADOW"
    assert m["primary_value"] is False


def test_phase4j_readiness_no_evaluable_when_missing(tmp_path):
    assert pa.display_readiness_module(tmp_path / "absent.json")["status"] == "NO_EVALUABLE"


# ------------------------------------------------------------------ report honesty + isolation
def test_report_no_betting_language():
    summary, rows = rg.build(write=False)
    text = rg.render_txt(summary, rows).lower()
    for bad in ["apuesta", "cuota", "stake", "odds", "edge", "pick", "roi", " bet", "mercado de"]:
        assert bad not in text
    assert "no activar nada en esta fase" in text


def test_no_market_or_api_calls_in_module():
    src = (HERE / "monitor_worldcup_display_correction_readiness.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient",
                "requests.get", "http://", "https://"):
        assert bad not in src
