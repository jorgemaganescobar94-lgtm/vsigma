from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
RAW = Path("data/raw")
INPUT_NAMES = [
    "probable_lineup_sources.csv",
    "probable_lineup_sources_manual.csv",
    "probable_lineup_sources_autonomous.csv",
    "vsigma_probable_lineup_sources_manual.csv",
    "vsigma_probable_lineup_sources_autonomous.csv",
]
OUT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "team_side", "source_name", "source_url", "probable_xi", "input_file", "import_status",
    "import_reason", "auto_apply", "production_change",
]
TEMPLATE_FIELDS = [
    "target_date", "fixture_id", "league", "country", "home_team", "away_team",
    "team_side", "source_name", "source_url", "probable_xi", "notes",
]
REPORT_FIELDS = [
    "target_date", "generated_at", "rows_seen", "rows_imported", "rows_rejected",
    "input_files", "import_status_counts", "sources_seen", "template_rows", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


def read(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day, name):
    return P / "today" / day / name


def fixture_rows(day):
    for name in ["matches_vsigma_scored_v3.csv", "vsigma_daily_execution_board.csv", "matches_league_filtered.csv"]:
        rows = read(d(day, name))
        if rows:
            return rows, name
    return [], "NONE"


def registry_sources(day):
    rows = read(d(day, "vsigma_probable_lineup_source_registry.csv")) or read(P / "governance" / "vsigma_probable_lineup_source_registry.csv")
    return [s(r.get("source_name")) for r in rows if s(r.get("source_name")) and s(r.get("enabled")).upper() == "YES"]


def input_rows(day):
    out = []
    used = []
    for name in INPUT_NAMES:
        for path in [d(day, name), P / "governance" / name, RAW / name]:
            rows = read(path)
            if rows:
                for r in rows:
                    rr = dict(r)
                    rr["_input_file"] = str(path)
                    out.append(rr)
                used.append(str(path))
    return out, used


def norm_side(x):
    v = s(x).lower()
    if v in {"home", "h", "local", "1"}:
        return "home"
    if v in {"away", "a", "visitante", "2"}:
        return "away"
    return ""


def norm_source(x):
    return s(x).lower().replace(" ", "_")


def fixture_map(fixtures):
    return {s(r.get("fixture_id")): r for r in fixtures if s(r.get("fixture_id"))}


def import_row(row, fixtures_by, day, generated):
    fixture_id = s(row.get("fixture_id"))
    fx = fixtures_by.get(fixture_id, {})
    side = norm_side(row.get("team_side") or row.get("side") or row.get("team"))
    source = norm_source(row.get("source_name") or row.get("source") or row.get("provider"))
    xi = s(row.get("probable_xi") or row.get("players") or row.get("xi"))
    status = "IMPORTED"
    reason = "OK"
    if not fixture_id or fixture_id not in fixtures_by:
        status, reason = "REJECTED", "fixture_id_not_in_daily_fixtures"
    elif side not in {"home", "away"}:
        status, reason = "REJECTED", "team_side_missing_or_invalid"
    elif not source:
        status, reason = "REJECTED", "source_name_missing"
    elif not xi:
        status, reason = "REJECTED", "probable_xi_empty"
    return {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": fixture_id,
        "league": s(fx.get("league")) or s(row.get("league")),
        "country": s(fx.get("country")) or s(row.get("country")),
        "home_team": s(fx.get("home_team")) or s(row.get("home_team")),
        "away_team": s(fx.get("away_team")) or s(row.get("away_team")),
        "team_side": side,
        "source_name": source,
        "source_url": s(row.get("source_url") or row.get("url")),
        "probable_xi": xi,
        "input_file": s(row.get("_input_file")),
        "import_status": status,
        "import_reason": reason,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build_template(day, fixtures, sources):
    active_sources = [x for x in sources if x] or ["sportsmole", "whoscored", "rotowire"]
    rows = []
    for fx in fixtures:
        for side in ["home", "away"]:
            for source in active_sources[:5]:
                rows.append({
                    "target_date": day,
                    "fixture_id": s(fx.get("fixture_id")),
                    "league": s(fx.get("league")),
                    "country": s(fx.get("country")),
                    "home_team": s(fx.get("home_team")),
                    "away_team": s(fx.get("away_team")),
                    "team_side": side,
                    "source_name": source,
                    "source_url": "",
                    "probable_xi": "",
                    "notes": "Fill probable_xi as semicolon-separated 11 players. Leave blank if unavailable.",
                })
    return rows


def md(day, report, imported_rows):
    lines = [
        f"# vSIGMA Probable Lineup Source Import - {day}",
        "",
        "## Summary",
    ]
    if report:
        r = report[0]
        lines += [
            f"- rows_seen: {r['rows_seen']}",
            f"- rows_imported: {r['rows_imported']}",
            f"- rows_rejected: {r['rows_rejected']}",
            f"- input_files: {r['input_files']}",
            f"- import_status_counts: {r['import_status_counts']}",
            f"- sources_seen: {r['sources_seen']}",
            f"- template_rows: {r['template_rows']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Imported Rows"]
    if not imported_rows:
        lines.append("- none. Fill probable_lineup_sources_manual.csv or template rows to feed consensus.")
    for r in imported_rows[:50]:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | side={r['team_side']} | source={r['source_name']} | status={r['import_status']} | reason={r['import_reason']}")
    lines += [
        "",
        "## Guardrails",
        "- Importer never scrapes and never fabricates probable XIs.",
        "- Imported rows still pass through registry-weighted consensus validation.",
        "- Probable XI never equals official lineup.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    fixtures, fixture_source = fixture_rows(day)
    fx_by = fixture_map(fixtures)
    sources = registry_sources(day)
    raw_rows, input_files = input_rows(day)
    normalized = [import_row(r, fx_by, day, generated) for r in raw_rows]
    imported = [r for r in normalized if r["import_status"] == "IMPORTED"]
    rejected = [r for r in normalized if r["import_status"] != "IMPORTED"]
    template = build_template(day, fixtures, sources)
    status_counts = Counter(r["import_status"] for r in normalized)
    source_counts = Counter(r["source_name"] for r in normalized if r.get("source_name"))
    report = [{
        "target_date": day,
        "generated_at": generated,
        "rows_seen": len(normalized),
        "rows_imported": len(imported),
        "rows_rejected": len(rejected),
        "input_files": ";".join(input_files) if input_files else "none",
        "import_status_counts": "; ".join(f"{k}={v}" for k, v in status_counts.items()) if status_counts else "none",
        "sources_seen": "; ".join(f"{k}={v}" for k, v in source_counts.items()) if source_counts else "none",
        "template_rows": len(template),
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_probable_lineup_sources.csv", imported, OUT_FIELDS)
        write(base / "vsigma_probable_lineup_source_import_report.csv", report, REPORT_FIELDS)
        write(base / "vsigma_probable_lineup_source_import_template.csv", template, TEMPLATE_FIELDS)
        (base / "vsigma_probable_lineup_source_import_report.md").write_text(md(day, report, normalized), encoding="utf-8")
    print("=== VSIGMA PROBABLE LINEUP SOURCE IMPORT ===")
    print(f"fixture_source={fixture_source}")
    print(f"rows_seen={len(normalized)}")
    print(f"rows_imported={len(imported)}")
    print(f"rows_rejected={len(rejected)}")
    print("auto_apply=NO")
    print("production_change=NO")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
