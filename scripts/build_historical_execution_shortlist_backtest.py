from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_today_execution_shortlist import (
        add_execution_score,
        apply_caps_by_phase,
        norm_text,
        premium_core_mask,
        premium_extended_mask,
        sort_execution_candidates,
        standard_fill_mask,
    )
    from build_competition_accuracy_mode import (
        add_accuracy_mode_fields,
        add_competition_probability_calibration,
        build_probability_calibration_table,
        build_probability_evaluation,
    )
except ModuleNotFoundError:
    from scripts.build_today_execution_shortlist import (
        add_execution_score,
        apply_caps_by_phase,
        norm_text,
        premium_core_mask,
        premium_extended_mask,
        sort_execution_candidates,
        standard_fill_mask,
    )
    from scripts.build_competition_accuracy_mode import (
        add_accuracy_mode_fields,
        add_competition_probability_calibration,
        build_probability_calibration_table,
        build_probability_evaluation,
    )


DEFAULT_HISTORICAL_DIR = Path("data/processed/historical")
DEFAULT_OUTPUT_DIR = Path("data/processed")

PREMIUM_CSV = "vsigma_final_approved_premium_candidates.csv"
STANDARD_CSV = "vsigma_final_approved_standard_candidates.csv"
LABELED_CSV = "vsigma_market_results_labeled.csv"

HISTORICAL_OUTPUT = "vsigma_execution_shortlist_historical.csv"
OVERALL_OUTPUT = "vsigma_execution_shortlist_backtest_overall.csv"
BY_DATE_OUTPUT = "vsigma_execution_shortlist_backtest_by_date.csv"
BY_SOURCE_OUTPUT = "vsigma_execution_shortlist_backtest_by_source.csv"
BY_BUCKET_OUTPUT = "vsigma_execution_shortlist_backtest_by_bucket.csv"
BY_MARKET_OUTPUT = "vsigma_execution_shortlist_backtest_by_market.csv"
BY_LEAGUE_OUTPUT = "vsigma_execution_shortlist_backtest_by_league.csv"
REPORT_OUTPUT = "vsigma_execution_shortlist_backtest_report.txt"
COMPETITION_HISTORICAL_OUTPUT = "vsigma_competition_accuracy_historical.csv"
COMPETITION_OVERALL_OUTPUT = "vsigma_competition_accuracy_backtest_overall.csv"
COMPETITION_BY_DATE_OUTPUT = "vsigma_competition_accuracy_backtest_by_date.csv"
COMPETITION_BY_SOURCE_OUTPUT = "vsigma_competition_accuracy_backtest_by_source.csv"
COMPETITION_BY_BUCKET_OUTPUT = "vsigma_competition_accuracy_backtest_by_bucket.csv"
COMPETITION_BY_MARKET_OUTPUT = "vsigma_competition_accuracy_backtest_by_market.csv"
COMPETITION_BY_LEAGUE_OUTPUT = "vsigma_competition_accuracy_backtest_by_league.csv"
COMPETITION_REPORT_OUTPUT = "vsigma_competition_accuracy_backtest_report.txt"

GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}
SUMMARY_COLUMNS = [
    "segment",
    "rows_total",
    "graded_rows",
    "wins",
    "losses",
    "pushes",
    "voids",
    "profit_units_total",
    "roi_percent",
]
HISTORICAL_COLUMNS = [
    "historical_batch_date",
    "execution_rank",
    "execution_shortlist_source",
    "final_execution_bucket",
    "final_recommendation",
    "execution_score",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "selection_score",
    "primary_model_prob",
    "primary_odds_used",
    "primary_edge",
    "accuracy_mode_eligible_flag",
    "accuracy_confidence_score",
    "accuracy_mode_reason",
    "accuracy_primary_risk",
    "accuracy_mode_bucket",
    "accuracy_mode_rank",
    "competition_raw_prob",
    "competition_calibrated_prob",
    "competition_prob_calibration_bucket",
    "competition_prob_calibration_reason",
    "competition_prob_shrinkage_applied_flag",
    "result_status",
    "actionable_result",
    "primary_result",
    "profit_units",
    "stake_units",
]


