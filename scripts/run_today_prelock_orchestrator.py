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
    from daily_hardening import PROCESSED_DIR, TODAY_DIR, make_run_id, split_fresh_stale_rows, stamp_csv, stale_date_summary, utc_now_iso
    from run_today_prelock_pipeline import PRELOCK_COLUMNS, build_prelock_outputs, minutes_to_kickoff
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, TODAY_DIR, make_run_id, split_fresh_stale_rows, stamp_csv, stale_date_summary, utc_now_iso
    from scripts.run_today_prelock_pipeline import PRELOCK_COLUMNS, build_prelock_outputs, minutes_to_kickoff


ROOT = Path(__file__).resolve().parents[1]

SUMMARY_CSV = "vsigma_today_prelock_orchestrator_summary.csv"
REPORT_TXT = "vsigma_today_prelock_orchestrator_report.txt"
PRELOCK_COMPARISON = "vsigma_today_prelock_comparison.csv"
PRELOCK_TOP = "vsigma_today_prelock_competition_top.csv"
PRELOCK_REPORT = "vsigma_today_prelock_report.txt"

V7_STEP = "scripts/run_today_shadow_candidate_v7.py"
ODDS_SNAPSHOT_STEP = "scripts/capture_odds_snapshots.py"
CLV_REPORT_STEP = "scripts/build_clv_calibration_report.py"
V7_ADVISOR_STEP = "scripts/build_candidate_v7_calibration_advisor.py"
IMMUTABLE_LEDGER_STEP = "scripts/update_immutable_daily_ledger.py"
EXPERIMENT_PERFORMANCE_STEP = "scripts/build_experiment_performance_report.py"
GOVERNANCE_STEP = "scripts/build_promotion_threshold_governance.py"
FRESHNESS_STEP = "scripts/validate_daily_output_freshness.py"
MASTER_REPORT_STEP = "scripts/build_daily_competition_master_report.py"
SCOREBOARD_STEP = "scripts/update_competition_scoreboard.py"

