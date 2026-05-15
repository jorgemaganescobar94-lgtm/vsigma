from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from api_football_client import APIFootballClient
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
RAW_JSON_PATH = ROOT / "data" / "raw" / "api_matches.json"
PROCESSED_DIR = ROOT / "data" / "processed"
HISTORICAL_DIR = PROCESSED_DIR / "historical"

STANDARD_DEEP_CSV = PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv"
STANDARD_LABELED_CSV = PROCESSED_DIR / "vsigma_market_results_labeled.csv"
STANDARD_BACKTEST_SOURCE = PROCESSED_DIR / "vsigma_backtest_enriched_source.csv"
STANDARD_CALIBRATION_CANDIDATES = PROCESSED_DIR / "vsigma_threshold_calibration_candidates.csv"

FINISHED_STATUSES = {"FT", "AET", "PEN"}

DEEP_ANALYSIS_STEP = "scripts/deep_analysis_candidates.py"
FINAL_EXECUTION_EXPORT_STEP = "scripts/final_execution_exports.py"
FINAL_EXECUTION_EXPORT_VALIDATION_STEP = "scripts/validate_final_execution_exports.py"
HISTORICAL_EXECUTION_SHORTLIST_BACKTEST_STEP = "scripts/build_historical_execution_shortlist_backtest.py"
EXECUTION_MODE_COMPARISON_STEP = "scripts/build_execution_mode_comparison.py"
FINAL_EXECUTION_RECONCILIATION_REPORT = PROCESSED_DIR / "vsigma_final_export_reconciliation_report.csv"
FINAL_EXECUTION_EXPORT_FILES = [
    PROCESSED_DIR / "vsigma_final_approved_premium_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_standard_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_candidates.csv",
    PROCESSED_DIR / "vsigma_final_downgraded_candidates.csv",
    PROCESSED_DIR / "vsigma_final_blocked_candidates.csv",
    PROCESSED_DIR / "vsigma_final_watch_candidates.csv",
    PROCESSED_DIR / "vsigma_final_governance_summary.csv",
    FINAL_EXECUTION_RECONCILIATION_REPORT,
]

PIPELINE_STEPS_BEFORE_DEEP = [
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
]

PIPELINE_STEPS_AFTER_DEEP = [
    "scripts/refresh_finished_results_by_date.py",
    "scripts/label_market_results.py",
]

SNAPSHOT_FILES = [
    ROOT / "data" / "raw" / "matches.csv",
    PROCESSED_DIR / "matches_league_filtered.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_matrix.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_summary.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_report.txt",
    PROCESSED_DIR / "matches_vsigma_scored_v3.csv",
    PROCESSED_DIR / "recent_fixture_statistics_enrichment_report.csv",
    PROCESSED_DIR / "injuries_availability_enrichment_report.csv",
    PROCESSED_DIR / "fixture_lineups_enrichment_report.csv",
    PROCESSED_DIR / "vsigma_core_shortlist.csv",
    PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv",
    *FINAL_EXECUTION_EXPORT_FILES,
    PROCESSED_DIR / "vsigma_market_results_labeled.csv",
    PROCESSED_DIR / "vsigma_market_results_report.csv",
    PROCESSED_DIR / "refresh_finished_results_by_date_report.csv",
]

