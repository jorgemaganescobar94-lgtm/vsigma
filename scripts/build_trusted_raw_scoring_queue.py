from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
QUEUE_FIELDS = [
    "target_date", "generated_at", "queue_rank", "fixture_id", "home_team", "away_team", "league",
    "gap_status", "scoring_needed", "priority", "reason", "recommended_fix", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "queue_rows", "priority_counts", "scoring_needed_counts",
    "source_gap_status", "next_action", "auto_apply", "production_change",
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


def queue_priority(row: dict[str, str]) -> str:
    league = up(row.get("league"))
    teams = f"{up(row.get('home_team'))} {up(row.get('away_team'))}"
    if any(token in league or token in teams for token in ["U17", "U19", "U20", "U21", "U23", "RESERVE", "W LEAGUE", "WOMEN"]):
        return "P3_LOW_TRUST_REVIEW_ONLY"
    if any(token in league for token in ["FRIENDLIES", "LANDESLIGA", "4. LIGA", "REGIONALLIGA", "USL LEAGUE TWO"]):
        return "P2_LOW_COVERAGE_SCORING"
    return "P1_TRUSTED_MISSING_SCORING"


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source = processed / "today" / day / "vsigma_scoring_gap_explainer.csv"
    rows = [row for row in read_rows(source) if up(row.get("gap_status")) == "MISSING_SCORED_ROW"]
    queue: list[dict[str, object]] = []
    for i, row in enumerate(rows, start=1):
        queue.append({
            "target_date": day,
            "generated_at": generated,
            "queue_rank": i,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "gap_status": norm(row.get("gap_status")),
            "scoring_needed": "YES",
            "priority": queue_priority(row),
            "reason": "trusted raw candidate has no matching scored row",
            "recommended_fix": norm(row.get("recommended_fix")) or "Run/repair scoring enrichment over trusted raw fixture candidates before market translation.",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "queue_rows": len(queue),
        "priority_counts": counts(queue, "priority"),
        "scoring_needed_counts": counts(queue, "scoring_needed"),
        "source_gap_status": "MISSING_SCORED_ROW",
        "next_action": "Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return queue, summary, md(day, queue, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, queue: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Trusted Raw Scoring Queue - {day}",
        "",
        "## Summary",
        f"- queue_rows: {summary['queue_rows']}",
        f"- priority_counts: {summary['priority_counts']}",
        f"- scoring_needed_counts: {summary['scoring_needed_counts']}",
        f"- source_gap_status: {summary['source_gap_status']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Queue Rows",
    ]
    if not queue:
        lines.append("- none. No trusted raw candidate is missing a scored row.")
    for row in queue:
        lines.append(f"- #{row['queue_rank']} | {row['priority']} | {row['home_team']} vs {row['away_team']} | league={row['league']} | scoring_needed={row['scoring_needed']} | reason={row['reason']}")
    lines += [
        "",
        "## Guardrails",
        "- This queue is diagnostic/planning only.",
        "- It does not call APIs, create picks, create stake permission, or bypass gates.",
        "- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    queue, summary, markdown = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_trusted_raw_scoring_queue.csv", queue, QUEUE_FIELDS)
        write_csv(base / "vsigma_trusted_raw_scoring_queue_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_trusted_raw_scoring_queue.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA TRUSTED RAW SCORING QUEUE ===")
    print(f"queue_rows={summary[0]['queue_rows']}")
    print(f"priority_counts={summary[0]['priority_counts']}")
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
