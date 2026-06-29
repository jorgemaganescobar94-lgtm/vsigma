"""
Fase 4C-4 offline tests (NO network, NO API, NO scraping, NO commit, NO betting, NO mutation of the real
data/external). Cover the persistable-snapshot builder, its --check mode, the guard running --strict over
a filtered snapshot, and the commit SIMULATION (which never calls git).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402
import guard_worldcup_external_persistence as guard  # noqa: E402
import build_worldcup_external_persistable_snapshot as snap  # noqa: E402
import simulate_worldcup_external_persistence_commit as sim  # noqa: E402


def _write(ext, fname, rows):
    cols = prep.COLUMNS[fname]
    pd.DataFrame(rows, columns=cols).to_csv(ext / fname, index=False)


def _seed_empty(ext, skip=()):
    for fname in prep.COLUMNS:
        if fname not in skip:
            _write(ext, fname, [])


def _ext(tmp_path):
    d = tmp_path / "ext"
    d.mkdir()
    return d


# ---------------------------------------------------------------- set_piece include/exclude
def test_snapshot_includes_penalty_auto(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "set_piece_takers.csv", [
        {"team_id": 10, "team_name": "H", "player_id": 100, "player_name": "PenA", "role": "penalty",
         "rank": 1, "attempts": 3, "last_taken_date": "2026-06-24", "source": "api_football_events",
         "data_quality": "alta", "confidence": "alta"}])
    _seed_empty(ext, skip=("set_piece_takers.csv",))
    df, info = snap.filter_file("set_piece_takers.csv", ext)
    assert info["included_rows"] == 1 and info["excluded_rows"] == 0
    assert list(df.columns) == prep.COLUMNS["set_piece_takers.csv"]   # full schema preserved


def test_snapshot_excludes_freekick_corner_and_manual(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "set_piece_takers.csv", [
        {"team_id": 10, "team_name": "H", "player_id": 100, "player_name": "PenA", "role": "penalty",
         "rank": 1, "attempts": 3, "last_taken_date": "2026-06-24", "source": "api_football_events",
         "data_quality": "alta", "confidence": "alta"},
        # direct free kick — never inferable, excluded
        {"team_id": 10, "team_name": "H", "player_id": 200, "player_name": "FK",
         "role": "direct_free_kick", "rank": 1, "attempts": 5, "last_taken_date": "2026-06-10",
         "source": "api_football_events", "data_quality": "alta", "confidence": "media"},
        # corner — excluded
        {"team_id": 10, "team_name": "H", "player_id": 201, "player_name": "Co", "role": "corner_left",
         "rank": 1, "attempts": 4, "last_taken_date": "2026-06-11", "source": "api_football_events",
         "data_quality": "alta", "confidence": "media"},
        # manual penalty (wrong source) — excluded
        {"team_id": 10, "team_name": "H", "player_id": 202, "player_name": "Man", "role": "penalty",
         "rank": 1, "attempts": 2, "last_taken_date": "2026-06-12", "source": "manual",
         "data_quality": "alta", "confidence": "media"}])
    _seed_empty(ext, skip=("set_piece_takers.csv",))
    df, info = snap.filter_file("set_piece_takers.csv", ext)
    assert info["included_rows"] == 1 and info["excluded_rows"] == 3
    assert set(df["role"]) == {"penalty"} and set(df["source"]) == {"api_football_events"}


# ---------------------------------------------------------------- positional blanking / schema
def test_snapshot_clears_manual_positional_fields(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "RB", "role": "carrilero",
         "preferred_zone": "right", "pace_threat": 0.8, "card_risk_role": "high",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _seed_empty(ext, skip=("player_positional_profiles.csv",))
    df, info = snap.filter_file("player_positional_profiles.csv", ext)
    assert info["included_rows"] == 1
    assert info["manual_cells_cleared"] == 4                      # role, preferred_zone, pace, card_risk
    row = df.iloc[0]
    for c in ("role", "preferred_zone", "pace_threat", "card_risk_role"):
        assert str(row[c]) == ""                                 # blanked
    assert row["position"] == "RB" and row["player_id"] == 1     # auto fields preserved


def test_snapshot_preserves_full_schema(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _seed_empty(ext, skip=("player_positional_profiles.csv",))
    df, _ = snap.filter_file("player_positional_profiles.csv", ext)
    assert list(df.columns) == prep.COLUMNS["player_positional_profiles.csv"]


def test_snapshot_excludes_manual_source_positional(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"},
        {"player_id": 2, "player_name": "Q", "team_id": 10, "position": "RB",
         "source": "manual", "data_quality": "alta", "confidence": "media"}])
    _seed_empty(ext, skip=("player_positional_profiles.csv",))
    df, info = snap.filter_file("player_positional_profiles.csv", ext)
    assert info["included_rows"] == 1 and info["excluded_rows"] == 1
    assert set(df["player_id"]) == {1}


# ---------------------------------------------------------------- weather blanking
def test_snapshot_clears_manual_weather_measurements(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "Estadio", "kickoff_time": "x", "temperature": 28, "wind_speed": 12,
         "humidity": 60, "source": "plantilla_kickoff", "data_quality": "media", "confidence": "media"}])
    _seed_empty(ext, skip=("weather_by_fixture.csv",))
    df, info = snap.filter_file("weather_by_fixture.csv", ext)
    assert info["included_rows"] == 1
    assert info["manual_cells_cleared"] == 3                      # temperature, wind_speed, humidity
    row = df.iloc[0]
    for c in ("temperature", "wind_speed", "humidity", "rain_probability", "pitch_condition"):
        assert str(row[c]) == ""
    assert row["venue"] == "Estadio" and row["kickoff_time"] == "x"   # auto preserved


def test_snapshot_weather_accepts_api_store_source(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "E", "kickoff_time": "x", "source": "api_football_store",
         "data_quality": "pendiente", "confidence": "pendiente"}])
    _seed_empty(ext, skip=("weather_by_fixture.csv",))
    df, info = snap.filter_file("weather_by_fixture.csv", ext)
    assert info["included_rows"] == 1


# ---------------------------------------------------------------- referees
def test_snapshot_referees_requires_both_fields(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "fixture_referees.csv", [{"fixture_id": 1, "referee_name": "Mr Ref"},
                                         {"fixture_id": 2, "referee_name": None}])
    _seed_empty(ext, skip=("fixture_referees.csv",))
    df, info = snap.filter_file("fixture_referees.csv", ext)
    assert info["included_rows"] == 1 and info["excluded_rows"] == 1


# ---------------------------------------------------------------- forbidden files never in snapshot
def test_snapshot_excludes_forbidden_files(tmp_path):
    ext = _ext(tmp_path)
    _seed_empty(ext)
    _write(ext, "player_xg_xa.csv", [{"player_id": 1, "xg90": 0.5, "xa90": 0.3}])
    rep = snap.build(ext, tmp_path / "snap", write=True)
    produced = {f["file"] for f in rep["files"]}
    assert produced == set(snap.SNAPSHOT_FILES)
    assert guard.FORBIDDEN_FILES == {f["file"] for f in rep["blocked"]}
    # no forbidden file was written into the snapshot dir
    for f in guard.FORBIDDEN_FILES:
        assert not (tmp_path / "snap" / f).exists()


# ---------------------------------------------------------------- check mode does not write
def test_check_mode_does_not_write(tmp_path):
    ext = _ext(tmp_path)
    _write(ext, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _seed_empty(ext, skip=("player_positional_profiles.csv",))
    snap_dir = tmp_path / "snap"
    rep = snap.build(ext, snap_dir, write=False)
    assert rep["total_included_rows"] == 1
    assert not snap_dir.exists()                                  # nothing written in check mode


def test_check_mode_detects_broken_schema(tmp_path):
    ext = _ext(tmp_path)
    _seed_empty(ext, skip=("weather_by_fixture.csv",))
    # weather with a missing contract column -> broken/unexpected schema
    pd.DataFrame([{"fixture_id": 1, "venue": "E"}]).to_csv(ext / "weather_by_fixture.csv", index=False)
    rep = snap.build(ext, tmp_path / "snap", write=False)
    assert rep["schema_error"] is True


# ---------------------------------------------------------------- guard --strict over the snapshot
def test_guard_strict_passes_over_filtered_snapshot(tmp_path):
    ext = _ext(tmp_path)
    # raw data: a CLEAN auto row (makes the file addable) + a manual scouting cell + a manual-source row.
    # The clean+manual mix makes guard --strict FAIL on raw; the snapshot must clean/drop the manual part.
    _write(ext, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"},
        {"player_id": 2, "player_name": "Q", "team_id": 10, "position": "RB", "role": "carrilero",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"},
        {"player_id": 3, "player_name": "R", "team_id": 10, "position": "ST",
         "source": "manual", "data_quality": "alta", "confidence": "media"}])
    _write(ext, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "E", "kickoff_time": "x", "temperature": 30,
         "source": "plantilla_kickoff", "data_quality": "media", "confidence": "media"}])
    _seed_empty(ext, skip=("player_positional_profiles.csv", "weather_by_fixture.csv"))

    # guard --strict over the RAW data must FAIL (manual data present)
    raw = guard.evaluate(ext)
    assert raw["strict_ok"] is False

    # build the filtered snapshot, then guard --strict over the SNAPSHOT must PASS
    snap_dir = tmp_path / "snap"
    snap.build(ext, snap_dir, write=True)
    snap_rep = guard.evaluate(snap_dir)
    assert snap_rep["strict_ok"] is True and snap_rep["violations"] == []
    assert snap_rep["manual_protected_rows"] == 0 and snap_rep["manual_protected_cells"] == 0
    assert snap_rep["would_commit"] is True                       # the clean auto row survived


# ---------------------------------------------------------------- simulation: empty vs changed
def test_simulation_detects_empty_commit(tmp_path):
    # snapshot dir with only header-only files -> nothing to add -> empty commit
    snap_dir = tmp_path / "snap"
    snap_dir.mkdir()
    for fname in snap.SNAPSHOT_FILES:
        _write(snap_dir, fname, [])
    ext = _ext(tmp_path)
    _seed_empty(ext)
    rep = sim.simulate(snap_dir, ext)
    assert rep["empty_commit"] is True and rep["would_commit"] is False
    assert rep["add_set"] == [] and rep["paths_with_changes"] == []


def test_simulation_detects_paths_with_changes(tmp_path):
    # snapshot has a referee row that data/external does NOT -> a real diff -> path listed
    snap_dir = tmp_path / "snap"
    snap_dir.mkdir()
    for fname in snap.SNAPSHOT_FILES:
        _write(snap_dir, fname, [])
    _write(snap_dir, "fixture_referees.csv", [{"fixture_id": 1, "referee_name": "Mr Ref"}])
    ext = _ext(tmp_path)
    _seed_empty(ext)                                             # data/external has no referees
    rep = sim.simulate(snap_dir, ext)
    assert rep["would_commit"] is True and rep["empty_commit"] is False
    assert any("fixture_referees.csv" in p for p in rep["paths_with_changes"])


# ---------------------------------------------------------------- real data/external is never mutated
def test_build_does_not_mutate_real_data_external():
    real = snap.EXT_DIR
    before = {f: (real / f).read_bytes() for f in prep.COLUMNS if (real / f).exists()}
    # build against the REAL data/external but write the snapshot to a throwaway dir
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        snap.build(real, Path(td) / "snap", write=True)
    after = {f: (real / f).read_bytes() for f in prep.COLUMNS if (real / f).exists()}
    assert before == after                                       # data/external bytes unchanged
