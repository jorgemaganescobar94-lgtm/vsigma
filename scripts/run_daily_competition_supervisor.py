from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, TODAY_DIR, format_markdown_table, read_csv_lenient, stale_date_summary
    from run_daily_competition_controller import build_plan_and_status, next_action, parse_target_date
    from run_vsigma_healthcheck import run_healthcheck
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, TODAY_DIR, format_markdown_table, read_csv_lenient, stale_date_summary
    from scripts.run_daily_competition_controller import build_plan_and_status, next_action, parse_target_date
    from scripts.run_vsigma_healthcheck import run_healthcheck


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "automation_logs" / "supervisor"
SUPERVISOR_REPORT = "daily_supervisor_report.md"
SUPERVISOR_STATUS = "daily_supervisor_status.csv"
SUPERVISOR_LATEST = "daily_supervisor_latest.md"

CONTROLLER_SCRIPT = "scripts/run_daily_competition_controller.py"
MASTER_REPORT_SCRIPT = "scripts/build_daily_competition_master_report.py"

TASK_NAMES = [
    "vSIGMA PRE Daily",
    "vSIGMA PRELOCK Check",
    "vSIGMA POST Daily",
    "vSIGMA POST Backup Yesterday",
]


@dataclass
class CommandResult:
    label: str
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str
    log_path: Path

    @property
    def status(self) -> str:
        return "PASS" if self.exit_code == 0 else "FAILED"


def local_today(timezone_name: str) -> date:
    return datetime.now(ZoneInfo(timezone_name)).date()


def default_target_date(mode: str, timezone_name: str) -> str:
    today = local_today(timezone_name)
    if mode == "post-backup":
        return (today - timedelta(days=1)).isoformat()
    return today.isoformat()


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M%S")


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def supervisor_log_path(target_date: str, mode: str, suffix: str = "run") -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    clean_mode = mode.replace("-", "_")
    return LOG_DIR / f"{target_date}_{clean_mode}_{timestamp()}_{suffix}.log"


def run_command(label: str, command: list[str], target_date: str, mode: str) -> CommandResult:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, env=env)
    log_path = supervisor_log_path(target_date, mode, label)
    lines = [
        f"date={target_date}",
        f"mode={mode}",
        f"timestamp={datetime.now().isoformat()}",
        f"label={label}",
        f"command={' '.join(command)}",
        f"exit_code={completed.returncode}",
        "",
        "=== STDOUT ===",
        completed.stdout,
        "",
        "=== STDERR ===",
        completed.stderr,
        "",
    ]
    log_path.write_text("\n".join(lines), encoding="utf-8")
    return CommandResult(label, command, completed.returncode, completed.stdout, completed.stderr, log_path)


def controller_command(target_date: str, timezone_name: str, mode: str, window_minutes: int) -> list[str]:
    command = [
        sys.executable,
        CONTROLLER_SCRIPT,
        "--date",
        target_date,
        "--timezone",
        timezone_name,
        "--mode",
        mode,
        "--window-minutes",
        str(window_minutes),
    ]
    return command


def master_report_command(target_date: str, processed_dir: Path) -> list[str]:
    return [
        sys.executable,
        MASTER_REPORT_SCRIPT,
        "--date",
        target_date,
        "--processed-dir",
        str(processed_dir),
        "--snapshot-dir",
        str(snapshot_dir(processed_dir, target_date)),
    ]


def stale_warnings(processed_dir: Path, target_date: str) -> str:
    prelock = read_csv_lenient(snapshot_dir(processed_dir, target_date) / "vsigma_today_prelock_comparison.csv")
    if prelock.empty:
        prelock = read_csv_lenient(processed_dir / "vsigma_today_prelock_comparison.csv")
    if not prelock.empty:
        try:
            from daily_hardening import split_fresh_stale_rows
        except ModuleNotFoundError:
            from scripts.daily_hardening import split_fresh_stale_rows
        _fresh, stale = split_fresh_stale_rows(prelock, target_date, include_target_date=True)
        if not stale.empty:
            return f"STALE_PRELOCK_EXCLUDED: {stale_date_summary(stale, include_target_date=True)}"
    return "NONE"


