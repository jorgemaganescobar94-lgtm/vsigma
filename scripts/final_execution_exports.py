from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

try:
    from deep_analysis_candidates import DEEP_ANALYSIS_OUTPUT_COLUMNS
except ModuleNotFoundError:
    from scripts.deep_analysis_candidates import DEEP_ANALYSIS_OUTPUT_COLUMNS


DEFAULT_SOURCE_CSV = Path("data/processed/vsigma_deep_analysis_candidates.csv")
DEFAULT_OUTPUT_DIR = Path("data/processed")

APPROVED_CSV = "vsigma_final_approved_candidates.csv"
APPROVED_PREMIUM_CSV = "vsigma_final_approved_premium_candidates.csv"
APPROVED_STANDARD_CSV = "vsigma_final_approved_standard_candidates.csv"
DOWNGRADED_CSV = "vsigma_final_downgraded_candidates.csv"
BLOCKED_CSV = "vsigma_final_blocked_candidates.csv"
WATCH_CSV = "vsigma_final_watch_candidates.csv"
SUMMARY_CSV = "vsigma_final_governance_summary.csv"

ACTIONABLE_RECOMMENDATIONS = {"BET", "LEAN_PLAY"}
MARKET_FIT_DOWNGRADED_STATUSES = {"MARKET_FIT_DOWNGRADED"}
MARKET_FIT_BLOCKED_STATUSES = {"MARKET_FIT_BLOCKED"}
BLOCKING_RECOMMENDATIONS = {
    "NO_BET",
    "NO BET",
    "PASS",
    "SKIP",
    "BLOCK",
    "BLOCKED",
    "REJECT",
    "REJECTED",
    "AVOID",
}

REQUIRED_COLUMNS = [
    "fixture_id",
    "final_recommendation",
    "execution_verdict",
    "production_governance_status",
]

BUCKET_ORDER = {
    "APPROVED_PREMIUM": 1,
    "APPROVED_STANDARD": 2,
    "DOWNGRADED": 3,
    "BLOCKED": 4,
    "WATCH": 5,
}

OUTPUT_FILENAMES = {
    "APPROVED_PREMIUM": APPROVED_PREMIUM_CSV,
    "APPROVED_STANDARD": APPROVED_STANDARD_CSV,
    "DOWNGRADED": DOWNGRADED_CSV,
    "BLOCKED": BLOCKED_CSV,
    "WATCH": WATCH_CSV,
}


def norm_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Final execution export source is missing required columns: {missing}")


def is_actionable_recommendation(value) -> bool:
    return norm_text(value) in ACTIONABLE_RECOMMENDATIONS


def is_blocking_recommendation(value) -> bool:
    return norm_text(value) in BLOCKING_RECOMMENDATIONS


