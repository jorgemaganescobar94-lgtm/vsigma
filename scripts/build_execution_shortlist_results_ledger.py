from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_PROCESSED_DIR = Path("data/processed")

SHORTLIST_CSV = "vsigma_today_execution_shortlist.csv"
LABELED_RESULTS_CSV = "vsigma_market_results_labeled.csv"
DEEP_ANALYSIS_CSV = "vsigma_deep_analysis_candidates.csv"

LEDGER_OUTPUT = "vsigma_execution_shortlist_results_ledger.csv"
SUMMARY_OUTPUT = "vsigma_execution_shortlist_results_summary.csv"

JOIN_KEYS = ["fixture_id", "market_primary"]
GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}

REQUIRED_SHORTLIST_COLUMNS = [
    "execution_rank",
    "execution_shortlist_source",
    "fixture_id",
    "date",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "final_execution_bucket",
    "final_recommendation",
    "execution_score",
    "selection_score",
    "primary_model_prob",
    "primary_odds_used",
    "primary_edge",
]

RESULT_COLUMNS = [
    "actionable_result",
    "actionable_profit_units",
    "primary_result",
    "primary_profit_units",
]

LEDGER_COLUMNS = [
    *REQUIRED_SHORTLIST_COLUMNS,
    *RESULT_COLUMNS,
    "ledger_result_status",
]

