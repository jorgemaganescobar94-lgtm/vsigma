from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUTPUT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "fixture_datetime_utc", "source_path", "source_status", "discovery_reason", "auto_apply", "production_change",
]
DIAG_FIELDS = [
    "target_date", "generated_at", "source_path", "rows", "same_day_rows", "accepted_rows",
    "rejected_rows", "status", "detail", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "overall_status", "files_scanned", "accepted_rows",
    "rejected_rows", "next_action", "auto_apply", "production_change",
]
EXCLUDE_HINTS = {
    "diagnostic", "summary", "ledger", "panel", "governor", "report", "health", "snapshot", "coverage_matrix",
}

def norm(v: object) -> str:
    return "" if v is None else str(v).strip()

def up(v: object) -> str:
    return norm(v).upper()

def read_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except Exception:
        return []

def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])

def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date", "fixture_datetime_utc", "generated_at"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""

def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [row for row in rows if row_day(row) == day]

def blocked(row: dict[str, str]) -> bool:
    text = " ".join(up(v) for v in row.values())
    return any(token in text for token in ["NO_DATA_BLOCKED", "NO_BET", "NO_STAKE", "BLOCKED", "LOW_COVERAGE_NO_BET"])

def identity(row: dict[str, str]) -> bool:
    return bool(norm(row.get("fixture_id")) and norm(row.get("home_team")) and norm(row.get("away_team")))

def discover_files(root: Path) -> list[Path]:
    bases = [root / "data" / "raw", root / "data" / "processed"]
    files: list[Path] = []
    for base in bases:
        if not base.exists():
            continue
        for path in base.rglob("*.csv"):
            low = path.name.lower()
            if any(hint in low for hint in EXCLUDE_HINTS):
                continue
            if any(token in low for token in ["fixture", "fixtures", "match", "matches", "candidate", "league_filtered", "scored"]):
                files.append(path)
    return sorted(set(files))

def candidate(row: dict[str, str], day: str, generated: str, source: Path) -> dict[str, object]:
    return {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": norm(row.get("fixture_id")).replace(".0", ""),
        "league": norm(row.get("league")),
        "country": norm(row.get("country")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "fixture_datetime_utc": norm(row.get("fixture_datetime_utc")),
        "source_path": str(source),
        "source_status": "LOCAL_RAW_DISCOVERY",
        "discovery_reason": "existing local row has fixture identity and is not blocked",
        "auto_apply": "NO",
        "production_change": "NO",
    }

def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, accepted: list[dict[str, object]], diagnostics: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Local Raw Fixture Discovery - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- files_scanned: {summary['files_scanned']}",
        f"- accepted_rows: {summary['accepted_rows']}",
        f"- rejected_rows: {summary['rejected_rows']}",
        f"- source_status_counts: {counts(diagnostics, 'status')}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Accepted Rows",
    ]
    if not accepted:
        lines.append("- none. No local raw source row passed identity/block gates.")
    for row in accepted:
        lines.append(f"- {row['home_team']} vs {row['away_team']} | fixture_id={row['fixture_id']} | league={row['league']} | source={row['source_path']}")
    lines += ["", "## Source Diagnostics"]
    for row in diagnostics[:80]:
        lines.append(f"- {row['source_path']} | status={row['status']} | rows={row['rows']} | same_day={row['same_day_rows']} | accepted={row['accepted_rows']} | rejected={row['rejected_rows']} | detail={row['detail']}")
    lines += [
        "",
        "## Guardrails",
        "- Local discovery does not call APIs, touch secrets, increase spend, create picks or bypass No Bet.",
        "- Blocked rows and NO_DATA_BLOCKED rows are refused.",
        "- Accepted rows are only raw candidates for normal scoring/safety gates.",
    ]
    return "\n".join(lines) + "\n"

def build(day: str, tz: str, root: Path, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    accepted: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    seen: set[str] = set()
    rejected_total = 0
    files = discover_files(root)

    for path in files:
        rows = read_rows(path)
        same = same_day(rows, day)
        accepted_count = 0
        rejected_count = 0

        for row in same:
            if not identity(row) or blocked(row):
                rejected_count += 1
                rejected_total += 1
                continue
            fid = norm(row.get("fixture_id")).replace(".0", "")
            if fid in seen:
                continue
            seen.add(fid)
            accepted.append(candidate(row, day, generated, path))
            accepted_count += 1

        if not rows:
            status = "EMPTY_OR_UNREADABLE"
            detail = "file has no readable CSV rows"
        elif not same:
            status = "NO_SAME_DAY_ROWS"
            detail = "file has no target-date rows"
        elif accepted_count == 0:
            status = "NO_ACCEPTED_ROWS"
            detail = "target-date rows exist but are blocked or missing identity"
        else:
            status = "HAS_ACCEPTED_ROWS"
            detail = "local source contains accepted raw fixture rows"

        diagnostics.append({
            "target_date": day,
            "generated_at": generated,
            "source_path": str(path),
            "rows": len(rows),
            "same_day_rows": len(same),
            "accepted_rows": accepted_count,
            "rejected_rows": rejected_count,
            "status": status,
            "detail": detail,
            "auto_apply": "NO",
            "production_change": "NO",
        })

    overall = "LOCAL_RAW_CANDIDATES_FOUND" if accepted else "NO_LOCAL_RAW_CANDIDATES_FOUND"
    next_action = "Review accepted rows, then feed normal scoring gates." if accepted else "No local source can build raw candidates; upstream fetch/filter producer is still required."
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "overall_status": overall,
        "files_scanned": len(files),
        "accepted_rows": len(accepted),
        "rejected_rows": rejected_total,
        "next_action": next_action,
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return accepted, diagnostics, summary, markdown(day, accepted, diagnostics, summary[0])

def run(day: str, tz: str, root: Path, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    accepted, diagnostics, summary, md = build(day, tz, root, processed)

    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_local_raw_fixture_discovery_candidates.csv", accepted, OUTPUT_FIELDS)
        write_csv(base / "vsigma_local_raw_fixture_discovery_diagnostic.csv", diagnostics, DIAG_FIELDS)
        write_csv(base / "vsigma_local_raw_fixture_discovery_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_local_raw_fixture_discovery.md").write_text(md, encoding="utf-8")

    print("=== VSIGMA LOCAL RAW FIXTURE DISCOVERY ===")
    print(f"overall_status={summary[0]['overall_status']}")
    print(f"files_scanned={summary[0]['files_scanned']}")
    print(f"accepted_rows={summary[0]['accepted_rows']}")
    print("auto_apply=NO")
    print("production_change=NO")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    run(args.date, args.timezone, args.root, args.processed_dir)

if __name__ == "__main__":
    main()
