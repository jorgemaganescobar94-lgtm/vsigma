from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd


DEFAULT_LABELED_CSV = Path("data/processed/vsigma_market_results_labeled.csv")
DEFAULT_DEEP_CSV = Path("data/processed/vsigma_deep_analysis_candidates.csv")
DEFAULT_OUTPUT_DIR = Path("data/processed")

GROUP_DIMENSIONS = [
    "market_primary",
    "edge_floor_band",
    "execution_verdict",
    "final_recommendation",
    "confidence_band",
    "shortlist_bucket",
    "analysis_label",
    "league",
]

BET_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}
NO_BET_VALUES = {
    "NO_BET",
    "PASS",
    "SKIP",
    "BLOCK",
    "BLOCKED",
    "HOLD",
    "WATCH",
    "WATCHLIST",
    "DATA_ONLY",
    "INFO_ONLY",
    "NO ACTION",
    "NO_ACTION",
    "NO BET",
}

ACTIONABLE_POSITIVE_HINTS = {
    "ACTIONABLE",
    "EXECUTE",
    "PLAY",
    "BET",
    "YES",
    "GO",
    "APPROVED",
    "ENTER",
    "ENTRY_OK",
}

ACTIONABLE_NEGATIVE_HINTS = {
    "NO_BET",
    "PASS",
    "SKIP",
    "BLOCK",
    "BLOCKED",
    "HOLD",
    "REJECT",
    "WATCH",
    "WATCHLIST",
    "DATA_ONLY",
    "INFO_ONLY",
    "NO ACTION",
    "NO_ACTION",
    "AVOID",
}

COLUMN_ALIASES: Dict[str, list[str]] = {
    "fixture_id": [
        "fixture_id", "fixture", "match_id", "event_id", "id_fixture", "api_fixture_id"
    ],
    "date": [
        "date", "match_date", "kickoff", "kickoff_time", "datetime", "event_date", "utc_date"
    ],
    "league": [
        "league", "competition", "league_name", "tournament", "comp", "league_label"
    ],
    "market_primary": [
        "market_primary", "primary_market", "recommended_market", "market", "bet_market"
    ],
    "edge_floor_band": [
        "edge_floor_band", "edge_band", "edge_floor", "edge_strength_band", "edge_label"
    ],
    "execution_verdict": [
        "execution_verdict", "execution_gate", "execution_status", "verdict", "entry_verdict"
    ],
    "final_recommendation": [
        "final_recommendation", "recommendation", "final_pick_status", "pick_status", "action_label"
    ],
    "confidence_band": [
        "confidence_band", "confidence", "confidence_label", "confidence_bucket"
    ],
    "shortlist_bucket": [
        "shortlist_bucket", "shortlist", "candidate_bucket", "core_bucket", "ranking_bucket"
    ],
    "analysis_label": [
        "analysis_label", "analysis_tag", "model_label", "candidate_label", "signal_label"
    ],
    "market_result": [
        "market_result", "actionable_result", "primary_result", "primary_market_result",
        "result_label", "graded_result", "bet_result", "market_outcome", "label_result"
    ],
    "odds": [
        "odds", "primary_odds_used", "market_odds", "bookmaker_odds", "price",
        "decimal_odds", "closing_odds"
    ],
    "units": [
        "units", "actionable_profit_units", "primary_profit_units", "profit_units",
        "pnl_units", "result_units", "units_result", "profit_u"
    ],
    "actionable_flag": [
        "actionable_flag", "is_actionable", "actionable", "bet_taken", "executed_flag"
    ],
    "model_edge_pct": [
        "model_edge_pct", "edge_pct", "edge_percent", "edge_percentage"
    ],
    "model_edge_abs": [
        "model_edge_abs", "primary_edge", "edge_abs", "edge_points", "edge_pp", "edge_value"
    ],
}


def norm_col_name(value: str) -> str:
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def norm_text(value) -> str:
    if pd.isna(value):
        return ""
    value = str(value).strip().upper()
    value = re.sub(r"\s+", "_", value)
    return value


def clean_blank_to_nan(series: pd.Series) -> pd.Series:
    return series.replace(r"^\s*$", np.nan, regex=True)


def to_bool(value) -> Optional[bool]:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value

    s = norm_text(value)
    if s in {"1", "TRUE", "YES", "Y", "SI", "S"}:
        return True
    if s in {"0", "FALSE", "NO", "N"}:
        return False
    return None


