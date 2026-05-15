from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd

try:
    from pick_explanations import add_pick_explanations
except ModuleNotFoundError:
    from scripts.pick_explanations import add_pick_explanations


DEFAULT_PROCESSED_DIR = Path("data/processed")

SHORTLIST_INPUT = "vsigma_today_execution_shortlist.csv"
BETS_ONLY_INPUT = "vsigma_today_execution_bets_only.csv"
PREMIUM_CORE_INPUT = "vsigma_today_premium_core.csv"

SAFE_OUTPUT = "vsigma_today_safe_top5.csv"
BALANCED_OUTPUT = "vsigma_today_balanced_top5.csv"
AGGRESSIVE_OUTPUT = "vsigma_today_aggressive_top5.csv"
SUMMARY_OUTPUT = "vsigma_today_pick_modes_summary.csv"

ACTIONABLE_RECOMMENDATIONS = {"BET", "LEAN_PLAY"}
BLOCKED_MARKET_FIT_STATUSES = {"MARKET_FIT_DOWNGRADED", "MARKET_FIT_BLOCKED"}
MAX_SAFE_ROWS = 5

REQUIRED_COLUMNS = [
    "execution_rank",
    "execution_score",
    "execution_shortlist_source",
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
    "confidence_band",
    "home_team",
    "away_team",
]

