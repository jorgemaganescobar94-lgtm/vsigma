from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
BOARD_FIELDS = [
    "target_date", "generated_at", "board_rank", "fixture_id", "home_team", "away_team",
    "final_decision", "board_bucket", "primary_market", "secondary_market", "stake_band",
    "execution_permission", "portfolio_status", "context_level", "forecast_confidence", "forecast_warning",
    "translation_score", "kill_switch", "stat_profile", "key_stat_forecast",
    "prelock_trigger", "live_trigger", "cancel_trigger", "operator_note",
    "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "self_heal_status", "promotion_rows_reviewed", "promoted_rows",
    "blocked_rows", "quarantine_rows", "board_rows_written", "reason", "auto_apply", "production_change",
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


def existing_board_rows(base: Path, day: str) -> list[dict[str, str]]:
    return read_rows(base / "today" / day / "vsigma_daily_execution_board.csv")


def should_self_heal(base: Path, day: str) -> tuple[bool, dict[str, str] | None, str]:
    if existing_board_rows(base, day):
        return False, None, "daily board already has rows"
    summary_rows = read_rows(base / "today" / day / "vsigma_trusted_raw_candidate_promotion_summary.csv") or read_rows(base / "governance" / "vsigma_trusted_raw_candidate_promotion_summary.csv")
    if not summary_rows:
        return False, None, "promotion summary missing"
    summary = summary_rows[0]
    promoted = int(float(norm(summary.get("promoted_rows")) or 0))
    if promoted == 0:
        return True, summary, "0 promoted raw candidates; no scoring-safe rows available"
    return False, summary, "promoted rows exist; normal scoring/translator should build board"


def diagnostic_row(day: str, generated: str, reason: str) -> dict[str, object]:
    return {
        "target_date": day,
        "generated_at": generated,
        "board_rank": "0",
        "fixture_id": "DIAGNOSTIC_EMPTY_BY_PROMOTION_GATE",
        "home_team": "NO_PROMOTED_RAW_CANDIDATES",
        "away_team": "NO_SCORING_SAFE_ROWS",
        "final_decision": "NO_BET",
        "board_bucket": "EMPTY_BY_PROMOTION_GATE",
        "primary_market": "NO_MARKET",
        "secondary_market": "NONE",
        "stake_band": "NO_STAKE",
        "execution_permission": "NO_BET",
        "portfolio_status": "PROMOTION_GATE_BLOCK",
        "context_level": "NO_PROMOTED_ROWS",
        "forecast_confidence": "NONE",
        "forecast_warning": "no promoted raw candidates",
        "translation_score": "0",
        "kill_switch": "EMPTY_BY_PROMOTION_GATE",
        "stat_profile": "none",
        "key_stat_forecast": "none; no scoring-safe rows available",
        "prelock_trigger": "none",
        "live_trigger": "none",
        "cancel_trigger": "default no bet; no promoted raw candidates",
        "operator_note": reason,
        "source_guard": "PROMOTION_GATE_DIAGNOSTIC_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Daily Execution Board - {day}",
        "",
        "## Summary",
        "- rows_on_board: 0",
        "- board_status: EMPTY_BY_PROMOTION_GATE",
        "- final_decision_counts: NO_BET=0",
        "- board_bucket_counts: EMPTY_BY_PROMOTION_GATE=1 diagnostic row",
        f"- promotion_rows_reviewed: {summary.get('promotion_rows_reviewed', 'UNKNOWN')}",
        f"- promoted_rows: {summary.get('promoted_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- quarantine_rows: {summary.get('quarantine_rows', 'UNKNOWN')}",
        "- source_guard: PROMOTION_GATE_DIAGNOSTIC_ONLY",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Board Rows",
    ]
    for row in rows:
        lines.append(
            f"- diagnostic | {row['final_decision']} | {row['home_team']} vs {row['away_team']} | bucket={row['board_bucket']} | reason={row['operator_note']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This board is diagnostic only and does not create pick permission.",
        "- EMPTY_BY_PROMOTION_GATE means zero promoted raw candidates reached scoring-safe state.",
        "- No stake, live-only, prematch, or combinada can be derived from this board.",
    ]
    return "\n".join(lines) + "\n"


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    do_heal, promotion_summary, reason = should_self_heal(base, day)
    if do_heal and promotion_summary:
        row = diagnostic_row(day, generated, reason)
        rows = [row]
        summary = {
            "target_date": day,
            "generated_at": generated,
            "self_heal_status": "EMPTY_BY_PROMOTION_GATE",
            "promotion_rows_reviewed": promotion_summary.get("rows_reviewed", "0"),
            "promoted_rows": promotion_summary.get("promoted_rows", "0"),
            "blocked_rows": promotion_summary.get("blocked_rows", "0"),
            "quarantine_rows": promotion_summary.get("quarantine_rows", "0"),
            "board_rows_written": "1_DIAGNOSTIC_ROW",
            "reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        }
        for out_base in [base / "today" / day, base / "governance"]:
            write_csv(out_base / "vsigma_daily_execution_board.csv", rows, BOARD_FIELDS)
            (out_base / "vsigma_daily_execution_board.md").write_text(md(day, rows, summary), encoding="utf-8")
            write_csv(out_base / "vsigma_daily_board_self_heal_summary.csv", [summary], SUMMARY_FIELDS)
    else:
        summary = {
            "target_date": day,
            "generated_at": generated,
            "self_heal_status": "NO_ACTION",
            "promotion_rows_reviewed": (promotion_summary or {}).get("rows_reviewed", "0"),
            "promoted_rows": (promotion_summary or {}).get("promoted_rows", "0"),
            "blocked_rows": (promotion_summary or {}).get("blocked_rows", "0"),
            "quarantine_rows": (promotion_summary or {}).get("quarantine_rows", "0"),
            "board_rows_written": "0",
            "reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        }
        for out_base in [base / "today" / day, base / "governance"]:
            write_csv(out_base / "vsigma_daily_board_self_heal_summary.csv", [summary], SUMMARY_FIELDS)
    print("=== VSIGMA DAILY BOARD SELF-HEAL FROM PROMOTION GATE ===")
    print(f"self_heal_status={summary['self_heal_status']}")
    print(f"promoted_rows={summary['promoted_rows']}")
    print(f"board_rows_written={summary['board_rows_written']}")
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
