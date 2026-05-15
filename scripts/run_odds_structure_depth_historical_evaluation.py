from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_execution_mode_comparison import build_execution_mode_comparison
    from build_historical_execution_shortlist_backtest import build_historical_execution_shortlist_backtest
    from run_historical_labeling_pipeline import PER_DATE_GENERATED_FILES, create_relaxed_historical_shortlist
except ModuleNotFoundError:
    from scripts.build_execution_mode_comparison import build_execution_mode_comparison
    from scripts.build_historical_execution_shortlist_backtest import build_historical_execution_shortlist_backtest
    from scripts.run_historical_labeling_pipeline import PER_DATE_GENERATED_FILES, create_relaxed_historical_shortlist


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
LAB_ROOT = PROCESSED_DIR / "recent_lab_historical"
V3_ROOT = LAB_ROOT / "odds_structure_depth"
V3_HISTORICAL_DIR = V3_ROOT / "historical"

COMPARISON_OUTPUT = LAB_ROOT / "vsigma_odds_structure_depth_comparison.csv"
COMPARISON_REPORT = LAB_ROOT / "vsigma_odds_structure_depth_comparison_report.txt"

LAB_OUTPUT_FILES = [
    PROCESSED_DIR / "vsigma_schedule_strength_summary.csv",
    PROCESSED_DIR / "vsigma_schedule_strength_report.txt",
    PROCESSED_DIR / "vsigma_recent_anomaly_summary.csv",
    PROCESSED_DIR / "vsigma_recent_anomaly_report.txt",
    PROCESSED_DIR / "vsigma_odds_structure_depth_summary.csv",
    PROCESSED_DIR / "vsigma_odds_structure_depth_report.txt",
]

SNAPSHOT_FILES = [
    RAW_MATCHES,
    PROCESSED_DIR / "matches_league_filtered.csv",
    PROCESSED_DIR / "matches_vsigma_scored_v3.csv",
    PROCESSED_DIR / "vsigma_core_shortlist.csv",
    PROCESSED_DIR / "vsigma_deep_analysis_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_premium_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_standard_candidates.csv",
    PROCESSED_DIR / "vsigma_final_approved_candidates.csv",
    PROCESSED_DIR / "vsigma_final_downgraded_candidates.csv",
    PROCESSED_DIR / "vsigma_final_blocked_candidates.csv",
    PROCESSED_DIR / "vsigma_final_watch_candidates.csv",
    PROCESSED_DIR / "vsigma_final_governance_summary.csv",
    PROCESSED_DIR / "vsigma_final_export_reconciliation_report.csv",
    PROCESSED_DIR / "vsigma_market_results_labeled.csv",
    PROCESSED_DIR / "vsigma_market_results_report.csv",
    *LAB_OUTPUT_FILES,
]

V3_STEPS_BEFORE_DEEP = [
    "scripts/filter_leagues.py",
    "scripts/build_api_league_coverage_matrix.py",
    "scripts/enrich_recent_schedule_strength.py",
    "scripts/enrich_recent_fixture_anomaly_flags.py",
    "scripts/filter_leagues.py",
    "scripts/enrich_odds_structure_depth.py",
    "scripts/filter_leagues.py",
    "scripts/score_matches_v3.py",
    "scripts/tie_state_adjust_scores.py",
    "scripts/select_core_candidates.py",
]

V3_STEPS_AFTER_DEEP = [
    "scripts/deep_analysis_candidates.py",
    "scripts/final_execution_exports.py",
    "scripts/validate_final_execution_exports.py",
    "scripts/label_market_results.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate candidate v3: recent lab v2 plus odds-structure-depth market translation."
    )
    parser.add_argument("--start-date", default="2026-04-23")
    parser.add_argument("--end-date", default="2026-05-08")
    parser.add_argument("--fallback-top-n", type=int, default=15)
    return parser.parse_args()


