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
    assert home[0]["source"] == "api_football_events"
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


# ================================================================ FASE 4B — safe incremental merge
SP = "set_piece_takers.csv"
SP_COLS = prep.COLUMNS[SP]
SP_KEYS = prep.KEY_COLS[SP]
SP_OWNED = prep.AUTO_OWNED[SP]


def _sp_row(team_id, player_id, attempts, date, source="api_football_events", rank=1,
            confidence="baja", player_name="P", role="penalty"):
    return {"team_id": team_id, "team_name": "T", "player_id": player_id, "player_name": player_name,
            "role": role, "rank": rank, "attempts": attempts, "last_taken_date": date,
            "source": source, "data_quality": "alta", "confidence": confidence}


def test_merge_appends_new_penalty_taker_without_duplicating():
    existing = pd.DataFrame([_sp_row(10, 100, 2, "2026-06-20")], columns=SP_COLS)
    new = [_sp_row(10, 100, 2, "2026-06-20"),           # same -> no change, no dup
           _sp_row(10, 101, 1, "2026-06-24")]           # new taker -> appended
    merged, stats = prep.safe_merge(existing, new, SP_COLS, SP_KEYS, SP_OWNED, "api_football_events")
    assert len(merged) == 2 and stats["added"] == 1
    assert set(merged["player_id"]) == {100, 101}


def test_merge_refreshes_attempts_and_last_date_only_when_auto():
    existing = pd.DataFrame([_sp_row(10, 100, 2, "2026-06-20")], columns=SP_COLS)
    # a later real run: same taker now has 3 attempts and a newer date
    new = [_sp_row(10, 100, 3, "2026-06-27", confidence="alta")]
    merged, stats = prep.safe_merge(existing, new, SP_COLS, SP_KEYS, SP_OWNED, "api_football_events")
    row = merged[merged["player_id"] == 100].iloc[0]
    assert int(row["attempts"]) == 3 and row["last_taken_date"] == "2026-06-27"
    assert row["confidence"] == "alta" and stats["refreshed"] >= 2


def test_merge_never_overwrites_manual_source_or_confidence():
    # a human-owned row (source=manual) with their own attempts/confidence
    manual = pd.DataFrame([_sp_row(10, 100, 5, "2026-06-01", source="manual", confidence="alta")],
                          columns=SP_COLS)
    new = [_sp_row(10, 100, 1, "2026-06-27", source="api_football_events", confidence="baja")]
    merged, stats = prep.safe_merge(manual, new, SP_COLS, SP_KEYS, SP_OWNED, "api_football_events")
    row = merged[merged["player_id"] == 100].iloc[0]
    assert int(row["attempts"]) == 5 and row["confidence"] == "alta" and row["source"] == "manual"
    assert stats["protected"] >= 1 and stats["refreshed"] == 0


def test_merge_completes_empty_cells_only():
    # auto row missing last_taken_date -> completed; team_name present -> protected
    existing = pd.DataFrame([{**_sp_row(10, 100, 2, None), "team_name": "RealName"}], columns=SP_COLS)
    new = [{**_sp_row(10, 100, 2, "2026-06-24"), "team_name": "OtherName"}]
    merged, stats = prep.safe_merge(existing, new, SP_COLS, SP_KEYS, SP_OWNED, "api_football_events")
    row = merged[merged["player_id"] == 100].iloc[0]
    assert row["last_taken_date"] == "2026-06-24"     # was empty -> completed
    assert row["team_name"] == "RealName"             # non-empty, not auto-owned -> protected
    assert stats["completed"] >= 1


def test_merge_never_deletes_rows():
    existing = pd.DataFrame([_sp_row(10, 100, 2, "2026-06-20"),
                             _sp_row(99, 900, 1, "2026-06-10", source="manual")], columns=SP_COLS)
    merged, stats = prep.safe_merge(existing, [], SP_COLS, SP_KEYS, SP_OWNED)
    assert len(merged) == 2 and stats["manual_rows"] >= 1   # nothing deleted


def test_prepare_incremental_appends_on_second_run(tmp_path):
    # first run: one penalty taker
    e1 = pd.DataFrame([{"fixture_id": 1, "date": "2026-06-20", "team_id": 10, "team_name": "H",
                        "player_id": 100, "player_name": "PenA", "is_penalty_goal": 1,
                        "is_penalty_miss": 0}])
    prep.prepare(ext_dir=tmp_path, events_df=e1, cards_df=_cards_df(), store_records=[])
    sp1 = pd.read_csv(tmp_path / SP)
    assert len(sp1) == 1
    # a human adds a manual free-kick taker row
    sp1m = pd.concat([sp1, pd.DataFrame([_sp_row(10, 555, 3, "2026-06-15", source="manual",
                                                 role="direct_free_kick", player_name="FKguy")])],
                     ignore_index=True)
    sp1m.to_csv(tmp_path / SP, index=False)
    # second run: a NEW penalty taker appears in events
    e2 = pd.concat([e1, pd.DataFrame([{"fixture_id": 2, "date": "2026-06-25", "team_id": 10,
                                       "team_name": "H", "player_id": 101, "player_name": "PenB",
                                       "is_penalty_goal": 1, "is_penalty_miss": 0}])],
                   ignore_index=True)
    summary = prep.prepare(ext_dir=tmp_path, events_df=e2, cards_df=_cards_df(), store_records=[])
    sp2 = pd.read_csv(tmp_path / SP)
    assert len(sp2) == 3                                   # 100 + manual 555 + new 101
    assert set(sp2["player_id"]) == {100, 555, 101}
    # the manual free-kick row is untouched
    fk = sp2[sp2["player_id"] == 555].iloc[0]
    assert fk["source"] == "manual" and fk["role"] == "direct_free_kick"
    assert summary[SP]["added"] == 1