def ledger_status(processed_dir: Path, target_date: str) -> str:
    ledger = read_csv_lenient(processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv")
    if ledger.empty or "target_date" not in ledger.columns:
        return "MISSING"
    day = ledger[ledger["target_date"].astype(str).eq(target_date)].copy()
    if day.empty:
        return "MISSING_FOR_DATE"
    if day.get("record_status", pd.Series(dtype=object)).astype(str).str.upper().isin(["SETTLED", "VOID"]).any():
        return "POST_UPDATED"
    if day.get("pipeline_stage", pd.Series(dtype=object)).astype(str).str.upper().eq("PRELOCK").any():
        return "PRELOCK_UPDATED"
    if day.get("pipeline_stage", pd.Series(dtype=object)).astype(str).str.upper().eq("PRE").any():
        return "PRE_UPDATED"
    return "AVAILABLE"


def task_status_summary() -> str:
    if os.name != "nt":
        return "TASK_STATUS_UNAVAILABLE_NON_WINDOWS"
    statuses: list[str] = []
    for task_name in TASK_NAMES:
        completed = subprocess.run(
            ["schtasks.exe", "/Query", "/TN", task_name, "/FO", "LIST"],
            capture_output=True,
            text=True,
            check=False,
        )
        statuses.append(f"{task_name}={'REGISTERED' if completed.returncode == 0 else 'NOT_REGISTERED'}")
    return "; ".join(statuses)


def status_row(
    target_date: str,
    mode: str,
    plan: pd.DataFrame,
    command_results: list[CommandResult],
    logs_path: Path,
    processed_dir: Path,
    outcome: str,
    detail: str,
    healthcheck_result: dict[str, object] | None = None,
) -> dict[str, object]:
    action, command = next_action(plan)
    healthcheck_result = healthcheck_result or {}
    return {
        "target_date": target_date,
        "mode": mode,
        "run_finished_at": datetime.now().isoformat(),
        "supervisor_status": outcome,
        "detail": detail,
        "commands_executed": len(command_results),
        "failed_commands": sum(result.exit_code != 0 for result in command_results),
        "next_recommended_action": action,
        "next_recommended_command": command,
        "logs_path": str(logs_path),
        "stale_warnings": stale_warnings(processed_dir, target_date),
        "ledger_update_status": ledger_status(processed_dir, target_date),
        "scheduled_automation_status": task_status_summary(),
        "healthcheck_status": str(healthcheck_result.get("global_status", "NOT_RUN_YET")),
        "healthcheck_report": str(healthcheck_result.get("snapshot_report_md", "")),
    }


def write_supervisor_outputs(
    target_date: str,
    mode: str,
    plan: pd.DataFrame,
    command_results: list[CommandResult],
    processed_dir: Path,
    outcome: str,
    detail: str,
    healthcheck_result: dict[str, object] | None = None,
) -> dict[str, Path]:
    snap = snapshot_dir(processed_dir, target_date)
    snap.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    row = status_row(target_date, mode, plan, command_results, LOG_DIR, processed_dir, outcome, detail, healthcheck_result)
    status_path = snap / SUPERVISOR_STATUS
    report_path = snap / SUPERVISOR_REPORT
    latest_path = processed_dir / SUPERVISOR_LATEST
    pd.DataFrame([row]).to_csv(status_path, index=False)
    commands_table = pd.DataFrame(
        [
            {
                "label": result.label,
                "exit_code": result.exit_code,
                "status": result.status,
                "log_path": str(result.log_path),
                "command": " ".join(result.command),
            }
            for result in command_results
        ]
    )
    lines = [
        f"# vSIGMA Daily Supervisor Report - {target_date}",
        "",
        f"- Mode run: {mode}",
        f"- Status: {outcome}",
        f"- Detail: {detail}",
        f"- Next recommended action: {row['next_recommended_action']}",
        f"- Next recommended command: `{row['next_recommended_command']}`",
        f"- Logs path: {LOG_DIR}",
        f"- Stale warnings: {row['stale_warnings']}",
        f"- Ledger update status: {row['ledger_update_status']}",
        f"- Scheduled automation status: {row['scheduled_automation_status']}",
        f"- Healthcheck status: {row['healthcheck_status']}",
        f"- Healthcheck report: {row['healthcheck_report'] or 'NOT_AVAILABLE'}",
        "",
        "## Commands Executed",
        format_markdown_table(commands_table, max_rows=20),
        "",
        "## Current Plan",
        format_markdown_table(plan, max_rows=50),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(report_path, latest_path)
    return {"report_md": report_path, "status_csv": status_path, "latest_md": latest_path}


def print_status(plan: pd.DataFrame, processed_dir: Path, target_date: str) -> None:
    action, command = next_action(plan)
    controller_status = snapshot_dir(processed_dir, target_date) / "daily_controller_status.md"
    print("\n=== VSIGMA DAILY SUPERVISOR STATUS ===")
    print(f"Date: {target_date}")
    print(f"Controller status: {controller_status if controller_status.exists() else 'NOT_AVAILABLE'}")
    print(f"Ledger: {ledger_status(processed_dir, target_date)}")
    print(f"Stale warnings: {stale_warnings(processed_dir, target_date)}")
    print(f"Next recommended action: {action}")
    print(f"Next recommended command: {command}")
    if not plan.empty:
        print("\nPlan:")
        print(plan.to_string(index=False))


def run_supervisor(
    target_date: str,
    timezone_name: str,
    mode: str,
    window_minutes: int = 90,
    processed_dir: Path = PROCESSED_DIR,
) -> dict[str, Path]:
    processed_dir.mkdir(parents=True, exist_ok=True)
    target_date = parse_target_date(target_date)
    command_results: list[CommandResult] = []
    healthcheck_result: dict[str, object] | None = None
    outcome = "PASS"
    detail = "NO_ACTION"

    if mode == "pre":
        command_results.append(run_command("controller_pre", controller_command(target_date, timezone_name, "pre", window_minutes), target_date, mode))
        detail = "PRE_RUN"
    elif mode == "post":
        command_results.append(run_command("controller_post", controller_command(target_date, timezone_name, "post", window_minutes), target_date, mode))
        detail = "POST_RUN"
    elif mode == "post-backup":
        command_results.append(run_command("controller_post_backup", controller_command(target_date, timezone_name, "post", window_minutes), target_date, mode))
        detail = "POST_BACKUP_RUN"
    elif mode == "prelock-check":
        plan, _paths, _state = build_plan_and_status(processed_dir, target_date, timezone_name, window_minutes)
        due = plan[plan.get("recommended_next_action", pd.Series(dtype=object)).astype(str).eq("RUN_PRELOCK_NOW")] if not plan.empty else pd.DataFrame()
        if due.empty:
            detail = "NO_PRELOCK_DUE"
        else:
            command_results.append(run_command("controller_prelock", controller_command(target_date, timezone_name, "prelock", window_minutes), target_date, mode))
            detail = "PRELOCK_RUN"
    elif mode == "status":
        detail = "STATUS_ONLY"
    elif mode == "full-cycle":
        command_results.append(run_command("controller_pre", controller_command(target_date, timezone_name, "pre", window_minutes), target_date, mode))
        detail = "FULL_CYCLE_PRE_RUN_PLAN_ONLY"
    else:
        raise ValueError(f"Unsupported supervisor mode: {mode}")

    if any(result.exit_code != 0 for result in command_results):
        outcome = "FAILED"

    plan, _paths, _state = build_plan_and_status(processed_dir, target_date, timezone_name, window_minutes)
    outputs = write_supervisor_outputs(target_date, mode, plan, command_results, processed_dir, outcome, detail)
    if mode in {"pre", "prelock-check", "post", "post-backup", "full-cycle", "status"}:
        master = run_command("master_report", master_report_command(target_date, processed_dir), target_date, mode)
        command_results.append(master)
        if master.exit_code != 0:
            outcome = "FAILED"

    try:
        healthcheck_result = run_healthcheck(target_date, timezone_name, "quick", processed_dir=processed_dir)
    except Exception as exc:  # pragma: no cover - defensive report path for scheduled runs
        outcome = "FAILED"
        healthcheck_result = {"global_status": "BROKEN", "snapshot_report_md": "", "error": str(exc)}

    outputs = write_supervisor_outputs(target_date, mode, plan, command_results, processed_dir, outcome, detail, healthcheck_result)
    print_status(plan, processed_dir, target_date)
    print(f"Supervisor report: {outputs['report_md']}")
    print(f"Supervisor status CSV: {outputs['status_csv']}")
    if mode == "full-cycle":
        action, command = next_action(plan)
        print("\nRecommended scheduled command/time:")
        print(f"PRE: run_vsigma_supervisor.ps1 -Mode pre -DaysOffset 0")
        print(f"PRELOCK: run_vsigma_supervisor.ps1 -Mode prelock-check -DaysOffset 0")
        print(f"POST: run_vsigma_supervisor.ps1 -Mode post -DaysOffset 0")
        print(f"POST BACKUP: run_vsigma_supervisor.ps1 -Mode post-backup -DaysOffset -1")
        print(f"Current next action: {action}")
        print(f"Current next command: {command}")
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vSIGMA daily supervisor for scheduled automation.")
    parser.add_argument("--date", default=None)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument(
        "--mode",
        choices=["pre", "prelock-check", "post", "post-backup", "status", "full-cycle"],
        default="status",
    )
    parser.add_argument("--window-minutes", type=int, default=90)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = parse_target_date(args.date) if args.date else default_target_date(args.mode, args.timezone)
    run_supervisor(target_date, args.timezone, args.mode, args.window_minutes, args.processed_dir)


if __name__ == "__main__":
    main()
