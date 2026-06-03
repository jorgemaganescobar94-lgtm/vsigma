from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
SUMMARY_FIELDS = [
    "target_date", "generated_at", "normalized_status", "board_status", "mismatch_count",
    "promoted_rows", "queue_rows", "board_rows", "diagnostic_no_bet_rows",
    "operator_state", "next_action", "auto_apply", "production_change",
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


def first(processed: Path, day: str, name: str) -> dict[str, str]:
    rows = read_rows(processed / "today" / day / name) or read_rows(processed / "governance" / name)
    return rows[0] if rows else {}


def board_rows(processed: Path, day: str) -> list[dict[str, str]]:
    return read_rows(processed / "today" / day / "vsigma_daily_execution_board.csv") or read_rows(processed / "governance" / "vsigma_daily_execution_board.csv")


def diagnostic_no_bet_count(rows: list[dict[str, str]]) -> int:
    count = 0
    for row in rows:
        text = " ".join(up(v) for v in row.values())
        if "NO_BET" in up(row.get("final_decision")) and (
            "PROMOTION_GATE_DIAGNOSTIC" in text
            or "EMPTY_BY_PROMOTION_GATE" in text
            or "NO_PROMOTED_RAW_CANDIDATES" in text
        ):
            count += 1
    return count


def classify(processed: Path, day: str, generated: str) -> dict[str, object]:
    date_summary = first(processed, day, "vsigma_date_coherence_guard_summary.csv")
    promotion_summary = first(processed, day, "vsigma_trusted_raw_candidate_promotion_summary.csv")
    queue_summary = first(processed, day, "vsigma_trusted_raw_scoring_queue_summary.csv")
    rows = board_rows(processed, day)

    board_status = norm(date_summary.get("board_status"))
    mismatch_count = as_int(date_summary.get("mismatch_count"))
    promoted_rows = as_int(promotion_summary.get("promoted_rows"))
    queue_rows = as_int(queue_summary.get("queue_rows"))
    board_count = len(rows)
    diagnostic_count = diagnostic_no_bet_count(rows)

    board_ok = "OK" in up(board_status)
    healthy_empty = board_ok and mismatch_count == 0 and promoted_rows == 0 and board_count >= 1 and diagnostic_count >= 1
    if healthy_empty:
        normalized_status = "OK_EMPTY_BY_PROMOTION_GATE"
        operator_state = "HEALTHY_EMPTY_NO_ACTION"
        next_action = "No picks. System is coherent and empty because zero candidates were promoted. Wait for future data or improved trusted source coverage."
    elif promoted_rows == 0 and board_count >= 1:
        normalized_status = "REVIEW_EMPTY_DIAGNOSTIC_BOARD"
        operator_state = "EMPTY_REVIEW_REQUIRED"
        next_action = "Review date guard and board diagnostics before market discussion."
    else:
        normalized_status = "NOT_EMPTY_OR_NOT_APPLICABLE"
        operator_state = "NORMAL_PIPELINE_REVIEW"
        next_action = "Continue normal panel interpretation."

    return {
        "target_date": day,
        "generated_at": generated,
        "normalized_status": normalized_status,
        "board_status": board_status,
        "mismatch_count": mismatch_count,
        "promoted_rows": promoted_rows,
        "queue_rows": queue_rows,
        "board_rows": board_count,
        "diagnostic_no_bet_rows": diagnostic_count,
        "operator_state": operator_state,
        "next_action": next_action,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def md(day: str, summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Empty Diagnostic Board State Normalizer - {day}",
        "",
        "## Summary",
        f"- normalized_status: {summary['normalized_status']}",
        f"- operator_state: {summary['operator_state']}",
        f"- board_status: {summary['board_status']}",
        f"- mismatch_count: {summary['mismatch_count']}",
        f"- promoted_rows: {summary['promoted_rows']}",
        f"- queue_rows: {summary['queue_rows']}",
        f"- board_rows: {summary['board_rows']}",
        f"- diagnostic_no_bet_rows: {summary['diagnostic_no_bet_rows']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Guardrails",
        "- Normalizer is diagnostic only.",
        "- It does not call APIs, create picks, create stake permission, or bypass gates.",
        "- OK_EMPTY_BY_PROMOTION_GATE means no market action is allowed; it only distinguishes a healthy empty board from a broken board.",
    ]
    return "\n".join(lines) + "\n"


def update_panel_md(path: Path, summary: dict[str, object]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    status = str(summary.get("normalized_status", "UNKNOWN"))
    if status == "OK_EMPTY_BY_PROMOTION_GATE":
        text = text.replace("- panel_status: PARTIAL_OUTPUTS", "- panel_status: OK_EMPTY_BY_PROMOTION_GATE")
        text = text.replace("- panel_status: NONE", "- panel_status: OK_EMPTY_BY_PROMOTION_GATE")
    section = "## Empty Diagnostic Board State Normalizer"
    block_lines = [
        section,
        f"- normalized_status: {summary.get('normalized_status', 'UNKNOWN')}",
        f"- operator_state: {summary.get('operator_state', 'UNKNOWN')}",
        f"- board_status: {summary.get('board_status', 'UNKNOWN')}",
        f"- mismatch_count: {summary.get('mismatch_count', 'UNKNOWN')}",
        f"- promoted_rows: {summary.get('promoted_rows', 'UNKNOWN')}",
        f"- queue_rows: {summary.get('queue_rows', 'UNKNOWN')}",
        f"- diagnostic_no_bet_rows: {summary.get('diagnostic_no_bet_rows', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(block_lines) + "\n"
    if section in text:
        before = text.split(section, 1)[0].rstrip()
        after = text.split(section, 1)[1]
        next_idx = after.find("\n## ")
        tail = after[next_idx:] if next_idx >= 0 else ""
        text = before + block + tail
    else:
        text = text.rstrip() + block
    path.write_text(text, encoding="utf-8")
    return True


def update_panel_csv(path: Path, day: str, summary: dict[str, object]) -> bool:
    rows = read_rows(path)
    if not rows:
        return False
    fields = list(rows[0].keys())
    section = "empty_diagnostic_board_state_normalizer"
    rows = [row for row in rows if row.get("section") != section]
    rows.append({
        "target_date": day,
        "generated_at": str(summary.get("generated_at", "")),
        "section": section,
        "status": str(summary.get("normalized_status", "UNKNOWN")),
        "detail": (
            f"operator_state={summary.get('operator_state', 'UNKNOWN')}; "
            f"promoted_rows={summary.get('promoted_rows', 'UNKNOWN')}; "
            f"queue_rows={summary.get('queue_rows', 'UNKNOWN')}; "
            f"diagnostic_no_bet_rows={summary.get('diagnostic_no_bet_rows', 'UNKNOWN')}"
        ),
        "next_action": str(summary.get("next_action", "UNKNOWN")),
        "auto_apply": "NO",
        "production_change": "NO",
    })
    write_csv(path, rows, fields)
    return True


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    summary = classify(processed, day, generated)
    md_text = md(day, summary)
    md_updates = 0
    csv_updates = 0
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_empty_diagnostic_board_state_normalizer_summary.csv", [summary], SUMMARY_FIELDS)
        (base / "vsigma_empty_diagnostic_board_state_normalizer.md").write_text(md_text, encoding="utf-8")
        if update_panel_md(base / "vsigma_consolidated_daily_operator_panel.md", summary):
            md_updates += 1
        if update_panel_csv(base / "vsigma_consolidated_daily_operator_panel.csv", day, summary):
            csv_updates += 1
    print("=== VSIGMA EMPTY DIAGNOSTIC BOARD STATE NORMALIZER ===")
    print(f"normalized_status={summary['normalized_status']}")
    print(f"operator_state={summary['operator_state']}")
    print(f"promoted_rows={summary['promoted_rows']}")
    print(f"queue_rows={summary['queue_rows']}")
    print(f"diagnostic_no_bet_rows={summary['diagnostic_no_bet_rows']}")
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
