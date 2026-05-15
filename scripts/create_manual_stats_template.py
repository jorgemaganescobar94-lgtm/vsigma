from __future__ import annotations

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

FILTERED_PATH = ROOT / "data" / "processed" / "matches_league_filtered.csv"
OUTPUT_DIR = ROOT / "data" / "input"
OUTPUT_PATH = OUTPUT_DIR / "manual_fixture_stats.csv"

MAX_TIER_RANK = 2


STAT_COLUMNS = [
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


def main() -> None:
    if not FILTERED_PATH.exists():
        raise FileNotFoundError(f"No existe: {FILTERED_PATH}. Ejecuta antes filter_leagues.py")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(FILTERED_PATH)

    df["league_tier_rank"] = pd.to_numeric(df["league_tier_rank"], errors="coerce")

    targets = df[df["league_tier_rank"] <= MAX_TIER_RANK].copy()

    base_cols = [
        "fixture_id",
        "date",
        "country",
        "league",
        "league_tier",
        "home_team",
        "away_team",
    ]

    template = targets[base_cols].copy()

    for col in STAT_COLUMNS:
        if col not in template.columns:
            template[col] = ""

    template["manual_notes"] = ""

    if OUTPUT_PATH.exists():
        old = pd.read_csv(OUTPUT_PATH)

        if "fixture_id" in old.columns:
            keep_cols = ["fixture_id"] + [c for c in STAT_COLUMNS + ["manual_notes"] if c in old.columns]
            old_keep = old[keep_cols].copy()

            template = template.drop(columns=[c for c in STAT_COLUMNS + ["manual_notes"] if c in template.columns])
            template = template.merge(old_keep, on="fixture_id", how="left")

            for col in STAT_COLUMNS + ["manual_notes"]:
                if col not in template.columns:
                    template[col] = ""

    template.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("\n=== PLANTILLA MANUAL CREADA ===")
    print(f"Archivo: {OUTPUT_PATH}")
    print(f"Partidos incluidos TIER_1/TIER_2: {len(template)}")
    print("\nRellena estas columnas con datos tipo:")
    print("- form_pts: puntos por partido últimos 5/8")
    print("- goals_for_pg: goles a favor por partido")
    print("- goals_against_pg: goles en contra por partido")
    print("- scored_rate: 0 a 1")
    print("- clean_sheet_rate: 0 a 1")
    print("- btts_rate: 0 a 1")
    print("- over15_rate / over25_rate: 0 a 1")
    print("\nVista previa:")
    print(template.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
