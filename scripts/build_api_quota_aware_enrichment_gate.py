from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
PLAN_NAME = "API-Football Ultra"
PLAN_REQUESTS_PER_DAY = 75_000
MAX_AUTO_UNITS_PER_DAY = 5_000
MAX_AUTO_UNITS_PER_RUN = 1_500
P2_PROBE_UNITS_PER_ROW = 1

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league",
    "queue_priority", "risk_label", "estimated_call_units", "quota_policy_decision",
    "planned_mode", "quota_units_reserved", "full_enrichment_allowed", "coverage_probe_allowed",
    "api_calls_allowed", "api_calls_executed", "policy_reason", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "quota_gate_status", "api_plan_name", "plan_requests_per_day",
    "rows_reviewed", "p1_rows", "p2_rows", "p1_estimated_units", "p2_estimated_units",
    "p2_probe_units", "total_estimated_units", "auto_units_reserved", "max_auto_units_per_day",
    "max_auto_units_per_run", "quota_decision_counts", "api_calls_allowed", "api_calls_executed",
    "recommended_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0


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


def load_plan_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_queue_to_enrichment_dry_run_plan.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_queue_to_enrichment_dry_run_plan.csv")
    return rows


def classify(row: dict[str, str], running_reserved: int) -> tuple[str, str, int, str, str, str, str]:
    priority = up(row.get("queue_priority"))
    risk = up(row.get("risk_label"))
    estimated = as_int(row.get("estimated_call_units"))

    if "P1_TRUSTED_MISSING_SCORING" in priority and risk == "MEDIUM":
        if running_reserved + estimated <= MAX_AUTO_UNITS_PER_RUN:
            return (
                "AUTO_ENRICHMENT_ALLOWED_P1",
                "FULL_ENRICHMENT_WITH_NORMAL_GATES",
                estimated,
                "YES",
                "NO",
                "YES_LIMITED",
                "P1 trusted fixture is within quota-aware run limit; normal downstream gates still required.",
            )
        return (
            "P1_OVER_RUN_LIMIT_WAIT",
            "WAIT_NEXT_RUN_OR_MANUAL_APPROVAL",
            0,
            "NO",
            "NO",
            "NO",
            "P1 fixture is trusted but would exceed the per-run auto-enrichment unit limit.",
        )

    if "P2_LOW_COVERAGE_SCORING" in priority or "HIGH_LOW_COVERAGE" in risk:
        probe_units = P2_PROBE_UNITS_PER_ROW
        if running_reserved + probe_units <= MAX_AUTO_UNITS_PER_RUN:
            return (
                "COVERAGE_PROBE_ALLOWED_P2",
                "COVERAGE_PROBE_ONLY",
                probe_units,
                "NO",
                "YES",
                "YES_PROBE_ONLY",
                "P2 low-coverage fixture may run a lightweight coverage probe only; full enrichment remains blocked.",
            )
        return (
            "P2_PROBE_OVER_RUN_LIMIT_WAIT",
            "WAIT_NEXT_RUN_OR_MANUAL_APPROVAL",
            0,
            "NO",
            "NO",
            "NO",
            "P2 fixture coverage probe would exceed the per-run auto-enrichment unit limit.",
        )

    return (
        "MANUAL_REVIEW_REQUIRED",
        "NO_AUTO_ENRICHMENT",
        0,
        "NO",
        "NO",
        "NO",
        "Fixture has context volatility or unsupported risk label; manual review required before API use.",
    )


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    plan_rows = load_plan_rows(processed, day)
    out: list[dict[str, object]] = []
    running_reserved = 0

    for row in plan_rows:
        decision, mode, reserved, full_allowed, probe_allowed, api_allowed, reason = classify(row, running_reserved)
        running_reserved += reserved
        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "queue_priority": norm(row.get("queue_priority")),
            "risk_label": norm(row.get("risk_label")),
            "estimated_call_units": as_int(row.get("estimated_call_units")),
            "quota_policy_decision": decision,
            "planned_mode": mode,
            "quota_units_reserved": reserved,
            "full_enrichment_allowed": full_allowed,
            "coverage_probe_allowed": probe_allowed,
            "api_calls_allowed": api_allowed,
            "api_calls_executed": "NO",
            "policy_reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        })

    p1_rows = [r for r in out if "P1_TRUSTED_MISSING_SCORING" in up(r.get("queue_priority"))]
    p2_rows = [r for r in out if "P2_LOW_COVERAGE_SCORING" in up(r.get("queue_priority"))]
    p1_units = sum(as_int(r.get("estimated_call_units")) for r in p1_rows)
    p2_units = sum(as_int(r.get("estimated_call_units")) for r in p2_rows)
    p2_probe_units = sum(as_int(r.get("quota_units_reserved")) for r in p2_rows)
    total_units = p1_units + p2_units
    allowed_count = sum(1 for r in out if str(r.get("api_calls_allowed", "")).startswith("YES"))
    status = "AUTO_ENRICHMENT_ALLOWED_LIMITED" if allowed_count else "NO_AUTO_ENRICHMENT_ALLOWED"
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "quota_gate_status": status,
        "api_plan_name": PLAN_NAME,
        "plan_requests_per_day": PLAN_REQUESTS_PER_DAY,
        "rows_reviewed": len(out),
        "p1_rows": len(p1_rows),
        "p2_rows": len(p2_rows),
        "p1_estimated_units": p1_units,
        "p2_estimated_units": p2_units,
        "p2_probe_units": p2_probe_units,
        "total_estimated_units": total_units,
        "auto_units_reserved": running_reserved,
        "max_auto_units_per_day": MAX_AUTO_UNITS_PER_DAY,
        "max_auto_units_per_run": MAX_AUTO_UNITS_PER_RUN,
        "quota_decision_counts": counts(out, "quota_policy_decision"),
        "api_calls_allowed": "YES_LIMITED" if allowed_count else "NO",
        "api_calls_executed": "NO",
        "recommended_action": "Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, md(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API Quota-Aware Enrichment Gate - {day}",
        "",
        "## Summary",
        f"- quota_gate_status: {summary['quota_gate_status']}",
        f"- api_plan_name: {summary['api_plan_name']}",
        f"- plan_requests_per_day: {summary['plan_requests_per_day']}",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- p1_rows: {summary['p1_rows']}",
        f"- p2_rows: {summary['p2_rows']}",
        f"- p1_estimated_units: {summary['p1_estimated_units']}",
        f"- p2_estimated_units: {summary['p2_estimated_units']}",
        f"- p2_probe_units: {summary['p2_probe_units']}",
        f"- total_estimated_units: {summary['total_estimated_units']}",
        f"- auto_units_reserved: {summary['auto_units_reserved']}",
        f"- max_auto_units_per_day: {summary['max_auto_units_per_day']}",
        f"- max_auto_units_per_run: {summary['max_auto_units_per_run']}",
        f"- quota_decision_counts: {summary['quota_decision_counts']}",
        f"- api_calls_allowed: {summary['api_calls_allowed']}",
        f"- api_calls_executed: {summary['api_calls_executed']}",
        f"- recommended_action: {summary['recommended_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Allowlist / Policy Rows",
    ]
    if not rows:
        lines.append("- none. Dry-run enrichment plan is missing or empty.")
    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | priority={row['queue_priority']} | risk={row['risk_label']} | decision={row['quota_policy_decision']} | mode={row['planned_mode']} | reserved={row['quota_units_reserved']} | api_allowed={row['api_calls_allowed']} | executed={row['api_calls_executed']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This gate is policy/allowlist only; it does not call APIs.",
        "- API calls executed remains NO until a separate enrichment executor is explicitly run.",
        "- P1 may be auto-allowlisted within quota; P2 is coverage-probe-only; volatile/manual rows stay blocked.",
        "- Enrichment alone never creates pick or stake permission.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_quota_aware_enrichment_gate.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_quota_aware_enrichment_gate_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_quota_aware_enrichment_gate.md").write_text(markdown, encoding="utf-8")
    s = summary[0]
    print("=== VSIGMA API QUOTA-AWARE ENRICHMENT GATE ===")
    print(f"quota_gate_status={s['quota_gate_status']}")
    print(f"api_plan_name={s['api_plan_name']}")
    print(f"plan_requests_per_day={s['plan_requests_per_day']}")
    print(f"auto_units_reserved={s['auto_units_reserved']}")
    print(f"api_calls_allowed={s['api_calls_allowed']}")
    print(f"api_calls_executed={s['api_calls_executed']}")
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
