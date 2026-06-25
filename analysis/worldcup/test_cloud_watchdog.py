"""
Offline tests for cloud_watchdog.py — NO network, NO git, NO Telegram.
Exercise only the pure decision/parse/build functions with injected timestamps.

Run:  python -m pytest analysis/worldcup/test_cloud_watchdog.py -q
  or:  python analysis/worldcup/test_cloud_watchdog.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cloud_watchdog as W  # noqa: E402

NOW = datetime(2026, 6, 27, 14, 0, 0, tzinfo=timezone.utc)


def test_fresh_output_is_silent():
    """Output 2h old -> not stale -> no alert."""
    latest = NOW - timedelta(hours=2)
    is_stale, age = W.decide(NOW, latest, 26)
    assert is_stale is False
    assert 1.9 < age < 2.1


def test_stale_output_triggers_alert():
    """Output 30h old -> stale -> alert text carries timestamp + hint."""
    latest = NOW - timedelta(hours=30)
    is_stale, age = W.decide(NOW, latest, 26)
    assert is_stale is True
    assert 29.9 < age < 30.1
    msg = W.build_alert(latest, age, 26)
    assert "30.0h" in msg
    assert "GitHub Actions" in msg
    assert latest.isoformat(timespec="seconds") in msg


def test_unreadable_output_triggers_alert():
    """latest=None (cannot read) -> stale -> 'No pude leer' alert, no crash."""
    is_stale, age = W.decide(NOW, None, 26)
    assert is_stale is True
    assert age is None
    msg = W.build_alert(None, None, 26)
    assert "No pude leer" in msg
    assert "GitHub Actions" in msg


def test_boundary_just_under_threshold_is_fresh():
    latest = NOW - timedelta(hours=25, minutes=59)
    is_stale, _ = W.decide(NOW, latest, 26)
    assert is_stale is False


def test_boundary_just_over_threshold_is_stale():
    latest = NOW - timedelta(hours=26, minutes=1)
    is_stale, _ = W.decide(NOW, latest, 26)
    assert is_stale is True


def test_parse_scorecard_ts_valid():
    text = ("📊 Track record (19 resueltos · 2026-06-24)\n"
            "...\n"
            "generated_at_utc: 2026-06-24T10:52:22+00:00\n")
    ts = W.parse_scorecard_ts(text)
    assert ts == datetime(2026, 6, 24, 10, 52, 22, tzinfo=timezone.utc)


def test_parse_scorecard_ts_garbage_is_none():
    assert W.parse_scorecard_ts("no timestamp here at all") is None
    assert W.parse_scorecard_ts("generated_at_utc: not-a-date") is None
    assert W.parse_scorecard_ts("") is None


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
        passed += 1
    print(f"\n{passed}/{len(fns)} offline tests passed (no network, no git, no Telegram).")


if __name__ == "__main__":
    _run()
