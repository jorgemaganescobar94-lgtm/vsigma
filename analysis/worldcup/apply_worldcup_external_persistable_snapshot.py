"""
WORLD CUP 2026 — SAFE EXTERNAL-PERSISTABLE-SNAPSHOT APPLIER (Fase 4C-5, option B). NO API · NO scraping ·
NO market/odds/betting · NO fabrication · NO secrets · NO push. This is the ONLY script that copies the
filtered auto-only snapshot into data/external/, and it does so ONLY when it is provably safe.

It applies analysis/worldcup/persistable_external_snapshot/ to data/external/ for the FOUR allowed files:
    fixture_referees.csv, weather_by_fixture.csv, set_piece_takers.csv, player_positional_profiles.csv
It NEVER touches the forbidden files (player_xg_xa.csv, referee_profiles.csv, coach_tactical_profiles.csv)
— it never reads or writes them.

TWO blocking pre-conditions (either failing => exit 1, data/external UNTOUCHED):
  1. The SNAPSHOT is clean & well-formed: it exists, contains only allowed files (no forbidden file),
     every file matches its contract schema, and `guard --strict` over it passes (0 manual rows/cells).
  2. The CURRENT data/external is MANUAL-FREE for the 4 files (guard reports 0 manual rows/cells). This
     is the critical safeguard: the snapshot has manual columns BLANKED, so copying it over a file that
     holds a manual edit would DESTROY that edit. If any manual data is present, we ABORT rather than
     overwrite it. (Today data/external is 100% auto-derived, so the copy is identity/refresh-only.)

Modes:
  (default)  apply: validate, then copy the 4 allowed snapshot files into data/external.
  --dry-run  report which files WOULD be copied, whether each differs, and whether a commit would
             follow — WITHOUT modifying data/external.

Run:  python analysis/worldcup/apply_worldcup_external_persistable_snapshot.py [--dry-run]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402  (COLUMNS)
import guard_worldcup_external_persistence as guard  # noqa: E402  (evaluate / forbidden set)
import build_worldcup_external_persistable_snapshot as snap  # noqa: E402  (SNAPSHOT_FILES / dirs)
import simulate_worldcup_external_persistence_commit as sim  # noqa: E402  (_frames_differ)

EXT_DIR = ROOT / "data" / "external"
SNAP_DIR = snap.SNAP_DIR
ALLOWED_FILES = list(snap.SNAPSHOT_FILES)
FORBIDDEN_FILES = guard.FORBIDDEN_FILES

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def preflight(snap_dir=SNAP_DIR, ext_dir=EXT_DIR):
    """Run every blocking safety check. Returns (ok, info). NEVER writes."""
    snap_dir, ext_dir = Path(snap_dir), Path(ext_dir)
    info = {"checks": [], "snapshot_dir": str(snap_dir).replace("\\", "/"), "blockers": []}

    def add(name, passed, detail=""):
        info["checks"].append({"check": name, "ok": bool(passed), "detail": detail})
        if not passed:
            info["blockers"].append(f"{name}: {detail}" if detail else name)

    # 1) snapshot dir present
    add("snapshot_exists", snap_dir.exists(), "" if snap_dir.exists() else "directorio ausente")
    if not snap_dir.exists():
        return False, info

    # 2) no forbidden file inside the snapshot dir
    present = {p.name for p in snap_dir.glob("*.csv")}
    forbidden_present = sorted(present & set(FORBIDDEN_FILES))
    add("no_forbidden_in_snapshot", not forbidden_present,
        ("prohibidos presentes: " + ", ".join(forbidden_present)) if forbidden_present else "")

    # 3) only allowed files (anything unexpected blocks)
    unexpected = sorted(present - set(ALLOWED_FILES))
    add("only_allowed_files", not unexpected,
        ("ficheros inesperados: " + ", ".join(unexpected)) if unexpected else "")

    # 4) schema of each present allowed file matches the contract
    schema_bad = []
    for f in ALLOWED_FILES:
        p = snap_dir / f
        if not p.exists():
            continue
        try:
            cols = list(pd.read_csv(p, nrows=0).columns)
        except Exception:
            schema_bad.append(f"{f} (ilegible)")
            continue
        if cols != prep.COLUMNS[f]:
            schema_bad.append(f"{f} (esquema)")
    add("snapshot_schema_ok", not schema_bad, ", ".join(schema_bad))

    # 5) guard --strict over the SNAPSHOT must pass (0 manual rows/cells)
    snap_rep = guard.evaluate(snap_dir)
    add("guard_strict_snapshot", snap_rep["strict_ok"],
        "; ".join(snap_rep["violations"]) if not snap_rep["strict_ok"] else "")
    add("snapshot_zero_manual",
        snap_rep["manual_protected_rows"] == 0 and snap_rep["manual_protected_cells"] == 0,
        f"filas={snap_rep['manual_protected_rows']} celdas={snap_rep['manual_protected_cells']}")

    # 6) CURRENT data/external must be MANUAL-FREE for the 4 files (else copy would blank manual data)
    ext_rep = guard.evaluate(ext_dir)
    ext_clean = (ext_rep["manual_protected_rows"] == 0 and ext_rep["manual_protected_cells"] == 0)
    add("data_external_manual_free", ext_clean,
        "" if ext_clean else (f"data/external tiene datos MANUALES "
                              f"(filas={ext_rep['manual_protected_rows']} "
                              f"celdas={ext_rep['manual_protected_cells']}); copiar los borraría -> ABORTA"))

    info["snapshot_report"] = snap_rep
    info["ext_report"] = ext_rep
    return len(info["blockers"]) == 0, info


def plan_copy(snap_dir=SNAP_DIR, ext_dir=EXT_DIR):
    """Per-file copy plan (which files, would each change). Pure, NEVER writes."""
    snap_dir, ext_dir = Path(snap_dir), Path(ext_dir)
    files = []
    for f in ALLOWED_FILES:
        sp, ep = snap_dir / f, ext_dir / f
        sdf = pd.read_csv(sp) if sp.exists() else None
        edf = pd.read_csv(ep) if ep.exists() else None
        changed = bool(sp.exists() and sim._frames_differ(sdf, edf))
        files.append({"file": f, "snapshot_exists": sp.exists(),
                      "snapshot_rows": 0 if sdf is None else len(sdf),
                      "ext_rows": 0 if edf is None else len(edf), "changed": changed,
                      "dest": f"data/external/{f}"})
    return files


def apply(snap_dir=SNAP_DIR, ext_dir=EXT_DIR, dry_run=False):
    """Validate, then (unless dry_run) copy the 4 allowed snapshot files into data/external. Returns a
    report dict. On any blocker: ok=False, NOTHING copied. NEVER touches forbidden files."""
    ok, info = preflight(snap_dir, ext_dir)
    files = plan_copy(snap_dir, ext_dir) if ok else []
    copied = []
    would_change = [f for f in files if f["changed"]]
    if ok and not dry_run:
        for f in files:
            if f["snapshot_exists"]:
                shutil.copyfile(Path(snap_dir) / f["file"], Path(ext_dir) / f["file"])
                copied.append(f["dest"])
    return {
        "ok": ok, "dry_run": dry_run, "blockers": info["blockers"], "checks": info["checks"],
        "snapshot_dir": info["snapshot_dir"], "files": files,
        "would_change_paths": [f["dest"] for f in would_change],
        "would_commit": len(would_change) > 0,
        "copied": copied,
        "forbidden_untouched": sorted(FORBIDDEN_FILES),
        "info": info,
    }


def render_txt(rep) -> str:
    head = "DRY-RUN (no escribe)" if rep["dry_run"] else "APPLY"
    L = [f"===== WORLD CUP — APPLY PERSISTABLE SNAPSHOT ({head}) =====", "",
         f"Snapshot: {rep['snapshot_dir']}", ""]
    L.append("Comprobaciones de seguridad (todas deben pasar):")
    for c in rep["checks"]:
        L.append(f"  [{'OK ' if c['ok'] else 'X  '}] {c['check']}"
                 f"{(' — ' + c['detail']) if c['detail'] else ''}")
    L.append("")
    if not rep["ok"]:
        L.append("RESULTADO: BLOQUEADO -> data/external NO se toca (exit 1).")
        for b in rep["blockers"]:
            L.append(f"  ✗ {b}")
        L.append("")
        L.append("Nota: ningún fichero copiado. Archivos prohibidos nunca tocados: "
                 + ", ".join(rep["forbidden_untouched"]))
        return "\n".join(L)
    L.append("Plan de copia (snapshot -> data/external):")
    for f in rep["files"]:
        tag = "CAMBIO" if f["changed"] else "igual"
        L.append(f"  {f['file']:34s} snapshot={f['snapshot_rows']:>3} data/external={f['ext_rows']:>3} "
                 f"-> {tag}  ({f['dest']})")
    L.append("")
    L.append(f"¿Habría diff/commit?: {'SÍ' if rep['would_commit'] else 'NO (idéntico, commit vacío)'}")
    if rep["would_change_paths"]:
        L.append("Rutas que cambiarían:")
        for p in rep["would_change_paths"]:
            L.append(f"  ~ {p}")
    if rep["dry_run"]:
        L.append("\nDRY-RUN: data/external NO modificado.")
    else:
        L.append("\nCopiados: " + (", ".join(rep["copied"]) if rep["copied"] else "ninguno"))
    L.append("Archivos PROHIBIDOS nunca tocados: " + ", ".join(rep["forbidden_untouched"]))
    L.append("Nunca hace git add/commit/push. (Eso lo hace commit_worldcup_external_auto_persistence.py)")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Safely apply the filtered auto-only snapshot to "
                                             "data/external (option B). Blocks unless snapshot is clean "
                                             "AND data/external is manual-free. --dry-run = no writes.")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what WOULD be copied / changed WITHOUT modifying data/external.")
    a = ap.parse_args()
    rep = apply(dry_run=a.dry_run)
    print(render_txt(rep))
    if not rep["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