def classify_final_execution_bucket(row: pd.Series) -> tuple[str, str]:
    governance_status = norm_text(row.get("production_governance_status"))
    final_recommendation = norm_text(row.get("final_recommendation"))
    execution_verdict = norm_text(row.get("execution_verdict"))
    base_recommendation = norm_text(row.get("base_final_recommendation"))
    market_fit_status = norm_text(row.get("execution_market_fit_status"))
    fragility_reason = norm_text(row.get("execution_fragility_reason"))

    final_actionable = final_recommendation in ACTIONABLE_RECOMMENDATIONS
    base_actionable = base_recommendation in ACTIONABLE_RECOMMENDATIONS

    if market_fit_status in MARKET_FIT_DOWNGRADED_STATUSES:
        return (
            "DOWNGRADED",
            f"Execution market-fit hardening downgraded the candidate: {fragility_reason or market_fit_status}.",
        )

    if market_fit_status in MARKET_FIT_BLOCKED_STATUSES:
        return (
            "BLOCKED",
            f"Execution market-fit hardening blocked the candidate: {fragility_reason or market_fit_status}.",
        )

    if governance_status in {
        "DOWNGRADED_NO_PROMOTED_RULE_MATCH",
        "DOWNGRADED_GENERIC_PROMOTED_RULE_ONLY",
    }:
        return (
            "DOWNGRADED",
            "Base actionable recommendation was downgraded because promoted-rule evidence was absent or too generic.",
        )

    if governance_status == "APPROVED_BY_PREMIUM_PROMOTED_RULE" and final_actionable:
        return (
            "APPROVED_PREMIUM",
            "Final actionable recommendation is approved by premium promoted-rule evidence.",
        )

    if governance_status == "APPROVED_BY_PROMOTED_RULE" and final_actionable:
        return (
            "APPROVED_STANDARD",
            "Final actionable recommendation is approved by standard promoted-rule evidence.",
        )

    if final_actionable:
        return (
            "BLOCKED",
            "Final recommendation is actionable but lacks an approved production governance status.",
        )

    if (
        is_blocking_recommendation(final_recommendation)
        or is_blocking_recommendation(execution_verdict)
        or (base_actionable and not final_actionable)
    ):
        return (
            "BLOCKED",
            "Candidate is explicitly non-executable after final recommendation or execution governance.",
        )

    return (
        "WATCH",
        "Candidate remains non-actionable watchlist context after production governance.",
    )


def add_final_execution_buckets(df: pd.DataFrame) -> pd.DataFrame:
    require_columns(df, REQUIRED_COLUMNS)

    out = df.copy()
    classifications = out.apply(classify_final_execution_bucket, axis=1)
    out["final_execution_bucket"] = [bucket for bucket, _ in classifications]
    out["final_execution_reason"] = [reason for _, reason in classifications]
    out["final_execution_bucket_order"] = out["final_execution_bucket"].map(BUCKET_ORDER)
    return sort_candidates(out)


