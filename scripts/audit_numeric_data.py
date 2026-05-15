from __future__ import annotations

from pathlib import Path
import json
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
RAW_JSON = ROOT / "data" / "raw" / "api_matches.json"
FILTERED_CSV = ROOT / "data" / "processed" / "matches_league_filtered.csv"


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


def print_csv_audit(path: Path, name: str) -> None:
    print(f"\n=== AUDITANDO {name} ===")
    print(f"Ruta: {path}")

    if not path.exists():
        print("NO EXISTE")
        return

    df = pd.read_csv(path)
    print(f"Filas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")

    existing_numeric = [c for c in NUMERIC_COLUMNS if c in df.columns]

    if not existing_numeric:
        print("No hay columnas numéricas vSIGMA.")
        return

    print("\nResumen columnas numéricas:")
    rows = []

    for col in existing_numeric:
        s = pd.to_numeric(df[col], errors="coerce")
        rows.append({
            "column": col,
            "non_null": int(s.notna().sum()),
            "zeros": int((s.fillna(0) == 0).sum()),
            "non_zero": int((s.fillna(0) != 0).sum()),
            "min": s.min(),
            "max": s.max(),
            "mean": s.mean(),
        })

    report = pd.DataFrame(rows)
    print(report.to_string(index=False))

    numeric_sum = df[existing_numeric].apply(pd.to_numeric, errors="coerce").fillna(0).abs().sum(axis=1)
    print("\nFilas con todo numérico a cero:")
    print(int((numeric_sum == 0).sum()), "/", len(df))

    print("\nPrimeras 10 filas clave:")
    cols = [
        "date", "country", "league", "fixture_id", "home_team", "away_team",
        "home_xg_for", "away_xg_for", "home_sot_for", "away_sot_for",
        "home_big_for", "away_big_for", "home_form_pts", "away_form_pts",
        "home_scored_rate", "away_scored_rate",
    ]
    existing_cols = [c for c in cols if c in df.columns]
    print(df[existing_cols].head(10).to_string(index=False))


def print_json_audit(path: Path) -> None:
    print("\n=== AUDITANDO api_matches.json ===")
    print(f"Ruta: {path}")

    if not path.exists():
        print("NO EXISTE")
        return

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        print(f"Tipo raíz: dict")
        print(f"Claves raíz: {list(data.keys())}")

        response = data.get("response")
        if isinstance(response, list):
            print(f"Partidos en response: {len(response)}")

            if response:
                item = response[0]
                print("\nClaves del primer partido:")
                print(list(item.keys()))

                for key in ["fixture", "league", "teams", "goals", "score"]:
                    if key in item:
                        print(f"\n[{key}]")
                        print(item[key])

                possible_stat_keys = [
                    "statistics", "stats", "xg", "shots", "big_chances",
                    "standings", "form", "fixtures"
                ]

                print("\n¿Aparecen claves de estadísticas directas en el primer partido?")
                for k in possible_stat_keys:
                    print(f"{k}: {k in item}")

    elif isinstance(data, list):
        print(f"Tipo raíz: list")
        print(f"Elementos: {len(data)}")
        if data:
            print(f"Claves primer elemento: {list(data[0].keys())}")
    else:
        print(f"Estructura no reconocida: {type(data)}")


def main() -> None:
    print_csv_audit(MATCHES_CSV, "matches.csv")
    print_csv_audit(FILTERED_CSV, "matches_league_filtered.csv")
    print_json_audit(RAW_JSON)


if __name__ == "__main__":
    main()
