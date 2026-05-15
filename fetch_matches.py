from pathlib import Path
from datetime import datetime
import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv


RAW_JSON_PATH = Path("data/raw/api_matches.json")
CSV_PATH = Path("data/raw/matches.csv")


ALLOWED_STATUSES = {"NS", "TBD", "PST"}


def load_api_config() -> tuple[str, str]:
    load_dotenv()

    api_key = os.getenv("API_FOOTBALL_KEY", "").strip()
    api_host = os.getenv("API_FOOTBALL_HOST", "").strip()

    if not api_key:
        raise ValueError("Falta API_FOOTBALL_KEY en el archivo .env")

    if not api_host:
        raise ValueError("Falta API_FOOTBALL_HOST en el archivo .env")

    return api_key, api_host


def fetch_fixtures(date_str: str) -> dict:
    api_key, api_host = load_api_config()

    url = f"https://{api_host}/fixtures"
    headers = {
        "x-apisports-key": api_key,
        "x-rapidapi-host": api_host,
    }
    params = {
        "date": date_str,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_json(payload: dict) -> None:
    RAW_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def normalize_matches(payload: dict) -> pd.DataFrame:
    rows = []

    for item in payload.get("response", []):
        fixture = item.get("fixture", {})
        league = item.get("league", {})
        teams = item.get("teams", {})

        home = teams.get("home", {})
        away = teams.get("away", {})

        rows.append(
            {
                "date": fixture.get("date", "")[:10],
                "league": league.get("name", ""),
                "league_id": league.get("id", ""),
                "season": league.get("season", ""),
                "fixture_id": fixture.get("id", ""),
                "status": fixture.get("status", {}).get("short", ""),
                "home_team": home.get("name", ""),
                "home_team_id": home.get("id", ""),
                "away_team": away.get("name", ""),
                "away_team_id": away.get("id", ""),
                "home_xg_for": 0.0,
                "home_xg_against": 0.0,
                "away_xg_for": 0.0,
                "away_xg_against": 0.0,
                "home_sot_for": 0.0,
                "away_sot_for": 0.0,
                "home_big_for": 0.0,
                "away_big_for": 0.0,
                "home_form_pts": 0.0,
                "away_form_pts": 0.0,
                "home_scored_rate": 0.0,
                "away_scored_rate": 0.0,
                "home_clean_sheet_rate": 0.0,
                "away_clean_sheet_rate": 0.0,
                "home_motivation": 5.0,
                "away_motivation": 5.0,
                "home_absences": 0.0,
                "away_absences": 0.0,
            }
        )

    return pd.DataFrame(rows)


def filter_upcoming_matches(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    filtered = df[df["status"].isin(ALLOWED_STATUSES)].copy()
    filtered = filtered.reset_index(drop=True)
    return filtered


def save_csv(df: pd.DataFrame) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)


def main() -> None:
    target_date = input("Fecha a descargar (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("La fecha debe estar en formato YYYY-MM-DD")

    payload = fetch_fixtures(target_date)
    save_raw_json(payload)

    raw_df = normalize_matches(payload)
    filtered_df = filter_upcoming_matches(raw_df)
    save_csv(filtered_df)

    print("\n=== DESCARGA COMPLETADA ===\n")
    print(f"Partidos totales descargados: {len(raw_df)}")
    print(f"Partidos útiles guardados: {len(filtered_df)}")
    print(f"JSON bruto guardado en: {RAW_JSON_PATH}")
    print(f"CSV base guardado en: {CSV_PATH}")

    if not filtered_df.empty:
        print("\nPrimeros partidos útiles encontrados:\n")
        print(
            filtered_df[
                [
                    "date",
                    "league",
                    "fixture_id",
                    "home_team",
                    "away_team",
                    "status",
                ]
            ].head(20).to_string(index=False)
        )
    else:
        print("\nNo se encontraron partidos útiles con esos estados.")


if __name__ == "__main__":
    main()