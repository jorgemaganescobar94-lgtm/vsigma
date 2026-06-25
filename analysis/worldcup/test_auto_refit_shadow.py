"""
Offline tests for auto_refit_shadow.py — append/dedup, the gate sub-checks, and the
SHADOW no-touch guarantee (main() must never write the production ratings file).

Run:  python analysis/worldcup/test_auto_refit_shadow.py
"""
from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import auto_refit_shadow as S  # noqa: E402

HERE = Path(__file__).resolve().parent

BASE_COLS = ["fixture_id", "date", "league_id", "league_tag", "season", "neutral",
             "home_id", "home", "away_id", "away", "gh", "ga", "venue_city"]


def _base():
    return pd.DataFrame([
        {"fixture_id": 1, "date": "2026-06-11T19:00:00+00:00", "league_id": 1, "league_tag": "WC",
         "season": 2026, "neutral": 1, "home_id": 100, "home": "Alpha", "away_id": 200, "away": "Beta",
         "gh": 1, "ga": 0, "venue_city": "X"},
        {"fixture_id": 2, "date": "2026-06-12T19:00:00+00:00", "league_id": 1, "league_tag": "WC",
         "season": 2026, "neutral": 1, "home_id": 200, "home": "Beta", "away_id": 300, "away": "Gamma",
         "gh": 2, "ga": 2, "venue_city": "Y"},
    ], columns=BASE_COLS)


def _log(rows):
    cols = ["fixture_id", "kickoff_utc", "home", "away", "round", "settled",
            "result_ft_gh", "result_ft_ga"]
    return pd.DataFrame(rows, columns=cols)


def test_append_adds_only_new_settled_mapped():
    base = _base()
    log = _log([
        # already in base (fid 1) -> skip
        {"fixture_id": 1, "kickoff_utc": "2026-06-11 19:00", "home": "Alpha", "away": "Beta",
         "round": "G1", "settled": 1, "result_ft_gh": 1, "result_ft_ga": 0},
        # NEW, both teams known -> add
        {"fixture_id": 9, "kickoff_utc": "2026-06-20 19:00", "home": "Alpha", "away": "Gamma",
         "round": "G3", "settled": 1, "result_ft_gh": 3, "result_ft_ga": 1},
        # NEW but unsettled -> skip
        {"fixture_id": 10, "kickoff_utc": "2026-06-21 19:00", "home": "Beta", "away": "Gamma",
         "round": "G3", "settled": 0, "result_ft_gh": np.nan, "result_ft_ga": np.nan},
        # NEW but unknown team -> unmapped, skip
        {"fixture_id": 11, "kickoff_utc": "2026-06-21 19:00", "home": "Zeta", "away": "Alpha",
         "round": "G3", "settled": 1, "result_ft_gh": 0, "result_ft_ga": 0},
    ])
    enriched, new_rows, unmapped = S.build_enriched(base, log)
    assert len(new_rows) == 1 and new_rows[0]["fixture_id"] == 9
    assert new_rows[0]["neutral"] == 1 and new_rows[0]["league_tag"] == "WC"
    assert new_rows[0]["home_id"] == 100 and new_rows[0]["away_id"] == 300
    assert new_rows[0]["date"] == "2026-06-20T19:00:00+00:00"
    assert len(unmapped) == 1 and unmapped[0] == ("Zeta", "Alpha")
    assert len(enriched) == len(base) + 1


def test_append_dedupes_repeated_fixture_in_log():
    base = _base()
    log = _log([
        {"fixture_id": 9, "kickoff_utc": "2026-06-20 19:00", "home": "Alpha", "away": "Gamma",
         "round": "G3", "settled": 1, "result_ft_gh": 3, "result_ft_ga": 1},
        {"fixture_id": 9, "kickoff_utc": "2026-06-20 19:00", "home": "Alpha", "away": "Gamma",
         "round": "G3", "settled": 1, "result_ft_gh": 3, "result_ft_ga": 1},
    ])
    _, new_rows, _ = S.build_enriched(base, log)
    assert len(new_rows) == 1  # deduped


def test_gate_finite():
    assert S.check_finite({1: 0.5, 2: -1.0}) is True
    assert S.check_finite({1: 0.5, 2: float("nan")}) is False
    assert S.check_finite({1: float("inf")}) is False
    assert S.check_finite({}) is False


def test_gate_team_count_non_decreasing():
    assert S.team_count_ok({1: 0, 2: 0, 3: 0}, {1: 0, 2: 0}) is True
    assert S.team_count_ok({1: 0}, {1: 0, 2: 0}) is False


def test_gate_max_move():
    cand = {1: 1.00, 2: 0.50, 3: 2.00}
    comm = {1: 0.90, 2: 0.20, 3: 2.05}
    mv, tid, old, new = S.max_move(cand, comm)
    assert tid == 2 and abs(mv - 0.30) < 1e-9


def test_gate_oos_not_worse():
    good = S.oos_not_worse({"n": 10, "logloss": 0.9, "ECE": 0.02},
                           {"n": 10, "logloss": 0.9, "ECE": 0.02})
    worse = S.oos_not_worse({"n": 10, "logloss": 0.9, "ECE": 0.02},
                            {"n": 10, "logloss": 0.95, "ECE": 0.02})
    assert good is True and worse is False


def test_gate_aggregate_fail_on_big_move():
    cand = {1: 1.00, 2: 0.50}
    comm = {1: 0.00, 2: 0.50}   # team 1 moved 1.0 > cap 0.6
    g = S.evaluate_gate(cand, comm, repro=0.0,
                        mo={"n": 5, "logloss": 0.9, "ECE": 0.02},
                        mn={"n": 5, "logloss": 0.9, "ECE": 0.02})
    assert g["ok"] is False and g["checks"]["max_move<=cap"] is False


def test_shadow_does_not_touch_production_ratings():
    """Run main() against the real committed files; assert the prod ratings file is
    byte-identical afterwards and a report was produced."""
    prod_rat = HERE / "national_elo_layer3_ratings.csv"
    base = HERE / "international_results.csv"
    log = HERE / "worldcup_predictions_log.csv"
    if not (prod_rat.exists() and base.exists() and log.exists()):
        print("  SKIP no-touch test (production files absent)")
        return
    before = hashlib.md5(prod_rat.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as td:
        report = Path(td) / "shadow.txt"
        rc = S.main(["--base", str(base), "--log", str(log),
                     "--committed", str(prod_rat), "--report", str(report)])
        assert rc == 0
        assert report.exists() and report.read_text(encoding="utf-8").strip()
    after = hashlib.md5(prod_rat.read_bytes()).hexdigest()
    assert before == after, "SHADOW violated: production ratings file changed!"


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} offline tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
