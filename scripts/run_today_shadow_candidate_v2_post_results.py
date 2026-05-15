from __future__ import annotations

import argparse
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_daily_decision_journal import build_shadow_candidate_v2_post_summary
    from label_market_results import (
        GOAL_COL_PAIRS,
        STATUS_COL_CANDIDATES,
        evaluate_market,
        first_existing_column,
        resolve_goals,
        settle_profit,
        status_is_finished,
    )
except ModuleNotFoundError:
    from scripts.build_daily_decision_journal import build_shadow_candidate_v2_post_summary
    from scripts.label_market_results import (
        GOAL_COL_PAIRS,
        STATUS_COL_CANDIDATES,
        evaluate_market,
        first_existing_column,
        resolve_goals,
        settle_profit,
        status_is_finished,
    )


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"
CANDIDATE_LEDGER_CSV = "vsigma_today_candidate_v2_results_ledger.csv"
CANDIDATE_SUMMARY_CSV = "vsigma_today_candidate_v2_results_summary.csv"
RESULT_COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_results.csv"
RESULT_COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_results_report.txt"
SHADOW_POST_REPORT = "today_shadow_candidate_v2_post_report.csv"

GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def read_csv_required(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")
    return pd.read_csv(path)


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def raw_merge_columns(raw: pd.DataFrame) -> list[str]:
    cols = ["fixture_id"]
    for pair in GOAL_COL_PAIRS:
        for col in pair:
            if col in raw.columns and col not in cols:
                cols.append(col)
    status_col = first_existing_column(raw, STATUS_COL_CANDIDATES)
    if status_col and status_col not in cols:
        cols.append(status_col)
    for col in ["date", "home_team", "away_team", "league"]:
        if col in raw.columns and col not in cols:
            cols.append(col)
    return cols


def pick_rank(row: pd.Series) -> object:
    for col in ["accuracy_mode_rank", "execution_rank", "shortlist_rank"]:
        if col in row.index and pd.notna(row.get(col)):
            return row.get(col)
    return pd.NA


def compare_key(df: pd.DataFrame) -> pd.Series:
    fixture = df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()
    market = df.get("market_primary", pd.Series("", index=df.index)).astype(str).str.strip().str.upper()
    return fixture + "::" + market


def evaluate_competition_picks(picks: pd.DataFrame, raw_results: pd.DataFrame, mode: str) -> pd.DataFrame:
    if picks.empty:
        return pd.DataFrame()
    if "fixture_id" not in picks.columns or "market_primary" not in picks.columns:
        raise ValueError(f"{mode} competition picks require fixture_id and market_primary.")
    if "fixture_id" not in raw_results.columns:
        raise ValueError("Raw results require fixture_id.")

    status_col = first_existing_column(raw_results, STATUS_COL_CANDIDATES)
    merge_cols = raw_merge_columns(raw_results)
    raw_unique = raw_results[merge_cols].drop_duplicates("fixture_id")
    merged = picks.merge(raw_unique, on="fixture_id", how="left", suffixes=("", "_result"), indicator=True)

    rows: list[dict[str, object]] = []
    for _, row in merged.iterrows():
        matched = row.get("_merge") == "both"
        if not matched:
            ledger_status = "UNMATCHED"
            result = "UNMATCHED"
            profit = pd.NA
            hg = ag = pd.NA
        else:
            hg, ag = resolve_goals(row)
            finished = status_is_finished(row, status_col)
            if finished and (pd.isna(hg) or pd.isna(ag)):
                finished = False
            if not finished:
                ledger_status = "PENDING"
                result = "PENDING"
                profit = pd.NA
            else:
                ledger_status = "RESULT_AVAILABLE"
                result = evaluate_market(norm_upper(row.get("market_primary")), hg, ag)
                profit = settle_profit(result, row.get("primary_odds_used"))

        out = row.drop(labels=["_merge"], errors="ignore").to_dict()
        out["comparison_mode"] = mode
        out["competition_pick_rank"] = pick_rank(row)
        out["resolved_home_goals"] = hg
        out["resolved_away_goals"] = ag
        out["ledger_result_status"] = ledger_status
        out["actionable_result"] = result
        out["actionable_profit_units"] = profit
        out["primary_result"] = result
        out["primary_profit_units"] = profit
        rows.append(out)

    ledger = pd.DataFrame(rows)
    if "competition_pick_rank" in ledger.columns:
        ledger["_rank_sort"] = pd.to_numeric(ledger["competition_pick_rank"], errors="coerce")
        ledger = ledger.sort_values("_rank_sort", ascending=True, na_position="last").drop(
            columns=["_rank_sort"]
        )
    return ledger.reset_index(drop=True)


def summarize_ledger(ledger: pd.DataFrame, mode: str) -> dict[str, object]:
    if ledger.empty:
        return {
            "mode": mode,
            "pick_count": 0,
            "settled_rows": 0,
            "pending_rows": 0,
            "unmatched_rows": 0,
            "wins": 0,
            "losses": 0,
            "pushes": 0,
            "voids": 0,
            "profit_units": 0.0,
            "roi_percent": pd.NA,
        }

    status = ledger["ledger_result_status"].map(norm_upper)
    result = ledger["actionable_result"].map(norm_upper)
    settled = status.eq("RESULT_AVAILABLE") & result.isin(GRADED_RESULTS)
    profit = pd.to_numeric(ledger.get("actionable_profit_units", pd.Series(index=ledger.index)), errors="coerce")
    settled_count = int(settled.sum())
    profit_total = float(profit.where(settled).sum(skipna=True)) if settled_count else 0.0
    return {
        "mode": mode,
        "pick_count": int(len(ledger)),
        "settled_rows": settled_count,
        "pending_rows": int(status.eq("PENDING").sum()),
        "unmatched_rows": int(status.eq("UNMATCHED").sum()),
        "wins": int(result.eq("WIN").sum()),
        "losses": int(result.eq("LOSS").sum()),
        "pushes": int(result.eq("PUSH").sum()),
        "voids": int(result.eq("VOID").sum()),
        "profit_units": round(profit_total, 6),
        "roi_percent": round(profit_total / settled_count * 100.0, 6) if settled_count else pd.NA,
    }


def first_available(row: pd.Series, columns: list[str]) -> object:
    for col in columns:
        if col in row.index and pd.notna(row.get(col)) and norm_text(row.get(col)):
            return row.get(col)
    return pd.NA


def build_result_comparison(baseline_ledger: pd.DataFrame, candidate_ledger: pd.DataFrame) -> pd.DataFrame:
    baseline = baseline_ledger.copy()
    candidate = candidate_ledger.copy()
    baseline["_compare_key"] = compare_key(baseline) if not baseline.empty else pd.Series(dtype=str)
    candidate["_compare_key"] = compare_key(candidate) if not candidate.empty else pd.Series(dtype=str)
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
        source = b if exists_b else c
        status = "BOTH" if exists_b and exists_c else ("BASELINE_ONLY" if exists_b else "CANDIDATE_V2_ONLY")
        rows.append(
            {
                "comparison_status": status,
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["competition_pick_rank"]) if exists_b else pd.NA,
                "candidate_v2_rank": first_available(c, ["competition_pick_rank"]) if exists_c else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if exists_b else pd.NA,
                "candidate_v2_market": first_available(c, ["market_primary"]) if exists_c else pd.NA,
                "baseline_result_status": first_available(b, ["ledger_result_status"]) if exists_b else pd.NA,
                "candidate_v2_result_status": first_available(c, ["ledger_result_status"]) if exists_c else pd.NA,
                "baseline_result": first_available(b, ["actionable_result"]) if exists_b else pd.NA,
                "candidate_v2_result": first_available(c, ["actionable_result"]) if exists_c else pd.NA,
                "baseline_profit_units": first_available(b, ["actionable_profit_units"]) if exists_b else pd.NA,
                "candidate_v2_profit_units": first_available(c, ["actionable_profit_units"]) if exists_c else pd.NA,
            }
        )
    return pd.DataFrame(rows)


