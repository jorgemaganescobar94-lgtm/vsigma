"""
WORLD CUP 2026 — EXTERNAL-PERSISTENCE COMMIT SIMULATION (Fase 4C-4). READ-ONLY · NO API · NO scraping ·
NO market/odds/betting · NO secrets. CRITICAL: this script NEVER runs `git add`, NEVER runs
`git commit`, NEVER pushes, and NEVER modifies main or data/external. It only SIMULATES what a future
(still-not-activated) "option B" bounded commit WOULD do, so the decision is data-driven.

What it simulates, purely from the filtered snapshot dir vs data/external:
  * which explicit paths a bounded `git add` WOULD target (snapshot CSVs with >=1 data row);
  * whether each would introduce a REAL change vs the current data/external content (a "diff"), so we
    do not stage a no-op;
  * whether the whole thing would be an EMPTY commit (nothing to add / nothing changed).

It deliberately works on the snapshot (auto-only, manual columns blanked) the Fase 4C-4 builder
produced — never on raw data/external — so simulating can never leak a manual edit into the add-set.

Output (read-only artifact):
  * analysis/worldcup/worldcup_external_persistence_commit_simulation.txt

Run:  python analysis/worldcup/simulate_worldcup_external_persistence_commit.py [--snapshot DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402  (COLUMNS)
import build_worldcup_external_persistable_snapshot as snap  # noqa: E402  (SNAPSHOT_FILES / dirs)

EXT_DIR = ROOT / "data" / "external"
SNAP_DIR = snap.SNAP_DIR
OUT_TXT = HERE / "worldcup_external_persistence_commit_simulation.txt"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _read_csv(path):
    try:
        return pd.read_csv(path) if Path(path).exists() else None
    except Exception:
        return None


def _frames_differ(a, b) -> bool:
    """True if the two dataframes differ in shape or content (NaN-insensitive comparison)."""
    if a is None or b is None:
        return (a is None) != (b is None)
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        return True
    aa = a.fillna("").astype(str).reset_index(drop=True)
    bb = b.fillna("").astype(str).reset_index(drop=True)
    return not aa.equals(bb)


def simulate(snap_dir=SNAP_DIR, ext_dir=EXT_DIR):
    """Pure simulation. Reads the snapshot (and data/external for the diff check) and returns a dict.
    NEVER calls git, NEVER writes data/external, NEVER commits."""
    snap_dir, ext_dir = Path(snap_dir), Path(ext_dir)
    files = []
    paths_with_changes = []
    snapshot_present = snap_dir.exists()
    for fname in snap.SNAPSHOT_FILES:
        sp = snap_dir / fname
        sdf = _read_csv(sp)
        edf = _read_csv(ext_dir / fname)
        snap_rows = 0 if sdf is None else len(sdf)
        would_add = sdf is not None and snap_rows > 0
        changed = bool(would_add and _frames_differ(sdf, edf))
        rel = f"analysis/worldcup/persistable_external_snapshot/{fname}"
        files.append({"file": fname, "snapshot_exists": sp.exists(), "snapshot_rows": snap_rows,
                      "would_add": would_add, "changed": changed,
                      "ext_rows": 0 if edf is None else len(edf), "path": rel})
        if changed:
            paths_with_changes.append(rel)

    would_commit = len(paths_with_changes) > 0
    return {
        "snapshot_present": snapshot_present,
        "snapshot_dir": str(snap_dir).replace("\\", "/"),
        "files": files,
        "add_set": [f["path"] for f in files if f["would_add"]],
        "paths_with_changes": paths_with_changes,
        "would_commit": would_commit,
        "empty_commit": not would_commit,
    }


def render_txt(rep) -> str:
    L = ["===== WORLD CUP — SIMULACIÓN DE COMMIT DE PERSISTENCIA EXTERNA (NO ejecuta git) =====", "",
         f"Snapshot: {rep['snapshot_dir']}"
         f"{'' if rep['snapshot_present'] else '  (AUSENTE -> nada que simular)'}", ""]
    L.append("Por archivo:")
    for f in rep["files"]:
        if not f["snapshot_exists"]:
            L.append(f"  {f['file']:34s} sin snapshot")
            continue
        tag = "CAMBIO" if f["changed"] else ("igual" if f["would_add"] else "vacío")
        L.append(f"  {f['file']:34s} snapshot={f['snapshot_rows']:>3} data/external={f['ext_rows']:>3} "
                 f"-> {tag}")
    L.append("")
    if rep["add_set"]:
        L.append("git add que SE SIMULARÍA (rutas explícitas, NO ejecutado):")
        for p in rep["add_set"]:
            L.append(f"  git add {p}   # SIMULADO — no ejecutado")
    else:
        L.append("git add simulado: ninguno (sin filas auto-persistibles)")
    L.append("")
    if rep["paths_with_changes"]:
        L.append("Rutas con DIFF real frente a data/external:")
        for p in rep["paths_with_changes"]:
            L.append(f"  ~ {p}")
    else:
        L.append("Rutas con diff real: ninguna")
    L.append("")
    L.append(f"¿Commit vacío?: {'SÍ (nada que commitear)' if rep['empty_commit'] else 'NO'}")
    L.append(f"¿Habría commit?: {'SÍ' if rep['would_commit'] else 'NO'}")
    L.append("")
    L.append("NO se ha ejecutado git add. NO se ha ejecutado git commit. NO se ha tocado main ni "
             "data/external. Persistencia automática SIGUE desactivada.")
    return "\n".join(L)


def run(snap_dir=SNAP_DIR, ext_dir=EXT_DIR, out_txt=OUT_TXT):
    rep = simulate(snap_dir, ext_dir)
    txt = render_txt(rep)
    Path(out_txt).write_text(txt + "\n", encoding="utf-8")
    rep["txt"] = txt
    return rep


def main():
    ap = argparse.ArgumentParser(description="Simulate (NEVER execute) the bounded option-B commit of "
                                             "the filtered external snapshot. No git add/commit/push.")
    ap.add_argument("--snapshot", metavar="DIR", default=str(SNAP_DIR),
                    help="snapshot dir to simulate against (default: the Fase 4C-4 snapshot dir).")
    a = ap.parse_args()
    rep = run(snap_dir=Path(a.snapshot))
    print(rep["txt"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
