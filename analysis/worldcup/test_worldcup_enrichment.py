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
    "fixture": {"id": FIX_ID, "date": "2026-06-23T19:00:00+00:00", "referee": "Daniele Orsato",
                "status": {"short": "FT"},
                "venue": {"id": VENUE_ID, "name": "Estadio X", "city": "Ciudad"}},
    "teams": {"home": {"id": HOME_ID, "name": "Spain"}, "away": {"id": AWAY_ID, "name": "France"}},
    "goals": {"home": 2, "away": 1},
    "score": {"fulltime": {"home": 2, "away": 1}},
}]

STATS_RESP = [
    {"team": {"id": HOME_ID, "name": "Spain"}, "statistics": [
        {"type": "Total Shots", "value": 14},
        {"type": "Shots on Goal", "value": 6},
        {"type": "Shots off Goal", "value": 5},
        {"type": "Blocked Shots", "value": 3},
        {"type": "Shots insidebox", "value": 10},
        {"type": "Shots outsidebox", "value": 4},
        {"type": "Fouls", "value": 11},
        {"type": "Ball Possession", "value": "58%"},
        {"type": "Corner Kicks", "value": 6},
        {"type": "Offsides", "value": 2},
        {"type": "Goalkeeper Saves", "value": 1},
        {"type": "Total passes", "value": 520},
        {"type": "Passes accurate", "value": 470},
        {"type": "Passes %", "value": "90%"},
        {"type": "Yellow Cards", "value": 1},
        {"type": "Red Cards", "value": None},
        {"type": "goals_prevented", "value": "0.4"},
        {"type": "expected_goals", "value": "1.8"},
    ]},
    {"team": {"id": AWAY_ID, "name": "France"}, "statistics": [
        {"type": "Total Shots", "value": 7},
        {"type": "Shots on Goal", "value": 3},
        {"type": "Shots insidebox", "value": 5},
        {"type": "Ball Possession", "value": "42%"},
        {"type": "Corner Kicks", "value": 4},
        {"type": "Offsides", "value": 1},
        {"type": "Goalkeeper Saves", "value": 4},
        {"type": "Passes %", "value": "84%"},
        {"type": "expected_goals", "value": "0.9"},
    ]},
]

EVENTS_RESP = [
    {"time": {"elapsed": 23}, "team": {"id": HOME_ID}, "type": "Goal", "detail": "Normal Goal"},
    {"time": {"elapsed": 40}, "team": {"id": AWAY_ID}, "type": "Card", "detail": "Yellow Card"},
    {"time": {"elapsed": 55}, "team": {"id": HOME_ID}, "type": "Goal", "detail": "Normal Goal"},
    {"time": {"elapsed": 70}, "team": {"id": HOME_ID}, "type": "Card", "detail": "Yellow Card"},
]

PLAYERS_RESP = [
    {"team": {"id": HOME_ID}, "players": [
        {"player": {"id": 1, "name": "Rodri"},
         "statistics": [{"games": {"rating": "8.4", "minutes": 90, "position": "M"}}]},
        {"player": {"id": 2, "name": "Morata"},
         "statistics": [{"games": {"rating": "7.0", "minutes": 80, "position": "F"}}]},
        {"player": {"id": 3, "name": "Bench"},  # no rating (DNP) -> excluded
         "statistics": [{"games": {"rating": None, "minutes": 0, "position": "M"}}]},
    ]},
    {"team": {"id": AWAY_ID}, "players": [
        {"player": {"id": 4, "name": "Mbappe"},
         "statistics": [{"games": {"rating": "7.9", "minutes": 90, "position": "F"}}]},
    ]},
]

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


def test_parse_statistics_summary_new_fields():
    s = wc.parse_statistics_summary(STATS_RESP, HOME_ID, AWAY_ID)
    # newly captured non-betting sheet (free, same call)
    assert s["sot_home"] == 6 and s["sot_away"] == 3
    assert s["shots_inbox_home"] == 10 and s["shots_outbox_home"] == 4
    assert s["shots_blocked_home"] == 3 and s["shots_off_home"] == 5
    assert s["offsides_home"] == 2 and s["offsides_away"] == 1
    assert s["gk_saves_home"] == 1 and s["gk_saves_away"] == 4
    assert s["passes_total_home"] == 520 and s["passes_acc_home"] == 470
    assert s["passes_pct_home"] == 90 and s["passes_pct_away"] == 84
    assert s["fouls_home"] == 11 and s["goals_prevented_home"] == 0.4
    assert s["cards_yellow_home"] == 1 and s["cards_red_home"] is None


def test_parse_players_summary_ratings():
    r = wc.parse_players_summary(PLAYERS_RESP, HOME_ID, AWAY_ID)["ratings"]
    assert r["home"]["mvp_name"] == "Rodri" and r["home"]["mvp_rating"] == 8.4
    assert r["home"]["n_rated"] == 2                       # bench DNP (no rating) excluded
    assert r["home"]["avg_rating"] == round((8.4 + 7.0) / 2, 2)
    assert r["away"]["mvp_name"] == "Mbappe" and r["away"]["mvp_rating"] == 7.9
    # empty response -> no ratings block (soft)
    assert wc.parse_players_summary([], HOME_ID, AWAY_ID) == {}


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