def sort_candidates(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    sort_cols = []
    ascending = []

    if "final_execution_bucket_order" in out.columns:
        sort_cols.append("final_execution_bucket_order")
        ascending.append(True)

    if "shortlist_rank" in out.columns:
        out["_sort_shortlist_rank"] = pd.to_numeric(out["shortlist_rank"], errors="coerce")
        sort_cols.append("_sort_shortlist_rank")
        ascending.append(True)

    if "selection_score" in out.columns:
        out["_sort_selection_score"] = pd.to_numeric(out["selection_score"], errors="coerce")
        sort_cols.append("_sort_selection_score")
        ascending.append(False)

    if "primary_edge" in out.columns:
        out["_sort_primary_edge"] = pd.to_numeric(out["primary_edge"], errors="coerce")
        sort_cols.append("_sort_primary_edge")
        ascending.append(False)

    if "fixture_id" in out.columns:
        sort_cols.append("fixture_id")
        ascending.append(True)

    if sort_cols:
        out = out.sort_values(sort_cols, ascending=ascending, na_position="last")

    return out.drop(
        columns=[
            "_sort_shortlist_rank",
            "_sort_selection_score",
            "_sort_primary_edge",
        ],
        errors="ignore",
    ).reset_index(drop=True)


def summarize_group(df: pd.DataFrame, group_cols: list[str], summary_scope: str) -> pd.DataFrame:
    working = df.copy()
    for col in group_cols:
        if col not in working.columns:
            working[col] = ""

    rows = []
    groupby_cols = group_cols if group_cols else ["_all"]
    if not group_cols:
        working["_all"] = "ALL"

    for keys, subset in working.groupby(groupby_cols, dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)

        row = {
            "summary_scope": summary_scope,
            "rows_total": int(len(subset)),
            "base_actionable_rows": int(
                subset.get("base_final_recommendation", pd.Series(index=subset.index, dtype=object))
                .map(is_actionable_recommendation)
                .sum()
            ),
            "final_actionable_rows": int(
                subset["final_recommendation"].map(is_actionable_recommendation).sum()
            )
            if "final_recommendation" in subset.columns
            else 0,
            "bet_rows": int((subset.get("final_recommendation", "") == "BET").sum())
            if "final_recommendation" in subset.columns
            else 0,
            "lean_play_rows": int((subset.get("final_recommendation", "") == "LEAN_PLAY").sum())
            if "final_recommendation" in subset.columns
            else 0,
        }
        for col, key in zip(groupby_cols, keys):
            if col != "_all":
                row[col] = key

        if "selection_score" in subset.columns:
            row["avg_selection_score"] = round(
                pd.to_numeric(subset["selection_score"], errors="coerce").mean(),
                4,
            )
        else:
            row["avg_selection_score"] = pd.NA

        if "primary_edge" in subset.columns:
            row["avg_primary_edge"] = round(
                pd.to_numeric(subset["primary_edge"], errors="coerce").mean(),
                6,
            )
        else:
            row["avg_primary_edge"] = pd.NA

        for metric in [
            "production_governance_rule_count",
            "production_governance_premium_rule_count",
            "production_governance_standard_rule_count",
            "production_governance_generic_rule_count",
        ]:
            if metric in subset.columns:
                row[f"avg_{metric}"] = round(
                    pd.to_numeric(subset[metric], errors="coerce").mean(),
                    4,
                )
            else:
                row[f"avg_{metric}"] = pd.NA

        rows.append(row)

    if not group_cols:
        working = working.drop(columns=["_all"], errors="ignore")

    return pd.DataFrame(rows)


def build_governance_summary(df: pd.DataFrame) -> pd.DataFrame:
    parts = [
        summarize_group(df, [], "overall"),
        summarize_group(df, ["final_execution_bucket"], "by_final_execution_bucket"),
        summarize_group(
            df,
            ["final_execution_bucket", "production_governance_status"],
            "by_bucket_and_governance_status",
        ),
        summarize_group(
            df,
            ["final_execution_bucket", "final_recommendation"],
            "by_bucket_and_final_recommendation",
        ),
        summarize_group(
            df,
            ["final_execution_bucket", "execution_verdict"],
            "by_bucket_and_execution_verdict",
        ),
        summarize_group(
            df,
            ["final_execution_bucket", "production_governance_best_evidence_tier"],
            "by_bucket_and_best_evidence_tier",
        ),
    ]
    summary = pd.concat(parts, ignore_index=True, sort=False)

    display_cols = [
        "summary_scope",
        "final_execution_bucket",
        "production_governance_status",
        "final_recommendation",
        "execution_verdict",
        "production_governance_best_evidence_tier",
        "rows_total",
        "base_actionable_rows",
        "final_actionable_rows",
        "bet_rows",
        "lean_play_rows",
        "avg_selection_score",
        "avg_primary_edge",
        "avg_production_governance_rule_count",
        "avg_production_governance_premium_rule_count",
        "avg_production_governance_standard_rule_count",
        "avg_production_governance_generic_rule_count",
    ]
    existing = [col for col in display_cols if col in summary.columns]
    return summary[existing]


def load_source_candidates(source_csv: Path) -> pd.DataFrame:
    """Load the deep candidates CSV, returning an empty frame when the file is
    absent or has no rows (legitimate NO_BET day with zero candidates)."""
    if not source_csv.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(source_csv)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def build_no_bet_summary() -> pd.DataFrame:
    """Coherent governance summary for a zero-candidate NO_BET day: exactly one
    'overall' row with rows_total == 0."""
    row = {
        "summary_scope": "overall",
        "final_execution_bucket": pd.NA,
        "production_governance_status": pd.NA,
        "final_recommendation": "NO_BET",
        "execution_verdict": "NO_BET",
        "production_governance_best_evidence_tier": pd.NA,
        "rows_total": 0,
        "base_actionable_rows": 0,
        "final_actionable_rows": 0,
        "bet_rows": 0,
        "lean_play_rows": 0,
        "avg_selection_score": pd.NA,
        "avg_primary_edge": pd.NA,
        "avg_production_governance_rule_count": pd.NA,
        "avg_production_governance_premium_rule_count": pd.NA,
        "avg_production_governance_standard_rule_count": pd.NA,
        "avg_production_governance_generic_rule_count": pd.NA,
    }
    return pd.DataFrame([row])


def generate_empty_no_bet_exports(
    output_dir: Path,
) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame]:
    """Write the full set of empty execution exports plus a NO_BET governance
    summary, so downstream validation and the pipeline succeed with exit 0 on a
    zero-candidate day.

    The empty exports are derived through the exact same code path as a normal
    day: a 0-row frame carrying the full deep-analysis schema is run through
    add_final_execution_buckets, so every export carries the identical column
    set (header) it would on a real day, only with 0 rows."""
    output_dir.mkdir(parents=True, exist_ok=True)

    exported = add_final_execution_buckets(pd.DataFrame(columns=DEEP_ANALYSIS_OUTPUT_COLUMNS))

    paths: dict[str, Path] = {}
    for bucket, filename in OUTPUT_FILENAMES.items():
        bucket_path = output_dir / filename
        exported[exported["final_execution_bucket"] == bucket].to_csv(bucket_path, index=False)
        paths[bucket] = bucket_path

    approved_path = output_dir / APPROVED_CSV
    exported[
        exported["final_execution_bucket"].isin({"APPROVED_PREMIUM", "APPROVED_STANDARD"})
    ].to_csv(approved_path, index=False)
    paths["APPROVED"] = approved_path

    summary = build_no_bet_summary()
    summary_path = output_dir / SUMMARY_CSV
    summary.to_csv(summary_path, index=False)
    paths["SUMMARY"] = summary_path

    return paths, exported, summary


