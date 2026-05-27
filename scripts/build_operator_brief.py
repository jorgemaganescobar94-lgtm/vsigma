from __future__ import annotations

import argparse
import csv
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
FIELDS = ["target_date", "generated_at", "section", "status", "detail", "next_action"]
CLOSED = {"MATCH_FINISHED", "TOO_LATE", "MATCH_FINISHED_OR_TOO_LATE"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def read_csv(p: Path) -> list[dict[str, str]]:
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def clean_line(s: str) -> str:
    s = s.strip()
    while s.startswith("-"):
        s = s[1:].strip()
    return s


def meta(text: str, key: str) -> str:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def grep(text: str, keys: list[str], limit: int = 12) -> list[str]:
    out = []
    for line in text.splitlines():
        s = clean_line(line)
        if s and any(k in s for k in keys):
            out.append(s)
    return out[:limit]


def fid(row: dict[str, str]) -> str:
    return str(row.get("fixture_id", "")).replace(".0", "").strip()


def add(rows: list[dict[str, str]], day: str, generated: str, section: str, status: str, detail: str, action: str) -> None:
    rows.append({"target_date": day, "generated_at": generated, "section": section, "status": status, "detail": detail, "next_action": action})


def classify(prelock_rows: list[dict[str, str]], live_rows: list[dict[str, str]], health_status: str) -> tuple[str, str, list[str], list[str], list[str]]:
    live_by_id = {fid(r): r for r in live_rows if fid(r)}
    active: list[str] = []
    waiting: list[str] = []
    closed: list[str] = []
    confirmed = False

    for r in prelock_rows:
        decision = r.get("recheck_decision", "")
        if decision not in {"READY_LOW_STAKE_REVIEW", "LIVE_ONLY_WAIT_TRIGGER", "LIVE_RECHECK_ONLY"}:
            continue
        lr = live_by_id.get(fid(r), {})
        ldec = lr.get("live_trigger_decision", "")
        win = lr.get("window_status", "")
        teams = f"{r.get('home_team','')} vs {r.get('away_team','')}"
        market = r.get("primary_market") or r.get("market") or ""
        desc = f"{decision} | {teams} | market={market} | window={win or 'UNKNOWN'} | live_decision={ldec or 'UNKNOWN'}"
        if ldec == "LIVE_TRIGGER_CONFIRMED":
            confirmed = True
            active.append(desc)
        elif win in CLOSED or ldec in CLOSED:
            closed.append(desc)
        elif decision == "READY_LOW_STAKE_REVIEW" and win not in CLOSED:
            active.append(desc)
        elif decision in {"LIVE_ONLY_WAIT_TRIGGER", "LIVE_RECHECK_ONLY"}:
            waiting.append(desc)

    if health_status == "BROKEN":
        return "BROKEN", "Fix missing/broken workflow input before using any market signal.", active, waiting, closed
    if confirmed:
        return "ACTION_REVIEW_NOW", "Review LIVE_TRIGGER_CONFIRMED manually; no automatic execution.", active, waiting, closed
    if active:
        return "PRELOCK_REVIEW", "Review active low-stake candidates only if price/prelock/live still supports thesis.", active, waiting, closed
    if waiting:
        return "WAIT_LIVE_WINDOW", "Wait for useful live window and rerun live trigger validator.", active, waiting, closed
    if closed:
        return "CLOSED_OR_WINDOW_MISSED", "No active candidate; previous signals are finished or outside useful window.", active, waiting, closed
    if health_status == "ATTENTION":
        return "REVIEW", "Open health/board/recheck summaries; no automatic action.", active, waiting, closed
    return "OK", "No operator action required.", active, waiting, closed


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
    prelock_rows = read_csv(folder / "vsigma_prelock_live_recheck.csv")
    live_rows = read_csv(folder / "vsigma_live_trigger_validator.csv")

    hs = meta(health, "system_status")
    op_status, op_action, active, waiting, closed = classify(prelock_rows, live_rows, hs)
    rows: list[dict[str, str]] = []
    add(rows, day, generated, "operator_status", op_status, f"health={hs}; active={len(active)}; waiting={len(waiting)}; closed={len(closed)}", op_action)
    add(rows, day, generated, "daily_board", meta(board, "final_decision_counts"), f"rows={meta(board, 'rows_on_board')}", "Review only candidates still active after live-window override.")
    add(rows, day, generated, "prelock_live", meta(prelock, "recheck_decision_counts"), f"rows={meta(prelock, 'rows_rechecked')}", "Use recheck state with live validator freshness override.")
    add(rows, day, generated, "live_trigger", meta(live, "live_trigger_counts"), f"windows={meta(live, 'window_counts')}", "Only LIVE_TRIGGER_CONFIRMED can justify manual live review.")
    add(rows, day, generated, "issue_alert", meta(issue, "severity"), f"required={meta(issue, 'required')}; notify={meta(issue, 'notify_required')}", "Issue alert is informational; no auto action.")
    add(rows, day, generated, "postmatch_learning", meta(cal, "calibration_status_counts"), f"actual_rows={meta(post, 'rows_final')}; detail_rows={meta(cal, 'detail_rows')}", "Use learning only after sufficient sample.")

    blocked_lines = grep(board + "\n" + prelock, ["CANCELLED_NO_BET", "NO_BET", "NO_BET_OR_WATCH"], 12)
    live_lines = grep(live, ["window=", "LIVE_TRIGGER", "TOO_EARLY", "TOO_LATE", "MATCH_FINISHED"], 16)
    calibration_lines = grep(cal, ["MODEL_OVER_ESTIMATING", "MODEL_UNDER_ESTIMATING", "CALIBRATION_OK", "PATCH_CANDIDATE"], 12)

    md = [
        f"# vSIGMA Daily Operator Brief - {day}", "",
        "## Executive Summary",
        f"- operator_status: {op_status}",
        f"- primary_next_action: {op_action}",
        f"- health_status: {hs}",
        f"- active_candidates: {len(active)}",
        f"- waiting_live_window: {len(waiting)}",
        f"- closed_or_missed: {len(closed)}",
        f"- board_decisions: {meta(board, 'final_decision_counts')}",
        f"- recheck_decisions: {meta(prelock, 'recheck_decision_counts')}",
        f"- live_triggers: {meta(live, 'live_trigger_counts')}",
        f"- alert_notify_required: {meta(issue, 'notify_required')}",
        "- auto_apply: NO", "- production_change: NO", "",
        "## Active Review Candidates",
    ]
    md += [f"- {x}" for x in active] if active else ["- none"]
    md += ["", "## Waiting Live Window"]
    md += [f"- {x}" for x in waiting] if waiting else ["- none"]
    md += ["", "## Closed / Window Missed"]
    md += [f"- {x}" for x in closed] if closed else ["- none"]
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