# ---------------------------------------------------------------- fine position
def _store_with_fine_lineup():
    return [{
        "postft": {
            "players": [{"team": {"id": 10, "name": "H"}, "players": [
                {"player": {"id": 100, "name": "Defender"},
                 "statistics": [{"games": {"position": "D"}}]}]}],
            "lineups": [{"team": {"id": 10}, "startXI": [
                {"player": {"id": 100, "name": "Defender", "pos": "LB", "grid": "2:1"}}]}],
        }
    }]


def test_positional_uses_fine_position_when_present():
    rows = prep.derive_positional_profiles(_store_with_fine_lineup())
    r = [x for x in rows if x["player_id"] == 100][0]
    assert r["position"] == "LB" and r["source"] == "api_football_lineup"


def test_positional_keeps_coarse_when_no_fine():
    rows = prep.derive_positional_profiles(_store_records())   # only G/D/M/F
    by_id = {r["player_id"]: r for r in rows}
    assert by_id[200]["position"] == "DEF" and by_id[200]["source"] == "api_football_lineup_position"


def test_positional_does_not_overwrite_manual_profile(tmp_path):
    POS = "player_positional_profiles.csv"
    cols = prep.COLUMNS[POS]
    # human filled player 100 with a fine position + threats
    manual = pd.DataFrame([{"player_id": 100, "player_name": "Defender", "team_id": 10,
                            "position": "RB", "role": "carrilero", "pace_threat": 0.8,
                            "source": "manual", "data_quality": "alta", "confidence": "media"}],
                          columns=cols)
    manual.to_csv(tmp_path / POS, index=False)
    # the deriver would say coarse 'DEF' for player 100 — must NOT overwrite the manual fine row
    prep.prepare(ext_dir=tmp_path, events_df=None, cards_df=None, store_records=_store_records())
    df = pd.read_csv(tmp_path / POS)
    row = df[df["player_id"] == 100].iloc[0]
    assert row["position"] == "RB" and row["source"] == "manual"
    assert float(row["pace_threat"]) == 0.8         # manual threat preserved


# ---------------------------------------------------------------- referee / venue detection
def test_detect_referee_present_and_absent():
    assert prep.detect_referees([{"fixture_id": 1, "fixture": {"referee": "Mr Ref"}}]) == {1: "Mr Ref"}
    assert prep.detect_referees(_store_records()) == {}          # none in the real-shaped store


def test_fixture_referees_prepopulated_when_present(tmp_path):
    store = [{"fixture_id": 7, "referee": "Daniele Orsato", "postft": {}}]
    prep.prepare(ext_dir=tmp_path, events_df=None, cards_df=_cards_df(), store_records=store)
    fr = pd.read_csv(tmp_path / "fixture_referees.csv")
    assert list(fr.loc[fr["fixture_id"] == 7, "referee_name"]) == ["Daniele Orsato"]


def test_fixture_referees_empty_when_absent(tmp_path):
    prep.prepare(ext_dir=tmp_path, events_df=None, cards_df=_cards_df(), store_records=_store_records())
    assert len(pd.read_csv(tmp_path / "fixture_referees.csv")) == 0   # no referee invented


def test_detect_venue_and_complete_weather(tmp_path):
    store = [{"fixture_id": 1, "prematch": {"venue": [{"name": "Estadio Azteca", "city": "CDMX"}]}}]
    prep.prepare(ext_dir=tmp_path, events_df=None, cards_df=_cards_df(), store_records=store)
    w = pd.read_csv(tmp_path / "weather_by_fixture.csv")
    assert list(w.loc[w["fixture_id"] == 1, "venue"]) == ["Estadio Azteca"]
    # but measurements are still NOT invented
    assert w.loc[w["fixture_id"] == 1, "temperature"].isna().all()


def test_venue_not_invented_when_absent(tmp_path):
    prep.prepare(ext_dir=tmp_path, events_df=None, cards_df=_cards_df(), store_records=_store_records())
    w = pd.read_csv(tmp_path / "weather_by_fixture.csv")
    assert w["venue"].isna().all()   # no venue in store -> stays empty


def test_weather_does_not_overwrite_manual_venue(tmp_path):
    WB = "weather_by_fixture.csv"
    cols = prep.COLUMNS[WB]
    manual = pd.DataFrame([{"fixture_id": 1, "venue": "Manual Stadium", "kickoff_time": "x",
                            "source": "manual"}], columns=cols)
    manual.to_csv(tmp_path / WB, index=False)
    store = [{"fixture_id": 1, "prematch": {"venue": [{"name": "API Stadium"}]}}]
    prep.prepare(ext_dir=tmp_path, events_df=None, cards_df=_cards_df(), store_records=store)
    w = pd.read_csv(tmp_path / WB)
    assert list(w.loc[w["fixture_id"] == 1, "venue"]) == ["Manual Stadium"]   # manual preserved
