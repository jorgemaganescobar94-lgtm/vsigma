from pathlib import Path
import pandas as pd


DATA_PATH = Path("data/raw/matches.csv")
OUTPUT_PATH = Path("outputs/predictions.csv")


def load_matches(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("El CSV está vacío.")
    return df


def estimate_goals(df: pd.DataFrame) -> pd.DataFrame:
    df["est_home_goals"] = (
        (
            df["home_xg_for"] * 0.6
            + df["away_xg_against"] * 0.4
            + df["home_scored_rate"] * 0.35
            - df["away_clean_sheet_rate"] * 0.20
        )
    ).round(2)

    df["est_away_goals"] = (
        (
            df["away_xg_for"] * 0.6
            + df["home_xg_against"] * 0.4
            + df["away_scored_rate"] * 0.35
            - df["home_clean_sheet_rate"] * 0.20
        )
    ).round(2)

    df["est_home_goals"] = df["est_home_goals"].clip(lower=0.2, upper=3.5)
    df["est_away_goals"] = df["est_away_goals"].clip(lower=0.2, upper=3.5)
    df["total_est_goals"] = (df["est_home_goals"] + df["est_away_goals"]).round(2)
    return df


def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    df["damage_home"] = (
        df["home_xg_for"] * 4.0
        + df["home_sot_for"] * 1.2
        + df["home_big_for"] * 2.0
        + df["home_form_pts"] * 0.25
        + df["home_scored_rate"] * 3.0
        + df["home_motivation"] * 0.35
        - df["home_absences"] * 0.8
    ).round(2)

    df["damage_away"] = (
        df["away_xg_for"] * 4.0
        + df["away_sot_for"] * 1.2
        + df["away_big_for"] * 2.0
        + df["away_form_pts"] * 0.25
        + df["away_scored_rate"] * 3.0
        + df["away_motivation"] * 0.35
        - df["away_absences"] * 0.8
    ).round(2)

    df["suppression_home"] = (
        df["home_clean_sheet_rate"] * 5.0
        + (2.0 - df["home_xg_against"]) * 2.0
        - df["away_scored_rate"] * 2.0
    ).round(2)

    df["suppression_away"] = (
        df["away_clean_sheet_rate"] * 5.0
        + (2.0 - df["away_xg_against"]) * 2.0
        - df["home_scored_rate"] * 2.0
    ).round(2)

    df["control_home"] = (
        df["damage_home"] + df["suppression_home"] - df["damage_away"]
    ).round(2)

    df["control_away"] = (
        df["damage_away"] + df["suppression_away"] - df["damage_home"]
    ).round(2)

    df["edge_home"] = (df["damage_home"] - df["damage_away"]).round(2)
    df["edge_away"] = (df["damage_away"] - df["damage_home"]).round(2)

    df["under_35_score"] = (
        8.5
        - df["total_est_goals"] * 1.3
        - (df["home_big_for"] + df["away_big_for"]) * 0.45
        - (df["home_sot_for"] + df["away_sot_for"]) * 0.08
        + (df["home_clean_sheet_rate"] + df["away_clean_sheet_rate"]) * 1.4
    ).round(2)

    df["fragility_score"] = (
        df["total_est_goals"]
        + (df["home_big_for"] + df["away_big_for"]) * 0.5
        + (df["home_absences"] + df["away_absences"]) * 0.35
    ).round(2)

    return df


def detect_regime(row: pd.Series) -> str:
    if row["control_home"] >= 6.5 and row["est_home_goals"] > row["est_away_goals"] + 0.25:
        return "control_local_fuerte"
    if row["control_away"] >= 6.5 and row["est_away_goals"] > row["est_home_goals"] + 0.25:
        return "control_visitante_fuerte"
    if row["under_35_score"] >= 3.0 and row["total_est_goals"] <= 2.7:
        return "partido_corto"
    if abs(row["est_home_goals"] - row["est_away_goals"]) <= 0.20:
        return "partido_equilibrado"
    return "partido_mixto"


def choose_market(row: pd.Series) -> str:
    if row["under_35_score"] >= 3.0 and row["total_est_goals"] <= 2.7:
        return "under_3_5"

    if (
        row["control_home"] >= 6.5
        and row["edge_home"] >= 4.0
        and row["est_home_goals"] > row["est_away_goals"]
        and row["away_scored_rate"] <= 0.65
    ):
        return "local_dnb_o_1x"

    if (
        row["control_away"] >= 6.5
        and row["edge_away"] >= 4.0
        and row["est_away_goals"] > row["est_home_goals"]
        and row["home_scored_rate"] <= 0.65
    ):
        return "visitante_dnb_o_x2"

    if row["away_scored_rate"] <= 0.55 and row["control_home"] >= 4.5:
        return "away_under_1_5"

    if row["home_scored_rate"] <= 0.55 and row["control_away"] >= 4.5:
        return "home_under_1_5"

    return "no_bet"


def choose_aggressive_market(row: pd.Series) -> str:
    if row["market"] == "under_3_5" and row["total_est_goals"] <= 2.2:
        return "under_2_5"
    if row["market"] == "local_dnb_o_1x" and row["control_home"] >= 8.5:
        return "local_win"
    if row["market"] == "visitante_dnb_o_x2" and row["control_away"] >= 8.5:
        return "visitante_win"
    if row["market"] == "away_under_1_5" and row["est_home_goals"] >= 1.4:
        return "local_win + away_under_1_5"
    if row["market"] == "home_under_1_5" and row["est_away_goals"] >= 1.4:
        return "visitante_win + home_under_1_5"
    return "no_recomiendo_subir_cuota"


def probable_score(row: pd.Series) -> str:
    home = max(0, min(4, round(row["est_home_goals"])))
    away = max(0, min(4, round(row["est_away_goals"])))
    return f"{home}-{away}"


def classify_pick(row: pd.Series) -> str:
    if row["market"] == "no_bet":
        return "NO_BET"

    base_strength = max(row["control_home"], row["control_away"], row["under_35_score"])

    if (
        row["market"] == "under_3_5"
        and row["under_35_score"] >= 3.8
        and row["fragility_score"] <= 4.2
        and row["total_est_goals"] <= 2.6
    ):
        return "CORE_A"

    if (
        row["market"] in ["local_dnb_o_1x", "visitante_dnb_o_x2"]
        and base_strength >= 8.5
        and row["fragility_score"] <= 4.2
        and abs(row["est_home_goals"] - row["est_away_goals"]) >= 0.35
    ):
        return "CORE_A"

    if (
        row["market"] in [
            "under_3_5",
            "local_dnb_o_1x",
            "visitante_dnb_o_x2",
            "away_under_1_5",
            "home_under_1_5",
        ]
        and base_strength >= 6.0
    ):
        return "CORE_B"

    return "SECUNDARIO"


def confidence_label(row: pd.Series) -> str:
    if row["market"] == "no_bet":
        return "baja"

    strength = max(row["control_home"], row["control_away"], row["under_35_score"])

    if strength >= 8.5:
        return "alta"
    if strength >= 6:
        return "media"
    return "baja"


def execution_window(row: pd.Series) -> str:
    if row["market"] == "no_bet":
        return "no_bet"
    if row["home_absences"] >= 3 or row["away_absences"] >= 3:
        return "post_lineup"
    if row["fragility_score"] >= 4.5:
        return "min_10_15"
    return "prematch"


def build_reason(row: pd.Series) -> str:
    if row["market"] == "under_3_5":
        return "Guion de goles contenidos y estructura de partido corto."
    if row["market"] == "local_dnb_o_1x":
        return "El local combina mejor daño real, supresión y contexto."
    if row["market"] == "visitante_dnb_o_x2":
        return "El visitante llega con superioridad estructural y cobertura útil."
    if row["market"] == "away_under_1_5":
        return "El visitante tiene baja ruta ofensiva y producción limitada."
    if row["market"] == "home_under_1_5":
        return "El local tiene baja ruta ofensiva y producción limitada."
    return "No hay ventaja estructural suficientemente limpia."


def compute_final_score(row: pd.Series) -> float:
    if row["market"] == "no_bet":
        return 0.0

    base_strength = max(row["control_home"], row["control_away"], row["under_35_score"])

    market_bonus_map = {
        "under_3_5": 1.4,
        "local_dnb_o_1x": 1.2,
        "visitante_dnb_o_x2": 1.2,
        "away_under_1_5": 1.0,
        "home_under_1_5": 1.0,
    }
    market_bonus = market_bonus_map.get(row["market"], 0.0)

    grade_bonus_map = {
        "CORE_A": 2.0,
        "CORE_B": 1.0,
        "SECUNDARIO": 0.3,
        "NO_BET": 0.0,
    }
    grade_bonus = grade_bonus_map.get(row["pick_grade"], 0.0)

    confidence_bonus_map = {
        "alta": 1.4,
        "media": 0.8,
        "baja": 0.0,
    }
    confidence_bonus = confidence_bonus_map.get(row["confidence"], 0.0)

    score = (
        base_strength
        + market_bonus
        + grade_bonus
        + confidence_bonus
        - (row["fragility_score"] * 0.35)
    )

    return round(score, 2)


def is_eligible_pick(row: pd.Series) -> str:
    if row["market"] == "no_bet":
        return "NO"

    if row["pick_grade"] == "CORE_A" and row["final_score"] >= 12:
        return "SI"

    if row["pick_grade"] == "CORE_B" and row["final_score"] >= 9:
        return "SI"

    return "NO"


def add_ranking(df: pd.DataFrame) -> pd.DataFrame:
    df["final_score"] = df.apply(compute_final_score, axis=1)
    df = df.sort_values(by="final_score", ascending=False).reset_index(drop=True)
    df["ranking"] = df.index + 1
    df["eligible_pick"] = df.apply(is_eligible_pick, axis=1)
    return df


def build_predictions(df: pd.DataFrame) -> pd.DataFrame:
    df["regime"] = df.apply(detect_regime, axis=1)
    df["market"] = df.apply(choose_market, axis=1)
    df["aggressive_market"] = df.apply(choose_aggressive_market, axis=1)
    df["predicted_score"] = df.apply(probable_score, axis=1)
    df["pick_grade"] = df.apply(classify_pick, axis=1)
    df["confidence"] = df.apply(confidence_label, axis=1)
    df["execution_window"] = df.apply(execution_window, axis=1)
    df["reason"] = df.apply(build_reason, axis=1)

    df = add_ranking(df)

    columns = [
        "ranking",
        "final_score",
        "eligible_pick",
        "date",
        "league",
        "home_team",
        "away_team",
        "regime",
        "market",
        "aggressive_market",
        "pick_grade",
        "confidence",
        "execution_window",
        "predicted_score",
        "reason",
        "est_home_goals",
        "est_away_goals",
        "total_est_goals",
        "damage_home",
        "damage_away",
        "suppression_home",
        "suppression_away",
        "control_home",
        "control_away",
        "edge_home",
        "edge_away",
        "under_35_score",
        "fragility_score",
    ]
    return df[columns].copy()


def print_summary(result: pd.DataFrame) -> None:
    print("\n=== PREDICCIONES vSIGMA 0.5 ===\n")
    for _, row in result.iterrows():
        print(
            f"#{row['ranking']} | Score {row['final_score']} | "
            f"Elegible: {row['eligible_pick']} | {row['home_team']} vs {row['away_team']}"
        )
        print(f"  Régimen: {row['regime']}")
        print(f"  Mercado base: {row['market']}")
        print(f"  Mercado para subir cuota: {row['aggressive_market']}")
        print(f"  Grado: {row['pick_grade']} | Confianza: {row['confidence']}")
        print(f"  Ventana de entrada: {row['execution_window']}")
        print(f"  Marcador estimado: {row['predicted_score']}")
        print(f"  Motivo: {row['reason']}")
        print("")

def print_eligible_summary(result: pd.DataFrame) -> None:
    eligible = result[result["eligible_pick"] == "SI"].copy()

    print("\n=== TOP OPERATIVO (SOLO ELEGIBLES) ===\n")

    if eligible.empty:
        print("No hay picks elegibles.\n")
        return

    for _, row in eligible.iterrows():
        print(
            f"#{row['ranking']} | Score {row['final_score']} | "
            f"{row['home_team']} vs {row['away_team']}"
        )
        print(f"  Mercado: {row['market']}")
        print(f"  Grado: {row['pick_grade']}")
        print(f"  Confianza: {row['confidence']}")
        print(f"  Entrada: {row['execution_window']}")
        print("")

def main() -> None:
    df = load_matches(DATA_PATH)
    df = estimate_goals(df)
    df = compute_scores(df)
    result = build_predictions(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)

    print_summary(result)
    print_eligible_summary(result)
    print(f"Archivo guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()