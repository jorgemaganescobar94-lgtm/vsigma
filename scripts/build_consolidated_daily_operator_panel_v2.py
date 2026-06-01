from __future__ import annotations

import argparse
from datetime import date

import build_consolidated_daily_operator_panel as panel


def safe_operator_summary(operator_text: str, health_text: str, board_rows: list[dict[str, str]], prelock_rows: list[dict[str, str]], live_rows: list[dict[str, str]]):
    action = panel.meta(operator_text, "action_level") if operator_text else "UNAVAILABLE"
    final = panel.meta(operator_text, "compact_final_decision") if operator_text else "UNAVAILABLE"
    risk = panel.meta(operator_text, "risk_label") if operator_text else "UNAVAILABLE"
    health = panel.meta(health_text, "system_status") if health_text else "UNKNOWN"

    if not board_rows:
        if prelock_rows or live_rows or operator_text:
            status = "PARTIAL_OUTPUTS"
            next_action = "Daily execution board is missing; do not use operator/prelock/live outputs as pick permission. Run daily chain first."
        else:
            status = "WAIT_DAILY_CHAIN"
            next_action = "Run daily decision chain before using any market signal."
    elif action == "UNAVAILABLE":
        status = "PANEL_ONLY"
        next_action = "Operator brief missing; panel summarizes available files only."
    elif action == "BROKEN" or final == "SYSTEM_FIX_REQUIRED" or health == "BROKEN":
        status = "BROKEN"
        next_action = "Fix workflow/input before market discussion."
    else:
        status = action
        next_action = "Follow operator brief and panel categories; no automatic execution."

    detail = f"action={action}; final={final}; risk={risk}; health={health}; board_rows={len(board_rows)}"
    lines = [
        f"- action_level: {action}",
        f"- compact_final_decision: {final}",
        f"- risk_label: {risk}",
        f"- health_status: {health}",
        f"- board_rows: {len(board_rows)}",
        f"- panel_status: {status}",
        f"- next_action: {next_action}",
    ]
    return status, detail, lines


def run(day: str, tz: str) -> None:
    panel.operator_summary = safe_operator_summary
    panel.run(date.fromisoformat(day).isoformat(), tz)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
