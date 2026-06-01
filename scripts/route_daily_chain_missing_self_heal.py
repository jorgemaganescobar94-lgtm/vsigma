from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
TODAY = ROOT / "today"
GOVERNANCE = ROOT / "governance"
TRIGGER = Path(".vsigma/triggers/daily_decision_chain_v2.trigger")

FIELDS = [
    "target_date",
    "generated_at",
    "self_heal_status",
    "daily_board_exists",
    "daily_board_rows",
    "current_trigger_date",
    "trigger_action",
    "reason",
    "next_action",
    "auto_apply",
    "production_change",
]


def read_trigger_date() -> str:
    if not TRIGGER.exists():
        return "MISSING"
    for line in TRIGGER.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("date="):
            return line.split("=", 1)[1].strip() or "UNKNOWN"
    return "UNKNOWN"


def board_rows(day: str) -> tuple[bool, int]:
    path = TODAY / day / "vsigma_daily_execution_board.csv"
    if not path.exists():
        return False, 0
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return True, 0


def write_report(day: str, tz: str, row: dict[str, str]) -> None:
    for base in [TODAY / day, GOVERNANCE]:
        base.mkdir(parents=True, exist_ok=True)
        csv_path = base / "vsigma_daily_chain_self_heal_router.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow({field: row.get(field, "") for field in FIELDS})
        md = [
            f"# vSIGMA Daily Chain Missing Self-Heal Router - {day}",
            "",
            "## Summary",
            f"- self_heal_status: {row['self_heal_status']}",
            f"- daily_board_exists: {row['daily_board_exists']}",
            f"- daily_board_rows: {row['daily_board_rows']}",
            f"- current_trigger_date: {row['current_trigger_date']}",
            f"- trigger_action: {row['trigger_action']}",
            f"- reason: {row['reason']}",
            f"- next_action: {row['next_action']}",
            "- auto_apply: NO",
            "- production_change: NO",
            "",
            "## Guardrails",
            "- This router only updates the daily decision chain trigger when the daily board is missing/stale.",
            "- It does not execute bets, place stakes, change secrets, or alter model gates.",
            "- If the trigger is already on the target date, it does not rewrite it repeatedly.",
        ]
        (base / "vsigma_daily_chain_self_heal_router.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    exists, rows = board_rows(day)
    trigger_date = read_trigger_date()

    if exists and rows > 0:
        status = "OK_BOARD_PRESENT"
        action = "NO_TRIGGER_CHANGE"
        reason = "daily board exists with rows"
        next_action = "Use consolidated panel/operator brief normally."
    elif trigger_date == day:
        status = "WAIT_DAILY_CHAIN_ALREADY_TRIGGERED"
        action = "NO_TRIGGER_CHANGE"
        reason = "daily board missing/empty, but trigger already targets this date"
        next_action = "Wait for daily chain output or inspect workflow if it does not produce board."
    else:
        status = "DAILY_CHAIN_TRIGGER_WRITTEN"
        action = "UPDATED_DAILY_CHAIN_TRIGGER"
        reason = "daily board missing/empty and trigger did not target current date"
        next_action = "Daily chain should run through trigger bridge and regenerate board/panel."
        TRIGGER.parent.mkdir(parents=True, exist_ok=True)
        TRIGGER.write_text(
            "\n".join(
                [
                    f"date={day}",
                    "include_backtest=false",
                    "requested_by=chatgpt",
                    "reason=run_daily_decision_chain_v2_v67_6_missing_board_self_heal",
                    f"triggered_at={generated}",
                    f"nonce=daily-self-heal-{day.replace('-', '')}-{generated[-8:].replace(':', '')}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    row = {
        "target_date": day,
        "generated_at": generated,
        "self_heal_status": status,
        "daily_board_exists": str(exists).lower(),
        "daily_board_rows": str(rows),
        "current_trigger_date": trigger_date,
        "trigger_action": action,
        "reason": reason,
        "next_action": next_action,
        "auto_apply": "NO",
        "production_change": "NO",
    }
    write_report(day, tz, row)
    print("=== VSIGMA DAILY CHAIN SELF-HEAL ROUTER ===")
    print(f"self_heal_status={status}")
    print(f"daily_board_exists={exists}")
    print(f"daily_board_rows={rows}")
    print(f"current_trigger_date={trigger_date}")
    print(f"trigger_action={action}")
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
