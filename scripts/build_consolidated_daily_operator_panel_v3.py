from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

import build_consolidated_daily_operator_panel_v2 as panel_v2
import build_date_coherence_guard as date_guard
import build_upstream_board_input_diagnostic as upstream_diag

ROOT = Path("data/processed")
TODAY = ROOT / "today"
GOVERNANCE = ROOT / "governance"


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


def append_panel_section(day: str, section_title: str, section_key: str, summary: dict[str, str], lines: list[str], status_field: str, detail_builder) -> None:
    for base in [TODAY / day, GOVERNANCE]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        csv_path = base / "vsigma_consolidated_daily_operator_panel.csv"

        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            block = "\n".join(["", f"## {section_title}", *lines]) + "\n"
            if f"## {section_title}" not in text:
                md_path.write_text(text + block, encoding="utf-8")

        rows = read_csv(csv_path)
        if rows:
            fields = list(rows[0].keys())
            existing = {row.get("section") for row in rows}
            if section_key not in existing:
                rows.append(
                    {
                        "target_date": day,
                        "generated_at": summary.get("generated_at", ""),
                        "section": section_key,
                        "status": summary.get(status_field, "UNKNOWN"),
                        "detail": detail_builder(summary),
                        "next_action": summary.get("next_action", "UNKNOWN"),
                        "auto_apply": "NO",
                        "production_change": "NO",
                    }
                )
                write_csv(csv_path, rows, fields)


def append_date_guard_to_panel(day: str, guard_summary: dict[str, str]) -> None:
    append_panel_section(
        day,
        "Date Coherence Guard",
        "date_coherence_guard",
        guard_summary,
        [
            f"- overall_status: {guard_summary.get('overall_status', 'UNKNOWN')}",
            f"- board_status: {guard_summary.get('board_status', 'UNKNOWN')}",
            f"- mismatch_count: {guard_summary.get('mismatch_count', 'UNKNOWN')}",
            f"- missing_core_count: {guard_summary.get('missing_core_count', 'UNKNOWN')}",
            f"- trigger_date_counts: {guard_summary.get('trigger_date_counts', 'UNKNOWN')}",
            f"- next_action: {guard_summary.get('next_action', 'UNKNOWN')}",
        ],
        "overall_status",
        lambda s: (
            f"board_status={s.get('board_status', 'UNKNOWN')}; "
            f"mismatch_count={s.get('mismatch_count', 'UNKNOWN')}; "
            f"missing_core_count={s.get('missing_core_count', 'UNKNOWN')}; "
            f"trigger_date_counts={s.get('trigger_date_counts', 'UNKNOWN')}"
        ),
    )


def append_upstream_diag_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(
        day,
        "Upstream Board Input Diagnostic",
        "upstream_board_input_diagnostic",
        summary,
        [
            f"- overall_status: {summary.get('overall_status', 'UNKNOWN')}",
            f"- first_empty_required_component: {summary.get('first_empty_required_component', 'UNKNOWN')}",
            f"- missing_required_count: {summary.get('missing_required_count', 'UNKNOWN')}",
            f"- empty_required_count: {summary.get('empty_required_count', 'UNKNOWN')}",
            f"- date_issue_count: {summary.get('date_issue_count', 'UNKNOWN')}",
            f"- forecast_rows: {summary.get('forecast_rows', 'UNKNOWN')}",
            f"- translator_rows: {summary.get('translator_rows', 'UNKNOWN')}",
            f"- board_rows: {summary.get('board_rows', 'UNKNOWN')}",
            f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
        ],
        "overall_status",
        lambda s: (
            f"first_empty_required_component={s.get('first_empty_required_component', 'UNKNOWN')}; "
            f"forecast_rows={s.get('forecast_rows', 'UNKNOWN')}; "
            f"translator_rows={s.get('translator_rows', 'UNKNOWN')}; "
            f"board_rows={s.get('board_rows', 'UNKNOWN')}"
        ),
    )


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    date_guard.run(day, tz)
    upstream_diag.run(day, tz)
    panel_v2.run(day, tz)

    date_rows = read_csv(TODAY / day / "vsigma_date_coherence_guard_summary.csv") or read_csv(GOVERNANCE / "vsigma_date_coherence_guard_summary.csv")
    upstream_rows = read_csv(TODAY / day / "vsigma_upstream_board_input_diagnostic_summary.csv") or read_csv(GOVERNANCE / "vsigma_upstream_board_input_diagnostic_summary.csv")
    if date_rows:
        append_date_guard_to_panel(day, date_rows[0])
    if upstream_rows:
        append_upstream_diag_to_panel(day, upstream_rows[0])
    print("=== VSIGMA CONSOLIDATED DAILY OPERATOR PANEL V3 ===")
    if date_rows:
        print(f"date_guard={date_rows[0].get('overall_status', 'UNKNOWN')}")
    if upstream_rows:
        print(f"upstream_diag={upstream_rows[0].get('overall_status', 'UNKNOWN')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
