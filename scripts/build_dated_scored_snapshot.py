from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
ROOT_SCORED = PROCESSED / "matches_vsigma_scored_v3.csv"
SUMMARY_FIELDS = [
    "target_date", "generated_at", "source_path", "output_path", "source_rows", "same_day_rows",
    "rows_written", "no_data_blocked_rows", "non_blocked_rows", "snapshot_status",
    "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
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


def is_no_data_blocked(row: dict[str, str]) -> bool:
    return "NO_DATA_BLOCKED" in " ".join(up(value) for value in row.values())


def counts(rows: list[dict[str, str]], field: str) -> str:
    if not rows or field not in rows[0]:
        return "none"
    counter = Counter(norm(row.get(field)) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def build(day: str, tz: str, processed: Path, source_path: Path | None = None) -> tuple[list[dict[str, str]], dict[str, object], str, list[str]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source = source_path or processed / "matches_vsigma_scored_v3.csv"
    output = processed / "today" / day / "matches_vsigma_scored_v3.csv"
    fields, rows = read_rows(source)
    same = [row for row in rows if row_day(row) == day]
    no_data = sum(1 for row in same if is_no_data_blocked(row))
    non_blocked = len(same) - no_data

    if not source.exists():
        status = "SOURCE_MISSING"
        next_action = "Run or repair root scoring producer before snapshot."
    elif not same:
        status = "NO_SAME_DAY_ROWS"
        next_action = "Repair scoring date coverage; no dated snapshot rows can be written."
    elif non_blocked == 0:
        status = "SNAPSHOT_DIAGNOSTIC_ONLY_ALL_NO_DATA_BLOCKED"
        next_action = "Snapshot written for coverage diagnostics only; do not create picks. Repair enrichment/coverage."
    else:
        status = "SNAPSHOT_WRITTEN_WITH_REAL_ROWS"
        next_action = "Rerun coverage matrix and selector chain; downstream gates still required."

    if fields:
        write_rows(output, fields, same)

    summary = {
        "target_date": day,
        "generated_at": generated,
        "source_path": str(source),
        "output_path": str(output),
        "source_rows": len(rows),
        "same_day_rows": len(same),
        "rows_written": len(same) if fields else 0,
        "no_data_blocked_rows": no_data,
        "non_blocked_rows": non_blocked,
        "snapshot_status": status,
        "next_action": next_action,
        "auto_apply": "NO",
        "production_change": "NO",
    }
    return same, summary, md(day, same, summary), fields


def md(day: str, rows: list[dict[str, str]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Dated Scored Snapshot - {day}",
        "",
        "## Summary",
        f"- snapshot_status: {summary['snapshot_status']}",
        f"- source_rows: {summary['source_rows']}",
        f"- same_day_rows: {summary['same_day_rows']}",
        f"- rows_written: {summary['rows_written']}",
        f"- no_data_blocked_rows: {summary['no_data_blocked_rows']}",
        f"- non_blocked_rows: {summary['non_blocked_rows']}",
        f"- source_path: {summary['source_path']}",
        f"- output_path: {summary['output_path']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Snapshot Rows",
    ]
    if not rows:
        lines.append("- none. No same-day scored rows available.")
    for row in rows:
        lines.append(
            f"- {row.get('home_team')} vs {row.get('away_team')} | fixture_id={row.get('fixture_id')} | league={row.get('league')} | priority={row.get('vsigma_priority')} | market_hint={row.get('market_family_hint')} | data_warning={row.get('data_warning')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Snapshot creation does not create picks, stake permission, or live permission.",
        "- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.",
        "- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path, source_path: Path | None = None) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown, fields = build(day, tz, processed, source_path)
    for base in [processed / "today" / day, processed / "governance"]:
        write_rows(base / "vsigma_dated_scored_snapshot_summary.csv", SUMMARY_FIELDS, [summary])
        (base / "vsigma_dated_scored_snapshot.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA DATED SCORED SNAPSHOT ===")
    print(f"snapshot_status={summary['snapshot_status']}")
    print(f"rows_written={summary['rows_written']}")
    print(f"no_data_blocked_rows={summary['no_data_blocked_rows']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    parser.add_argument("--source-path", type=Path, default=None)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir, args.source_path)


if __name__ == "__main__":
    main()
