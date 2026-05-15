from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_daily_decision_journal import build_shadow_candidate_v2_pre_summary
except ModuleNotFoundError:
    from scripts.build_daily_decision_journal import build_shadow_candidate_v2_pre_summary


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_COMPETITION_SHORTLIST = PROCESSED_DIR / "vsigma_today_competition_shortlist.csv"
BASELINE_COMPETITION_TOP = PROCESSED_DIR / "vsigma_today_competition_top.csv"
BASELINE_COMPETITION_REPORT = PROCESSED_DIR / "vsigma_today_competition_report.txt"

CANDIDATE_OUTPUT_MAP = {
    "vsigma_today_execution_shortlist.csv": "vsigma_today_candidate_v2_execution_shortlist.csv",
    "vsigma_today_execution_bets_only.csv": "vsigma_today_candidate_v2_execution_bets_only.csv",
    "vsigma_today_execution_summary.csv": "vsigma_today_candidate_v2_execution_summary.csv",
    "vsigma_today_competition_shortlist.csv": "vsigma_today_candidate_v2_competition_shortlist.csv",
    "vsigma_today_competition_top.csv": "vsigma_today_candidate_v2_competition_top.csv",
    "vsigma_today_competition_report.txt": "vsigma_today_candidate_v2_competition_report.txt",
    "vsigma_today_match_script_forecasts.csv": "vsigma_today_candidate_v2_match_script_forecasts.csv",
    "vsigma_today_match_script_forecasts_report.txt": "vsigma_today_candidate_v2_match_script_forecasts_report.txt",
    "vsigma_deep_analysis_candidates.csv": "vsigma_today_candidate_v2_deep_analysis_candidates.csv",
    "matches_vsigma_scored_v3.csv": "vsigma_today_candidate_v2_scored_v3.csv",
    "vsigma_schedule_strength_summary.csv": "vsigma_today_candidate_v2_schedule_strength_summary.csv",
    "vsigma_schedule_strength_report.txt": "vsigma_today_candidate_v2_schedule_strength_report.txt",
    "vsigma_recent_anomaly_summary.csv": "vsigma_today_candidate_v2_recent_anomaly_summary.csv",
    "vsigma_recent_anomaly_report.txt": "vsigma_today_candidate_v2_recent_anomaly_report.txt",
}

COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2.csv"
COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_report.txt"
SHADOW_RUN_REPORT = "today_shadow_candidate_v2_report.csv"

SHADOW_STEPS = [
    "scripts/filter_leagues.py",
    "scripts/build_api_league_coverage_matrix.py",
    "scripts/enrich_recent_schedule_strength.py",
    "scripts/enrich_recent_fixture_anomaly_flags.py",
    "scripts/filter_leagues.py",
    "scripts/score_matches_v3.py",
    "scripts/tie_state_adjust_scores.py",
    "scripts/select_core_candidates.py",
    "scripts/deep_analysis_candidates.py",
    "scripts/final_execution_exports.py",
    "scripts/validate_final_execution_exports.py",
    "scripts/build_today_execution_shortlist.py",
    "scripts/build_competition_accuracy_mode.py",
    "scripts/build_match_script_forecasts.py",
]

MUTATED_PROCESSED_FILENAMES = [
    "matches_league_filtered.csv",
    "matches_league_rejected.csv",
    "league_filter_report.csv",
    "vsigma_api_league_coverage_matrix.csv",
    "vsigma_api_league_coverage_summary.csv",
    "vsigma_api_league_coverage_report.txt",
    "vsigma_schedule_strength_summary.csv",
    "vsigma_schedule_strength_report.txt",
    "vsigma_recent_anomaly_summary.csv",
    "vsigma_recent_anomaly_report.txt",
    "matches_vsigma_scored_v3.csv",
    "vsigma_score_report_v3.csv",
    "vsigma_top_candidates_v3.csv",
    "tie_state_adjust_report.csv",
    "vsigma_core_shortlist.csv",
    "vsigma_core_shortlist_report.csv",
    "vsigma_deep_analysis_candidates.csv",
    "vsigma_final_approved_premium_candidates.csv",
    "vsigma_final_approved_standard_candidates.csv",
    "vsigma_final_approved_candidates.csv",
    "vsigma_final_downgraded_candidates.csv",
    "vsigma_final_blocked_candidates.csv",
    "vsigma_final_watch_candidates.csv",
    "vsigma_final_governance_summary.csv",
    "vsigma_final_export_reconciliation_report.csv",
    "vsigma_today_premium_core.csv",
    "vsigma_today_execution_shortlist.csv",
    "vsigma_today_execution_bets_only.csv",
    "vsigma_today_execution_summary.csv",
    "vsigma_today_pick_explanations.csv",
    "vsigma_today_pick_explanations_report.txt",
    "vsigma_today_competition_shortlist.csv",
    "vsigma_today_competition_top.csv",
    "vsigma_today_competition_report.txt",
    "vsigma_today_match_script_forecasts.csv",
    "vsigma_today_match_script_forecasts_report.txt",
    "vsigma_probability_evaluation_summary.csv",
    "vsigma_probability_evaluation_report.txt",
    "vsigma_probability_calibration_table.csv",
    "vsigma_probability_calibration_report.txt",
]