def resolve_column(df: pd.DataFrame, aliases: Iterable[str]) -> Optional[str]:
    normalized_map = {norm_col_name(col): col for col in df.columns}
    for alias in aliases:
        key = norm_col_name(alias)
        if key in normalized_map:
            return normalized_map[key]
    return None


def first_existing_column(df: pd.DataFrame, logical_name: str) -> Optional[str]:
    aliases = COLUMN_ALIASES.get(logical_name, [logical_name])
    return resolve_column(df, aliases)


def get_single_column(df: pd.DataFrame, col_name: str) -> Optional[pd.Series]:
    if col_name not in df.columns:
        return None

    payload = df.loc[:, df.columns == col_name]

    if isinstance(payload, pd.Series):
        return payload

    if payload.shape[1] == 1:
        return payload.iloc[:, 0]

    temp = payload.copy()
    for i in range(temp.shape[1]):
        temp.iloc[:, i] = clean_blank_to_nan(temp.iloc[:, i])

    return temp.bfill(axis=1).iloc[:, 0]


def collapse_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    result = {}
    seen = []

    for col in df.columns:
        if col not in seen:
            seen.append(col)

    for col in seen:
        series = get_single_column(df, col)
        result[col] = series

    return pd.DataFrame(result)


def drop_all_named_columns(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    if col_name not in df.columns:
        return df
    return df.loc[:, df.columns != col_name].copy()


def ensure_logical_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = collapse_duplicate_columns(df.copy())

    for logical_name in GROUP_DIMENSIONS + [
        "fixture_id",
        "date",
        "market_result",
        "odds",
        "units",
        "actionable_flag",
        "model_edge_pct",
        "model_edge_abs",
    ]:
        physical = first_existing_column(out, logical_name)
        if physical is None:
            if logical_name not in out.columns:
                out[logical_name] = np.nan
        else:
            out[logical_name] = get_single_column(out, physical)

    return collapse_duplicate_columns(out)


def normalize_result(value) -> str:
    s = norm_text(value)

    if s in {"", "NAN", "NONE"}:
        return "UNGRADED"

    if re.search(r"(^|_)(NO_BET|SKIP|SKIPPED|PASS|BLOCK|BLOCKED|HOLD)($|_)", s):
        return "NO_BET"

    if re.search(r"(^|_)(VOID|CANCELLED|CANCELED|POSTPONED|ABANDONED)($|_)", s):
        return "VOID"

    if re.search(r"(^|_)(PUSH|VOID_PUSH|DRAW_REFUND|REFUND)($|_)", s):
        return "PUSH"

    if re.search(r"(^|_)(LOSS|LOST|FAIL|FAILED|RED|L)($|_)", s):
        return "LOSS"

    if re.search(r"(^|_)(WIN|WON|SUCCESS|GREEN|HIT|W)($|_)", s):
        return "WIN"

    return s


def normalize_text_bucket(series: pd.Series, unknown_label: str = "UNKNOWN") -> pd.Series:
    out = series.copy()
    out = clean_blank_to_nan(out)
    out = out.astype("object")
    out = out.where(~out.isna(), other=unknown_label)
    out = out.astype(str).str.strip()
    out = out.replace("", unknown_label)
    return out


def safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def merge_missing_fields(
    labeled_df: pd.DataFrame,
    deep_df: Optional[pd.DataFrame],
) -> pd.DataFrame:
    labeled = ensure_logical_columns(labeled_df)

    if deep_df is None or deep_df.empty:
        return labeled.copy()

    deep = ensure_logical_columns(deep_df)

    fixture_labeled = get_single_column(labeled, "fixture_id")
    fixture_deep = get_single_column(deep, "fixture_id")

    if fixture_labeled is None or fixture_deep is None:
        return labeled.copy()

    if fixture_labeled.isna().all() or fixture_deep.isna().all():
        return labeled.copy()

    use_cols = ["fixture_id"] + [
        c for c in (
            GROUP_DIMENSIONS
            + ["date", "league", "odds", "units", "actionable_flag", "model_edge_pct", "model_edge_abs"]
        )
        if c in deep.columns
    ]

    deep = deep[use_cols].copy()
    deep = collapse_duplicate_columns(deep)
    deep = deep.drop_duplicates(subset=["fixture_id"], keep="last")

    merged = labeled.merge(
        deep,
        on="fixture_id",
        how="left",
        suffixes=("", "_deep"),
    )
    merged = collapse_duplicate_columns(merged)

    to_fill = GROUP_DIMENSIONS + [
        "date", "league", "odds", "units",
        "actionable_flag", "model_edge_pct", "model_edge_abs"
    ]

    for logical_name in to_fill:
        deep_col = f"{logical_name}_deep"

        base = get_single_column(merged, logical_name)
        fill = get_single_column(merged, deep_col)

        if fill is None:
            continue

        fill = clean_blank_to_nan(fill)

        if base is None:
            final_series = fill
        else:
            base = clean_blank_to_nan(base)
            final_series = base.fillna(fill)

        merged = drop_all_named_columns(merged, logical_name)
        merged = drop_all_named_columns(merged, deep_col)
        merged[logical_name] = final_series

    return collapse_duplicate_columns(merged)


def derive_actionable_flag(df: pd.DataFrame) -> pd.Series:
    explicit = df["actionable_flag"].map(to_bool)

    final_rec = df["final_recommendation"].map(norm_text)
    verdict = df["execution_verdict"].map(norm_text)

    rec_positive = final_rec.isin(ACTIONABLE_POSITIVE_HINTS)
    rec_negative = final_rec.isin(ACTIONABLE_NEGATIVE_HINTS | NO_BET_VALUES)

    verdict_positive = verdict.isin(ACTIONABLE_POSITIVE_HINTS)
    verdict_negative = verdict.isin(ACTIONABLE_NEGATIVE_HINTS | NO_BET_VALUES)

    actionable = pd.Series(index=df.index, dtype="object")

    actionable.loc[explicit.notna()] = explicit.loc[explicit.notna()]
    actionable.loc[actionable.isna() & rec_positive] = True
    actionable.loc[actionable.isna() & rec_negative] = False
    actionable.loc[actionable.isna() & verdict_positive] = True
    actionable.loc[actionable.isna() & verdict_negative] = False

    market_present = clean_blank_to_nan(df["market_primary"]).notna()
    graded_result = df["market_result_norm"].isin(BET_RESULTS)
    no_bet_style = final_rec.isin(NO_BET_VALUES) | verdict.isin(NO_BET_VALUES)

    actionable.loc[actionable.isna() & market_present & graded_result & ~no_bet_style] = True
    actionable.loc[actionable.isna()] = False

    return actionable.astype(bool)


def derive_profit_units(row, stake: float) -> float:
    if not row["is_actionable"]:
        return 0.0

    result = row["market_result_norm"]
    if result not in BET_RESULTS:
        return 0.0

    existing_units = row["units_num"]
    if pd.notna(existing_units):
        return float(existing_units)

    odds = row["odds_num"]

    if result == "WIN":
        if pd.notna(odds) and odds > 1:
            return float((odds - 1.0) * stake)
        return float(stake)
    if result == "LOSS":
        return float(-1.0 * stake)
    if result in {"PUSH", "VOID"}:
        return 0.0

    return 0.0


def derive_stake_units(row, stake: float) -> float:
    if row["is_actionable"] and row["market_result_norm"] in BET_RESULTS:
        return float(stake)
    return 0.0


def add_date_parts(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    primary = pd.to_datetime(out["date"], errors="coerce", utc=True)
    fallback = pd.to_datetime(out["date"], errors="coerce")
    out["date_dt"] = primary.fillna(fallback)

    out["date_day"] = out["date_dt"].dt.strftime("%Y-%m-%d")
    out["date_day"] = out["date_day"].fillna("UNKNOWN_DATE")

    return out


def build_summary(df: pd.DataFrame, group_col: Optional[str] = None) -> pd.DataFrame:
    if group_col is None:
        working = df.copy()
        working["_group_key"] = "ALL"
        group_col = "_group_key"
    else:
        working = df.copy()
        working[group_col] = normalize_text_bucket(working[group_col])

    rows = []

    for key, grp in working.groupby(group_col, dropna=False):
        total_rows = len(grp)
        actionable_rows = int(grp["is_actionable"].sum())
        non_actionable_rows = int((~grp["is_actionable"]).sum())

        graded_actionable = grp[grp["is_actionable"] & grp["market_result_norm"].isin(BET_RESULTS)]
        blocked_rows = grp[~grp["is_actionable"]]

        wins = int((graded_actionable["market_result_norm"] == "WIN").sum())
        losses = int((graded_actionable["market_result_norm"] == "LOSS").sum())
        pushes = int((graded_actionable["market_result_norm"] == "PUSH").sum())
        voids = int((graded_actionable["market_result_norm"] == "VOID").sum())

        blocked_win = int((blocked_rows["market_result_norm"] == "WIN").sum())
        blocked_loss = int((blocked_rows["market_result_norm"] == "LOSS").sum())
        blocked_push = int((blocked_rows["market_result_norm"] == "PUSH").sum())
        blocked_void = int((blocked_rows["market_result_norm"] == "VOID").sum())
        blocked_no_bet = int((blocked_rows["market_result_norm"] == "NO_BET").sum())

        stake_units = float(grp["stake_units_effective"].sum())
        profit_units = float(grp["profit_units_effective"].sum())
        graded_bets = len(graded_actionable)
        decided_bets = wins + losses

        hit_rate_decided = (wins / decided_bets) if decided_bets > 0 else np.nan
        roi_pct = (profit_units / stake_units * 100.0) if stake_units > 0 else np.nan

        avg_odds_actionable = graded_actionable["odds_num"].dropna().mean()
        avg_edge_pct = graded_actionable["model_edge_pct_num"].dropna().mean()
        avg_edge_abs = graded_actionable["model_edge_abs_num"].dropna().mean()

        rows.append({
            "group_value": key,
            "rows_total": total_rows,
            "actionable_rows": actionable_rows,
            "non_actionable_rows": non_actionable_rows,
            "graded_bets": graded_bets,
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "voids": voids,
            "blocked_win": blocked_win,
            "blocked_loss": blocked_loss,
            "blocked_push": blocked_push,
            "blocked_void": blocked_void,
            "blocked_no_bet": blocked_no_bet,
            "stake_units": round(stake_units, 4),
            "profit_units": round(profit_units, 4),
            "roi_pct": round(roi_pct, 4) if pd.notna(roi_pct) else np.nan,
            "hit_rate_decided_pct": round(hit_rate_decided * 100.0, 4) if pd.notna(hit_rate_decided) else np.nan,
            "avg_odds_actionable": round(avg_odds_actionable, 4) if pd.notna(avg_odds_actionable) else np.nan,
            "avg_model_edge_pct": round(avg_edge_pct, 4) if pd.notna(avg_edge_pct) else np.nan,
            "avg_model_edge_abs": round(avg_edge_abs, 4) if pd.notna(avg_edge_abs) else np.nan,
        })

    out = pd.DataFrame(rows)

    sort_cols = []
    if "profit_units" in out.columns:
        sort_cols.append("profit_units")
    if "roi_pct" in out.columns:
        sort_cols.append("roi_pct")
    if "group_value" in out.columns:
        sort_cols.append("group_value")

    ascending = [False, False, True][:len(sort_cols)]
    out = out.sort_values(sort_cols, ascending=ascending, na_position="last").reset_index(drop=True)
    return out


def build_actionable_summary(df: pd.DataFrame) -> pd.DataFrame:
    blocks = []

    overall_all = build_summary(df)
    overall_all.insert(0, "scope_type", "OVERALL")
    overall_all.insert(1, "scope_value", "ALL_ROWS")
    blocks.append(overall_all)

    actionable_only = build_summary(df[df["is_actionable"]].copy())
    actionable_only.insert(0, "scope_type", "FILTER")
    actionable_only.insert(1, "scope_value", "ACTIONABLE_ONLY")
    blocks.append(actionable_only)

    non_actionable_only = build_summary(df[~df["is_actionable"]].copy())
    non_actionable_only.insert(0, "scope_type", "FILTER")
    non_actionable_only.insert(1, "scope_value", "NON_ACTIONABLE_ONLY")
    blocks.append(non_actionable_only)

    for logical_col in ["edge_floor_band", "execution_verdict", "final_recommendation"]:
        sub = build_summary(df[df["is_actionable"]].copy(), group_col=logical_col)
        if "group_value" not in sub.columns:
            sub["group_value"] = pd.Series(dtype="object")
        sub.insert(0, "scope_type", logical_col.upper())
        sub.insert(1, "scope_value", sub["group_value"])
        blocks.append(sub)

    return pd.concat(blocks, ignore_index=True)


def build_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["date_day"] = normalize_text_bucket(working["date_day"], unknown_label="UNKNOWN_DATE")

    rows = []
    for day, grp in working.groupby("date_day", dropna=False):
        actionable = grp[grp["is_actionable"] & grp["market_result_norm"].isin(BET_RESULTS)]
        blocked = grp[~grp["is_actionable"]]

        wins = int((actionable["market_result_norm"] == "WIN").sum())
        losses = int((actionable["market_result_norm"] == "LOSS").sum())
        pushes = int((actionable["market_result_norm"] == "PUSH").sum())
        voids = int((actionable["market_result_norm"] == "VOID").sum())

        blocked_win = int((blocked["market_result_norm"] == "WIN").sum())
        blocked_loss = int((blocked["market_result_norm"] == "LOSS").sum())

        stake_units = float(grp["stake_units_effective"].sum())
        profit_units = float(grp["profit_units_effective"].sum())
        roi_pct = (profit_units / stake_units * 100.0) if stake_units > 0 else np.nan
        decided = wins + losses
        hit_rate = (wins / decided) if decided > 0 else np.nan

        rows.append({
            "date_day": day,
            "rows_total": len(grp),
            "actionable_rows": int(grp["is_actionable"].sum()),
            "non_actionable_rows": int((~grp["is_actionable"]).sum()),
            "graded_bets": len(actionable),
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "voids": voids,
            "blocked_win": blocked_win,
            "blocked_loss": blocked_loss,
            "stake_units": round(stake_units, 4),
            "profit_units": round(profit_units, 4),
            "roi_pct": round(roi_pct, 4) if pd.notna(roi_pct) else np.nan,
            "hit_rate_decided_pct": round(hit_rate * 100.0, 4) if pd.notna(hit_rate) else np.nan,
        })

    out = pd.DataFrame(rows)
    return out.sort_values("date_day").reset_index(drop=True)


def print_console_report(
    df: pd.DataFrame,
    overall: pd.DataFrame,
    actionable_summary: pd.DataFrame,
    daily_summary: pd.DataFrame,
) -> None:
    all_row = overall.iloc[0].to_dict()

    print("\n=== BACKTEST VSIGMA ===")
    print(f"Partidos totales: {len(df)}")
    print(f"Actionables: {int(df['is_actionable'].sum())}")
    print(f"No action / bloqueados: {int((~df['is_actionable']).sum())}")
    print(f"Graded bets: {int((df['is_actionable'] & df['market_result_norm'].isin(BET_RESULTS)).sum())}")
    print(f"Profit units: {all_row.get('profit_units', 0.0):.2f}u")
    print(
        f"ROI: {all_row.get('roi_pct', float('nan')):.2f}%"
        if pd.notna(all_row.get("roi_pct"))
        else "ROI: nan"
    )
    print(
        f"Hit rate decided: {all_row.get('hit_rate_decided_pct', float('nan')):.2f}%"
        if pd.notna(all_row.get("hit_rate_decided_pct"))
        else "Hit rate decided: nan"
    )

    action_row = actionable_summary[actionable_summary["scope_value"] == "ACTIONABLE_ONLY"]
    if not action_row.empty:
        r = action_row.iloc[0].to_dict()
        print("\n--- ACTIONABLE_ONLY ---")
        print(f"Rows: {int(r.get('rows_total', 0))}")
        print(f"Graded bets: {int(r.get('graded_bets', 0))}")
        print(f"Profit units: {r.get('profit_units', 0.0):.2f}u")
        print(
            f"ROI: {r.get('roi_pct', float('nan')):.2f}%"
            if pd.notna(r.get("roi_pct"))
            else "ROI: nan"
        )
        print(
            f"Hit rate decided: {r.get('hit_rate_decided_pct', float('nan')):.2f}%"
            if pd.notna(r.get("hit_rate_decided_pct"))
            else "Hit rate decided: nan"
        )

    if not daily_summary.empty:
        print("\n--- DAILY ---")
        for _, row in daily_summary.iterrows():
            roi_display = f"{row['roi_pct']:.2f}%" if pd.notna(row["roi_pct"]) else "nan"
            print(
                f"{row['date_day']} | rows={int(row['rows_total'])} | actionables={int(row['actionable_rows'])} "
                f"| graded={int(row['graded_bets'])} | PnL={row['profit_units']:.2f}u | ROI={roi_display}"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Backtest real de vSIGMA a partir del CSV etiquetado con resultados."
    )
    parser.add_argument(
        "--labeled-csv",
        default=str(DEFAULT_LABELED_CSV),
        help="Ruta al CSV etiquetado con resultados reales.",
    )
    parser.add_argument(
        "--deep-csv",
        default=str(DEFAULT_DEEP_CSV),
        help="Ruta al CSV de deep analysis candidates para completar metadatos si faltan.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directorio de salida para reportes del backtest.",
    )
    parser.add_argument(
        "--stake",
        type=float,
        default=1.0,
        help="Stake plano por pick actionable. Default = 1.0u",
    )
    args = parser.parse_args()

    labeled_path = Path(args.labeled_csv)
    deep_path = Path(args.deep_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not labeled_path.exists():
        raise FileNotFoundError(f"No existe labeled CSV: {labeled_path}")

    labeled_df = pd.read_csv(labeled_path)
    deep_df = pd.read_csv(deep_path) if deep_path.exists() else None

    df = merge_missing_fields(labeled_df, deep_df)
    df = ensure_logical_columns(df)
    df = add_date_parts(df)

    for col in GROUP_DIMENSIONS + ["league", "market_primary"]:
        df[col] = normalize_text_bucket(df[col])

    df["market_result_norm"] = df["market_result"].map(normalize_result)
    df["odds_num"] = safe_numeric(df["odds"])
    df["units_num"] = safe_numeric(df["units"])
    df["model_edge_pct_num"] = safe_numeric(df["model_edge_pct"])
    df["model_edge_abs_num"] = safe_numeric(df["model_edge_abs"])

    df["is_actionable"] = derive_actionable_flag(df)

    df["profit_units_effective"] = df.apply(lambda row: derive_profit_units(row, args.stake), axis=1)
    df["stake_units_effective"] = df.apply(lambda row: derive_stake_units(row, args.stake), axis=1)

    overall = build_summary(df)

    output_files = []

    overview_path = output_dir / "vsigma_backtest_overall.csv"
    overall.to_csv(overview_path, index=False)
    output_files.append(overview_path)

    for dim in GROUP_DIMENSIONS:
        summary_df = build_summary(df, group_col=dim)
        out_path = output_dir / f"vsigma_backtest_by_{dim}.csv"
        summary_df.to_csv(out_path, index=False)
        output_files.append(out_path)

    actionable_summary = build_actionable_summary(df)
    actionable_path = output_dir / "vsigma_backtest_actionable_summary.csv"
    actionable_summary.to_csv(actionable_path, index=False)
    output_files.append(actionable_path)

    daily_summary = build_daily_summary(df)
    daily_path = output_dir / "vsigma_backtest_daily_summary.csv"
    daily_summary.to_csv(daily_path, index=False)
    output_files.append(daily_path)

    enriched_path = output_dir / "vsigma_backtest_enriched_source.csv"
    df.to_csv(enriched_path, index=False)
    output_files.append(enriched_path)

    report_txt_path = output_dir / "vsigma_backtest_report.txt"
    with open(report_txt_path, "w", encoding="utf-8") as f:
        f.write("=== BACKTEST VSIGMA ===\n")
        f.write(f"Rows total: {len(df)}\n")
        f.write(f"Actionable rows: {int(df['is_actionable'].sum())}\n")
        f.write(f"Non-actionable rows: {int((~df['is_actionable']).sum())}\n")
        f.write(f"Graded bets: {int((df['is_actionable'] & df['market_result_norm'].isin(BET_RESULTS)).sum())}\n\n")
        f.write("--- OVERALL ---\n")
        f.write(overall.to_string(index=False))
        f.write("\n\n--- ACTIONABLE SUMMARY ---\n")
        f.write(actionable_summary.to_string(index=False))
        f.write("\n\n--- DAILY SUMMARY ---\n")
        f.write(daily_summary.to_string(index=False))
        f.write("\n")
    output_files.append(report_txt_path)

    print_console_report(df, overall, actionable_summary, daily_summary)

    print("\n=== ARCHIVOS GENERADOS ===")
    for p in output_files:
        print(p)

    print("\n=== BACKTEST VSIGMA COMPLETADO ===")


if __name__ == "__main__":
    main()
