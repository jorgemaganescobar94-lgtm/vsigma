from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
MAX_ALLOWED_WITHOUT_MANUAL_APPROVAL = 0
SUMMARY_FIELDS = [
    "target_date", "generated_at", "approval_gate_status", "rows_planned", "estimated_call_units",
    "approval_required", "max_allowed_without_manual_approval", "api_calls_allowed", "api_calls_planned",
    "api_calls_executed", "recommended_action", "approval_reason", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


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


def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0


def load_dry_run_summary(processed: Path, day: str) -> dict[str, str] | None:
    rows = read_rows(processed / "today" / day / "vsigma_queue_to_enrichment_dry_run_summary.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_queue_to_enrichment_dry_run_summary.csv")
    return rows[0] if rows else None


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    dry = load_dry_run_summary(processed, day)
    if not dry:
        summary = {
            "target_date": day,
            "generated_at": generated,
            "approval_gate_status": "MISSING_DRY_RUN_PLAN",
            "rows_planned": 0,
            "estimated_call_units": 0,
            "approval_required": "YES",
            "max_allowed_without_manual_approval": MAX_ALLOWED_WITHOUT_MANUAL_APPROVAL,
            "api_calls_allowed": "NO",
            "api_calls_planned": "NO",
            "api_calls_executed": "NO",
            "recommended_action": "RUN_DRY_RUN_PLANNER_FIRST",
            "approval_reason": "Dry-run plan missing; enrichment cannot proceed.",
            "auto_apply": "NO",
            "production_change": "NO",
        }
        return [summary], md(day, summary)

    rows_planned = as_int(dry.get("rows_planned"))
    estimated_units = as_int(dry.get("total_estimated_call_units"))
    needs_approval = estimated_units > MAX_ALLOWED_WITHOUT_MANUAL_APPROVAL or rows_planned > 0
    summary = {
        "target_date": day,
        "generated_at": generated,
        "approval_gate_status": "WAIT_FOR_MANUAL_APPROVAL" if needs_approval else "NO_ENRICHMENT_NEEDED",
        "rows_planned": rows_planned,
        "estimated_call_units": estimated_units,
        "approval_required": "YES" if needs_approval else "NO",
        "max_allowed_without_manual_approval": MAX_ALLOWED_WITHOUT_MANUAL_APPROVAL,
        "api_calls_allowed": "NO" if needs_approval else "NO",
        "api_calls_planned": "NO",
        "api_calls_executed": "NO",
        "recommended_action": "WAIT_FOR_MANUAL_APPROVAL" if needs_approval else "NO_ACTION",
        "approval_reason": (
            f"Estimated enrichment workload is {estimated_units} call units across {rows_planned} planned rows; manual approval is required before any API/enrichment stage."
            if needs_approval else "No planned enrichment workload."
        ),
        "auto_apply": "NO",
        "production_change": "NO",
    }
    return [summary], md(day, summary)


def md(day: str, summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Enrichment Cost & Approval Gate - {day}",
        "",
        "## Summary",
        f"- approval_gate_status: {summary['approval_gate_status']}",
        f"- rows_planned: {summary['rows_planned']}",
        f"- estimated_call_units: {summary['estimated_call_units']}",
        f"- approval_required: {summary['approval_required']}",
        f"- max_allowed_without_manual_approval: {summary['max_allowed_without_manual_approval']}",
        f"- api_calls_allowed: {summary['api_calls_allowed']}",
        f"- api_calls_planned: {summary['api_calls_planned']}",
        f"- api_calls_executed: {summary['api_calls_executed']}",
        f"- recommended_action: {summary['recommended_action']}",
        f"- approval_reason: {summary['approval_reason']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Guardrails",
        "- This gate does not call APIs, touch secrets, increase spend, create picks, create stake permission, or bypass gates.",
        "- Any future enrichment/API stage requires explicit manual approval.",
        "- The default maximum allowed without manual approval is 0 call units.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, markdown = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_enrichment_cost_approval_gate_summary.csv", rows, SUMMARY_FIELDS)
        (base / "vsigma_enrichment_cost_approval_gate.md").write_text(markdown, encoding="utf-8")
    summary = rows[0]
    print("=== VSIGMA ENRICHMENT COST & APPROVAL GATE ===")
    print(f"approval_gate_status={summary['approval_gate_status']}")
    print(f"estimated_call_units={summary['estimated_call_units']}")
    print(f"approval_required={summary['approval_required']}")
    print(f"api_calls_executed={summary['api_calls_executed']}")
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
