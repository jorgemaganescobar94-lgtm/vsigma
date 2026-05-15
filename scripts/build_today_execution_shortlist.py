from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd

try:
    from pick_explanations import add_pick_explanations, write_pick_explanation_outputs
except ModuleNotFoundError:
    from scripts.pick_explanations import add_pick_explanations, write_pick_explanation_outputs


DEFAULT_PROCESSED_DIR = Path("data/processed")

PREMIUM_INPUT = "vsigma_final_approved_premium_candidates.csv"
STANDARD_INPUT = "vsigma_final_approved_standard_candidates.csv"

PREMIUM_CORE_OUTPUT = "vsigma_today_premium_core.csv"
EXECUTION_SHORTLIST_OUTPUT = "vsigma_today_execution_shortlist.csv"
BETS_ONLY_OUTPUT = "vsigma_today_execution_bets_only.csv"
SUMMARY_OUTPUT = "vsigma_today_execution_summary.csv"
PICK_EXPLANATIONS_OUTPUT = "vsigma_today_pick_explanations.csv"
PICK_EXPLANATIONS_REPORT = "vsigma_today_pick_explanations_report.txt"

ACTIONABLE_RECOMMENDATIONS = {"BET", "LEAN_PLAY"}
CORE_VERDICTS = {"TOP_CORE", "CORE_SHORTLIST"}
BLOCKED_MARKET_FIT_STATUSES = {"MARKET_FIT_DOWNGRADED", "MARKET_FIT_BLOCKED"}
PREMIUM_EXTENDED_ALLOWED_MARKETS = {"OVER_1_5", "OVER_2_5", "UNDER_3_5"}
PREMIUM_EXTENDED_MIN_EDGE = 0.08
PREMIUM_EXTENDED_MIN_MODEL_PROB = 0.82
MAX_FINAL_ROWS = 8
MAX_PER_LEAGUE = 2
MAX_PER_MARKET = 2
MAX_PER_FIXTURE = 1