# ----------------------------------------------------------------- Fase 4C-1: referee/venue block
def test_build_fixture_block_real_merge_and_empty():
    m = {"referee": "Mr Ref", "venue_id": 50, "venue_name": "Estadio X", "venue_city": "Ciudad",
         "date": "2026-06-23T19:00:00+00:00"}
    fb = wc.build_fixture_block(m)
    assert fb["referee"] == "Mr Ref" and fb["venue"] == {"id": 50, "name": "Estadio X",
                                                         "city": "Ciudad"}
    assert fb["date"].startswith("2026-06-23")
    # merge-safe: a null referee in meta keeps the previously-captured one (no wipe)
    fb2 = wc.build_fixture_block({"venue_name": "New"}, {"referee": "Kept", "venue": {"name": "Old"}})
    assert fb2["referee"] == "Kept" and fb2["venue"]["name"] == "New"
    # nothing real -> None (never an empty/invented block)
    assert wc.build_fixture_block({}, {}) is None


def test_fixtures_index_captures_referee_and_venue():
    m = MockClient(ALL_RESPONSES)
    idx = wc._fixtures_index(m, [])
    meta = idx[FIX_ID]
    assert meta["referee"] == "Daniele Orsato"
    assert meta["venue_name"] == "Estadio X" and meta["venue_city"] == "Ciudad"


def test_postft_writes_fixture_block_referee_venue():
    m = MockClient(ALL_RESPONSES)
    wc.enrich_postft([FIX_ID], client=m)
    fx = wc.load_store(FIX_ID)["fixture"]
    assert fx["referee"] == "Daniele Orsato"
    assert fx["venue"]["name"] == "Estadio X" and fx["venue"]["city"] == "Ciudad"
    assert fx["date"].startswith("2026-06-23")


def test_postft_backfills_fixture_block_even_when_cached():
    # first pass writes postft + fixture block
    wc.enrich_postft([FIX_ID], client=MockClient(ALL_RESPONSES))
    # simulate an OLD store that has postft summary but NO fixture block (pre-4C1)
    store = wc.load_store(FIX_ID)
    store.pop("fixture", None)
    wc.save_store(FIX_ID, store)
    # second pass: store-guard skips the heavy FT endpoints, but the fixture block is backfilled
    m2 = MockClient(ALL_RESPONSES)
    wc.enrich_postft([FIX_ID], client=m2)
    assert m2.count("/fixtures/statistics") == 0          # heavy endpoints NOT recalled
    assert wc.load_store(FIX_ID)["fixture"]["referee"] == "Daniele Orsato"   # but block restored


def test_postft_no_referee_not_invented():
    resp = dict(ALL_RESPONSES)
    resp["/fixtures"] = [{"fixture": {"id": FIX_ID, "date": "2026-06-23T19:00:00+00:00",
                                      "status": {"short": "FT"}, "venue": {"id": VENUE_ID}},
                          "teams": {"home": {"id": HOME_ID, "name": "Spain"},
                                    "away": {"id": AWAY_ID, "name": "France"}}}]
    wc.enrich_postft([FIX_ID], client=MockClient(resp))
    fx = wc.load_store(FIX_ID).get("fixture") or {}
    assert "referee" not in fx                            # no referee in API -> none invented
    assert (fx.get("venue") or {}).get("name") is None    # no venue name either


def test_prematch_writes_fixture_block():
    wc.enrich_prematch([FIX_ID], client=MockClient(ALL_RESPONSES))
    fx = wc.load_store(FIX_ID)["fixture"]
    assert fx["referee"] == "Daniele Orsato" and fx["venue"]["name"] == "Estadio X"


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


def test_postft_backfills_summary_schema_zero_api():
    # first pass writes full postft (raw + summary)
    wc.enrich_postft([FIX_ID], client=MockClient(ALL_RESPONSES))
    # simulate an OLD store: raw kept, but summary is the pre-expansion thin one (no new fields)
    store = wc.load_store(FIX_ID)
    store["postft"]["summary"] = {"xg_home": 1.8, "xg_away": 0.9}  # legacy shape
    wc.save_store(FIX_ID, store)
    # second pass: store-guard skips the heavy FT endpoints, but summary is re-derived from raw
    m2 = MockClient(ALL_RESPONSES)
    res = wc.enrich_postft([FIX_ID], client=m2)
    assert res["enriched"] == 0
    assert m2.count("/fixtures/statistics") == 0          # ZERO extra API
    assert m2.count("/fixtures/players") == 0
    s = wc.load_store(FIX_ID)["postft"]["summary"]
    assert s["sot_home"] == 6 and s["passes_pct_home"] == 90   # new fields backfilled for free
    assert (s.get("ratings") or {}).get("home", {}).get("mvp_name") == "Rodri"


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
    joined = "\n".join(lines)
    assert "xG 1.8-0.9" in lines[0] and "tiros 14-7" in lines[0]
    assert "posesión 58-42" in lines[0] and "córners 6-4" in lines[0]
    assert "1er gol min 23" in lines[1] and "tarjetas 2A/0R" in lines[1] and "final 2-1" in lines[1]
    # NEW advanced-stats line (free, same call)
    assert "SOT 6-3" in joined and "área 10-5" in joined
    assert "fueras 2-1" in joined and "paradas 1-4" in joined and "pase 90%-84%" in joined
    # NEW MVP line from per-match ratings
    assert "MVP" in joined and "Rodri 8.4 (local)" in joined and "Mbappe 7.9 (visit.)" in joined


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
