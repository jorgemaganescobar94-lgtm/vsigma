from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
PLAN_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league",
    "queue_priority", "dry_run_decision", "enrichment_blocks_needed", "standings_needed",
    "odds_needed", "recent_stats_needed", "injuries_needed", "lineups_needed",
    "estimated_call_units", "api_calls_planned", "api_calls_executed", "risk_label",
    "planner_note", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_planned", "dry_run_decision_counts", "risk_label_counts",
    "priority_counts", "total_estimated_call_units", "api_calls_planned", "api_calls_executed",
    "next_action", "auto_apply", "production_change",
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


def blocks_for(row: dict[str, str]) -> tuple[list[str], str, int, str]:
    priority = up(row.get("priority"))
    league = up(row.get("league"))
    blocks = ["recent_stats", "standings", "odds"]
    risk = "MEDIUM"
    units = 3
    note = "Core enrichment needed before scoring: recent stats, standings and odds."

    if "P2_LOW_COVERAGE" in priority:
        risk = "HIGH_LOW_COVERAGE"
        blocks.append("coverage_probe")
        units += 1
        note = "Low-coverage league: dry-run recommends coverage probe before full enrichment."
    else:
        blocks.extend(["injuries_optional", "lineups_prelock_optional"])
        units += 2

    if any(token in league for token in ["FRIENDLIES", "CUP", "PLAY-OFF", "PLAYOFF"]):
        risk = "HIGH_CONTEXT_VOLATILITY" if risk == "MEDIUM" else risk
        if "context_manual_review" not in blocks:
            blocks.append("context_manual_review")
            units += 1
        note += " Context/manual review needed due cup, friendly or playoff environment."

    return blocks, risk, units, note


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    queue_rows = read_rows(processed / "today" / day / "vsigma_trusted_raw_scoring_queue.csv") or read_rows(processed / "governance" / "vsigma_trusted_raw_scoring_queue.csv")
    plan: list[dict[str, object]] = []
    for row in queue_rows:
        blocks, risk, units, note = blocks_for(row)
        plan.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "queue_priority": norm(row.get("priority")),
            "dry_run_decision": "DRY_RUN_ONLY_NO_API_CALLS",
            "enrichment_blocks_needed": "; ".join(blocks),
            "standings_needed": "YES" if "standings" in blocks else "NO",
            "odds_needed": "YES" if "odds" in blocks else "NO",
            "recent_stats_needed": "YES" if "recent_stats" in blocks else "NO",
            "injuries_needed": "OPTIONAL" if "injuries_optional" in blocks else "NO",
            "lineups_needed": "PRELOCK_OPTIONAL" if "lineups_prelock_optional" in blocks else "NO",
            "estimated_call_units": units,
            "api_calls_planned": "NO",
            "api_calls_executed": "NO",
            "risk_label": risk,
            "planner_note": note,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    total_units = sum(int(row.get("estimated_call_units", 0)) for row in plan)
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_planned": len(plan),
        "dry_run_decision_counts": counts(plan, "dry_run_decision"),
        "risk_label_counts": counts(plan, "risk_label"),
        "priority_counts": counts(plan, "queue_priority"),
        "total_estimated_call_units": total_units,
        "api_calls_planned": "NO",
        "api_calls_executed": "NO",
        "next_action": "Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return plan, summary, md(day, plan, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, plan: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Queue-to-Enrichment Dry Run Planner - {day}",
        "",
        "## Summary",
        f"- rows_planned: {summary['rows_planned']}",
        f"- dry_run_decision_counts: {summary['dry_run_decision_counts']}",
        f"- risk_label_counts: {summary['risk_label_counts']}",
        f"- priority_counts: {summary['priority_counts']}",
        f"- total_estimated_call_units: {summary['total_estimated_call_units']}",
        "- api_calls_planned: NO",
        "- api_calls_executed: NO",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Dry Run Rows",
    ]
    if not plan:
        lines.append("- none. Trusted raw scoring queue is empty or missing.")
    for row in plan[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | priority={row['queue_priority']} | risk={row['risk_label']} | units={row['estimated_call_units']} | blocks={row['enrichment_blocks_needed']} | decision={row['dry_run_decision']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This planner is dry-run only.",
        "- It does not call APIs, touch secrets, increase spend, create picks, create stake permission, or bypass gates.",
        "- Any future enrichment/API stage requires explicit approval and its own safety gate.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    plan, summary, markdown = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_queue_to_enrichment_dry_run_plan.csv", plan, PLAN_FIELDS)
        write_csv(base / "vsigma_queue_to_enrichment_dry_run_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_queue_to_enrichment_dry_run_plan.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA QUEUE-TO-ENRICHMENT DRY RUN PLANNER ===")
    print(f"rows_planned={summary[0]['rows_planned']}")
    print(f"risk_label_counts={summary[0]['risk_label_counts']}")
    print(f"total_estimated_call_units={summary[0]['total_estimated_call_units']}")
    print("api_calls_executed=NO")
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
