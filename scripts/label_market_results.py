from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
DEEP_ANALYSIS_CSV = ROOT / "data" / "processed" / "vsigma_deep_analysis_candidates.csv"

OUTPUT_CSV = ROOT / "data" / "processed" / "vsigma_market_results_labeled.csv"
REPORT_CSV = ROOT / "data" / "processed" / "vsigma_market_results_report.csv"


FINISHED_STATUSES = {
    "FT",      # full time
    "AET",     # after extra time
    "PEN",     # penalties
}

STATUS_COL_CANDIDATES = [
    "status",
    "fixture_status_short",
    "status_short",
    "match_status",
]

GOAL_COL_PAIRS = [
    ("score_fulltime_home", "score_fulltime_away"),
    ("fulltime_home", "fulltime_away"),
    ("ft_home_goals", "ft_away_goals"),
    ("goals_home", "goals_away"),
    ("home_goals", "away_goals"),
    ("score_home", "score_away"),
]

SUPPORTED_MARKETS = {
    "HOME_WIN",
    "AWAY_WIN",
    "HOME_DNB",
    "AWAY_DNB",
    "OVER_1_5",
    "OVER_2_5",
    "UNDER_3_5",
    "BTTS_YES",
    "BTTS_NO",
    "HOME_TEAM_OVER_0_5",
    "AWAY_TEAM_OVER_0_5",
}


def first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def status_is_finished(row: pd.Series, status_col: str | None) -> bool:
    if status_col is None:
        return False
    value = str(row.get(status_col, "")).strip().upper()
    return value in FINISHED_STATUSES


def safe_num(value):
    try:
        if pd.isna(value):
            return np.nan
        return float(value)
    except Exception:
        return np.nan


def resolve_goals(row: pd.Series) -> tuple[float, float]:
    """
    Intenta localizar los goles FT usando varias parejas de columnas.
    Si no encuentra nada, devuelve (nan, nan).
    """
    for home_col, away_col in GOAL_COL_PAIRS:
        if home_col in row.index and away_col in row.index:
            hg = safe_num(row.get(home_col))
            ag = safe_num(row.get(away_col))
            if not pd.isna(hg) and not pd.isna(ag):
                return hg, ag

    # fallback adicional por si existe nomenclatura rara
    extra_home = [c for c in row.index if c.lower() in {"goals.home", "score.fulltime.home"}]
    extra_away = [c for c in row.index if c.lower() in {"goals.away", "score.fulltime.away"}]
    if extra_home and extra_away:
        hg = safe_num(row.get(extra_home[0]))
        ag = safe_num(row.get(extra_away[0]))
        if not pd.isna(hg) and not pd.isna(ag):
            return hg, ag

    return np.nan, np.nan


def evaluate_market(market: str, home_goals: float, away_goals: float) -> str:
    if pd.isna(home_goals) or pd.isna(away_goals):
        return "NO_SCORE"

    total_goals = home_goals + away_goals

    if market == "HOME_WIN":
        return "WIN" if home_goals > away_goals else "LOSS"

    if market == "AWAY_WIN":
        return "WIN" if away_goals > home_goals else "LOSS"

    if market == "HOME_DNB":
        if home_goals > away_goals:
            return "WIN"
        if home_goals == away_goals:
            return "PUSH"
        return "LOSS"

    if market == "AWAY_DNB":
        if away_goals > home_goals:
            return "WIN"
        if home_goals == away_goals:
            return "PUSH"
        return "LOSS"

    if market == "OVER_1_5":
        return "WIN" if total_goals >= 2 else "LOSS"

    if market == "OVER_2_5":
        return "WIN" if total_goals >= 3 else "LOSS"

    if market == "UNDER_3_5":
        return "WIN" if total_goals <= 3 else "LOSS"

    if market == "BTTS_YES":
        return "WIN" if home_goals >= 1 and away_goals >= 1 else "LOSS"

    if market == "BTTS_NO":
        return "WIN" if (home_goals == 0 or away_goals == 0) else "LOSS"

    if market == "HOME_TEAM_OVER_0_5":
        return "WIN" if home_goals >= 1 else "LOSS"

    if market == "AWAY_TEAM_OVER_0_5":
        return "WIN" if away_goals >= 1 else "LOSS"

    return "UNSUPPORTED_MARKET"


