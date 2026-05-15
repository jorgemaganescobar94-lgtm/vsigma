from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_SOURCE_CSV = Path("data/processed/vsigma_execution_shortlist_historical.csv")
DEFAULT_OUTPUT_DIR = Path("data/processed")

OVERALL_OUTPUT = "vsigma_execution_mode_comparison_overall.csv"
BY_DATE_OUTPUT = "vsigma_execution_mode_comparison_by_date.csv"
BY_SOURCE_MIX_OUTPUT = "vsigma_execution_mode_comparison_by_source_mix.csv"
BY_MARKET_OUTPUT = "vsigma_execution_mode_comparison_by_market.csv"
BY_BUCKET_OUTPUT = "vsigma_execution_mode_comparison_by_bucket.csv"
REPORT_OUTPUT = "vsigma_execution_mode_comparison_report.txt"

MODE_SOURCES = {
    "CORE_ONLY": {"PREMIUM_CORE"},
    "CORE_PLUS_STANDARD": {"PREMIUM_CORE", "STANDARD_FILL"},
    "FULL_SHORTLIST": {"PREMIUM_CORE", "PREMIUM_EXTENDED", "STANDARD_FILL"},
    "COMPETITION_ACCURACY_MODE": {"PREMIUM_CORE", "PREMIUM_EXTENDED", "STANDARD_FILL"},
}

GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}
SUMMARY_COLUMNS = [
    "mode",
    "rows_total",
    "graded_rows",
    "wins",
    "losses",
    "pushes",
    "voids",
    "hit_rate",
    "profit_units_total",
    "roi_percent",
    "avg_odds",
    "avg_edge",
    "avg_execution_score",
    "max_drawdown",
]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def read_source(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing historical execution-shortlist source: {path}")
    df = pd.read_csv(path)
    required = [
        "historical_batch_date",
        "execution_shortlist_source",
        "actionable_result",
        "result_status",
        "profit_units",
        "primary_odds_used",
        "primary_edge",
        "execution_score",
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Historical execution-shortlist source is missing columns: {missing}")
    return df


def filter_mode(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode not in MODE_SOURCES:
        raise ValueError(f"Unknown execution mode: {mode}")
    if mode == "COMPETITION_ACCURACY_MODE":
        if "accuracy_mode_eligible_flag" not in df.columns:
            return df.iloc[0:0].copy()
        return df[
            pd.to_numeric(df["accuracy_mode_eligible_flag"], errors="coerce").fillna(0).eq(1)
        ].copy()
    sources = MODE_SOURCES[mode]
    source_norm = df["execution_shortlist_source"].map(norm_text)
    return df[source_norm.isin(sources)].copy()


def graded_mask(df: pd.DataFrame) -> pd.Series:
    return df["result_status"].map(norm_text).eq("RESULT_AVAILABLE") & df["actionable_result"].map(
        norm_text
    ).isin(GRADED_RESULTS)


def compute_max_drawdown(by_date: pd.DataFrame) -> float | pd.NA:
    if by_date.empty:
        return pd.NA
    daily = by_date.sort_values("historical_batch_date")["profit_units_total"].fillna(0.0)
    equity = daily.cumsum()
    running_peak = equity.cummax()
    drawdown = equity - running_peak
    return round(float(drawdown.min()), 6)


def summarize_mode(df: pd.DataFrame, mode: str) -> dict[str, object]:
    mode_df = filter_mode(df, mode)
    graded = mode_df[graded_mask(mode_df)].copy()
    result = graded["actionable_result"].map(norm_text)
    wins = int(result.eq("WIN").sum())
    losses = int(result.eq("LOSS").sum())
    pushes = int(result.eq("PUSH").sum())
    voids = int(result.eq("VOID").sum())
    decided = wins + losses
    graded_rows = int(len(graded))
    profit_total = pd.to_numeric(graded["profit_units"], errors="coerce").sum()
    by_date = summarize_mode_by_date(df, mode)

    return {
        "mode": mode,
        "rows_total": int(len(mode_df)),
        "graded_rows": graded_rows,
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "voids": voids,
        "hit_rate": round(wins / decided * 100.0, 6) if decided else pd.NA,
        "profit_units_total": round(float(profit_total), 6) if graded_rows else 0.0,
        "roi_percent": round(float(profit_total) / graded_rows * 100.0, 6) if graded_rows else pd.NA,
        "avg_odds": round(pd.to_numeric(graded["primary_odds_used"], errors="coerce").mean(), 6)
        if graded_rows
        else pd.NA,
        "avg_edge": round(pd.to_numeric(mode_df["primary_edge"], errors="coerce").mean(), 6)
        if len(mode_df)
        else pd.NA,
        "avg_execution_score": round(pd.to_numeric(mode_df["execution_score"], errors="coerce").mean(), 6)
        if len(mode_df)
        else pd.NA,
        "max_drawdown": compute_max_drawdown(by_date),
    }


def summarize_mode_by_date(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    mode_df = filter_mode(df, mode)
    if mode_df.empty:
        return pd.DataFrame(
            columns=[
                "mode",
                "historical_batch_date",
                "rows_total",
                "graded_rows",
                "wins",
                "losses",
                "pushes",
                "voids",
                "profit_units_total",
                "roi_percent",
                "equity_units",
            ]
        )

    rows = []
    for date_value, subset in mode_df.groupby("historical_batch_date", dropna=False, sort=True):
        graded = subset[graded_mask(subset)].copy()
        result = graded["actionable_result"].map(norm_text)
        profit_total = pd.to_numeric(graded["profit_units"], errors="coerce").sum()
        graded_rows = int(len(graded))
        rows.append(
            {
                "mode": mode,
                "historical_batch_date": date_value,
                "rows_total": int(len(subset)),
                "graded_rows": graded_rows,
                "wins": int(result.eq("WIN").sum()),
                "losses": int(result.eq("LOSS").sum()),
                "pushes": int(result.eq("PUSH").sum()),
                "voids": int(result.eq("VOID").sum()),
                "profit_units_total": round(float(profit_total), 6) if graded_rows else 0.0,
                "roi_percent": round(float(profit_total) / graded_rows * 100.0, 6)
                if graded_rows
                else pd.NA,
            }
        )
    out = pd.DataFrame(rows).sort_values(["mode", "historical_batch_date"]).reset_index(drop=True)
    out["equity_units"] = out.groupby("mode")["profit_units_total"].cumsum().round(6)
    return out


def build_overall(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([summarize_mode(df, mode) for mode in MODE_SOURCES], columns=SUMMARY_COLUMNS)


def build_by_date(df: pd.DataFrame) -> pd.DataFrame:
    parts = [summarize_mode_by_date(df, mode) for mode in MODE_SOURCES]
    return pd.concat(parts, ignore_index=True, sort=False) if parts else pd.DataFrame()


def build_by_source_mix(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mode, sources in MODE_SOURCES.items():
        mode_df = filter_mode(df, mode)
        for source in sorted(sources):
            subset = mode_df[mode_df["execution_shortlist_source"].map(norm_text).eq(source)].copy()
            graded = subset[graded_mask(subset)].copy()
            result = graded["actionable_result"].map(norm_text)
            profit_total = pd.to_numeric(graded["profit_units"], errors="coerce").sum()
            graded_rows = int(len(graded))
            rows.append(
                {
                    "mode": mode,
                    "execution_shortlist_source": source,
                    "rows_total": int(len(subset)),
                    "graded_rows": graded_rows,
                    "wins": int(result.eq("WIN").sum()),
                    "losses": int(result.eq("LOSS").sum()),
                    "pushes": int(result.eq("PUSH").sum()),
                    "voids": int(result.eq("VOID").sum()),
                    "profit_units_total": round(float(profit_total), 6) if graded_rows else 0.0,
                    "roi_percent": round(float(profit_total) / graded_rows * 100.0, 6)
                    if graded_rows
                    else pd.NA,
                }
            )
    return pd.DataFrame(rows)


def summarize_mode_by_group(df: pd.DataFrame, mode: str, group_col: str) -> pd.DataFrame:
    mode_df = filter_mode(df, mode)
    if mode_df.empty or group_col not in mode_df.columns:
        return pd.DataFrame(
            columns=[
                "mode",
                group_col,
                "rows_total",
                "graded_rows",
                "wins",
                "losses",
                "pushes",
                "voids",
                "profit_units_total",
                "roi_percent",
            ]
        )

    rows = []
    for value, subset in mode_df.groupby(group_col, dropna=False, sort=True):
        graded = subset[graded_mask(subset)].copy()
        result = graded["actionable_result"].map(norm_text)
        profit_total = pd.to_numeric(graded["profit_units"], errors="coerce").sum()
        graded_rows = int(len(graded))
        rows.append(
            {
                "mode": mode,
                group_col: value,
                "rows_total": int(len(subset)),
                "graded_rows": graded_rows,
                "wins": int(result.eq("WIN").sum()),
                "losses": int(result.eq("LOSS").sum()),
                "pushes": int(result.eq("PUSH").sum()),
                "voids": int(result.eq("VOID").sum()),
                "profit_units_total": round(float(profit_total), 6) if graded_rows else 0.0,
                "roi_percent": round(float(profit_total) / graded_rows * 100.0, 6)
                if graded_rows
                else pd.NA,
            }
        )
    return pd.DataFrame(rows)


def build_by_market(df: pd.DataFrame) -> pd.DataFrame:
    parts = [summarize_mode_by_group(df, mode, "market_primary") for mode in MODE_SOURCES]
    return pd.concat(parts, ignore_index=True, sort=False) if parts else pd.DataFrame()


def build_by_bucket(df: pd.DataFrame) -> pd.DataFrame:
    group_col = "accuracy_mode_bucket" if "accuracy_mode_bucket" in df.columns else "final_execution_bucket"
    parts = [summarize_mode_by_group(df, mode, group_col) for mode in MODE_SOURCES]
    return pd.concat(parts, ignore_index=True, sort=False) if parts else pd.DataFrame()


def write_report(
    path: Path,
    overall: pd.DataFrame,
    by_date: pd.DataFrame,
    by_source_mix: pd.DataFrame,
    by_market: pd.DataFrame,
    by_bucket: pd.DataFrame,
) -> None:
    if overall.empty:
        best_text = "N/A"
    else:
        best = overall.sort_values(
            ["roi_percent", "profit_units_total", "graded_rows"],
            ascending=[False, False, False],
            na_position="last",
        ).iloc[0]
        best_text = (
            f"{best['mode']} | ROI={best['roi_percent']}% | "
            f"profit={best['profit_units_total']}u | graded={int(best['graded_rows'])}"
        )

    lines = [
        "VSIGMA EXECUTION MODE COMPARISON",
        "",
        f"Best mode: {best_text}",
        "",
        "Overall",
        overall.to_string(index=False) if not overall.empty else "No rows",
        "",
        "Profit by date sequence",
        by_date.to_string(index=False) if not by_date.empty else "No rows",
        "",
        "Source mix",
        by_source_mix.to_string(index=False) if not by_source_mix.empty else "No rows",
        "",
        "Market composition",
        by_market.to_string(index=False) if not by_market.empty else "No rows",
        "",
        "Bucket composition",
        by_bucket.to_string(index=False) if not by_bucket.empty else "No rows",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_execution_mode_comparison(
    source_csv: Path = DEFAULT_SOURCE_CSV,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source = read_source(source_csv)
    output_dir.mkdir(parents=True, exist_ok=True)

    overall = build_overall(source)
    by_date = build_by_date(source)
    by_source_mix = build_by_source_mix(source)
    by_market = build_by_market(source)
    by_bucket = build_by_bucket(source)

    paths = {
        "overall": output_dir / OVERALL_OUTPUT,
        "by_date": output_dir / BY_DATE_OUTPUT,
        "by_source_mix": output_dir / BY_SOURCE_MIX_OUTPUT,
        "by_market": output_dir / BY_MARKET_OUTPUT,
        "by_bucket": output_dir / BY_BUCKET_OUTPUT,
        "report": output_dir / REPORT_OUTPUT,
    }
    overall.to_csv(paths["overall"], index=False)
    by_date.to_csv(paths["by_date"], index=False)
    by_source_mix.to_csv(paths["by_source_mix"], index=False)
    by_market.to_csv(paths["by_market"], index=False)
    by_bucket.to_csv(paths["by_bucket"], index=False)
    write_report(paths["report"], overall, by_date, by_source_mix, by_market, by_bucket)
    return paths, overall, by_date, by_source_mix


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare vSIGMA historical execution modes from execution-shortlist backtest data."
    )
    parser.add_argument("--source-csv", default=str(DEFAULT_SOURCE_CSV))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    paths, overall, by_date, by_source_mix = build_execution_mode_comparison(
        source_csv=Path(args.source_csv),
        output_dir=Path(args.output_dir),
    )

    print("\n=== EXECUTION MODE COMPARISON COMPLETADO ===")
    for key, path in paths.items():
        print(f"{key}: {path}")
    print("\nOverall:")
    print(overall.to_string(index=False))
    if not overall.empty:
        best = overall.sort_values(
            ["roi_percent", "profit_units_total", "graded_rows"],
            ascending=[False, False, False],
            na_position="last",
        ).iloc[0]
        print(
            f"\nBest mode: {best['mode']} | ROI={best['roi_percent']}% | "
            f"profit={best['profit_units_total']}u | graded={int(best['graded_rows'])}"
        )


if __name__ == "__main__":
    main()
