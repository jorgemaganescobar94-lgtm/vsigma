from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "processed" / "matches_league_filtered.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_SCORED = OUTPUT_DIR / "matches_vsigma_scored_v2.csv"
OUTPUT_TOP = OUTPUT_DIR / "vsigma_top_candidates_v2.csv"
OUTPUT_REPORT = OUTPUT_DIR / "vsigma_score_report_v2.csv"


LEAGUE_BASE_SCORE = {
    "TIER_1": 30,
    "TIER_2": 23,
    "TIER_3": 13,
    "TIER_4": 4,
}


NUMERIC_COLS = [
    # capa antigua
    "home_xg_for", "home_xg_against", "away_xg_for", "away_xg_against",
    "home_sot_for", "away_sot_for", "home_big_for", "away_big_for",
    # capa reciente / prior histórica
    "home_form_pts", "away_form_pts",
    "home_goals_for_pg", "away_goals_for_pg",
    "home_goals_against_pg", "away_goals_against_pg",
    "home_scored_rate", "away_scored_rate",
    "home_clean_sheet_rate", "away_clean_sheet_rate",
    "home_btts_rate", "away_btts_rate",
    "home_over15_rate", "away_over15_rate",
    "home_over25_rate", "away_over25_rate",
]

TEXT_COLS = [
    "home_motivation", "away_motivation",
    "home_absences", "away_absences",
]


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in NUMERIC_COLS:
        if col not in df.columns:
            df[col] = np.nan

    for col in TEXT_COLS:
        if col not in df.columns:
            df[col] = ""

    return df


