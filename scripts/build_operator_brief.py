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
ACTIVE_RECHECK = {"READY_LOW_STAKE_REVIEW"}
WAITING_RECHECK = {"LIVE_ONLY_WAIT_TRIGGER", "LIVE_RECHECK_ONLY"}
WATCH_BOARD = {"NO_BET_OR_WATCH", "STAT_WATCH_ONLY", "LIVE_ONLY"}
NO_BET_BOARD = {"NO_BET", "CANCELLED_NO_BET"}


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


def clean_value(s: str, limit: int = 160) -> str:
    s = str(s or "").strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) > limit:
        return s[: max(0, limit - 1)].rstrip() + "…"
    return s


def nz(*values: object, default: str = "", limit: int = 160) -> str:
    for value in values:
        s = clean_value(str(value or ""), limit=limit)
        if s and s.lower() not in {"none", "nan", "unknown"}:
            return s
    return default


def meta(text: str, key: str) -> str:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def grep(text: str, keys: list[str], limit: int = 12) -> list[str]:
    out = []
    seen = set()
    for line in text.splitlines():
        s = clean_line(line)
        if not s or not any(k in s for k in keys):
            continue
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= limit:
            break
    return out


def fid(row: dict[str, str]) -> str:
    return str(row.get("fixture_id", "")).replace(".0", "").strip()


def row_key(row: dict[str, str]) -> str:
    return fid(row) or "|".join(
        [
            nz(row.get("home_team")),
            nz(row.get("away_team")),
            nz(row.get("primary_market"), row.get("market")),
        ]
    )


def unique_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        key = row_key(row)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def teams(row: dict[str, str]) -> str:
    return f"{nz(row.get('home_team'), default='UNKNOWN_HOME')} vs {nz(row.get('away_team'), default='UNKNOWN_AWAY')}"


def add(rows: list[dict[str, str]], day: str, generated: str, section: str, status: str, detail: str, action: str) -> None:
    rows.append({"target_date": day, "generated_at": generated, "section": section, "status": status, "detail": detail, "next_action": action})


def fmt_review_row(row: dict[str, str], live_row: dict[str, str] | None = None) -> str:
    live_row = live_row or {}
    rank = nz(row.get("rank"), row.get("board_rank"), live_row.get("rank"))
    prefix = f"#{rank} | " if rank else ""
    decision = nz(row.get("recheck_decision"), row.get("base_decision"), live_row.get("recheck_decision"))
    market = nz(row.get("primary_market"), row.get("market"), live_row.get("market"))
    window = nz(live_row.get("window_status"), default="UNKNOWN")
    live_decision = nz(live_row.get("live_trigger_decision"), default="UNKNOWN")
    score = nz(live_row.get("score"))
    elapsed = nz(live_row.get("elapsed"))
    status = nz(live_row.get("match_status"))
    reason = nz(live_row.get("reason"), row.get("operator_note"), limit=90)

    parts = [
        f"{prefix}{decision}",
        teams(row),
        f"market={market}" if market else "",
        f"window={window}",
        f"live={live_decision}",
        f"match={status}" if status else "",
        f"elapsed={elapsed}" if elapsed else "",
        f"score={score}" if score else "",
        f"reason={reason}" if reason else "",
    ]
    return " | ".join(p for p in parts if p)


def fmt_board_row(row: dict[str, str]) -> str:
    rank = nz(row.get("board_rank"), row.get("rank"))
    prefix = f"#{rank} | " if rank else ""
    decision = nz(row.get("final_decision"), row.get("recheck_decision"), row.get("base_decision"))
    market = nz(row.get("primary_market"), row.get("market"))
    secondary = nz(row.get("secondary_market"))
    conf = nz(row.get("forecast_confidence"))
    score = nz(row.get("translation_score"))
    bucket = nz(row.get("board_bucket"))
    live = nz(row.get("live_trigger"), limit=95)
    cancel = nz(row.get("cancel_trigger"), row.get("operator_note"), limit=95)

    parts = [
        f"{prefix}{decision}",
        teams(row),
        f"market={market}" if market else "",
        f"alt={secondary}" if secondary else "",
        f"bucket={bucket}" if bucket else "",
        f"conf={conf}" if conf else "",
        f"score={score}" if score else "",
        f"live={live}" if live else "",
        f"cancel={cancel}" if cancel else "",
    ]
    return " | ".join(p for p in parts if p)


