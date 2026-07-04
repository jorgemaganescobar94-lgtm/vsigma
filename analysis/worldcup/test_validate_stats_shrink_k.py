"""
Offline tests for the shrink-K validation of the stats level correction (córners/tiros). No network,
no API. Covers: the in-sample residual formula, that _corr_for mirrors the correction module, the
walk-forward overshoot detection, the floor-respecting choice, and the governance fact that the
APPLIED K is 10 (lowered from 25 on 2026-07-04).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import validate_stats_shrink_k as V  # noqa: E402
import worldcup_stats_level_correction as lc  # noqa: E402


def _synthetic_csv(tmp_path, pred_real_corners, pred_real_shots):
    """Write a minimal settled-log CSV that _series can read (ordered by kickoff)."""
    n = len(pred_real_corners)
    rows = []
    for i in range(n):
        pc, rc = pred_real_corners[i]
        ps, rs = pred_real_shots[i]
        rows.append({
            "fixture_id": 1000 + i, "kickoff_utc": f"2026-06-{i+1:02d} 12:00",
            "settled": 1, "result_1x2": "H",
            "st_corners_total": pc, "result_corners": rc,
            "st_shots_total": ps, "result_shots": rs})
    p = tmp_path / "log.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


# ----------------------------------------------------------------- pure formulas
def test_insample_residual_formula():
    pred = np.full(54, 18.0); real = np.full(54, 24.0)   # constant bias -6
    # residual = raw_bias * K/(N+K); K=10 -> -6*10/64 ; K=25 -> -6*25/79
    assert V.insample_residual(pred, real, 10.0, cap=8.0) == pytest.approx(-6 * 10 / 64, abs=1e-6)
    assert V.insample_residual(pred, real, 25.0, cap=8.0) == pytest.approx(-6 * 25 / 79, abs=1e-6)
    # lower K -> smaller |residual| (corrects more)
    assert abs(V.insample_residual(pred, real, 10.0, 8.0)) < abs(V.insample_residual(pred, real, 25.0, 8.0))


def test_corr_for_matches_module():
    """_corr_for must equal what worldcup_stats_level_correction.estimate() would compute (shrink+cap)."""
    pred = np.array([10.0, 12.0, 11.0]); real = np.array([16.0, 18.0, 17.0])   # bias -6
    k, cap = 10.0, 8.0
    got = V._corr_for(pred, real, k, cap)
    raw_bias = float(np.mean(pred - real))
    want = lc._clip(-raw_bias * len(pred) / (len(pred) + k), -cap, cap)
    assert got == pytest.approx(want)


# ----------------------------------------------------------------- walk-forward
def test_stable_underestimate_no_overshoot():
    pred = np.full(40, 18.0); real = np.full(40, 24.0)     # perfectly stable -6 bias
    r_wf, n = V.walk_forward_residual(pred, real, 10.0, cap=8.0)
    assert n == 40
    assert r_wf < 0            # corrected pred stays BELOW real -> no overshoot
    assert r_wf > -6.0         # but the correction did move it toward 0


def test_overshoot_flagged_for_aggressive_low_k():
    """Regime shift: 10 heavy under-estimates then perfectly-calibrated matches. A too-low K learns
    the early bias and OVER-corrects the calibrated tail -> walk-forward residual turns positive."""
    heavy = [(14.0, 24.0)] * 10          # bias -10
    calm = [(24.0, 24.0)] * 30           # bias 0
    pred = np.array([p for p, _ in heavy + calm], float)
    real = np.array([r for _, r in heavy + calm], float)
    r_small, _ = V.walk_forward_residual(pred, real, 3.0, cap=20.0)    # aggressive
    r_big, _ = V.walk_forward_residual(pred, real, 40.0, cap=20.0)     # conservative
    assert r_small > 0        # aggressive K overshoots on average
    assert r_big < r_small     # conservative K overshoots less (or not at all)


# ----------------------------------------------------------------- choice + governance
def test_run_respects_floor_and_picks_ten(tmp_path):
    pc = [(7.0, 9.0)] * 54       # corners bias -2
    ps = [(18.0, 25.0)] * 54     # shots bias -7
    csv = _synthetic_csv(tmp_path, pc, ps)
    chosen, _lines = V.run(csv)
    # stable bias -> no overshoot anywhere -> choice pinned at the regularization floor
    assert chosen["corners"] == V.K_FLOOR == 10.0
    assert chosen["shots"] == V.K_FLOOR == 10.0


def test_applied_k_is_ten():
    """Governance: the correction module ships K=10 (lowered from 25 on 2026-07-04, validated)."""
    assert lc.K_SHRINK == 10.0


def test_k10_beats_k25_residual_without_overshoot(tmp_path):
    """The applied K=10 leaves a SMALLER |residual| than the old K=25, still without overshoot."""
    pred = np.full(54, 7.12); real = np.full(54, 9.07)    # corners-like stable under-estimate
    r10 = V.insample_residual(pred, real, 10.0, cap=4.0)
    r25 = V.insample_residual(pred, real, 25.0, cap=4.0)
    assert abs(r10) < abs(r25)      # corrects more
    assert r10 < 0 and r25 < 0      # neither overshoots (μ_corr < μ_real)
