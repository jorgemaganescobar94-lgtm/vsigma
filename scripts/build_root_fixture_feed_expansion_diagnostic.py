from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

CHECKS = [
    ("root_scored_matches", "data/processed/matches_vsigma_scored_v3.csv", "SCORING_ROOT"),
    ("dated_scored_snapshot", "data/processed/today/{day}/matches_vsigma_scored_v3.csv", "SCORING_DATED"),
    ("dated_top_candidates", "data/processed/today/{day}/vsigma_top_candidates_v3.csv", "CANDIDATES_DATED"),
    ("dated_league_filtered", "data/processed/today/{day}/matches_league_filtered.csv", "LEAGUE_FILTERED_DATED"),
    ("fixture_api_coverage_matrix", "data/processed/today/{day}/vsigma_fixture_api_coverage_matrix.csv", "COVERAGE_MATRIX"),
    ("real_selector_summary", "data/processed/today/{day}/vsigma_scored_to_real_shortlist_summary.csv", "REAL_SELECTOR_SUMMARY"),
    ("real_source_expander", "data/processed/today/{day}/vsigma_real_source_coverage_expander_summary.csv", "REAL_SOURCE_SUMMARY"),
    ("fixture_scoring_repair", "data/processed/today/{day}/vsigma_fixture_scoring_coverage_repair_summary.csv", "REPAIR_SUMMARY"),
]

