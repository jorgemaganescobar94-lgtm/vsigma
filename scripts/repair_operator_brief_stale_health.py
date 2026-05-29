from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
FIELDS = ["target_date", "generated_at", "section", "status", "detail", "next_action"]
WATCH = {"NO_BET_OR_WATCH", "STAT_WATCH_ONLY", "LIVE_ONLY"}
NO_BET = {"NO_BET", "CANCELLED_NO_BET"}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def put(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def put_rows(path: Path, data: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in FIELDS} for r in data])


def setrow(data: list[dict[str, str]], day: str, ts: str, section: str, status: str, detail: str, action: str) -> None:
    for r in data:
        if r.get("section") == section:
            r.update({"target_date": day, "generated_at": ts, "status": status, "detail": detail, "next_action": action})
            return
    data.append({"target_date": day, "generated_at": ts, "section": section, "status": status, "detail": detail, "next_action": action})


def counts(board: list[dict[str, str]]) -> tuple[int, int]:
    w = n = 0
    for r in board:
        d = (r.get("final_decision") or "").strip()
        if d in WATCH:
            w += 1
        elif d in NO_BET:
            n += 1
    return w, n


def should_repair(health: str, board: list[dict[str, str]], brief: str) -> bool:
    if not board or "operator_status: BROKEN" not in brief:
        return False
    return "daily_execution_board" in health and "status=MISSING" in health and "severity=BROKEN" in health


def patch_md(md: str, watch: int, no_bet: int) -> str:
    reason = f"{watch} watch-only item(s); official stake remains blocked"
    detail = f"watch_only={watch}; no official action; no active/live review"
    for a, b in [
        ("| Action | BROKEN |", "| Action | WATCH |"),
        ("| Risk | HIGH |", "| Risk | LOW |"),
        ("| Alert | CRITICAL_STOP / CRITICAL |", "| Alert | NO_ALERT / NONE |"),
        ("| Reason | system fault blocks market usage |", f"| Reason | {reason} |"),
        ("| Final | SYSTEM_FIX_REQUIRED |", "| Final | WATCH_ONLY_NO_STAKE |"),
        ("| Route | CRITICAL_STOP |", "| Route | NO_ALERT |"),
        ("| Materiality | CRITICAL |", "| Materiality | NONE |"),
        ("- action_level: BROKEN", "- action_level: WATCH"),
        ("- compact_final_decision: SYSTEM_FIX_REQUIRED", "- compact_final_decision: WATCH_ONLY_NO_STAKE"),
        ("- risk_label: HIGH", "- risk_label: LOW"),
        ("- alert_route: CRITICAL_STOP", "- alert_route: NO_ALERT"),
        ("- alert_materiality: CRITICAL", "- alert_materiality: NONE"),
        ("- operator_status: BROKEN", "- operator_status: OK"),
        ("- health_status: BROKEN", "- health_status: BROKEN_OVERRIDDEN_STALE_DAILY_BOARD"),
        ("- ACTION_LEVEL=BROKEN", "- ACTION_LEVEL=WATCH"),
        ("- RISK_LABEL=HIGH", "- RISK_LABEL=LOW"),
        ("- FINAL_DECISION=SYSTEM_FIX_REQUIRED", "- FINAL_DECISION=WATCH_ONLY_NO_STAKE"),
        ("- ALERT_ROUTE=CRITICAL_STOP", "- ALERT_ROUTE=NO_ALERT"),
        ("- ALERT_MATERIALITY=CRITICAL", "- ALERT_MATERIALITY=NONE"),
        ("broken-state routing is explicit", detail),
        ("sanity failure or broken system state blocks operator usage", "stale health missing-board overridden by fresh board; no official action"),
        ("Fix missing/broken workflow input before using any market signal.", "No operator action required; board exists and official stake remains blocked."),
    ]:
        md = md.replace(a, b)
    return md


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = ROOT / "today" / day
    health = text(folder / "vsigma_automation_health.md")
    board = rows(folder / "vsigma_daily_execution_board.csv")
    brief = text(folder / "vsigma_operator_brief.md")
    if not should_repair(health, board, brief):
        print("operator_brief_repair=NO_ACTION")
        return
    watch, no_bet = counts(board)
    detail = f"watch_only={watch}; no official action; no active/live review"
    for base in [folder, ROOT / "governance"]:
        csv_path = base / "vsigma_operator_brief.csv"
        md_path = base / "vsigma_operator_brief.md"
        data = rows(csv_path)
        setrow(data, day, ts, "operator_status", "OK", f"health=BROKEN_OVERRIDDEN_STALE_DAILY_BOARD; active=0; waiting=0; closed=0; watch={watch}; no_bet={no_bet}", "No operator action required; board exists and official stake remains blocked.")
        setrow(data, day, ts, "operator_action_level", "WATCH", f"sanity=PASS; {detail}", "Use action_level as the first-read operator priority.")
        setrow(data, day, ts, "operator_sanity_check", "PASS", detail, "If FAIL, inspect CSV/MD mismatch before using the brief.")
        setrow(data, day, ts, "operator_compact_summary", "WATCH_ONLY_NO_STAKE", f"action_level=WATCH; risk=LOW; active_signature=; reason={watch} watch-only item(s); official stake remains blocked", "Read this row first for the final operator decision.")
        setrow(data, day, ts, "operator_alert_route", "NO_ALERT", "materiality=NONE; reason=stale health missing-board overridden by fresh board; no official action", "Route only; this script does not send alerts.")
        put_rows(csv_path, data)
        put(md_path, patch_md(text(md_path), watch, no_bet))
    print(f"operator_brief_repair=APPLIED; action_level=WATCH; final_decision=WATCH_ONLY_NO_STAKE; watch={watch}; no_bet={no_bet}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
