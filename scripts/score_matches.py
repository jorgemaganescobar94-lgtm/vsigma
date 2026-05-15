from __future__ import annotations

from pathlib import Path
import re
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "processed" / "matches_league_filtered.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_SCORED = OUTPUT_DIR / "matches_vsigma_scored.csv"
OUTPUT_TOP = OUTPUT_DIR / "vsigma_top_candidates.csv"
OUTPUT_REPORT = OUTPUT_DIR / "vsigma_score_report.csv"


NUMERIC_COLUMNS = [
    "home_xg_for",
    "home_xg_against",
    "away_xg_for",
    "away_xg_against",
    "home_sot_for",
    "away_sot_for",
    "home_big_for",
    "away_big_for",
    "home_form_pts",
    "away_form_pts",
    "home_scored_rate",
    "away_scored_rate",
    "home_clean_sheet_rate",
    "away_clean_sheet_rate",
]


LEAGUE_BASE_SCORE = {
    "TIER_1": 30,
    "TIER_2": 23,
    "TIER_3": 13,
    "TIER_4": 4,
}


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in NUMERIC_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    for col in ["home_motivation", "away_motivation", "home_absences", "away_absences"]:
        if col not in df.columns:
            df[col] = ""

    return df


def to_numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def normalize_rate(s: pd.Series) -> pd.Series:
    """
    Convierte tasas 0-100 a 0-1 si vienen en porcentaje.
    Si ya vienen 0-1, las deja igual.
    """
    s = pd.to_numeric(s, errors="coerce")

    if s.dropna().empty:
        return s

    if s.dropna().max() > 1.5:
        return s / 100.0

    return s


def motivation_to_num(value) -> float:
    if pd.isna(value):
        return 0.0

    txt = str(value).strip().lower()

    if txt in {"", "nan", "none", "-", "null"}:
        return 0.0

    try:
        num = float(txt)

        # De momento solo aceptamos motivación ya normalizada entre -1 y 1.
        # Valores como 5.0 suelen ser placeholders falsos del pipeline.
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
        "low", "baja", "nothing", "nada", "safe", "rotacion",
        "rotation", "friendly"
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

    # Si viene como número directo
    try:
        return min(float(txt), 6.0)
    except ValueError:
        pass

    # Si viene como texto con nombres, contamos separadores
    parts = re.split(r"[,;/|]+", txt)
    parts = [p.strip() for p in parts if p.strip()]

    return min(float(len(parts)), 6.0)