NUMERIC_LEDGER_COLUMNS = [
    "execution_rank",
    "execution_score",
    "selection_score",
    "primary_model_prob",
    "primary_odds_used",
    "primary_edge",
    "actionable_profit_units",
    "primary_profit_units",
]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def read_csv_required(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")
    return pd.read_csv(path)


def require_columns(df: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def read_labeled_results(processed_dir: Path) -> pd.DataFrame:
    labeled_path = processed_dir / LABELED_RESULTS_CSV
    if labeled_path.exists():
        labeled = pd.read_csv(labeled_path)
        require_columns(labeled, JOIN_KEYS, LABELED_RESULTS_CSV)
        for col in RESULT_COLUMNS:
            if col not in labeled.columns:
                labeled[col] = pd.NA
        return labeled[JOIN_KEYS + RESULT_COLUMNS].copy()

    deep_path = processed_dir / DEEP_ANALYSIS_CSV
    if deep_path.exists():
        deep = pd.read_csv(deep_path)
        require_columns(deep, JOIN_KEYS, DEEP_ANALYSIS_CSV)
        fallback = deep[JOIN_KEYS].copy()
        for col in RESULT_COLUMNS:
            fallback[col] = pd.NA
        return fallback

    return pd.DataFrame(columns=JOIN_KEYS + RESULT_COLUMNS)


def validate_shortlist(shortlist: pd.DataFrame) -> None:
    require_columns(shortlist, REQUIRED_SHORTLIST_COLUMNS, SHORTLIST_CSV)

    if shortlist["execution_rank"].duplicated().any():
        duplicated = shortlist.loc[
            shortlist["execution_rank"].duplicated(keep=False), "execution_rank"
        ].head(10).tolist()
        raise ValueError(f"Execution shortlist has duplicate execution_rank values: {duplicated}")

    row_keys = shortlist[["fixture_id", "market_primary", "execution_rank"]]
    if row_keys.duplicated().any():
        duplicated = row_keys[row_keys.duplicated(keep=False)].head(10).to_dict("records")
        raise ValueError(
            "Execution shortlist has duplicate fixture_id + market_primary + execution_rank rows: "
            f"{duplicated}"
        )


def validate_labeled_matches(shortlist: pd.DataFrame, labeled: pd.DataFrame) -> None:
    if labeled.empty:
        return

    shortlist_keys = shortlist[JOIN_KEYS].drop_duplicates()
    matched = labeled.merge(shortlist_keys, on=JOIN_KEYS, how="inner")
    duplicate_counts = matched.groupby(JOIN_KEYS, dropna=False).size().reset_index(name="matches")
    duplicate_counts = duplicate_counts[duplicate_counts["matches"].gt(1)]
    if not duplicate_counts.empty:
        raise ValueError(
            "Execution shortlist row matches multiple labeled result rows: "
            f"{duplicate_counts.head(10).to_dict('records')}"
        )


def result_status(row: pd.Series) -> str:
    if not bool(row.get("_matched_labeled_result", False)):
        return "UNMATCHED"
    actionable = norm_text(row.get("actionable_result"))
    if actionable in GRADED_RESULTS:
        return "RESULT_AVAILABLE"
    return "PENDING"


def add_profit_columns(ledger: pd.DataFrame) -> pd.DataFrame:
    out = ledger.copy()
    for col in ["actionable_profit_units", "primary_profit_units"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out["_ledger_profit_units"] = out["actionable_profit_units"].combine_first(
        out["primary_profit_units"]
    )
    return out


def build_ledger(processed_dir: Path = DEFAULT_PROCESSED_DIR) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame]:
    shortlist = read_csv_required(processed_dir / SHORTLIST_CSV, "execution shortlist")
    validate_shortlist(shortlist)
    labeled = read_labeled_results(processed_dir)
    validate_labeled_matches(shortlist, labeled)

    if labeled.empty:
        labeled_for_merge = pd.DataFrame(columns=[*JOIN_KEYS, *RESULT_COLUMNS])
    else:
        labeled_for_merge = labeled.copy()
    labeled_for_merge["_matched_labeled_result"] = True

    ledger = shortlist[REQUIRED_SHORTLIST_COLUMNS].merge(
        labeled_for_merge,
        on=JOIN_KEYS,
        how="left",
        sort=False,
        validate="many_to_one",
    )
    ledger["_matched_labeled_result"] = ledger["_matched_labeled_result"].fillna(False)

    for col in NUMERIC_LEDGER_COLUMNS:
        if col in ledger.columns:
            ledger[col] = pd.to_numeric(ledger[col], errors="coerce")

    ledger["ledger_result_status"] = ledger.apply(result_status, axis=1)
    ledger = add_profit_columns(ledger)
    ledger = ledger.sort_values("execution_rank", ascending=True, na_position="last").reset_index(drop=True)

    validate_ledger(ledger)
    summary = build_summary(ledger)

    processed_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "LEDGER": processed_dir / LEDGER_OUTPUT,
        "SUMMARY": processed_dir / SUMMARY_OUTPUT,
    }
    ledger[LEDGER_COLUMNS].to_csv(paths["LEDGER"], index=False)
    summary.to_csv(paths["SUMMARY"], index=False)
    return paths, ledger[LEDGER_COLUMNS].copy(), summary


def validate_ledger(ledger: pd.DataFrame) -> None:
    if len(ledger) != len(ledger[["fixture_id", "market_primary", "execution_rank"]].drop_duplicates()):
        duplicated = ledger.loc[
            ledger[["fixture_id", "market_primary", "execution_rank"]].duplicated(keep=False),
            ["fixture_id", "market_primary", "execution_rank"],
        ].head(10).to_dict("records")
        raise ValueError(
            "Execution ledger has duplicate fixture_id + market_primary + execution_rank rows: "
            f"{duplicated}"
        )
    if ledger["execution_rank"].duplicated().any():
        duplicated = ledger.loc[
            ledger["execution_rank"].duplicated(keep=False), "execution_rank"
        ].head(10).tolist()
        raise ValueError(f"Execution ledger has duplicate execution_rank values: {duplicated}")


def summary_row(
    summary_scope: str,
    metric: str,
    rows_total: int,
    value_num: float | int | None = None,
    value_text: object = pd.NA,
) -> dict[str, object]:
    return {
        "summary_scope": summary_scope,
        "metric": metric,
        "rows_total": int(rows_total),
        "value_num": value_num if value_num is not None else pd.NA,
        "value_text": value_text,
    }


def build_metric_rows(df: pd.DataFrame, summary_scope: str = "overall") -> list[dict[str, object]]:
    result_norm = df["actionable_result"].map(norm_text) if "actionable_result" in df.columns else pd.Series("", index=df.index)
    recommendation_norm = df["final_recommendation"].map(norm_text)
    bucket_norm = df["final_execution_bucket"].map(norm_text)
    status = df["ledger_result_status"].map(norm_text)
    profit = pd.to_numeric(df.get("_ledger_profit_units", pd.Series(index=df.index)), errors="coerce")
    result_available = status.eq("RESULT_AVAILABLE")
    graded_profit = profit.where(result_available)
    stake_rows = int(result_available.sum())
    profit_total = float(graded_profit.sum(skipna=True)) if stake_rows else 0.0
    roi_percent = (profit_total / stake_rows * 100.0) if stake_rows else pd.NA

    return [
        summary_row(summary_scope, "shortlist_rows", len(df), len(df)),
        summary_row(summary_scope, "result_available_rows", len(df), int(result_available.sum())),
        summary_row(summary_scope, "pending_rows", len(df), int(status.eq("PENDING").sum())),
        summary_row(summary_scope, "unmatched_rows", len(df), int(status.eq("UNMATCHED").sum())),
        summary_row(summary_scope, "bet_rows", len(df), int(recommendation_norm.eq("BET").sum())),
        summary_row(summary_scope, "lean_play_rows", len(df), int(recommendation_norm.eq("LEAN_PLAY").sum())),
        summary_row(summary_scope, "premium_rows", len(df), int(bucket_norm.eq("APPROVED_PREMIUM").sum())),
        summary_row(summary_scope, "standard_rows", len(df), int(bucket_norm.eq("APPROVED_STANDARD").sum())),
        summary_row(summary_scope, "wins", len(df), int(result_norm.eq("WIN").sum())),
        summary_row(summary_scope, "losses", len(df), int(result_norm.eq("LOSS").sum())),
        summary_row(summary_scope, "pushes", len(df), int(result_norm.eq("PUSH").sum())),
        summary_row(summary_scope, "voids", len(df), int(result_norm.eq("VOID").sum())),
        summary_row(summary_scope, "profit_units_total", len(df), round(profit_total, 6)),
        summary_row(
            summary_scope,
            "roi_percent",
            len(df),
            round(float(roi_percent), 6) if pd.notna(roi_percent) else pd.NA,
        ),
        summary_row(
            summary_scope,
            "avg_execution_score",
            len(df),
            round(pd.to_numeric(df["execution_score"], errors="coerce").mean(), 6)
            if len(df)
            else pd.NA,
        ),
        summary_row(
            summary_scope,
            "avg_primary_edge",
            len(df),
            round(pd.to_numeric(df["primary_edge"], errors="coerce").mean(), 6) if len(df) else pd.NA,
        ),
    ]


def build_group_rows(df: pd.DataFrame, group_col: str, summary_scope: str) -> list[dict[str, object]]:
    if group_col not in df.columns:
        return []

    rows: list[dict[str, object]] = []
    for group_value, subset in df.groupby(group_col, dropna=False, sort=True):
        for row in build_metric_rows(subset, summary_scope):
            row["value_text"] = group_value
            rows.append(row)
    return rows


def build_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    working = add_profit_columns(ledger)
    rows = build_metric_rows(working)
    group_specs = [
        ("final_execution_bucket", "by_final_execution_bucket"),
        ("final_recommendation", "by_final_recommendation"),
        ("execution_shortlist_source", "by_execution_shortlist_source"),
        ("league", "by_league"),
        ("market_primary", "by_market_primary"),
    ]
    for group_col, scope in group_specs:
        rows.extend(build_group_rows(working, group_col, scope))
    return pd.DataFrame(rows, columns=["summary_scope", "metric", "rows_total", "value_num", "value_text"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a results ledger for today's final execution shortlist."
    )
    parser.add_argument(
        "--processed-dir",
        default=str(DEFAULT_PROCESSED_DIR),
        help="Directory containing execution shortlist and labeled market result CSVs.",
    )
    args = parser.parse_args()

    paths, ledger, summary = build_ledger(Path(args.processed_dir))

    print("\n=== EXECUTION SHORTLIST RESULTS LEDGER COMPLETADO ===")
    print(f"LEDGER: {paths['LEDGER']}")
    print(f"SUMMARY: {paths['SUMMARY']}")

    metric_map = summary[summary["summary_scope"].eq("overall")].set_index("metric")["value_num"].to_dict()
    print("\nCounts:")
    print(f"Ledger rows: {len(ledger)}")
    print(f"Result available: {int(metric_map.get('result_available_rows', 0) or 0)}")
    print(f"Pending: {int(metric_map.get('pending_rows', 0) or 0)}")
    print(f"Unmatched: {int(metric_map.get('unmatched_rows', 0) or 0)}")
    print(f"Profit units total: {metric_map.get('profit_units_total')}")
    print(f"ROI percent: {metric_map.get('roi_percent')}")

    display_cols = [
        col
        for col in [
            "execution_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "final_recommendation",
            "ledger_result_status",
            "actionable_result",
            "actionable_profit_units",
            "primary_result",
            "primary_profit_units",
        ]
        if col in ledger.columns
    ]
    print("\nFirst ledger rows:")
    print(ledger[display_cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
