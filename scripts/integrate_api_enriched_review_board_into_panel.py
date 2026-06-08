from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from datetime import date

PROCESSED = Path("data/processed")
SECTION_TITLE = "## API-Enriched Review Board"

def norm(value: object) -> str:
    return "" if value is None else str(value).strip()

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]

def first_existing(processed: Path, day: str, name: str) -> Path | None:
    for path in [processed / "today" / day / name, processed / "governance" / name]:
        if path.exists():
            return path
    return None

def counts(rows: list[dict[str, str]], field: str) -> str:
    counter: dict[str, int] = {}
    for row in rows:
        key = norm(row.get(field)) or "UNKNOWN"
        counter[key] = counter.get(key, 0) + 1
    if not counter:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in sorted(counter.items(), key=lambda item: (-item[1], item[0])))

def remove_existing_section(text: str) -> str:
    pattern = rf"\n?{re.escape(SECTION_TITLE)}\n.*?(?=\n## |\Z)"
    return re.sub(pattern, "\n", text, flags=re.S).rstrip() + "\n"

def build_section(day: str, processed: Path) -> str:
    board_path = first_existing(processed, day, "vsigma_api_enriched_review_board.csv")
    summary_path = first_existing(processed, day, "vsigma_api_enriched_review_board_summary.csv")

    rows = read_csv(board_path) if board_path else []
    summary_rows = read_csv(summary_path) if summary_path else []
    summary = summary_rows[0] if summary_rows else {}

    ready = norm(summary.get("ready_for_manual_review_rows")) or str(sum(1 for row in rows if norm(row.get("review_board_status")) == "API_ENRICHED_REVIEW_READY"))
    total = norm(summary.get("review_rows_written")) or str(len(rows))
    blocked = norm(summary.get("blocked_rows")) or str(sum(1 for row in rows if norm(row.get("review_board_status")) != "API_ENRICHED_REVIEW_READY"))

    lines = [
        SECTION_TITLE,
        f"- source: {board_path.as_posix() if board_path else 'MISSING'}",
        f"- review_rows_written: {total}",
        f"- ready_for_manual_review_rows: {ready}",
        f"- blocked_rows: {blocked}",
        f"- review_priority_counts: {norm(summary.get('review_priority_counts')) or counts(rows, 'review_priority')}",
        f"- canonical_board_permission_counts: {norm(summary.get('canonical_board_permission_counts')) or counts(rows, 'canonical_board_permission')}",
        f"- pick_permission_counts: {norm(summary.get('pick_permission_counts')) or counts(rows, 'pick_permission')}",
        f"- stake_permission_counts: {norm(summary.get('stake_permission_counts')) or counts(rows, 'stake_permission')}",
        "- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.",
        "",
        "### API Review Rows",
    ]

    if not rows:
        lines.append("- none")

    for row in rows[:10]:
        lines.append(
            "- "
            f"{norm(row.get('review_priority'))} | "
            f"{norm(row.get('home_team'))} vs {norm(row.get('away_team'))} | "
            f"status={norm(row.get('review_board_status'))} | "
            f"score={norm(row.get('candidate_signal_score'))} | "
            f"canonical={norm(row.get('canonical_board_permission'))} | "
            f"pick={norm(row.get('pick_permission'))} | "
            f"stake={norm(row.get('stake_permission'))} | "
            f"summary={norm(row.get('market_signal_summary'))}"
        )

    lines += [
        "",
        "### API Review Guardrails",
        "- This section is informational only.",
        "- It does not modify the canonical daily execution board.",
        "- Manual review remains mandatory.",
        "- auto_apply=NO and production_change=NO remain hardcoded.",
    ]

    return "\n".join(lines) + "\n"

def integrate_panel(path: Path, section: str) -> bool:
    if not path.exists():
        return False

    original = path.read_text(encoding="utf-8")
    cleaned = remove_existing_section(original)

    insert_after = "## API Coverage"
    if insert_after in cleaned:
        # Put section before Official / Probable Lineups if possible.
        marker = "\n## Official / Probable Lineups"
        if marker in cleaned:
            updated = cleaned.replace(marker, "\n" + section + marker, 1)
        else:
            updated = cleaned.rstrip() + "\n\n" + section
    else:
        updated = cleaned.rstrip() + "\n\n" + section

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False

def run(day: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    section = build_section(day, processed)

    changed = 0
    for panel in [
        processed / "today" / day / "vsigma_consolidated_daily_operator_panel.md",
        processed / "governance" / "vsigma_consolidated_daily_operator_panel.md",
    ]:
        if integrate_panel(panel, section):
            changed += 1

    print("=== VSIGMA API REVIEW PANEL INTEGRATION ===")
    print(f"panels_changed={changed}")
    print("auto_apply=NO")
    print("production_change=NO")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.processed_dir)

if __name__ == "__main__":
    main()
