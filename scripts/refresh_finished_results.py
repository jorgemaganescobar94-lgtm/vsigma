from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
import time
import os

import pandas as pd
import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
DEEP_ANALYSIS_CSV = ROOT / "data" / "processed" / "vsigma_deep_analysis_candidates.csv"

OUTPUT_REPORT_CSV = ROOT / "data" / "processed" / "refresh_finished_results_report.csv"
CACHE_JSON = ROOT / "data" / "cache" / "fixture_details_cache.json"

API_BASE = "https://api-football-v1.p.rapidapi.com/v3"
DEFAULT_SLEEP_SECONDS = 0.25


FINISHED_STATUSES = {"FT", "AET", "PEN"}
LIVE_OR_OPEN_STATUSES = {"NS", "TBD", "1H", "HT", "2H", "ET", "BT", "P", "SUSP", "INT", "LIVE"}


def load_env() -> tuple[str, str]:
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("API_FOOTBALL_KEY") or os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY")
    api_host = os.getenv("API_FOOTBALL_HOST", "api-football-v1.p.rapidapi.com")

    if not api_key:
        raise RuntimeError("No encontré API_FOOTBALL_KEY / RAPIDAPI_KEY en .env")

    return api_key, api_host


def api_get(endpoint: str, params: dict, api_key: str, api_host: str) -> dict:
    url = f"{API_BASE}/{endpoint}"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
    }

    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()

    data = r.json()
    if isinstance(data, dict) and data.get("errors"):
        raise RuntimeError(f"API devolvió errors en /{endpoint}: {data['errors']}")
    return data


