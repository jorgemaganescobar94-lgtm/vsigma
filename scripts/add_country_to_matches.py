from __future__ import annotations

from pathlib import Path
import json
import shutil
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

RAW_JSON_PATH = ROOT / "data" / "raw" / "api_matches.json"
MATCHES_CSV_PATH = ROOT / "data" / "raw" / "matches.csv"
BACKUP_CSV_PATH = ROOT / "data" / "raw" / "matches_before_country_backup.csv"


def load_api_entries(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"No existe el JSON bruto: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and isinstance(data.get("response"), list):
        return data["response"]

    if isinstance(data, list):
        return data

    raise ValueError("No reconozco la estructura de api_matches.json")


def safe_get_fixture_id(item: dict):
    if isinstance(item.get("fixture"), dict):
        return item["fixture"].get("id")

    for key in ["fixture_id", "id"]:
        if key in item:
            return item.get(key)

    return None


def safe_get_league_country(item: dict) -> str:
    if isinstance(item.get("league"), dict):
        country = item["league"].get("country")
        if country:
            return str(country).strip()

    for key in ["country", "league_country", "country_name"]:
        if item.get(key):
            return str(item.get(key)).strip()

    return ""


def safe_get_league_name(item: dict) -> str:
    if isinstance(item.get("league"), dict):
        name = item["league"].get("name")
        if name:
            return str(name).strip()

    for key in ["league", "league_name"]:
        if item.get(key):
            return str(item.get(key)).strip()

    return ""


def main() -> None:
    if not MATCHES_CSV_PATH.exists():
        raise FileNotFoundError(f"No existe matches.csv: {MATCHES_CSV_PATH}")

    entries = load_api_entries(RAW_JSON_PATH)

    fixture_to_country = {}
    fixture_to_league_name = {}

    for item in entries:
        fixture_id = safe_get_fixture_id(item)
        if fixture_id is None:
            continue

        fixture_id = str(fixture_id)
        country = safe_get_league_country(item)
        league_name = safe_get_league_name(item)

        fixture_to_country[fixture_id] = country
        fixture_to_league_name[fixture_id] = league_name

    df = pd.read_csv(MATCHES_CSV_PATH)

    if "fixture_id" not in df.columns:
        raise ValueError("matches.csv no tiene columna fixture_id")

    if not BACKUP_CSV_PATH.exists():
        shutil.copy2(MATCHES_CSV_PATH, BACKUP_CSV_PATH)

    df["fixture_id_str"] = df["fixture_id"].astype(str)

    df["country"] = df["fixture_id_str"].map(fixture_to_country).fillna("")

    # Opcional defensivo: si el nombre de liga del CSV viniera vacío, lo rellenamos desde el JSON.
    if "league" in df.columns:
        empty_league_mask = df["league"].isna() | (df["league"].astype(str).str.strip() == "")
        df.loc[empty_league_mask, "league"] = df.loc[empty_league_mask, "fixture_id_str"].map(fixture_to_league_name)

    df = df.drop(columns=["fixture_id_str"])

    df.to_csv(MATCHES_CSV_PATH, index=False)

    total = len(df)
    with_country = int((df["country"].astype(str).str.strip() != "").sum())
    without_country = total - with_country

    print("\n=== COUNTRY AÑADIDO A matches.csv ===")
    print(f"Partidos totales: {total}")
    print(f"Con country detectado: {with_country}")
    print(f"Sin country detectado: {without_country}")
    print(f"Backup creado en: {BACKUP_CSV_PATH}")
    print(f"CSV actualizado: {MATCHES_CSV_PATH}")

    print("\nPrimeras filas con country:")
    cols = ["date", "country", "league", "fixture_id", "home_team", "away_team", "status"]
    existing_cols = [c for c in cols if c in df.columns]
    print(df[existing_cols].head(25).to_string(index=False))

    print("\nResumen por country:")
    print(df["country"].value_counts(dropna=False).head(30).to_string())


if __name__ == "__main__":
    main()