PER_DATE_GENERATED_FILES = [
    PROCESSED_DIR / "matches_league_filtered.csv",
    PROCESSED_DIR / "matches_league_rejected.csv",
    PROCESSED_DIR / "league_filter_report.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_matrix.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_summary.csv",
    PROCESSED_DIR / "vsigma_api_league_coverage_report.txt",
    PROCESSED_DIR / "matches_vsigma_scored_v3.csv",
    PROCESSED_DIR / "recent_fixture_statistics_enrichment_report.csv",
    PROCESSED_DIR / "injuries_availability_enrichment_report.csv",
    PROCESSED_DIR / "fixture_lineups_enrichment_report.csv",
    PROCESSED_DIR / "vsigma_score_report_v3.csv",
    PROCESSED_DIR / "vsigma_top_candidates_v3.csv",
    PROCESSED_DIR / "tie_state_adjust_report.csv",
    PROCESSED_DIR / "vsigma_core_shortlist.csv",
    PROCESSED_DIR / "vsigma_core_shortlist_report.csv",
    PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv",
    *FINAL_EXECUTION_EXPORT_FILES,
    PROCESSED_DIR / "vsigma_market_results_labeled.csv",
    PROCESSED_DIR / "vsigma_market_results_report.csv",
    PROCESSED_DIR / "refresh_finished_results_by_date_report.csv",
]


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def date_range(start: date, end: date) -> list[str]:
    if end < start:
        raise ValueError("--end-date cannot be earlier than --start-date")

    out = []
    current = start
    while current <= end:
        out.append(current.isoformat())
        current += timedelta(days=1)
    return out


def default_dates(lookback_days: int) -> list[str]:
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=max(lookback_days - 1, 0))
    return date_range(start, end)


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
        "results_last_refresh_at": datetime.now(timezone.utc).isoformat(),
    }


def fetch_date_matches(client: APIFootballClient, match_date: str, timezone_name: str) -> pd.DataFrame:
    payload = client.fixtures(date=match_date, timezone=timezone_name)
    RAW_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = [normalize_fixture_payload(item) for item in payload.get("response", []) or []]
    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df[df["status"].astype(str).str.upper().isin(FINISHED_STATUSES)].copy()
    return df.reset_index(drop=True)


def run_step(script_path: str) -> None:
    command = [sys.executable, script_path]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    print("\n=== RUNNING ===")
    print(" ".join(command))
    subprocess.run(command, cwd=ROOT, check=True, env=env)


def is_final_execution_validation_error(exc: subprocess.CalledProcessError) -> bool:
    cmd = exc.cmd
    if isinstance(cmd, (list, tuple)):
        return FINAL_EXECUTION_EXPORT_VALIDATION_STEP in {str(part) for part in cmd}
    return FINAL_EXECUTION_EXPORT_VALIDATION_STEP in str(cmd)


def run_deep_analysis_and_final_exports() -> None:
    run_step(DEEP_ANALYSIS_STEP)
    run_step(FINAL_EXECUTION_EXPORT_STEP)
    run_step(FINAL_EXECUTION_EXPORT_VALIDATION_STEP)


def clear_per_date_outputs() -> None:
    for path in PER_DATE_GENERATED_FILES:
        if path.exists():
            path.unlink()


def shortlist_has_rows() -> bool:
    path = PROCESSED_DIR / "vsigma_core_shortlist.csv"
    if not path.exists():
        return False
    try:
        return not pd.read_csv(path).empty
    except Exception:
        return False


