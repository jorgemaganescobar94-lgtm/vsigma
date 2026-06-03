from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

import build_date_coherence_guard as date_guard

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


def load_summary(day: str) -> dict[str, str]:
    rows = read_csv(TODAY / day / "vsigma_date_coherence_guard_summary.csv") or read_csv(GOVERNANCE / "vsigma_date_coherence_guard_summary.csv")
    return rows[0] if rows else {}


def section_lines(summary: dict[str, str]) -> list[str]:
    return [
        "## Date Coherence Guard",
        f"- overall_status: {summary.get('overall_status', 'UNKNOWN')}",
        f"- board_status: {summary.get('board_status', 'UNKNOWN')}",
        f"- mismatch_count: {summary.get('mismatch_count', 'UNKNOWN')}",
        f"- missing_core_count: {summary.get('missing_core_count', 'UNKNOWN')}",
        f"- trigger_date_counts: {summary.get('trigger_date_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]


def replace_md_section(path: Path, summary: dict[str, str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    section = "## Date Coherence Guard"
    block = "\n" + "\n".join(section_lines(summary)) + "\n"
    if section not in text:
        path.write_text(text.rstrip() + block, encoding="utf-8")
        return True
    before = text.split(section, 1)[0].rstrip()
    after = text.split(section, 1)[1]
    next_idx = after.find("\n## ")
    tail = after[next_idx:] if next_idx >= 0 else ""
    path.write_text(before + block + tail, encoding="utf-8")
    return True


def upsert_csv_section(path: Path, day: str, summary: dict[str, str]) -> bool:
    rows = read_csv(path)
    if not rows:
        return False
    fields = list(rows[0].keys())
    section = "date_coherence_guard"
    rows = [row for row in rows if row.get("section") != section]
    rows.append({
        "target_date": day,
        "generated_at": summary.get("generated_at", ""),
        "section": section,
        "status": summary.get("overall_status", "UNKNOWN"),
        "detail": (
            f"board_status={summary.get('board_status', 'UNKNOWN')}; "
            f"mismatch_count={summary.get('mismatch_count', 'UNKNOWN')}; "
            f"missing_core_count={summary.get('missing_core_count', 'UNKNOWN')}; "
            f"trigger_date_counts={summary.get('trigger_date_counts', 'UNKNOWN')}"
        ),
        "next_action": summary.get("next_action", "UNKNOWN"),
        "auto_apply": "NO",
        "production_change": "NO",
    })
    write_csv(path, rows, fields)
    return True


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    date_guard.run(day, tz)
    summary = load_summary(day)
    md_updates = 0
    csv_updates = 0
    for base in [processed / "today" / day, processed / "governance"]:
        if replace_md_section(base / "vsigma_consolidated_daily_operator_panel.md", summary):
            md_updates += 1
        if upsert_csv_section(base / "vsigma_consolidated_daily_operator_panel.csv", day, summary):
            csv_updates += 1
    print("=== VSIGMA POST-SELF-HEAL DATE GUARD REFRESH ===")
    print(f"overall_status={summary.get('overall_status', 'UNKNOWN')}")
    print(f"board_status={summary.get('board_status', 'UNKNOWN')}")
    print(f"mismatch_count={summary.get('mismatch_count', 'UNKNOWN')}")
    print(f"missing_core_count={summary.get('missing_core_count', 'UNKNOWN')}")
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
