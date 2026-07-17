"""Offline tests for read-only World Cup evidence diagnostics."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_evidence_diagnostics as ev  # noqa: E402


def test_paired_bootstrap_is_deterministic_and_detects_direction():
    delta = np.array([0.2, 0.3, 0.4, 0.5])
    first = ev.paired_bootstrap(delta, n_bootstrap=2_000, seed=123)
    second = ev.paired_bootstrap(delta, n_bootstrap=2_000, seed=123)
    assert first == second
    assert first["ci95_low"] > 0 and first["conclusion"] == "CANDIDATE_FAVORED"


def test_paired_bootstrap_marks_crossing_zero_inconclusive():
    result = ev.paired_bootstrap([-1.0, 1.0], n_bootstrap=2_000, seed=123)
    assert result["ci95_low"] <= 0 <= result["ci95_high"]
    assert result["conclusion"] == "INCONCLUSIVE"


def test_compare_models_uses_only_common_settled_rows():
    frame = pd.DataFrame([
        {"settled": 1, "result_1x2": "H", "l3_home": .5, "l3_draw": .3, "l3_away": .2,
         "fd_home": .7, "fd_draw": .2, "fd_away": .1},
        {"settled": 0, "result_1x2": None, "l3_home": .3, "l3_draw": .3, "l3_away": .4,
         "fd_home": .2, "fd_draw": .3, "fd_away": .5},
    ])
    rows = ev.compare_models(frame, "full_data", "l3")
    assert len(rows) == 2 and all(row["n"] == 1 for row in rows)
    assert all(row["delta_reference_minus_candidate"] > 0 for row in rows)


def test_disagreement_flags_only_outside_historical_range():
    rows = [
        {"fixture_id": 1, "home": "A", "away": "B", "settled": 1,
         "fd_home": .55, "fd_draw": .25, "fd_away": .20,
         "l3_home": .50, "l3_draw": .27, "l3_away": .23},
        {"fixture_id": 2, "home": "C", "away": "D", "settled": 0,
         "fd_home": .80, "fd_draw": .10, "fd_away": .10,
         "l3_home": .30, "l3_draw": .35, "l3_away": .35},
    ]
    result = ev.disagreement_diagnostics(pd.DataFrame(rows))
    assert result[0]["status"] == "EXTREME_OUTSIDE_SETTLED_RANGE"
    assert result[0]["action"] == "REVIEW_ONLY_NO_MODEL_CHANGE"


def test_live_report_is_read_only_and_has_no_production_effect():
    report = ev.build_report(ev.load_evidence_frame())
    assert report["production_effect"] == "NONE"
    assert report["protocol"]["paired_bootstrap_resamples"] == 10_000
    assert report["protocol"]["seed"] == 20_260_713
    assert report["comparisons"]