def write_result_report(path: Path, baseline_summary: dict[str, object], candidate_summary: dict[str, object], comparison: pd.DataFrame) -> None:
    overlap = int(comparison["comparison_status"].eq("BOTH").sum()) if not comparison.empty else 0
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 RESULTS",
        "",
        f"Baseline pick count: {baseline_summary['pick_count']}",
        f"Candidate pick count: {candidate_summary['pick_count']}",
        f"Overlap picks: {overlap}",
        "",
        "Mode summary",
        pd.DataFrame([baseline_summary, candidate_summary]).to_string(index=False),
        "",
        "Pick result comparison",
        comparison.to_string(index=False) if not comparison.empty else "No compared picks.",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_shadow_post_outputs(
    processed_dir: Path,
    today_dir: Path,
    match_date: str,
    timezone_name: str,
    raw_results: pd.DataFrame,
    baseline_top: pd.DataFrame,
    candidate_top: pd.DataFrame,
) -> dict[str, Path]:
    snapshot_dir = today_dir / match_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    baseline_ledger = evaluate_competition_picks(baseline_top, raw_results, "BASELINE_OFFICIAL")
    candidate_ledger = evaluate_competition_picks(candidate_top, raw_results, "SHADOW_CANDIDATE_V2")
    baseline_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
    candidate_summary = summarize_ledger(candidate_ledger, "SHADOW_CANDIDATE_V2")
    comparison = build_result_comparison(baseline_ledger, candidate_ledger)

    candidate_ledger_path = processed_dir / CANDIDATE_LEDGER_CSV
    candidate_summary_path = processed_dir / CANDIDATE_SUMMARY_CSV
    comparison_path = processed_dir / RESULT_COMPARISON_CSV
    comparison_report_path = processed_dir / RESULT_COMPARISON_REPORT
    shadow_post_report_path = processed_dir / SHADOW_POST_REPORT

    candidate_ledger.to_csv(candidate_ledger_path, index=False)
    pd.DataFrame([candidate_summary]).to_csv(candidate_summary_path, index=False)
    comparison.to_csv(comparison_path, index=False)
    write_result_report(comparison_report_path, baseline_summary, candidate_summary, comparison)

    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "baseline_pick_count": baseline_summary["pick_count"],
                "candidate_v2_pick_count": candidate_summary["pick_count"],
                "overlap_picks": int(comparison["comparison_status"].eq("BOTH").sum()) if not comparison.empty else 0,
                "baseline_wins": baseline_summary["wins"],
                "baseline_losses": baseline_summary["losses"],
                "baseline_profit_units": baseline_summary["profit_units"],
                "baseline_roi_percent": baseline_summary["roi_percent"],
                "candidate_v2_wins": candidate_summary["wins"],
                "candidate_v2_losses": candidate_summary["losses"],
                "candidate_v2_profit_units": candidate_summary["profit_units"],
                "candidate_v2_roi_percent": candidate_summary["roi_percent"],
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(shadow_post_report_path, index=False)

    for path in [
        candidate_ledger_path,
        candidate_summary_path,
        comparison_path,
        comparison_report_path,
        shadow_post_report_path,
    ]:
        copy_if_exists(path, snapshot_dir)

    journal_path = build_shadow_candidate_v2_post_summary(processed_dir, today_dir, match_date, timezone_name)

    return {
        "candidate_results_ledger": candidate_ledger_path,
        "candidate_results_summary": candidate_summary_path,
        "result_comparison_csv": comparison_path,
        "result_comparison_report": comparison_report_path,
        "shadow_post_report": shadow_post_report_path,
        "shadow_post_journal": journal_path,
    }


def run_shadow_candidate_v2_post_results(match_date: str, timezone_name: str) -> dict[str, Path]:
    raw = read_csv_required(RAW_MATCHES_CSV, "raw match results")
    baseline_top = read_csv_required(PROCESSED_DIR / BASELINE_TOP_CSV, "official baseline competition top")
    candidate_top = read_csv_required(PROCESSED_DIR / CANDIDATE_TOP_CSV, "candidate v2 competition top")

    print("\n=== TODAY SHADOW CANDIDATE V2 POST-RESULTS ===")
    print(f"Date: {match_date}")
    print(f"Timezone: {timezone_name}")
    print(f"Baseline competition top rows: {len(baseline_top)}")
    print(f"Candidate v2 competition top rows: {len(candidate_top)}")

    return write_shadow_post_outputs(
        PROCESSED_DIR,
        TODAY_DIR,
        match_date,
        timezone_name,
        raw,
        baseline_top,
        candidate_top,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate candidate v2 shadow picks after today's official post-results refresh."
    )
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = run_shadow_candidate_v2_post_results(match_date, args.timezone)

    print("\n=== TODAY SHADOW CANDIDATE V2 POST-RESULTS COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
