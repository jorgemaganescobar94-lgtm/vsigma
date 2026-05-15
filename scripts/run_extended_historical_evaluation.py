from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top
    from run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from run_today_shadow_candidate_v4 import V4_MODE_NAME, apply_over25_low_conversion_firewall
    from run_today_shadow_candidate_v5 import V5_MODE_NAME, apply_player_impact_layer
    from run_today_shadow_candidate_v6 import V6_MODE_NAME, apply_api_predictions_benchmark_layer
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top
    from scripts.run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from scripts.run_today_shadow_candidate_v4 import V4_MODE_NAME, apply_over25_low_conversion_firewall
    from scripts.run_today_shadow_candidate_v5 import V5_MODE_NAME, apply_player_impact_layer
    from scripts.run_today_shadow_candidate_v6 import V6_MODE_NAME, apply_api_predictions_benchmark_layer


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
RECENT_LAB_HISTORICAL_DIR = PROCESSED_DIR / "recent_lab_historical" / "historical"
OUTPUT_DIR = PROCESSED_DIR / "extended_historical"

SUMMARY_CSV = "vsigma_extended_backtest_summary.csv"
REPORT_TXT = "vsigma_extended_backtest_report.txt"
MARKET_BREAKDOWN_CSV = "vsigma_extended_market_breakdown.csv"
FAILURE_BREAKDOWN_CSV = "vsigma_extended_failure_mode_breakdown.csv"
LEAGUE_BREAKDOWN_CSV = "vsigma_extended_league_breakdown.csv"
ALL_LEDGERS_CSV = "vsigma_extended_all_ledgers.csv"

MODE_LABELS = {
    "baseline": "BASELINE_OFFICIAL",
    "candidate_v2": "SHADOW_CANDIDATE_V2",
    "candidate_v4": V4_MODE_NAME,
    "candidate_v5": V5_MODE_NAME,
    "candidate_v6": V6_MODE_NAME,
}


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def norm_upper(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


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
            "projected_home_goals",
            "projected_away_goals",
            "projected_total_goals",
            "likely_scoreline",
            "pick_primary_risk",
            "pick_failure_mode",
            "odds_total_ladder_shape",
            "odds_line_aggression_flag",
            "odds_over25_support_flag",
            "odds_over15_support_flag",
            "player_impact_quality_flag",
            "player_impact_market_translation_hint",
            "api_prediction_alignment_flag",
        ]
        if c in deep.columns
    ]
    out = shortlist.drop(columns=[c for c in merge_cols if c != "fixture_id" and c in shortlist.columns], errors="ignore")
    return out.merge(deep[merge_cols].drop_duplicates("fixture_id"), on="fixture_id", how="left") if len(merge_cols) > 1 else out


