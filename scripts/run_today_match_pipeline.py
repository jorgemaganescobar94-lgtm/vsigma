from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from api_football_client import APIFootballClient
    from build_daily_decision_journal import PRE_SUMMARY_FILENAME, build_pre_summary
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient
    from scripts.build_daily_decision_journal import PRE_SUMMARY_FILENAME, build_pre_summary


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
RAW_JSON_PATH = ROOT / "data" / "raw" / "api_matches.json"
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

UPCOMING_STATUSES = {"NS", "TBD", "PST"}

PIPELINE_STEPS = [
    "scripts/filter_leagues.py",
    "scripts/build_api_league_coverage_matrix.py",
    "scripts/enrich_recent_form_v2.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_recent_fixture_statistics.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_injuries_availability.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_fixture_lineups.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_standings_context.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_odds_context_v3.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_tie_context.py",
    "scripts/filter_leagues.py",
    "scripts/score_matches_v3.py",
    "scripts/tie_state_adjust_scores.py",
    "scripts/select_core_candidates.py",
    "scripts/deep_analysis_candidates.py",
    "scripts/final_execution_exports.py",
    "scripts/validate_final_execution_exports.py",
    "scripts/build_today_execution_shortlist.py",
    "scripts/build_execution_pick_modes.py",
    "scripts/build_competition_accuracy_mode.py",
    "scripts/build_match_script_forecasts.py",
]

SHADOW_CANDIDATE_V2_STEP = "scripts/run_today_shadow_candidate_v2.py"
SHADOW_CANDIDATE_V4_STEP = "scripts/run_today_shadow_candidate_v4.py"
SHADOW_CANDIDATE_V5_STEP = "scripts/run_today_shadow_candidate_v5.py"
SHADOW_CANDIDATE_V6_STEP = "scripts/run_today_shadow_candidate_v6.py"
SHADOW_CANDIDATE_V7_STEP = "scripts/run_today_shadow_candidate_v7.py"
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

TODAY_GENERATED_FILES = [
    RAW_MATCHES_CSV,
    RAW_JSON_PATH,
    PROCESSED_DIR / "matches_league_filtered.csv",
    PROCESSED_DIR / "matches_league_rejected.csv",
    PROCESSED_DIR / "league_filter_report.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_matrix.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_summary.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_report.txt",
    PROCESSED_DIR / "recent_fixture_statistics_enrichment_report.csv",
    PROCESSED_DIR / "injuries_availability_enrichment_report.csv",
    PROCESSED_DIR / "fixture_lineups_enrichment_report.csv",
    PROCESSED_DIR / "matches_vsigma_scored_v3.csv",
    PROCESSED_DIR / "vsigma_score_report_v3.csv",
    PROCESSED_DIR / "vsigma_top_candidates_v3.csv",
    PROCESSED_DIR / "tie_state_adjust_report.csv",
    PROCESSED_DIR / "vsigma_core_shortlist.csv",
    PROCESSED_DIR / "vsigma_core_shortlist_report.csv",
    PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_premium_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_standard_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_candidates.csv",
    PROCESSED_DIR / "vsigma_final_downgraded_candidates.csv",
    PROCESSED_DIR / "vsigma_final_blocked_candidates.csv",
    PROCESSED_DIR / "vsigma_final_watch_candidates.csv",
    PROCESSED_DIR / "vsigma_final_governance_summary.csv",
    PROCESSED_DIR / "vsigma_final_export_reconciliation_report.csv",
    PROCESSED_DIR / "vsigma_today_premium_core.csv",
    PROCESSED_DIR / "vsigma_today_execution_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_execution_bets_only.csv",
    PROCESSED_DIR / "vsigma_today_execution_summary.csv",
    PROCESSED_DIR / "vsigma_today_pick_explanations.csv",
    PROCESSED_DIR / "vsigma_today_pick_explanations_report.txt",
    PROCESSED_DIR / "vsigma_today_safe_top5.csv",
    PROCESSED_DIR / "vsigma_today_balanced_top5.csv",
    PROCESSED_DIR / "vsigma_today_aggressive_top5.csv",
    PROCESSED_DIR / "vsigma_today_pick_modes_summary.csv",
    PROCESSED_DIR / "vsigma_today_competition_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_competition_top.csv",
    PROCESSED_DIR / "vsigma_today_competition_report.txt",
    PROCESSED_DIR / "vsigma_today_match_script_forecasts.csv",
    PROCESSED_DIR / "vsigma_today_match_script_forecasts_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v2_competition_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v2_competition_top.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v2_competition_report.txt",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v4_competition_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v4_competition_top.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v4_competition_report.txt",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v5_competition_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v5_competition_top.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v5_competition_report.txt",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v6_competition_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v6_competition_top.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v6_competition_report.txt",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6_report.txt",
    PROCESSED_DIR / "vsigma_today_candidate_v7_competition_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v7_competition_top.csv",
    PROCESSED_DIR / "vsigma_today_candidate_v7_competition_report.txt",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv",
    PROCESSED_DIR / "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7_report.txt",
    PROCESSED_DIR / "vsigma_daily_freshness_report.csv",
    PROCESSED_DIR / "vsigma_daily_freshness_report.txt",
    PROCESSED_DIR / "vsigma_candidate_isolation_report.csv",
    PROCESSED_DIR / "vsigma_candidate_isolation_report.txt",
    PROCESSED_DIR / "vsigma_probability_evaluation_summary.csv",
    PROCESSED_DIR / "vsigma_probability_evaluation_report.txt",
    PROCESSED_DIR / "vsigma_probability_calibration_table.csv",
    PROCESSED_DIR / "vsigma_probability_calibration_report.txt",
]