def classify(
    prelock_rows: list[dict[str, str]],
    live_rows: list[dict[str, str]],
    health_status: str,
    health_requires_review: bool,
) -> tuple[str, str, list[str], list[str], list[str], set[str]]:
    live_by_id = {fid(r): r for r in unique_rows(live_rows) if fid(r)}
    active: list[str] = []
    waiting: list[str] = []
    closed: list[str] = []
    used_ids: set[str] = set()
    confirmed = False

    for r in unique_rows(prelock_rows):
        decision = r.get("recheck_decision", "")
        if decision not in (ACTIVE_RECHECK | WAITING_RECHECK):
            continue

        key = row_key(r)
        lr = live_by_id.get(fid(r), {})
        ldec = lr.get("live_trigger_decision", "")
        win = lr.get("window_status", "")

        if ldec == "LIVE_TRIGGER_CONFIRMED":
            confirmed = True
            active.append(fmt_review_row(r, lr))
            used_ids.add(key)
        elif win in CLOSED or ldec in CLOSED:
            closed.append(fmt_review_row(r, lr))
            used_ids.add(key)
        elif decision in ACTIVE_RECHECK:
            active.append(fmt_review_row(r, lr))
            used_ids.add(key)
        elif decision in WAITING_RECHECK:
            waiting.append(fmt_review_row(r, lr))
            used_ids.add(key)

    if health_status == "BROKEN":
        return "BROKEN", "Fix missing/broken workflow input before using any market signal.", active, waiting, closed, used_ids
    if confirmed:
        return "ACTION_REVIEW_NOW", "Review LIVE_TRIGGER_CONFIRMED manually; no automatic execution.", active, waiting, closed, used_ids
    if active:
        return "PRELOCK_REVIEW", "Review active low-stake candidates only if price/prelock/live still supports thesis.", active, waiting, closed, used_ids
    if waiting:
        return "WAIT_LIVE_WINDOW", "Wait for useful live window and rerun live trigger validator.", active, waiting, closed, used_ids
    if closed:
        return "CLOSED_OR_WINDOW_MISSED", "No active candidate; previous signals are finished or outside useful window.", active, waiting, closed, used_ids
    if health_status == "ATTENTION" and health_requires_review:
        return "REVIEW", "Open health/board/recheck summaries; no automatic action.", active, waiting, closed, used_ids
    return "OK", "No operator action required.", active, waiting, closed, used_ids


def health_requires_operator_review(health_text: str, issue_text: str) -> bool:
    """Return True only for actionable system faults, not routine WARN/ATTENTION text.

    The health markdown contains explanatory guardrails such as "BROKEN means...".
    Scanning the whole document with substring tokens makes those guardrails look
    actionable. This function therefore inspects only structured component rows.
    """
    issue_severity = meta(issue_text, "severity").upper()
    if issue_severity in {"BROKEN", "CRITICAL", "ERROR"}:
        return True

    fault_statuses = {"BROKEN", "FAILED", "ERROR", "MISSING"}
    fault_severities = {"CRITICAL", "ERROR"}
    fault_actions = {"FIX", "REPAIR", "RERUN_REQUIRED"}

    for line in health_text.splitlines():
        s = clean_line(line)
        if "severity=" not in s or "status=" not in s or "|" not in s:
            continue

        fields: dict[str, str] = {}
        for part in s.split("|"):
            if "=" not in part:
                continue
            key, value = part.strip().split("=", 1)
            fields[key.strip().lower()] = value.strip().upper()

        status = fields.get("status", "")
        severity = fields.get("severity", "")
        action = fields.get("action", "")

        if status in fault_statuses:
            return True
        if severity in fault_severities:
            return True
        if any(token in action for token in fault_actions):
            return True

    return False


def operator_action_level(op_status: str, active: list[str], waiting: list[str], watch_only: list[str]) -> str:
    """First-read operator priority, independent from diagnostic health noise."""
    if op_status == "BROKEN":
        return "BROKEN"
    if op_status in {"ACTION_REVIEW_NOW", "PRELOCK_REVIEW", "REVIEW"} or active:
        return "REVIEW_NOW"
    if op_status == "WAIT_LIVE_WINDOW" or waiting:
        return "LIVE"
    if watch_only:
        return "WATCH"
    return "NONE"