MARKET_SAFETY_BONUS = {
    "OVER_1_5": 6.0,
    "UNDER_3_5": 5.0,
    "HOME_DNB": 4.0,
    "AWAY_DNB": 4.0,
    "OVER_2_5": 1.0,
    "HOME_WIN": 0.0,
    "AWAY_WIN": 0.0,
    "BTTS_YES": -1.0,
}
MARKET_BALANCE_BONUS = {
    "OVER_1_5": 4.0,
    "UNDER_3_5": 4.0,
    "OVER_2_5": 3.0,
    "HOME_DNB": 3.0,
    "AWAY_DNB": 3.0,
    "HOME_WIN": 2.0,
    "AWAY_WIN": 2.0,
    "BTTS_YES": 1.0,
}
MARKET_AGGRESSIVE_BONUS = {
    "AWAY_WIN": 4.0,
    "HOME_WIN": 4.0,
    "OVER_2_5": 4.0,
    "BTTS_YES": 3.0,
    "OVER_1_5": 1.0,
    "UNDER_3_5": 0.0,
    "HOME_DNB": 1.0,
    "AWAY_DNB": 1.0,
}


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def read_csv_required(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing pick-mode input: {path}")
    return pd.read_csv(path)


def require_columns(df: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def odds_safety_bonus(odds: object) -> float:
    value = pd.to_numeric(pd.Series([odds]), errors="coerce").iloc[0]
    if pd.isna(value):
        return 0.0
    if value <= 1.30:
        return 2.0
    if value <= 1.65:
        return 5.0
    if value <= 1.95:
        return 3.0
    if value <= 2.25:
        return 0.0
    return -4.0


def bucket_bonus(bucket: object) -> float:
    return {"APPROVED_PREMIUM": 6.0, "APPROVED_STANDARD": 2.0}.get(norm_text(bucket), 0.0)


def recommendation_bonus(recommendation: object) -> float:
    return 4.0 if norm_text(recommendation) == "BET" else 0.0


def verdict_bonus(verdict: object) -> float:
    return {"TOP_CORE": 6.0, "CORE_SHORTLIST": 4.0, "WATCH": -3.0}.get(norm_text(verdict), 0.0)


def confidence_bonus(confidence: object) -> float:
    return {"HIGH": 4.0, "MEDIUM_HIGH": 2.0}.get(norm_text(confidence), 0.0)


def source_priority(row: pd.Series) -> int:
    if norm_text(row.get("execution_shortlist_source")) == "PREMIUM_CORE":
        return 1
    if norm_text(row.get("final_execution_bucket")) == "APPROVED_PREMIUM":
        return 2
    if norm_text(row.get("final_execution_bucket")) == "APPROVED_STANDARD":
        return 3
    return 9


def mode_entry_reason(row: pd.Series, mode: str) -> str:
    source = norm_text(row.get("execution_shortlist_source"))
    bucket = norm_text(row.get("final_execution_bucket"))
    rec = norm_text(row.get("final_recommendation"))
    confidence = norm_text(row.get("confidence_band"))
    edge = pd.to_numeric(pd.Series([row.get("primary_edge")]), errors="coerce").iloc[0]

    if mode == "AGGRESSIVE_TOP5" and pd.notna(edge) and edge >= 0.20:
        return "AGGRESSIVE_HIGH_EDGE_UPSIDE"
    if source == "PREMIUM_CORE" and rec == "BET" and confidence == "HIGH":
        return "PREMIUM_CORE_BET_HIGH_SAFETY"
    if bucket == "APPROVED_PREMIUM" and rec == "BET" and pd.notna(edge) and edge >= 0.10:
        return "PREMIUM_BET_STRONG_EDGE"
    if source == "STANDARD_FILL" and rec == "BET":
        return "STANDARD_FILL_BET"
    if rec == "LEAN_PLAY":
        return "LEAN_PLAY_FILL"
    return f"{bucket or 'UNKNOWN'}_{rec or 'UNKNOWN'}"


def normalize_and_score(df: pd.DataFrame) -> pd.DataFrame:
    require_columns(df, REQUIRED_COLUMNS, SHORTLIST_INPUT)
    out = df.copy()
    for col in [
        "execution_rank",
        "execution_score",
        "selection_score",
        "primary_model_prob",
        "primary_odds_used",
        "primary_edge",
    ]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    actionable = out["final_recommendation"].map(norm_text).isin(ACTIONABLE_RECOMMENDATIONS)
    market_fit_ok = (
        ~out["execution_market_fit_status"].map(norm_text).isin(BLOCKED_MARKET_FIT_STATUSES)
        if "execution_market_fit_status" in out.columns
        else pd.Series(True, index=out.index)
    )
    out = out[
        out["primary_edge"].gt(0)
        & out["primary_odds_used"].notna()
        & actionable
        & market_fit_ok
    ].copy()

    b_bonus = out["final_execution_bucket"].map(bucket_bonus)
    r_bonus = out["final_recommendation"].map(recommendation_bonus)
    v_bonus = out["base_execution_verdict"].map(verdict_bonus)
    c_bonus = out["confidence_band"].map(confidence_bonus)
    market = out["market_primary"].map(norm_text)

    out["safe_score"] = (
        out["execution_score"].fillna(0.0)
        + b_bonus
        + r_bonus
        + v_bonus
        + c_bonus
        + market.map(MARKET_SAFETY_BONUS).fillna(0.0)
        + out["primary_odds_used"].map(odds_safety_bonus)
        + out["primary_edge"].clip(upper=0.25).fillna(0.0) * 40.0
        + out["primary_model_prob"].clip(upper=0.90).fillna(0.0) * 10.0
    )
    out["balanced_score"] = (
        out["execution_score"].fillna(0.0)
        + b_bonus
        + r_bonus
        + v_bonus
        + c_bonus
        + market.map(MARKET_BALANCE_BONUS).fillna(0.0)
        + out["primary_edge"].clip(upper=0.30).fillna(0.0) * 60.0
        + out["primary_model_prob"].fillna(0.0) * 10.0
    )
    out["aggressive_score"] = (
        out["execution_score"].fillna(0.0)
        + b_bonus
        + r_bonus
        + v_bonus
        + market.map(MARKET_AGGRESSIVE_BONUS).fillna(0.0)
        + out["primary_edge"].fillna(0.0) * 120.0
        + (out["primary_odds_used"].fillna(0.0) - 1.60).clip(lower=0.0) * 8.0
    )
    out["mode_source_priority"] = out.apply(source_priority, axis=1)
    return out


def cap_key(value: object) -> object:
    if pd.isna(value):
        return "__MISSING__"
    return value


def select_with_caps(
    df: pd.DataFrame,
    mode: str,
    sort_cols: list[str],
    ascending: list[bool],
    max_per_league: int,
    max_per_market: int,
    max_total: int = 5,
    initial_selected: list[pd.Series] | None = None,
) -> pd.DataFrame:
    selected: list[pd.Series] = []
    league_counts: dict[object, int] = {}
    market_counts: dict[object, int] = {}
    fixture_counts: dict[object, int] = {}

    for initial in initial_selected or []:
        initial_row = initial.copy()
        initial_row["pick_mode"] = mode
        if "mode_entry_reason" not in initial_row or pd.isna(initial_row.get("mode_entry_reason")):
            initial_row["mode_entry_reason"] = mode_entry_reason(initial_row, mode)
        selected.append(initial_row)
        league = cap_key(initial_row.get("league"))
        market = cap_key(initial_row.get("market_primary"))
        fixture = cap_key(initial_row.get("fixture_id"))
        league_counts[league] = league_counts.get(league, 0) + 1
        market_counts[market] = market_counts.get(market, 0) + 1
        fixture_counts[fixture] = fixture_counts.get(fixture, 0) + 1

    ordered = df.sort_values(sort_cols, ascending=ascending, na_position="last", kind="mergesort")
    for _, row in ordered.iterrows():
        if len(selected) >= max_total:
            break
        league = cap_key(row.get("league"))
        market = cap_key(row.get("market_primary"))
        fixture = cap_key(row.get("fixture_id"))
        if league_counts.get(league, 0) >= max_per_league:
            continue
        if market_counts.get(market, 0) >= max_per_market:
            continue
        if fixture_counts.get(fixture, 0) >= 1:
            continue

        selected_row = row.copy()
        selected_row["pick_mode"] = mode
        selected_row["mode_entry_reason"] = mode_entry_reason(selected_row, mode)
        selected.append(selected_row)
        league_counts[league] = league_counts.get(league, 0) + 1
        market_counts[market] = market_counts.get(market, 0) + 1
        fixture_counts[fixture] = fixture_counts.get(fixture, 0) + 1

    if not selected:
        return pd.DataFrame(columns=[*df.columns, "pick_mode", "mode_rank", "mode_entry_reason"])
    out = pd.DataFrame(selected).reset_index(drop=True)
    out.insert(0, "mode_rank", range(1, len(out) + 1))
    return out


def select_safe(df: pd.DataFrame) -> pd.DataFrame:
    bets = df[df["final_recommendation"].map(norm_text).eq("BET")].copy()
    return select_with_caps(
        bets,
        "SAFE_TOP5",
        [
            "mode_source_priority",
            "safe_score",
            "selection_score",
            "primary_edge",
            "primary_model_prob",
            "execution_rank",
        ],
        [True, False, False, False, False, True],
        max_per_league=1,
        max_per_market=1,
    )


def select_bet_then_lean(
    df: pd.DataFrame,
    mode: str,
    sort_cols: list[str],
    ascending: list[bool],
    max_per_league: int,
    max_per_market: int,
) -> pd.DataFrame:
    bets = df[df["final_recommendation"].map(norm_text).eq("BET")].copy()
    selected = select_with_caps(
        bets,
        mode,
        sort_cols,
        ascending,
        max_per_league=max_per_league,
        max_per_market=max_per_market,
    )
    if len(selected) >= 5:
        return selected

    initial_rows = [
        row
        for _, row in selected.drop(columns=["mode_rank"], errors="ignore").iterrows()
    ]
    used = set(selected["fixture_id"].tolist()) if "fixture_id" in selected.columns else set()
    leans = df[
        df["final_recommendation"].map(norm_text).eq("LEAN_PLAY")
        & ~df["fixture_id"].isin(used)
    ].copy()
    return select_with_caps(
        leans,
        mode,
        sort_cols,
        ascending,
        max_per_league=max_per_league,
        max_per_market=max_per_market,
        initial_selected=initial_rows,
    )


def select_balanced(df: pd.DataFrame) -> pd.DataFrame:
    return select_bet_then_lean(
        df,
        "BALANCED_TOP5",
        ["balanced_score", "selection_score", "primary_edge", "primary_model_prob", "execution_rank"],
        [False, False, False, False, True],
        max_per_league=2,
        max_per_market=2,
    )


def select_aggressive(df: pd.DataFrame) -> pd.DataFrame:
    return select_bet_then_lean(
        df,
        "AGGRESSIVE_TOP5",
        ["aggressive_score", "primary_edge", "primary_odds_used", "selection_score", "execution_rank"],
        [False, False, False, False, True],
        max_per_league=2,
        max_per_market=2,
    )


def summarize_mode(mode_df: pd.DataFrame, summary_scope: str) -> list[dict[str, object]]:
    rows = [
        {
            "summary_scope": summary_scope,
            "pick_mode": summary_scope,
            "metric": "rows_total",
            "rows_total": int(len(mode_df)),
        }
    ]
    for scope, col in [
        ("by_final_execution_bucket", "final_execution_bucket"),
        ("by_final_recommendation", "final_recommendation"),
        ("by_league", "league"),
        ("by_market_primary", "market_primary"),
    ]:
        if mode_df.empty or col not in mode_df.columns:
            continue
        grouped = mode_df.groupby(col, dropna=False, sort=True).size().reset_index(name="rows_total")
        for _, row in grouped.iterrows():
            rows.append(
                {
                    "summary_scope": scope,
                    "pick_mode": summary_scope,
                    "metric": col,
                    col: row[col],
                    "rows_total": int(row["rows_total"]),
                }
            )
    return rows


def build_summary(
    available: pd.DataFrame,
    bets_only: pd.DataFrame,
    safe: pd.DataFrame,
    balanced: pd.DataFrame,
    aggressive: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = [
        {
            "summary_scope": "input",
            "pick_mode": "ALL",
            "metric": "input_shortlist_rows",
            "rows_total": int(len(available)),
        },
        {
            "summary_scope": "input",
            "pick_mode": "ALL",
            "metric": "bets_only_rows",
            "rows_total": int(len(bets_only)),
        },
        {
            "summary_scope": "mode",
            "pick_mode": "SAFE_TOP5",
            "metric": "safe_top5_rows",
            "rows_total": int(len(safe)),
        },
        {
            "summary_scope": "mode",
            "pick_mode": "BALANCED_TOP5",
            "metric": "balanced_top5_rows",
            "rows_total": int(len(balanced)),
        },
        {
            "summary_scope": "mode",
            "pick_mode": "AGGRESSIVE_TOP5",
            "metric": "aggressive_top5_rows",
            "rows_total": int(len(aggressive)),
        },
    ]
    rows.extend(summarize_mode(safe, "SAFE_TOP5"))
    rows.extend(summarize_mode(balanced, "BALANCED_TOP5"))
    rows.extend(summarize_mode(aggressive, "AGGRESSIVE_TOP5"))
    return pd.DataFrame(rows)


def build_execution_pick_modes(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    shortlist = read_csv_required(processed_dir / SHORTLIST_INPUT)
    bets_only = read_csv_required(processed_dir / BETS_ONLY_INPUT)
    read_csv_required(processed_dir / PREMIUM_CORE_INPUT)

    available = normalize_and_score(shortlist)
    available = add_pick_explanations(available)
    safe = add_pick_explanations(select_safe(available), "SAFE_TOP5")
    balanced = add_pick_explanations(select_balanced(available), "BALANCED_TOP5")
    aggressive = add_pick_explanations(select_aggressive(available), "AGGRESSIVE_TOP5")
    summary = build_summary(available, bets_only, safe, balanced, aggressive)

    paths = {
        "SAFE_TOP5": processed_dir / SAFE_OUTPUT,
        "BALANCED_TOP5": processed_dir / BALANCED_OUTPUT,
        "AGGRESSIVE_TOP5": processed_dir / AGGRESSIVE_OUTPUT,
        "SUMMARY": processed_dir / SUMMARY_OUTPUT,
    }
    processed_dir.mkdir(parents=True, exist_ok=True)
    safe.to_csv(paths["SAFE_TOP5"], index=False)
    balanced.to_csv(paths["BALANCED_TOP5"], index=False)
    aggressive.to_csv(paths["AGGRESSIVE_TOP5"], index=False)
    summary.to_csv(paths["SUMMARY"], index=False)
    return paths, safe, balanced, aggressive, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build today vSIGMA explicit pick modes.")
    parser.add_argument("--processed-dir", default=str(DEFAULT_PROCESSED_DIR))
    args = parser.parse_args()

    paths, safe, balanced, aggressive, summary = build_execution_pick_modes(Path(args.processed_dir))

    print("\n=== EXECUTION PICK MODES COMPLETADO ===")
    for key, path in paths.items():
        print(f"{key}: {path}")
    print(f"SAFE_TOP5 count: {len(safe)}")
    print(f"BALANCED_TOP5 count: {len(balanced)}")
    print(f"AGGRESSIVE_TOP5 count: {len(aggressive)}")

    for label, df in [("SAFE_TOP5", safe), ("BALANCED_TOP5", balanced), ("AGGRESSIVE_TOP5", aggressive)]:
        print(f"\n{label}:")
        cols = [
            col
            for col in [
                "mode_rank",
                "fixture_id",
                "league",
                "home_team",
                "away_team",
                "market_primary",
                "final_execution_bucket",
                "final_recommendation",
                "execution_shortlist_source",
                "safe_score",
                "balanced_score",
                "aggressive_score",
                "mode_entry_reason",
            ]
            if col in df.columns
        ]
        print(df[cols].to_string(index=False) if not df.empty else "No rows")


if __name__ == "__main__":
    main()
