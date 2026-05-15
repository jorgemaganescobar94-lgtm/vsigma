from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
import os
import shutil
import time
import requests
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_recent_form_backup.csv"
CACHE_PATH = ROOT / "data" / "raw" / "team_recent_fixtures_cache.json"

API_BASE = "https://v3.football.api-sports.io"
LAST_N = 8

# Plan gratis API-Football: normalmente solo permite 2022-2024.
FREE_PLAN_ALLOWED_SEASONS = [2024, 2023, 2022]

# De momento enriquecemos solo TIER_1/TIER_2 para no gastar llamadas.
MAX_TIER_RANK_TO_ENRICH = 2


def load_env_file() -> None:
    env_path = ROOT / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def get_api_key() -> str:
    load_env_file()

    candidates = [
        "API_FOOTBALL_KEY",
        "APIFOOTBALL_KEY",
        "API_SPORTS_KEY",
        "APISPORTS_KEY",
        "RAPIDAPI_KEY",
        "X_RAPIDAPI_KEY",
    ]

    for name in candidates:
        value = os.environ.get(name)
        if value:
            return value.strip()

    raise RuntimeError(
        "No encuentro API key. Crea un archivo .env en C:\\vsigma con:\n"
        "API_FOOTBALL_KEY=TU_API_KEY_AQUI"
    )


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def api_get(path: str, params: dict, api_key: str) -> dict:
    url = f"{API_BASE}{path}"
    headers = {"x-apisports-key": api_key}

    response = requests.get(url, headers=headers, params=params, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"Error API {response.status_code}: {response.text[:500]}")

    return response.json()


def has_plan_error(data: dict) -> bool:
    errors = data.get("errors")

    if not errors:
        return False

    txt = str(errors).lower()
    return "free plans do not have access" in txt or "plan" in txt


def get_recent_team_fixtures_freeplan(
    team_id: int,
    league_id: int,
    original_season: int,
    api_key: str,
    cache: dict,
) -> tuple[list[dict], int | None, str]:
    """
    Intenta enriquecer con:
    1) temporada original si está permitida
    2) fallback 2024, 2023, 2022

    Devuelve:
    fixtures, season_used, source_mode
    """

    seasons_to_try = []

    if original_season in FREE_PLAN_ALLOWED_SEASONS:
        seasons_to_try.append(original_season)

    for s in FREE_PLAN_ALLOWED_SEASONS:
        if s not in seasons_to_try:
            seasons_to_try.append(s)

    for season in seasons_to_try:
        cache_key = f"team={team_id}|league={league_id}|season={season}|last={LAST_N}"

        if cache_key in cache:
            cached = cache[cache_key]
            return cached, season, "CACHE_FREEPLAN_HISTORICAL_PRIOR"

        params = {
            "team": team_id,
            "league": league_id,
            "season": season,
            "last": LAST_N,
        }

        data = api_get("/fixtures", params, api_key)

        if has_plan_error(data):
            print(f"PLAN_LIMIT team={team_id} league={league_id} season={season}")
            continue

        fixtures = data.get("response", [])

        # Solo cacheamos respuestas válidas.
        cache[cache_key] = fixtures
        save_cache(cache)

        time.sleep(0.35)

        if fixtures:
            return fixtures, season, "API_FREEPLAN_HISTORICAL_PRIOR"

    return [], None, "NO_AVAILABLE_FREEPLAN_DATA"


def fixture_is_finished(fixture: dict) -> bool:
    status = fixture.get("fixture", {}).get("status", {}).get("short")
    return status in {"FT", "AET", "PEN"}


