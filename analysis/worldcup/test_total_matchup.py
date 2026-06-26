"""
Offline tests for the MATCH-DEPENDENT GOAL TOTAL (auditoría candidato #1, forma b) integrated into
the L3 predictor. NO network, NO API.

Covers: total_goals forma b vs constant · raw_xg keeps the DIFFERENCE (1X2 driver) unchanged and only
moves the TOTAL · matchup raises the total in mismatches · Predictor picks total+isotonic by the
matchup flag and exposes the *_const A/B fields · the flag reverts exactly to the constant path · the
committed calibration JSON carries total_coef + iso_const · learning_loop has the A/B log columns.

Run:  python analysis/worldcup/test_total_matchup.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import l3_offline as LO                      # noqa: E402
import worldcup_learning_loop as LL          # noqa: E402

CALIB = HERE / "national_elo_layer3_calibration.json"
IDENT = {"ux": [0.0, 1.0], "uf": [0.0, 1.0]}


def _calib(total_coef=None):
    # iso (matchup) = identity; iso_const = a DIFFERENT curve (so we can tell which one was used)
    return {"a0": 0.0, "a1": 1.0, "total_mean": 2.0, "total_coef": total_coef,
            "iso": [dict(IDENT), dict(IDENT), dict(IDENT)],
            "iso_const": [{"ux": [0.0, 1.0], "uf": [0.10, 0.90]}] * 3}


# ----------------------------------------------------------------- total / raw_xg math
def test_total_goals_forma_b_vs_const():
    coef = [2.0, 0.5, 0.1]
    assert LO.total_goals(1.0, 2.0, coef, matchup=True) == 2.0 + 0.5 * 1.0 + 0.1 * 1.0
    assert LO.total_goals(-2.0, 2.0, coef, matchup=True) == 2.0 + 0.5 * 2.0 + 0.1 * 4.0  # |sup| & sup^2
    assert LO.total_goals(1.0, 2.0, coef, matchup=False) == 2.0                          # constant
    assert LO.total_goals(1.0, 2.0, None, matchup=True) == 2.0                            # no coef -> const


def test_raw_xg_difference_is_unchanged_by_total():
    # the 1X2 driver is the DIFFERENCE lh-la = s = a0+a1*sup; it must NOT depend on the total mode
    coef = [2.0, 0.5, 0.1]
    for sup in (-1.5, -0.3, 0.0, 0.8, 1.7):
        lh_m, la_m = LO.raw_xg(sup, -0.1, 1.5, 2.6, coef, matchup=True)
        lh_c, la_c = LO.raw_xg(sup, -0.1, 1.5, 2.6, coef, matchup=False)
        if min(lh_m, la_m, lh_c, la_c) > 0.05:   # away from the xg floor
            assert abs((lh_m - la_m) - (lh_c - la_c)) < 1e-9


def test_matchup_raises_total_in_mismatch():
    # committed forma b has tb1,tb2 > 0 -> bigger |sup| -> bigger total
    coef = [2.39, 0.075, 0.273]
    t_even = LO.total_goals(0.0, 2.66, coef, matchup=True)
    t_big = LO.total_goals(1.5, 2.66, coef, matchup=True)
    assert t_big > t_even                       # mismatch -> more goals
    lh, la = LO.raw_xg(1.5, -0.1, 1.5, 2.66, coef, matchup=True)
    lhc, lac = LO.raw_xg(1.5, -0.1, 1.5, 2.66, coef, matchup=False)
    assert (lh + la) > (lhc + lac)              # matchup total > constant total in a mismatch


# ----------------------------------------------------------------- Predictor flag / A/B
def test_predictor_matchup_uses_total_coef_and_iso():
    p = LO.Predictor({"A": 1.0, "B": 0.0}, _calib([2.0, 0.5, 0.1]))
    cal_m, lh_m, la_m = p._predict_with(1.0, matchup=True)
    cal_c, lh_c, la_c = p._predict_with(1.0, matchup=False)
    assert abs((lh_m + la_m) - 2.6) < 1e-9      # matchup total = 2.0+0.5+0.1
    assert abs((lh_c + la_c) - 2.0) < 1e-9      # constant total_mean
    # different isotonic used (iso vs iso_const) -> calibrated probs differ
    assert not np.allclose(cal_m, cal_c)


def test_predict_attaches_const_ab_fields():
    p = LO.Predictor({"A": 1.0, "B": 0.0}, _calib([2.0, 0.5, 0.1]))
    out = p.predict("A", "B")
    for k in ("our_xg_home_const", "our_xg_away_const", "our_home_const", "our_draw_const", "our_away_const"):
        assert k in out
    # with total_coef present, live (matchup) xG total != constant xG total in a mismatch
    assert abs((out["our_xg_home"] + out["our_xg_away"]) - (out["our_xg_home_const"] + out["our_xg_away_const"])) > 1e-6


def test_flag_off_uses_constant_path(monkeypatch=None):
    # _predict_with(matchup=False) is the exact constant path (total_mean + iso_const), independent of
    # total_coef -> identical whether or not coefficients are present
    p_with = LO.Predictor({"A": 1.0, "B": 0.0}, _calib([2.0, 0.5, 0.1]))
    p_none = LO.Predictor({"A": 1.0, "B": 0.0}, _calib(None))
    a = p_with._predict_with(1.0, matchup=False)
    b = p_none._predict_with(1.0, matchup=False)
    assert np.allclose(a[0], b[0]) and abs(a[1] - b[1]) < 1e-9 and abs(a[2] - b[2]) < 1e-9


def test_no_rating_returns_none():
    assert LO.Predictor({"A": 1.0}, _calib([2.0, 0.5, 0.1])).predict("A", "ZZ") is None


# ----------------------------------------------------------------- committed artifacts
def test_committed_calibration_has_total_fields():
    c = json.loads(CALIB.read_text(encoding="utf-8"))
    assert "total_coef" in c and len(c["total_coef"]) == 3
    assert "iso_const" in c and "total_mean" in c
    assert c["total_coef"][1] > 0 and c["total_coef"][2] > 0   # forma b: total rises with |sup|/sup^2


def test_learning_loop_has_ab_columns():
    assert "l3_xg_home_const" in LL.LOG_COLUMNS and "l3_xg_away_const" in LL.LOG_COLUMNS


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} total-matchup tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