TODAY_JOURNAL_FILES = [
    PRE_SUMMARY_FILENAME,
]

PER_RUN_OUTPUTS_TO_CLEAR = [
    path for path in TODAY_GENERATED_FILES if path.parent == PROCESSED_DIR
]

STALE_POST_RESULT_OUTPUTS_TO_CLEAR = [
    PROCESSED_DIR / "vsigma_execution_shortlist_results_ledger.csv",
    PROCESSED_DIR / "vsigma_execution_shortlist_results_summary.csv",
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
]


def normalize_fixture_payload(item: dict[str, Any]) -> dict[str, Any]:
    fixture = item.get("fixture", {}) or {}
    league = item.get("league", {}) or {}
    teams = item.get("teams", {}) or {}
    goals = item.get("goals", {}) or {}
    score = item.get("score", {}) or {}

    home = teams.get("home", {}) or {}
    away = teams.get("away", {}) or {}
    status = fixture.get("status", {}) or {}
    fulltime = score.get("fulltime", {}) or {}
    halftime = score.get("halftime", {}) or {}
    extratime = score.get("extratime", {}) or {}
    penalty = score.get("penalty", {}) or {}

    return {
        "date": str(fixture.get("date", ""))[:10],
        "fixture_datetime_utc": fixture.get("date"),
        "fixture_timestamp": fixture.get("timestamp"),
        "league": league.get("name"),
        "league_id": league.get("id"),
        "season": league.get("season"),
        "fixture_id": fixture.get("id"),
        "status": status.get("short"),
        "home_team": home.get("name"),
        "home_team_id": home.get("id"),
        "away_team": away.get("name"),
        "away_team_id": away.get("id"),
        "country": league.get("country"),
        "fixture_status_short": status.get("short"),
        "fixture_status_long": status.get("long"),
        "fixture_status_elapsed": status.get("elapsed"),
        "goals_home": goals.get("home"),
        "goals_away": goals.get("away"),
        "score_fulltime_home": fulltime.get("home"),
        "score_fulltime_away": fulltime.get("away"),
        "score_halftime_home": halftime.get("home"),
        "score_halftime_away": halftime.get("away"),
        "score_extratime_home": extratime.get("home"),
        "score_extratime_away": extratime.get("away"),
        "score_penalty_home": penalty.get("home"),
        "score_penalty_away": penalty.get("away"),
        "home_xg_for": 0.0,
        "home_xg_against": 0.0,
        "away_xg_for": 0.0,
        "away_xg_against": 0.0,
        "home_sot_for": 0.0,
        "away_sot_for": 0.0,
        "home_big_for": 0.0,
        "away_big_for": 0.0,
        "home_motivation": 0.0,
        "away_motivation": 0.0,
        "home_absences": None,
        "away_absences": None,
        "today_pipeline_fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def fetch_today_matches(
    client: APIFootballClient,
    match_date: str,
    timezone_name: str,
) -> tuple[pd.DataFrame, dict[str, int]]:
    payload = client.request(
        "/fixtures",
        params={"date": match_date, "timezone": timezone_name},
        ttl_hours=1,
        force_refresh=True,
    )
    RAW_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = [normalize_fixture_payload(item) for item in payload.get("response", []) or []]
    raw = pd.DataFrame(rows)
    if raw.empty:
        return raw, {"api_fixtures": 0, "upcoming_fixtures": 0}

    statuses = raw["status"].astype(str).str.upper()
    today_rows = raw[raw["date"].astype(str).eq(match_date)].copy()
    upcoming = today_rows[statuses.loc[today_rows.index].isin(UPCOMING_STATUSES)].copy()

    return upcoming.reset_index(drop=True), {
        "api_fixtures": int(len(raw)),
        "local_date_fixtures": int(len(today_rows)),
        "upcoming_fixtures": int(len(upcoming)),
    }


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