def operator_sanity_check(
    op_status: str,
    action_level: str,
    active: list[str],
    waiting: list[str],
    closed: list[str],
    watch_only: list[str],
    no_bet: list[str],
) -> tuple[str, str]:
    """Detect impossible status/count combinations before the brief is trusted."""
    errors: list[str] = []

    if op_status == "OK" and (active or waiting or closed):
        errors.append("OK cannot have active/waiting/closed candidates")
    if op_status == "WAIT_LIVE_WINDOW" and not waiting:
        errors.append("WAIT_LIVE_WINDOW requires waiting candidates")
    if op_status == "PRELOCK_REVIEW" and not active:
        errors.append("PRELOCK_REVIEW requires active candidates")
    if op_status == "ACTION_REVIEW_NOW" and not active:
        errors.append("ACTION_REVIEW_NOW requires active candidates")
    if op_status == "CLOSED_OR_WINDOW_MISSED" and not closed:
        errors.append("CLOSED_OR_WINDOW_MISSED requires closed candidates")
    if action_level == "BROKEN" and op_status != "BROKEN":
        errors.append("BROKEN action level requires BROKEN operator status")
    if action_level == "REVIEW_NOW" and not (active or op_status in {"ACTION_REVIEW_NOW", "PRELOCK_REVIEW", "REVIEW"}):
        errors.append("REVIEW_NOW requires active/review status")
    if action_level == "LIVE" and not (waiting or op_status == "WAIT_LIVE_WINDOW"):
        errors.append("LIVE action level requires waiting live window")
    if action_level == "WATCH" and (active or waiting):
        errors.append("WATCH cannot coexist with active/waiting candidates")
    if action_level == "NONE" and (active or waiting or watch_only):
        errors.append("NONE cannot coexist with active/waiting/watch candidates")

    if errors:
        return "FAIL", "; ".join(errors)

    if action_level == "WATCH":
        return "PASS", f"watch_only={len(watch_only)}; no official action; no active/live review"
    if action_level == "NONE":
        return "PASS", f"no active/live/watch action; no_bet={len(no_bet)}; closed={len(closed)}"
    if action_level == "LIVE":
        return "PASS", f"waiting_live_window={len(waiting)}; manual live validator rerun required"
    if action_level == "REVIEW_NOW":
        return "PASS", f"active_review={len(active)}; manual review required; no auto execution"
    return "PASS", "broken-state routing is explicit"


def compact_risk_label(action_level: str, sanity_status: str, health_status: str, alert_notify_required: str) -> str:
    if sanity_status == "FAIL" or action_level == "BROKEN" or health_status == "BROKEN":
        return "HIGH"
    if action_level == "REVIEW_NOW":
        return "HIGH"
    if action_level == "LIVE":
        return "MEDIUM"
    if action_level == "WATCH" and alert_notify_required.lower() == "true":
        return "LOW_ALERT"
    if action_level == "WATCH":
        return "LOW"
    return "NONE"


def compact_final_decision(action_level: str, sanity_status: str) -> str:
    if sanity_status == "FAIL":
        return "STOP_SANITY_FAIL"
    return {
        "BROKEN": "SYSTEM_FIX_REQUIRED",
        "REVIEW_NOW": "MANUAL_REVIEW_REQUIRED",
        "LIVE": "WAIT_LIVE_WINDOW",
        "WATCH": "WATCH_ONLY_NO_STAKE",
        "NONE": "NO_OPERATOR_ACTION",
    }.get(action_level, "UNKNOWN")


def compact_reason(action_level: str, active: list[str], waiting: list[str], watch_only: list[str], no_bet: list[str]) -> str:
    if action_level == "BROKEN":
        return "system fault blocks market usage"
    if action_level == "REVIEW_NOW":
        return f"{len(active)} active manual-review candidate(s); no automatic execution"
    if action_level == "LIVE":
        return f"{len(waiting)} candidate(s) waiting for live validation window"
    if action_level == "WATCH":
        return f"{len(watch_only)} watch-only item(s); official stake remains blocked"
    return f"no active/live/watch action; no_bet={len(no_bet)}"