def create_relaxed_historical_shortlist(max_rows: int) -> int:
    scored_path = PROCESSED_DIR / "matches_vsigma_scored_v3.csv"
    shortlist_path = PROCESSED_DIR / "vsigma_core_shortlist.csv"
    report_path = PROCESSED_DIR / "vsigma_core_shortlist_report.csv"

    if not scored_path.exists():
        return 0

    scored = pd.read_csv(scored_path)
    if scored.empty:
        return 0

    def text_col(name: str) -> pd.Series:
        if name in scored.columns:
            return scored[name].astype(str)
        return pd.Series("", index=scored.index, dtype="object")

    for col in ["vsigma_pre_score", "league_tier_rank", "home_recent_matches", "away_recent_matches"]:
        if col not in scored.columns:
            scored[col] = pd.NA
        scored[col] = pd.to_numeric(scored[col], errors="coerce")

    has_data = text_col("data_warning").isin(
        [
            "OK_FULL",
            "OK_PRIOR",
            "OK_STANDINGS",
            "OK_PRIOR_STANDINGS",
            "OK_FULL_STATS",
            "OK_PRIOR_STATS",
            "OK_STANDINGS_STATS",
            "OK_PRIOR_STANDINGS_STATS",
        ]
    )
    has_market_hint = text_col("market_family_hint") != "NO_DATA_ENRICHMENT_REQUIRED"
    has_recent_sample = (
        scored["home_recent_matches"].fillna(0).ge(3)
        & scored["away_recent_matches"].fillna(0).ge(3)
    )
    has_odds = text_col("odds_context_v3_status").eq("OK")
    supported_tier = scored["league_tier_rank"].fillna(99).le(3)

    relaxed = scored[has_data & has_market_hint & has_recent_sample & has_odds & supported_tier].copy()
    if relaxed.empty:
        return 0

    relaxed = relaxed.sort_values(
        ["vsigma_pre_score", "league_tier_rank"],
        ascending=[False, True],
        na_position="last",
    ).head(max_rows)

    relaxed["selection_score"] = relaxed["vsigma_pre_score"].fillna(0).round(2)
    relaxed["shortlist_rank"] = range(1, len(relaxed) + 1)
    relaxed["shortlist_bucket"] = "HISTORICAL_RELAXED"
    relaxed.loc[relaxed["shortlist_rank"] <= 5, "shortlist_bucket"] = "CORE_SHORTLIST"
    relaxed.loc[relaxed["shortlist_rank"] <= 2, "shortlist_bucket"] = "TOP_CORE"

    shortlist_path.parent.mkdir(parents=True, exist_ok=True)
    relaxed.to_csv(shortlist_path, index=False)

    report = (
        relaxed.groupby(["shortlist_bucket", "vsigma_priority", "market_family_hint"], dropna=False)
        .size()
        .reset_index(name="matches")
    )
    report["report_note"] = "historical_relaxed_fallback"
    report.to_csv(report_path, index=False)

    print(f"Created relaxed historical shortlist rows={len(relaxed)}")
    return int(len(relaxed))


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def snapshot_date_outputs(match_date: str) -> None:
    date_dir = HISTORICAL_DIR / match_date
    date_dir.mkdir(parents=True, exist_ok=True)

    for src in SNAPSHOT_FILES:
        copy_if_exists(src, date_dir)


def count_graded(path: Path) -> int:
    if not path.exists():
        return 0
    df = pd.read_csv(path)
    if "actionable_result" not in df.columns or "actionable_flag" not in df.columns:
        return 0

    actionable = pd.to_numeric(df["actionable_flag"], errors="coerce").fillna(0).astype(int) == 1
    graded = df["actionable_result"].astype(str).str.upper().isin(["WIN", "LOSS", "PUSH", "VOID"])
    return int((actionable & graded).sum())