def run_shadow_candidate_v2_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V2_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v4_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V4_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v5_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V5_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v6_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V6_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_shadow_candidate_v7_step(match_date: str, timezone_name: str) -> None:
    run_optional_step_with_args(
        SHADOW_CANDIDATE_V7_STEP,
        ["--date", match_date, "--timezone", timezone_name],
    )


def run_odds_clv_pre_steps(match_date: str) -> None:
    run_optional_step_with_args(ODDS_SNAPSHOT_STEP, ["--date", match_date, "--stage", "PRE"])
    run_optional_step_with_args(CLV_REPORT_STEP, ["--date", match_date])
    run_optional_step_with_args(V7_CALIBRATION_ADVISOR_STEP, ["--date", match_date])


def run_daily_hardening_steps(match_date: str) -> None:
    snapshot_dir = TODAY_DIR / match_date
    common_args = ["--date", match_date, "--snapshot-dir", str(snapshot_dir)]
    run_optional_step_with_args(METADATA_STAMP_STEP, [*common_args, "--phase", "pre"])
    run_optional_step_with_args(IMMUTABLE_LEDGER_STEP, ["--date", match_date, "--stage", "PRE"])
    run_optional_step_with_args(EXPERIMENT_PERFORMANCE_STEP, [])
    run_optional_step_with_args(GOVERNANCE_STEP, ["--date", match_date])
    for step in [FRESHNESS_VALIDATION_STEP, CANDIDATE_ISOLATION_STEP, MASTER_REPORT_STEP]:
        run_optional_step_with_args(step, common_args)
    run_optional_step_with_args(SCOREBOARD_STEP, ["--date", match_date])


def clear_previous_today_outputs() -> None:
    for path in [*PER_RUN_OUTPUTS_TO_CLEAR, *STALE_POST_RESULT_OUTPUTS_TO_CLEAR]:
        if path.exists():
            path.unlink()


def clear_stale_snapshot_post_outputs(match_date: str) -> None:
    snapshot_dir = TODAY_DIR / match_date
    for src in STALE_POST_RESULT_OUTPUTS_TO_CLEAR:
        target = snapshot_dir / src.name
        if target.exists():
            target.unlink()


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def snapshot_today_outputs(match_date: str) -> Path:
    dest_dir = TODAY_DIR / match_date
    dest_dir.mkdir(parents=True, exist_ok=True)

    for src in TODAY_GENERATED_FILES:
        copy_if_exists(src, dest_dir)

    return dest_dir


def validate_today_only_outputs(match_date: str) -> None:
    checked_files = [
        PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv",
        PROCESSED_DIR / "vsigma_final_approved_premium_candidates.csv",
        PROCESSED_DIR / "vsigma_final_approved_standard_candidates.csv",
        PROCESSED_DIR / "vsigma_final_approved_candidates.csv",
        PROCESSED_DIR / "vsigma_final_downgraded_candidates.csv",
        PROCESSED_DIR / "vsigma_final_blocked_candidates.csv",
        PROCESSED_DIR / "vsigma_final_watch_candidates.csv",
    ]
    for path in checked_files:
        if not path.exists():
            raise FileNotFoundError(f"Missing today output: {path}")

        df = pd.read_csv(path)
        if df.empty:
            continue
        if "date" not in df.columns:
            raise ValueError(f"{path} is missing date column")

        observed = sorted(df["date"].dropna().astype(str).unique().tolist())
        if observed != [match_date]:
            raise ValueError(f"{path} contains non-today dates: {observed}")


def read_count(path: Path) -> int:
    if not path.exists():
        return 0
    return int(len(pd.read_csv(path)))


