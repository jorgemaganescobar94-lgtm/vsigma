"""
Fase 4C-3 offline tests (NO network, NO API, NO writes to data/external, NO commit, NO betting).
Covers the persistence guard: which auto-derived rows are persistible, which manual rows/cells are
protected, forbidden files always blocked, strict exit codes, and txt/csv artifact generation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import guard_worldcup_external_persistence as guard  # noqa: E402
import prepare_worldcup_external_templates as prep  # noqa: E402


def _write(ext, fname, rows):
    cols = prep.COLUMNS[fname]
    pd.DataFrame(rows, columns=cols).to_csv(ext / fname, index=False)


def _seed_empty(ext, skip=()):
    """Create every contract as an empty template except the ones being driven by the test."""
    for fname in prep.COLUMNS:
        if fname not in skip:
            _write(ext, fname, [])


# ---------------------------------------------------------------- set_piece_takers
def test_guard_allows_penalty_auto_row(tmp_path):
    _write(tmp_path, "set_piece_takers.csv", [
        {"team_id": 10, "team_name": "H", "player_id": 100, "player_name": "PenA", "role": "penalty",
         "rank": 1, "attempts": 3, "last_taken_date": "2026-06-24", "source": "api_football_events",
         "data_quality": "alta", "confidence": "alta"}])
    _seed_empty(tmp_path, skip=("set_piece_takers.csv",))
    r = guard.classify_file("set_piece_takers.csv", tmp_path)
    assert r["auto_rows"] == 1 and r["manual_rows"] == 0


def test_guard_protects_free_kick_and_manual_set_piece(tmp_path):
    _write(tmp_path, "set_piece_takers.csv", [
        # a real penalty (auto)
        {"team_id": 10, "team_name": "H", "player_id": 100, "player_name": "PenA", "role": "penalty",
         "rank": 1, "attempts": 3, "last_taken_date": "2026-06-24", "source": "api_football_events",
         "data_quality": "alta", "confidence": "alta"},
        # a manual free-kick taker (protected: role != penalty, source manual)
        {"team_id": 10, "team_name": "H", "player_id": 200, "player_name": "FKguy",
         "role": "direct_free_kick", "rank": 1, "attempts": 5, "last_taken_date": "2026-06-10",
         "source": "manual", "data_quality": "alta", "confidence": "media"}])
    _seed_empty(tmp_path, skip=("set_piece_takers.csv",))
    r = guard.classify_file("set_piece_takers.csv", tmp_path)
    assert r["auto_rows"] == 1 and r["manual_rows"] == 1


def test_guard_protects_penalty_with_wrong_source(tmp_path):
    _write(tmp_path, "set_piece_takers.csv", [
        {"team_id": 10, "team_name": "H", "player_id": 100, "player_name": "PenA", "role": "penalty",
         "rank": 1, "attempts": 3, "last_taken_date": "2026-06-24", "source": "manual",
         "data_quality": "alta", "confidence": "alta"}])
    _seed_empty(tmp_path, skip=("set_piece_takers.csv",))
    r = guard.classify_file("set_piece_takers.csv", tmp_path)
    assert r["auto_rows"] == 0 and r["manual_rows"] == 1   # manual source -> protected


# ---------------------------------------------------------------- positional
def test_guard_allows_auto_position(tmp_path):
    _write(tmp_path, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _seed_empty(tmp_path, skip=("player_positional_profiles.csv",))
    r = guard.classify_file("player_positional_profiles.csv", tmp_path)
    assert r["auto_rows"] == 1 and r["manual_cells"] == 0


def test_guard_protects_manual_scouting_fields(tmp_path):
    _write(tmp_path, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "RB",
         "role": "carrilero", "pace_threat": 0.8,            # manual scouting cells filled
         "source": "api_football_lineup_position", "data_quality": "alta", "confidence": "media"}])
    _seed_empty(tmp_path, skip=("player_positional_profiles.csv",))
    r = guard.classify_file("player_positional_profiles.csv", tmp_path)
    assert r["auto_rows"] == 0 and r["manual_rows"] == 1
    assert r["manual_cells"] == 2                            # role + pace_threat


# ---------------------------------------------------------------- weather
def test_guard_allows_venue_kickoff_auto(tmp_path):
    _write(tmp_path, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "Estadio", "kickoff_time": "x", "source": "plantilla_kickoff",
         "data_quality": "pendiente", "confidence": "pendiente"}])
    _seed_empty(tmp_path, skip=("weather_by_fixture.csv",))
    r = guard.classify_file("weather_by_fixture.csv", tmp_path)
    assert r["auto_rows"] == 1 and r["manual_cells"] == 0


def test_guard_protects_manual_weather_measurements(tmp_path):
    _write(tmp_path, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "Estadio", "kickoff_time": "x", "temperature": 28, "wind_speed": 12,
         "source": "plantilla_kickoff", "data_quality": "media", "confidence": "media"}])
    _seed_empty(tmp_path, skip=("weather_by_fixture.csv",))
    r = guard.classify_file("weather_by_fixture.csv", tmp_path)
    assert r["auto_rows"] == 0 and r["manual_rows"] == 1
    assert r["manual_cells"] == 2                            # temperature + wind_speed


# ---------------------------------------------------------------- fixture_referees
def test_guard_requires_referee_name(tmp_path):
    _write(tmp_path, "fixture_referees.csv", [{"fixture_id": 1, "referee_name": "Mr Ref"},
                                              {"fixture_id": 2, "referee_name": None}])
    _seed_empty(tmp_path, skip=("fixture_referees.csv",))
    r = guard.classify_file("fixture_referees.csv", tmp_path)
    assert r["auto_rows"] == 1 and r["manual_rows"] == 1     # the empty-name row is not persistible


# ---------------------------------------------------------------- forbidden files
def test_guard_blocks_forbidden_files(tmp_path):
    _seed_empty(tmp_path)
    # even with data, xg_xa is always blocked
    _write(tmp_path, "player_xg_xa.csv", [{"player_id": 1, "xg90": 0.5, "xa90": 0.3}])
    rep = guard.evaluate(tmp_path)
    blocked = {b["file"] for b in rep["blocked"]}
    assert blocked == guard.FORBIDDEN_FILES
    assert all(p.split("/")[-1] not in guard.FORBIDDEN_FILES for p in rep["addable_paths"])


# ---------------------------------------------------------------- would_commit / addable
def test_guard_detects_empty_commit(tmp_path):
    _seed_empty(tmp_path)                                    # all empty templates
    rep = guard.evaluate(tmp_path)
    assert rep["would_commit"] is False and rep["addable_paths"] == []


def test_guard_addable_paths_are_posix(tmp_path):
    _write(tmp_path, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _seed_empty(tmp_path, skip=("player_positional_profiles.csv",))
    rep = guard.evaluate(tmp_path)
    assert rep["would_commit"] is True
    assert "data/external/player_positional_profiles.csv" in rep["addable_paths"]
    assert all("\\" not in p for p in rep["addable_paths"])   # forward slashes only


# ---------------------------------------------------------------- strict mode
def test_strict_fails_on_forbidden_in_candidate_set(tmp_path):
    _seed_empty(tmp_path)
    rep = guard.evaluate(tmp_path, candidate_files=["player_xg_xa.csv"])
    assert rep["strict_ok"] is False
    assert any("prohibido" in v for v in rep["violations"])


def test_strict_fails_when_addable_file_has_manual_data(tmp_path):
    # an addable file with a manual scouting cell -> wholesale add unsafe -> strict fails
    _write(tmp_path, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"},
        {"player_id": 2, "player_name": "Q", "team_id": 10, "position": "RB", "role": "carrilero",
         "source": "manual", "data_quality": "alta", "confidence": "media"}])
    _seed_empty(tmp_path, skip=("player_positional_profiles.csv",))
    rep = guard.evaluate(tmp_path)
    assert rep["strict_ok"] is False
    assert any("MANUALES" in v for v in rep["violations"])


def test_strict_passes_on_clean_auto_only(tmp_path):
    _write(tmp_path, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _write(tmp_path, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "E", "kickoff_time": "x", "source": "plantilla_kickoff",
         "data_quality": "pendiente", "confidence": "pendiente"}])
    _seed_empty(tmp_path, skip=("player_positional_profiles.csv", "weather_by_fixture.csv"))
    rep = guard.evaluate(tmp_path)
    assert rep["strict_ok"] is True and rep["violations"] == []
    assert rep["would_commit"] is True


def test_strict_fails_on_column_mismatch(tmp_path):
    # a positional file missing a contract column -> columns inconsistent
    pd.DataFrame([{"player_id": 1, "position": "DEF", "source": "api_football_lineup_position"}]).to_csv(
        tmp_path / "player_positional_profiles.csv", index=False)
    _seed_empty(tmp_path, skip=("player_positional_profiles.csv",))
    rep = guard.evaluate(tmp_path)
    assert rep["strict_ok"] is False
    assert any("columnas" in v for v in rep["violations"])


# ---------------------------------------------------------------- artifacts
def test_guard_writes_txt_and_csv(tmp_path):
    _seed_empty(tmp_path)
    out_txt = tmp_path / "g.txt"
    out_csv = tmp_path / "g.csv"
    rep = guard.run(ext_dir=tmp_path, out_txt=out_txt, out_csv=out_csv, write=True)
    assert out_txt.exists() and out_csv.exists()
    assert "PERSISTENCE GUARD" in rep["txt"]
    df = pd.read_csv(out_csv)
    assert set(df["policy"]) == {"allowed", "blocked"}
