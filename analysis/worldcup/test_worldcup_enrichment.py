"""
Offline tests for the World Cup enrichment collector (mock API, no network).

Covers: parse + JSON store write (postft), [REAL] line extraction, store-guard cache
(no re-call when already enriched), prematch h2h + team lane, render soft-fail without
enrichment, and the purification guard (never touches odds/predictions/odds-live).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_worldcup_enrichment as wc  # noqa: E402
import build_worldcup_full_card as fc  # noqa: E402


# ----------------------------------------------------------------- mock client
class MockClient:
    """Records every request and returns canned responses keyed by path."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def request(self, path, params=None, *, ttl_hours=None, use_cache=True, force_refresh=False):
        self.calls.append((path, dict(params or {})))
        if path in wc.EXCLUDED:  # the module must never reach here
            raise AssertionError(f"forbidden endpoint requested: {path}")
        return {"response": self.responses.get(path, [])}

    def count(self, path):
        return sum(1 for p, _ in self.calls if p == path)


FIX_ID = 1001
HOME_ID, AWAY_ID, VENUE_ID, COACH_ID = 9, 2, 50, 100

FIXTURES_RESP = [{
    "fixture": {"id": FIX_ID, "date": "2026-06-23T19:00:00+00:00",
                "status": {"short": "FT"}, "venue": {"id": VENUE_ID, "name": "Estadio X"}},
    "teams": {"home": {"id": HOME_ID, "name": "Spain"}, "away": {"id": AWAY_ID, "name": "France"}},
    "goals": {"home": 2, "away": 1},
    "score": {"fulltime": {"home": 2, "away": 1}},
}]

STATS_RESP = [
    {"team": {"id": HOME_ID, "name": "Spain"}, "statistics": [
        {"type": "Total Shots", "value": 14},
        {"type": "Ball Possession", "value": "58%"},
        {"type": "Corner Kicks", "value": 6},
        {"type": "expected_goals", "value": "1.8"},
    ]},
    {"team": {"id": AWAY_ID, "name": "France"}, "statistics": [
        {"type": "Total Shots", "value": 7},
        {"type": "Ball Possession", "value": "42%"},
        {"type": "Corner Kicks", "value": 4},
        {"type": "expected_goals", "value": "0.9"},
    ]},
]

EVENTS_RESP = [
    {"time": {"elapsed": 23}, "team": {"id": HOME_ID}, "type": "Goal", "detail": "Normal Goal"},
    {"time": {"elapsed": 40}, "team": {"id": AWAY_ID}, "type": "Card", "detail": "Yellow Card"},
    {"time": {"elapsed": 55}, "team": {"id": HOME_ID}, "type": "Goal", "detail": "Normal Goal"},
    {"time": {"elapsed": 70}, "team": {"id": HOME_ID}, "type": "Card", "detail": "Yellow Card"},
]

PLAYERS_RESP = [{"team": {"id": HOME_ID}, "players": [{"player": {"id": 1, "name": "X"},
                 "statistics": [{"games": {"rating": "7.5", "minutes": 90}}]}]}]

H2H_RESP = [{"fixture": {"id": 7}, "teams": {"home": {"id": HOME_ID}, "away": {"id": AWAY_ID}}}]
TEAMSTATS_RESP = {"form": "WWDLW", "fixtures": {"played": {"total": 5}}}
TRANSFERS_RESP = [{"player": {"id": 1, "name": "X"}}]
SIDELINED_RESP = [{"player": {"name": "Y"}, "type": "Injury"}]
COACHS_RESP = [{"id": COACH_ID, "name": "Coach Z"}]
TROPHIES_RESP = [{"league": "World Cup", "place": "Winner"}]
VENUE_RESP = [{"id": VENUE_ID, "name": "Estadio X", "city": "Ciudad"}]

ALL_RESPONSES = {
    "/fixtures": FIXTURES_RESP,
    "/fixtures/statistics": STATS_RESP,
    "/fixtures/events": EVENTS_RESP,
    "/fixtures/players": PLAYERS_RESP,
    "/fixtures/headtohead": H2H_RESP,
    "/teams/statistics": TEAMSTATS_RESP,
    "/transfers": TRANSFERS_RESP,
    "/sidelined": SIDELINED_RESP,
    "/coachs": COACHS_RESP,
    "/trophies": TROPHIES_RESP,
    "/venues": VENUE_RESP,
}


@pytest.fixture(autouse=True)
def isolated_store(tmp_path, monkeypatch):
    """Point the store at a temp dir so tests never touch real data/."""
    monkeypatch.setattr(wc, "STORE_DIR", tmp_path / "api_enrichment")
    return tmp_path


# ----------------------------------------------------------------- parsing
def test_parse_statistics_summary():
    s = wc.parse_statistics_summary(STATS_RESP, HOME_ID, AWAY_ID)
    assert s["xg_home"] == 1.8 and s["xg_away"] == 0.9
    assert s["shots_home"] == 14 and s["shots_away"] == 7
    assert s["possession_home"] == 58 and s["possession_away"] == 42
    assert s["corners_home"] == 6 and s["corners_away"] == 4


def test_parse_events_summary():
    e = wc.parse_events_summary(EVENTS_RESP, HOME_ID, AWAY_ID)
    assert e["first_goal_minute"] == 23 and e["first_goal_side"] == "home"
    assert e["yellow"] == 2 and e["red"] == 0 and e["n_goals"] == 2