def generate_final_execution_exports(
    source_csv: Path = DEFAULT_SOURCE_CSV,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame]:
    source = load_source_candidates(source_csv)
    if source.empty:
        return generate_empty_no_bet_exports(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    exported = add_final_execution_buckets(source)

    paths: dict[str, Path] = {}
    for bucket, filename in OUTPUT_FILENAMES.items():
        bucket_path = output_dir / filename
        exported[exported["final_execution_bucket"] == bucket].to_csv(bucket_path, index=False)
        paths[bucket] = bucket_path

    approved_path = output_dir / APPROVED_CSV
    exported[
        exported["final_execution_bucket"].isin({"APPROVED_PREMIUM", "APPROVED_STANDARD"})
    ].to_csv(approved_path, index=False)
    paths["APPROVED"] = approved_path

    summary = build_governance_summary(exported)
    summary_path = output_dir / SUMMARY_CSV
    summary.to_csv(summary_path, index=False)
    paths["SUMMARY"] = summary_path

    return paths, exported, summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create final execution-ready vSIGMA exports from governed deep candidates."
    )
    parser.add_argument(
        "--source-csv",
        default=str(DEFAULT_SOURCE_CSV),
        help="Governed deep analysis candidates CSV.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where final execution exports will be written.",
    )
    args = parser.parse_args()

    paths, exported, summary = generate_final_execution_exports(
        source_csv=Path(args.source_csv),
        output_dir=Path(args.output_dir),
    )

    print("\n=== FINAL EXECUTION EXPORTS COMPLETADO ===")
    if exported.empty:
        print("DAY_STATUS: NO_BET (0 candidatos; exports vacios generados)")
    for key in [
        "APPROVED_PREMIUM",
        "APPROVED_STANDARD",
        "APPROVED",
        "DOWNGRADED",
        "BLOCKED",
        "WATCH",
        "SUMMARY",
    ]:
        print(f"{key}: {paths[key]}")

    print("\nBucket counts:")
    counts = exported["final_execution_bucket"].value_counts().reindex(BUCKET_ORDER.keys(), fill_value=0)
    for bucket, count in counts.items():
        print(f"{bucket}: {int(count)}")

    print("\nGovernance summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
