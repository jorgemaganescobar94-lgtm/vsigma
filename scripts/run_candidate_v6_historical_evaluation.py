from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top
    from run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from run_today_shadow_candidate_v6 import (
        ALIGNED_STRENGTHEN,
        DISAGREEMENT_SECONDARY,
        DISAGREEMENT_WEAKEN,
        V6_MODE_NAME,
        apply_api_predictions_benchmark_layer,
        norm_upper,
    )
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top
    from scripts.run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from scripts.run_today_shadow_candidate_v6 import (
        ALIGNED_STRENGTHEN,
        DISAGREEMENT_SECONDARY,
        DISAGREEMENT_WEAKEN,
        V6_MODE_NAME,
        apply_api_predictions_benchmark_layer,
        norm_upper,
    )


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
RECENT_LAB_HISTORICAL_DIR = PROCESSED_DIR / "recent_lab_historical" / "historical"
OUTPUT_DIR = PROCESSED_DIR / "candidate_v6_historical"

SUMMARY_CSV = "vsigma_candidate_v6_historical_summary.csv"
DATE_LEDGER_CSV = "vsigma_candidate_v6_historical_by_date.csv"
BENCHMARK_ROWS_CSV = "vsigma_candidate_v6_historical_predictions_benchmark_rows.csv"
REPORT_TXT = "vsigma_candidate_v6_historical_report.txt"


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def date_dirs(root: Path, start_date: str, end_date: str) -> list[Path]:
    if not root.exists():
        return []
    return [path for path in sorted(root.iterdir()) if path.is_dir() and start_date <= path.name <= end_date]


def merge_deep_fields(shortlist: pd.DataFrame, deep: pd.DataFrame) -> pd.DataFrame:
    if shortlist.empty or deep.empty or "fixture_id" not in shortlist.columns or "fixture_id" not in deep.columns:
        return shortlist.copy()
    merge_cols = [
        c
        for c in [
            "fixture_id",
            "home_team_id",
            "away_team_id",
            "market_alt",
            "alt_model_prob",
            "alt_odds_used",
            "alt_implied_prob",
            "alt_edge",
            "pick_primary_risk",
            "pick_failure_mode",
        ]
        if c in deep.columns
    ]
    if len(merge_cols) <= 1:
        return shortlist.copy()
    out = shortlist.drop(columns=[c for c in merge_cols if c != "fixture_id" and c in shortlist.columns], errors="ignore")
    return out.merge(deep[merge_cols].drop_duplicates("fixture_id"), on="fixture_id", how="left")


