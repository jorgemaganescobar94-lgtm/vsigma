from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

ROW_FIELDS = [
    "target_date", "generated_at", "check_name", "path", "exists", "rows", "same_day_rows",
    "unique_same_day_fixtures", "status", "detail", "recommended_fix", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "overall_status", "root_cause", "root_scored_rows",
    "dated_scored_rows", "dated_candidate_sources_found", "coverage_matrix_rows", "recommended_fix",
    "auto_apply", "production_change",
]
CHECKS = [
    ("root_scored_matches", "data/processed/matches_vsigma_scored_v3.csv", "root scored source"),
    ("dated_scored_matches", "data/processed/today/{day}/matches_vsigma_scored_v3.csv", "dated scored snapshot"),
    ("dated_top_candidates", "data/processed/today/{day}/vsigma_top_candidates_v3.csv", "dated candidate source"),
    ("dated_league_filtered", "data/processed/today/{day}/matches_league_filtered.csv", "dated candidate source"),
    ("fixture_api_coverage_matrix", "data/processed/today/{day}/vsigma_fixture_api_coverage_matrix.csv", "coverage matrix output"),
    ("real_source_expander", "data/processed/today/{day}/vsigma_real_source_coverage_expander_summary.csv", "coverage diagnosis"),
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def unique_fixtures(rows: list[dict[str, str]]) -> set[str]:
    return {fixture_id(row) for row in rows if fixture_id(row)}


def is_no_data_blocked(row: dict[str, str]) -> bool:
    return "NO_DATA_BLOCKED" in " ".join(up(v) for v in row.values())


def check_status(name: str, exists: bool, rows: list[dict[str, str]], same: list[dict[str, str]]) -> tuple[str, str, str]:
    if not exists:
        if name in {"dated_scored_matches", "dated_top_candidates", "dated_league_filtered"}:
            return "MISSING_DATED_SOURCE", "Dated input source is missing.", "Create/copy dated scored or candidate snapshot before coverage matrix."
        return "MISSING", "File is missing.", "Create source in upstream workflow."
    if not rows:
        return "EMPTY", "File exists but has no data rows.", "Repair producer or upstream source."
    if not same:
        return "NO_SAME_DAY_ROWS", "File has rows but none for target date.", "Refresh date filter or regenerate dated snapshot."
    if name == "root_scored_matches" and all(is_no_data_blocked(row) for row in same):
        return "ONLY_NO_DATA_BLOCKED", "Root scored rows exist but all same-day rows are NO_DATA_BLOCKED.", "Repair scoring enrichment/coverage, not market selection."
    return "OK", "Same-day rows available.", "No repair needed for this file."


def build(day: str, tz: str) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows_out: list[dict[str, object]] = []
    metrics = {
        "root_scored_rows": 0,
        "dated_scored_rows": 0,
        "dated_candidate_sources_found": 0,
        "coverage_matrix_rows": 0,
    }

    for name, template, _desc in CHECKS:
        path = Path(template.format(day=day))
        exists = path.exists()
        rows = read_rows(path)
        same = same_day(rows, day)
        status, detail, fix = check_status(name, exists, rows, same)
        if name == "root_scored_matches":
            metrics["root_scored_rows"] = len(same)
        if name == "dated_scored_matches":
            metrics["dated_scored_rows"] = len(same)
        if name in {"dated_scored_matches", "dated_top_candidates", "dated_league_filtered"} and len(same) > 0:
            metrics["dated_candidate_sources_found"] += 1
        if name == "fixture_api_coverage_matrix":
            metrics["coverage_matrix_rows"] = len(same)
        rows_out.append(
            {
                "target_date": day,
                "generated_at": generated,
                "check_name": name,
                "path": str(path),
                "exists": str(exists).lower(),
                "rows": len(rows),
                "same_day_rows": len(same),
                "unique_same_day_fixtures": len(unique_fixtures(same)),
                "status": status,
                "detail": detail,
                "recommended_fix": fix,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )

    overall, root_cause, fix = decide(metrics)
    summary = [
        {
            "target_date": day,
            "generated_at": generated,
            "overall_status": overall,
            "root_cause": root_cause,
            "root_scored_rows": metrics["root_scored_rows"],
            "dated_scored_rows": metrics["dated_scored_rows"],
            "dated_candidate_sources_found": metrics["dated_candidate_sources_found"],
            "coverage_matrix_rows": metrics["coverage_matrix_rows"],
            "recommended_fix": fix,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    ]
    return rows_out, summary, md(day, rows_out, summary[0])


def decide(metrics: dict[str, int]) -> tuple[str, str, str]:
    if metrics["dated_candidate_sources_found"] == 0:
        return (
            "MISSING_DATED_SCORING_SNAPSHOT",
            "coverage/scoring stage has no dated source for fixture matrix",
            "Create dated snapshot data/processed/today/<date>/matches_vsigma_scored_v3.csv from scored root or repair fetch/scoring producer."
        )
    if metrics["root_scored_rows"] <= 1:
        return (
            "ROOT_SCORING_FEED_TOO_NARROW",
            "root scored feed has one or fewer same-day rows",
            "Repair fixture fetch/scoring coverage before selector/model evaluation."
        )
    if metrics["coverage_matrix_rows"] == 0:
        return (
            "COVERAGE_MATRIX_EMPTY_DESPITE_INPUTS",
            "dated sources exist but coverage matrix is empty",
            "Inspect build_fixture_api_coverage_matrix_v3 source_rows/date parsing."
        )
    return "SCORING_COVERAGE_OK", "dated scoring/candidate sources exist", "Use downstream gates."


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Fixture / Scoring Coverage Repair Diagnostic - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- root_cause: {summary['root_cause']}",
        f"- root_scored_rows: {summary['root_scored_rows']}",
        f"- dated_scored_rows: {summary['dated_scored_rows']}",
        f"- dated_candidate_sources_found: {summary['dated_candidate_sources_found']}",
        f"- coverage_matrix_rows: {summary['coverage_matrix_rows']}",
        f"- recommended_fix: {summary['recommended_fix']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Checks",
    ]
    for row in rows:
        lines.append(
            f"- {row['check_name']} | status={row['status']} | rows={row['rows']} | same_day={row['same_day_rows']} | unique_same_day={row['unique_same_day_fixtures']} | path={row['path']} | fix={row['recommended_fix']}"
        )
    lines += [
        "",
        "## Repair Notes",
        "- build_fixture_api_coverage_matrix_v3 currently reads dated sources only: matches_vsigma_scored_v3.csv, vsigma_top_candidates_v3.csv, or matches_league_filtered.csv under data/processed/today/<date>/.",
        "- Root-level data/processed/matches_vsigma_scored_v3.csv is not enough for the fixture coverage matrix unless copied/snapshotted into the dated folder or the matrix source lookup is expanded.",
        "- This diagnostic does not fetch paid API data, change secrets, execute bets, or bypass No Bet gates.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_fixture_scoring_coverage_repair_diagnostic.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_fixture_scoring_coverage_repair_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_fixture_scoring_coverage_repair_diagnostic.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA FIXTURE / SCORING COVERAGE REPAIR DIAGNOSTIC ===")
    print(f"overall_status={summary[0]['overall_status']}")
    print(f"root_cause={summary[0]['root_cause']}")
    print(f"recommended_fix={summary[0]['recommended_fix']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
