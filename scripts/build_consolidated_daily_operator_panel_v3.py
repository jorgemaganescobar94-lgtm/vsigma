from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

import build_consolidated_daily_operator_panel_v2 as panel_v2
import build_date_coherence_guard as date_guard

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


def append_date_guard_to_panel(day: str, guard_summary: dict[str, str]) -> None:
    for base in [TODAY / day, GOVERNANCE]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        csv_path = base / "vsigma_consolidated_daily_operator_panel.csv"

        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            block = "\n".join(
                [
                    "",
                    "## Date Coherence Guard",
                    f"- overall_status: {guard_summary.get('overall_status', 'UNKNOWN')}",
                    f"- board_status: {guard_summary.get('board_status', 'UNKNOWN')}",
                    f"- mismatch_count: {guard_summary.get('mismatch_count', 'UNKNOWN')}",
                    f"- missing_core_count: {guard_summary.get('missing_core_count', 'UNKNOWN')}",
                    f"- trigger_date_counts: {guard_summary.get('trigger_date_counts', 'UNKNOWN')}",
                    f"- next_action: {guard_summary.get('next_action', 'UNKNOWN')}",
                ]
            ) + "\n"
            if "## Date Coherence Guard" not in text:
                md_path.write_text(text + block, encoding="utf-8")

        rows = read_csv(csv_path)
        if rows:
            fields = list(rows[0].keys())
            existing = {row.get("section") for row in rows}
            if "date_coherence_guard" not in existing:
                rows.append(
                    {
                        "target_date": day,
                        "generated_at": guard_summary.get("generated_at", ""),
                        "section": "date_coherence_guard",
                        "status": guard_summary.get("overall_status", "UNKNOWN"),
                        "detail": (
                            f"board_status={guard_summary.get('board_status', 'UNKNOWN')}; "
                            f"mismatch_count={guard_summary.get('mismatch_count', 'UNKNOWN')}; "
                            f"missing_core_count={guard_summary.get('missing_core_count', 'UNKNOWN')}; "
                            f"trigger_date_counts={guard_summary.get('trigger_date_counts', 'UNKNOWN')}"
                        ),
                        "next_action": guard_summary.get("next_action", "UNKNOWN"),
                        "auto_apply": "NO",
                        "production_change": "NO",
                    }
                )
                write_csv(csv_path, rows, fields)


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    date_guard.run(day, tz)
    panel_v2.run(day, tz)
    summary_rows = read_csv(TODAY / day / "vsigma_date_coherence_guard_summary.csv") or read_csv(GOVERNANCE / "vsigma_date_coherence_guard_summary.csv")
    if summary_rows:
        append_date_guard_to_panel(day, summary_rows[0])
    print("=== VSIGMA CONSOLIDATED DAILY OPERATOR PANEL V3 ===")
    if summary_rows:
        print(f"date_guard={summary_rows[0].get('overall_status', 'UNKNOWN')}")
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