def read_table(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def date_dirs(start: str, end: str) -> list[Path]:
    if not BASELINE_HISTORICAL_DIR.exists():
        return []
    return [
        path
        for path in sorted(BASELINE_HISTORICAL_DIR.iterdir())
        if path.is_dir() and start <= path.name <= end
    ]


def run_step(script_path: str) -> None:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    subprocess.run([sys.executable, script_path], cwd=ROOT, env=env, check=True)


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


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


def clear_generated_outputs() -> None:
    for path in [*PER_DATE_GENERATED_FILES, *LAB_OUTPUT_FILES]:
        if path.exists():
            path.unlink()


def shortlist_empty() -> bool:
    path = PROCESSED_DIR / "vsigma_core_shortlist.csv"
    if not path.exists():
        return True
    try:
        return pd.read_csv(path).empty
    except Exception:
        return True


def run_one_date(date_dir: Path, fallback_top_n: int) -> dict[str, Any]:
    source_raw = date_dir / "matches.csv"
    if not source_raw.exists():
        return {"date": date_dir.name, "status": "MISSING_MATCHES", "rows": 0}

    clear_generated_outputs()
    RAW_MATCHES.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_raw, RAW_MATCHES)

    for step in V3_STEPS_BEFORE_DEEP:
        run_step(step)

    fallback_rows = 0
    if shortlist_empty():
        fallback_rows = create_relaxed_historical_shortlist(fallback_top_n)
    if shortlist_empty():
        return {"date": date_dir.name, "status": "NO_CANDIDATES", "rows": 0, "fallback_rows": fallback_rows}

    for step in V3_STEPS_AFTER_DEEP:
        run_step(step)

    out_dir = V3_HISTORICAL_DIR / date_dir.name
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in SNAPSHOT_FILES:
        copy_if_exists(path, out_dir)

    labeled = pd.read_csv(PROCESSED_DIR / "vsigma_market_results_labeled.csv")
    graded = labeled["actionable_result"].astype(str).str.upper().isin(["WIN", "LOSS", "PUSH", "VOID"])
    return {
        "date": date_dir.name,
        "status": "OK",
        "rows": int(len(labeled)),
        "graded_rows": int(graded.sum()),
        "fallback_rows": fallback_rows,
    }


def metric_row(label: str, output_dir: Path) -> dict[str, object]:
    overall = read_table(output_dir / "vsigma_execution_mode_comparison_overall.csv")
    probability = read_table(output_dir / "vsigma_probability_evaluation_summary.csv")
    competition = overall[overall["mode"].eq("COMPETITION_ACCURACY_MODE")] if not overall.empty else pd.DataFrame()
    probability_comp = (
        probability[
            probability.get("summary_scope", pd.Series(dtype=object)).astype(str).eq("mode")
            & probability.get("segment", pd.Series(dtype=object)).astype(str).eq("COMPETITION_ACCURACY_MODE")
        ]
        if not probability.empty
        else pd.DataFrame()
    )
    row = competition.iloc[0].to_dict() if not competition.empty else {}
    prob = probability_comp.iloc[0].to_dict() if not probability_comp.empty else {}
    return {
        "variant": label,
        "rows": row.get("rows_total", 0),
        "graded_rows": row.get("graded_rows", 0),
        "wins": row.get("wins", 0),
        "losses": row.get("losses", 0),
        "hit_rate": row.get("hit_rate", pd.NA),
        "profit": row.get("profit_units_total", 0.0),
        "roi": row.get("roi_percent", pd.NA),
        "brier": prob.get("brier_score_calibrated", prob.get("brier_score", pd.NA)),
        "avg_probability": prob.get("avg_probability_calibrated", pd.NA),
    }


def count_market_changes(left_path: Path, right_path: Path) -> int:
    left = read_table(left_path)
    right = read_table(right_path)
    if left.empty or right.empty:
        return 0
    key_cols = ["historical_batch_date", "fixture_id"]
    if any(col not in left.columns for col in key_cols) or any(col not in right.columns for col in key_cols):
        return 0
    merged = left[key_cols + ["market_primary"]].merge(
        right[key_cols + ["market_primary"]],
        on=key_cols,
        how="inner",
        suffixes=("_left", "_right"),
    )
    if merged.empty:
        return 0
    return int(merged["market_primary_left"].astype(str).ne(merged["market_primary_right"].astype(str)).sum())