OFFICIAL_FROZEN_FILES = [
    RAW_MATCHES_CSV,
    BASELINE_COMPETITION_SHORTLIST,
    BASELINE_COMPETITION_TOP,
    BASELINE_COMPETITION_REPORT,
    PROCESSED_DIR / "vsigma_today_execution_shortlist.csv",
    PROCESSED_DIR / "vsigma_today_execution_bets_only.csv",
    PROCESSED_DIR / "vsigma_today_execution_summary.csv",
]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def file_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def read_text_optional(path: Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def run_step(script_path: str) -> None:
    command = [sys.executable, script_path]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    print("\n=== SHADOW CANDIDATE V2 RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True, env=env)


def copy_if_exists(src: Path, dest_dir: Path, dest_name: str | None = None) -> Path | None:
    if not src.exists():
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / (dest_name or src.name)
    shutil.copy2(src, dest)
    return dest


def backup_live_files(paths: list[Path], backup_dir: Path) -> dict[Path, bool]:
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    existed: dict[Path, bool] = {}
    for path in paths:
        existed[path] = path.exists()
        if path.exists():
            dest = backup_dir / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    return existed


def restore_live_files(paths: list[Path], backup_dir: Path, existed: dict[Path, bool]) -> None:
    for path in paths:
        backup = backup_dir / path.relative_to(ROOT)
        if existed.get(path, False):
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, path)
        elif path.exists():
            path.unlink()


def validate_baseline_date(match_date: str) -> None:
    for path in [RAW_MATCHES_CSV, BASELINE_COMPETITION_SHORTLIST, BASELINE_COMPETITION_TOP]:
        if not path.exists():
            raise FileNotFoundError(f"Missing baseline prerequisite for shadow run: {path}")

    raw = read_csv_optional(RAW_MATCHES_CSV)
    if raw.empty:
        raise RuntimeError(f"Raw matches file is empty: {RAW_MATCHES_CSV}")
    if "date" in raw.columns:
        observed = sorted({str(value)[:10] for value in raw["date"].dropna().tolist()})
        if observed and observed != [match_date]:
            raise ValueError(f"Raw matches dates {observed} do not match requested date {match_date}.")


def comparison_key(df: pd.DataFrame) -> pd.Series:
    fixture = df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()
    market = df.get("market_primary", pd.Series("", index=df.index)).astype(str).str.strip().str.upper()
    return fixture + "::" + market


def first_available(row: pd.Series, columns: list[str]) -> object:
    for col in columns:
        if col in row.index and pd.notna(row.get(col)) and norm_text(row.get(col)):
            return row.get(col)
    return pd.NA


def build_baseline_candidate_comparison(baseline: pd.DataFrame, candidate: pd.DataFrame) -> pd.DataFrame:
    baseline = baseline.copy()
    candidate = candidate.copy()
    baseline["_compare_key"] = comparison_key(baseline) if not baseline.empty else pd.Series(dtype=str)
    candidate["_compare_key"] = comparison_key(candidate) if not candidate.empty else pd.Series(dtype=str)

    baseline_by_key = {
        key: row for key, row in baseline.drop_duplicates("_compare_key").set_index("_compare_key").iterrows()
    }
    candidate_by_key = {
        key: row for key, row in candidate.drop_duplicates("_compare_key").set_index("_compare_key").iterrows()
    }

    rows: list[dict[str, object]] = []
    for key in sorted(set(baseline_by_key) | set(candidate_by_key)):
        b = baseline_by_key.get(key, pd.Series(dtype=object))
        c = candidate_by_key.get(key, pd.Series(dtype=object))
        exists_b = not b.empty
        exists_c = not c.empty
        if exists_b and exists_c:
            status = "BOTH"
        elif exists_b:
            status = "BASELINE_ONLY"
        else:
            status = "CANDIDATE_V2_ONLY"
        row_source = b if exists_b else c
        rows.append(
            {
                "comparison_status": status,
                "fixture_id": first_available(row_source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(row_source, ['home_team']))} vs {norm_text(first_available(row_source, ['away_team']))}",
                "league": first_available(row_source, ["league"]),
                "baseline_rank": first_available(b, ["accuracy_mode_rank", "execution_rank"]) if exists_b else pd.NA,
                "candidate_v2_rank": first_available(c, ["accuracy_mode_rank", "execution_rank"]) if exists_c else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if exists_b else pd.NA,
                "candidate_v2_market": first_available(c, ["market_primary"]) if exists_c else pd.NA,
                "baseline_raw_prob": first_available(b, ["competition_raw_prob", "primary_model_prob"]) if exists_b else pd.NA,
                "candidate_v2_raw_prob": first_available(c, ["competition_raw_prob", "primary_model_prob"]) if exists_c else pd.NA,
                "baseline_calibrated_prob": first_available(b, ["competition_calibrated_prob"]) if exists_b else pd.NA,
                "candidate_v2_calibrated_prob": first_available(c, ["competition_calibrated_prob"]) if exists_c else pd.NA,
                "baseline_confidence_score": first_available(b, ["accuracy_confidence_score", "execution_score"]) if exists_b else pd.NA,
                "candidate_v2_confidence_score": first_available(c, ["accuracy_confidence_score", "execution_score"]) if exists_c else pd.NA,
                "baseline_bucket": first_available(b, ["accuracy_mode_bucket", "execution_shortlist_source", "final_execution_bucket"]) if exists_b else pd.NA,
                "candidate_v2_bucket": first_available(c, ["accuracy_mode_bucket", "execution_shortlist_source", "final_execution_bucket"]) if exists_c else pd.NA,
                "baseline_main_reason": first_available(b, ["accuracy_mode_reason", "pick_main_why", "reason_1"]) if exists_b else pd.NA,
                "candidate_v2_main_reason": first_available(c, ["accuracy_mode_reason", "pick_main_why", "reason_1"]) if exists_c else pd.NA,
                "baseline_primary_risk": first_available(b, ["accuracy_primary_risk", "pick_primary_risk"]) if exists_b else pd.NA,
                "candidate_v2_primary_risk": first_available(c, ["accuracy_primary_risk", "pick_primary_risk"]) if exists_c else pd.NA,
            }
        )
    return pd.DataFrame(rows)