def mode_top(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "accuracy_mode_eligible_flag" not in df.columns:
        return pd.DataFrame()
    return select_competition_top(df)


def evaluate_mode(top: pd.DataFrame, raw: pd.DataFrame, mode: str) -> pd.DataFrame:
    if top.empty:
        return pd.DataFrame()
    return evaluate_competition_picks(top, raw, mode)


def add_date_to_ledger(ledger: pd.DataFrame, match_date: str) -> pd.DataFrame:
    out = ledger.copy()
    if not out.empty:
        out.insert(0, "evaluation_date", match_date)
    return out


def concat_nonempty(frames: list[pd.DataFrame]) -> pd.DataFrame:
    nonempty = [df for df in frames if not df.empty]
    return pd.concat(nonempty, ignore_index=True) if nonempty else pd.DataFrame()


def brier_score(ledger: pd.DataFrame) -> Any:
    if ledger.empty:
        return pd.NA
    result = ledger.get("actionable_result", pd.Series("", index=ledger.index)).map(norm_upper)
    probs = pd.to_numeric(
        ledger.get("competition_calibrated_prob", ledger.get("primary_model_prob", pd.Series(index=ledger.index))),
        errors="coerce",
    )
    mask = result.isin({"WIN", "LOSS"}) & probs.notna()
    if not mask.any():
        return pd.NA
    y = result[mask].eq("WIN").astype(float)
    return round(float(((probs[mask] - y) ** 2).mean()), 6)


def market_mix(ledger: pd.DataFrame) -> str:
    if ledger.empty or "market_primary" not in ledger.columns:
        return ""
    return ";".join(f"{market}:{count}" for market, count in ledger["market_primary"].map(norm_upper).value_counts().sort_index().items())


def aggregate_ledger(ledger: pd.DataFrame, mode: str) -> dict[str, Any]:
    summary = summarize_ledger(ledger, mode)
    decided = int(summary["wins"]) + int(summary["losses"])
    return {
        "mode": mode,
        "segment": "OVERALL",
        "rows": int(summary["pick_count"]),
        "settled_rows": int(summary["settled_rows"]),
        "wins": int(summary["wins"]),
        "losses": int(summary["losses"]),
        "hit_rate": round(float(summary["wins"]) / decided * 100.0, 6) if decided else pd.NA,
        "profit_units": summary["profit_units"],
        "roi_percent": summary["roi_percent"],
        "brier_score": brier_score(ledger),
        "market_mix": market_mix(ledger),
    }


def segment_ledger(ledger: pd.DataFrame, mode: str, segment: str, mask: pd.Series) -> dict[str, Any]:
    subset = ledger[mask].copy() if not ledger.empty else pd.DataFrame()
    row = aggregate_ledger(subset, mode)
    row["segment"] = segment
    return row


def benchmark_counts(rows: pd.DataFrame) -> dict[str, int]:
    actions = rows.get("api_prediction_benchmark_action", pd.Series(dtype=object)).map(norm_upper)
    alignment = rows.get("api_prediction_alignment_flag", pd.Series(dtype=object)).map(norm_upper)
    available = pd.to_numeric(rows.get("api_prediction_available_flag", pd.Series(dtype=float)), errors="coerce").fillna(0)
    return {
        "api_prediction_available_rows": int(available.eq(1).sum()) if len(rows) else 0,
        "api_prediction_aligned_rows": int(alignment.eq("ALIGNED").sum()) if len(rows) else 0,
        "api_prediction_disagreement_rows": int(alignment.eq("DISAGREEMENT").sum()) if len(rows) else 0,
        "api_prediction_strengthened_rows": int(actions.eq(ALIGNED_STRENGTHEN).sum()) if len(rows) else 0,
        "api_prediction_weakened_rows": int(actions.eq(DISAGREEMENT_WEAKEN).sum()) if len(rows) else 0,
        "api_prediction_secondary_rows": int(actions.eq(DISAGREEMENT_SECONDARY).sum()) if len(rows) else 0,
    }


def evaluate_range(start_date: str, end_date: str, *, use_api: bool = False) -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline_ledgers: list[pd.DataFrame] = []
    v2_ledgers: list[pd.DataFrame] = []
    v6_ledgers: list[pd.DataFrame] = []
    benchmark_frames: list[pd.DataFrame] = []
    by_date_rows: list[dict[str, Any]] = []
    total_api_calls = 0
    total_cache_hits = 0
    total_api_errors = 0

    for base_dir in date_dirs(BASELINE_HISTORICAL_DIR, start_date, end_date):
        match_date = base_dir.name
        v2_dir = RECENT_LAB_HISTORICAL_DIR / match_date
        raw = read_csv_optional(base_dir / "matches.csv")
        baseline_source = read_csv_optional(base_dir / "vsigma_execution_shortlist_historical.csv")
        v2_source = read_csv_optional(v2_dir / "vsigma_execution_shortlist_historical.csv")
        v2_deep = read_csv_optional(v2_dir / "vsigma_deep_analysis_candidates.csv")
        if raw.empty or baseline_source.empty or v2_source.empty:
            by_date_rows.append({"date": match_date, "status": "MISSING_INPUT"})
            continue

        baseline_top = mode_top(baseline_source)
        v2_source = merge_deep_fields(v2_source, v2_deep)
        v2_top = mode_top(v2_source)
        all_v6, _v6_shortlist, v6_top, counters = apply_api_predictions_benchmark_layer(v2_source, use_api=use_api)
        total_api_calls += counters.get("api_calls_made", 0)
        total_cache_hits += counters.get("cache_hits", 0)
        total_api_errors += counters.get("api_errors", 0)

        if not all_v6.empty:
            bench = all_v6.copy()
            bench.insert(0, "evaluation_date", match_date)
            benchmark_frames.append(bench)

        baseline_ledger = add_date_to_ledger(evaluate_mode(baseline_top, raw, "BASELINE_OFFICIAL"), match_date)
        v2_ledger = add_date_to_ledger(evaluate_mode(v2_top, raw, "SHADOW_CANDIDATE_V2"), match_date)
        v6_ledger = add_date_to_ledger(evaluate_mode(v6_top, raw, V6_MODE_NAME), match_date)
        baseline_ledgers.append(baseline_ledger)
        v2_ledgers.append(v2_ledger)
        v6_ledgers.append(v6_ledger)

        base_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
        v2_summary = summarize_ledger(v2_ledger, "SHADOW_CANDIDATE_V2")
        v6_summary = summarize_ledger(v6_ledger, V6_MODE_NAME)
        by_date_rows.append(
            {
                "date": match_date,
                "status": "OK",
                "baseline_rows": base_summary["pick_count"],
                "baseline_wins": base_summary["wins"],
                "baseline_losses": base_summary["losses"],
                "baseline_profit": base_summary["profit_units"],
                "candidate_v2_rows": v2_summary["pick_count"],
                "candidate_v2_wins": v2_summary["wins"],
                "candidate_v2_losses": v2_summary["losses"],
                "candidate_v2_profit": v2_summary["profit_units"],
                "candidate_v6_rows": v6_summary["pick_count"],
                "candidate_v6_wins": v6_summary["wins"],
                "candidate_v6_losses": v6_summary["losses"],
                "candidate_v6_profit": v6_summary["profit_units"],
                **benchmark_counts(all_v6),
                "api_calls_made": counters.get("api_calls_made", 0),
                "cache_hits": counters.get("cache_hits", 0),
                "api_errors": counters.get("api_errors", 0),
            }
        )

    all_baseline = concat_nonempty(baseline_ledgers)
    all_v2 = concat_nonempty(v2_ledgers)
    all_v6 = concat_nonempty(v6_ledgers)
    all_benchmark = concat_nonempty(benchmark_frames)

    summary_rows = [
        aggregate_ledger(all_baseline, "BASELINE_OFFICIAL"),
        aggregate_ledger(all_v2, "SHADOW_CANDIDATE_V2"),
        {
            **aggregate_ledger(all_v6, V6_MODE_NAME),
            **benchmark_counts(all_benchmark),
            "api_calls_made": total_api_calls,
            "cache_hits": total_cache_hits,
            "api_errors": total_api_errors,
        },
    ]
    if not all_v6.empty and "api_prediction_alignment_flag" in all_v6.columns:
        alignment = all_v6["api_prediction_alignment_flag"].map(norm_upper)
        summary_rows.append(segment_ledger(all_v6, V6_MODE_NAME, "API_ALIGNED_SUBSET", alignment.eq("ALIGNED")))
        summary_rows.append(segment_ledger(all_v6, V6_MODE_NAME, "API_DISAGREEMENT_SUBSET", alignment.eq("DISAGREEMENT")))

    summary = pd.DataFrame(summary_rows)
    by_date = pd.DataFrame(by_date_rows)
    summary_path = OUTPUT_DIR / SUMMARY_CSV
    by_date_path = OUTPUT_DIR / DATE_LEDGER_CSV
    benchmark_path = OUTPUT_DIR / BENCHMARK_ROWS_CSV
    report_path = OUTPUT_DIR / REPORT_TXT
    summary.to_csv(summary_path, index=False)
    by_date.to_csv(by_date_path, index=False)
    all_benchmark.to_csv(benchmark_path, index=False)

    usable_dates = by_date[by_date.get("status", pd.Series(dtype=object)).eq("OK")]["date"].tolist() if not by_date.empty else []
    lines = [
        "vSIGMA candidate v6 historical evaluation",
        "",
        f"Requested historical range: {start_date} through {end_date}",
        f"Usable dates: {', '.join(usable_dates) if usable_dates else 'none'}",
        "Baseline: frozen historical outputs.",
        "Candidate v2: recent lab historical outputs.",
        "Candidate v6: candidate v2 + API Predictions Benchmark.",
        f"API fetch enabled: {int(use_api)}",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Summary",
        summary.to_string(index=False) if not summary.empty else "No summary rows.",
        "",
        "By date",
        by_date.to_string(index=False) if not by_date.empty else "No date rows.",
        "",
        "API Predictions Benchmark rows",
        all_benchmark[
            [
                c
                for c in [
                    "evaluation_date",
                    "fixture_id",
                    "home_team",
                    "away_team",
                    "market_primary",
                    "api_prediction_quality_flag",
                    "api_prediction_alignment_flag",
                    "api_prediction_benchmark_action",
                    "api_prediction_benchmark_reason",
                ]
                if c in all_benchmark.columns
            ]
        ].to_string(index=False)
        if not all_benchmark.empty
        else "No benchmark rows.",
        "",
        "Small-sample limitation: API predictions are an external benchmark only; missing coverage is neutral uncertainty.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "summary": summary_path,
        "by_date": by_date_path,
        "benchmark_rows": benchmark_path,
        "report": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate candidate v6 API Predictions benchmark on historical snapshots.")
    parser.add_argument("--start-date", default="2026-04-23")
    parser.add_argument("--end-date", default="2026-05-08")
    parser.add_argument("--use-api", action="store_true", help="Fetch missing predictions from the API.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = evaluate_range(args.start_date, args.end_date, use_api=args.use_api)
    print("\n=== CANDIDATE V6 HISTORICAL EVALUATION COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    summary = pd.read_csv(paths["summary"])
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