# ----------------------------------------------------------------- postft
def test_postft_writes_json_store():
    m = MockClient(ALL_RESPONSES)
    res = wc.enrich_postft([FIX_ID], client=m)
    assert res["enriched"] == 1
    store = wc.load_store(FIX_ID)
    assert store["postft"]["summary"]["xg_home"] == 1.8
    assert store["postft"]["statistics"] and store["postft"]["events"] and store["postft"]["players"]
    assert "fetched_at_utc" in store
    # traceability: the three FT endpoints recorded
    assert any("/fixtures/statistics" in s for s in store["endpoints_called"])
    assert any("/fixtures/events" in s for s in store["endpoints_called"])
    assert any("/fixtures/players" in s for s in store["endpoints_called"])


def test_postft_store_guard_no_recall():
    m1 = MockClient(ALL_RESPONSES)
    wc.enrich_postft([FIX_ID], client=m1)
    # second pass with a fresh client: store-guard -> ZERO per-fixture FT calls
    m2 = MockClient(ALL_RESPONSES)
    res = wc.enrich_postft([FIX_ID], client=m2)
    assert res["enriched"] == 0
    assert m2.count("/fixtures/statistics") == 0
    assert m2.count("/fixtures/events") == 0
    assert m2.count("/fixtures/players") == 0


def test_postft_force_refetches():
    m1 = MockClient(ALL_RESPONSES)
    wc.enrich_postft([FIX_ID], client=m1)
    m2 = MockClient(ALL_RESPONSES)
    res = wc.enrich_postft([FIX_ID], client=m2, force=True)
    assert res["enriched"] == 1
    assert m2.count("/fixtures/statistics") == 1


# ----------------------------------------------------------------- prematch
def test_prematch_writes_h2h_and_team_lane():
    m = MockClient(ALL_RESPONSES)
    res = wc.enrich_prematch([FIX_ID], client=m)
    assert res["enriched"] == 1
    store = wc.load_store(FIX_ID)
    pm = store["prematch"]
    assert pm["headtohead"] == H2H_RESP
    assert str(HOME_ID) in pm["teams"] and str(AWAY_ID) in pm["teams"]
    assert pm["teams"][str(HOME_ID)]["trophies"] == TROPHIES_RESP  # trophies BY COACH
    assert pm["venue"] == VENUE_RESP
    # trophies fetched by coach id, never by player
    assert ("/trophies", {"coach": COACH_ID}) in m.calls


# ----------------------------------------------------------------- ficha lines
def test_real_lines_for_fixture():
    wc.enrich_postft([FIX_ID], client=MockClient(ALL_RESPONSES))
    lines = wc.real_lines_for_fixture(FIX_ID, score="2-1")
    assert len(lines) == 2
    assert "xG 1.8-0.9" in lines[0] and "tiros 14-7" in lines[0]
    assert "posesión 58-42" in lines[0] and "córners 6-4" in lines[0]
    assert "1er gol min 23" in lines[1] and "tarjetas 2A/0R" in lines[1] and "final 2-1" in lines[1]


def test_real_lines_absent_store_is_soft():
    assert wc.real_lines_for_fixture(999999) == []


# ----------------------------------------------------------------- render soft
def _yesterday_log_df():
    return pd.DataFrame([{
        "fixture_id": FIX_ID, "kickoff_utc": "2026-06-23 19:00",
        "home": "Spain", "away": "France",
        "settled": 1, "result_1x2": "H", "result_ft_gh": 2, "result_ft_ga": 1,
        "l3_home": 0.5, "l3_draw": 0.3, "l3_away": 0.2,
    }])


def test_render_yesterday_soft_without_enrichment(tmp_path, monkeypatch):
    # enrichment module shares the isolated empty store -> no [REAL] lines, base output intact
    monkeypatch.setattr(fc.wc_enrich, "STORE_DIR", tmp_path / "empty_store")
    log = tmp_path / "log.csv"
    _yesterday_log_df().to_csv(log, index=False)
    from datetime import datetime, timezone
    now = datetime(2026, 6, 23, 23, 0, tzinfo=timezone.utc)
    lines = fc.build_yesterday_block(str(log), now)
    assert any("Spain 2-1 France" in ln for ln in lines)
    assert not any("[REAL]" in ln for ln in lines)  # SOFT: nothing added without store


def test_render_yesterday_with_enrichment(tmp_path, monkeypatch):
    store_dir = tmp_path / "api_enrichment"
    monkeypatch.setattr(wc, "STORE_DIR", store_dir)
    monkeypatch.setattr(fc.wc_enrich, "STORE_DIR", store_dir)
    wc.enrich_postft([FIX_ID], client=MockClient(ALL_RESPONSES))
    log = tmp_path / "log.csv"
    _yesterday_log_df().to_csv(log, index=False)
    from datetime import datetime, timezone
    now = datetime(2026, 6, 23, 23, 0, tzinfo=timezone.utc)
    lines = fc.build_yesterday_block(str(log), now)
    assert any("[REAL]" in ln and "xG 1.8-0.9" in ln for ln in lines)
    assert any("[REAL]" in ln and "1er gol min 23" in ln for ln in lines)


# ----------------------------------------------------------------- purification
def test_purification_guard_rejects_odds():
    m = MockClient(ALL_RESPONSES)
    with pytest.raises(RuntimeError):
        wc._get(m, "/odds", {"fixture": FIX_ID}, wc.TTL_FT, [])
    with pytest.raises(RuntimeError):
        wc._get(m, "/predictions", {"fixture": FIX_ID}, wc.TTL_FT, [])


def test_no_market_endpoints_ever_called():
    m = MockClient(ALL_RESPONSES)
    wc.enrich_prematch([FIX_ID], client=m)
    wc.enrich_postft([FIX_ID], client=m, force=True)
    called_paths = {p for p, _ in m.calls}
    assert called_paths.isdisjoint({"/odds", "/predictions", "/odds/live"})
