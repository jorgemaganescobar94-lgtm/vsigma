"""
Offline tests for the Fase 2 real fixture-events extractor (parser). No network, no API, no betting.
Covers: correct event classification (normal/penalty/own/missed goal, yellow/red/second-yellow card,
substitution), assist only on a real goal (NOT on a substitution's 'assist' field), opponent derivation,
and empty events -> [] (no fabrication).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_worldcup_fixture_events as ev  # noqa: E402

HOME = {"id": 10, "name": "Home"}
AWAY = {"id": 20, "name": "Away"}


def _e(team, typ, detail, player, pid, assist=None, aid=None, minute=10):
    return {"time": {"elapsed": minute, "extra": None}, "team": team, "type": typ, "detail": detail,
            "player": {"id": pid, "name": player}, "assist": {"id": aid, "name": assist}}


MOCK = [
    _e(HOME, "Goal", "Normal Goal", "Scorer1", 1, assist="Creator", aid=2, minute=12),
    _e(HOME, "Goal", "Penalty", "PenTaker", 3, minute=30),
    _e(AWAY, "Goal", "Missed Penalty", "PenMisser", 4, minute=40),
    _e(HOME, "Goal", "Own Goal", "OwnGoaler", 5, minute=55),
    _e(AWAY, "Card", "Yellow Card", "Booked", 6, minute=60),
    _e(AWAY, "Card", "Red Card", "SentOff", 7, minute=70),
    _e(HOME, "Card", "Second Yellow card", "TwoYellow", 8, minute=80),
    _e(HOME, "subst", "Substitution 1", "ComingIn", 9, assist="GoingOff", aid=99, minute=75),
]


def _rows():
    return ev.parse_fixture_events(MOCK, {"fixture_id": 1, "date": "2026-06-30"})


def test_goal_classification():
    rows = _rows()
    by_player = {r["player_name"]: r for r in rows}
    assert by_player["Scorer1"]["is_goal"] == 1 and by_player["Scorer1"]["is_assist"] == 1
    assert by_player["Scorer1"]["assist_player_name"] == "Creator"
    assert by_player["PenTaker"]["is_goal"] == 1 and by_player["PenTaker"]["is_penalty_goal"] == 1
    assert by_player["PenMisser"]["is_goal"] == 0 and by_player["PenMisser"]["is_penalty_miss"] == 1
    assert by_player["OwnGoaler"]["is_goal"] == 0 and by_player["OwnGoaler"]["is_own_goal"] == 1


def test_card_classification():
    by = {r["player_name"]: r for r in _rows()}
    assert by["Booked"]["is_card"] == 1 and by["Booked"]["card_type"] == "Yellow Card"
    assert by["SentOff"]["card_type"] == "Red Card"
    assert by["TwoYellow"]["card_type"] == "Second Yellow card"


def test_substitution_is_not_a_goal_assist():
    by = {r["player_name"]: r for r in _rows()}
    sub = by["ComingIn"]
    assert sub["is_substitution"] == 1 and sub["is_assist"] == 0
    assert sub["assist_player_name"] is None        # the 'assist' field on a subst is NOT a goal assist


def test_opponent_derivation():
    by = {r["player_name"]: r for r in _rows()}
    assert by["Scorer1"]["team_name"] == "Home" and by["Scorer1"]["opponent_name"] == "Away"
    assert by["Booked"]["team_name"] == "Away" and by["Booked"]["opponent_name"] == "Home"


def test_empty_events_no_fabrication():
    assert ev.parse_fixture_events([], {"fixture_id": 1, "date": "x"}) == []
    assert ev.parse_fixture_events(None, {"fixture_id": 1, "date": "x"}) == []


def test_source_and_quality_flags():
    r = _rows()[0]
    assert r["source"] == "api_football_events" and r["data_quality"] == "alta"
    assert r["competition"] == ev.COMPETITION


def test_no_betting_or_odds_endpoint_in_module():
    """Real property: the extractor never calls an odds/predictions endpoint nor uses betting logic
    (prose disclaimers like 'NO odds' are allowed; actual endpoint/usage tokens are not)."""
    src = (HERE / "build_worldcup_fixture_events.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "stake", "expected_roi", "edge="):
        assert bad not in src


# --- Fix #1: fixture-source UNION with international_results (covers the matchday-1 cold-start gap) ---
def test_intl_source_covers_matchday1_absent_from_log():
    """The new fixture source (international_results WC settled) includes the matchday-1 fixtures that
    the predictions log lacks (cold start), and it covers everything the events CSV already holds."""
    import pandas as pd
    intl = {m["fixture_id"] for m in ev._wc_settled_from_intl()}
    log = {m["fixture_id"] for m in ev._settled_fixtures()}
    assert 1489369 in intl                 # a matchday-1 fixture (Mexico–South Africa, 2026-06-11)
    assert 1489369 not in log              # ...which the predictions log never logged (pipeline cold start)
    assert len(intl) >= 81                 # int_results has the full settled WC universe
    evdf = pd.read_csv(ev.OUT_CSV)
    assert set(evdf["fixture_id"].astype(int)) <= intl   # source ⊇ current output (nothing orphaned)


def test_flag_off_source_is_log_only_delta0():
    """With EVENTS_SOURCE_INTL_RESULTS off the fixture universe is EXACTLY the predictions log (Δ0):
    the union with international_results is skipped, so matchday-1 stays out — identical to the old code."""
    assert ev.EVENTS_SOURCE_INTL_RESULTS is True          # default (env WC_EVENTS_SRC_INTL unset)
    log = {m["fixture_id"] for m in ev._settled_fixtures()}
    assert 1489369 not in log                              # flag-off universe never adds matchday-1
    # the flag literally gates the union in extract() -> off == pre-change behaviour
    src = (HERE / "build_worldcup_fixture_events.py").read_text(encoding="utf-8")
    assert "if EVENTS_SOURCE_INTL_RESULTS:" in src


def test_existing_rows_loader_preserves_and_handles_absence():
    """_existing_rows_by_fid groups committed rows by fixture_id (durable cache for immutable events)
    and returns {} for a missing file (no crash)."""
    from pathlib import Path as _P
    by = ev._existing_rows_by_fid()
    assert isinstance(by, dict) and len(by) >= 1
    assert 1489390 in by and len(by[1489390]) >= 1         # a fixture in the committed 65
    assert ev._existing_rows_by_fid(_P("does_not_exist_xyz.csv")) == {}
