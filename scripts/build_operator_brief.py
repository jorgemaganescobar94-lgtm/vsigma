from __future__ import annotations

import argparse
import csv
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
FIELDS = ["target_date", "generated_at", "section", "status", "detail", "next_action"]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def meta(text: str, key: str) -> str:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def grep(text: str, keys: list[str], limit: int = 12) -> list[str]:
    out = []
    for line in text.splitlines():
        s = line.strip()
        if any(k in s for k in keys):
            out.append(s)
    return out[:limit]


def add(rows: list[dict[str, str]], day: str, generated: str, section: str, status: str, detail: str, action: str) -> None:
    rows.append({"target_date": day, "generated_at": generated, "section": section, "status": status, "detail": detail, "next_action": action})


def operator_status(health_status: str, combined: str) -> tuple[str, str]:
    if health_status == "BROKEN":
        return "BROKEN", "Fix missing/broken workflow input before using any market signal."
    if "LIVE_TRIGGER_CONFIRMED" in combined:
        return "ACTION_REVIEW_NOW", "Review live trigger confirmation manually; no automatic execution."
    if "READY_LOW_STAKE_REVIEW" in combined:
        return "PRELOCK_REVIEW", "Review low-stake candidates only if price/prelock/live still supports thesis."
    if "LIVE_ONLY_WAIT_TRIGGER" in combined or "TOO_EARLY" in combined:
        return "WAIT_LIVE_WINDOW", "Wait for useful live window and rerun live trigger validator."
    if health_status == "ATTENTION":
        return "REVIEW", "Open health/board/recheck summaries; no automatic action."
    return "OK", "No operator action required."


def build(day: str, tz: str) -> tuple[list[dict[str, str]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = ROOT / "today" / day
    health = read(folder / "vsigma_automation_health.md")
    board = read(folder / "vsigma_daily_execution_board.md")
    prelock = read(folder / "vsigma_prelock_live_recheck.md")
    live = read(folder / "vsigma_live_trigger_validator.md")
    issue = read(folder / "vsigma_issue_alert_status.md")
    cal = read(folder / "vsigma_match_stat_forecast_calibration.md")
    post = read(folder / "vsigma_post_match_stat_actuals.md")
    combined = "\n".join([health, board, prelock, live, issue, cal, post])

    hs = meta(health, "system_status")
    op_status, op_action = operator_status(hs, combined)
    rows: list[dict[str, str]] = []
    add(rows, day, generated, "operator_status", op_status, f"health={hs}", op_action)
    add(rows, day, generated, "daily_board", meta(board, "final_decision_counts"), f"rows={meta(board, 'rows_on_board')}", "Review only candidates marked PRELOCK_REVIEW_LOW_STAKE or LIVE_ONLY.")
    add(rows, day, generated, "prelock_live", meta(prelock, "recheck_decision_counts"), f"rows={meta(prelock, 'rows_rechecked')}", "Use recheck state before any manual review.")
    add(rows, day, generated, "live_trigger", meta(live, "live_trigger_counts"), f"windows={meta(live, 'window_counts')}", "Only LIVE_TRIGGER_CONFIRMED can justify manual live review.")
    add(rows, day, generated, "issue_alert", meta(issue, "severity"), f"required={meta(issue, 'required')}; notify={meta(issue, 'notify_required')}", "Issue alert is informational; no auto action.")
    add(rows, day, generated, "postmatch_learning", meta(cal, "calibration_status_counts"), f"actual_rows={meta(post, 'rows_final')}; detail_rows={meta(cal, 'detail_rows')}", "Use learning only after sufficient sample.")

    action_lines = grep(combined, ["LIVE_TRIGGER_CONFIRMED", "READY_LOW_STAKE_REVIEW", "LIVE_ONLY_WAIT_TRIGGER", "BROKEN"], 20)
    blocked_lines = grep(combined, ["CANCELLED_NO_BET", "NO_BET", "NO_BET_OR_WATCH"], 12)
    live_lines = grep(live, ["window=", "LIVE_TRIGGER", "TOO_EARLY", "TOO_LATE", "MATCH_FINISHED"], 16)
    calibration_lines = grep(cal, ["MODEL_OVER_ESTIMATING", "MODEL_UNDER_ESTIMATING", "CALIBRATION_OK", "PATCH_CANDIDATE"], 12)

    md = [
        f"# vSIGMA Daily Operator Brief - {day}", "",
        "## Executive Summary",
        f"- operator_status: {op_status}",
        f"- primary_next_action: {op_action}",
        f"- health_status: {hs}",
        f"- board_decisions: {meta(board, 'final_decision_counts')}",
        f"- recheck_decisions: {meta(prelock, 'recheck_decision_counts')}",
        f"- live_triggers: {meta(live, 'live_trigger_counts')}",
        f"- alert_notify_required: {meta(issue, 'notify_required')}",
        "- auto_apply: NO", "- production_change: NO", "",
        "## What To Review Now",
    ]
    md += [f"- {x}" for x in action_lines] if action_lines else ["- none"]
    md += ["", "## Live Trigger Status"]
    md += [f"- {x}" for x in live_lines] if live_lines else ["- no live trigger report or no live candidates"]
    md += ["", "## Blocked / Watch Only"]
    md += [f"- {x}" for x in blocked_lines] if blocked_lines else ["- none"]
    md += ["", "## Learning / Calibration"]
    md += [f"- {x}" for x in calibration_lines] if calibration_lines else ["- no calibration signal"]
    md += ["", "## Key Files", f"- {folder / 'vsigma_daily_execution_board.md'}", f"- {folder / 'vsigma_prelock_live_recheck.md'}", f"- {folder / 'vsigma_live_trigger_validator.md'}", f"- {folder / 'vsigma_automation_health.md'}", f"- {folder / 'vsigma_issue_alert_status.md'}", "", "## Guardrails", "- Brief is diagnostic only; it does not execute bets.", "- Manual review remains mandatory for every market."]
    return rows, "\n".join(md) + "\n"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, brief = build(day, tz)
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write_csv(base / "vsigma_operator_brief.csv", rows)
        write(base / "vsigma_operator_brief.md", brief)
    print(f"operator_status={rows[0]['status'] if rows else 'UNKNOWN'}")


def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--date", required=True); p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args(); run(a.date, a.timezone)


if __name__ == "__main__": main()
