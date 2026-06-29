"""
Fase 4C-5 offline tests (NO network, NO API, NO scraping, NO real git push, NO betting, NO mutation of
the real data/external). Cover the safe snapshot APPLIER (preflight gates + copy + dry-run), the
controlled COMMITTER (explicit allow-list, empty-commit, forbidden-path block, no push), and that the
workflow only stages explicit paths (never `git add data/external` wholesale, never `git add .`).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402
import guard_worldcup_external_persistence as guard  # noqa: E402
import build_worldcup_external_persistable_snapshot as snap  # noqa: E402
import apply_worldcup_external_persistable_snapshot as appl  # noqa: E402
import commit_worldcup_external_auto_persistence as commit  # noqa: E402

WORKFLOW = ROOT / ".github" / "workflows" / "vsigma_worldcup_cards.yml"


def _write(d, fname, rows):
    cols = prep.COLUMNS[fname]
    pd.DataFrame(rows, columns=cols).to_csv(d / fname, index=False)


def _seed_empty(d, skip=()):
    for fname in prep.COLUMNS:
        if fname not in skip:
            _write(d, fname, [])


def _clean_ext(tmp_path):
    """A data/external dir holding only clean auto-derived rows (manual-free)."""
    ext = tmp_path / "ext"
    ext.mkdir()
    _write(ext, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "DEF",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _write(ext, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "E", "kickoff_time": "x", "source": "plantilla_kickoff",
         "data_quality": "pendiente", "confidence": "pendiente"}])
    _seed_empty(ext, skip=("player_positional_profiles.csv", "weather_by_fixture.csv"))
    return ext


# ---------------------------------------------------------------- APPLY: allowed snapshot
def test_apply_allowed_snapshot_copies(tmp_path):
    ext = _clean_ext(tmp_path)
    snap_dir = tmp_path / "snap"
    snap.build(ext, snap_dir, write=True)
    # wipe the dest rows so the copy is observable (still manual-free)
    _write(ext, "player_positional_profiles.csv", [])
    rep = appl.apply(snap_dir, ext, dry_run=False)
    assert rep["ok"] is True and not rep["blockers"]
    assert "data/external/player_positional_profiles.csv" in rep["copied"]
    # the dest now has the snapshot's auto row back
    df = pd.read_csv(ext / "player_positional_profiles.csv")
    assert len(df) == 1 and df.iloc[0]["position"] == "DEF"


def test_apply_blocks_forbidden_file_in_snapshot(tmp_path):
    ext = _clean_ext(tmp_path)
    snap_dir = tmp_path / "snap"
    snap.build(ext, snap_dir, write=True)
    # a forbidden file sneaks into the snapshot dir -> must block, copy nothing
    _write(snap_dir, "player_xg_xa.csv", [{"player_id": 9, "xg90": 0.4}])
    rep = appl.apply(snap_dir, ext, dry_run=False)
    assert rep["ok"] is False
    assert any("no_forbidden_in_snapshot" in b or "prohibidos" in b for b in rep["blockers"])
    assert rep["copied"] == []                                   # nothing copied
    # forbidden file is never written into data/external
    assert not (ext / "player_xg_xa.csv").exists() or len(pd.read_csv(ext / "player_xg_xa.csv")) == 0


def test_apply_blocks_when_snapshot_has_manual_data(tmp_path):
    ext = _clean_ext(tmp_path)
    snap_dir = tmp_path / "snap"
    snap_dir.mkdir()
    # hand-built snapshot with a MANUAL scouting cell -> guard --strict fails -> block
    _write(snap_dir, "player_positional_profiles.csv", [
        {"player_id": 1, "player_name": "P", "team_id": 10, "position": "RB", "role": "carrilero",
         "source": "api_football_lineup_position", "data_quality": "media", "confidence": "baja"}])
    _seed_empty(snap_dir, skip=("player_positional_profiles.csv",))
    rep = appl.apply(snap_dir, ext, dry_run=False)
    assert rep["ok"] is False
    assert any("guard_strict" in b or "manual" in b for b in rep["blockers"])
    assert rep["copied"] == []


def test_apply_blocks_when_data_external_has_manual_data(tmp_path):
    # the critical safeguard: data/external holds a manual edit -> copying the (blanked) snapshot would
    # destroy it -> ABORT, do not touch data/external.
    ext = tmp_path / "ext"
    ext.mkdir()
    _write(ext, "weather_by_fixture.csv", [
        {"fixture_id": 1, "venue": "E", "kickoff_time": "x", "temperature": 30,   # MANUAL measurement
         "source": "plantilla_kickoff", "data_quality": "media", "confidence": "media"}])
    _seed_empty(ext, skip=("weather_by_fixture.csv",))
    snap_dir = tmp_path / "snap"
    snap.build(ext, snap_dir, write=True)                       # snapshot blanks the manual temp
    before = (ext / "weather_by_fixture.csv").read_bytes()
    rep = appl.apply(snap_dir, ext, dry_run=False)
    assert rep["ok"] is False
    assert any("manual_free" in b or "MANUALES" in b for b in rep["blockers"])
    assert (ext / "weather_by_fixture.csv").read_bytes() == before   # untouched -> manual temp survives


def test_apply_dry_run_does_not_modify_data_external(tmp_path):
    ext = _clean_ext(tmp_path)
    snap_dir = tmp_path / "snap"
    snap.build(ext, snap_dir, write=True)
    _write(ext, "player_positional_profiles.csv", [])           # make snapshot differ from dest
    before = {f: (ext / f).read_bytes() for f in prep.COLUMNS}
    rep = appl.apply(snap_dir, ext, dry_run=True)
    assert rep["ok"] is True and rep["dry_run"] is True
    assert rep["would_commit"] is True                          # it WOULD change something
    after = {f: (ext / f).read_bytes() for f in prep.COLUMNS}
    assert before == after                                      # but dry-run wrote nothing


# ---------------------------------------------------------------- COMMIT: pure plan
def test_commit_detects_empty_commit():
    pl = commit.plan([])
    assert pl["empty_commit"] is True and pl["blocked"] is False and pl["would_commit"] is False
    assert pl["add_set"] == []


def test_commit_blocks_forbidden_path():
    pl = commit.plan(["data/external/player_xg_xa.csv"])
    assert pl["blocked"] is True
    assert "data/external/player_xg_xa.csv" in pl["forbidden"]
    assert pl["add_set"] == []                                  # never staged


def test_commit_blocks_any_non_allowlisted_path():
    pl = commit.plan(["data/external/weather_by_fixture.csv", "data/external/README.md"])
    assert pl["blocked"] is True                                # README is outside the allow-list
    assert "data/external/README.md" in pl["forbidden"]


def test_commit_allows_only_explicit_paths():
    pl = commit.plan(["data/external/weather_by_fixture.csv",
                      "data/external/player_positional_profiles.csv"])
    assert pl["blocked"] is False and pl["would_commit"] is True
    assert set(pl["add_set"]) == {"data/external/weather_by_fixture.csv",
                                  "data/external/player_positional_profiles.csv"}
    assert all(p in commit.ALLOWED_PATHS for p in pl["add_set"])


def test_commit_allowlist_is_exactly_the_four():
    assert commit.ALLOWED_PATHS == [
        "data/external/fixture_referees.csv",
        "data/external/weather_by_fixture.csv",
        "data/external/set_piece_takers.csv",
        "data/external/player_positional_profiles.csv",
    ]


# ---------------------------------------------------------------- COMMIT: run() with a fake git runner
class _FakeProc:
    def __init__(self, stdout="", returncode=0, stderr=""):
        self.stdout, self.returncode, self.stderr = stdout, returncode, stderr


def test_commit_run_executes_only_explicit_add(monkeypatch):
    calls = []

    def fake(args):
        calls.append(list(args))
        if args[:2] == ["diff", "--name-only"]:
            return _FakeProc(stdout="data/external/weather_by_fixture.csv\n")
        return _FakeProc(returncode=0)

    code, pl = commit.run(execute=True, runner=fake)
    assert code == 0 and pl["commit_done"] is True
    add_calls = [c for c in calls if c and c[0] == "add"]
    assert add_calls == [["add", "--", "data/external/weather_by_fixture.csv"]]
    commit_calls = [c for c in calls if c and c[0] == "commit"]
    assert commit_calls and commit_calls[0][-1] == commit.COMMIT_MESSAGE
    assert not any(c and c[0] == "push" for c in calls)         # NEVER pushes


def test_commit_run_blocks_forbidden_without_touching_repo():
    calls = []

    def fake(args):
        calls.append(list(args))
        if args[:2] == ["diff", "--name-only"]:
            return _FakeProc(stdout="data/external/coach_tactical_profiles.csv\n")
        return _FakeProc(returncode=0)

    code, pl = commit.run(execute=True, runner=fake)
    assert code == 1 and pl["blocked"] is True
    assert not any(c and c[0] in ("add", "commit", "push") for c in calls)


def test_commit_run_empty_does_not_commit():
    calls = []

    def fake(args):
        calls.append(list(args))
        if args[:2] == ["diff", "--name-only"]:
            return _FakeProc(stdout="")
        return _FakeProc(returncode=0)

    code, pl = commit.run(execute=True, runner=fake)
    assert code == 0 and pl["empty_commit"] is True
    assert not any(c and c[0] in ("add", "commit", "push") for c in calls)


# ---------------------------------------------------------------- WORKFLOW shape
def _workflow_run_lines(non_comment_only=True):
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    lines = []
    for job in data["jobs"].values():
        for step in job.get("steps", []):
            run = step.get("run")
            if not run:
                continue
            for ln in run.splitlines():
                if non_comment_only and ln.lstrip().startswith("#"):
                    continue
                lines.append(ln)
    return lines


def test_workflow_has_explicit_external_paths():
    # the 4 explicit paths are documented in the persistence step and enforced by the committer script
    text = WORKFLOW.read_text(encoding="utf-8")
    for p in commit.ALLOWED_PATHS:
        assert p in text, f"workflow debe referenciar la ruta explícita {p}"
    # the persistence step must invoke the applier + the controlled committer (single source of truth)
    blob = "\n".join(_workflow_run_lines())
    assert "apply_worldcup_external_persistable_snapshot.py" in blob
    assert "commit_worldcup_external_auto_persistence.py --execute" in blob


def test_workflow_never_adds_data_external_wholesale():
    import re
    for ln in _workflow_run_lines():
        # a `git add data/external` NOT immediately followed by `/<file>` is a wholesale dir add -> forbidden
        assert not re.search(r"git add\s+data/external(?![/\w])", ln), f"add wholesale: {ln!r}"


def test_workflow_never_git_add_dot():
    import re
    for ln in _workflow_run_lines():
        assert not re.search(r"git add\s+\.(\s|$)", ln), f"git add . prohibido: {ln!r}"


def test_workflow_persistence_step_is_main_only():
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = [s for job in data["jobs"].values() for s in job.get("steps", [])]
    persist = [s for s in steps if s.get("name") and "4C-5" in s["name"]]
    assert persist, "falta el paso de persistencia Fase 4C-5"
    cond = persist[0].get("if", "")
    assert "refs/heads/main" in cond and "pull_request" in cond
