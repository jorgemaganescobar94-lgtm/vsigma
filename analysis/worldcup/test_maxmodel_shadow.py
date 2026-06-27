"""
Tests for the WC MAX shadow model (worldcup_maxmodel_shadow.py). NO network, NO API.
Focus: the ANTI-LEAKAGE invariant of the feature builder + helper sanity. The A/B itself is a
measurement (its verdict lives in the scorecard), so we lock the property that matters: no feature
ever uses the current/future match.

Run:  python -m pytest analysis/worldcup/test_maxmodel_shadow.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import worldcup_maxmodel_shadow as M  # noqa: E402


def test_feature_builder_no_leakage_and_clean():
    df = M.build_features()
    # ordered by date, no NaN in the feature matrix, valid 1X2 target
    assert df["date"].is_monotonic_increasing
    assert not df[M.FEATURES].isna().any().any(), "features must be fully populated (fallback to neutral)"
    assert set(df["res"].unique()) <= {0, 1, 2}
    # ANTI-LEAKAGE: the chronologically FIRST fixture has NO prior history for either team, so every
    # result-derived diff feature must be exactly neutral (0). If any were non-zero, the builder would
    # be peeking at the current/other matches.
    first = df.iloc[0]
    for f in ("gf_diff", "ga_diff", "ppg_diff", "strk_diff", "rest_diff", "h2h"):
        assert abs(float(first[f])) < 1e-9, f"first fixture leaked via {f}={first[f]}"


def test_ou_btts_in_range():
    for lh, la in ((0.3, 2.4), (1.5, 1.5), (2.6, 0.4)):
        o, b = M._ou_btts(lh, la)
        assert 0.0 <= o <= 1.0 and 0.0 <= b <= 1.0
    # higher total -> higher Over 2.5
    assert M._ou_btts(2.5, 2.0)[0] > M._ou_btts(0.5, 0.4)[0]


def test_bootstrap_diff_sign():
    # b strictly better (lower loss) on every row -> obs>0, CI excludes 0, p≈0
    la = np.full(200, 1.0); lb = np.full(200, 0.8)
    obs, lo, hi, p = M._boot_diff(la, lb)
    assert obs > 0 and lo > 0 and p < 0.05


if __name__ == "__main__":
    test_feature_builder_no_leakage_and_clean()
    test_ou_btts_in_range()
    test_bootstrap_diff_sign()
    print("OK")