PRELOCK_INPUT_FILES = [
    "vsigma_today_competition_top.csv",
    "vsigma_today_candidate_v2_competition_top.csv",
    "vsigma_today_candidate_v7_competition_top.csv",
    "vsigma_today_candidate_v7_competition_shortlist.csv",
]


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def run_optional_step_with_args(script_path: str, extra_args: list[str]) -> bool:
    command = [sys.executable, script_path, *extra_args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(command, cwd=ROOT, check=False, env=env)
    if completed.returncode != 0:
        print(f"WARNING: optional step failed ({script_path}) with exit code {completed.returncode}", flush=True)
        return False
    return True


def load_current_rows(processed_dir: Path, target_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    current_frames: list[pd.DataFrame] = []
    stale_frames: list[pd.DataFrame] = []
    for filename in PRELOCK_INPUT_FILES:
        df = read_csv_optional(processed_dir / filename)
        if df.empty:
            continue
        fresh, stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
        if not fresh.empty:
            fresh = fresh.copy()
            fresh["prelock_source_file"] = filename
            current_frames.append(fresh)
        if not stale.empty:
            stale = stale.copy()
            stale["prelock_source_file"] = filename
            stale_frames.append(stale)
    current = pd.concat(current_frames, ignore_index=True) if current_frames else pd.DataFrame()
    stale = pd.concat(stale_frames, ignore_index=True) if stale_frames else pd.DataFrame()
    return current, stale


def fixture_window_summary(rows: pd.DataFrame, window_minutes: int, now_utc: datetime | None = None) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame(columns=["fixture_id", "home_team", "away_team", "market_primary", "minutes_to_kickoff", "prelock_window_status"])
    records: list[dict[str, object]] = []
    keys = ["fixture_id", "market_primary"]
    for _, row in rows.drop_duplicates([column for column in keys if column in rows.columns]).iterrows():
        minutes = minutes_to_kickoff(row, now_utc=now_utc)
        in_window = minutes is not None and 0 <= minutes <= window_minutes
        records.append(
            {
                "fixture_id": row.get("fixture_id", ""),
                "home_team": row.get("home_team", ""),
                "away_team": row.get("away_team", ""),
                "market_primary": row.get("market_primary", ""),
                "minutes_to_kickoff": round(float(minutes), 2) if minutes is not None else pd.NA,
                "prelock_window_status": "IN_PRELOCK_WINDOW" if in_window else "OUTSIDE_PRELOCK_WINDOW",
            }
        )
    return pd.DataFrame(records)


def write_empty_prelock_outputs(processed_dir: Path, today_dir: Path, target_date: str, reason: str) -> dict[str, Path]:
    snapshot_dir = today_dir / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    columns = [*PRELOCK_COLUMNS, "prelock_orchestrator_status"]
    comparison = pd.DataFrame(columns=columns)
    comparison_path = processed_dir / PRELOCK_COMPARISON
    top_path = processed_dir / PRELOCK_TOP
    report_path = processed_dir / PRELOCK_REPORT
    comparison.to_csv(comparison_path, index=False)
    comparison.to_csv(top_path, index=False)
    run_id = make_run_id(target_date)
    stamp_csv(comparison_path, target_date, "PRELOCK", "PRELOCK_COMPARISON", run_id)
    stamp_csv(top_path, target_date, "PRELOCK", "OFFICIAL_BASELINE_PRELOCK", run_id)
    report_path.write_text(
        "\n".join(
            [
                "# vSIGMA Pre-Lock Report",
                "",
                f"- Target date: {target_date}",
                f"- Status: {reason}",
                "- No stale pre-lock rows reused.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    for path in [comparison_path, top_path, report_path]:
        if path.exists():
            shutil.copy2(path, snapshot_dir / path.name)
    return {"prelock_comparison": comparison_path, "prelock_top": top_path, "prelock_report": report_path}


def v7_status_counts(processed_dir: Path) -> dict[str, int]:
    df = read_csv_optional(processed_dir / "vsigma_today_candidate_v7_competition_shortlist.csv")
    if df.empty:
        return {
            "v7_waiting_for_prelock": 0,
            "v7_prelock_confirmed": 0,
            "v7_prelock_rejected": 0,
            "v7_prelock_unavailable": 0,
        }
    status = df.get("candidate_v7_execution_status", pd.Series("", index=df.index)).astype(str).str.upper()
    return {
        "v7_waiting_for_prelock": int(status.eq("V7_WAITING_FOR_PRELOCK").sum()),
        "v7_prelock_confirmed": int(status.eq("V7_PRELOCK_CONFIRMED").sum()),
        "v7_prelock_rejected": int(status.isin(["V7_PRELOCK_REJECTED", "V7_PRICE_REJECTED", "V7_SECONDARY_ONLY"]).sum()),
        "v7_prelock_unavailable": int(status.eq("V7_PRELOCK_UNAVAILABLE").sum()),
    }


def write_orchestrator_outputs(
    processed_dir: Path,
    today_dir: Path,
    target_date: str,
    summary_row: dict[str, object],
    fixture_summary: pd.DataFrame,
) -> dict[str, Path]:
    snapshot_dir = today_dir / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    summary_path = processed_dir / SUMMARY_CSV
    report_path = processed_dir / REPORT_TXT
    pd.DataFrame([summary_row]).to_csv(summary_path, index=False)
    lines = [
        "# vSIGMA Pre-Lock Orchestrator Report",
        "",
        f"- Target date: {target_date}",
        f"- Status: {summary_row.get('orchestrator_status')}",
        f"- Fixtures checked: {summary_row.get('fixtures_checked')}",
        f"- Fixtures inside window: {summary_row.get('fixtures_inside_window')}",
        f"- Fixtures outside window: {summary_row.get('fixtures_outside_window')}",
        f"- Stale pre-lock excluded: {summary_row.get('stale_prelock_excluded')}",
        f"- Candidate v7 waiting: {summary_row.get('v7_waiting_for_prelock')}",
        f"- Candidate v7 confirmed: {summary_row.get('v7_prelock_confirmed')}",
        f"- Candidate v7 rejected/secondary: {summary_row.get('v7_prelock_rejected')}",
        f"- Candidate v7 unavailable: {summary_row.get('v7_prelock_unavailable')}",
        f"- Odds snapshot status: {summary_row.get('odds_snapshot_status')}",
        f"- Ledger update status: {summary_row.get('ledger_update_status')}",
        "",
        "## Fixtures Checked",
        fixture_summary.to_string(index=False) if not fixture_summary.empty else "No current-day fixtures found.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    for path in [summary_path, report_path]:
        shutil.copy2(path, snapshot_dir / path.name)
    return {"summary": summary_path, "report": report_path}


def run_prelock_orchestrator(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    target_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
    window_minutes: int = 90,
    now_utc: datetime | None = None,
) -> dict[str, Path]:
    target_date = target_date or date.today().isoformat()
    snapshot_dir = today_dir / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    current_rows, stale_rows = load_current_rows(processed_dir, target_date)
    stale_prelock = read_csv_optional(processed_dir / PRELOCK_COMPARISON)
    _fresh_prelock, stale_prelock_rows = split_fresh_stale_rows(stale_prelock, target_date, include_target_date=True) if not stale_prelock.empty else (pd.DataFrame(), pd.DataFrame())
    fixture_summary = fixture_window_summary(current_rows, window_minutes, now_utc=now_utc)
    inside = fixture_summary[fixture_summary["prelock_window_status"].eq("IN_PRELOCK_WINDOW")].copy() if not fixture_summary.empty else pd.DataFrame()
    outside = fixture_summary[fixture_summary["prelock_window_status"].eq("OUTSIDE_PRELOCK_WINDOW")].copy() if not fixture_summary.empty else pd.DataFrame()

    odds_snapshot_status = "NOT_RUN"
    ledger_update_status = "NOT_RUN"
    prelock_status = "NOT_RUN"
    if inside.empty:
        write_empty_prelock_outputs(processed_dir, today_dir, target_date, "PRELOCK_NO_FIXTURES_IN_WINDOW")
        prelock_status = "PRELOCK_NO_FIXTURES_IN_WINDOW"
    else:
        build_prelock_outputs(processed_dir, today_dir, target_date, timezone_name, window_minutes, refresh=True, now_utc=now_utc)
        prelock_status = "PRELOCK_PIPELINE_RUN"
        odds_ok = run_optional_step_with_args(ODDS_SNAPSHOT_STEP, ["--date", target_date, "--stage", "PRELOCK", "--processed-dir", str(processed_dir)])
        odds_snapshot_status = "PASS" if odds_ok else "WARNING_FAILED"
        run_optional_step_with_args(CLV_REPORT_STEP, ["--date", target_date, "--processed-dir", str(processed_dir), "--odds-dir", str(processed_dir / "odds_snapshots")])
        run_optional_step_with_args(V7_ADVISOR_STEP, ["--date", target_date, "--processed-dir", str(processed_dir), "--odds-dir", str(processed_dir / "odds_snapshots")])

    v7_ok = run_optional_step_with_args(V7_STEP, ["--date", target_date, "--timezone", timezone_name])
    ledger_pre_ok = run_optional_step_with_args(IMMUTABLE_LEDGER_STEP, ["--date", target_date, "--stage", "PRE", "--processed-dir", str(processed_dir)])
    ledger_prelock_ok = run_optional_step_with_args(IMMUTABLE_LEDGER_STEP, ["--date", target_date, "--stage", "PRELOCK", "--processed-dir", str(processed_dir)])
    ledger_update_status = "PASS" if ledger_pre_ok and ledger_prelock_ok else "WARNING_FAILED"
    run_optional_step_with_args(EXPERIMENT_PERFORMANCE_STEP, ["--processed-dir", str(processed_dir), "--ledger-path", str(processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv")])
    run_optional_step_with_args(GOVERNANCE_STEP, ["--date", target_date, "--processed-dir", str(processed_dir)])
    run_optional_step_with_args(FRESHNESS_STEP, ["--date", target_date, "--processed-dir", str(processed_dir), "--snapshot-dir", str(snapshot_dir)])
    run_optional_step_with_args(MASTER_REPORT_STEP, ["--date", target_date, "--processed-dir", str(processed_dir), "--snapshot-dir", str(snapshot_dir)])
    run_optional_step_with_args(SCOREBOARD_STEP, ["--date", target_date, "--processed-dir", str(processed_dir)])
    counts = v7_status_counts(processed_dir)
    summary_row: dict[str, object] = {
        "target_date": target_date,
        "timezone": timezone_name,
        "window_minutes": window_minutes,
        "orchestrator_status": prelock_status,
        "fixtures_checked": int(len(fixture_summary)),
        "fixtures_inside_window": int(len(inside)),
        "fixtures_outside_window": int(len(outside)),
        "stale_input_rows_excluded": int(len(stale_rows)),
        "stale_prelock_excluded": int(len(stale_prelock_rows)),
        "stale_prelock_dates": stale_date_summary(stale_prelock_rows, include_target_date=True) if not stale_prelock_rows.empty else "",
        "v7_rerun_status": "PASS" if v7_ok else "WARNING_FAILED",
        "odds_snapshot_status": odds_snapshot_status,
        "ledger_update_status": ledger_update_status,
        "run_finished_at": utc_now_iso(),
        **counts,
    }
    paths = write_orchestrator_outputs(processed_dir, today_dir, target_date, summary_row, fixture_summary)
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run vSIGMA pre-lock orchestration without changing official baseline selection.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--window-minutes", type=int, default=90)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    paths = run_prelock_orchestrator(args.processed_dir, TODAY_DIR, target_date, args.timezone, args.window_minutes)
    print("\n=== TODAY PRE-LOCK ORCHESTRATOR COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