def write_comparison_report(path: Path, baseline: pd.DataFrame, candidate: pd.DataFrame, comparison: pd.DataFrame) -> None:
    counts = comparison["comparison_status"].value_counts().to_dict() if not comparison.empty else {}
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2",
        "",
        "Baseline: official frozen Competition Accuracy Mode + Probability Calibration.",
        "Candidate v2: SHADOW experimental schedule-strength + anomaly-cleaning layer.",
        "",
        f"Baseline official picks: {len(baseline)}",
        f"Candidate v2 shadow picks: {len(candidate)}",
        f"Overlap: {int(counts.get('BOTH', 0))}",
        f"Only baseline chose: {int(counts.get('BASELINE_ONLY', 0))}",
        f"Only candidate chose: {int(counts.get('CANDIDATE_V2_ONLY', 0))}",
        "",
        "Side-by-side picks",
    ]
    if comparison.empty:
        lines.append("No comparable rows.")
    else:
        display_cols = [
            "comparison_status",
            "fixture",
            "baseline_rank",
            "candidate_v2_rank",
            "baseline_market",
            "candidate_v2_market",
            "baseline_calibrated_prob",
            "candidate_v2_calibrated_prob",
            "baseline_confidence_score",
            "candidate_v2_confidence_score",
        ]
        lines.append(comparison[[c for c in display_cols if c in comparison.columns]].to_string(index=False))
        diff = comparison[comparison["comparison_status"].ne("BOTH")].copy()
        lines.extend(["", "Reason differences"])
        if diff.empty:
            lines.append("All compared picks overlap. Review probability/confidence deltas in the CSV.")
        else:
            reason_cols = [
                "comparison_status",
                "fixture",
                "baseline_main_reason",
                "candidate_v2_main_reason",
                "baseline_primary_risk",
                "candidate_v2_primary_risk",
            ]
            lines.append(diff[[c for c in reason_cols if c in diff.columns]].to_string(index=False))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def copy_candidate_outputs(processed_dir: Path, snapshot_dir: Path) -> list[Path]:
    copied: list[Path] = []
    for source_name, candidate_name in CANDIDATE_OUTPUT_MAP.items():
        live_copy = copy_if_exists(processed_dir / source_name, processed_dir, candidate_name)
        snap_copy = copy_if_exists(processed_dir / source_name, snapshot_dir, candidate_name)
        if live_copy is not None:
            copied.append(live_copy)
        if snap_copy is not None:
            copied.append(snap_copy)
    return copied


