from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import (
        PROCESSED_DIR,
        TODAY_DIR,
        format_markdown_table,
        read_csv_lenient,
        split_fresh_stale_rows,
        stale_date_summary,
    )
except ModuleNotFoundError:
    from scripts.daily_hardening import (
        PROCESSED_DIR,
        TODAY_DIR,
        format_markdown_table,
        read_csv_lenient,
        split_fresh_stale_rows,
        stale_date_summary,
    )


ROOT = Path(__file__).resolve().parents[1]

HEALTH_DIR_NAME = "health"
SUMMARY_CSV = "vsigma_healthcheck_summary.csv"
REPORT_MD = "vsigma_healthcheck_report.md"

STATUSES = ["HEALTHY", "WARNING", "NEEDS_ATTENTION", "BROKEN", "NOT_RUN_YET"]
SEVERITY = {"HEALTHY": 0, "NOT_RUN_YET": 1, "WARNING": 2, "NEEDS_ATTENTION": 3, "BROKEN": 4}

API_ENV_NAMES = [
    "API_FOOTBALL_KEY",
    "APIFOOTBALL_KEY",
    "API_SPORTS_KEY",
    "APISPORTS_KEY",
    "RAPIDAPI_KEY",
    "X_RAPIDAPI_KEY",
]

REQUIRED_SCRIPTS = [
    "scripts/run_daily_competition_controller.py",
    "scripts/run_daily_competition_supervisor.py",
    "scripts/run_today_prelock_orchestrator.py",
    "scripts/run_today_post_results_pipeline.py",
    "scripts/update_immutable_daily_ledger.py",
    "scripts/build_daily_competition_master_report.py",
    "scripts/build_promotion_threshold_governance.py",
    "scripts/validate_daily_output_freshness.py",
    "scripts/validate_candidate_isolation.py",
    "scripts/register_vsigma_windows_tasks.ps1",
    "scripts/unregister_vsigma_windows_tasks.ps1",
]

OFFICIAL_BASELINE = "vsigma_today_competition_top.csv"
CANDIDATE_FILES = [
    ("CANDIDATE_V2", "vsigma_today_candidate_v2_competition_top.csv", True),
    ("CANDIDATE_V7", "vsigma_today_candidate_v7_competition_top.csv", True),
    ("CANDIDATE_V7_SHORTLIST", "vsigma_today_candidate_v7_competition_shortlist.csv", True),
    ("CANDIDATE_V4", "vsigma_today_candidate_v4_competition_top.csv", False),
    ("CANDIDATE_V5", "vsigma_today_candidate_v5_competition_top.csv", False),
    ("CANDIDATE_V6", "vsigma_today_candidate_v6_competition_top.csv", False),
]

TASK_NAMES = [
    "vSIGMA PRE Daily",
    "vSIGMA PRELOCK Check",
    "vSIGMA POST Daily",
    "vSIGMA POST Backup Yesterday",
]


@dataclass(frozen=True)
class HealthCheck:
    check_name: str
    status: str
    detail: str
    recovery_command: str = ""
    evidence_path: str = ""


def parse_target_date(value: str | None) -> str:
    return pd.Timestamp(value or date.today().isoformat()).date().isoformat()