def safe_num(value):
    try:
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def load_cache() -> dict:
    if CACHE_JSON.exists():
        try:
            return json.loads(CACHE_JSON.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_JSON.parent.mkdir(parents=True, exist_ok=True)
    CACHE_JSON.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def ensure_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def normalize_fixture_payload(item: dict) -> dict:
    fixture = item.get("fixture", {}) or {}
    league = item.get("league", {}) or {}
    teams = item.get("teams", {}) or {}
    goals = item.get("goals", {}) or {}
    score = item.get("score", {}) or {}

    status_obj = fixture.get("status", {}) or {}
    ft_obj = score.get("fulltime", {}) or {}
    ht_obj = score.get("halftime", {}) or {}
    et_obj = score.get("extratime", {}) or {}
    pen_obj = score.get("penalty", {}) or {}

    return {
        "fixture_id": fixture.get("id"),
        "fixture_date": fixture.get("date"),
        "fixture_timestamp": fixture.get("timestamp"),
        "status_long": status_obj.get("long"),
        "status_short": status_obj.get("short"),
        "status_elapsed": status_obj.get("elapsed"),
        "league_id": league.get("id"),
        "league_name": league.get("name"),
        "league_country": league.get("country"),
        "league_season": league.get("season"),
        "home_team_id": (teams.get("home") or {}).get("id"),
        "home_team_name": (teams.get("home") or {}).get("name"),
        "away_team_id": (teams.get("away") or {}).get("id"),
        "away_team_name": (teams.get("away") or {}).get("name"),
        "goals_home": goals.get("home"),
        "goals_away": goals.get("away"),
        "score_fulltime_home": ft_obj.get("home"),
        "score_fulltime_away": ft_obj.get("away"),
        "score_halftime_home": ht_obj.get("home"),
        "score_halftime_away": ht_obj.get("away"),
        "score_extratime_home": et_obj.get("home"),
        "score_extratime_away": et_obj.get("away"),
        "score_penalty_home": pen_obj.get("home"),
        "score_penalty_away": pen_obj.get("away"),
    }


def fetch_fixture_detail(fixture_id: int, api_key: str, api_host: str, cache: dict) -> dict:
    fixture_key = str(int(fixture_id))

    if fixture_key in cache:
        return cache[fixture_key]

    data = api_get("fixtures", {"id": int(fixture_id)}, api_key, api_host)
    response = data.get("response", []) or []
    if not response:
        raise RuntimeError(f"No encontré detalle para fixture_id={fixture_id}")

    normalized = normalize_fixture_payload(response[0])
    cache[fixture_key] = normalized
    return normalized


def main() -> None:
    if not RAW_MATCHES_CSV.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES_CSV}")
    if not DEEP_ANALYSIS_CSV.exists():
        raise FileNotFoundError(f"No existe: {DEEP_ANALYSIS_CSV}")

    api_key, api_host = load_env()

    raw = pd.read_csv(RAW_MATCHES_CSV)
    deep = pd.read_csv(DEEP_ANALYSIS_CSV)

    if deep.empty:
        print("No hay análisis profundo del que sacar fixture_id.")
        return

    raw = ensure_columns(
        raw,
        [
            "fixture_status_short",
            "fixture_status_long",
            "fixture_status_elapsed",
            "goals_home",
            "goals_away",
            "score_fulltime_home",
            "score_fulltime_away",
            "score_halftime_home",
            "score_halftime_away",
            "score_extratime_home",
            "score_extratime_away",
            "score_penalty_home",
            "score_penalty_away",
            "results_last_refresh_at",
        ],
    )

    fixture_ids = (
        deep["fixture_id"]
        .dropna()
        .astype(int)
        .drop_duplicates()
        .tolist()
    )

    cache = load_cache()
    report_rows = []

    print("\n=== REFRESH FINISHED RESULTS ===")
    print(f"Fixtures objetivo: {len(fixture_ids)}")

    for fixture_id in fixture_ids:
        try:
            detail = fetch_fixture_detail(fixture_id, api_key, api_host, cache)

            mask = raw["fixture_id"].astype("Int64") == int(fixture_id)
            if not mask.any():
                report_rows.append(
                    {
                        "fixture_id": fixture_id,
                        "result": "NOT_FOUND_IN_RAW",
                        "status_short": detail.get("status_short"),
                        "home_team": detail.get("home_team_name"),
                        "away_team": detail.get("away_team_name"),
                    }
                )
                print(f"NOT_FOUND_IN_RAW fixture={fixture_id}")
                continue

            raw.loc[mask, "fixture_status_short"] = detail.get("status_short")
            raw.loc[mask, "fixture_status_long"] = detail.get("status_long")
            raw.loc[mask, "fixture_status_elapsed"] = detail.get("status_elapsed")

            raw.loc[mask, "goals_home"] = detail.get("goals_home")
            raw.loc[mask, "goals_away"] = detail.get("goals_away")
            raw.loc[mask, "score_fulltime_home"] = detail.get("score_fulltime_home")
            raw.loc[mask, "score_fulltime_away"] = detail.get("score_fulltime_away")
            raw.loc[mask, "score_halftime_home"] = detail.get("score_halftime_home")
            raw.loc[mask, "score_halftime_away"] = detail.get("score_halftime_away")
            raw.loc[mask, "score_extratime_home"] = detail.get("score_extratime_home")
            raw.loc[mask, "score_extratime_away"] = detail.get("score_extratime_away")
            raw.loc[mask, "score_penalty_home"] = detail.get("score_penalty_home")
            raw.loc[mask, "score_penalty_away"] = detail.get("score_penalty_away")

            # Intentamos mantener también "status" si existe
            if "status" in raw.columns and detail.get("status_short"):
                raw.loc[mask, "status"] = detail.get("status_short")

            raw.loc[mask, "results_last_refresh_at"] = datetime.now(timezone.utc).isoformat()

            status_short = str(detail.get("status_short", "")).upper()
            result_label = "FINISHED" if status_short in FINISHED_STATUSES else "OPEN_OR_LIVE"

            report_rows.append(
                {
                    "fixture_id": fixture_id,
                    "result": result_label,
                    "status_short": status_short,
                    "home_team": detail.get("home_team_name"),
                    "away_team": detail.get("away_team_name"),
                    "goals_home": detail.get("goals_home"),
                    "goals_away": detail.get("goals_away"),
                    "score_fulltime_home": detail.get("score_fulltime_home"),
                    "score_fulltime_away": detail.get("score_fulltime_away"),
                }
            )

            print(
                f"OK fixture={fixture_id} "
                f"{detail.get('home_team_name')} vs {detail.get('away_team_name')} "
                f"| status={status_short} "
                f"| FT={detail.get('score_fulltime_home')}-{detail.get('score_fulltime_away')}"
            )

            save_cache(cache)
            time.sleep(DEFAULT_SLEEP_SECONDS)

        except Exception as e:
            report_rows.append(
                {
                    "fixture_id": fixture_id,
                    "result": "ERROR",
                    "note": str(e),
                }
            )
            print(f"ERROR fixture={fixture_id} -> {e}")

    raw.to_csv(RAW_MATCHES_CSV, index=False)

    report = pd.DataFrame(report_rows)
    OUTPUT_REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT_REPORT_CSV, index=False)

    save_cache(cache)

    print("\n=== REFRESH FINISHED RESULTS COMPLETADO ===")
    print(f"CSV actualizado: {RAW_MATCHES_CSV}")
    print(f"Reporte: {OUTPUT_REPORT_CSV}")

    if not report.empty:
        print("\nResumen:")
        print(report.to_string(index=False))


if __name__ == "__main__":
    main()