def write_shadow_outputs(
    processed_dir: Path,
    today_dir: Path,
    match_date: str,
    timezone_name: str,
    baseline_shortlist: pd.DataFrame,
    candidate_shortlist: pd.DataFrame,
) -> dict[str, Path]:
    snapshot_dir = today_dir / match_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    copy_candidate_outputs(processed_dir, snapshot_dir)

    comparison = build_baseline_candidate_comparison(baseline_shortlist, candidate_shortlist)
    comparison_path = processed_dir / COMPARISON_CSV
    comparison_report_path = processed_dir / COMPARISON_REPORT
    comparison.to_csv(comparison_path, index=False)
    write_comparison_report(comparison_report_path, baseline_shortlist, candidate_shortlist, comparison)
    copy_if_exists(comparison_path, snapshot_dir)
    copy_if_exists(comparison_report_path, snapshot_dir)

    report_path = processed_dir / SHADOW_RUN_REPORT
    row = {
        "date": match_date,
        "timezone": timezone_name,
        "mode": "SHADOW_CANDIDATE_V2",
        "baseline_competition_rows": int(len(baseline_shortlist)),
        "candidate_v2_competition_rows": int(len(candidate_shortlist)),
        "overlap_rows": int(comparison["comparison_status"].eq("BOTH").sum()) if not comparison.empty else 0,
        "baseline_only_rows": int(comparison["comparison_status"].eq("BASELINE_ONLY").sum()) if not comparison.empty else 0,
        "candidate_v2_only_rows": int(comparison["comparison_status"].eq("CANDIDATE_V2_ONLY").sum()) if not comparison.empty else 0,
        "official_baseline_preserved": 1,
        "run_finished_at": datetime.now(timezone.utc).isoformat(),
    }
    pd.DataFrame([row]).to_csv(report_path, index=False)
    copy_if_exists(report_path, snapshot_dir)

    journal_path = build_shadow_candidate_v2_pre_summary(processed_dir, today_dir, match_date, timezone_name)

    return {
        "candidate_shortlist": processed_dir / "vsigma_today_candidate_v2_competition_shortlist.csv",
        "candidate_top": processed_dir / "vsigma_today_candidate_v2_competition_top.csv",
        "candidate_report": processed_dir / "vsigma_today_candidate_v2_competition_report.txt",
        "candidate_match_script_forecasts": processed_dir / "vsigma_today_candidate_v2_match_script_forecasts.csv",
        "candidate_match_script_forecasts_report": processed_dir / "vsigma_today_candidate_v2_match_script_forecasts_report.txt",
        "comparison_csv": comparison_path,
        "comparison_report": comparison_report_path,
        "shadow_run_report": report_path,
        "shadow_pre_journal": journal_path,
    }


def validate_official_hashes(before: dict[Path, str | None]) -> None:
    changed = []
    for path, expected_hash in before.items():
        observed = file_hash(path)
        if observed != expected_hash:
            changed.append(str(path))
    if changed:
        raise RuntimeError(f"Shadow candidate v2 changed official baseline files: {changed}")


def run_shadow_candidate_v2(match_date: str, timezone_name: str) -> dict[str, Path]:
    validate_baseline_date(match_date)
    baseline_shortlist = read_csv_optional(BASELINE_COMPETITION_SHORTLIST)
    official_hashes = {path: file_hash(path) for path in OFFICIAL_FROZEN_FILES}

    backup_paths = sorted(
        set([RAW_MATCHES_CSV, *[PROCESSED_DIR / name for name in MUTATED_PROCESSED_FILENAMES]]),
        key=lambda value: str(value),
    )
    backup_dir = PROCESSED_DIR / "_shadow_candidate_v2_live_backup"
    existed = backup_live_files(backup_paths, backup_dir)

    try:
        print("\n=== TODAY SHADOW CANDIDATE V2 ===")
        print(f"Date: {match_date}")
        print(f"Timezone: {timezone_name}")
        print("Mode: SHADOW experimental schedule-strength + anomaly cleaning")
        for step in SHADOW_STEPS:
            run_step(step)

        candidate_shortlist = read_csv_optional(PROCESSED_DIR / "vsigma_today_competition_shortlist.csv")
        paths = write_shadow_outputs(
            PROCESSED_DIR,
            TODAY_DIR,
            match_date,
            timezone_name,
            baseline_shortlist,
            candidate_shortlist,
        )
    finally:
        restore_live_files(backup_paths, backup_dir, existed)

    validate_official_hashes(official_hashes)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run candidate v2 in daily shadow mode without replacing official competition outputs."
    )
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = run_shadow_candidate_v2(match_date, args.timezone)

    print("\n=== TODAY SHADOW CANDIDATE V2 COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    print("Official baseline files restored and hash-verified.")


if __name__ == "__main__":
    main()