def settle_profit(result: str, odds_value) -> float:
    odds_value = safe_num(odds_value)

    if result == "WIN":
        if pd.isna(odds_value) or odds_value <= 1.0:
            return np.nan
        return round(float(odds_value) - 1.0, 4)

    if result == "LOSS":
        return -1.0

    if result in {"PUSH", "VOID"}:
        return 0.0

    return np.nan


def recommendation_is_actionable(rec: str) -> bool:
    return str(rec).strip().upper() in {"BET", "LEAN_PLAY"}


def summarize_primary(group: pd.DataFrame) -> pd.Series:
    settled = group[group["primary_result"].isin(["WIN", "LOSS", "PUSH"])]
    wins = int((settled["primary_result"] == "WIN").sum())
    losses = int((settled["primary_result"] == "LOSS").sum())
    pushes = int((settled["primary_result"] == "PUSH").sum())

    decisive = wins + losses
    win_rate = round(wins / decisive, 4) if decisive > 0 else np.nan
    roi = round(settled["primary_profit_units"].dropna().sum(), 4) if not settled.empty else np.nan
    avg_edge = round(group["primary_edge"].dropna().mean(), 4) if group["primary_edge"].notna().any() else np.nan

    return pd.Series(
        {
            "n_total": int(len(group)),
            "n_settled": int(len(settled)),
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "win_rate_no_push": win_rate,
            "roi_units": roi,
            "avg_primary_edge": avg_edge,
        }
    )


