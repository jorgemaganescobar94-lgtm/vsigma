from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

import build_api_quota_aware_enrichment_gate as quota_gate

PROCESSED = Path("data/processed")
TODAY = PROCESSED / "today"
GOVERNANCE = PROCESSED / "governance"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def panel_lines(summary: dict[str, str]) -> list[str]:
    return [
        "## API Quota-Aware Enrichment Gate",
        f"- quota_gate_status: {summary.get('quota_gate_status', 'UNKNOWN')}",
        f"- api_plan_name: {summary.get('api_plan_name', 'UNKNOWN')}",
        f"- plan_requests_per_day: {summary.get('plan_requests_per_day', 'UNKNOWN')}",
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- p1_rows: {summary.get('p1_rows', 'UNKNOWN')}",
        f"- p2_rows: {summary.get('p2_rows', 'UNKNOWN')}",
        f"- p1_estimated_units: {summary.get('p1_estimated_units', 'UNKNOWN')}",
        f"- p2_estimated_units: {summary.get('p2_estimated_units', 'UNKNOWN')}",
        f"- auto_units_reserved: {summary.get('auto_units_reserved', 'UNKNOWN')}",
        f"- max_auto_units_per_day: {summary.get('max_auto_units_per_day', 'UNKNOWN')}",
        f"- max_auto_units_per_run: {summary.get('max_auto_units_per_run', 'UNKNOWN')}",
        f"- quota_decision_counts: {summary.get('quota_decision_counts', 'UNKNOWN')}",
        f"- api_calls_allowed: {summary.get('api_calls_allowed', 'UNKNOWN')}",
        f"- api_calls_executed: {summary.get('api_calls_executed', 'UNKNOWN')}",
        f"- recommended_action: {summary.get('recommended_action', 'UNKNOWN')}",
    ]


def append_md_section(path: Path, summary: dict[str, str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    section = "## API Quota-Aware Enrichment Gate"
    block = "\n" + "\n".join(panel_lines(summary)) + "\n"
    if section in text:
        before = text.split(section)[0].rstrip()
        after = text.split(section, 1)[1]
        next_idx = after.find("\n## ")
        if next_idx >= 0:
            tail = after[next_idx:]
            path.write_text(before + block + tail, encoding="utf-8")
        else:
            path.write_text(before + block, encoding="utf-8")
    else:
        path.write_text(text.rstrip() + block, encoding="utf-8")
    return True


def append_csv_row(path: Path, day: str, summary: dict[str, str]) -> bool:
    rows = read_csv(path)
    if not rows:
        return False
    fields = list(rows[0].keys())
    section = "api_quota_aware_enrichment_gate"
    rows = [row for row in rows if row.get("section") != section]
    rows.append({
        "target_date": day,
        "generated_at": summary.get("generated_at", ""),
        "section": section,
        "status": summary.get("quota_gate_status", "UNKNOWN"),
        "detail": (
            f"plan={summary.get('api_plan_name', 'UNKNOWN')}; "
            f"rows={summary.get('rows_reviewed', 'UNKNOWN')}; "
            f"reserved={summary.get('auto_units_reserved', 'UNKNOWN')}; "
            f"allowed={summary.get('api_calls_allowed', 'UNKNOWN')}; "
            f"executed={summary.get('api_calls_executed', 'UNKNOWN')}"
        ),
        "next_action": summary.get("recommended_action", "UNKNOWN"),
        "auto_apply": "NO",
        "production_change": "NO",
    })
    write_csv(path, rows, fields)
    return True


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    quota_gate.run(day, tz, processed)
    summary_rows = read_csv(processed / "today" / day / "vsigma_api_quota_aware_enrichment_gate_summary.csv") or read_csv(processed / "governance" / "vsigma_api_quota_aware_enrichment_gate_summary.csv")
    summary = summary_rows[0] if summary_rows else {}
    md_updates = 0
    csv_updates = 0
    for base in [processed / "today" / day, processed / "governance"]:
        if append_md_section(base / "vsigma_consolidated_daily_operator_panel.md", summary):
            md_updates += 1
        if append_csv_row(base / "vsigma_consolidated_daily_operator_panel.csv", day, summary):
            csv_updates += 1
    print("=== VSIGMA API QUOTA GATE PANEL INTEGRATION ===")
    print(f"quota_gate_status={summary.get('quota_gate_status', 'UNKNOWN')}")
    print(f"api_calls_allowed={summary.get('api_calls_allowed', 'UNKNOWN')}")
    print(f"api_calls_executed={summary.get('api_calls_executed', 'UNKNOWN')}")
    print(f"panel_md_updates={md_updates}")
    print(f"panel_csv_updates={csv_updates}")
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
