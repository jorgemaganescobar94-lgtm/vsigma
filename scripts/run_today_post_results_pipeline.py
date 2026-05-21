from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_daily_decision_journal import POST_SUMMARY_FILENAME, build_post_summary
except ModuleNotFoundError:
    from scripts.build_daily_decision_journal import POST_SUMMARY_FILENAME, build_post_summary


ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

SHORTLIST_CSV = PROCESSED_DIR / "vsigma_today_execution_shortlist.csv"
BETS_ONLY_CSV = PROCESSED_DIR / "vsigma_today_execution_bets_only.csv"

POST_RESULTS_STEPS = [
    "scripts/refresh_finished_results_by_date.py",
    "scripts/label_market_results.py",
    "scripts/build_execution_shortlist_results_ledger.py",
]

SHADOW_CANDIDATE_V2_POST_STEP = "scripts/run_today_shadow_candidate_v2_post_results.py"
SHADOW_CANDIDATE_V4_POST_STEP = "scripts/run_today_shadow_candidate_v4_post_results.py"
SHADOW_CANDIDATE_V5_POST_STEP = "scripts/run_today_shadow_candidate_v5_post_results.py"
SHADOW_CANDIDATE_V6_POST_STEP = "scripts/run_today_shadow_candidate_v6_post_results.py"
SHADOW_CANDIDATE_V7_POST_STEP = "scripts/run_today_shadow_candidate_v7_post_results.py"
ODDS_SNAPSHOT_STEP = "scripts/capture_odds_snapshots.py"
CLV_REPORT_STEP = "scripts/build_clv_calibration_report.py"
V7_CALIBRATION_ADVISOR_STEP = "scripts/build_candidate_v7_calibration_advisor.py"
METADATA_STAMP_STEP = "scripts/stamp_daily_output_metadata.py"
FRESHNESS_VALIDATION_STEP = "scripts/validate_daily_output_freshness.py"
CANDIDATE_ISOLATION_STEP = "scripts/validate_candidate_isolation.py"
MASTER_REPORT_STEP = "scripts/build_daily_competition_master_report.py"
SCOREBOARD_STEP = "scripts/update_competition_scoreboard.py"
IMMUTABLE_LEDGER_STEP = "scripts/update_immutable_daily_ledger.py"
EXPERIMENT_PERFORMANCE_STEP = "scripts/build_experiment_performance_report.py"
GOVERNANCE_STEP = "scripts/build_promotion_threshold_governance.py"

POST_RESULTS_SNAPSHOT_FILES = [
    PROCESSED_DIR / "vsigma_today_premium_core.csv",
    SHORTLIST_CSV,
    BETS_ONLY_CSV,
    PROCESSED_DIR / "vsigma_today_execution_summary.csv",
    PROCESSED_DIR / "vsigma_execution_shortlist_results_ledger.csv",
    PROCESSED_DIR / "vsigma_execution_shortlist_results_summary.csv",
    PROCESSED_DIR / "vsigma_market_results_labeled.csv",
    PROCESSED_DIR / "vsigma_market_results_report.csv",
    PROCESSED_DIR / "refresh_finished_results_by_date_report.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v2_results_ledger.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v2_results_summary.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_results.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_results_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v4_results_ledger.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v4_results_summary.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_results.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_results_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v5_results_ledger.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v5_results_summary.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_results.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_results_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v6_results_ledger.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v6_results_summary.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6_results.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6_results_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v7_results_ledger.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v7_results_summary.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7_results.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7_results_report.txt",
    PROCESSED_DIR / "vsigma_daily_freshness_report.csv",
    PROCESSED_DIR / "vsigma_daily_freshness_report.txt",
    PROCESSED_DIR / "vsigma_candidate_isolation_report.csv",
    PROCESSED_DIR / "vsigma_candidate_isolation_report.txt",
]

POST_RESULTS_JOURNAL_FILES = [
    POST_SUMMARY_FILENAME,
]