def mode_top(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "accuracy_mode_eligible_flag" not in df.columns:
        return pd.DataFrame()
    return select_competition_top(df)


def with_eval_date(ledger: pd.DataFrame, evaluation_date: str) -> pd.DataFrame:
    out = ledger.copy()
    if not out.empty:
        out.insert(0, "evaluation_date", evaluation_date)
    return out


def concat_nonempty(frames: list[pd.DataFrame]) -> pd.DataFrame:
    nonempty = [df for df in frames if not df.empty]
    return pd.concat(nonempty, ignore_index=True) if nonempty else pd.DataFrame()


def brier_score(ledger: pd.DataFrame) -> Any:
    if ledger.empty:
        return pd.NA
    result = ledger.get("actionable_result", pd.Series("", index=ledger.index)).map(norm_upper)
    probs = pd.to_numeric(ledger.get("competition_calibrated_prob", ledger.get("primary_model_prob", pd.Series(index=ledger.index))), errors="coerce")
    mask = result.isin({"WIN", "LOSS"}) & probs.notna()
    if not mask.any():
        return pd.NA
    y = result[mask].eq("WIN").astype(float)
    return round(float(((probs[mask] - y) ** 2).mean()), 6)


def max_drawdown(ledger: pd.DataFrame) -> float:
    if ledger.empty or "actionable_profit_units" not in ledger.columns:
        return 0.0
    status = ledger.get("ledger_result_status", pd.Series("", index=ledger.index)).map(norm_upper)
    profit = pd.to_numeric(ledger["actionable_profit_units"], errors="coerce").where(status.eq("RESULT_AVAILABLE")).dropna()
    if profit.empty:
        return 0.0
    cumulative = profit.cumsum()
    drawdown = cumulative - cumulative.cummax()
    return round(float(drawdown.min()), 6)


def aggregate_ledger(ledger: pd.DataFrame, mode: str, segment: str = "OVERALL") -> dict[str, Any]:
    summary = summarize_ledger(ledger, mode)
    decided = int(summary["wins"]) + int(summary["losses"])
    return {
        "mode": mode,
        "segment": segment,
        "rows": int(summary["pick_count"]),
        "settled_rows": int(summary["settled_rows"]),
        "wins": int(summary["wins"]),
        "losses": int(summary["losses"]),
        "pushes": int(summary["pushes"]),
        "hit_rate": round(float(summary["wins"]) / decided * 100.0, 6) if decided else pd.NA,
        "profit_units": summary["profit_units"],
        "roi_percent": summary["roi_percent"],
        "brier_score": brier_score(ledger),
        "max_drawdown": max_drawdown(ledger),
    }


def breakdown(ledger: pd.DataFrame, column: str, output_column: str) -> pd.DataFrame:
    if ledger.empty or column not in ledger.columns:
        return pd.DataFrame(columns=["mode", output_column, "rows", "settled_rows", "wins", "losses", "profit_units", "roi_percent"])
    rows: list[dict[str, Any]] = []
    for (mode, value), subset in ledger.groupby(["comparison_mode", column], dropna=False):
        row = aggregate_ledger(subset, str(mode), str(value))
        row[output_column] = value
        rows.append(row)
    cols = ["mode", output_column, "rows", "settled_rows", "wins", "losses", "profit_units", "roi_percent", "hit_rate"]
    return pd.DataFrame(rows)[cols] if rows else pd.DataFrame(columns=cols)


def build_mode_ledgers(raw: pd.DataFrame, baseline_source: pd.DataFrame, v2_source: pd.DataFrame, modes: set[str]) -> list[pd.DataFrame]:
    ledgers: list[pd.DataFrame] = []
    baseline_top = mode_top(baseline_source)
    v2_top = mode_top(v2_source)
    if "baseline" in modes:
        ledgers.append(evaluate_competition_picks(baseline_top, raw, MODE_LABELS["baseline"]))
    if "candidate_v2" in modes:
        ledgers.append(evaluate_competition_picks(v2_top, raw, MODE_LABELS["candidate_v2"]))
    if "candidate_v4" in modes:
        all_v4, _shortlist, v4_top = apply_over25_low_conversion_firewall(v2_source)
        ledgers.append(evaluate_competition_picks(v4_top, raw, MODE_LABELS["candidate_v4"]))
    if "candidate_v5" in modes:
        _all_v5, _shortlist, v5_top = apply_player_impact_layer(v2_source)
        ledgers.append(evaluate_competition_picks(v5_top, raw, MODE_LABELS["candidate_v5"]))
    if "candidate_v6" in modes:
        _all_v6, _shortlist, v6_top, _counters = apply_api_predictions_benchmark_layer(v2_source, use_api=False)
        ledgers.append(evaluate_competition_picks(v6_top, raw, MODE_LABELS["candidate_v6"]))
    return ledgers


def evaluate_range(
    start_date: str,
    end_date: str,
    timezone_name: str = "Atlantic/Canary",
    modes: set[str] | None = None,
    output_dir: Path = OUTPUT_DIR,
) -> dict[str, Path]:
    modes = modes or set(MODE_LABELS)
    output_dir.mkdir(parents=True, exist_ok=True)
    all_ledgers: list[pd.DataFrame] = []
    by_date_rows: list[dict[str, Any]] = []

    for base_dir in date_dirs(BASELINE_HISTORICAL_DIR, start_date, end_date):
        evaluation_date = base_dir.name
        v2_dir = RECENT_LAB_HISTORICAL_DIR / evaluation_date
        raw = read_csv_optional(base_dir / "matches.csv")
        baseline_source = read_csv_optional(base_dir / "vsigma_execution_shortlist_historical.csv")
        v2_source = read_csv_optional(v2_dir / "vsigma_execution_shortlist_historical.csv")
        v2_deep = read_csv_optional(v2_dir / "vsigma_deep_analysis_candidates.csv")
        v2_source = merge_deep_fields(v2_source, v2_deep)
        if raw.empty or baseline_source.empty or v2_source.empty:
            by_date_rows.append({"evaluation_date": evaluation_date, "status": "MISSING_INPUT"})
            continue
        ledgers = [with_eval_date(ledger, evaluation_date) for ledger in build_mode_ledgers(raw, baseline_source, v2_source, modes)]
        all_ledgers.extend(ledgers)
        for ledger in ledgers:
            if ledger.empty:
                continue
            mode = str(ledger["comparison_mode"].iloc[0])
            row = aggregate_ledger(ledger, mode, evaluation_date)
            row["evaluation_date"] = evaluation_date
            row["status"] = "OK"
            by_date_rows.append(row)

    ledger = concat_nonempty(all_ledgers)
    summary = pd.DataFrame([aggregate_ledger(group, str(mode)) for mode, group in ledger.groupby("comparison_mode")]) if not ledger.empty else pd.DataFrame()
    market = breakdown(ledger, "market_primary", "market_primary")
    league = breakdown(ledger, "league", "league")
    failure_col = "accuracy_primary_risk" if "accuracy_primary_risk" in ledger.columns else "pick_failure_mode"
    failure = breakdown(ledger, failure_col, "failure_mode")
    if not failure.empty:
        failure["failure_mode"] = failure["failure_mode"].astype(str)
    all_ledgers_path = output_dir / ALL_LEDGERS_CSV
    summary_path = output_dir / SUMMARY_CSV
    market_path = output_dir / MARKET_BREAKDOWN_CSV
    failure_path = output_dir / FAILURE_BREAKDOWN_CSV
    league_path = output_dir / LEAGUE_BREAKDOWN_CSV
    report_path = output_dir / REPORT_TXT
    by_date_path = output_dir / "vsigma_extended_by_date.csv"

    ledger.to_csv(all_ledgers_path, index=False)
    summary.to_csv(summary_path, index=False)
    market.to_csv(market_path, index=False)
    failure.to_csv(failure_path, index=False)
    league.to_csv(league_path, index=False)
    pd.DataFrame(by_date_rows).to_csv(by_date_path, index=False)

    lines = [
        "# vSIGMA Extended Historical Evaluation",
        "",
        f"- Range: {start_date} to {end_date}",
        f"- Timezone: {timezone_name}",
        f"- Modes: {', '.join(sorted(modes))}",
        f"- Ledger rows: {len(ledger)}",
        "",
        "## Summary",
        summary.to_string(index=False) if not summary.empty else "No evaluable rows.",
        "",
        "This evaluation does not alter official baseline selection logic or promote candidates.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "summary": summary_path,
        "report": report_path,
        "market_breakdown": market_path,
        "failure_mode_breakdown": failure_path,
        "league_breakdown": league_path,
        "all_ledgers": all_ledgers_path,
        "by_date": by_date_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run extended vSIGMA historical evaluation across official and shadow modes.")
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--modes", default="baseline,candidate_v2,candidate_v4,candidate_v5,candidate_v6")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    modes = {mode.strip() for mode in args.modes.split(",") if mode.strip()}
    invalid = sorted(modes - set(MODE_LABELS))
    if invalid:
        raise ValueError(f"Unknown modes: {invalid}")
    paths = evaluate_range(args.start_date, args.end_date, args.timezone, modes)
    print("\n=== EXTENDED HISTORICAL EVALUATION COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