def clip_series(s: pd.Series, low: float, high: float) -> pd.Series:
    return s.clip(lower=low, upper=high)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo filtrado: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df = ensure_columns(df)

    # Convertimos columnas numéricas
    for col in NUMERIC_COLUMNS:
        df[col] = to_numeric_series(df, col)

    df["home_scored_rate"] = normalize_rate(df["home_scored_rate"])
    df["away_scored_rate"] = normalize_rate(df["away_scored_rate"])
    df["home_clean_sheet_rate"] = normalize_rate(df["home_clean_sheet_rate"])
    df["away_clean_sheet_rate"] = normalize_rate(df["away_clean_sheet_rate"])

    # ==============================
    # 1) Score de liga
    # ==============================
    df["league_quality_score"] = df["league_tier"].map(LEAGUE_BASE_SCORE).fillna(0)

    # ==============================
    # 2) Calidad de datos
    # ==============================
    core_cols = [
        "home_xg_for",
        "home_xg_against",
        "away_xg_for",
        "away_xg_against",
        "home_sot_for",
        "away_sot_for",
        "home_big_for",
        "away_big_for",
        "home_form_pts",
        "away_form_pts",
        "home_scored_rate",
        "away_scored_rate",
        "home_clean_sheet_rate",
        "away_clean_sheet_rate",
    ]

    df["data_available_count"] = df[core_cols].notna().sum(axis=1)
    df["data_quality_score"] = (df["data_available_count"] / len(core_cols) * 15).round(2)

    # Si todos los datos numéricos son 0 o NaN, marcamos alerta
    numeric_sum = df[core_cols].fillna(0).abs().sum(axis=1)
    df["data_warning"] = np.where(
        numeric_sum <= 0,
        "NO_NUMERIC_DATA_OR_ALL_ZERO",
        "OK"
    )

    # ==============================
    # 3) Daño ofensivo estimado
    # ==============================
    home_attack = (
        df["home_xg_for"].fillna(0) * 8.0
        + df["home_sot_for"].fillna(0) * 1.0
        + df["home_big_for"].fillna(0) * 2.2
        + df["home_scored_rate"].fillna(0) * 8.0
    )

    away_attack = (
        df["away_xg_for"].fillna(0) * 8.0
        + df["away_sot_for"].fillna(0) * 1.0
        + df["away_big_for"].fillna(0) * 2.2
        + df["away_scored_rate"].fillna(0) * 8.0
    )

    df["home_attack_score_raw"] = home_attack
    df["away_attack_score_raw"] = away_attack

    df["attack_environment_score"] = clip_series(
        (home_attack + away_attack) / 2.0,
        0,
        18
    ).round(2)

    # ==============================
    # 4) Supresión defensiva / fragilidad rival
    # ==============================
    home_can_hurt = (
        df["home_xg_for"].fillna(0) * 5.0
        + df["away_xg_against"].fillna(0) * 5.0
        + df["home_big_for"].fillna(0) * 1.5
        - df["away_clean_sheet_rate"].fillna(0) * 4.0
    )

    away_can_hurt = (
        df["away_xg_for"].fillna(0) * 5.0
        + df["home_xg_against"].fillna(0) * 5.0
        + df["away_big_for"].fillna(0) * 1.5
        - df["home_clean_sheet_rate"].fillna(0) * 4.0
    )

    df["home_goal_path_score"] = clip_series(home_can_hurt, 0, 18).round(2)
    df["away_goal_path_score"] = clip_series(away_can_hurt, 0, 18).round(2)

    # ==============================
    # 5) Diferencial de equipo
    # ==============================
    home_strength = (
        df["home_xg_for"].fillna(0) * 8.0
        - df["home_xg_against"].fillna(0) * 5.0
        + df["home_sot_for"].fillna(0) * 0.8
        + df["home_big_for"].fillna(0) * 2.0
        + df["home_form_pts"].fillna(0) * 2.0
        + df["home_scored_rate"].fillna(0) * 5.0
        + df["home_clean_sheet_rate"].fillna(0) * 3.0
    )

    away_strength = (
        df["away_xg_for"].fillna(0) * 8.0
        - df["away_xg_against"].fillna(0) * 5.0
        + df["away_sot_for"].fillna(0) * 0.8
        + df["away_big_for"].fillna(0) * 2.0
        + df["away_form_pts"].fillna(0) * 2.0
        + df["away_scored_rate"].fillna(0) * 5.0
        + df["away_clean_sheet_rate"].fillna(0) * 3.0
    )

    df["home_strength_raw"] = home_strength.round(2)
    df["away_strength_raw"] = away_strength.round(2)
    df["team_edge_raw"] = (home_strength - away_strength).round(2)
    df["team_edge_abs"] = df["team_edge_raw"].abs().round(2)

    df["team_edge_score"] = clip_series(df["team_edge_abs"], 0, 16).round(2)

    # ==============================
    # 6) Motivación y bajas
    # ==============================
    df["home_motivation_num"] = df["home_motivation"].apply(motivation_to_num)
    df["away_motivation_num"] = df["away_motivation"].apply(motivation_to_num)

    df["home_absences_num"] = df["home_absences"].apply(absences_to_num)
    df["away_absences_num"] = df["away_absences"].apply(absences_to_num)

    df["motivation_total_score"] = clip_series(
        (df["home_motivation_num"].abs() + df["away_motivation_num"].abs()) * 3.0,
        0,
        6,
    ).round(2)

    df["absences_noise_penalty"] = clip_series(
        (df["home_absences_num"] + df["away_absences_num"]) * 1.2,
        0,
        8,
    ).round(2)

    # ==============================
    # 7) Score total preliminar
    # ==============================
    df["vsigma_pre_score"] = (
        df["league_quality_score"]
        + df["data_quality_score"]
        + df["attack_environment_score"]
        + df["team_edge_score"]
        + df["motivation_total_score"]
        - df["absences_noise_penalty"]
    ).round(2)

    # Penalización dura para TIER_4
    df.loc[df["league_tier"] == "TIER_4", "vsigma_pre_score"] = (
        df.loc[df["league_tier"] == "TIER_4", "vsigma_pre_score"] - 12
    ).round(2)

    # Penalización si no hay datos numéricos útiles
    df.loc[df["data_warning"] != "OK", "vsigma_pre_score"] = (
        df.loc[df["data_warning"] != "OK", "vsigma_pre_score"] - 18
    ).round(2)

    # ==============================
    # 8) Etiqueta de prioridad
    # ==============================
    has_real_data = df["data_warning"] == "OK"

    conditions = [
        has_real_data & (df["vsigma_pre_score"] >= 70),
        has_real_data & (df["vsigma_pre_score"] >= 58),
        has_real_data & (df["vsigma_pre_score"] >= 45),
        has_real_data & (df["vsigma_pre_score"] >= 30),
    ]

    choices = [
        "A_ANALIZAR_PRIMERO",
        "B_ANALIZAR",
        "C_SOLO_SI_BLOQUE_SECO",
        "D_CONTEXT_ONLY",
    ]

    df["vsigma_priority"] = np.select(
        conditions,
        choices,
        default="NO_DATA_BLOCKED"
    )

    # ==============================
    # 9) Pista inicial de mercado
    # ==============================
    df["market_family_hint"] = "NO_DATA_ENRICHMENT_REQUIRED"

    # Favorito local / visitante por edge
    df.loc[
        has_real_data
        & (df["team_edge_raw"] >= 8)
        & (df["home_goal_path_score"] >= 8),
        "market_family_hint"
    ] = "HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK"

    df.loc[
        has_real_data
        & (df["team_edge_raw"] <= -8)
        & (df["away_goal_path_score"] >= 8),
        "market_family_hint"
    ] = "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK"

    # Partido con rutas de gol en ambos lados
    df.loc[
        has_real_data
        & (df["home_goal_path_score"] >= 7)
        & (df["away_goal_path_score"] >= 7)
        & (df["attack_environment_score"] >= 10),
        "market_family_hint"
    ] = "OVER_OR_BTTS_CHECK"

    # Partido de baja ruta ofensiva
    df.loc[
        has_real_data
        & (df["home_goal_path_score"] <= 5)
        & (df["away_goal_path_score"] <= 5)
        & (df["attack_environment_score"] <= 8),
        "market_family_hint"
    ] = "UNDER_OR_TEAM_TOTAL_UNDER_CHECK"

    # ==============================
    # 10) Orden final
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
    "home_motivation_num",
    "away_motivation_num",
    "home_absences_num",
    "away_absences_num",
    "home_xg_for",
    "home_xg_against",
    "away_xg_for",
    "away_xg_against",
    "home_sot_for",
    "away_sot_for",
    "home_big_for",
    "away_big_for",
    "home_form_pts",
    "away_form_pts",
    "home_scored_rate",
    "away_scored_rate",
    "home_clean_sheet_rate",
    "away_clean_sheet_rate",
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

    print("\n=== SCORE INICIAL vSIGMA COMPLETADO ===")
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