REQUIRED_COLUMNS = [
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

SORT_COLUMNS = [
    "execution_score",
    "selection_score",
    "primary_edge",
    "primary_model_prob",
    "shortlist_rank",
]
SORT_ASCENDING = [False, False, False, False, True]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def read_csv_required(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing execution-shortlist input: {path}")
    return pd.read_csv(path)


def require_columns(df: pd.DataFrame, label: str) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def normalize_inputs(df: pd.DataFrame, expected_bucket: str, label: str) -> pd.DataFrame:
    require_columns(df, label)
    out = df.copy()
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
    out["_source_row_id"] = range(len(out))
    return out


def add_execution_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    premium_bonus = out["_final_execution_bucket_norm"].map(
        {"APPROVED_PREMIUM": 8.0, "APPROVED_STANDARD": 3.0}
    ).fillna(0.0)
    bet_bonus = out["_final_recommendation_norm"].eq("BET").astype(float) * 5.0
    base_core_bonus = out["_base_execution_verdict_norm"].isin(CORE_VERDICTS).astype(float) * 6.0
    watch_penalty = out["_base_execution_verdict_norm"].eq("WATCH").astype(float) * 8.0

    out["execution_score"] = (
        out["selection_score"].fillna(0.0)
        + (out["primary_edge"].fillna(0.0) * 100.0)
        + premium_bonus
        + bet_bonus
        + base_core_bonus
        - watch_penalty
    )
    return out


def sort_execution_candidates(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    return df.sort_values(
        SORT_COLUMNS,
        ascending=SORT_ASCENDING,
        na_position="last",
        kind="mergesort",
    ).reset_index(drop=True)


def premium_core_mask(df: pd.DataFrame) -> pd.Series:
    market_fit_ok = (
        ~df["execution_market_fit_status"].map(norm_text).isin(BLOCKED_MARKET_FIT_STATUSES)
        if "execution_market_fit_status" in df.columns
        else pd.Series(True, index=df.index)
    )
    return (
        df["_final_execution_bucket_norm"].eq("APPROVED_PREMIUM")
        & df["_final_recommendation_norm"].eq("BET")
        & df["_base_execution_verdict_norm"].isin(CORE_VERDICTS)
        & df["primary_edge"].gt(0)
        & df["primary_odds_used"].notna()
        & market_fit_ok
    )


def premium_extended_mask(df: pd.DataFrame) -> pd.Series:
    if "premium_extended_governance_status" not in df.columns:
        df = add_premium_extended_governance(df)
    return df["premium_extended_governance_status"].eq("EXTENDED_QUALITY_OK")


def has_premium_evidence(row: pd.Series) -> bool:
    status = norm_text(row.get("production_governance_status"))
    if status and status != "APPROVED_BY_PREMIUM_PROMOTED_RULE":
        return False

    best_tier = norm_text(row.get("production_governance_best_evidence_tier"))
    if best_tier and best_tier != "PREMIUM_EVIDENCE":
        return False

    if "production_governance_premium_rule_count" in row.index:
        premium_count = pd.to_numeric(
            pd.Series([row.get("production_governance_premium_rule_count")]),
            errors="coerce",
        ).iloc[0]
        if pd.notna(premium_count) and premium_count < 1:
            return False

    return True


def official_coverage_loaded(row: pd.Series) -> bool:
    return norm_text(row.get("league_coverage_source_status")).startswith("OFFICIAL_API")


def thin_league_coverage(row: pd.Series) -> bool:
    return official_coverage_loaded(row) and norm_text(row.get("league_coverage_class")) in {
        "COVERAGE_THIN",
        "COVERAGE_MINIMAL",
    }


def classify_premium_extended_governance(row: pd.Series) -> tuple[str, str]:
    if norm_text(row.get("final_execution_bucket")) != "APPROVED_PREMIUM":
        return "EXTENDED_NOT_PREMIUM", "Candidate is not in the approved premium bucket."

    if norm_text(row.get("base_execution_verdict")) in CORE_VERDICTS and norm_text(row.get("final_recommendation")) == "BET":
        return "PREMIUM_CORE_PROTECTED", "Premium core architecture is preserved; extended governance is not applied."

    market_fit_status = norm_text(row.get("execution_market_fit_status"))
    if market_fit_status in BLOCKED_MARKET_FIT_STATUSES:
        return "EXTENDED_MARKET_FIT_WEAK", f"Market-fit status is {market_fit_status}."

    if norm_text(row.get("final_recommendation")) != "BET":
        return "EXTENDED_DOWNGRADED_TO_WATCH", "Premium extended requires a BET recommendation, not a lean."

    if not has_premium_evidence(row):
        return "EXTENDED_EVIDENCE_TOO_GENERIC", "Premium extended requires explicit premium promoted-rule evidence."

    market = norm_text(row.get("market_primary"))
    if market not in PREMIUM_EXTENDED_ALLOWED_MARKETS:
        return "EXTENDED_MARKET_FIT_WEAK", f"Premium extended only admits robust total markets; got {market or 'UNKNOWN'}."

    edge = pd.to_numeric(pd.Series([row.get("primary_edge")]), errors="coerce").iloc[0]
    if pd.isna(edge) or edge < PREMIUM_EXTENDED_MIN_EDGE:
        return (
            "EXTENDED_EDGE_TOO_THIN",
            f"Primary edge must be at least {PREMIUM_EXTENDED_MIN_EDGE:.2f} for premium extended.",
        )

    model_prob = pd.to_numeric(pd.Series([row.get("primary_model_prob")]), errors="coerce").iloc[0]
    if pd.isna(model_prob) or model_prob < PREMIUM_EXTENDED_MIN_MODEL_PROB:
        return (
            "EXTENDED_STRUCTURE_TOO_THIN",
            f"Primary model probability must be at least {PREMIUM_EXTENDED_MIN_MODEL_PROB:.2f}.",
        )

    if thin_league_coverage(row) and (edge < 0.12 or model_prob < 0.86):
        return (
            "EXTENDED_COVERAGE_TOO_THIN",
            "Thin official league coverage requires stronger edge/probability for premium extended execution.",
        )

    odds = pd.to_numeric(pd.Series([row.get("primary_odds_used")]), errors="coerce").iloc[0]
    if pd.isna(odds) or odds <= 1.0:
        return "EXTENDED_STRUCTURE_TOO_THIN", "Premium extended requires usable primary odds."

    return "EXTENDED_QUALITY_OK", "Premium extended passed stricter edge, probability, evidence, and market-fit gates."


def add_premium_extended_governance(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    classifications = out.apply(classify_premium_extended_governance, axis=1)
    out["premium_extended_governance_status"] = [status for status, _ in classifications]
    out["premium_extended_governance_reason"] = [reason for _, reason in classifications]
    return out


def standard_fill_mask(df: pd.DataFrame) -> pd.Series:
    market_fit_ok = (
        ~df["execution_market_fit_status"].map(norm_text).isin(BLOCKED_MARKET_FIT_STATUSES)
        if "execution_market_fit_status" in df.columns
        else pd.Series(True, index=df.index)
    )
    return (
        df["_final_execution_bucket_norm"].eq("APPROVED_STANDARD")
        & df["_final_recommendation_norm"].isin(ACTIONABLE_RECOMMENDATIONS)
        & df["primary_edge"].gt(0)
        & df["primary_odds_used"].notna()
        & market_fit_ok
    )


def cap_key(value: object) -> object:
    if pd.isna(value):
        return "__MISSING__"
    return value


def apply_caps_by_phase(phases: Iterable[tuple[str, pd.DataFrame]]) -> pd.DataFrame:
    selected: list[pd.Series] = []
    league_counts: dict[object, int] = {}
    market_counts: dict[object, int] = {}
    fixture_counts: dict[object, int] = {}

    for phase_name, phase in phases:
        if len(selected) >= MAX_FINAL_ROWS:
            break
        for _, row in sort_execution_candidates(phase).iterrows():
            if len(selected) >= MAX_FINAL_ROWS:
                break

            league = cap_key(row.get("league"))
            market = cap_key(row.get("market_primary"))
            fixture = cap_key(row.get("fixture_id"))

            if league_counts.get(league, 0) >= MAX_PER_LEAGUE:
                continue
            if market_counts.get(market, 0) >= MAX_PER_MARKET:
                continue
            if fixture_counts.get(fixture, 0) >= MAX_PER_FIXTURE:
                continue

            selected_row = row.copy()
            selected_row["execution_shortlist_source"] = phase_name
            selected.append(selected_row)
            league_counts[league] = league_counts.get(league, 0) + 1
            market_counts[market] = market_counts.get(market, 0) + 1
            fixture_counts[fixture] = fixture_counts.get(fixture, 0) + 1

    if not selected:
        return pd.DataFrame()

    out = pd.DataFrame(selected)
    out = sort_execution_candidates(out)
    out.insert(0, "execution_rank", range(1, len(out) + 1))
    return out.reset_index(drop=True)


def summarize_counts(
    premium_core: pd.DataFrame,
    premium_extended: pd.DataFrame,
    standard_fill: pd.DataFrame,
    shortlist: pd.DataFrame,
    bets_only: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = [
        {
            "summary_scope": "eligibility",
            "metric": "premium_core_rows",
            "rows_total": int(len(premium_core)),
        },
        {
            "summary_scope": "eligibility",
            "metric": "premium_extended_eligible_rows",
            "rows_total": int(len(premium_extended)),
        },
        {
            "summary_scope": "eligibility",
            "metric": "standard_eligible_rows",
            "rows_total": int(len(standard_fill)),
        },
        {
            "summary_scope": "final",
            "metric": "final_shortlist_rows",
            "rows_total": int(len(shortlist)),
        },
        {
            "summary_scope": "final",
            "metric": "bets_only_rows",
            "rows_total": int(len(bets_only)),
        },
    ]

    group_specs = [
        ("by_final_execution_bucket", "final_execution_bucket"),
        ("by_final_recommendation", "final_recommendation"),
        ("by_league", "league"),
        ("by_market_primary", "market_primary"),
    ]
    for scope, col in group_specs:
        if shortlist.empty or col not in shortlist.columns:
            continue
        grouped = shortlist.groupby(col, dropna=False, sort=True).size().reset_index(name="rows_total")
        for _, row in grouped.iterrows():
            rows.append(
                {
                    "summary_scope": scope,
                    col: row[col],
                    "rows_total": int(row["rows_total"]),
                }
            )

    return pd.DataFrame(rows)


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


def build_today_execution_shortlist(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    premium = normalize_inputs(
        read_csv_required(processed_dir / PREMIUM_INPUT),
        "APPROVED_PREMIUM",
        PREMIUM_INPUT,
    )
    standard = normalize_inputs(
        read_csv_required(processed_dir / STANDARD_INPUT),
        "APPROVED_STANDARD",
        STANDARD_INPUT,
    )

    premium = add_execution_score(premium)
    standard = add_execution_score(standard)
    premium = add_premium_extended_governance(premium)

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
    if shortlist.empty and "final_recommendation" not in shortlist.columns:
        shortlist = pd.DataFrame(columns=[*premium.columns, "execution_shortlist_source", "execution_rank"])
    premium_core = add_pick_explanations(premium_core)
    shortlist = add_pick_explanations(shortlist)
    bets_only = shortlist[shortlist["final_recommendation"].map(norm_text).eq("BET")].copy()
    summary = summarize_counts(premium_core, premium_extended, standard_fill, shortlist, bets_only)

    processed_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "PREMIUM_CORE": processed_dir / PREMIUM_CORE_OUTPUT,
        "EXECUTION_SHORTLIST": processed_dir / EXECUTION_SHORTLIST_OUTPUT,
        "BETS_ONLY": processed_dir / BETS_ONLY_OUTPUT,
        "SUMMARY": processed_dir / SUMMARY_OUTPUT,
        "PICK_EXPLANATIONS": processed_dir / PICK_EXPLANATIONS_OUTPUT,
        "PICK_EXPLANATIONS_REPORT": processed_dir / PICK_EXPLANATIONS_REPORT,
    }

    strip_internal_columns(premium_core).to_csv(paths["PREMIUM_CORE"], index=False)
    strip_internal_columns(shortlist).to_csv(paths["EXECUTION_SHORTLIST"], index=False)
    strip_internal_columns(bets_only).to_csv(paths["BETS_ONLY"], index=False)
    summary.to_csv(paths["SUMMARY"], index=False)
    explanation_csv, explanation_report = write_pick_explanation_outputs(
        strip_internal_columns(shortlist),
        processed_dir,
    )
    paths["PICK_EXPLANATIONS"] = explanation_csv
    paths["PICK_EXPLANATIONS_REPORT"] = explanation_report

    return (
        paths,
        strip_internal_columns(premium_core),
        strip_internal_columns(shortlist),
        strip_internal_columns(bets_only),
        summary,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build today's execution-ready vSIGMA shortlist from final approved candidates."
    )
    parser.add_argument(
        "--processed-dir",
        default=str(DEFAULT_PROCESSED_DIR),
        help="Directory containing final approved candidate exports.",
    )
    args = parser.parse_args()

    paths, premium_core, shortlist, bets_only, summary = build_today_execution_shortlist(
        Path(args.processed_dir)
    )

    print("\n=== TODAY EXECUTION SHORTLIST COMPLETADO ===")
    for key, path in paths.items():
        print(f"{key}: {path}")

    print("\nCounts:")
    print(f"Premium core: {len(premium_core)}")
    print(f"Final shortlist: {len(shortlist)}")
    print(f"Bets only: {len(bets_only)}")
    if not shortlist.empty:
        display_cols = [
            col
            for col in [
                "execution_rank",
                "fixture_id",
                "league",
                "home_team",
                "away_team",
                "market_primary",
                "final_execution_bucket",
                "final_recommendation",
                "execution_score",
                "primary_edge",
            ]
            if col in shortlist.columns
        ]
        print("\nTop shortlist rows:")
        print(shortlist[display_cols].head(8).to_string(index=False))

    print("\nSummary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