def to_numeric(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def normalize_rate(s: pd.Series) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")

    if s.dropna().empty:
        return s

    if s.dropna().max() > 1.5:
        return s / 100.0

    return s


def clip(s: pd.Series | float, low: float, high: float):
    if isinstance(s, pd.Series):
        return s.clip(lower=low, upper=high)
    return max(low, min(high, s))


def motivation_to_num(value) -> float:
    if pd.isna(value):
        return 0.0

    txt = str(value).strip().lower()

    if txt in {"", "nan", "none", "-", "null"}:
        return 0.0

    try:
        num = float(txt)
        if -1.0 <= num <= 1.0:
            return num
        return 0.0
    except ValueError:
        pass

    high_words = [
        "high", "alta", "must win", "title", "champion", "promotion",
        "relegation", "survival", "europe", "playoff", "play-off",
        "final", "derby", "objective", "urgent", "necesita"
    ]
    medium_words = [
        "medium", "media", "normal", "moderate", "competitive",
        "compite", "important"
    ]
    low_words = [
        "low", "baja", "nothing", "nada", "safe", "rotation", "rotacion", "friendly"
    ]

    if any(w in txt for w in high_words):
        return 1.0
    if any(w in txt for w in medium_words):
        return 0.5
    if any(w in txt for w in low_words):
        return -0.5

    return 0.0


def absences_to_num(value) -> float:
    if pd.isna(value):
        return 0.0

    txt = str(value).strip().lower()

    if txt in {"", "nan", "none", "no", "0", "-", "sin bajas"}:
        return 0.0

    try:
        return min(float(txt), 6.0)
    except ValueError:
        pass

    parts = [p.strip() for p in txt.replace("|", ",").replace("/", ",").replace(";", ",").split(",") if p.strip()]
    return min(float(len(parts)), 6.0)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo filtrado: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df = ensure_columns(df)

    for col in NUMERIC_COLS:
        df[col] = to_numeric(df, col)

    rate_cols = [
        "home_scored_rate", "away_scored_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_btts_rate", "away_btts_rate",
        "home_over15_rate", "away_over15_rate",
        "home_over25_rate", "away_over25_rate",
    ]
    for col in rate_cols:
        df[col] = normalize_rate(df[col])

    # ==============================
    # 1) score de liga
    # ==============================
    df["league_quality_score"] = df["league_tier"].map(LEAGUE_BASE_SCORE).fillna(0)

    # ==============================
    # 2) calidad de datos
    # ==============================
    old_core = [
        "home_xg_for", "home_xg_against", "away_xg_for", "away_xg_against",
        "home_sot_for", "away_sot_for", "home_big_for", "away_big_for",
    ]

    prior_core = [
        "home_form_pts", "away_form_pts",
        "home_goals_for_pg", "away_goals_for_pg",
        "home_goals_against_pg", "away_goals_against_pg",
        "home_scored_rate", "away_scored_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_btts_rate", "away_btts_rate",
        "home_over15_rate", "away_over15_rate",
        "home_over25_rate", "away_over25_rate",
    ]

    df["old_data_count"] = df[old_core].notna().sum(axis=1)
    df["prior_data_count"] = df[prior_core].notna().sum(axis=1)

    df["data_quality_score"] = (
        (df["old_data_count"] / len(old_core)) * 9
        + (df["prior_data_count"] / len(prior_core)) * 11
    ).round(2)

    df["data_warning"] = "NO_DATA"

    df.loc[df["prior_data_count"] >= 8, "data_warning"] = "OK_PRIOR"
    df.loc[df["old_data_count"] >= 4, "data_warning"] = "OK_FULL"

    # ==============================
    # 3) capa reciente / prior
    # ==============================
    home_attack_prior = (
        df["home_goals_for_pg"].fillna(0) * 4.2
        + df["home_scored_rate"].fillna(0) * 5.5
        + df["home_over15_rate"].fillna(0) * 2.2
        + df["home_over25_rate"].fillna(0) * 1.8
        + df["home_btts_rate"].fillna(0) * 1.4
    )

    away_attack_prior = (
        df["away_goals_for_pg"].fillna(0) * 4.2
        + df["away_scored_rate"].fillna(0) * 5.5
        + df["away_over15_rate"].fillna(0) * 2.2
        + df["away_over25_rate"].fillna(0) * 1.8
        + df["away_btts_rate"].fillna(0) * 1.4
    )

    df["attack_environment_score"] = clip(
        (
            home_attack_prior
            + away_attack_prior
            + (df["home_goals_against_pg"].fillna(0) * 1.8)
            + (df["away_goals_against_pg"].fillna(0) * 1.8)
        ) / 2.4,
        0, 18
    ).round(2)

    # ==============================
    # 4) rutas de gol
    # ==============================
    df["home_goal_path_score"] = clip(
        df["home_goals_for_pg"].fillna(0) * 3.5
        + df["home_scored_rate"].fillna(0) * 5.0
        + df["away_goals_against_pg"].fillna(0) * 2.8
        - df["away_clean_sheet_rate"].fillna(0) * 2.5,
        0, 18
    ).round(2)

    df["away_goal_path_score"] = clip(
        df["away_goals_for_pg"].fillna(0) * 3.5
        + df["away_scored_rate"].fillna(0) * 5.0
        + df["home_goals_against_pg"].fillna(0) * 2.8
        - df["home_clean_sheet_rate"].fillna(0) * 2.5,
        0, 18
    ).round(2)

    # ==============================
    # 5) edge de equipo
    # ==============================
    home_strength = (
        df["home_form_pts"].fillna(0) * 3.5
        + df["home_goals_for_pg"].fillna(0) * 4.0
        - df["home_goals_against_pg"].fillna(0) * 2.8
        + df["home_scored_rate"].fillna(0) * 3.0
        + df["home_clean_sheet_rate"].fillna(0) * 1.5
    )

    away_strength = (
        df["away_form_pts"].fillna(0) * 3.5
        + df["away_goals_for_pg"].fillna(0) * 4.0
        - df["away_goals_against_pg"].fillna(0) * 2.8
        + df["away_scored_rate"].fillna(0) * 3.0
        + df["away_clean_sheet_rate"].fillna(0) * 1.5
    )

    df["team_edge_raw"] = (home_strength - away_strength).round(2)
    df["team_edge_score"] = clip(df["team_edge_raw"].abs() * 1.15, 0, 16).round(2)

    # ==============================
    # 6) motivación y bajas
    # ==============================
    df["home_motivation_num"] = df["home_motivation"].apply(motivation_to_num)
    df["away_motivation_num"] = df["away_motivation"].apply(motivation_to_num)

    df["home_absences_num"] = df["home_absences"].apply(absences_to_num)
    df["away_absences_num"] = df["away_absences"].apply(absences_to_num)

    df["motivation_total_score"] = clip(
        (df["home_motivation_num"].abs() + df["away_motivation_num"].abs()) * 3.0,
        0, 6
    ).round(2)

    df["absences_noise_penalty"] = clip(
        (df["home_absences_num"] + df["away_absences_num"]) * 1.2,
        0, 8
    ).round(2)

    # ==============================
    # 7) score total
    # ==============================
    df["vsigma_pre_score"] = (
        df["league_quality_score"]
        + df["data_quality_score"]
        + df["attack_environment_score"]
        + df["team_edge_score"]
        + df["motivation_total_score"]
        - df["absences_noise_penalty"]
    ).round(2)

    df.loc[df["league_tier"] == "TIER_4", "vsigma_pre_score"] = (
        df.loc[df["league_tier"] == "TIER_4", "vsigma_pre_score"] - 12
    ).round(2)

    df.loc[df["data_warning"] == "NO_DATA", "vsigma_pre_score"] = (
        df.loc[df["data_warning"] == "NO_DATA", "vsigma_pre_score"] - 18
    ).round(2)

    # ==============================
    # 8) prioridad
    # ==============================
    has_real_data = df["data_warning"].isin(["OK_FULL", "OK_PRIOR"])

    conditions = [
        has_real_data & (df["vsigma_pre_score"] >= 62),
        has_real_data & (df["vsigma_pre_score"] >= 52),
        has_real_data & (df["vsigma_pre_score"] >= 42),
        has_real_data & (df["vsigma_pre_score"] >= 34),
    ]

    choices = [
        "A_ANALIZAR_PRIMERO",
        "B_ANALIZAR",
        "C_SOLO_SI_BLOQUE_SECO",
        "D_CONTEXT_ONLY",
    ]

    df["vsigma_priority"] = np.select(conditions, choices, default="NO_DATA_BLOCKED")

    # ==============================
    # 9) pista de mercado
    # ==============================
    df["market_family_hint"] = "NO_DATA_ENRICHMENT_REQUIRED"

    # OVER / BTTS
    df.loc[
        has_real_data
        & (df["home_goal_path_score"] >= 7.2)
        & (df["away_goal_path_score"] >= 7.2)
        & (
            (df["home_btts_rate"].fillna(0) + df["away_btts_rate"].fillna(0) >= 0.95)
            | (df["attack_environment_score"] >= 8.8)
            | (
                (df["home_goals_for_pg"].fillna(0) + df["away_goals_for_pg"].fillna(0) >= 3.4)
                & (df["home_goals_against_pg"].fillna(0) + df["away_goals_against_pg"].fillna(0) >= 2.2)
            )
        ),
        "market_family_hint"
    ] = "OVER_OR_BTTS_CHECK"

    # HOME
    df.loc[
        has_real_data
        & (df["team_edge_raw"] >= 2.0)
        & (df["home_goal_path_score"] >= 7.0)
        & (df["home_form_pts"].fillna(0) >= df["away_form_pts"].fillna(0)),
        "market_family_hint"
    ] = "HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK"

    # AWAY
    df.loc[
        has_real_data
        & (df["team_edge_raw"] <= -2.0)
        & (df["away_goal_path_score"] >= 7.0)
        & (df["away_form_pts"].fillna(0) >= df["home_form_pts"].fillna(0)),
        "market_family_hint"
    ] = "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK"

    # UNDER
    df.loc[
        has_real_data
        & (df["home_goal_path_score"] <= 5.8)
        & (df["away_goal_path_score"] <= 5.8)
        & (df["attack_environment_score"] <= 7.0)
        & (
            (df["home_over25_rate"].fillna(0) + df["away_over25_rate"].fillna(0) <= 0.85)
            | (df["home_goals_for_pg"].fillna(0) + df["away_goals_for_pg"].fillna(0) <= 2.2)
        ),
        "market_family_hint"
    ] = "UNDER_OR_TEAM_TOTAL_UNDER_CHECK"

    # ==============================
    # 10) orden final
    # ==============================
    df = df.sort_values(
        by=[
            "vsigma_pre_score",
            "league_tier_rank",
            "data_quality_score",
            "team_edge_score",
        ],
        ascending=[False, True, False, False],
    )

    output_cols = [
        "date",
        "country",
        "league",
        "league_tier",
        "fixture_id",
        "home_team",
        "away_team",
        "status",
        "vsigma_pre_score",
        "vsigma_priority",
        "market_family_hint",
        "data_warning",
        "league_quality_score",
        "data_quality_score",
        "attack_environment_score",
        "team_edge_score",
        "team_edge_raw",
        "home_goal_path_score",
        "away_goal_path_score",
        "motivation_total_score",
        "absences_noise_penalty",
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

    existing_output_cols = [c for c in output_cols if c in df.columns]

    df.to_csv(OUTPUT_SCORED, index=False)
    df[existing_output_cols].head(30).to_csv(OUTPUT_TOP, index=False)

    report = (
        df.groupby(["league_tier", "vsigma_priority", "market_family_hint"])
        .size()
        .reset_index(name="matches")
        .sort_values(["league_tier", "vsigma_priority", "matches"], ascending=[True, True, False])
    )
    report.to_csv(OUTPUT_REPORT, index=False)

    print("\n=== SCORE INICIAL vSIGMA v2 COMPLETADO ===")
    print(f"Partidos recibidos del filtro: {len(df)}")
    print(f"Archivo score completo: {OUTPUT_SCORED}")
    print(f"Archivo top candidatos: {OUTPUT_TOP}")
    print(f"Archivo reporte: {OUTPUT_REPORT}")

    print("\nDistribución por prioridad:")
    print(df["vsigma_priority"].value_counts().to_string())

    print("\nDistribución por pista de mercado:")
    print(df["market_family_hint"].value_counts().to_string())

    print("\nTOP 25 candidatos iniciales:")
    print(df[existing_output_cols].head(25).to_string(index=False))


if __name__ == "__main__":
    main()