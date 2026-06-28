"""
WORLD CUP 2026 — EXTERNAL-CONTEXT AUDIT (Fase 4C-2). READ-ONLY · NO API · NO scraping · NO betting ·
does NOT modify the store or the CSVs · does NOT spend any quota.

Two coverage reports, both purely diagnostic:

  1) STORE coverage — reads data/processed/worldcup/api_enrichment/<fid>.json and reports, per fixture,
     whether the isolated World Cup store carries the Fase 4C-1 `fixture` block (referee / venue name /
     venue city / date) and the post-FT sections (events / players / lineups). Flags old stores that
     are compatible but incomplete (no `fixture` block yet).

  2) EXTERNAL-CSV coverage — reads data/external/*.csv and reports, per contract, total rows, how many
     are auto-derived vs manual (by `source`), which columns are completed vs pending, the distinct
     sources seen, and whether the file holds REAL data or is still an empty template.

Outputs (read-only artifacts; the workflow may print them, it does NOT commit data/external from here):
  * analysis/worldcup/worldcup_store_external_context_audit.txt   (human-readable, both reports)
  * analysis/worldcup/worldcup_store_external_context_audit.csv   (per-fixture store coverage table)

Run:  python analysis/worldcup/audit_worldcup_store_external_context.py
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import prepare_worldcup_external_templates as prep  # noqa: E402  (reuse COLUMNS/AUTO_SOURCES/_is_empty)

STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "api_enrichment"
EXT_DIR = ROOT / "data" / "external"
OUT_TXT = HERE / "worldcup_store_external_context_audit.txt"
OUT_CSV = HERE / "worldcup_store_external_context_audit.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ store audit (pure)
def audit_store(store_records) -> dict:
    """Per-fixture store coverage from a list of store dicts. Returns {rows:[...], totals:{...}}.
    NEVER fetches or mutates — it only inspects what is already on disk."""
    rows = []
    for s in store_records or []:
        s = s or {}
        fx = s.get("fixture") or {}
        venue = fx.get("venue") or {}
        pf = s.get("postft") or {}
        has_block = bool(fx)
        row = {
            "fixture_id": s.get("fixture_id"),
            "has_fixture_block": int(has_block),
            "has_referee": int(bool(fx.get("referee"))),
            "has_venue_name": int(bool(venue.get("name"))),
            "has_venue_city": int(bool(venue.get("city"))),
            "has_date": int(bool(fx.get("date"))),
            "has_events": int(bool(pf.get("events"))),
            "has_players": int(bool(pf.get("players"))),
            "has_lineups": int(bool(pf.get("lineups"))),
            # "old but compatible": has post-FT data yet no fixture block (pre-4C-1 store)
            "incomplete_old": int(bool(pf.get("summary") or pf.get("events")) and not has_block),
        }
        rows.append(row)
    keys = ["has_fixture_block", "has_referee", "has_venue_name", "has_venue_city", "has_date",
            "has_events", "has_players", "has_lineups", "incomplete_old"]
    totals = {"fixtures_total": len(rows)}
    for k in keys:
        totals[k] = sum(r[k] for r in rows)
    return {"rows": rows, "totals": totals}


# ============================================================ external-CSV audit (pure)
def _classify_source(val) -> str:
    if prep._is_empty(val):
        return "blank"
    return "auto" if str(val).strip() in prep.AUTO_SOURCES else "manual"


def audit_external_csvs(ext_dir=EXT_DIR) -> dict:
    """Per-contract coverage of data/external/*.csv. For each file: rows, auto/manual/blank-source
    counts, completed vs pending columns, distinct sources, and real-data-vs-empty-template. Files
    without a `source` column (e.g. fixture_referees.csv) report source classification as n/a."""
    ext_dir = Path(ext_dir)
    out = {}
    for fname, cols in prep.COLUMNS.items():
        path = ext_dir / fname
        rec = {"exists": path.exists(), "rows": 0, "auto_rows": 0, "manual_rows": 0,
               "blank_source_rows": 0, "has_source_col": False, "completed_columns": [],
               "pending_columns": list(cols), "sources": [], "has_real_data": False}
        if path.exists():
            try:
                df = pd.read_csv(path)
            except Exception:
                df = pd.DataFrame(columns=cols)
            rec["rows"] = len(df)
            rec["has_source_col"] = "source" in df.columns
            if len(df):
                rec["completed_columns"] = [c for c in cols if c in df.columns
                                            and not df[c].isna().all()
                                            and not df[c].astype(str).str.strip()
                                            .replace("nan", "").eq("").all()]
                rec["pending_columns"] = [c for c in cols if c not in rec["completed_columns"]]
                rec["has_real_data"] = len(rec["completed_columns"]) > 0
                if rec["has_source_col"]:
                    classes = df["source"].apply(_classify_source)
                    rec["auto_rows"] = int((classes == "auto").sum())
                    rec["manual_rows"] = int((classes == "manual").sum())
                    rec["blank_source_rows"] = int((classes == "blank").sum())
                    rec["sources"] = sorted({str(v).strip() for v in df["source"].dropna()
                                             if str(v).strip()})
        out[fname] = rec
    return out


# ============================================================ rendering / I/O
def _bar(label, n, total):
    return f"  {label:18s} {n:>3}/{total:<3}"


def render_txt(store_audit, csv_audit) -> str:
    t = store_audit["totals"]
    L = ["===== WORLD CUP — STORE EXTERNAL-CONTEXT AUDIT (read-only, no API) =====", ""]
    L.append(f"Fixtures en store: {t['fixtures_total']}")
    if t["fixtures_total"]:
        for k, lab in (("has_fixture_block", "bloque fixture"), ("has_referee", "referee"),
                       ("has_venue_name", "venue.name"), ("has_venue_city", "venue.city"),
                       ("has_date", "fixture.date"), ("has_events", "postft.events"),
                       ("has_players", "postft.players"), ("has_lineups", "postft.lineups"),
                       ("incomplete_old", "antiguos sin bloque")):
            L.append(_bar(lab, t[k], t["fixtures_total"]))
    L.append("")
    L.append("===== EXTERNAL CSVs (data/external/) =====")
    for fname, r in csv_audit.items():
        if not r["exists"]:
            L.append(f"  {fname:34s} AUSENTE")
            continue
        kind = "DATOS REALES" if r["has_real_data"] else "plantilla vacía"
        src = (", ".join(r["sources"]) if r["sources"] else
               ("n/a (sin columna source)" if not r["has_source_col"] else "—"))
        L.append(f"  {fname:34s} {r['rows']:>3} filas | {kind}")
        L.append(f"      auto={r['auto_rows']} manual={r['manual_rows']} blank={r['blank_source_rows']}"
                 f" | fuentes: {src}")
        if r["pending_columns"]:
            shown = ", ".join(r["pending_columns"][:8]) + ("…" if len(r["pending_columns"]) > 8 else "")
            L.append(f"      pendientes: {shown}")
    L.append("")
    L.append("Nota: auditoría puramente diagnóstica. No llama API, no modifica el store ni los CSV.")
    return "\n".join(L)


def run(store_dir=STORE_DIR, ext_dir=EXT_DIR, out_txt=OUT_TXT, out_csv=OUT_CSV, write=True):
    store_records = []
    for fp in sorted(glob.glob(str(Path(store_dir) / "*.json"))):
        try:
            store_records.append(json.load(open(fp, encoding="utf-8")))
        except Exception:
            continue
    store_audit = audit_store(store_records)
    csv_audit = audit_external_csvs(ext_dir)
    txt = render_txt(store_audit, csv_audit)
    if write:
        Path(out_txt).write_text(txt + "\n", encoding="utf-8")
        pd.DataFrame(store_audit["rows"]).to_csv(out_csv, index=False)
    return {"store": store_audit, "csv": csv_audit, "txt": txt}


def main():
    res = run()
    print(res["txt"])
    return res


if __name__ == "__main__":
    main()