def main() -> None:
    if not RAW_MATCHES_CSV.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES_CSV}")
    if not DEEP_ANALYSIS_CSV.exists():
        raise FileNotFoundError(f"No existe: {DEEP_ANALYSIS_CSV}")

    raw = pd.read_csv(RAW_MATCHES_CSV)
    deep = pd.read_csv(DEEP_ANALYSIS_CSV)

    if deep.empty:
        print("No hay análisis profundo para etiquetar.")
        return

    status_col = first_existing_column(raw, STATUS_COL_CANDIDATES)

    merge_cols = ["fixture_id"]
    for col in GOAL_COL_PAIRS:
        for c in col:
            if c in raw.columns and c not in merge_cols:
                merge_cols.append(c)

    if status_col and status_col not in merge_cols:
        merge_cols.append(status_col)

    merged = deep.merge(raw[merge_cols].copy(), on="fixture_id", how="left")

    home_goals_list = []
    away_goals_list = []
    match_finished_list = []
    primary_result_list = []
    alt_result_list = []
    primary_profit_list = []
    alt_profit_list = []
    actionable_flag_list = []
    actionable_result_list = []
    actionable_profit_list = []

    for _, row in merged.iterrows():
        hg, ag = resolve_goals(row)
        home_goals_list.append(hg)
        away_goals_list.append(ag)

        finished = status_is_finished(row, status_col)
        if finished and (pd.isna(hg) or pd.isna(ag)):
            finished = False

        match_finished_list.append(1 if finished else 0)

        primary_market = str(row.get("market_primary", "")).strip().upper()
        alt_market = str(row.get("market_alt", "")).strip().upper()

        if not finished:
            primary_result = "PENDING"
            alt_result = "PENDING"
            primary_profit = np.nan
            alt_profit = np.nan
        else:
            primary_result = evaluate_market(primary_market, hg, ag)
            alt_result = evaluate_market(alt_market, hg, ag)

            primary_profit = settle_profit(primary_result, row.get("primary_odds_used"))
            alt_profit = settle_profit(alt_result, row.get("alt_odds_used"))

        primary_result_list.append(primary_result)
        alt_result_list.append(alt_result)
        primary_profit_list.append(primary_profit)
        alt_profit_list.append(alt_profit)

        actionable = recommendation_is_actionable(str(row.get("final_recommendation", "")))
        actionable_flag_list.append(1 if actionable else 0)

        if actionable:
            actionable_result_list.append(primary_result)
            actionable_profit_list.append(primary_profit)
        else:
            actionable_result_list.append("SKIPPED")
            actionable_profit_list.append(np.nan)

    merged["resolved_home_goals"] = home_goals_list
    merged["resolved_away_goals"] = away_goals_list
    merged["match_finished_flag"] = match_finished_list

    merged["primary_result"] = primary_result_list
    merged["alt_result"] = alt_result_list
    merged["primary_profit_units"] = primary_profit_list
    merged["alt_profit_units"] = alt_profit_list

    merged["actionable_flag"] = actionable_flag_list
    merged["actionable_result"] = actionable_result_list
    merged["actionable_profit_units"] = actionable_profit_list

    merged.to_csv(OUTPUT_CSV, index=False)

    report_parts = []

    by_market = (
        merged.groupby("market_primary", dropna=False)
        .apply(summarize_primary, include_groups=False)
        .reset_index()
    )
    by_market["report_type"] = "by_market_primary"
    report_parts.append(by_market)

    by_edge_band = (
        merged.groupby("edge_floor_band", dropna=False)
        .apply(summarize_primary, include_groups=False)
        .reset_index()
    )
    by_edge_band["report_type"] = "by_edge_floor_band"
    report_parts.append(by_edge_band)

    by_execution = (
        merged.groupby("execution_verdict", dropna=False)
        .apply(summarize_primary, include_groups=False)
        .reset_index()
    )
    by_execution["report_type"] = "by_execution_verdict"
    report_parts.append(by_execution)

    actionable = merged[merged["actionable_flag"] == 1].copy()
    if not actionable.empty:
        actionable_settled = actionable[actionable["actionable_result"].isin(["WIN", "LOSS", "PUSH"])].copy()
        if not actionable_settled.empty:
            wins = int((actionable_settled["actionable_result"] == "WIN").sum())
            losses = int((actionable_settled["actionable_result"] == "LOSS").sum())
            pushes = int((actionable_settled["actionable_result"] == "PUSH").sum())
            decisive = wins + losses
            win_rate = round(wins / decisive, 4) if decisive > 0 else np.nan
            roi = round(actionable_settled["actionable_profit_units"].dropna().sum(), 4)

            actionable_summary = pd.DataFrame(
                [
                    {
                        "report_type": "actionable_summary",
                        "market_primary": "ACTIONABLE_ONLY",
                        "n_total": int(len(actionable)),
                        "n_settled": int(len(actionable_settled)),
                        "wins": wins,
                        "losses": losses,
                        "pushes": pushes,
                        "win_rate_no_push": win_rate,
                        "roi_units": roi,
                        "avg_primary_edge": round(actionable["primary_edge"].dropna().mean(), 4)
                        if actionable["primary_edge"].notna().any()
                        else np.nan,
                    }
                ]
            )
            report_parts.append(actionable_summary)

    report = pd.concat(report_parts, ignore_index=True, sort=False)
    report.to_csv(REPORT_CSV, index=False)

    print("\n=== LABEL MARKET RESULTS COMPLETADO ===")
    print(f"Entrada análisis: {DEEP_ANALYSIS_CSV}")
    print(f"Entrada resultados: {RAW_MATCHES_CSV}")
    print(f"Salida etiquetada: {OUTPUT_CSV}")
    print(f"Reporte: {REPORT_CSV}")

    print("\nVista previa etiquetada:")
    preview_cols = [
        "fixture_id",
        "home_team",
        "away_team",
        "market_primary",
        "market_alt",
        "resolved_home_goals",
        "resolved_away_goals",
        "match_finished_flag",
        "primary_result",
        "alt_result",
        "primary_profit_units",
        "alt_profit_units",
        "execution_verdict",
        "final_recommendation",
    ]
    preview_cols = [c for c in preview_cols if c in merged.columns]
    print(merged[preview_cols].to_string(index=False))

    print("\nResumen reporte:")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()