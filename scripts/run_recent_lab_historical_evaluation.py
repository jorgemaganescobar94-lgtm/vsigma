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
    from run_historical_labeling_pipeline import (
        PER_DATE_GENERATED_FILES,
        create_relaxed_historical_shortlist,
    )
except ModuleNotFoundError:
    from scripts.build_execution_mode_comparison import build_execution_mode_comparison
    from scripts.build_historical_execution_shortlist_backtest import build_historical_execution_shortlist_backtest
    from scripts.run_historical_labeling_pipeline import (
        PER_DATE_GENERATED_FILES,
        create_relaxed_historical_shortlist,
    )


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
LAB_ROOT = PROCESSED_DIR / "recent_lab_historical"
LAB_HISTORICAL_DIR = LAB_ROOT / "historical"

LAB_OUTPUT_FILES = [
    PROCESSED_DIR / "vsigma_schedule_strength_summary.csv",
    PROCESSED_DIR / "vsigma_schedule_strength_report.txt",
    PROCESSED_DIR / "vsigma_recent_anomaly_summary.csv",
    PROCESSED_DIR / "vsigma_recent_anomaly_report.txt",
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

LAB_STEPS_BEFORE_DEEP = [
    "scripts/filter_leagues.py",
    "scripts/build_api_league_coverage_matrix.py",
    "scripts/enrich_recent_schedule_strength.py",
    "scripts/enrich_recent_fixture_anomaly_flags.py",
    "scripts/filter_leagues.py",
    "scripts/score_matches_v3.py",
    "scripts/tie_state_adjust_scores.py",
    "scripts/select_core_candidates.py",
]

LAB_STEPS_AFTER_DEEP = [
    "scripts/deep_analysis_candidates.py",
    "scripts/final_execution_exports.py",
    "scripts/validate_final_execution_exports.py",
    "scripts/label_market_results.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate recent schedule-strength and anomaly-cleaning lab layer on historical snapshots."
    )
    parser.add_argument("--start-date", default="2026-04-23")
    parser.add_argument("--end-date", default="2026-05-08")
    parser.add_argument("--fallback-top-n", type=int, default=15)
    return parser.parse_args()


def date_dirs(start: str, end: str) -> list[Path]:
    dirs = [
        path
        for path in sorted(BASELINE_HISTORICAL_DIR.iterdir())
        if path.is_dir() and start <= path.name <= end
    ]
    return dirs


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
    existed: dict[Path, bool] = {}
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
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

    for step in LAB_STEPS_BEFORE_DEEP:
        run_step(step)

    fallback_rows = 0
    if shortlist_empty():
        fallback_rows = create_relaxed_historical_shortlist(fallback_top_n)
    if shortlist_empty():
        return {"date": date_dir.name, "status": "NO_CANDIDATES", "rows": 0, "fallback_rows": fallback_rows}

    for step in LAB_STEPS_AFTER_DEEP:
        run_step(step)

    out_dir = LAB_HISTORICAL_DIR / date_dir.name
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


def read_table(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def overall_line(df: pd.DataFrame, mode: str = "FULL_SHORTLIST") -> dict[str, Any]:
    if df.empty or "mode" not in df.columns:
        return {}
    row = df[df["mode"].eq(mode)]
    if row.empty:
        return {}
    return row.iloc[0].to_dict()


def compare_outputs(output_dir: Path) -> pd.DataFrame:
    baseline = read_table(PROCESSED_DIR / "vsigma_execution_mode_comparison_overall.csv")
    lab = read_table(output_dir / "vsigma_execution_mode_comparison_overall.csv")
    rows = []
    for mode in ["CORE_ONLY", "CORE_PLUS_STANDARD", "FULL_SHORTLIST", "COMPETITION_ACCURACY_MODE"]:
        base = overall_line(baseline, mode)
        exp = overall_line(lab, mode)
        if not base and not exp:
            continue
        rows.append(
            {
                "mode": mode,
                "baseline_rows": base.get("rows_total", 0),
                "experimental_rows": exp.get("rows_total", 0),
                "baseline_wins": base.get("wins", 0),
                "experimental_wins": exp.get("wins", 0),
                "baseline_losses": base.get("losses", 0),
                "experimental_losses": exp.get("losses", 0),
                "baseline_hit_rate": base.get("hit_rate", pd.NA),
                "experimental_hit_rate": exp.get("hit_rate", pd.NA),
                "baseline_profit": base.get("profit_units_total", 0.0),
                "experimental_profit": exp.get("profit_units_total", 0.0),
                "baseline_roi": base.get("roi_percent", pd.NA),
                "experimental_roi": exp.get("roi_percent", pd.NA),
            }
        )
    return pd.DataFrame(rows)


def write_report(output_dir: Path, batch: pd.DataFrame, comparison: pd.DataFrame) -> None:
    by_market = read_table(output_dir / "vsigma_execution_shortlist_backtest_by_market.csv")
    by_source = read_table(output_dir / "vsigma_execution_shortlist_backtest_by_source.csv")
    probability = read_table(output_dir / "vsigma_probability_evaluation_summary.csv")
    lines = [
        "vSIGMA recent lab historical evaluation",
        "",
        "Lab layers: recent schedule strength + recent fixture anomaly cleaning.",
        "Baseline: frozen historical execution-mode outputs in data/processed.",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Batch status",
        batch.to_string(index=False) if not batch.empty else "No batch rows.",
        "",
        "Baseline vs experimental",
        comparison.to_string(index=False) if not comparison.empty else "No comparison rows.",
        "",
        "Experimental market-family breakdown",
        by_market.to_string(index=False) if not by_market.empty else "No market rows.",
        "",
        "Experimental CORE / EXTENDED / STANDARD breakdown",
        by_source.to_string(index=False) if not by_source.empty else "No source rows.",
        "",
        "Experimental probability/Brier summary",
        probability.to_string(index=False) if not probability.empty else "No probability summary.",
        "",
    ]
    (output_dir / "vsigma_recent_lab_historical_evaluation_report.txt").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    dirs = date_dirs(args.start_date, args.end_date)
    if not dirs:
        raise RuntimeError("No historical date directories found for requested range.")

    LAB_ROOT.mkdir(parents=True, exist_ok=True)
    if LAB_HISTORICAL_DIR.exists():
        shutil.rmtree(LAB_HISTORICAL_DIR)
    LAB_HISTORICAL_DIR.mkdir(parents=True, exist_ok=True)

    backup_paths = sorted(set([RAW_MATCHES, *PER_DATE_GENERATED_FILES, *LAB_OUTPUT_FILES]))
    backup_dir = LAB_ROOT / "_live_backup"
    existed = backup_live_files(backup_paths, backup_dir)

    batch_rows = []
    try:
        for date_dir in dirs:
            print(f"\n=== RECENT LAB HISTORICAL DATE {date_dir.name} ===")
            batch_rows.append(run_one_date(date_dir, args.fallback_top_n))

        batch = pd.DataFrame(batch_rows)
        batch.to_csv(LAB_ROOT / "vsigma_recent_lab_historical_batch_report.csv", index=False)

        paths, _historical, _summaries, _dates = build_historical_execution_shortlist_backtest(
            historical_dir=LAB_HISTORICAL_DIR,
            output_dir=LAB_ROOT,
            preserve_per_date=True,
        )
        build_execution_mode_comparison(
            source_csv=paths["historical"],
            output_dir=LAB_ROOT,
        )
        comparison = compare_outputs(LAB_ROOT)
        comparison.to_csv(LAB_ROOT / "vsigma_recent_lab_historical_comparison.csv", index=False)
        write_report(LAB_ROOT, batch, comparison)

        print("\n=== RECENT LAB HISTORICAL EVALUATION COMPLETADO ===")
        print(f"Lab root: {LAB_ROOT}")
        print(comparison.to_string(index=False))
    finally:
        restore_live_files(backup_paths, backup_dir, existed)


if __name__ == "__main__":
    main()
