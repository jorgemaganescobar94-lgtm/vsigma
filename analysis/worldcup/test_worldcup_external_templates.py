"""
Fase 4A offline tests (NO network, NO API, NO scraping, NO betting). Covers the external-data template
preparer: creates exact headers when missing, never overwrites manual edits, pre-populates ONLY from
real repo data (penalty takers from real events, position from cached lineups, fixture_id+kickoff for
weather), and NEVER fabricates xG/xA, referees or weather measurements.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402


# ---------------------------------------------------------------- synthetic REAL inputs
def _events_df():
    """Real-event-shaped rows: two penalty takers (one with 2 attempts), plus a normal goal + a card."""
    return pd.DataFrame([
        {"fixture_id": 1, "date": "2026-06-20", "team_id": 10, "team_name": "Home",
         "player_id": 100, "player_name": "PenA", "is_penalty_goal": 1, "is_penalty_miss": 0,
         "is_goal": 1, "is_card": 0, "card_type": ""},
        {"fixture_id": 2, "date": "2026-06-24", "team_id": 10, "team_name": "Home",
         "player_id": 100, "player_name": "PenA", "is_penalty_goal": 0, "is_penalty_miss": 1,
         "is_goal": 0, "is_card": 0, "card_type": ""},
        {"fixture_id": 1, "date": "2026-06-20", "team_id": 20, "team_name": "Away",
         "player_id": 200, "player_name": "PenB", "is_penalty_goal": 1, "is_penalty_miss": 0,
         "is_goal": 1, "is_card": 0, "card_type": ""},
        {"fixture_id": 1, "date": "2026-06-20", "team_id": 10, "team_name": "Home",
         "player_id": 101, "player_name": "Scorer", "is_penalty_goal": 0, "is_penalty_miss": 0,
         "is_goal": 1, "is_card": 0, "card_type": ""},
    ])


def _cards_df():
    return pd.DataFrame([
        {"fixture_id": 1, "kickoff_utc": "2026-06-20 18:00", "home": "Home", "away": "Away"},
        {"fixture_id": 2, "kickoff_utc": "2026-06-24 21:00", "home": "X", "away": "Y"},
    ])


def _store_records():
    return [{
        "postft": {"players": [
            {"team": {"id": 10, "name": "Home"}, "players": [
                {"player": {"id": 100, "name": "PenA"},
                 "statistics": [{"games": {"position": "F", "minutes": 90}}]},
                {"player": {"id": 102, "name": "Keeper"},
                 "statistics": [{"games": {"position": "G", "minutes": 90}}]},
            ]},
            {"team": {"id": 20, "name": "Away"}, "players": [
                {"player": {"id": 200, "name": "PenB"},
                 "statistics": [{"games": {"position": "D", "minutes": 90}}]},
                {"player": {"id": 201, "name": "NoPos"},
                 "statistics": [{"games": {"position": None}}]},   # no position -> dropped
            ]},
        ]}
    }]


# ---------------------------------------------------------------- pure derivations
def test_derive_set_piece_only_penalties_ranked():
    rows = prep.derive_set_piece_takers(_events_df())
    # only penalty takers, never free-kick/corner (not inferable)
    assert all(r["role"] == "penalty" for r in rows)
    home = [r for r in rows if r["team_id"] == 10]
    assert home[0]["player_name"] == "PenA" and home[0]["attempts"] == 2 and home[0]["rank"] == 1
    assert home[0]["last_taken_date"] == "2026-06-24"   # latest
    assert home[0]["source"] == "worldcup_events"
    # the non-penalty scorer is NOT a set-piece taker
    assert not any(r["player_id"] == 101 for r in rows)


def test_derive_set_piece_empty_when_no_penalties():
    df = pd.DataFrame([{"fixture_id": 1, "date": "2026-06-20", "team_id": 10, "team_name": "H",
                        "player_id": 1, "player_name": "P", "is_penalty_goal": 0, "is_penalty_miss": 0}])
    assert prep.derive_set_piece_takers(df) == []
    assert prep.derive_set_piece_takers(None) == []


def test_derive_positional_position_only_no_threats():
    rows = prep.derive_positional_profiles(_store_records())
    by_id = {r["player_id"]: r for r in rows}
    assert by_id[100]["position"] == "FWD" and by_id[102]["position"] == "GK"
    assert by_id[200]["position"] == "DEF"
    assert 201 not in by_id                       # no position -> not emitted
    # scouting fields are EMPTY (never fabricated)
    for f in ("role", "pace_threat", "aerial_threat", "1v1_threat", "card_risk_role"):
        assert by_id[100][f] is None
    assert by_id[100]["source"] == "api_football_lineup_position"


def test_derive_weather_kickoff_only_no_measurements():
    rows = prep.derive_weather_template(_cards_df())
    assert {r["fixture_id"] for r in rows} == {1, 2}
    r0 = rows[0]
    assert r0["kickoff_time"] == "2026-06-20 18:00"
    # NO invented measurements
    for f in ("temperature", "humidity", "wind_speed", "rain_probability", "pitch_condition", "venue"):
        assert r0[f] is None
    assert r0["data_quality"] == "pendiente"


# ---------------------------------------------------------------- orchestration / writer
def test_prepare_creates_exact_headers(tmp_path):
    summary = prep.prepare(ext_dir=tmp_path, events_df=_events_df(), cards_df=_cards_df(),
                           store_records=_store_records())
    for fname, cols in prep.COLUMNS.items():
        p = tmp_path / fname
        assert p.exists(), f"{fname} not created"
        df = pd.read_csv(p)
        assert list(df.columns) == cols, f"{fname} header mismatch"
        assert summary[fname]["action"] == "created"


def test_prepare_prepopulates_only_real(tmp_path):
    summary = prep.prepare(ext_dir=tmp_path, events_df=_events_df(), cards_df=_cards_df(),
                           store_records=_store_records())
    # derived templates have real rows
    assert summary["set_piece_takers.csv"]["prepopulated"] >= 2
    assert summary["player_positional_profiles.csv"]["prepopulated"] == 3
    assert summary["weather_by_fixture.csv"]["prepopulated"] == 2
    # empty-only templates stay headers-only (NO fabrication)
    for fname in ("player_xg_xa.csv", "referee_profiles.csv", "fixture_referees.csv",
                  "coach_tactical_profiles.csv"):
        assert summary[fname]["prepopulated"] == 0
        assert len(pd.read_csv(tmp_path / fname)) == 0


def test_no_xg_xa_fabricated_even_with_events(tmp_path):
    # even though events carry goals, player_xg_xa stays empty (no proxy-as-real)
    prep.prepare(ext_dir=tmp_path, events_df=_events_df(), cards_df=_cards_df(),
                 store_records=_store_records())
    assert len(pd.read_csv(tmp_path / "player_xg_xa.csv")) == 0


def test_no_referee_or_weather_invented(tmp_path):
    prep.prepare(ext_dir=tmp_path, events_df=_events_df(), cards_df=_cards_df(),
                 store_records=_store_records())
    assert len(pd.read_csv(tmp_path / "referee_profiles.csv")) == 0
    assert len(pd.read_csv(tmp_path / "fixture_referees.csv")) == 0
    w = pd.read_csv(tmp_path / "weather_by_fixture.csv")
    # weather rows exist (kickoff) but every measurement column is empty/NaN
    for col in ("temperature", "wind_speed", "rain_probability"):
        assert w[col].isna().all()


def test_does_not_overwrite_manual_edits(tmp_path):
    # a human filled referee_profiles by hand
    manual = tmp_path / "referee_profiles.csv"
    pd.DataFrame([{"referee_name": "Manual Ref", "yellow_cards_pg": 5.0}]).to_csv(manual, index=False)
    before = manual.read_text(encoding="utf-8")
    summary = prep.prepare(ext_dir=tmp_path, events_df=_events_df(), cards_df=_cards_df(),
                           store_records=_store_records())
    assert summary["referee_profiles.csv"]["action"] == "exists"
    assert manual.read_text(encoding="utf-8") == before     # untouched
    # the other (missing) templates were still created
    assert (tmp_path / "set_piece_takers.csv").exists()


def test_write_template_create_if_missing(tmp_path):
    p = tmp_path / "x.csv"
    action, n = prep.write_template(p, ["a", "b"], rows=[{"a": 1, "b": 2}])
    assert action == "created" and n == 1
    action2, n2 = prep.write_template(p, ["a", "b"], rows=[{"a": 9, "b": 9}])
    assert action2 == "exists"                # never overwrites by default
    assert pd.read_csv(p)["a"].iloc[0] == 1   # original preserved