ROW_FIELDS = [
    "target_date", "generated_at", "check_name", "component_type", "path", "exists",
    "total_rows", "same_day_rows", "unique_same_day_fixtures", "date_counts_top",
    "league_counts_top", "country_counts_top", "blocked_rows", "no_data_blocked_rows",
    "diagnostic_status", "detail", "recommended_fix", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "overall_status", "root_cause", "root_scored_same_day_rows",
    "dated_scored_same_day_rows", "coverage_matrix_rows", "raw_candidate_sources_found",
    "recommended_fix", "auto_apply", "production_change",
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


def counts(rows: list[dict[str, str]], field: str, limit: int = 8) -> str:
    if not rows or field not in rows[0]:
        return "none"
    counter = Counter(norm(row.get(field)) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common(limit)) if counter else "none"


def date_counts(rows: list[dict[str, str]], limit: int = 8) -> str:
    counter = Counter(row_day(row) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common(limit)) if counter else "none"


def is_no_data_blocked(row: dict[str, str]) -> bool:
    return "NO_DATA_BLOCKED" in " ".join(up(value) for value in row.values())


def is_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(up(value) for value in row.values())
    return any(token in joined for token in ["NO_DATA_BLOCKED", "NO_BET", "NO_STAKE", "BLOCKED", "LOW_COVERAGE_NO_BET"])


def status(name: str, exists: bool, rows: list[dict[str, str]], same: list[dict[str, str]]) -> tuple[str, str, str]:
    if not exists:
        if name in {"dated_top_candidates", "dated_league_filtered"}:
            return "MISSING_RAW_CANDIDATE_SOURCE", "dated raw/candidate source is missing", "Repair fixture fetch/filter stage before scoring."
        return "MISSING", "file missing", "Create or regenerate this source."
    if not rows:
        return "EMPTY", "file exists but has no rows", "Repair source producer."
    if not same:
        return "NO_SAME_DAY_ROWS", "rows exist but not for target date", "Check date range/timezone filters."
    if name in {"root_scored_matches", "dated_scored_snapshot"} and all(is_no_data_blocked(row) for row in same):
        return "ONLY_NO_DATA_BLOCKED", "same-day scored rows exist but all are no-data blocked", "Expand source coverage and enrich stats/odds/standings before selection."
    if name == "fixture_api_coverage_matrix" and all(is_blocked(row) for row in same):
        return "COVERAGE_BLOCKED", "coverage matrix exists but blocks all rows", "Repair missing stats/odds/lineup/standings coverage."
    return "OK", "same-day rows found", "No immediate repair for this file."


def build(day: str, tz: str) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    report: list[dict[str, object]] = []
    metrics = {
        "root_scored_same_day_rows": 0,
        "dated_scored_same_day_rows": 0,
        "coverage_matrix_rows": 0,
        "raw_candidate_sources_found": 0,
    }

    for name, template, component_type in CHECKS:
        path = Path(template.format(day=day))
        exists = path.exists()
        rows = read_rows(path)
        same = same_day(rows, day)
        diag, detail, fix = status(name, exists, rows, same)
        if name == "root_scored_matches":
            metrics["root_scored_same_day_rows"] = len(same)
        if name == "dated_scored_snapshot":
            metrics["dated_scored_same_day_rows"] = len(same)
        if name == "fixture_api_coverage_matrix":
            metrics["coverage_matrix_rows"] = len(same)
        if name in {"dated_top_candidates", "dated_league_filtered"} and same:
            metrics["raw_candidate_sources_found"] += 1
        report.append(
            {
                "target_date": day,
                "generated_at": generated,
                "check_name": name,
                "component_type": component_type,
                "path": str(path),
                "exists": str(exists).lower(),
                "total_rows": len(rows),
                "same_day_rows": len(same),
                "unique_same_day_fixtures": len(unique_fixtures(same)),
                "date_counts_top": date_counts(rows),
                "league_counts_top": counts(rows, "league"),
                "country_counts_top": counts(rows, "country"),
                "blocked_rows": sum(1 for row in same if is_blocked(row)),
                "no_data_blocked_rows": sum(1 for row in same if is_no_data_blocked(row)),
                "diagnostic_status": diag,
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
            "root_scored_same_day_rows": metrics["root_scored_same_day_rows"],
            "dated_scored_same_day_rows": metrics["dated_scored_same_day_rows"],
            "coverage_matrix_rows": metrics["coverage_matrix_rows"],
            "raw_candidate_sources_found": metrics["raw_candidate_sources_found"],
            "recommended_fix": fix,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    ]
    return report, summary, md(day, report, summary[0])


def decide(metrics: dict[str, int]) -> tuple[str, str, str]:
    if metrics["raw_candidate_sources_found"] == 0:
        return "RAW_FIXTURE_SOURCE_MISSING", "no dated raw candidate/filter source exists before scoring", "Repair fixture fetch/filter producer to create matches_league_filtered.csv or vsigma_top_candidates_v3.csv for the date."
    if metrics["root_scored_same_day_rows"] <= 1:
        return "ROOT_FEED_TOO_NARROW", "root scored feed contains one or fewer same-day fixtures", "Inspect fixture fetch limits, league filters and date window before scoring."
    if metrics["coverage_matrix_rows"] > 0:
        return "COVERAGE_VISIBLE_BUT_BLOCKED", "coverage matrix can see fixtures but they are blocked by missing enrichment", "Repair enrichment sources; do not change market logic."
    return "UNKNOWN_FEED_BREAK", "feed break not fully classified", "Inspect raw fixture producer and scoring script manually."


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Root Fixture Feed Expansion Diagnostic - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- root_cause: {summary['root_cause']}",
        f"- root_scored_same_day_rows: {summary['root_scored_same_day_rows']}",
        f"- dated_scored_same_day_rows: {summary['dated_scored_same_day_rows']}",
        f"- coverage_matrix_rows: {summary['coverage_matrix_rows']}",
        f"- raw_candidate_sources_found: {summary['raw_candidate_sources_found']}",
        f"- recommended_fix: {summary['recommended_fix']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Feed Checks",
    ]
    for row in rows:
        lines.append(
            f"- {row['check_name']} | status={row['diagnostic_status']} | type={row['component_type']} | total={row['total_rows']} | same_day={row['same_day_rows']} | unique_same_day={row['unique_same_day_fixtures']} | blocked={row['blocked_rows']} | no_data_blocked={row['no_data_blocked_rows']} | path={row['path']} | fix={row['recommended_fix']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This diagnostic does not call APIs, alter secrets, change spend, execute bets or bypass safety gates.",
        "- It diagnoses source width before scoring; it does not relax scoring or selector floors.",
        "- No Bet remains correct until real scored fixtures pass coverage and selector gates.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_root_fixture_feed_expansion_diagnostic.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_root_fixture_feed_expansion_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_root_fixture_feed_expansion_diagnostic.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA ROOT FIXTURE FEED EXPANSION DIAGNOSTIC ===")
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
