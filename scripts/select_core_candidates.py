from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "processed" / "matches_vsigma_scored_v3.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_SHORTLIST = OUTPUT_DIR / "vsigma_core_shortlist.csv"
OUTPUT_REPORT = OUTPUT_DIR / "vsigma_core_shortlist_report.csv"


PRIORITY_RANK = {
    "A_ANALIZAR_PRIMERO": 1,
    "B_ANALIZAR": 2,
    "C_SOLO_SI_BLOQUE_SECO": 3,
    "D_CONTEXT_ONLY": 4,
    "NO_DATA_BLOCKED": 99,
}

MARKET_BONUS = {
    "HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK": 1.4,
    "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK": 1.4,
    "OVER_OR_BTTS_CHECK": 1.2,
    "UNDER_OR_TEAM_TOTAL_UNDER_CHECK": 0.9,
    "NO_DATA_ENRICHMENT_REQUIRED": -99.0,
}


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    needed_defaults = {
        "vsigma_priority": "NO_DATA_BLOCKED",
        "market_family_hint": "NO_DATA_ENRICHMENT_REQUIRED",
        "data_warning": "NO_DATA",
        "data_enrichment_level": "",
        "home_recent_matches": np.nan,
        "away_recent_matches": np.nan,
        "vsigma_pre_score": np.nan,
        "league_tier_rank": np.nan,
        "injuries_quality_flag": "NONE",
        "home_absence_risk_score": np.nan,
        "away_absence_risk_score": np.nan,
        "home_absence_severity_flag": "UNKNOWN",
        "away_absence_severity_flag": "UNKNOWN",
        "availability_uncertainty_penalty": np.nan,
        "lineup_quality_flag": "NONE",
        "lineup_activation_state": "INACTIVE",
        "lineup_confirmation_score": np.nan,
        "lineup_uncertainty_penalty": np.nan,
        "lineup_score_nudge": np.nan,
        "league_coverage_class": "COVERAGE_UNKNOWN",
        "league_data_reliability_score": np.nan,
        "league_coverage_source_status": "COVERAGE_NOT_LOADED",
        "league_has_fixture_stats_coverage": np.nan,
        "league_has_odds_coverage": np.nan,
        "league_has_injuries_coverage": np.nan,
        "league_has_lineups_coverage": np.nan,
        "league_stats_reliability_multiplier": np.nan,
        "league_coverage_uncertainty_penalty": np.nan,
    }

    for col, default in needed_defaults.items():
        if col not in df.columns:
            df[col] = default

    return df


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No existe: {INPUT_PATH}. Ejecuta antes score_matches_v2.py")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df = ensure_columns(df)

    df["vsigma_pre_score"] = pd.to_numeric(df["vsigma_pre_score"], errors="coerce")
    df["league_tier_rank"] = pd.to_numeric(df["league_tier_rank"], errors="coerce")
    df["home_recent_matches"] = pd.to_numeric(df["home_recent_matches"], errors="coerce")
    df["away_recent_matches"] = pd.to_numeric(df["away_recent_matches"], errors="coerce")
    df["home_absence_risk_score"] = pd.to_numeric(df["home_absence_risk_score"], errors="coerce")
    df["away_absence_risk_score"] = pd.to_numeric(df["away_absence_risk_score"], errors="coerce")
    df["availability_uncertainty_penalty"] = pd.to_numeric(
        df["availability_uncertainty_penalty"],
        errors="coerce",
    )
    df["league_data_reliability_score"] = pd.to_numeric(df["league_data_reliability_score"], errors="coerce")
    df["league_coverage_uncertainty_penalty"] = pd.to_numeric(
        df["league_coverage_uncertainty_penalty"],
        errors="coerce",
    ).fillna(0.0)

    df["priority_rank"] = df["vsigma_priority"].map(PRIORITY_RANK).fillna(99)
    df["market_bonus"] = df["market_family_hint"].map(MARKET_BONUS).fillna(0.0)

    # Elegibilidad real
    has_valid_priority = df["vsigma_priority"].isin([
        "A_ANALIZAR_PRIMERO",
        "B_ANALIZAR",
        "C_SOLO_SI_BLOQUE_SECO",
    ])

    has_valid_data = df["data_warning"].isin([
        "OK_FULL",
        "OK_PRIOR",
        "OK_STANDINGS",
        "OK_PRIOR_STANDINGS",
        "OK_FULL_STATS",
        "OK_PRIOR_STATS",
        "OK_STANDINGS_STATS",
        "OK_PRIOR_STANDINGS_STATS",
    ])

    not_hard_blocked = ~df["data_enrichment_level"].astype(str).str.contains(
        "NO_AVAILABLE|ERROR",
        case=False,
        na=False,
    )

    has_market_hint = df["market_family_hint"] != "NO_DATA_ENRICHMENT_REQUIRED"

    enough_recent_matches = (
        (df["home_recent_matches"].fillna(0) >= 4)
        & (df["away_recent_matches"].fillna(0) >= 4)
    )

    soft_recent_matches = (
        (
            (df["home_recent_matches"].fillna(0) >= 4)
            & (df["away_recent_matches"].fillna(0) >= 3)
        )
        | (
            (df["home_recent_matches"].fillna(0) >= 3)
            & (df["away_recent_matches"].fillna(0) >= 4)
        )
    )

    df["selection_eligible"] = (
        has_valid_priority
        & has_valid_data
        & not_hard_blocked
        & has_market_hint
        & (enough_recent_matches | soft_recent_matches)
    )

    # Penalizaci?n si una muestra es d?bil
    df["sample_penalty"] = 0.0
    df.loc[df["home_recent_matches"].fillna(0) < 6, "sample_penalty"] += 1.0
    df.loc[df["away_recent_matches"].fillna(0) < 6, "sample_penalty"] += 1.0
    df.loc[df["home_recent_matches"].fillna(0) < 4, "sample_penalty"] += 1.0
    df.loc[df["away_recent_matches"].fillna(0) < 4, "sample_penalty"] += 1.0
    df["sample_penalty"] += df["league_coverage_uncertainty_penalty"].clip(lower=0, upper=1.25) * 0.60
    # Advisory mode: injury coverage/risk survives as output context, but it
    # no longer changes core shortlist eligibility or ranking.

    # Bonus por prioridad
    df["priority_bonus"] = 0.0
    df.loc[df["vsigma_priority"] == "A_ANALIZAR_PRIMERO", "priority_bonus"] = 3.0
    df.loc[df["vsigma_priority"] == "B_ANALIZAR", "priority_bonus"] = 1.5
    df.loc[df["vsigma_priority"] == "C_SOLO_SI_BLOQUE_SECO", "priority_bonus"] = 0.5

    # Bonus ligero por TIER
    df["tier_bonus"] = 0.0
    df.loc[df["league_tier_rank"] == 1, "tier_bonus"] = 1.5
    df.loc[df["league_tier_rank"] == 2, "tier_bonus"] = 0.8

    df["selection_score"] = (
        df["vsigma_pre_score"].fillna(0)
        + df["priority_bonus"]
        + df["tier_bonus"]
        + df["market_bonus"]
        - df["sample_penalty"]
    ).round(2)

    shortlist = df[df["selection_eligible"]].copy()

    shortlist = shortlist.sort_values(
        by=[
            "priority_rank",
            "selection_score",
            "vsigma_pre_score",
        ],
        ascending=[True, False, False],
    )

    shortlist["shortlist_rank"] = range(1, len(shortlist) + 1)

    shortlist["shortlist_bucket"] = "WATCHLIST"
    shortlist.loc[shortlist["shortlist_rank"] <= 5, "shortlist_bucket"] = "CORE_SHORTLIST"
    shortlist.loc[
        (shortlist["vsigma_priority"].isin(["A_ANALIZAR_PRIMERO", "B_ANALIZAR"]))
        & (shortlist["shortlist_rank"] <= 2),
        "shortlist_bucket"
    ] = "TOP_CORE"

    output_cols = [
        "shortlist_rank",
        "shortlist_bucket",
        "date",
        "country",
        "league",
        "league_tier",
        "fixture_id",
        "home_team",
        "away_team",
        "vsigma_priority",
        "market_family_hint",
        "selection_score",
        "vsigma_pre_score",
        "data_warning",
        "data_enrichment_level",
        "league_coverage_class",
        "league_data_reliability_score",
        "league_coverage_rich_flag",
        "league_has_odds_coverage",
        "league_has_fixture_stats_coverage",
        "league_has_injuries_coverage",
        "league_has_lineups_coverage",
        "league_has_predictions_coverage",
        "league_stats_reliability_multiplier",
        "league_coverage_uncertainty_penalty",
        "league_coverage_source_status",
        "league_coverage_note",
        "home_recent_matches",
        "away_recent_matches",
        "home_recent_stats_matches_used",
        "away_recent_stats_matches_used",
        "home_recent_stats_coverage_ratio",
        "away_recent_stats_coverage_ratio",
        "home_recent_shots_for_pg",
        "away_recent_shots_for_pg",
        "home_recent_sot_for_pg",
        "away_recent_sot_for_pg",
        "home_recent_sot_against_pg",
        "away_recent_sot_against_pg",
        "recent_stats_quality_flag",
        "home_injuries_count",
        "away_injuries_count",
        "home_injuries_coverage_flag",
        "away_injuries_coverage_flag",
        "home_absence_risk_score",
        "away_absence_risk_score",
        "home_absence_severity_flag",
        "away_absence_severity_flag",
        "injuries_quality_flag",
        "availability_uncertainty_penalty",
        "home_lineup_available_flag",
        "away_lineup_available_flag",
        "home_lineup_quality_flag",
        "away_lineup_quality_flag",
        "lineup_quality_flag",
        "lineup_activation_state",
        "lineup_activation_window_minutes",
        "lineup_minutes_to_kickoff",
        "lineup_timing_eligible_flag",
        "lineup_structural_confidence_flag",
        "home_lineup_known_starters_count",
        "away_lineup_known_starters_count",
        "home_lineup_bench_known_flag",
        "away_lineup_bench_known_flag",
        "home_lineup_attacker_count",
        "away_lineup_attacker_count",
        "home_lineup_defender_count",
        "away_lineup_defender_count",
        "home_lineup_midfielder_count",
        "away_lineup_midfielder_count",
        "home_lineup_goalkeeper_known_flag",
        "away_lineup_goalkeeper_known_flag",
        "home_lineup_attack_continuity_score",
        "away_lineup_attack_continuity_score",
        "home_lineup_defense_continuity_score",
        "away_lineup_defense_continuity_score",
        "lineup_confirmation_score",
        "lineup_uncertainty_penalty",
        "lineup_score_nudge",
        "home_form_pts",
        "away_form_pts",
        "home_goals_for_pg",
        "away_goals_for_pg",
        "home_goals_against_pg",
        "away_goals_against_pg",
        "home_scored_rate",
        "away_scored_rate",
        "home_clean_sheet_rate",
        "away_clean_sheet_rate",
        "home_btts_rate",
        "away_btts_rate",
        "home_over15_rate",
        "away_over15_rate",
        "home_over25_rate",
        "away_over25_rate",
    ]

    existing_output_cols = [c for c in output_cols if c in shortlist.columns]

    shortlist.to_csv(OUTPUT_SHORTLIST, index=False, encoding="utf-8-sig")

    report = (
        shortlist.groupby(["shortlist_bucket", "vsigma_priority", "market_family_hint"])
        .size()
        .reset_index(name="matches")
        .sort_values(["shortlist_bucket", "matches"], ascending=[True, False])
    )
    report.to_csv(OUTPUT_REPORT, index=False, encoding="utf-8-sig")

    print("\n=== SHORTLIST CORE vSIGMA COMPLETADO ===")
    print(f"Entrada total score v3: {len(df)}")
    print(f"Elegibles reales: {len(shortlist)}")
    print(f"Archivo shortlist: {OUTPUT_SHORTLIST}")
    print(f"Archivo reporte: {OUTPUT_REPORT}")

    print("\nDistribución por bucket:")
    if not shortlist.empty:
        print(shortlist["shortlist_bucket"].value_counts().to_string())
    else:
        print("Ningún partido elegible todavía.")

    print("\nTOP shortlist:")
    if not shortlist.empty:
        print(shortlist[existing_output_cols].head(15).to_string(index=False))
    else:
        print("Vacío")


if __name__ == "__main__":
    main()
