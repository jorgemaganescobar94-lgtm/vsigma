"""
Offline tests for the Fase-4P display-only level-correction REVERSIBLE SKELETON. Read-only, no network,
no model, no API, no market/odds/betting. Cover:
  * missing config -> no correction;
  * global enabled=false -> no correction;
  * module enabled=false -> no correction;
  * readiness NOT_READY_SAMPLE -> no correction;
  * readiness READY_FOR_PROPOSAL + flag true -> correction applies;
  * non-numeric value -> no correction;
  * corrected value never below 0;
  * EXACT reversibility with flags off (display == original byte-for-byte);
  * activation guard BLOCKS the current live state for all three modules;
  * activation guard ALLOWS a synthetic ready state;
  * nothing modifies Telegram / writes files in the apply path;
  * the module touches no market/API endpoint.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import display_level_correction as dlc  # noqa: E402
import monitor_worldcup_display_correction_readiness as rg  # noqa: E402


# ------------------------------------------------------------------ fixtures
def _cfg(global_on=False, module="team_shots", module_on=False, mode="global_ratio", req_ready=True):
    return {"enabled": global_on,
            "modules": {module: {"enabled": module_on, "mode": mode, "requires_readiness": req_ready}}}


def _ready_summary(module="team_shots", status="READY_FOR_PROPOSAL", n=60, propose=True,
                   anti=True, no_inv=True, dmae=0.9):
    key = dlc.READINESS_KEY[module]
    return {"should_propose_activation_any": propose, "ready_modules": [key] if status == "READY_FOR_PROPOSAL" else [],
            "modules": [{"module": key, "readiness_status": status, "n": n,
                         "delta_mae_pre_fixture": dmae,
                         "gates": {"anti_lookahead_available": anti, "no_strong_bias_inversion_gate": no_inv,
                                   "sample_gate": n >= 50}}]}


# ------------------------------------------------------------------ config + apply gate
def test_missing_config_safe_default_no_apply(tmp_path):
    cfg = dlc.load_display_correction_config(tmp_path / "nope.json")
    assert cfg["enabled"] is False and dlc.config_status(cfg) == "all_disabled"
    ok, _r = dlc.should_apply_display_correction("team_sot", _ready_summary("team_sot"), cfg)
    assert ok is False


def test_global_disabled_no_apply():
    ok, reason = dlc.should_apply_display_correction("team_shots", _ready_summary(), _cfg(global_on=False))
    assert ok is False and "global" in reason


def test_module_disabled_no_apply():
    cfg = _cfg(global_on=True, module_on=False)
    ok, reason = dlc.should_apply_display_correction("team_shots", _ready_summary(), cfg)
    assert ok is False and "team_shots" in reason


def test_not_ready_no_apply():
    cfg = _cfg(global_on=True, module_on=True)
    rs = _ready_summary(status="NOT_READY_SAMPLE", propose=False)
    ok, reason = dlc.should_apply_display_correction("team_shots", rs, cfg)
    assert ok is False and "NOT_READY_SAMPLE" in reason


def test_ready_plus_flag_applies():
    cfg = _cfg(global_on=True, module_on=True)
    ok, _r = dlc.should_apply_display_correction("team_shots", _ready_summary(), cfg)
    assert ok is True


# ------------------------------------------------------------------ apply correction
def test_apply_ratio_when_ready_and_enabled():
    cfg = _cfg(global_on=True, module_on=True, mode="global_ratio")
    res = dlc.apply_shots_display_correction(6.0, {"global_ratio": 0.5}, cfg, _ready_summary())
    assert res["correction_applied"] is True and res["display_value"] == pytest.approx(3.0)
    assert res["original_value"] == 6.0 and res["correction_mode"] == "global_ratio"


def test_apply_bias_clips_at_zero():
    cfg = _cfg(global_on=True, module_on=True, mode="global_bias")
    res = dlc.apply_shots_display_correction(3.0, {"global_bias": 10.0}, cfg, _ready_summary())
    assert res["correction_applied"] is True and res["display_value"] == 0.0   # max(0, 3-10)


def test_non_numeric_value_no_apply():
    cfg = _cfg(global_on=True, module_on=True)
    res = dlc.apply_shots_display_correction("n/a", {"global_ratio": 0.5}, cfg, _ready_summary())
    assert res["correction_applied"] is False and res["correction_mode"] == "disabled"
    assert res["display_value"] == "n/a"


def test_no_profile_fallback_original():
    cfg = _cfg(global_on=True, module_on=True, mode="global_ratio")
    res = dlc.apply_shots_display_correction(5.0, {}, cfg, _ready_summary())   # empty profile
    assert res["correction_applied"] is False and res["correction_mode"] == "fallback_no_profile"
    assert res["display_value"] == 5.0


# ------------------------------------------------------------------ EXACT reversibility (flags off)
def test_exact_reversibility_with_flags_off():
    cfg = dlc.load_display_correction_config()       # the real committed config (all OFF)
    assert dlc.config_status(cfg) == "all_disabled"
    rs = rg.build(write=False)[0]                    # live readiness (all NOT_READY_SAMPLE)
    for module, applier in (("team_sot", dlc.apply_sot_display_correction),
                            ("team_shots", dlc.apply_shots_display_correction),
                            ("team_corners", dlc.apply_corners_display_correction)):
        for v in (0.0, 1.0, 4.213, 18.5, 7.7):
            res = applier(v, {"global_ratio": 0.5, "global_bias": 2.0}, cfg, rs)
            assert res["display_value"] == v                 # byte-for-byte original
            assert res["correction_applied"] is False and res["correction_mode"] == "disabled"


def test_corrected_never_below_zero_even_if_applied():
    cfg = _cfg(global_on=True, module_on=True, mode="global_bias")
    for v in (0.0, 0.5, 2.0):
        res = dlc.apply_shots_display_correction(v, {"global_bias": 99.0}, cfg, _ready_summary())
        assert res["display_value"] >= 0.0


# ------------------------------------------------------------------ activation guard
def test_guard_blocks_current_live_state():
    rs = rg.build(write=False)[0]
    cfg = dlc.load_display_correction_config()
    for module in ("team_sot", "team_shots", "team_corners"):
        allowed, _r = dlc.check_activation_allowed(module, rs, cfg)
        assert allowed is False
        with pytest.raises(dlc.DisplayCorrectionActivationError):
            dlc.assert_display_correction_activation_allowed(module, rs, cfg)


def test_guard_allows_synthetic_ready_state():
    cfg = _cfg(global_on=True, module_on=True)
    rs = _ready_summary("team_shots", status="READY_FOR_PROPOSAL", n=60, propose=True)
    allowed, _r = dlc.check_activation_allowed("team_shots", rs, cfg)
    assert allowed is True
    assert dlc.assert_display_correction_activation_allowed("team_shots", rs, cfg) is True


def test_guard_blocks_when_global_gate_false():
    rs = _ready_summary(status="READY_FOR_PROPOSAL", propose=False)   # module ready but global gate off
    allowed, reason = dlc.check_activation_allowed("team_shots", rs, _cfg(True, module_on=True))
    assert allowed is False and "should_propose_activation_any" in reason


def test_guard_blocks_on_bias_inversion():
    rs = _ready_summary(no_inv=False)
    allowed, reason = dlc.check_activation_allowed("team_shots", rs, _cfg(True, module_on=True))
    assert allowed is False and "inversión" in reason


# ------------------------------------------------------------------ --check diagnostic (no writes)
def test_check_reports_no_activation(capsys):
    out = dlc.run_check()
    assert out["global_enabled"] is False and out["config_status"] == "all_disabled"
    assert out["any_activation_allowed"] is False
    text = capsys.readouterr().out.lower()
    assert "no activation" in text and "reversibilidad exacta" in text


def test_check_writes_no_files(tmp_path, monkeypatch):
    # run_check must not create the readiness/scorecard/config files (read-only diagnostic)
    before = set(p.name for p in HERE.glob("worldcup_display_correction_readiness*"))
    dlc.run_check()
    after = set(p.name for p in HERE.glob("worldcup_display_correction_readiness*"))
    assert before == after


# ------------------------------------------------------------------ isolation
def test_no_telegram_or_market_or_api_in_module():
    # No real network / Telegram-send / market call patterns (the prose may mention 'Telegram' to say it
    # is NOT touched; we check for actual CALLS, not the word).
    src = (HERE / "display_level_correction.py").read_text(encoding="utf-8")
    for bad in ("send_message", "sendmessage", "requests.post", "requests.get", "urlopen",
                'request("/odds"', "request('/odds'", ".odds(", ".predictions(", "APIFootballClient",
                "http://", "https://"):
        assert bad.lower() not in src.lower()
