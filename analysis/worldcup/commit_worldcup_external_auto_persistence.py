"""
WORLD CUP 2026 — CONTROLLED AUTO-PERSISTENCE COMMITTER (Fase 4C-5, option B). NO API · NO scraping · NO
market/odds/betting · NO secrets · NO PUSH. Stages and commits ONLY the four auto-derived external CSVs,
with an explicit path allow-list and a final `git diff` guard. It NEVER pushes (push is controlled by the
GitHub Actions workflow, never here) and by default it does NOT mutate the repo — you must pass
--execute. Without --execute it only reports what it WOULD do.

Allow-list (the ONLY paths this script may ever stage):
    data/external/fixture_referees.csv
    data/external/weather_by_fixture.csv
    data/external/set_piece_takers.csv
    data/external/player_positional_profiles.csv

Final safety guard (section 6): `git diff --name-only HEAD -- data/external` must NOT contain ANY path
outside the allow-list. If it does (e.g. a forbidden xg_xa/referee_profiles/coach file changed, or the
README), the script BLOCKS (exit 1) and stages/commits nothing.

Behaviour:
  * no changes under the allow-list  -> empty commit -> exit 0, nothing committed.
  * a non-allow-listed data/external path changed -> BLOCK -> exit 1.
  * allow-listed changes only:
      --execute  -> git add <those explicit paths> && git commit -m
                    "chore(worldcup): persist auto-derived external data [skip ci]"   (NO push)
      (default)  -> report the planned add-set + commit, mutate NOTHING.

Run:  python analysis/worldcup/commit_worldcup_external_auto_persistence.py [--execute]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# the ONLY paths that may ever be staged (posix, git-add-ready)
ALLOWED_PATHS = [
    "data/external/fixture_referees.csv",
    "data/external/weather_by_fixture.csv",
    "data/external/set_piece_takers.csv",
    "data/external/player_positional_profiles.csv",
]
COMMIT_MESSAGE = "chore(worldcup): persist auto-derived external data [skip ci]"


def _git(args, cwd=ROOT):
    """Thin git wrapper. Returns CompletedProcess. NEVER pushes (no caller passes 'push')."""
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def changed_external_paths(cwd=ROOT, runner=None):
    """All data/external paths that differ from HEAD (staged or not), posix-normalised."""
    runner = runner or (lambda args: _git(args, cwd))
    r = runner(["diff", "--name-only", "HEAD", "--", "data/external"])
    out = getattr(r, "stdout", "") or ""
    return [ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()]


def plan(changed_paths):
    """Pure decision from the list of changed data/external paths. NEVER calls git."""
    changed = [p.replace("\\", "/") for p in changed_paths]
    allowed = [p for p in changed if p in ALLOWED_PATHS]
    forbidden = [p for p in changed if p not in ALLOWED_PATHS]
    blocked = len(forbidden) > 0
    empty = (len(allowed) == 0)
    return {
        "changed": changed, "allowed": allowed, "forbidden": forbidden,
        "blocked": blocked, "empty_commit": empty and not blocked,
        "would_commit": (not blocked) and (not empty),
        "add_set": allowed,
        "message": COMMIT_MESSAGE,
    }


def run(execute=False, cwd=ROOT, runner=None):
    """Compute the plan and (only with execute=True and a clean allow-listed diff) git add + commit.
    NEVER pushes. Returns (exit_code, report)."""
    runner = runner or (lambda args: _git(args, cwd))
    changed = changed_external_paths(cwd, runner)
    pl = plan(changed)
    pl["executed"] = False
    pl["commit_done"] = False

    if pl["blocked"]:
        return 1, pl
    if pl["empty_commit"]:
        return 0, pl                      # nothing to commit -> success, no commit
    if not execute:
        return 0, pl                      # default: report only, mutate nothing
    # execute: stage ONLY the explicit allow-listed paths, then commit (NO push)
    add = runner(["add", "--", *pl["add_set"]])
    if getattr(add, "returncode", 1) != 0:
        pl["error"] = "git add falló: " + (getattr(add, "stderr", "") or "")
        return 1, pl
    commit = runner(["commit", "-m", pl["message"]])
    pl["executed"] = True
    pl["commit_done"] = getattr(commit, "returncode", 1) == 0
    if not pl["commit_done"]:
        pl["error"] = "git commit falló: " + (getattr(commit, "stderr", "") or "")
        return 1, pl
    return 0, pl


def render_txt(pl, execute) -> str:
    L = ["===== WORLD CUP — COMMIT CONTROLADO DE PERSISTENCIA EXTERNA (NO push) =====", ""]
    L.append("Allow-list de rutas (únicas permitidas):")
    for p in ALLOWED_PATHS:
        L.append(f"  · {p}")
    L.append("")
    L.append("Cambios detectados en data/external vs HEAD:")
    if pl["changed"]:
        for p in pl["changed"]:
            tag = "PERMITIDA" if p in ALLOWED_PATHS else "PROHIBIDA"
            L.append(f"  [{tag}] {p}")
    else:
        L.append("  (ninguno)")
    L.append("")
    if pl["blocked"]:
        L.append("RESULTADO: BLOQUEADO -> ruta fuera de la allow-list (exit 1). No se commitea nada.")
        for p in pl["forbidden"]:
            L.append(f"  ✗ {p}")
        return "\n".join(L)
    if pl["empty_commit"]:
        L.append("RESULTADO: commit VACÍO (sin cambios permitidos) -> exit 0, no se commitea.")
        return "\n".join(L)
    L.append("git add que se aplicaría (rutas explícitas):")
    for p in pl["add_set"]:
        L.append(f"  git add {p}")
    L.append(f"git commit -m \"{pl['message']}\"")
    L.append("(push: NUNCA aquí — lo controla el workflow de GitHub Actions)")
    L.append("")
    if execute:
        L.append("EJECUTADO." if pl.get("commit_done") else "EJECUCIÓN con error: "
                 + pl.get("error", ""))
    else:
        L.append("Modo informe (sin --execute): no se ha tocado el repo.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Commit ONLY the 4 auto-derived external CSVs (explicit "
                                             "allow-list + diff guard). NEVER pushes. Default = report "
                                             "only; pass --execute to actually git add + commit.")
    ap.add_argument("--execute", action="store_true",
                    help="actually `git add` the allow-listed paths and `git commit`. Without it the "
                         "script only reports (no repo mutation).")
    a = ap.parse_args()
    code, pl = run(execute=a.execute)
    print(render_txt(pl, a.execute))
    return code


if __name__ == "__main__":
    sys.exit(main())
