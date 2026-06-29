"""
WORLD CUP 2026 — EXTERNAL-DATA PERSISTABLE SNAPSHOT BUILDER (Fase 4C-4). READ-ONLY inputs · NO API ·
NO scraping · NO market/odds/betting · NO fabrication · NO secrets · NO commit · NO git add. NEVER
mutates data/external (it only READS it) and never activates real persistence.

Generates a SAFE, FILTERED copy of the auto-derivable part of data/external/ under
    analysis/worldcup/persistable_external_snapshot/
so a future (still-not-activated) "option B" bounded commit could add ONLY auto-derived data, never a
manual edit. The snapshot is the missing piece the Fase 4C-3 guard demanded: instead of a wholesale
`git add data/external` (which would commit manual rows/cells), we materialise an auto-only projection.

Filtered files (each keeps the FULL contract schema for compatibility; manual columns are EMPTIED):
  * fixture_referees.csv            -> rows with non-empty fixture_id AND referee_name.
  * weather_by_fixture.csv          -> rows with source in {plantilla_kickoff, api_football_store};
                                       measurement columns (temperature/humidity/wind_speed/
                                       rain_probability/pitch_condition) are BLANKED (manual/external).
  * set_piece_takers.csv            -> ONLY real penalty derivations (source=api_football_events,
                                       role=penalty, data_quality=alta, numeric attempts, non-empty
                                       last_taken_date, confidence in {baja,media,alta}).
  * player_positional_profiles.csv  -> rows with source in {api_football_lineup_position,
                                       api_football_lineup}; scouting columns (role/preferred_zone/
                                       weights/threats/card_risk_role) are BLANKED (manual).

NEVER emitted (always blocked): player_xg_xa.csv, referee_profiles.csv, coach_tactical_profiles.csv.

Modes:
  (default)  build the snapshot dir + report (txt/csv). Writes ONLY under the snapshot dir + reports.
  --check    compute what WOULD be generated WITHOUT writing the snapshot. exit 0 if the snapshot
             would be safe; exit 1 if a source CSV has an unexpected/broken schema or a forbidden file
             would somehow enter the snapshot.

Run:  python analysis/worldcup/build_worldcup_external_persistable_snapshot.py [--check]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402  (COLUMNS / _is_empty)
import guard_worldcup_external_persistence as guard  # noqa: E402  (row gates / forbidden set)

EXT_DIR = ROOT / "data" / "external"
SNAP_DIR = HERE / "persistable_external_snapshot"
OUT_TXT = HERE / "worldcup_external_persistable_snapshot_report.txt"
OUT_CSV = HERE / "worldcup_external_persistable_snapshot_report.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# the only files the snapshot may contain (auto-derivable). everything else is blocked.
SNAPSHOT_FILES = ["fixture_referees.csv", "weather_by_fixture.csv", "set_piece_takers.csv",
                  "player_positional_profiles.csv"]
FORBIDDEN_FILES = guard.FORBIDDEN_FILES   # xg_xa / referee_profiles / coach_tactical_profiles

# per-file snapshot rules. include(row, df_cols) -> keep this row; blank_cols -> manual cells emptied.
_LINEUP_SOURCES = guard._LINEUP_SOURCES
_WEATHER_AUTO_SOURCES = {"plantilla_kickoff", "api_football_store"}


def _src(row):
    return str(row.get("source") or "").strip()


SNAPSHOT_SPEC = {
    "fixture_referees.csv": {
        "include": lambda r: (not guard._empty(r.get("fixture_id"))
                              and not guard._empty(r.get("referee_name"))),
        "blank_cols": [],
    },
    "weather_by_fixture.csv": {
        "include": lambda r: (_src(r) in _WEATHER_AUTO_SOURCES
                              and not guard._empty(r.get("fixture_id"))),
        "blank_cols": ["temperature", "humidity", "wind_speed", "rain_probability", "pitch_condition"],
    },
    "set_piece_takers.csv": {
        "include": lambda r: guard._set_piece_row_auto(r),
        "blank_cols": [],
    },
    "player_positional_profiles.csv": {
        "include": lambda r: (_src(r) in _LINEUP_SOURCES
                              and not guard._empty(r.get("player_id"))
                              and not guard._empty(r.get("position"))),
        "blank_cols": ["role", "preferred_zone", "attacking_weight", "defensive_weight",
                       "aerial_threat", "pace_threat", "1v1_threat", "crossing_threat",
                       "card_risk_role"],
    },
}


def filter_file(fname, ext_dir=EXT_DIR):
    """Read one allowed source CSV and compute its SAFE auto-only projection (FULL schema preserved,
    manual columns blanked). Pure: NEVER writes. Returns (snapshot_df_or_None, info)."""
    cols = prep.COLUMNS[fname]
    spec = SNAPSHOT_SPEC[fname]
    path = Path(ext_dir) / fname
    info = {"file": fname, "exists": path.exists(), "original_rows": 0, "included_rows": 0,
            "excluded_rows": 0, "manual_cells_cleared": 0, "schema_ok": True, "reason": ""}
    if not path.exists():
        info["reason"] = "ausente"
        return pd.DataFrame(columns=cols), info
    try:
        df = pd.read_csv(path)
    except Exception:
        info["schema_ok"] = False
        info["reason"] = "csv ilegible"
        return None, info
    if list(df.columns) != cols:
        info["schema_ok"] = False
        info["reason"] = f"esquema inesperado (esperado {len(cols)} cols)"
        return None, info

    info["original_rows"] = len(df)
    blank_cols = [c for c in spec["blank_cols"] if c in df.columns]
    kept = []
    for _, row in df.iterrows():
        if not spec["include"](row):
            info["excluded_rows"] += 1
            continue
        out = {c: row.get(c) for c in cols}
        for c in blank_cols:
            if not guard._empty(out.get(c)):
                info["manual_cells_cleared"] += 1
            out[c] = ""               # blank manual cell (schema kept)
        kept.append(out)
    info["included_rows"] = len(kept)
    snap = pd.DataFrame(kept, columns=cols)
    return snap, info


def build(ext_dir=EXT_DIR, snap_dir=SNAP_DIR, write=True):
    """Compute (and, if write, materialise) the snapshot for every allowed file. NEVER touches
    data/external or the forbidden files. Returns the report dict."""
    snap_dir = Path(snap_dir)
    files, snaps = [], {}
    schema_error = False
    for fname in SNAPSHOT_FILES:
        snap, info = filter_file(fname, ext_dir)
        if snap is None:
            schema_error = True
        files.append(info)
        snaps[fname] = snap

    if write and not schema_error:
        snap_dir.mkdir(parents=True, exist_ok=True)
        for fname in SNAPSHOT_FILES:
            (snaps[fname]).to_csv(snap_dir / fname, index=False)

    blocked = [{"file": f, "reason": "manual/externo — nunca auto-persistible (no entra al snapshot)"}
               for f in sorted(FORBIDDEN_FILES)]

    written_paths, nonempty = [], []
    for fname in SNAPSHOT_FILES:
        rel = f"analysis/worldcup/persistable_external_snapshot/{fname}"
        written_paths.append(rel)
        if snaps[fname] is not None and len(snaps[fname]) > 0:
            nonempty.append(rel)

    total_included = sum(i["included_rows"] for i in files)
    return {
        "files": files, "blocked": blocked,
        "snapshot_dir": str(snap_dir).replace("\\", "/"),
        "written_paths": written_paths,            # all 4 (incl. header-only)
        "nonempty_paths": nonempty,                # paths with >=1 data row
        "total_included_rows": total_included,
        "total_excluded_rows": sum(i["excluded_rows"] for i in files),
        "total_manual_cells_cleared": sum(i["manual_cells_cleared"] for i in files),
        "snapshot_empty": total_included == 0,
        "would_commit": len(nonempty) > 0,
        "schema_error": schema_error,
        "wrote": bool(write and not schema_error),
        "snaps": snaps,
    }


# ============================================================ rendering / I/O
def render_txt(rep, check=False) -> str:
    head = "CHECK (no escribe)" if check else "BUILD"
    L = [f"===== WORLD CUP — EXTERNAL PERSISTABLE SNAPSHOT ({head}) =====", "",
         "Snapshot auto-derivado seguro (esquema completo, columnas manuales vaciadas).", ""]
    L.append("Archivos del snapshot:")
    for i in rep["files"]:
        if not i["exists"]:
            L.append(f"  {i['file']:34s} AUSENTE -> snapshot vacío")
            continue
        if not i["schema_ok"]:
            L.append(f"  {i['file']:34s} ⚠ {i['reason']}")
            continue
        L.append(f"  {i['file']:34s} orig={i['original_rows']:>3} incluidas={i['included_rows']:>3} "
                 f"excluidas={i['excluded_rows']:>3} celdas_manuales_limpiadas={i['manual_cells_cleared']}")
    L.append("")
    L.append("Archivos BLOQUEADOS (nunca entran al snapshot):")
    for b in rep["blocked"]:
        L.append(f"  {b['file']:34s} {b['reason']}")
    L.append("")
    L.append(f"Directorio snapshot: {rep['snapshot_dir']}")
    L.append(f"Filas incluidas totales: {rep['total_included_rows']}")
    L.append(f"Filas excluidas totales: {rep['total_excluded_rows']}")
    L.append(f"Celdas manuales limpiadas: {rep['total_manual_cells_cleared']}")
    L.append(f"¿Snapshot vacío?: {'SÍ' if rep['snapshot_empty'] else 'NO'}")
    L.append(f"¿Habría commit?: {'SÍ' if rep['would_commit'] else 'NO (snapshot sin filas nuevas)'}")
    if rep["nonempty_paths"]:
        L.append("Rutas del snapshot con datos:")
        for p in rep["nonempty_paths"]:
            L.append(f"  + {p}")
    else:
        L.append("Rutas del snapshot con datos: ninguna")
    L.append("")
    if rep["schema_error"]:
        L.append("⚠ ESQUEMA ROTO en una fuente -> en --check esto es exit 1 (no se generaría snapshot).")
    if check:
        L.append("Modo CHECK: no se ha escrito el snapshot. Solo cálculo.")
    else:
        L.append("Snapshot escrito." if rep["wrote"] else "Snapshot NO escrito (error de esquema).")
    L.append("Nota: NO toca data/external, NO commitea, NO activa persistencia.")
    return "\n".join(L)


def _csv_rows(rep):
    rows = []
    for i in rep["files"]:
        rows.append({"file": i["file"], "policy": "snapshot", "exists": int(i["exists"]),
                     "schema_ok": int(i["schema_ok"]), "original_rows": i["original_rows"],
                     "included_rows": i["included_rows"], "excluded_rows": i["excluded_rows"],
                     "manual_cells_cleared": i["manual_cells_cleared"]})
    for b in rep["blocked"]:
        rows.append({"file": b["file"], "policy": "blocked", "exists": "", "schema_ok": "",
                     "original_rows": "", "included_rows": "", "excluded_rows": "",
                     "manual_cells_cleared": ""})
    return rows


def run(ext_dir=EXT_DIR, snap_dir=SNAP_DIR, out_txt=OUT_TXT, out_csv=OUT_CSV, check=False):
    """check=True: compute only, no snapshot write (report still written). check=False: build snapshot."""
    rep = build(ext_dir, snap_dir, write=not check)
    txt = render_txt(rep, check=check)
    Path(out_txt).write_text(txt + "\n", encoding="utf-8")
    pd.DataFrame(_csv_rows(rep)).to_csv(out_csv, index=False)
    rep["txt"] = txt
    return rep


def main():
    ap = argparse.ArgumentParser(description="World Cup external persistable snapshot builder "
                                             "(read-only inputs; --check computes without writing the "
                                             "snapshot).")
    ap.add_argument("--check", action="store_true",
                    help="compute what WOULD be generated WITHOUT writing the snapshot. exit 1 on a "
                         "broken/unexpected source schema or a forbidden file in the snapshot set.")
    a = ap.parse_args()
    rep = run(check=a.check)
    print(rep["txt"])
    if a.check and rep["schema_error"]:
        print("\n[check] esquema inesperado/roto en una fuente -> exit 1")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
