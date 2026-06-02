from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

SOURCES = [
    ("root_scored_matches", "data/processed/matches_vsigma_scored_v3.csv", "SCORING_ROOT", True),
    ("dated_scored_matches", "data/processed/today/{day}/matches_vsigma_scored_v3.csv", "SCORING_DATED", True),
    ("real_shortlist", "data/processed/today/{day}/vsigma_real_today_execution_shortlist.csv", "REAL_SELECTOR", True),
    ("real_bets_only", "data/processed/today/{day}/vsigma_real_today_execution_bets_only.csv", "REAL_SELECTOR", True),
    ("selector_summary", "data/processed/today/{day}/vsigma_scored_to_real_shortlist_summary.csv", "REAL_SELECTOR_SUMMARY", False),
    ("official_lineups", "data/processed/today/{day}/official_lineup_sources.csv", "LINEUP_SNAPSHOT", False),
    ("probable_lineup_consensus", "data/processed/today/{day}/vsigma_probable_lineup_consensus.csv", "LINEUP_PROBABLE", False),
    ("daily_board", "data/processed/today/{day}/vsigma_daily_execution_board.csv", "BOARD", False),
]

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "component",
    "component_type",
    "path",
    "exists",
    "total_rows",
    "same_day_rows",
    "unique_fixtures_total",
    "unique_fixtures_same_day",
    "date_counts_top",
    "league_counts_top",
    "country_counts_top",
    "blocked_rows",
    "no_data_blocked_rows",
    "real_candidate_like_rows",
    "proxy_like_rows",
    "diagnostic_status",
    "detail",
    "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "overall_status",
    "root_cause",
    "max_same_day_fixture_count",
    "root_scored_same_day_rows",
    "dated_scored_same_day_rows",
    "real_shortlist_rows",
    "real_bets_rows",
    "official_lineup_same_day_rows",
    "official_lineup_unique_same_day_fixtures",
    "next_action",
    "auto_apply",
    "production_change",
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
    counter = Counter(norm(row.get(field))[:10] if field in {"date", "target_date", "fixture_datetime_utc", "generated_at"} else norm(row.get(field)) for row in rows)
    counter.pop("", None)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common(limit)) if counter else "none"


def date_counts(rows: list[dict[str, str]], limit: int = 8) -> str:
    counter = Counter(row_day(row) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common(limit)) if counter else "none"


def is_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(up(v) for v in row.values())
    return any(token in joined for token in ["NO_DATA_BLOCKED", "NO_BET", "NO_STAKE", "BLOCKED", "MAX_BLOCK", "HARD_DOWN"])


def is_no_data_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(up(v) for v in row.values())
    return "NO_DATA_BLOCKED" in joined


def is_proxy(row: dict[str, str]) -> bool:
    joined = " ".join(up(row.get(field)) for field in ["bridge_source", "guardrail_status", "candidate_origin", "allowed_downstream_use"])
    return "OBJECTIVE_PROXY" in joined or "BASE_PROXY_FROM_OBJECTIVE_GATE" in joined or "DIAGNOSTIC_ONLY" in joined


def is_real_candidate_like(row: dict[str, str]) -> bool:
    if is_proxy(row) or is_blocked(row):
        return False
    joined = " ".join(up(row.get(field)) for field in ["final_recommendation", "execution_verdict", "adjusted_final_status", "execution_permission", "final_decision"])
    return any(token in joined for token in ["BET", "WATCH", "REVIEW", "LIVE_ONLY", "STAT_WATCH"])


def component_status(exists: bool, rows: list[dict[str, str]], same: list[dict[str, str]], component_type: str) -> tuple[str, str]:
    if not exists:
        return "MISSING", "file not present"
    if not rows:
        return "EMPTY", "file exists but has no rows"
    if not same:
        return "NO_SAME_DAY_ROWS", "file has rows but none for target date"
    if component_type.startswith("SCORING") and all(is_no_data_blocked(row) for row in same):
        return "ONLY_NO_DATA_BLOCKED", "same-day scoring rows exist but all are NO_DATA_BLOCKED"
    if component_type == "LINEUP_SNAPSHOT":
        return "LINEUP_ONLY", "lineup rows exist but are not scored fixture candidates by themselves"
    if component_type == "REAL_SELECTOR" and not any(is_real_candidate_like(row) for row in same):
        return "NO_REAL_CANDIDATES", "selector output has no real actionable candidate rows"
    return "HAS_SAME_DAY_ROWS", "file has same-day rows"