def read_csv_required(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required historical input: {path}")
    return pd.read_csv(path)


def discover_complete_dates(historical_dir: Path) -> list[Path]:
    if not historical_dir.exists():
        return []
    complete = []
    for date_dir in sorted(path for path in historical_dir.iterdir() if path.is_dir()):
        if all((date_dir / name).exists() for name in [PREMIUM_CSV, STANDARD_CSV, LABELED_CSV]):
            complete.append(date_dir)
    return complete


def normalize_candidate_inputs(df: pd.DataFrame, expected_bucket: str) -> pd.DataFrame:
    out = df.copy()
    required = [
        "shortlist_rank",
        "fixture_id",
        "league",
        "market_primary",
        "selection_score",
        "primary_model_prob",
        "primary_odds_used",
        "primary_edge",
        "base_execution_verdict",
        "final_recommendation",
        "final_execution_bucket",
    ]
    missing = [col for col in required if col not in out.columns]
    if missing:
        raise ValueError(f"{expected_bucket} historical candidates missing columns: {missing}")

    for col in [
        "shortlist_rank",
        "selection_score",
        "primary_model_prob",
        "primary_odds_used",
        "primary_edge",
    ]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out["_final_execution_bucket_norm"] = out["final_execution_bucket"].map(norm_text)
    out["_final_recommendation_norm"] = out["final_recommendation"].map(norm_text)
    out["_base_execution_verdict_norm"] = out["base_execution_verdict"].map(norm_text)
    out["_input_bucket"] = expected_bucket
    out["_source_row_id"] = [f"{expected_bucket}:{idx}" for idx in range(len(out))]
    return out


def strip_internal_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(
        columns=[
            "_final_execution_bucket_norm",
            "_final_recommendation_norm",
            "_base_execution_verdict_norm",
            "_input_bucket",
            "_source_row_id",
        ],
        errors="ignore",
    )


def reconstruct_execution_shortlist(
    premium_candidates: pd.DataFrame,
    standard_candidates: pd.DataFrame,
) -> pd.DataFrame:
    premium = add_execution_score(normalize_candidate_inputs(premium_candidates, "APPROVED_PREMIUM"))
    standard = add_execution_score(normalize_candidate_inputs(standard_candidates, "APPROVED_STANDARD"))

    premium_core = sort_execution_candidates(premium[premium_core_mask(premium)].copy())
    premium_core["execution_shortlist_source"] = "PREMIUM_CORE"

    premium_extended = premium[premium_extended_mask(premium)].copy()
    premium_extended_remaining = premium_extended.loc[
        ~premium_extended["_source_row_id"].isin(premium_core["_source_row_id"])
    ].copy()
    standard_fill = standard[standard_fill_mask(standard)].copy()

    shortlist = apply_caps_by_phase(
        [
            ("PREMIUM_CORE", premium_core),
            ("PREMIUM_EXTENDED", premium_extended_remaining),
            ("STANDARD_FILL", standard_fill),
        ]
    )
    if shortlist.empty:
        return pd.DataFrame(columns=HISTORICAL_COLUMNS)
    return add_accuracy_mode_fields(strip_internal_columns(shortlist))


def validate_labeled_for_join(labeled: pd.DataFrame, date_label: str) -> None:
    missing = [col for col in ["fixture_id", "market_primary"] if col not in labeled.columns]
    if missing:
        raise ValueError(f"Labeled results for {date_label} missing columns: {missing}")

    duplicated = labeled[labeled[["fixture_id", "market_primary"]].duplicated(keep=False)]
    if not duplicated.empty:
        sample = duplicated[["fixture_id", "market_primary"]].head(10).to_dict("records")
        raise ValueError(f"Labeled results for {date_label} contain duplicate fixture+market rows: {sample}")


def result_value(row: pd.Series) -> str:
    actionable = norm_text(row.get("actionable_result"))
    if actionable in GRADED_RESULTS:
        return actionable
    primary = norm_text(row.get("primary_result"))
    if primary in GRADED_RESULTS:
        return primary
    return actionable or primary


def profit_value(row: pd.Series) -> float | pd.NA:
    actionable_profit = pd.to_numeric(pd.Series([row.get("actionable_profit_units")]), errors="coerce").iloc[0]
    primary_profit = pd.to_numeric(pd.Series([row.get("primary_profit_units")]), errors="coerce").iloc[0]
    if pd.notna(actionable_profit):
        return float(actionable_profit)
    if pd.notna(primary_profit):
        return float(primary_profit)
    return pd.NA


def join_shortlist_to_labeled(
    shortlist: pd.DataFrame,
    labeled: pd.DataFrame,
    date_label: str,
) -> pd.DataFrame:
    if shortlist.empty:
        return pd.DataFrame(columns=HISTORICAL_COLUMNS)

    validate_labeled_for_join(labeled, date_label)
    labeled_join_cols = [
        col
        for col in [
            "fixture_id",
            "market_primary",
            "actionable_result",
            "actionable_profit_units",
            "primary_result",
            "primary_profit_units",
        ]
        if col in labeled.columns
    ]
    labeled_exact = labeled[labeled_join_cols].copy()
    labeled_exact["_matched_market"] = True

    merged = shortlist.merge(
        labeled_exact,
        on=["fixture_id", "market_primary"],
        how="left",
        validate="many_to_one",
        suffixes=("", "_labeled"),
    )

    labeled_fixture_ids = set(labeled["fixture_id"].dropna().tolist())
    merged["_matched_market"] = merged["_matched_market"].fillna(False)
    merged["result_status"] = "UNMATCHED_FIXTURE"
    merged.loc[merged["fixture_id"].isin(labeled_fixture_ids), "result_status"] = "UNMATCHED_MARKET"
    merged.loc[merged["_matched_market"], "result_status"] = "RESULT_AVAILABLE"

    for col in ["actionable_result", "primary_result"]:
        if col not in merged.columns:
            merged[col] = pd.NA

    merged["actionable_result"] = merged.apply(result_value, axis=1)
    merged["profit_units"] = merged.apply(profit_value, axis=1)
    merged["stake_units"] = merged["result_status"].eq("RESULT_AVAILABLE").astype(float)
    merged["historical_batch_date"] = date_label

    for col in HISTORICAL_COLUMNS:
        if col not in merged.columns:
            merged[col] = pd.NA
    return merged[HISTORICAL_COLUMNS].copy()


def build_summary(df: pd.DataFrame, segment_col: str | None = None) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMNS)

    if segment_col is None:
        groups = [("ALL", df)]
    else:
        groups = [(value, subset) for value, subset in df.groupby(segment_col, dropna=False, sort=True)]

    rows = []
    for segment, subset in groups:
        result = subset["actionable_result"].map(norm_text)
        result_status = subset["result_status"].map(norm_text)
        graded = result_status.eq("RESULT_AVAILABLE") & result.isin(GRADED_RESULTS)
        graded_subset = subset[graded].copy()
        profit_total = pd.to_numeric(graded_subset["profit_units"], errors="coerce").sum()
        graded_rows = int(len(graded_subset))
        rows.append(
            {
                "segment": segment,
                "rows_total": int(len(subset)),
                "graded_rows": graded_rows,
                "wins": int(result[graded].eq("WIN").sum()),
                "losses": int(result[graded].eq("LOSS").sum()),
                "pushes": int(result[graded].eq("PUSH").sum()),
                "voids": int(result[graded].eq("VOID").sum()),
                "profit_units_total": round(float(profit_total), 6) if graded_rows else 0.0,
                "roi_percent": round(float(profit_total) / graded_rows * 100.0, 6)
                if graded_rows
                else pd.NA,
            }
        )
    return pd.DataFrame(rows, columns=SUMMARY_COLUMNS)