def calc_team_recent_stats(fixtures: list[dict], team_id: int) -> dict:
    rows = []

    for item in fixtures:
        if not fixture_is_finished(item):
            continue

        teams = item.get("teams", {})
        goals = item.get("goals", {})

        home = teams.get("home", {})
        away = teams.get("away", {})

        home_id = home.get("id")
        away_id = away.get("id")

        home_goals = goals.get("home")
        away_goals = goals.get("away")

        if home_goals is None or away_goals is None:
            continue

        if team_id == home_id:
            gf = int(home_goals)
            ga = int(away_goals)
        elif team_id == away_id:
            gf = int(away_goals)
            ga = int(home_goals)
        else:
            continue

        if gf > ga:
            pts = 3
        elif gf == ga:
            pts = 1
        else:
            pts = 0

        rows.append({
            "gf": gf,
            "ga": ga,
            "pts": pts,
            "scored": 1 if gf > 0 else 0,
            "clean_sheet": 1 if ga == 0 else 0,
            "btts": 1 if gf > 0 and ga > 0 else 0,
            "over15": 1 if gf + ga >= 2 else 0,
            "over25": 1 if gf + ga >= 3 else 0,
        })

    n = len(rows)

    if n == 0:
        return {
            "recent_matches": 0,
            "form_pts": np.nan,
            "goals_for_pg": np.nan,
            "goals_against_pg": np.nan,
            "scored_rate": np.nan,
            "clean_sheet_rate": np.nan,
            "btts_rate": np.nan,
            "over15_rate": np.nan,
            "over25_rate": np.nan,
        }

    df = pd.DataFrame(rows)

    return {
        "recent_matches": n,
        "form_pts": round(float(df["pts"].mean()), 3),
        "goals_for_pg": round(float(df["gf"].mean()), 3),
        "goals_against_pg": round(float(df["ga"].mean()), 3),
        "scored_rate": round(float(df["scored"].mean()), 3),
        "clean_sheet_rate": round(float(df["clean_sheet"].mean()), 3),
        "btts_rate": round(float(df["btts"].mean()), 3),
        "over15_rate": round(float(df["over15"].mean()), 3),
        "over25_rate": round(float(df["over25"].mean()), 3),
    }


def apply_stats_to_row(df: pd.DataFrame, idx, side: str, stats: dict) -> None:
    prefix = side

    df.loc[idx, f"{prefix}_form_pts"] = stats["form_pts"]
    df.loc[idx, f"{prefix}_scored_rate"] = stats["scored_rate"]
    df.loc[idx, f"{prefix}_clean_sheet_rate"] = stats["clean_sheet_rate"]

    df.loc[idx, f"{prefix}_recent_matches"] = stats["recent_matches"]
    df.loc[idx, f"{prefix}_goals_for_pg"] = stats["goals_for_pg"]
    df.loc[idx, f"{prefix}_goals_against_pg"] = stats["goals_against_pg"]
    df.loc[idx, f"{prefix}_btts_rate"] = stats["btts_rate"]
    df.loc[idx, f"{prefix}_over15_rate"] = stats["over15_rate"]
    df.loc[idx, f"{prefix}_over25_rate"] = stats["over25_rate"]


