"""
Offline tests for LOCK-AT-KO in worldcup_learning_loop.cmd_log (Phase 2).
NO network, NO API. Drives cmd_log with temp CARDS/LOG files and real wall-clock
relative kickoffs (future = pre-KO, past = frozen).

Verifies: NS insert · NS update-while-pre-KO · FREEZE at/after KO · settled rows
never touched · result_*/settled never written by the log step · gap on first-seen-post-KO.

Run:  python analysis/worldcup/test_lock_at_ko.py
"""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_learning_loop as W  # noqa: E402

NOW = datetime.now(timezone.utc)
FUT = (NOW + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")   # pre-KO (updatable)
PAST = (NOW - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")  # started (frozen)


def _setup(tmp):
    W.CARDS = Path(tmp) / "worldcup_cards.csv"
    W.LOG = Path(tmp) / "worldcup_predictions_log.csv"
    W.V2 = Path(tmp) / "worldcup_our_model_v2_predictions.csv"
    W.GAPS = Path(tmp) / "worldcup_gaps.txt"


def _card(fid, ko, home, away, ph):
    return {"fixture_id": fid, "kickoff_utc": ko, "home": home, "away": away, "round": "G3",
            "our_home": ph, "our_draw": 0.25, "our_away": round(1 - ph - 0.25, 4),
            "our_xg_home": 1.5, "our_xg_away": 1.0}


def _write_cards(rows):
    pd.DataFrame(rows).to_csv(W.CARDS, index=False)


def _seed_log(rows):
    """Write a LOG csv from partial row dicts; missing columns are filled by _read_log."""
    pd.DataFrame(rows, columns=W.LOG_COLUMNS).to_csv(W.LOG, index=False)


def _log():
    return pd.read_csv(W.LOG)


def test_insert_then_update_while_preko():
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp)
        # 1st run: NS fixture (future KO) -> INSERT
        _write_cards([_card(1, FUT, "Alpha", "Beta", 0.50)])
        W.cmd_log()
        df = _log()
        assert len(df) == 1
        row = df[df.fixture_id == 1].iloc[0]
        assert abs(row.l3_home - 0.50) < 1e-9
        assert row.pred_policy == "last_preko"
        assert int(row.settled) == 0

        # 2nd run: still pre-KO, NEW prediction -> UPDATE in place (not a new row)
        _write_cards([_card(1, FUT, "Alpha", "Beta", 0.70)])
        W.cmd_log()
        df = _log()
        assert len(df) == 1, "update must not append a second row"
        row = df[df.fixture_id == 1].iloc[0]
        assert abs(row.l3_home - 0.70) < 1e-9, "pre-KO row should reflect the latest prediction"
        assert row.kickoff_utc == FUT and row.home == "Alpha"


def test_freeze_after_kickoff():
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp)
        # seed a logged row whose kickoff is already in the PAST, settled=0
        _seed_log([{"fixture_id": 2, "kickoff_utc": PAST, "home": "Gamma", "away": "Delta",
                    "round": "G3", "l3_home": 0.40, "settled": 0, "pred_policy": "last_preko"}])
        # card tries to push a new prediction AFTER kickoff -> must be IGNORED (frozen)
        _write_cards([_card(2, PAST, "Gamma", "Delta", 0.99)])
        W.cmd_log()
        row = _log().iloc[0]
        assert abs(row.l3_home - 0.40) < 1e-9, "post-KO prediction must be frozen"


def test_settled_row_never_touched():
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp)
        _seed_log([{"fixture_id": 3, "kickoff_utc": FUT, "home": "Eta", "away": "Zeta",  # even if "pre-KO"
                    "round": "G3", "l3_home": 0.30, "settled": 1, "result_1x2": "H",
                    "result_ft_gh": 2, "result_ft_ga": 0}])
        _write_cards([_card(3, FUT, "Eta", "Zeta", 0.88)])
        W.cmd_log()
        row = _log().iloc[0]
        assert abs(row.l3_home - 0.30) < 1e-9, "settled row prediction must not change"
        assert row.result_1x2 == "H" and int(row.settled) == 1
        assert int(row.result_ft_gh) == 2 and int(row.result_ft_ga) == 0


def test_update_row_predating_lockatko():
    """Regression: an existing NS row whose pred_policy/lead are all-NaN (logged before
    lock-at-KO) must update cleanly, not raise LossySetitemError."""
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp)
        # seed WITHOUT pred_policy/pred_lead_min (NaN float64 columns after _read_log)
        _seed_log([{"fixture_id": 5, "kickoff_utc": FUT, "home": "Mu", "away": "Nu",
                    "round": "G3", "l3_home": 0.33, "settled": 0}])
        _write_cards([_card(5, FUT, "Mu", "Nu", 0.66)])
        W.cmd_log()
        row = _log().iloc[0]
        assert abs(row.l3_home - 0.66) < 1e-9
        assert row.pred_policy == "last_preko"


def test_gap_when_first_seen_after_kickoff():
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp)
        _write_cards([_card(4, PAST, "Iota", "Kappa", 0.55)])  # never logged, KO already passed
        W.cmd_log()
        df = _log()
        assert (df.fixture_id == 4).sum() == 0, "must NOT log a fixture first seen post-KO"
        assert W.GAPS.exists(), "should record a coverage gap"


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} lock-at-KO tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