def build(day: str, tz: str) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    report_rows: list[dict[str, object]] = []
    metrics = {
        "max_same_day_fixture_count": 0,
        "root_scored_same_day_rows": 0,
        "dated_scored_same_day_rows": 0,
        "real_shortlist_rows": 0,
        "real_bets_rows": 0,
        "official_lineup_same_day_rows": 0,
        "official_lineup_unique_same_day_fixtures": 0,
    }

    for component, template, component_type, candidate_source in SOURCES:
        path = Path(template.format(day=day))
        exists = path.exists()
        rows = read_rows(path)
        same = same_day(rows, day)
        unique_total = len(unique_fixtures(rows))
        unique_same = len(unique_fixtures(same))
        blocked = sum(1 for row in same if is_blocked(row))
        no_data = sum(1 for row in same if is_no_data_blocked(row))
        real_like = sum(1 for row in same if is_real_candidate_like(row))
        proxy_like = sum(1 for row in same if is_proxy(row))
        status, detail = component_status(exists, rows, same, component_type)

        if candidate_source:
            metrics["max_same_day_fixture_count"] = max(metrics["max_same_day_fixture_count"], unique_same)
        if component == "root_scored_matches":
            metrics["root_scored_same_day_rows"] = len(same)
        if component == "dated_scored_matches":
            metrics["dated_scored_same_day_rows"] = len(same)
        if component == "real_shortlist":
            metrics["real_shortlist_rows"] = real_like
        if component == "real_bets_only":
            metrics["real_bets_rows"] = real_like
        if component == "official_lineups":
            metrics["official_lineup_same_day_rows"] = len(same)
            metrics["official_lineup_unique_same_day_fixtures"] = unique_same

        report_rows.append(
            {
                "target_date": day,
                "generated_at": generated,
                "component": component,
                "component_type": component_type,
                "path": str(path),
                "exists": str(exists).lower(),
                "total_rows": len(rows),
                "same_day_rows": len(same),
                "unique_fixtures_total": unique_total,
                "unique_fixtures_same_day": unique_same,
                "date_counts_top": date_counts(rows),
                "league_counts_top": counts(rows, "league"),
                "country_counts_top": counts(rows, "country"),
                "blocked_rows": blocked,
                "no_data_blocked_rows": no_data,
                "real_candidate_like_rows": real_like,
                "proxy_like_rows": proxy_like,
                "diagnostic_status": status,
                "detail": detail,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )

    overall, root_cause, next_action = decide(metrics)
    summary = [
        {
            "target_date": day,
            "generated_at": generated,
            "overall_status": overall,
            "root_cause": root_cause,
            "max_same_day_fixture_count": metrics["max_same_day_fixture_count"],
            "root_scored_same_day_rows": metrics["root_scored_same_day_rows"],
            "dated_scored_same_day_rows": metrics["dated_scored_same_day_rows"],
            "real_shortlist_rows": metrics["real_shortlist_rows"],
            "real_bets_rows": metrics["real_bets_rows"],
            "official_lineup_same_day_rows": metrics["official_lineup_same_day_rows"],
            "official_lineup_unique_same_day_fixtures": metrics["official_lineup_unique_same_day_fixtures"],
            "next_action": next_action,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    ]
    return report_rows, summary, md(day, report_rows, summary[0])


def decide(metrics: dict[str, int]) -> tuple[str, str, str]:
    if metrics["real_bets_rows"] > 0 or metrics["real_shortlist_rows"] > 0:
        return "REAL_COVERAGE_OK", "real selector produced rows", "Use normal gates; no expansion needed."
    if metrics["root_scored_same_day_rows"] == 0 and metrics["dated_scored_same_day_rows"] == 0:
        return "NO_SCORED_FIXTURE_SOURCE", "no same-day scored rows found", "Run or repair fixture fetch/scoring stage before selection."
    if metrics["root_scored_same_day_rows"] <= 1 and metrics["dated_scored_same_day_rows"] == 0:
        return "SOURCE_FEED_TOO_NARROW", "scored source has only one same-day fixture and no dated scored snapshot", "Expand or repair fixture fetch/scoring coverage for the target date."
    if metrics["official_lineup_unique_same_day_fixtures"] > metrics["max_same_day_fixture_count"]:
        return "LINEUP_COVERAGE_NOT_SCORING_COVERAGE", "lineup snapshots include fixtures that did not reach scored source", "Do not treat lineups as scored candidates; inspect scoring input linkage."
    return "REAL_SOURCE_PRESENT_BUT_ALL_BLOCKED", "same-day scored rows exist but no row passed real selector floors", "Inspect data quality floors and source coverage; keep No Bet."


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Real Source Coverage Expander - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- root_cause: {summary['root_cause']}",
        f"- max_same_day_fixture_count: {summary['max_same_day_fixture_count']}",
        f"- root_scored_same_day_rows: {summary['root_scored_same_day_rows']}",
        f"- dated_scored_same_day_rows: {summary['dated_scored_same_day_rows']}",
        f"- real_shortlist_rows: {summary['real_shortlist_rows']}",
        f"- real_bets_rows: {summary['real_bets_rows']}",
        f"- official_lineup_same_day_rows: {summary['official_lineup_same_day_rows']}",
        f"- official_lineup_unique_same_day_fixtures: {summary['official_lineup_unique_same_day_fixtures']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Source Rows",
    ]
    for row in rows:
        lines.append(
            f"- {row['component']} | status={row['diagnostic_status']} | type={row['component_type']} | total={row['total_rows']} | same_day={row['same_day_rows']} | unique_same_day={row['unique_fixtures_same_day']} | blocked={row['blocked_rows']} | no_data_blocked={row['no_data_blocked_rows']} | real_like={row['real_candidate_like_rows']} | proxy_like={row['proxy_like_rows']} | path={row['path']} | detail={row['detail']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This expander is diagnostic; it does not fetch paid API data or execute bets.",
        "- Lineup snapshots are coverage evidence only, not candidate permission.",
        "- Real candidates must come from scored fixture rows and pass selector floors.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_real_source_coverage_expander.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_real_source_coverage_expander_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_real_source_coverage_expander.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA REAL SOURCE COVERAGE EXPANDER ===")
    print(f"overall_status={summary[0]['overall_status']}")
    print(f"root_cause={summary[0]['root_cause']}")
    print(f"max_same_day_fixture_count={summary[0]['max_same_day_fixture_count']}")
    print(f"real_shortlist_rows={summary[0]['real_shortlist_rows']}")
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