LEDGER_CSV = PROCESSED_DIR / "vsigma_execution_shortlist_results_ledger.csv"
LEDGER_SUMMARY_CSV = PROCESSED_DIR / "vsigma_execution_shortlist_results_summary.csv"

VALID_LEDGER_STATUSES = {"RESULT_AVAILABLE", "PENDING", "UNMATCHED"}
GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}

REQUIRED_LEDGER_COLUMNS = [
    "execution_rank",
    "fixture_id",
    "market_primary",
    "ledger_result_status",
    "actionable_result",
    "actionable_profit_units",
    "primary_profit_units",
]


def read_csv_required(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")
    return pd.read_csv(path)


def normalize_date_value(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()[:10]


def normalize_result(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def validate_shortlist_for_date(shortlist: pd.DataFrame, match_date: str) -> None:
    if shortlist.empty:
        raise RuntimeError(f"Execution shortlist is empty for requested post-results date {match_date}.")
    if "fixture_id" not in shortlist.columns:
        raise ValueError("Execution shortlist is missing fixture_id.")
    if "date" not in shortlist.columns:
        raise ValueError("Execution shortlist is missing date.")

    observed_dates = sorted(
        {
            normalize_date_value(value)
            for value in shortlist["date"].dropna().tolist()
            if normalize_date_value(value)
        }
    )
    if observed_dates != [match_date]:
        raise ValueError(
            f"Execution shortlist dates {observed_dates} do not match requested date {match_date}."
        )


def shortlist_snapshot_path(match_date: str) -> Path:
    return TODAY_DIR / match_date / SHORTLIST_CSV.name


def load_shortlist_for_date(match_date: str) -> tuple[pd.DataFrame, Path]:
    snapshot_path = shortlist_snapshot_path(match_date)
    if snapshot_path.exists():
        shortlist = read_csv_required(
            snapshot_path,
            f"date-scoped today execution shortlist for {match_date}",
        )
        validate_shortlist_for_date(shortlist, match_date)
        return shortlist, snapshot_path

    shortlist = read_csv_required(SHORTLIST_CSV, "rolling today execution shortlist")
    try:
        validate_shortlist_for_date(shortlist, match_date)
    except ValueError as exc:
        raise ValueError(
            f"No date-scoped execution shortlist found at {snapshot_path} and rolling shortlist "
            f"{SHORTLIST_CSV} is not for requested date {match_date}. "
            "Run PRE for that date or restore the snapshot before running post-results."
        ) from exc

    return shortlist, SHORTLIST_CSV


def run_step(script_path: str) -> None:
    command = [sys.executable, script_path]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    print("\n=== RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True, env=env)


def run_step_with_args(script_path: str, extra_args: list[str]) -> None:
    command = [sys.executable, script_path, *extra_args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    print("\n=== RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True, env=env)


def run_optional_step_with_args(script_path: str, extra_args: list[str]) -> bool:
    command = [sys.executable, script_path, *extra_args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    print("\n=== OPTIONAL RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False, env=env)
    if completed.returncode != 0:
        print(f"WARNING: optional step failed ({script_path}) with exit code {completed.returncode}", flush=True)
        return False
    return True


def run_shadow_candidate_v2_post_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V2_POST_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v4_post_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V4_POST_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v5_post_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V5_POST_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v6_post_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V6_POST_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v7_post_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V7_POST_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_odds_clv_post_steps(match_date: str) -> None:
    run_optional_step_with_args(ODDS_SNAPSHOT_STEP, ["--date", match_date, "--stage", "CLOSE_PROXY"])
    run_optional_step_with_args(ODDS_SNAPSHOT_STEP, ["--date", match_date, "--stage", "POST"])
    run_optional_step_with_args(CLV_REPORT_STEP, ["--date", match_date])
    run_optional_step_with_args(V7_CALIBRATION_ADVISOR_STEP, ["--date", match_date])


def run_daily_hardening_steps(match_date: str) -> None:
    snapshot_dir = TODAY_DIR / match_date
    common_args = ["--date", match_date, "--snapshot-dir", str(snapshot_dir)]
    run_optional_step_with_args(METADATA_STAMP_STEP, [*common_args, "--phase", "post"])
    run_optional_step_with_args(IMMUTABLE_LEDGER_STEP, ["--date", match_date, "--stage", "POST"])
    run_optional_step_with_args(EXPERIMENT_PERFORMANCE_STEP, [])
    run_optional_step_with_args(GOVERNANCE_STEP, ["--date", match_date])
    for step in [FRESHNESS_VALIDATION_STEP, CANDIDATE_ISOLATION_STEP, MASTER_REPORT_STEP]:
        run_optional_step_with_args(step, common_args)
    run_optional_step_with_args(SCOREBOARD_STEP, ["--date", match_date])


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def validate_date_scoped_file(path: Path, match_date: str) -> None:
    if not path.exists() or path.stat().st_size == 0:
        return
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return

    if df.empty or "date" not in df.columns:
        return

    observed = sorted(
        {
            normalize_date_value(value)
            for value in df["date"].dropna().tolist()
            if normalize_date_value(value)
        }
    )
    if observed and observed != [match_date]:
        raise ValueError(f"Snapshot file {path} contains non-requested dates: {observed}")


def snapshot_post_results_outputs(match_date: str) -> Path:
    dest_dir = TODAY_DIR / match_date
    dest_dir.mkdir(parents=True, exist_ok=True)

    for src in POST_RESULTS_SNAPSHOT_FILES:
        copied = dest_dir / src.name
        if src.exists():
            copy_if_exists(src, dest_dir)
            validate_date_scoped_file(copied, match_date)
        elif copied.exists():
            copied.unlink()

    return dest_dir


def require_columns(df: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def validate_ledger_against_shortlist(ledger: pd.DataFrame, shortlist: pd.DataFrame) -> None:
    require_columns(ledger, REQUIRED_LEDGER_COLUMNS, "execution shortlist results ledger")

    if len(ledger) != len(shortlist):
        raise ValueError(
            f"Execution ledger rows {len(ledger)} do not equal shortlist rows {len(shortlist)}."
        )

    shortlist_fixture_ids = set(shortlist["fixture_id"].dropna().tolist())
    ledger_fixture_ids = set(ledger["fixture_id"].dropna().tolist())
    unexpected = sorted(ledger_fixture_ids - shortlist_fixture_ids)
    if unexpected:
        raise ValueError(f"Execution ledger contains fixture_ids outside shortlist: {unexpected[:10]}")

    statuses = {normalize_result(value) for value in ledger["ledger_result_status"].dropna().tolist()}
    invalid = sorted(statuses - VALID_LEDGER_STATUSES)
    if invalid:
        raise ValueError(f"Execution ledger has invalid ledger_result_status values: {invalid}")


def preferred_profit(ledger: pd.DataFrame) -> pd.Series:
    actionable = pd.to_numeric(ledger["actionable_profit_units"], errors="coerce")
    primary = pd.to_numeric(ledger["primary_profit_units"], errors="coerce")
    return actionable.combine_first(primary)


def compute_report_row(
    match_date: str,
    timezone_name: str,
    shortlist: pd.DataFrame,
    ledger: pd.DataFrame,
    snapshot_dir: Path,
) -> dict[str, Any]:
    status = ledger["ledger_result_status"].map(normalize_result)
    actionable_result = ledger["actionable_result"].map(normalize_result)
    recommendation = shortlist.get("final_recommendation", pd.Series(index=shortlist.index, dtype=object)).map(
        normalize_result
    )
    result_available = status.eq("RESULT_AVAILABLE")
    profit = preferred_profit(ledger).where(result_available)
    result_available_rows = int(result_available.sum())
    profit_units_total = float(profit.sum(skipna=True)) if result_available_rows else 0.0
    roi_percent = (
        round((profit_units_total / result_available_rows) * 100.0, 6)
        if result_available_rows
        else pd.NA
    )

    return {
        "date": match_date,
        "timezone": timezone_name,
        "shortlist_rows": int(len(shortlist)),
        "shortlist_bet_rows": int(recommendation.eq("BET").sum()),
        "ledger_rows": int(len(ledger)),
        "result_available_rows": result_available_rows,
        "pending_rows": int(status.eq("PENDING").sum()),
        "unmatched_rows": int(status.eq("UNMATCHED").sum()),
        "win_rows": int(actionable_result.eq("WIN").sum()),
        "loss_rows": int(actionable_result.eq("LOSS").sum()),
        "push_rows": int(actionable_result.eq("PUSH").sum()),
        "void_rows": int(actionable_result.eq("VOID").sum()),
        "profit_units_total": round(profit_units_total, 6),
        "roi_percent": roi_percent,
        "snapshot_dir": str(snapshot_dir),
        "run_finished_at": datetime.now(timezone.utc).isoformat(),
    }


def write_post_results_report(
    match_date: str,
    timezone_name: str,
    shortlist: pd.DataFrame,
    ledger: pd.DataFrame,
    snapshot_dir: Path,
) -> Path:
    report_path = snapshot_dir / "today_post_results_report.csv"
    row = compute_report_row(match_date, timezone_name, shortlist, ledger, snapshot_dir)
    pd.DataFrame([row]).to_csv(report_path, index=False)
    validate_date_scoped_file(report_path, match_date)
    return report_path


def run_today_post_results_pipeline(match_date: str, timezone_name: str) -> tuple[Path, Path, pd.DataFrame]:
    shortlist, shortlist_source = load_shortlist_for_date(match_date)

    print("\n=== TODAY POST-RESULTS PIPELINE ===")
    print(f"Date: {match_date}")
    print(f"Timezone: {timezone_name}")
    print(f"Execution shortlist source: {shortlist_source}")
    print(f"Execution shortlist rows: {len(shortlist)}")

    for step in POST_RESULTS_STEPS:
        run_step(step)

    ledger = read_csv_required(LEDGER_CSV, "execution shortlist results ledger")
    validate_ledger_against_shortlist(ledger, shortlist)

    snapshot_dir = snapshot_post_results_outputs(match_date)
    report_path = write_post_results_report(match_date, timezone_name, shortlist, ledger, snapshot_dir)
    post_journal_path = build_post_summary(PROCESSED_DIR, TODAY_DIR, match_date, timezone_name)
    run_shadow_candidate_v2_post_step(match_date, timezone_name)
    run_shadow_candidate_v4_post_step(match_date, timezone_name)
    run_shadow_candidate_v5_post_step(match_date, timezone_name)
    run_shadow_candidate_v6_post_step(match_date, timezone_name)
    run_shadow_candidate_v7_post_step(match_date, timezone_name)
    run_odds_clv_post_steps(match_date)
    run_daily_hardening_steps(match_date)

    print("\n=== TODAY POST-RESULTS PIPELINE COMPLETADO ===")
    print(f"Snapshot dir: {snapshot_dir}")
    print(f"Post-results report: {report_path}")
    print(f"Daily post journal: {post_journal_path}")
    print(f"Ledger rows: {len(ledger)}")
    print(f"Result available: {(ledger['ledger_result_status'].map(normalize_result) == 'RESULT_AVAILABLE').sum()}")
    print(f"Pending: {(ledger['ledger_result_status'].map(normalize_result) == 'PENDING').sum()}")
    print(f"Unmatched: {(ledger['ledger_result_status'].map(normalize_result) == 'UNMATCHED').sum()}")

    return snapshot_dir, report_path, ledger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh finished results, label markets, and rebuild today's execution shortlist ledger."
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Post-results date in YYYY-MM-DD.")
    parser.add_argument("--timezone", default="Atlantic/Canary", help="API timezone context for reporting.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    run_today_post_results_pipeline(match_date, args.timezone)


if __name__ == "__main__":
    main()