def main() -> None:
    api_key = get_api_key()

    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES}")

    if not FILTERED_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {FILTERED_MATCHES}. Ejecuta antes filter_leagues.py")

    raw = pd.read_csv(RAW_MATCHES)
    filtered = pd.read_csv(FILTERED_MATCHES)

    if not BACKUP_MATCHES.exists():
        shutil.copy2(RAW_MATCHES, BACKUP_MATCHES)

    required = [
        "fixture_id",
        "league_id",
        "season",
        "home_team_id",
        "away_team_id",
        "league_tier_rank",
    ]

    missing = [c for c in required if c not in filtered.columns]

    if missing:
        raise ValueError(f"Faltan columnas en matches_league_filtered.csv: {missing}")

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= MAX_TIER_RANK_TO_ENRICH
    ].copy()

    print("\n=== ENRIQUECIMIENTO RECENT FORM FREE PLAN ===")
    print(f"Partidos filtrados totales: {len(filtered)}")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")
    print(f"Últimos partidos por equipo: {LAST_N}")
    print(f"Temporadas fallback: {FREE_PLAN_ALLOWED_SEASONS}")

    cache = load_cache()

    enriched_fixtures = 0
    partial_fixtures = 0
    failed = 0

    for _, match in targets.iterrows():
        fixture_id = match["fixture_id"]

        league_id = int(match["league_id"])
        original_season = int(match["season"])

        home_team_id = int(match["home_team_id"])
        away_team_id = int(match["away_team_id"])

        raw_idx_list = raw.index[raw["fixture_id"] == fixture_id].tolist()

        if not raw_idx_list:
            continue

        raw_idx = raw_idx_list[0]

        try:
            home_fixtures, home_season_used, home_mode = get_recent_team_fixtures_freeplan(
                home_team_id,
                league_id,
                original_season,
                api_key,
                cache,
            )

            away_fixtures, away_season_used, away_mode = get_recent_team_fixtures_freeplan(
                away_team_id,
                league_id,
                original_season,
                api_key,
                cache,
            )

            home_stats = calc_team_recent_stats(home_fixtures, home_team_id)
            away_stats = calc_team_recent_stats(away_fixtures, away_team_id)

            apply_stats_to_row(raw, raw_idx, "home", home_stats)
            apply_stats_to_row(raw, raw_idx, "away", away_stats)

            raw.loc[raw_idx, "home_stats_season_used"] = home_season_used
            raw.loc[raw_idx, "away_stats_season_used"] = away_season_used
            raw.loc[raw_idx, "data_enrichment_source"] = f"{home_mode}|{away_mode}"
            raw.loc[raw_idx, "data_enrichment_updated_at"] = datetime.now(timezone.utc).isoformat()

            if home_stats["recent_matches"] > 0 and away_stats["recent_matches"] > 0:
                raw.loc[raw_idx, "data_enrichment_level"] = f"HISTORICAL_PRIOR_LAST_{LAST_N}"
                enriched_fixtures += 1
                status = "OK"
            elif home_stats["recent_matches"] > 0 or away_stats["recent_matches"] > 0:
                raw.loc[raw_idx, "data_enrichment_level"] = f"PARTIAL_HISTORICAL_PRIOR_LAST_{LAST_N}"
                partial_fixtures += 1
                status = "PARTIAL"
            else:
                raw.loc[raw_idx, "data_enrichment_level"] = "NO_AVAILABLE_FREEPLAN_DATA"
                status = "NO_DATA"

            print(
                f"{status} {fixture_id}: {match['home_team']} vs {match['away_team']} | "
                f"home_n={home_stats['recent_matches']} home_season={home_season_used} | "
                f"away_n={away_stats['recent_matches']} away_season={away_season_used}"
            )

        except Exception as e:
            failed += 1
            raw.loc[raw_idx, "data_enrichment_level"] = "ENRICHMENT_ERROR"
            raw.loc[raw_idx, "data_enrichment_error"] = str(e)
            print(f"ERROR {fixture_id}: {match['home_team']} vs {match['away_team']} -> {e}")

    raw.to_csv(RAW_MATCHES, index=False)
    save_cache(cache)

    print("\n=== ENRIQUECIMIENTO COMPLETADO ===")
    print(f"Partidos enriquecidos completos: {enriched_fixtures}")
    print(f"Partidos parciales: {partial_fixtures}")
    print(f"Fallos: {failed}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")
    print(f"Cache: {CACHE_PATH}")

    cols = [
        "date", "country", "league", "home_team", "away_team",
        "home_form_pts", "away_form_pts",
        "home_scored_rate", "away_scored_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_goals_for_pg", "away_goals_for_pg",
        "home_goals_against_pg", "away_goals_against_pg",
        "home_stats_season_used", "away_stats_season_used",
        "data_enrichment_level",
    ]

    existing = [c for c in cols if c in raw.columns]
    enriched_rows = raw[
        raw.get("data_enrichment_level", "").astype(str).str.contains("PRIOR|PARTIAL|NO_AVAILABLE", na=False)
    ]

    print("\nFilas procesadas:")
    if not enriched_rows.empty:
        print(enriched_rows[existing].head(30).to_string(index=False))
    else:
        print("No hay filas procesadas.")


if __name__ == "__main__":
    main()
