"""
WORLD CUP 2026 — EXTERNAL-DATA PERSISTENCE GUARD (Fase 4C-3). READ-ONLY by default · NO API · NO
scraping · NO writes to data/external · NO commit · NO betting.

Decides which data/external rows/cells would be SAFE to auto-persist from CI under persistence policy
"option B" (docs/worldcup_external_data_persistence_policy.md) — WITHOUT activating anything. It only
audits and reports; it never filters, writes or commits a CSV.

Policy enforced here (the ONLY files that may ever be auto-persisted, and only their auto-derived part):
  * fixture_referees.csv            -> fixture_id + referee_name (from store/prepare)
  * weather_by_fixture.csv          -> ONLY fixture_id, kickoff_time, venue, source, data_quality,
                                       confidence. Real weather measurements are MANUAL -> protected.
  * set_piece_takers.csv            -> ONLY rows with source=api_football_events, role=penalty,
                                       data_quality=alta, numeric attempts, non-empty last_taken_date,
                                       confidence in {baja,media,alta}. Anything else is protected.
  * player_positional_profiles.csv  -> ONLY player_id/name, team_id, position, source(auto-lineup),
                                       data_quality, confidence. Scouting fields are MANUAL -> protected.

NEVER auto-persistible (always blocked): player_xg_xa.csv, referee_profiles.csv,
coach_tactical_profiles.csv (manual / external sources).

Default run is diagnostic (exit 0). With --strict the process exits 1 if it detects an unsafe situation:
a forbidden file in the candidate add-set, a candidate file that still contains MANUAL rows/cells (so a
wholesale `git add` would commit manual data — needs filtering, Fase 4C-4), or a column inconsistency.

Outputs (read-only artifacts):
  * analysis/worldcup/worldcup_external_persistence_guard.txt
  * analysis/worldcup/worldcup_external_persistence_guard.csv

Run:  python analysis/worldcup/guard_worldcup_external_persistence.py [--strict]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402  (reuse COLUMNS/_is_empty)

EXT_DIR = ROOT / "data" / "external"
OUT_TXT = HERE / "worldcup_external_persistence_guard.txt"
OUT_CSV = HERE / "worldcup_external_persistence_guard.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# files that may NEVER be auto-persisted (manual / external) — blocked by policy
FORBIDDEN_FILES = {"player_xg_xa.csv", "referee_profiles.csv", "coach_tactical_profiles.csv"}
_CONF_OK = {"baja", "media", "alta"}
_LINEUP_SOURCES = {"api_football_lineup_position", "api_football_lineup"}

# per-allowed-file policy. manual_cols filled -> the row carries manual data (protected). A row is
# auto-persistible only if it passes `row_is_auto` AND has no manual_cols filled AND required are present.
ALLOWED_POLICY = {
    "fixture_referees.csv": {
        "manual_cols": [],
        "required_nonempty": ["fixture_id", "referee_name"],
        "auto_sources": None,                # no source column
        "extra": None,
    },
    "weather_by_fixture.csv": {
        "manual_cols": ["temperature", "humidity", "wind_speed", "rain_probability", "pitch_condition"],
        "required_nonempty": ["fixture_id"],
        "auto_sources": {"plantilla_kickoff"},
        "extra": None,
    },
    "set_piece_takers.csv": {
        "manual_cols": [],                   # whole-row gate instead (see _set_piece_row_auto)
        "required_nonempty": ["team_id", "player_id"],
        "auto_sources": {"api_football_events"},
        "extra": "set_piece",
    },
    "player_positional_profiles.csv": {
        "manual_cols": ["role", "preferred_zone", "attacking_weight", "defensive_weight",
                        "aerial_threat", "pace_threat", "1v1_threat", "crossing_threat",
                        "card_risk_role"],
        "required_nonempty": ["player_id", "position"],
        "auto_sources": _LINEUP_SOURCES,
        "extra": None,
    },
}


def _empty(v):
    return prep._is_empty(v)


def _is_number(v):
    try:
        float(v)
        return not _empty(v)
    except Exception:
        return False


def _set_piece_row_auto(row) -> bool:
    """A set-piece row is auto-persistible only if it is a REAL penalty derivation."""
    return (str(row.get("source") or "").strip() == "api_football_events"
            and str(row.get("role") or "").strip().lower() == "penalty"
            and str(row.get("data_quality") or "").strip().lower() == "alta"
            and _is_number(row.get("attempts"))
            and not _empty(row.get("last_taken_date"))
            and str(row.get("confidence") or "").strip().lower() in _CONF_OK)


def classify_file(fname, ext_dir=EXT_DIR):
    """Per-file persistence analysis. Returns a dict with auto/manual row counts, manual cell count,
    column-consistency, distinct sources and a per-row classification. NEVER writes."""
    cols = prep.COLUMNS[fname]
    policy = ALLOWED_POLICY[fname]
    path = Path(ext_dir) / fname
    res = {"file": fname, "exists": path.exists(), "rows": 0, "auto_rows": 0, "manual_rows": 0,
           "manual_cells": 0, "columns_ok": True, "sources": [], "reasons": []}
    if not path.exists():
        res["reasons"].append("ausente")
        return res
    try:
        df = pd.read_csv(path)
    except Exception:
        res["columns_ok"] = False
        res["reasons"].append("csv ilegible")
        return res
    # column consistency
    if list(df.columns) != cols:
        res["columns_ok"] = False
        res["reasons"].append(f"columnas != contrato (esperado {len(cols)})")
    res["rows"] = len(df)
    if "source" in df.columns:
        res["sources"] = sorted({str(v).strip() for v in df["source"].dropna() if str(v).strip()})

    manual_cols = [c for c in policy["manual_cols"] if c in df.columns]
    for _, row in df.iterrows():
        # required fields present?
        req_ok = all(not _empty(row.get(c)) for c in policy["required_nonempty"] if c in df.columns)
        # source gate (if the file has one)
        src_ok = True
        if policy["auto_sources"] is not None:
            src_ok = str(row.get("source") or "").strip() in policy["auto_sources"]
        # extra whole-row gate
        extra_ok = True
        if policy["extra"] == "set_piece":
            extra_ok = _set_piece_row_auto(row)
        # manual cells filled on this row
        filled_manual = [c for c in manual_cols if not _empty(row.get(c))]
        res["manual_cells"] += len(filled_manual)
        if req_ok and src_ok and extra_ok and not filled_manual:
            res["auto_rows"] += 1
        else:
            res["manual_rows"] += 1
    return res


def evaluate(ext_dir=EXT_DIR, candidate_files=None):
    """Full guard evaluation. candidate_files = the filenames a (future) CI step would `git add`;
    default = the four allowed files. Returns the report dict (no writes, no commit)."""
    if candidate_files is None:
        candidate_files = list(ALLOWED_POLICY.keys())

    allowed = {f: classify_file(f, ext_dir) for f in ALLOWED_POLICY}
    blocked = []
    for f in sorted(FORBIDDEN_FILES):
        p = Path(ext_dir) / f
        rows = 0
        if p.exists():
            try:
                rows = len(pd.read_csv(p))
            except Exception:
                rows = -1
        blocked.append({"file": f, "rows": rows,
                        "reason": "archivo de relleno manual/externo — NUNCA auto-persistible"})

    # which allowed files actually have auto-persistible content -> addable paths
    addable = [f for f in candidate_files if f in allowed and allowed[f]["auto_rows"] > 0]
    addable_paths = [f"data/external/{f}" for f in addable]   # posix paths (valid git add args)
    would_commit = len(addable) > 0

    # strict violations
    violations = []
    for f in candidate_files:
        if f in FORBIDDEN_FILES:
            violations.append(f"archivo prohibido en el set de commit: {f}")
    for f in addable:
        a = allowed[f]
        if not a["columns_ok"]:
            violations.append(f"{f}: inconsistencia de columnas")
        if a["manual_rows"] > 0 or a["manual_cells"] > 0:
            violations.append(
                f"{f}: contiene datos MANUALES ({a['manual_rows']} filas / {a['manual_cells']} celdas) "
                f"— un git add wholesale los commitearía; requiere filtrado (Fase 4C-4)")
    # also flag column inconsistency on any analyzed allowed file
    for f, a in allowed.items():
        if a["exists"] and not a["columns_ok"] and f not in addable:
            violations.append(f"{f}: inconsistencia de columnas")

    return {
        "allowed": allowed, "blocked": blocked,
        "candidate_files": list(candidate_files),
        "addable_paths": addable_paths, "would_commit": would_commit,
        "auto_persistible_rows": sum(a["auto_rows"] for a in allowed.values()),
        "manual_protected_rows": sum(a["manual_rows"] for a in allowed.values()),
        "manual_protected_cells": sum(a["manual_cells"] for a in allowed.values()),
        "violations": violations, "strict_ok": len(violations) == 0,
    }


# ============================================================ rendering / I/O
def render_txt(rep) -> str:
    L = ["===== WORLD CUP — EXTERNAL-DATA PERSISTENCE GUARD (read-only, no commit) =====", ""]
    L.append("Archivos PERMITIDOS (solo su parte auto-derivada sería persistible):")
    for f, a in rep["allowed"].items():
        if not a["exists"]:
            L.append(f"  {f:34s} AUSENTE")
            continue
        src = ", ".join(a["sources"]) if a["sources"] else "n/a"
        L.append(f"  {f:34s} {a['rows']:>3} filas | auto={a['auto_rows']} "
                 f"manual_protegidas={a['manual_rows']} celdas_manuales={a['manual_cells']}"
                 f"{'' if a['columns_ok'] else ' | ⚠ columnas'}")
        L.append(f"      fuentes: {src}")
    L.append("")
    L.append("Archivos BLOQUEADOS (nunca auto-persistibles):")
    for b in rep["blocked"]:
        L.append(f"  {b['file']:34s} {b['rows']:>3} filas | {b['reason']}")
    L.append("")
    L.append(f"¿Habría commit?: {'SÍ' if rep['would_commit'] else 'NO (nada auto-persistible nuevo)'}")
    L.append(f"Filas auto-persistibles: {rep['auto_persistible_rows']}")
    L.append(f"Filas manuales protegidas: {rep['manual_protected_rows']}")
    L.append(f"Celdas manuales protegidas: {rep['manual_protected_cells']}")
    if rep["addable_paths"]:
        L.append("Rutas que PODRÍAN añadirse a git (solo si se activa opción B + filtrado):")
        for p in rep["addable_paths"]:
            L.append(f"  + {p}")
    else:
        L.append("Rutas que podrían añadirse a git: ninguna")
    L.append("")
    if rep["violations"]:
        L.append("VIOLACIONES (strict -> exit 1):")
        for v in rep["violations"]:
            L.append(f"  ✗ {v}")
    else:
        L.append("Sin violaciones: lo auto-derivado actual sería seguro de persistir wholesale.")
    L.append("")
    L.append("Nota: diagnóstico. NO escribe data/external, NO commitea, NO activa persistencia.")
    return "\n".join(L)


def _csv_rows(rep):
    rows = []
    for f, a in rep["allowed"].items():
        rows.append({"file": f, "policy": "allowed", "exists": int(a["exists"]), "rows": a["rows"],
                     "auto_rows": a["auto_rows"], "manual_rows": a["manual_rows"],
                     "manual_cells": a["manual_cells"], "columns_ok": int(a["columns_ok"]),
                     "addable": int(f"data/external/{f}" in rep["addable_paths"])})
    for b in rep["blocked"]:
        rows.append({"file": b["file"], "policy": "blocked", "exists": int(b["rows"] >= 0),
                     "rows": max(b["rows"], 0), "auto_rows": 0, "manual_rows": 0, "manual_cells": 0,
                     "columns_ok": 1, "addable": 0})
    return rows


def run(ext_dir=EXT_DIR, out_txt=OUT_TXT, out_csv=OUT_CSV, candidate_files=None, write=True):
    rep = evaluate(ext_dir, candidate_files)
    txt = render_txt(rep)
    if write:
        Path(out_txt).write_text(txt + "\n", encoding="utf-8")
        pd.DataFrame(_csv_rows(rep)).to_csv(out_csv, index=False)
    rep["txt"] = txt
    return rep


def main():
    ap = argparse.ArgumentParser(description="World Cup external-data persistence guard (read-only; "
                                             "--strict exits 1 on an unsafe situation).")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if a forbidden file is in the add-set, an addable file still holds "
                         "manual data, or columns are inconsistent. Default: diagnostic (exit 0).")
    a = ap.parse_args()
    rep = run()
    print(rep["txt"])
    if a.strict and not rep["strict_ok"]:
        print(f"\n[strict] {len(rep['violations'])} violación(es) -> exit 1")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