def now_local(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def recovery_python(script: str, target_date: str, timezone_name: str, extra: str = "") -> str:
    command = f".\\.venv\\Scripts\\python.exe {script} --date {target_date}"
    if timezone_name:
        command += f" --timezone {timezone_name}"
    if extra:
        command += f" {extra}".rstrip()
    return command


def controller_recovery(target_date: str, timezone_name: str, mode: str) -> str:
    return recovery_python(
        "scripts\\run_daily_competition_controller.py",
        target_date,
        timezone_name,
        f"--mode {mode}",
    )


def ledger_recovery(target_date: str) -> str:
    return f".\\.venv\\Scripts\\python.exe scripts\\update_immutable_daily_ledger.py --date {target_date} --stage PRE"


def task_registration_recovery(root: Path) -> str:
    return f"powershell.exe -NoProfile -ExecutionPolicy Bypass -File {root / 'scripts' / 'register_vsigma_windows_tasks.ps1'}"


def read_snapshot_or_processed(processed_dir: Path, target_date: str, filename: str) -> tuple[Path, pd.DataFrame]:
    snap_path = snapshot_dir(processed_dir, target_date) / filename
    if snap_path.exists():
        return snap_path, read_csv_lenient(snap_path)
    path = processed_dir / filename
    return path, read_csv_lenient(path)


def file_status(path: Path, label: str, missing_status: str, missing_detail: str, recovery: str = "") -> HealthCheck:
    if path.exists():
        return HealthCheck(label, "HEALTHY", "present", evidence_path=str(path))
    return HealthCheck(label, missing_status, missing_detail, recovery or "Restore the missing vSIGMA file from the validated project source.", str(path))


def has_api_config(root: Path) -> bool:
    for name in API_ENV_NAMES:
        if os.environ.get(name):
            return True
    env_path = root / ".env"
    if not env_path.exists():
        return False
    for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() in API_ENV_NAMES and value.strip() and "TU_API_KEY_AQUI" not in value:
            return True
    return False


def pre_ran(processed_dir: Path, target_date: str) -> bool:
    today_report = snapshot_dir(processed_dir, target_date) / "today_pipeline_report.csv"
    official_path, official = read_snapshot_or_processed(processed_dir, target_date, OFFICIAL_BASELINE)
    return today_report.exists() or official_path.exists() or not official.empty


def check_output_file(
    processed_dir: Path,
    target_date: str,
    filename: str,
    label: str,
    required_after_pre: bool,
    timezone_name: str,
) -> HealthCheck:
    path, df = read_snapshot_or_processed(processed_dir, target_date, filename)
    if path.exists():
        if df.empty:
            return HealthCheck(label, "HEALTHY", "empty output with headers is valid for NO_BET", evidence_path=str(path))
        fresh, stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
        if stale.empty or not fresh.empty:
            return HealthCheck(label, "HEALTHY", f"present with {len(df)} row(s)", evidence_path=str(path))
        return HealthCheck(
            label,
            "WARNING",
            f"only stale rows found for {stale_date_summary(stale, include_target_date=True)}",
            controller_recovery(target_date, timezone_name, "pre"),
            str(path),
        )
    if required_after_pre and pre_ran(processed_dir, target_date):
        return HealthCheck(label, "WARNING", "expected daily output is missing", controller_recovery(target_date, timezone_name, "pre"), str(path))
    return HealthCheck(label, "NOT_RUN_YET", "output not available yet", controller_recovery(target_date, timezone_name, "pre"), str(path))


def ledger_check(processed_dir: Path, target_date: str) -> list[HealthCheck]:
    path = processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv"
    if not path.exists():
        return [HealthCheck("immutable_ledger_exists", "WARNING", "immutable ledger missing", ledger_recovery(target_date), str(path))]
    ledger = read_csv_lenient(path)
    checks = [HealthCheck("immutable_ledger_exists", "HEALTHY", f"ledger present with {len(ledger)} row(s)", evidence_path=str(path))]
    if ledger.empty:
        checks.append(HealthCheck("ledger_target_date_rows", "WARNING", "ledger has no rows", ledger_recovery(target_date), str(path)))
        return checks
    if "target_date" in ledger.columns:
        day = ledger[ledger["target_date"].astype(str).eq(target_date)].copy()
    else:
        day = pd.DataFrame()
        checks.append(HealthCheck("ledger_target_date_column", "WARNING", "ledger has no target_date column", ledger_recovery(target_date), str(path)))
    if day.empty:
        checks.append(HealthCheck("ledger_target_date_rows", "WARNING", "ledger has no rows for target date", ledger_recovery(target_date), str(path)))
    else:
        checks.append(HealthCheck("ledger_target_date_rows", "HEALTHY", f"{len(day)} row(s) for target date", evidence_path=str(path)))
    if "ledger_id" not in ledger.columns:
        checks.append(HealthCheck("ledger_duplicate_ids", "WARNING", "ledger_id column not available for duplicate check", ledger_recovery(target_date), str(path)))
        return checks
    duplicate_count = int(day["ledger_id"].astype(str).duplicated(keep=False).sum()) if not day.empty else 0
    if duplicate_count:
        checks.append(
            HealthCheck(
                "ledger_duplicate_ids",
                "BROKEN",
                f"{duplicate_count} duplicate ledger_id row(s) for target date",
                ledger_recovery(target_date),
                str(path),
            )
        )
    else:
        checks.append(HealthCheck("ledger_duplicate_ids", "HEALTHY", "no duplicate ledger_id values for target date", evidence_path=str(path)))
    return checks


def report_has_error(df: pd.DataFrame) -> bool:
    if df.empty:
        return False
    for column in df.columns:
        values = df[column].dropna().astype(str).str.upper()
        if values.str.contains("ERROR", regex=False).any():
            return True
    return False


def validation_report_check(
    processed_dir: Path,
    target_date: str,
    filename: str,
    label: str,
    recovery: str,
) -> HealthCheck:
    path, df = read_snapshot_or_processed(processed_dir, target_date, filename)
    if not path.exists():
        return HealthCheck(label, "WARNING", "validation report missing", recovery, str(path))
    if report_has_error(df):
        return HealthCheck(label, "NEEDS_ATTENTION", "validation report contains ERROR status", recovery, str(path))
    if not df.empty and "status" in df.columns and df["status"].astype(str).str.upper().str.startswith("WARNING").any():
        return HealthCheck(label, "WARNING", "validation report contains warning rows", recovery, str(path))
    return HealthCheck(label, "HEALTHY", "validation report present without ERROR", evidence_path=str(path))


def prelock_check(processed_dir: Path, target_date: str, timezone_name: str) -> HealthCheck:
    path, prelock = read_snapshot_or_processed(processed_dir, target_date, "vsigma_today_prelock_comparison.csv")
    if not path.exists():
        return HealthCheck("prelock_freshness", "NOT_RUN_YET", "prelock output absent", controller_recovery(target_date, timezone_name, "prelock"), str(path))
    if prelock.empty:
        return HealthCheck("prelock_freshness", "HEALTHY", "prelock output present and empty for NO_BET/unavailable state", evidence_path=str(path))
    fresh, stale = split_fresh_stale_rows(prelock, target_date, include_target_date=True)
    if not stale.empty and fresh.empty:
        return HealthCheck(
            "prelock_freshness",
            "WARNING",
            f"stale prelock rows found for {stale_date_summary(stale, include_target_date=True)}",
            recovery_python("scripts\\run_today_prelock_orchestrator.py", target_date, timezone_name, "--window-minutes 90"),
            str(path),
        )
    if not stale.empty:
        return HealthCheck(
            "prelock_freshness",
            "WARNING",
            f"fresh prelock rows present, stale rows excluded for {stale_date_summary(stale, include_target_date=True)}",
            controller_recovery(target_date, timezone_name, "status"),
            str(path),
        )
    return HealthCheck("prelock_freshness", "HEALTHY", f"fresh prelock rows present: {len(fresh)}", evidence_path=str(path))


def post_results_check(processed_dir: Path, target_date: str, timezone_name: str) -> HealthCheck:
    path, report = read_snapshot_or_processed(processed_dir, target_date, "today_post_results_report.csv")
    official_path, official = read_snapshot_or_processed(processed_dir, target_date, OFFICIAL_BASELINE)
    if not path.exists():
        if not official_path.exists() or official.empty:
            return HealthCheck("post_results_status", "NOT_RUN_YET", "post not required yet or NO_BET official output", evidence_path=str(path))
        return HealthCheck("post_results_status", "WARNING", "post-results report missing while official picks exist", controller_recovery(target_date, timezone_name, "post"), str(path))
    if report.empty:
        return HealthCheck("post_results_status", "WARNING", "post-results report is empty", controller_recovery(target_date, timezone_name, "post"), str(path))
    pending = pd.to_numeric(report.get("pending_rows", pd.Series(dtype=object)), errors="coerce").fillna(0)
    if float(pending.sum()) > 0:
        return HealthCheck("post_results_status", "WARNING", f"post has {int(pending.sum())} pending row(s)", controller_recovery(target_date, timezone_name, "post"), str(path))
    return HealthCheck("post_results_status", "HEALTHY", "post report present and settled", evidence_path=str(path))


def task_status(root: Path) -> HealthCheck:
    if os.name != "nt":
        return HealthCheck("windows_task_registration", "NOT_RUN_YET", "task registration check unavailable outside Windows", task_registration_recovery(root))
    statuses: list[str] = []
    missing: list[str] = []
    for task_name in TASK_NAMES:
        completed = subprocess.run(["schtasks.exe", "/Query", "/TN", task_name, "/FO", "LIST"], capture_output=True, text=True, check=False)
        if completed.returncode == 0:
            statuses.append(f"{task_name}=REGISTERED")
        else:
            statuses.append(f"{task_name}=NOT_REGISTERED")
            missing.append(task_name)
    if missing:
        return HealthCheck("windows_task_registration", "WARNING", "; ".join(statuses), task_registration_recovery(root))
    return HealthCheck("windows_task_registration", "HEALTHY", "; ".join(statuses))


def automation_logs_check(root: Path, now_value: datetime) -> HealthCheck:
    path = root / "automation_logs" / "supervisor"
    if not path.exists():
        return HealthCheck("recent_automation_logs", "WARNING", "supervisor log directory missing", controller_recovery(date.today().isoformat(), "Atlantic/Canary", "status"), str(path))
    files = [item for item in path.glob("*.log") if item.is_file()]
    if not files:
        return HealthCheck("recent_automation_logs", "WARNING", "no supervisor log files found", controller_recovery(date.today().isoformat(), "Atlantic/Canary", "status"), str(path))
    latest = max(files, key=lambda item: item.stat().st_mtime)
    latest_time = datetime.fromtimestamp(latest.stat().st_mtime)
    age = now_value.replace(tzinfo=None) - latest_time
    if age > timedelta(days=2):
        return HealthCheck("recent_automation_logs", "WARNING", f"latest supervisor log is older than 48h: {latest}", evidence_path=str(latest))
    return HealthCheck("recent_automation_logs", "HEALTHY", f"latest log: {latest}", evidence_path=str(latest))


def disk_space_check(root: Path) -> HealthCheck:
    usage = shutil.disk_usage(root)
    free_gb = usage.free / (1024**3)
    if free_gb < 1:
        return HealthCheck("disk_space", "BROKEN", f"free disk space critically low: {free_gb:.2f} GB", "Free disk space on the vSIGMA volume.")
    if free_gb < 5:
        return HealthCheck("disk_space", "WARNING", f"free disk space low: {free_gb:.2f} GB", "Free disk space on the vSIGMA volume.")
    return HealthCheck("disk_space", "HEALTHY", f"free disk space acceptable: {free_gb:.2f} GB")


def global_status(checks: list[HealthCheck]) -> str:
    if not checks:
        return "BROKEN"
    worst = max(checks, key=lambda check: SEVERITY.get(check.status, 4))
    return worst.status


def checks_to_frame(checks: list[HealthCheck], target_date: str, mode: str, generated_at: str) -> pd.DataFrame:
    overall = global_status(checks)
    rows = []
    for check in checks:
        rows.append(
            {
                "target_date": target_date,
                "mode": mode,
                "generated_at": generated_at,
                "global_health_status": overall,
                "check_name": check.check_name,
                "status": check.status,
                "detail": check.detail,
                "recovery_command": check.recovery_command,
                "evidence_path": check.evidence_path,
            }
        )
    return pd.DataFrame(rows)


def write_reports(report: pd.DataFrame, processed_dir: Path, target_date: str) -> dict[str, Path]:
    health_dir = processed_dir / HEALTH_DIR_NAME
    snap = snapshot_dir(processed_dir, target_date)
    health_dir.mkdir(parents=True, exist_ok=True)
    snap.mkdir(parents=True, exist_ok=True)

    summary_path = health_dir / SUMMARY_CSV
    report_path = health_dir / REPORT_MD
    snapshot_report_path = snap / REPORT_MD
    report.to_csv(summary_path, index=False)

    overall = str(report["global_health_status"].iloc[0]) if not report.empty else "BROKEN"
    critical = report[report["status"].astype(str).isin(["WARNING", "NEEDS_ATTENTION", "BROKEN"])].copy() if not report.empty else pd.DataFrame()
    recovery = ""
    if not critical.empty:
        recoveries = [str(value).strip() for value in critical["recovery_command"].dropna().tolist() if str(value).strip()]
        recovery = recoveries[0] if recoveries else ""

    counts = report["status"].value_counts().to_dict() if not report.empty else {}
    lines = [
        f"# vSIGMA Healthcheck Report - {target_date}",
        "",
        f"- Global health status: {overall}",
        f"- Generated at: {report['generated_at'].iloc[0] if not report.empty else datetime.now().isoformat()}",
        f"- Mode: {report['mode'].iloc[0] if not report.empty else ''}",
        f"- HEALTHY: {counts.get('HEALTHY', 0)}",
        f"- WARNING: {counts.get('WARNING', 0)}",
        f"- NEEDS_ATTENTION: {counts.get('NEEDS_ATTENTION', 0)}",
        f"- BROKEN: {counts.get('BROKEN', 0)}",
        f"- NOT_RUN_YET: {counts.get('NOT_RUN_YET', 0)}",
        f"- First recovery command: `{recovery}`" if recovery else "- First recovery command: ",
        "",
        "## Critical Warnings",
        format_markdown_table(critical, ["check_name", "status", "detail", "recovery_command"], max_rows=50) if not critical.empty else "_No warnings or errors._",
        "",
        "## All Checks",
        format_markdown_table(report, ["check_name", "status", "detail", "recovery_command", "evidence_path"], max_rows=200),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(report_path, snapshot_report_path)
    return {"summary_csv": summary_path, "report_md": report_path, "snapshot_report_md": snapshot_report_path}


def run_healthcheck(
    target_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
    mode: str = "quick",
    processed_dir: Path = PROCESSED_DIR,
    root: Path = ROOT,
) -> dict[str, object]:
    target_date = parse_target_date(target_date)
    generated_at = now_local(timezone_name).isoformat()
    snap = snapshot_dir(processed_dir, target_date)
    raw_dir = root / "data" / "raw"
    venv_python = root / ".venv" / "Scripts" / "python.exe"

    checks: list[HealthCheck] = [
        HealthCheck("project_root_exists", "HEALTHY" if root.exists() else "BROKEN", "project root present" if root.exists() else "project root missing", evidence_path=str(root)),
        HealthCheck(
            "venv_python_exists",
            "HEALTHY" if venv_python.exists() else "BROKEN",
            ".venv Python present" if venv_python.exists() else ".venv Python missing",
            "Create or repair .venv, then install project requirements.",
            str(venv_python),
        ),
        HealthCheck("data_raw_exists", "HEALTHY" if raw_dir.exists() else "WARNING", "data/raw present" if raw_dir.exists() else "data/raw missing", "Create data\\raw or run the raw data fetch pipeline.", str(raw_dir)),
        HealthCheck("data_processed_exists", "HEALTHY" if processed_dir.exists() else "BROKEN", "data/processed present" if processed_dir.exists() else "data/processed missing", "Create data\\processed or run the PRE pipeline.", str(processed_dir)),
    ]

    for script in REQUIRED_SCRIPTS:
        path = root / script
        checks.append(file_status(path, f"required_script:{script}", "BROKEN", "required script missing"))

    checks.append(
        HealthCheck(
            "api_config_available",
            "HEALTHY" if has_api_config(root) else "WARNING",
            "API configuration detected without exposing secrets" if has_api_config(root) else "API key not detected in environment or .env",
            "Set API_FOOTBALL_KEY, APISPORTS_KEY, RAPIDAPI_KEY, or X_RAPIDAPI_KEY in .env/environment.",
            str(root / ".env"),
        )
    )
    checks.append(
        HealthCheck(
            "today_snapshot_folder",
            "HEALTHY" if snap.exists() else "NOT_RUN_YET",
            "today snapshot folder present" if snap.exists() else "today snapshot folder not created yet",
            controller_recovery(target_date, timezone_name, "pre"),
            str(snap),
        )
    )

    checks.append(check_output_file(processed_dir, target_date, OFFICIAL_BASELINE, "official_baseline_output", True, timezone_name))
    for label, filename, required in CANDIDATE_FILES:
        checks.append(check_output_file(processed_dir, target_date, filename, f"candidate_output:{label}", required, timezone_name))

    master_report = snap / "daily_competition_master_report.md"
    checks.append(file_status(master_report, "daily_master_report", "WARNING", "daily master report missing", f".\\.venv\\Scripts\\python.exe scripts\\build_daily_competition_master_report.py --date {target_date}"))
    checks.extend(ledger_check(processed_dir, target_date))
    checks.append(
        validation_report_check(
            processed_dir,
            target_date,
            "vsigma_daily_freshness_report.csv",
            "freshness_report",
            f".\\.venv\\Scripts\\python.exe scripts\\validate_daily_output_freshness.py --date {target_date}",
        )
    )
    checks.append(
        validation_report_check(
            processed_dir,
            target_date,
            "vsigma_candidate_isolation_report.csv",
            "candidate_isolation_report",
            f".\\.venv\\Scripts\\python.exe scripts\\validate_candidate_isolation.py --date {target_date}",
        )
    )
    checks.append(prelock_check(processed_dir, target_date, timezone_name))
    checks.append(post_results_check(processed_dir, target_date, timezone_name))
    checks.append(file_status(processed_dir / "daily_supervisor_latest.md", "supervisor_latest_report", "WARNING", "supervisor latest report missing", recovery_python("scripts\\run_daily_competition_supervisor.py", target_date, timezone_name, "--mode status")))
    checks.append(task_status(root))
    checks.append(automation_logs_check(root, now_local(timezone_name)))
    checks.append(disk_space_check(root))

    if mode == "full":
        checks.append(
            HealthCheck(
                "healthcheck_mode",
                "HEALTHY",
                "full mode completed all quick checks plus environment diagnostics",
            )
        )
    else:
        checks.append(HealthCheck("healthcheck_mode", "HEALTHY", "quick mode completed"))

    report = checks_to_frame(checks, target_date, mode, generated_at)
    paths = write_reports(report, processed_dir, target_date)
    paths["global_status"] = global_status(checks)
    paths["checks"] = report
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run vSIGMA daily healthcheck and auto-recovery guard diagnostics.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--mode", choices=["quick", "full"], default="quick")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = run_healthcheck(args.date, args.timezone, args.mode, args.processed_dir)
    checks = paths["checks"]
    print("\n=== VSIGMA HEALTHCHECK ===")
    print(f"Date: {parse_target_date(args.date)}")
    print(f"Mode: {args.mode}")
    print(f"Global status: {paths['global_status']}")
    print(f"Summary CSV: {paths['summary_csv']}")
    print(f"Report: {paths['report_md']}")
    print(f"Snapshot report: {paths['snapshot_report_md']}")
    if isinstance(checks, pd.DataFrame) and not checks.empty:
        critical = checks[checks["status"].astype(str).isin(["WARNING", "NEEDS_ATTENTION", "BROKEN"])].copy()
        recoveries = [str(value).strip() for value in critical["recovery_command"].dropna().tolist() if str(value).strip()]
        if recoveries:
            print(f"First recovery command: {recoveries[0]}")


if __name__ == "__main__":
    main()