def write_run_report(
    match_date: str,
    timezone_name: str,
    fetch_counts: dict[str, int],
    snapshot_dir: Path,
) -> Path:
    report_path = snapshot_dir / "today_pipeline_report.csv"
    row = {
        "date": match_date,
        "timezone": timezone_name,
        **fetch_counts,
        "filtered_rows": read_count(PROCESSED_DIR / "matches_league_filtered.csv"),
        "scored_rows": read_count(PROCESSED_DIR / "matches_vsigma_scored_v3.csv"),
        "shortlist_rows": read_count(PROCESSED_DIR / "vsigma_core_shortlist.csv"),
        "deep_rows": read_count(PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv"),
        "approved_premium_rows": read_count(
            PROCESSED_DIR / "vsigma_final_approved_premium_candidates.csv"
        ),
        "approved_standard_rows": read_count(
            PROCESSED_DIR / "vsigma_final_approved_standard_candidates.csv"
        ),
        "approved_rows": read_count(PROCESSED_DIR / "vsigma_final_approved_candidates.csv"),
        "competition_shortlist_rows": read_count(PROCESSED_DIR / "vsigma_today_competition_shortlist.csv"),
        "competition_top_rows": read_count(PROCESSED_DIR / "vsigma_today_competition_top.csv"),
        "downgraded_rows": read_count(PROCESSED_DIR / "vsigma_final_downgraded_candidates.csv"),
        "blocked_rows": read_count(PROCESSED_DIR / "vsigma_final_blocked_candidates.csv"),
        "watch_rows": read_count(PROCESSED_DIR / "vsigma_final_watch_candidates.csv"),
        "snapshot_dir": str(snapshot_dir),
        "run_finished_at": datetime.now(timezone.utc).isoformat(),
    }
    pd.DataFrame([row]).to_csv(report_path, index=False)
    return report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the production vSIGMA today-match pipeline without historical labeling or backtest."
    )
    parser.add_argument("--date", default=date.today().isoformat(), help="Today date in YYYY-MM-DD.")
    parser.add_argument("--timezone", default="Atlantic/Canary", help="API timezone parameter.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    client = APIFootballClient()
    matches, fetch_counts = fetch_today_matches(client, match_date, args.timezone)

    if matches.empty:
        raise RuntimeError(
            f"No upcoming fixtures found for {match_date} in timezone {args.timezone}."
        )

    clear_previous_today_outputs()
    clear_stale_snapshot_post_outputs(match_date)
    RAW_MATCHES_CSV.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(RAW_MATCHES_CSV, index=False)

    print("\n=== TODAY MATCH PIPELINE ===")
    print(f"Date: {match_date}")
    print(f"Timezone: {args.timezone}")
    print(f"API fixtures: {fetch_counts['api_fixtures']}")
    print(f"Upcoming fixtures kept: {fetch_counts['upcoming_fixtures']}")
    print(f"Raw today CSV: {RAW_MATCHES_CSV}")

    for step in PIPELINE_STEPS:
        run_step(step)

    validate_today_only_outputs(match_date)
    snapshot_dir = snapshot_today_outputs(match_date)
    report_path = write_run_report(match_date, args.timezone, fetch_counts, snapshot_dir)
    pre_journal_path = build_pre_summary(PROCESSED_DIR, TODAY_DIR, match_date, args.timezone)
    run_shadow_candidate_v2_step(match_date, args.timezone)
    run_shadow_candidate_v4_step(match_date, args.timezone)
    run_shadow_candidate_v5_step(match_date, args.timezone)
    run_shadow_candidate_v6_step(match_date, args.timezone)
    run_shadow_candidate_v7_step(match_date, args.timezone)
    run_odds_clv_pre_steps(match_date)
    run_daily_hardening_steps(match_date)

    print("\n=== TODAY MATCH PIPELINE COMPLETADO ===")
    print(f"Snapshot dir: {snapshot_dir}")
    print(f"Run report: {report_path}")
    print(f"Daily pre journal: {pre_journal_path}")
    print(f"Approved premium: {read_count(PROCESSED_DIR / 'vsigma_final_approved_premium_candidates.csv')}")
    print(f"Approved standard: {read_count(PROCESSED_DIR / 'vsigma_final_approved_standard_candidates.csv')}")
    print(f"Approved: {read_count(PROCESSED_DIR / 'vsigma_final_approved_candidates.csv')}")
    print(f"Downgraded: {read_count(PROCESSED_DIR / 'vsigma_final_downgraded_candidates.csv')}")
    print(f"Blocked: {read_count(PROCESSED_DIR / 'vsigma_final_blocked_candidates.csv')}")
    print(f"Watch: {read_count(PROCESSED_DIR / 'vsigma_final_watch_candidates.csv')}")


if __name__ == "__main__":
    main()