def compact_top_summary_rows(
    action_level: str,
    sanity_status: str,
    sanity_detail: str,
    risk_label: str,
    final_decision: str,
    reason: str,
    active: list[str],
    waiting: list[str],
    closed: list[str],
    watch_only: list[str],
    no_bet: list[str],
) -> list[tuple[str, str, str]]:
    counts = f"active={len(active)}; live={len(waiting)}; closed={len(closed)}; watch={len(watch_only)}; no_bet={len(no_bet)}"
    return [
        ("Action", action_level, "First-read operator priority"),
        ("Risk", risk_label, "Operational risk after sanity + health gate"),
        ("Counts", counts, "Candidate distribution"),
        ("Reason", reason, "Why this action level was selected"),
        ("Final", final_decision, f"sanity={sanity_status}; {sanity_detail}"),
    ]


def split_board_rows(board_rows: list[dict[str, str]], used_ids: set[str]) -> tuple[list[str], list[str]]:
    watch: list[str] = []
    no_bet: list[str] = []

    for row in unique_rows(board_rows):
        key = row_key(row)
        if key in used_ids:
            continue

        decision = nz(row.get("final_decision"), row.get("recheck_decision"), row.get("base_decision"))
        line = fmt_board_row(row)
        if decision in WATCH_BOARD:
            watch.append(line)
        elif decision in NO_BET_BOARD:
            no_bet.append(line)

    return watch, no_bet


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
    board_rows = read_csv(folder / "vsigma_daily_execution_board.csv")
    prelock_rows = read_csv(folder / "vsigma_prelock_live_recheck.csv")
    live_rows = read_csv(folder / "vsigma_live_trigger_validator.csv")

    hs = meta(health, "system_status")
    alert_notify_required = meta(issue, "notify_required")
    requires_review = health_requires_operator_review(health, issue)
    op_status, op_action, active, waiting, closed, used_ids = classify(prelock_rows, live_rows, hs, requires_review)
    watch_only, no_bet = split_board_rows(board_rows, used_ids)
    action_level = operator_action_level(op_status, active, waiting, watch_only)
    sanity_status, sanity_detail = operator_sanity_check(op_status, action_level, active, waiting, closed, watch_only, no_bet)
    risk_label = compact_risk_label(action_level, sanity_status, hs, alert_notify_required)
    final_decision = compact_final_decision(action_level, sanity_status)
    reason = compact_reason(action_level, active, waiting, watch_only, no_bet)
    compact_rows = compact_top_summary_rows(
        action_level,
        sanity_status,
        sanity_detail,
        risk_label,
        final_decision,
        reason,
        active,
        waiting,
        closed,
        watch_only,
        no_bet,
    )

    rows: list[dict[str, str]] = []
    add(rows, day, generated, "operator_status", op_status, f"health={hs}; active={len(active)}; waiting={len(waiting)}; closed={len(closed)}; watch={len(watch_only)}; no_bet={len(no_bet)}", op_action)
    add(rows, day, generated, "operator_action_level", action_level, f"sanity={sanity_status}; {sanity_detail}", "Use action_level as the first-read operator priority.")
    add(rows, day, generated, "operator_sanity_check", sanity_status, sanity_detail, "If FAIL, inspect CSV/MD mismatch before using the brief.")
    add(rows, day, generated, "operator_compact_summary", final_decision, f"action_level={action_level}; risk={risk_label}; reason={reason}", "Read this row first for the final operator decision.")
    add(rows, day, generated, "daily_board", meta(board, "final_decision_counts"), f"rows={meta(board, 'rows_on_board')}", "Review only candidates still active after live-window override.")
    add(rows, day, generated, "prelock_live", meta(prelock, "recheck_decision_counts"), f"rows={meta(prelock, 'rows_rechecked')}", "Use recheck state with live validator freshness override.")
    add(rows, day, generated, "live_trigger", meta(live, "live_trigger_counts"), f"windows={meta(live, 'window_counts')}", "Only LIVE_TRIGGER_CONFIRMED can justify manual live review.")
    add(rows, day, generated, "issue_alert", meta(issue, "severity"), f"required={meta(issue, 'required')}; notify={alert_notify_required}", "Issue alert is informational; no auto action.")
    add(rows, day, generated, "postmatch_learning", meta(cal, "calibration_status_counts"), f"actual_rows={meta(post, 'rows_final')}; detail_rows={meta(cal, 'detail_rows')}", "Use learning only after sufficient sample.")

    live_lines = grep(live, ["window=", "LIVE_TRIGGER", "TOO_EARLY", "TOO_LATE", "MATCH_FINISHED"], 16)
    calibration_lines = grep(cal, ["MODEL_OVER_ESTIMATING", "MODEL_UNDER_ESTIMATING", "CALIBRATION_OK", "PATCH_CANDIDATE"], 12)

    md = [
        f"# vSIGMA Daily Operator Brief - {day}", "",
        "## Compact Top Summary",
        "| Field | Value | Meaning |",
        "|---|---|---|",
    ]
    md += [f"| {field} | {value} | {meaning} |" for field, value, meaning in compact_rows]
    md += [
        "",
        "## Executive Summary",
        f"- action_level: {action_level}",
        f"- compact_final_decision: {final_decision}",
        f"- risk_label: {risk_label}",
        f"- sanity_check: {sanity_status} | {sanity_detail}",
        f"- operator_status: {op_status}",
        f"- primary_next_action: {op_action}",
        f"- health_status: {hs}",
        f"- active_candidates: {len(active)}",
        f"- waiting_live_window: {len(waiting)}",
        f"- closed_or_missed: {len(closed)}",
        f"- watch_only: {len(watch_only)}",
        f"- no_bet: {len(no_bet)}",
        f"- board_decisions: {meta(board, 'final_decision_counts')}",
        f"- recheck_decisions: {meta(prelock, 'recheck_decision_counts')}",
        f"- live_triggers: {meta(live, 'live_trigger_counts')}",
        f"- alert_notify_required: {alert_notify_required}",
        "- auto_apply: NO", "- production_change: NO", "",
        "## Operator Priority",
        f"- ACTION_LEVEL={action_level}",
        f"- RISK_LABEL={risk_label}",
        f"- FINAL_DECISION={final_decision}",
        f"- SANITY_CHECK={sanity_status}",
        f"- SANITY_DETAIL={sanity_detail}",
        f"- WINDOWS_READ=UTF8 | Get-Content {folder / 'vsigma_operator_brief.md'} -Encoding UTF8",
        "",
        "## Active Review",
    ]
    md += [f"- {x}" for x in active] if active else ["- none"]
    md += ["", "## Waiting Live Window"]
    md += [f"- {x}" for x in waiting] if waiting else ["- none"]
    md += ["", "## Closed / Window Missed"]
    md += [f"- {x}" for x in closed] if closed else ["- none"]
    md += ["", "## Watch Only"]
    md += [f"- {x}" for x in watch_only] if watch_only else ["- none"]
    md += ["", "## No Bet"]
    md += [f"- {x}" for x in no_bet] if no_bet else ["- none"]
    md += ["", "## Live Trigger Status"]
    md += [f"- {x}" for x in live_lines] if live_lines else ["- no live trigger report or no live candidates"]
    md += ["", "## Learning / Calibration"]
    md += [f"- {x}" for x in calibration_lines] if calibration_lines else ["- no calibration signal"]
    md += [
        "",
        "## Key Files",
        f"- {folder / 'vsigma_daily_execution_board.md'}",
        f"- {folder / 'vsigma_prelock_live_recheck.md'}",
        f"- {folder / 'vsigma_live_trigger_validator.md'}",
        f"- {folder / 'vsigma_automation_health.md'}",
        f"- {folder / 'vsigma_issue_alert_status.md'}",
        "",
        "## Guardrails",
        "- Brief is diagnostic only; it does not execute bets.",
        "- Manual review remains mandatory for every market.",
        "- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.",
    ]
    return rows, "\n".join(md) + "\n"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, brief = build(day, tz)
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write_csv(base / "vsigma_operator_brief.csv", rows)
        write(base / "vsigma_operator_brief.md", brief)

    status = rows[0]["status"] if rows else "UNKNOWN"
    action_level = next((r["status"] for r in rows if r.get("section") == "operator_action_level"), "UNKNOWN")
    sanity = next((r["status"] for r in rows if r.get("section") == "operator_sanity_check"), "UNKNOWN")
    final_decision = next((r["status"] for r in rows if r.get("section") == "operator_compact_summary"), "UNKNOWN")
    print(f"operator_status={status}; action_level={action_level}; sanity_check={sanity}; final_decision={final_decision}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
