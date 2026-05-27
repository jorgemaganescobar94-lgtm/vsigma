from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "component", "status", "severity", "detail",
    "action_required", "source_guard", "auto_apply", "production_change",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def exists_all(*paths: Path) -> bool:
    return all(p.exists() for p in paths)


def extract_count(text: str, key: str) -> str:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def add(rows: list[dict[str, str]], day: str, generated_at: str, component: str, status: str, severity: str, detail: str, action: str) -> None:
    rows.append({
        "target_date": day,
        "generated_at": generated_at,
        "component": component,
        "status": status,
        "severity": severity,
        "detail": detail,
        "action_required": action,
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    })


def build(day: str, tz: str) -> list[dict[str, str]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = PROCESSED / "today" / day
    gov = PROCESSED / "governance"
    rows: list[dict[str, str]] = []

    board_md = folder / "vsigma_daily_execution_board.md"
    board_csv = folder / "vsigma_daily_execution_board.csv"
    board_text = read_text(board_md)
    if exists_all(board_md, board_csv):
        rows_on_board = extract_count(board_text, "rows_on_board")
        decision_counts = extract_count(board_text, "final_decision_counts")
        live_count = board_text.count("LIVE_ONLY") + board_text.count("READY_LOW_STAKE_REVIEW")
        severity = "WARN" if live_count else "OK"
        action = "REVIEW_BOARD" if live_count else "NO"
        add(rows, day, generated_at, "daily_execution_board", "OK", severity, f"rows={rows_on_board}; decisions={decision_counts}", action)
    else:
        add(rows, day, generated_at, "daily_execution_board", "MISSING", "BROKEN", "vsigma_daily_execution_board.md/csv missing", "RUN_DAILY_DECISION_CHAIN_V2")

    pre_md = folder / "vsigma_prelock_live_recheck.md"
    pre_csv = folder / "vsigma_prelock_live_recheck.csv"
    pre_text = read_text(pre_md)
    if exists_all(pre_md, pre_csv):
        counts = extract_count(pre_text, "recheck_decision_counts")
        active = pre_text.count("READY_LOW_STAKE_REVIEW") + pre_text.count("LIVE_ONLY_WAIT_TRIGGER") + pre_text.count("LIVE_RECHECK_ONLY")
        severity = "WARN" if active else "OK"
        action = "REVIEW_PRELOCK_LIVE" if active else "NO"
        add(rows, day, generated_at, "prelock_live_recheck", "OK", severity, f"decisions={counts}", action)
    else:
        add(rows, day, generated_at, "prelock_live_recheck", "MISSING", "WARN", "prelock/live report missing", "RUN_PRELOCK_RECHECK")

    refresh_md = folder / "vsigma_dated_post_match_results_refresh.md"
    refresh_text = read_text(refresh_md)
    if refresh_md.exists():
        if "REFRESH_SKIPPED_NO_API_CREDENTIALS" in refresh_text:
            add(rows, day, generated_at, "postmatch_results_refresh", "API_CREDENTIALS_MISSING", "BROKEN", "API key not available to workflow", "FIX_GITHUB_SECRET")
        elif "STATS_FETCHED" in refresh_text or "status_counts" in refresh_text:
            add(rows, day, generated_at, "postmatch_results_refresh", "OK", "OK", extract_count(refresh_text, "status_counts"), "NO")
        else:
            add(rows, day, generated_at, "postmatch_results_refresh", "UNKNOWN", "WARN", "refresh file exists but no clear status", "CHECK_REFRESH_REPORT")
    else:
        add(rows, day, generated_at, "postmatch_results_refresh", "WAITING_OR_NOT_RUN", "INFO", "postmatch refresh not present yet", "NO_IF_MATCHES_NOT_FINISHED")

    actuals_md = folder / "vsigma_post_match_stat_actuals.md"
    actuals_text = read_text(actuals_md)
    if actuals_md.exists():
        add(rows, day, generated_at, "postmatch_stat_actuals", "OK", "OK", f"rows_final={extract_count(actuals_text, 'rows_final')}", "NO")
    else:
        add(rows, day, generated_at, "postmatch_stat_actuals", "WAITING_OR_NOT_RUN", "INFO", "actuals report not present yet", "NO_IF_MATCHES_NOT_FINISHED")

    cal_md = folder / "vsigma_match_stat_forecast_calibration.md"
    cal_text = read_text(cal_md)
    if cal_md.exists():
        detail = f"detail_rows={extract_count(cal_text, 'detail_rows')}; statuses={extract_count(cal_text, 'calibration_status_counts')}"
        add(rows, day, generated_at, "forecast_calibration", "OK", "OK", detail, "NO")
    else:
        add(rows, day, generated_at, "forecast_calibration", "WAITING_OR_NOT_RUN", "INFO", "calibration report not present yet", "NO_IF_MATCHES_NOT_FINISHED")

    ledger = PROCESSED / "ledger" / "vsigma_stat_calibration_memory.csv"
    if ledger.exists():
        add(rows, day, generated_at, "calibration_memory_ledger", "OK", "OK", "global ledger exists", "NO")
    else:
        add(rows, day, generated_at, "calibration_memory_ledger", "MISSING", "WARN", "memory ledger missing", "RUN_POSTMATCH_LEARNING")

    workflows = {
        "daily_workflow_v2": "vsigma_daily_decision_chain_v2.yml active externally",
        "prelock_workflow": "vsigma_prelock_live_recheck.yml expected active",
        "postmatch_workflow": "vsigma_full_post_match_learning_chain.yml expected active",
    }
    for name, detail in workflows.items():
        add(rows, day, generated_at, name, "CONFIG_EXPECTED", "INFO", detail, "CHECK_GH_WORKFLOW_LIST_IF_NEEDED")

    return rows


def overall(rows: list[dict[str, str]]) -> str:
    if any(r["severity"] == "BROKEN" for r in rows):
        return "BROKEN"
    if any(r["severity"] == "WARN" for r in rows):
        return "ATTENTION"
    return "OK"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def md(day: str, rows: list[dict[str, str]]) -> str:
    sev = Counter(r["severity"] for r in rows)
    status = Counter(r["status"] for r in rows)
    lines = [
        f"# vSIGMA Automation Health Monitor - {day}",
        "",
        "## Summary",
        f"- system_status: {overall(rows)}",
        f"- components_checked: {len(rows)}",
        f"- severity_counts: {'; '.join(f'{k}={v}' for k, v in sev.items()) if sev else 'none'}",
        f"- status_counts: {'; '.join(f'{k}={v}' for k, v in status.items()) if status else 'none'}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Component Rows",
    ]
    for r in rows:
        lines.append(f"- {r['component']} | status={r['status']} | severity={r['severity']} | action={r['action_required']} | detail={r['detail']}")
    lines += [
        "",
        "## Guardrails",
        "- Health monitor does not execute bets or change production behavior.",
        "- WARN means review; BROKEN means a workflow/input needs fixing.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_automation_health.csv", rows)
        (base / "vsigma_automation_health.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA AUTOMATION HEALTH ===")
    print(f"system_status={overall(rows)}")
    print(f"components_checked={len(rows)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