def combine_snapshots(dates: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    deep_frames = []
    labeled_frames = []

    for match_date in dates:
        date_dir = HISTORICAL_DIR / match_date
        deep_path = date_dir / "vsigma_deep_analysis_candidates.csv"
        labeled_path = date_dir / "vsigma_market_results_labeled.csv"

        if deep_path.exists():
            deep = pd.read_csv(deep_path)
            if not deep.empty:
                deep["historical_batch_date"] = match_date
                deep_frames.append(deep)

        if labeled_path.exists():
            labeled = pd.read_csv(labeled_path)
            if not labeled.empty:
                labeled["historical_batch_date"] = match_date
                labeled_frames.append(labeled)

    deep_all = pd.concat(deep_frames, ignore_index=True, sort=False) if deep_frames else pd.DataFrame()
    labeled_all = pd.concat(labeled_frames, ignore_index=True, sort=False) if labeled_frames else pd.DataFrame()

    for df in (deep_all, labeled_all):
        if not df.empty and "fixture_id" in df.columns:
            df.drop_duplicates(subset=["fixture_id"], keep="last", inplace=True)

    return deep_all, labeled_all


def write_batch_report(rows: list[dict[str, Any]], before_graded: int, after_graded: int) -> Path:
    report_path = PROCESSED_DIR / "historical_labeling_batch_report.csv"
    report = pd.DataFrame(rows)
    report["graded_before_batch"] = before_graded
    report["graded_after_batch"] = after_graded
    report.to_csv(report_path, index=False)
    return report_path


def validate_expanded_sample(
    before_graded: int,
    after_graded: int,
    min_added_graded: int,
    min_total_graded: int,
) -> None:
    added = after_graded - before_graded
    if after_graded < min_total_graded:
        raise RuntimeError(
            f"Historical batch produced {after_graded} graded bets, below required total {min_total_graded}"
        )
    if min_added_graded > 0 and after_graded <= before_graded and before_graded >= min_total_graded:
        raise RuntimeError(
            f"Historical batch did not expand the graded sample: before={before_graded}, after={after_graded}"
        )
    if min_added_graded > 0 and before_graded > 0 and added < min_added_graded:
        raise RuntimeError(
            f"Historical batch added {added} graded bets, below required minimum {min_added_graded}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build historical vSIGMA labels across multiple past dates, then backtest and calibrate."
    )
    parser.add_argument("--dates", nargs="*", help="Explicit dates in YYYY-MM-DD format.")
    parser.add_argument("--start-date", help="Start date for inclusive date range.")
    parser.add_argument("--end-date", help="End date for inclusive date range.")
    parser.add_argument("--lookback-days", type=int, default=7, help="Default past-date window when no dates are given.")
    parser.add_argument("--timezone", default="Atlantic/Canary", help="API timezone parameter.")
    parser.add_argument("--min-added-graded", type=int, default=1, help="Minimum extra graded bets required.")
    parser.add_argument("--min-total-graded", type=int, default=6, help="Minimum total graded bets required after batch.")
    parser.add_argument(
        "--fallback-top-n",
        type=int,
        default=15,
        help="Rows to promote from scored output when strict shortlist is empty for a historical date.",
    )
    parser.add_argument("--skip-existing", action="store_true", help="Reuse existing per-date snapshots when present.")
    args = parser.parse_args()

    if args.dates:
        dates = sorted({parse_date(value).isoformat() for value in args.dates})
    elif args.start_date or args.end_date:
        if not args.start_date or not args.end_date:
            raise ValueError("--start-date and --end-date must be provided together")
        dates = date_range(parse_date(args.start_date), parse_date(args.end_date))
    else:
        dates = default_dates(args.lookback_days)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    HISTORICAL_DIR.mkdir(parents=True, exist_ok=True)

    before_graded = count_graded(STANDARD_LABELED_CSV)
    client = APIFootballClient()

    report_rows = []

    print("\n=== HISTORICAL LABELING PIPELINE ===")
    print(f"Dates: {dates}")
    print(f"Graded before batch: {before_graded}")

    for match_date in dates:
        date_dir = HISTORICAL_DIR / match_date
        existing_labeled = date_dir / "vsigma_market_results_labeled.csv"

        if args.skip_existing and existing_labeled.exists():
            graded = count_graded(existing_labeled)
            report_rows.append(
                {
                    "date": match_date,
                    "status": "SKIPPED_EXISTING",
                    "fixtures_fetched": pd.NA,
                    "graded_bets": graded,
                }
            )
            print(f"SKIP existing date={match_date} graded={graded}")
            continue

        print(f"\n=== DATE {match_date} ===")
        fetched = fetch_date_matches(client, match_date, args.timezone)

        if fetched.empty:
            report_rows.append(
                {
                    "date": match_date,
                    "status": "NO_FINISHED_FIXTURES",
                    "fixtures_fetched": 0,
                    "graded_bets": 0,
                }
            )
            print(f"No finished fixtures for {match_date}")
            continue

        clear_per_date_outputs()
        RAW_MATCHES_CSV.parent.mkdir(parents=True, exist_ok=True)
        fetched.to_csv(RAW_MATCHES_CSV, index=False)

        status = "OK"
        error_note = ""
        fallback_rows = 0
        try:
            for step in PIPELINE_STEPS_BEFORE_DEEP:
                run_step(step)

            if not shortlist_has_rows():
                fallback_rows = create_relaxed_historical_shortlist(args.fallback_top_n)

            if not shortlist_has_rows():
                status = "NO_CANDIDATES"
                error_note = "No strict or relaxed candidates produced for date."
                snapshot_date_outputs(match_date)
                report_rows.append(
                    {
                        "date": match_date,
                        "status": status,
                        "fixtures_fetched": len(fetched),
                        "relaxed_fallback_rows": fallback_rows,
                        "graded_bets": 0,
                        "note": error_note,
                    }
                )
                print(f"NO_CANDIDATES date={match_date}")
                continue

            run_deep_analysis_and_final_exports()

            if not STANDARD_DEEP_CSV.exists() or pd.read_csv(STANDARD_DEEP_CSV).empty:
                status = "NO_DEEP_CANDIDATES"
                error_note = "Deep analysis did not produce candidates."
                snapshot_date_outputs(match_date)
                report_rows.append(
                    {
                        "date": match_date,
                        "status": status,
                        "fixtures_fetched": len(fetched),
                        "relaxed_fallback_rows": fallback_rows,
                        "graded_bets": 0,
                        "note": error_note,
                    }
                )
                print(f"NO_DEEP_CANDIDATES date={match_date}")
                continue

            for step in PIPELINE_STEPS_AFTER_DEEP:
                run_step(step)

            snapshot_date_outputs(match_date)
        except subprocess.CalledProcessError as exc:
            status = "ERROR"
            error_note = f"{exc.cmd} exited with {exc.returncode}"
            snapshot_date_outputs(match_date)
            print(f"ERROR date={match_date}: {error_note}")
            if is_final_execution_validation_error(exc):
                raise

        graded = count_graded(existing_labeled)
        report_rows.append(
            {
                "date": match_date,
                "status": status,
                "fixtures_fetched": len(fetched),
                "relaxed_fallback_rows": fallback_rows,
                "graded_bets": graded,
                "note": error_note,
            }
        )

    deep_all, labeled_all = combine_snapshots(dates)
    if deep_all.empty or labeled_all.empty:
        raise RuntimeError("Historical batch did not produce combined deep/labeled outputs.")

    deep_all.to_csv(STANDARD_DEEP_CSV, index=False)
    labeled_all.to_csv(STANDARD_LABELED_CSV, index=False)

    run_step(FINAL_EXECUTION_EXPORT_STEP)
    run_step(FINAL_EXECUTION_EXPORT_VALIDATION_STEP)
    run_step("scripts/run_vsigma_backtest_calibration.py")
    run_step(HISTORICAL_EXECUTION_SHORTLIST_BACKTEST_STEP)
    run_step(EXECUTION_MODE_COMPARISON_STEP)

    after_graded = count_graded(STANDARD_LABELED_CSV)
    validate_expanded_sample(before_graded, after_graded, args.min_added_graded, args.min_total_graded)

    report_path = write_batch_report(report_rows, before_graded, after_graded)

    if not STANDARD_BACKTEST_SOURCE.exists():
        raise RuntimeError(f"Expected backtest source was not generated: {STANDARD_BACKTEST_SOURCE}")
    if not STANDARD_CALIBRATION_CANDIDATES.exists():
        raise RuntimeError(f"Expected calibration candidates were not generated: {STANDARD_CALIBRATION_CANDIDATES}")

    print("\n=== HISTORICAL LABELING PIPELINE COMPLETADO ===")
    print(f"Combined deep rows: {len(deep_all)}")
    print(f"Combined labeled rows: {len(labeled_all)}")
    print(f"Graded before batch: {before_graded}")
    print(f"Graded after batch: {after_graded}")
    print(f"Batch report: {report_path}")


if __name__ == "__main__":
    main()