def build_comparison() -> pd.DataFrame:
    rows = [
        metric_row("FROZEN_BASELINE", PROCESSED_DIR),
        metric_row("CANDIDATE_V2_RECENT_LAB", LAB_ROOT),
        metric_row("CANDIDATE_V3_ODDS_STRUCTURE_DEPTH", V3_ROOT),
    ]
    comparison = pd.DataFrame(rows)
    v2_historical = LAB_ROOT / "vsigma_execution_shortlist_historical.csv"
    v3_historical = V3_ROOT / "vsigma_execution_shortlist_historical.csv"
    comparison["market_changes_vs_candidate_v2"] = 0
    comparison.loc[
        comparison["variant"].eq("CANDIDATE_V3_ODDS_STRUCTURE_DEPTH"),
        "market_changes_vs_candidate_v2",
    ] = count_market_changes(v2_historical, v3_historical)
    return comparison


def write_comparison_report(batch: pd.DataFrame, comparison: pd.DataFrame) -> None:
    market_v3 = read_table(V3_ROOT / "vsigma_execution_mode_comparison_by_market.csv")
    bucket_v3 = read_table(V3_ROOT / "vsigma_execution_mode_comparison_by_bucket.csv")
    lines = [
        "vSIGMA ODDS STRUCTURE DEPTH HISTORICAL EVALUATION",
        "",
        "Variant definitions",
        "FROZEN_BASELINE: official competition accuracy mode + probability calibration.",
        "CANDIDATE_V2_RECENT_LAB: schedule strength + anomaly cleaning.",
        "CANDIDATE_V3_ODDS_STRUCTURE_DEPTH: candidate v2 plus odds ladder/dispersion market translation.",
        "",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Batch status",
        batch.to_string(index=False) if not batch.empty else "No batch rows.",
        "",
        "Baseline vs candidate v2 vs candidate v3",
        comparison.to_string(index=False) if not comparison.empty else "No comparison rows.",
        "",
        "Candidate v3 market-family composition",
        market_v3.to_string(index=False) if not market_v3.empty else "No market rows.",
        "",
        "Candidate v3 CORE / EXTENDED composition",
        bucket_v3.to_string(index=False) if not bucket_v3.empty else "No bucket rows.",
        "",
        "Interpretation",
        (
            "This layer is intended to change market translation and confidence modestly. "
            "Thin/no odds depth is neutral uncertainty. Any observed gain should be read as sample-sensitive "
            "unless it persists across larger labeled windows."
        ),
        "",
    ]
    COMPARISON_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    dirs = date_dirs(args.start_date, args.end_date)
    if not dirs:
        raise RuntimeError("No historical date directories found for requested range.")

    V3_ROOT.mkdir(parents=True, exist_ok=True)
    if V3_HISTORICAL_DIR.exists():
        shutil.rmtree(V3_HISTORICAL_DIR)
    V3_HISTORICAL_DIR.mkdir(parents=True, exist_ok=True)

    backup_paths = sorted(set([RAW_MATCHES, *PER_DATE_GENERATED_FILES, *LAB_OUTPUT_FILES]), key=lambda path: str(path))
    backup_dir = V3_ROOT / "_live_backup"
    existed = backup_live_files(backup_paths, backup_dir)

    batch_rows = []
    try:
        for date_dir in dirs:
            print(f"\n=== ODDS STRUCTURE DEPTH HISTORICAL DATE {date_dir.name} ===")
            batch_rows.append(run_one_date(date_dir, args.fallback_top_n))

        batch = pd.DataFrame(batch_rows)
        batch.to_csv(V3_ROOT / "vsigma_odds_structure_depth_batch_report.csv", index=False)

        paths, _historical, _summaries, _dates = build_historical_execution_shortlist_backtest(
            historical_dir=V3_HISTORICAL_DIR,
            output_dir=V3_ROOT,
            preserve_per_date=True,
        )
        build_execution_mode_comparison(paths["historical"], V3_ROOT)

        comparison = build_comparison()
        comparison.to_csv(COMPARISON_OUTPUT, index=False)
        write_comparison_report(batch, comparison)

        print("\n=== ODDS STRUCTURE DEPTH HISTORICAL EVALUATION COMPLETADO ===")
        print(f"Output root: {V3_ROOT}")
        print(f"Comparison: {COMPARISON_OUTPUT}")
        print(comparison.to_string(index=False))
    finally:
        restore_live_files(backup_paths, backup_dir, existed)
        if backup_dir.exists():
            shutil.rmtree(backup_dir)


if __name__ == "__main__":
    main()