def write_report(
    path: Path,
    historical: pd.DataFrame,
    summaries: dict[str, pd.DataFrame],
    dates_covered: list[str],
) -> None:
    overall = summaries["overall"]
    if overall.empty:
        total_rows = graded_rows = 0
        profit = 0.0
        roi = pd.NA
    else:
        total_rows = int(overall.loc[0, "rows_total"])
        graded_rows = int(overall.loc[0, "graded_rows"])
        profit = float(overall.loc[0, "profit_units_total"])
        roi = overall.loc[0, "roi_percent"]

    lines = [
        "VSIGMA EXECUTION SHORTLIST HISTORICAL BACKTEST",
        "",
        f"Dates covered: {', '.join(dates_covered) if dates_covered else 'NONE'}",
        f"Total shortlist rows: {total_rows}",
        f"Graded rows: {graded_rows}",
        f"Profit units: {profit:.6f}",
        f"ROI percent: {roi if pd.notna(roi) else 'N/A'}",
        "",
    ]

    for title, key in [
        ("Source breakdown", "by_source"),
        ("Bucket breakdown", "by_bucket"),
        ("Market breakdown", "by_market"),
        ("League breakdown", "by_league"),
    ]:
        lines.append(title)
        summary = summaries[key]
        lines.append(summary.to_string(index=False) if not summary.empty else "No rows")
        lines.append("")

    meaningful = []
    for key in ["by_source", "by_bucket", "by_market", "by_league"]:
        summary = summaries[key]
        if not summary.empty:
            tmp = summary[pd.to_numeric(summary["graded_rows"], errors="coerce").fillna(0).gt(0)].copy()
            if not tmp.empty:
                tmp["summary"] = key
                meaningful.append(tmp)
    if meaningful:
        segments = pd.concat(meaningful, ignore_index=True)
        best = segments.sort_values(["roi_percent", "graded_rows"], ascending=[False, False]).head(5)
        worst = segments.sort_values(["roi_percent", "graded_rows"], ascending=[True, False]).head(5)
        lines.append("Best segments by ROI")
        lines.append(best[["summary", "segment", "graded_rows", "profit_units_total", "roi_percent"]].to_string(index=False))
        lines.append("")
        lines.append("Worst segments by ROI")
        lines.append(worst[["summary", "segment", "graded_rows", "profit_units_total", "roi_percent"]].to_string(index=False))
    else:
        lines.append("Best and worst segments by ROI")
        lines.append("No segments with graded rows.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_competition_report(
    path: Path,
    historical: pd.DataFrame,
    competition: pd.DataFrame,
    summaries: dict[str, pd.DataFrame],
    competition_summaries: dict[str, pd.DataFrame],
    dates_covered: list[str],
) -> None:
    standard_overall = summaries["overall"]
    competition_overall = competition_summaries["overall"]

    lines = [
        "VSIGMA COMPETITION ACCURACY MODE HISTORICAL BACKTEST",
        "",
        f"Dates covered: {', '.join(dates_covered) if dates_covered else 'NONE'}",
        "",
        "Standard shortlist overall",
        standard_overall.to_string(index=False) if not standard_overall.empty else "No rows",
        "",
        "Competition accuracy mode overall",
        competition_overall.to_string(index=False) if not competition_overall.empty else "No rows",
        "",
        "Competition bucket composition",
        competition_summaries["by_bucket"].to_string(index=False)
        if not competition_summaries["by_bucket"].empty
        else "No rows",
        "",
        "Competition market composition",
        competition_summaries["by_market"].to_string(index=False)
        if not competition_summaries["by_market"].empty
        else "No rows",
        "",
        "Standard source mix",
        summaries["by_source"].to_string(index=False) if not summaries["by_source"].empty else "No rows",
        "",
        "Competition source mix",
        competition_summaries["by_source"].to_string(index=False)
        if not competition_summaries["by_source"].empty
        else "No rows",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_historical_execution_shortlist_backtest(
    historical_dir: Path = DEFAULT_HISTORICAL_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    preserve_per_date: bool = True,
) -> tuple[dict[str, Path], pd.DataFrame, dict[str, pd.DataFrame], list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)

    historical_rows = []
    dates_covered = []
    for date_dir in discover_complete_dates(historical_dir):
        date_label = date_dir.name
        premium = read_csv_required(date_dir / PREMIUM_CSV)
        standard = read_csv_required(date_dir / STANDARD_CSV)
        labeled = read_csv_required(date_dir / LABELED_CSV)

        shortlist = reconstruct_execution_shortlist(premium, standard)
        joined = join_shortlist_to_labeled(shortlist, labeled, date_label)
        if not joined.empty:
            historical_rows.append(joined)
        dates_covered.append(date_label)

        if preserve_per_date:
            joined.to_csv(date_dir / HISTORICAL_OUTPUT, index=False)

    historical = (
        pd.concat(historical_rows, ignore_index=True, sort=False)
        if historical_rows
        else pd.DataFrame(columns=HISTORICAL_COLUMNS)
    )
    calibration_table = build_probability_calibration_table(historical)
    historical = add_competition_probability_calibration(historical, calibration_table)
    for col in HISTORICAL_COLUMNS:
        if col not in historical.columns:
            historical[col] = pd.NA
    historical = historical[HISTORICAL_COLUMNS].copy()

    if preserve_per_date and not historical.empty:
        for date_value, subset in historical.groupby("historical_batch_date", dropna=False, sort=True):
            date_dir = historical_dir / str(date_value)
            if date_dir.exists():
                subset.to_csv(date_dir / HISTORICAL_OUTPUT, index=False)

    summaries = {
        "overall": build_summary(historical),
        "by_date": build_summary(historical, "historical_batch_date"),
        "by_source": build_summary(historical, "execution_shortlist_source"),
        "by_bucket": build_summary(historical, "final_execution_bucket"),
        "by_market": build_summary(historical, "market_primary"),
        "by_league": build_summary(historical, "league"),
    }

    competition = historical[
        pd.to_numeric(
            historical.get("accuracy_mode_eligible_flag", pd.Series(index=historical.index, dtype=float)),
            errors="coerce",
        )
        .fillna(0)
        .eq(1)
    ].copy()
    competition_summaries = {
        "overall": build_summary(competition),
        "by_date": build_summary(competition, "historical_batch_date"),
        "by_source": build_summary(competition, "execution_shortlist_source"),
        "by_bucket": build_summary(competition, "accuracy_mode_bucket"),
        "by_market": build_summary(competition, "market_primary"),
        "by_league": build_summary(competition, "league"),
    }

    paths = {
        "historical": output_dir / HISTORICAL_OUTPUT,
        "overall": output_dir / OVERALL_OUTPUT,
        "by_date": output_dir / BY_DATE_OUTPUT,
        "by_source": output_dir / BY_SOURCE_OUTPUT,
        "by_bucket": output_dir / BY_BUCKET_OUTPUT,
        "by_market": output_dir / BY_MARKET_OUTPUT,
        "by_league": output_dir / BY_LEAGUE_OUTPUT,
        "report": output_dir / REPORT_OUTPUT,
        "competition_historical": output_dir / COMPETITION_HISTORICAL_OUTPUT,
        "competition_overall": output_dir / COMPETITION_OVERALL_OUTPUT,
        "competition_by_date": output_dir / COMPETITION_BY_DATE_OUTPUT,
        "competition_by_source": output_dir / COMPETITION_BY_SOURCE_OUTPUT,
        "competition_by_bucket": output_dir / COMPETITION_BY_BUCKET_OUTPUT,
        "competition_by_market": output_dir / COMPETITION_BY_MARKET_OUTPUT,
        "competition_by_league": output_dir / COMPETITION_BY_LEAGUE_OUTPUT,
        "competition_report": output_dir / COMPETITION_REPORT_OUTPUT,
    }

    historical.to_csv(paths["historical"], index=False)
    for key in ["overall", "by_date", "by_source", "by_bucket", "by_market", "by_league"]:
        summaries[key].to_csv(paths[key], index=False)
    write_report(paths["report"], historical, summaries, dates_covered)
    competition.to_csv(paths["competition_historical"], index=False)
    for key, path_key in [
        ("overall", "competition_overall"),
        ("by_date", "competition_by_date"),
        ("by_source", "competition_by_source"),
        ("by_bucket", "competition_by_bucket"),
        ("by_market", "competition_by_market"),
        ("by_league", "competition_by_league"),
    ]:
        competition_summaries[key].to_csv(paths[path_key], index=False)
    write_competition_report(
        paths["competition_report"],
        historical,
        competition,
        summaries,
        competition_summaries,
        dates_covered,
    )
    probability_paths, _probability_summary = build_probability_evaluation(
        paths["historical"],
        output_dir,
    )
    paths["probability_summary"] = probability_paths["summary"]
    paths["probability_report"] = probability_paths["report"]
    paths["probability_calibration_table"] = probability_paths["calibration_table"]
    paths["probability_calibration_report"] = probability_paths["calibration_report"]

    return paths, historical, summaries, dates_covered


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backtest historical vSIGMA execution-shortlist selections from per-date snapshots."
    )
    parser.add_argument("--historical-dir", default=str(DEFAULT_HISTORICAL_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--no-preserve-per-date",
        action="store_true",
        help="Do not write per-date reconstructed shortlist artifacts into historical snapshots.",
    )
    args = parser.parse_args()

    paths, historical, summaries, dates_covered = build_historical_execution_shortlist_backtest(
        historical_dir=Path(args.historical_dir),
        output_dir=Path(args.output_dir),
        preserve_per_date=not args.no_preserve_per_date,
    )

    print("\n=== EXECUTION SHORTLIST HISTORICAL BACKTEST COMPLETADO ===")
    for key, path in paths.items():
        print(f"{key}: {path}")
    print(f"Dates covered: {dates_covered}")
    print(f"Total shortlist rows: {len(historical)}")
    overall = summaries["overall"]
    if not overall.empty:
        print(f"Graded rows: {int(overall.loc[0, 'graded_rows'])}")
        print(f"Profit units total: {overall.loc[0, 'profit_units_total']}")
        print(f"ROI percent: {overall.loc[0, 'roi_percent']}")
    else:
        print("Graded rows: 0")
        print("Profit units total: 0.0")
        print("ROI percent: N/A")

    if not historical.empty:
        display_cols = [
            col
            for col in [
                "historical_batch_date",
                "execution_rank",
                "execution_shortlist_source",
                "fixture_id",
                "league",
                "market_primary",
                "final_execution_bucket",
                "final_recommendation",
                "execution_score",
                "result_status",
                "actionable_result",
                "profit_units",
            ]
            if col in historical.columns
        ]
        print("\nTop rows by execution_score:")
        print(
            historical.sort_values("execution_score", ascending=False, na_position="last")[
                display_cols
            ]
            .head(10)
            .to_string(index=False)
        )


if __name__ == "__main__":
    main()
