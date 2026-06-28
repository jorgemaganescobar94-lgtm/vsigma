"""
Offline tests for the auto-learned, reversible STATS LEVEL CORRECTION (shown córners/tiros).
No network, no model, read-only over the model (post-hoc display fix). Covers: the shrunk estimate
(corr = target × N/(N+K), target = −raw_bias), cap, cards EXCLUDED, the additive per-team apply
(proportional split, totals consistent, non-negative clamp), EXACT revert with the flag off (Δ=0),
soft-fail with no state, the scorer reporting raw vs corrected bias, the panel surfacing both, and
that the module touches NO market/odds/API endpoint.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_learning_loop as ll  # noqa: E402
import worldcup_team_stats_scorer as ts  # noqa: E402
import worldcup_stats_level_correction as C  # noqa: E402
import build_worldcup_trackrecord_panel as panel  # noqa: E402

# two real settled matches (totals): (home, away, st_corn, res_corn, st_card, res_card, st_shot, res_shot)
SENEGAL_IRAQ = ("Senegal", "Iraq", 8.57, 15.0, 4.61, 5.0, 18.13, 34.0)
NORWAY_FRANCE = ("Norway", "France", 5.71, 9.0, 3.49, 2.0, 17.21, 28.0)


def _row(spec, fid):
    h, a, sc, rc, scd, rcd, ssh, rsh = spec
    r = {c: np.nan for c in ll.LOG_COLUMNS}
    r.update({"fixture_id": fid, "kickoff_utc": "2026-06-26 19:00", "home": h, "away": a,
              "result_1x2": "H", "settled": 1,
              "st_corners_total": sc, "st_cards_total": scd, "st_shots_total": ssh,
              "st_corners_over": 0.5, "st_corners_line": 7.5,
              "result_corners": rc, "result_cards": rcd, "result_shots": rsh})
    return r


def _log(tmp_path, specs):
    df = pd.DataFrame([_row(s, i + 1) for i, s in enumerate(specs)])[ll.LOG_COLUMNS]
    p = tmp_path / "log.csv"
    df.to_csv(p, index=False)
    return p


# ----------------------------------------------------------------- estimate
def test_estimate_shrink_target_and_excludes_cards(tmp_path):
    est = C.estimate(_log(tmp_path, [SENEGAL_IRAQ, NORWAY_FRANCE]))
    assert set(est) == {"corners", "shots"}        # cards EXCLUDED
    shrink = 2 / (2 + C.K_SHRINK)
    # shots: raw_bias mean(-15.87,-10.79) = -13.33 -> target +13.33 -> corr target*shrink
    assert est["shots"]["raw_bias"] == pytest.approx(-13.33, abs=1e-2)
    assert est["shots"]["target"] == pytest.approx(13.33, abs=1e-2)
    assert est["shots"]["shrink"] == pytest.approx(shrink, abs=1e-6)
    assert est["shots"]["correction_total"] == pytest.approx(13.33 * shrink, abs=1e-2)
    # corners: raw_bias mean(-6.43,-3.29) = -4.86
    assert est["corners"]["correction_total"] == pytest.approx(4.86 * shrink, abs=1e-2)
    assert est["shots"]["correction_total"] > 0   # additive UP (model under-estimates)


def test_cap_applied(tmp_path, monkeypatch):
    monkeypatch.setitem(C.CAP_TOTAL, "shots", 0.5)
    est = C.estimate(_log(tmp_path, [SENEGAL_IRAQ, NORWAY_FRANCE]))
    assert est["shots"]["capped"] is True
    assert est["shots"]["correction_total"] == pytest.approx(0.5, abs=1e-9)


def test_estimate_grows_toward_full_bias_with_n(tmp_path):
    """More matches -> larger shrink -> correction closer to the full bias (auto-learning)."""
    small = C.estimate(_log(tmp_path, [SENEGAL_IRAQ, NORWAY_FRANCE]))
    big = C.estimate(_log(tmp_path, [SENEGAL_IRAQ, NORWAY_FRANCE] * 30))
    assert big["shots"]["shrink"] > small["shots"]["shrink"]
    assert abs(big["shots"]["correction_total"]) > abs(small["shots"]["correction_total"])


# ----------------------------------------------------------------- apply (display only)
def _state(tmp_path, corners=2.0, shots=6.0):
    p = tmp_path / "state.csv"
    pd.DataFrame([
        {"stat": "corners", "n": 38, "raw_bias": -2.0, "target": 2.0, "shrink": 0.6,
         "correction_total": corners, "k": 25.0, "cap": 4.0, "capped": False},
        {"stat": "shots", "n": 38, "raw_bias": -6.0, "target": 6.0, "shrink": 0.6,
         "correction_total": shots, "k": 25.0, "cap": 8.0, "capped": False},
    ]).to_csv(p, index=False)
    return p


def _card_df():
    return pd.DataFrame([{
        "home": "A", "away": "B",
        "st_corners_home": 4.0, "st_corners_away": 2.0, "st_corners_total": 6.0,
        "st_shots_home": 10.0, "st_shots_away": 5.0, "st_shots_total": 15.0,
        "st_cards_total": 3.0,
    }])


def test_apply_additive_proportional_and_cards_untouched(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "STATS_LEVEL_CORRECTION", True)
    df = _card_df()
    n = C.apply_to_df(df, state_path=_state(tmp_path))
    assert n == 2
    r = df.iloc[0]
    # shots split proportional 10:5 -> home gets 6*2/3=4.0, away 6*1/3=2.0
    assert r["st_shots_home"] == pytest.approx(14.0, abs=1e-6)
    assert r["st_shots_away"] == pytest.approx(7.0, abs=1e-6)
    assert r["st_shots_total"] == pytest.approx(21.0, abs=1e-6)   # total = home+away
    # corners 4:2 -> home 2*2/3=1.333, away 0.667
    assert r["st_corners_home"] == pytest.approx(5.3333, abs=1e-3)
    assert r["st_corners_away"] == pytest.approx(2.6667, abs=1e-3)
    assert r["st_corners_total"] == pytest.approx(8.0, abs=1e-6)
    # dominant team rises more (proportional split)
    assert (14.0 - 10.0) > (7.0 - 5.0)
    # CARDS NEVER touched
    assert r["st_cards_total"] == pytest.approx(3.0, abs=1e-12)


def test_flag_off_is_exact_revert(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "STATS_LEVEL_CORRECTION", False)
    df = _card_df()
    ref = df.copy()
    n = C.apply_to_df(df, state_path=_state(tmp_path))
    assert n == 0
    for col in ("st_corners_home", "st_corners_away", "st_corners_total",
                "st_shots_home", "st_shots_away", "st_shots_total", "st_cards_total"):
        assert (df[col] - ref[col]).abs().max() == 0.0      # Δ=0 EXACT


def test_no_state_no_correction(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "STATS_LEVEL_CORRECTION", True)
    df = _card_df()
    ref = df.copy()
    assert C.apply_to_df(df, state_path=tmp_path / "nope.csv") == 0
    assert (df["st_shots_home"] - ref["st_shots_home"]).abs().max() == 0.0


def test_non_negative_clamp(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "STATS_LEVEL_CORRECTION", True)
    df = _card_df()
    C.apply_to_df(df, state_path=_state(tmp_path, shots=-100.0))
    assert df.iloc[0]["st_shots_home"] >= 0.0 and df.iloc[0]["st_shots_away"] >= 0.0


def test_load_corrections_respects_flag(tmp_path, monkeypatch):
    st = _state(tmp_path)
    monkeypatch.setattr(C, "STATS_LEVEL_CORRECTION", False)
    assert C.load_corrections(st) == {}
    monkeypatch.setattr(C, "STATS_LEVEL_CORRECTION", True)
    got = C.load_corrections(st)
    assert set(got) == {"corners", "shots"} and got["shots"] == pytest.approx(6.0)


# ----------------------------------------------------------------- scorer raw vs corrected (req 4)
def test_scorer_reports_raw_and_corrected_bias(tmp_path, monkeypatch):
    log = _log(tmp_path, [SENEGAL_IRAQ, NORWAY_FRANCE])
    state = _state(tmp_path, corners=2.0, shots=6.0)
    monkeypatch.setattr(ts, "CORRECTION_CSV", state)
    res = ts.compute_from_log(log)
    rc = next(r for r in res["rows"] if r["stat"] == "corners")
    rs = next(r for r in res["rows"] if r["stat"] == "shots")
    rcd = next(r for r in res["rows"] if r["stat"] == "cards")
    # corrected = raw + correction_total ; |corrected| < |raw| (bias drops toward 0)
    assert rs["bias_corr"] == pytest.approx(rs["bias"] + 6.0, abs=1e-6)
    assert abs(rs["bias_corr"]) < abs(rs["bias"])
    assert rc["bias_corr"] == pytest.approx(rc["bias"] + 2.0, abs=1e-6)
    # cards have NO correction
    assert rcd["bias_corr"] is None


def test_scorer_no_state_corrected_is_none(tmp_path, monkeypatch):
    log = _log(tmp_path, [SENEGAL_IRAQ, NORWAY_FRANCE])
    monkeypatch.setattr(ts, "CORRECTION_CSV", tmp_path / "nope.csv")
    res = ts.compute_from_log(log)
    assert all(r.get("bias_corr") is None for r in res["rows"])


# ----------------------------------------------------------------- panel surface
def test_panel_shows_raw_and_corrected_columns():
    csv = ("stat,n,mae,rmse,bias,bias_corr,mean_pred,mean_real,line_acc\n"
           "corners,38,2.56,3.03,-1.47,-0.58,7.0,8.5,47.0\n"
           "shots,38,7.56,9.01,-6.15,-2.44,18.3,24.5,\n"
           "cards,38,1.88,2.19,1.53,,4.2,2.6,\n")
    body = "\n".join(panel.section_team_stats(csv))
    assert "sesgo crudo" in body and "sesgo corregido" in body
    assert "-0.58" in body and "-2.44" in body          # corrected values surfaced
    assert "no corregido" in body                        # cards: no correction
    assert "Tarjetas EXCLUIDAS" in body
    assert "STATS_LEVEL_CORRECTION" in body


# ----------------------------------------------------------------- isolation
def test_no_market_or_api_calls_in_module():
    src = (HERE / "worldcup_stats_level_correction.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient"):
        assert bad not in src
