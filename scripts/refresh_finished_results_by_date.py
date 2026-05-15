from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
DEEP_ANALYSIS_CSV = ROOT / "data" / "processed" / "vsigma_deep_analysis_candidates.csv"
OUTPUT_REPORT_CSV = ROOT / "data" / "processed" / "refresh_finished_results_by_date_report.csv"

FINISHED_STATUSES = {"FT", "AET", "PEN"}

DIRECT_BASE = "https://v3.football.api-sports.io"
RAPID_BASE = "https://api-football-v1.p.rapidapi.com/v3"

SLEEP_BETWEEN_CALLS = 1.0
MAX_RETRIES = 4


def load_env() -> dict:
    load_dotenv(ROOT / ".env")

    env = {
        "apisports_key": os.getenv("API_FOOTBALL_KEY") or os.getenv("APISPORTS_KEY"),
        "rapidapi_key": os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY"),
        "rapidapi_host": os.getenv("API_FOOTBALL_HOST", "api-football-v1.p.rapidapi.com"),
        "timezone": os.getenv("API_FOOTBALL_TIMEZONE", "Atlantic/Canary"),
    }
    return env


def ensure_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        extra = pd.DataFrame({c: pd.NA for c in missing}, index=df.index)
        df = pd.concat([df, extra], axis=1)
    return df


def request_with_retry(
    url: str,
    headers: dict,
    params: dict,
    provider_name: str,
) -> dict:
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=headers, params=params, timeout=30)

            if r.status_code == 429:
                wait_s = min(2 ** attempt, 12)
                time.sleep(wait_s)
                last_error = RuntimeError(f"{provider_name}: 429 Too Many Requests")
                continue

            if r.status_code == 404:
                raise RuntimeError(f"{provider_name}: 404 Not Found -> {r.url}")

            r.raise_for_status()

            data = r.json()
            if isinstance(data, dict) and data.get("errors"):
                raise RuntimeError(f"{provider_name}: API errors -> {data['errors']}")

            return data

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(min(2 ** attempt, 8))
            else:
                break

    raise RuntimeError(str(last_error))


def api_get_fixtures_by_date(match_date: str, env: dict) -> tuple[dict, str]:
    params = {"date": match_date, "timezone": env["timezone"]}

    if env["apisports_key"]:
        url = f"{DIRECT_BASE}/fixtures"
        headers = {
            "x-apisports-key": env["apisports_key"],
        }
        try:
            data = request_with_retry(url, headers, params, "API-SPORTS_DIRECT")
            return data, "API-SPORTS_DIRECT"
        except Exception:
            pass

    if env["rapidapi_key"]:
        url = f"{RAPID_BASE}/fixtures"
        headers = {
            "x-rapidapi-key": env["rapidapi_key"],
            "x-rapidapi-host": env["rapidapi_host"],
        }
        data = request_with_retry(url, headers, params, "RAPIDAPI")
        return data, "RAPIDAPI"

    raise RuntimeError("No encontré credenciales válidas ni para API-SPORTS directo ni para RapidAPI")


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
        "fixture_status_short": status_obj.get("short"),
        "fixture_status_long": status_obj.get("long"),
        "fixture_status_elapsed": status_obj.get("elapsed"),
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


def fetch_fixtures_by_date(match_date: str, env: dict) -> tuple[pd.DataFrame, str]:
    data, provider_used = api_get_fixtures_by_date(match_date, env)
    response = data.get("response", []) or []

    rows = [normalize_fixture_payload(item) for item in response]
    if not rows:
        return pd.DataFrame(), provider_used

    return pd.DataFrame(rows), provider_used


def main() -> None:
    if not RAW_MATCHES_CSV.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES_CSV}")
    if not DEEP_ANALYSIS_CSV.exists():
        raise FileNotFoundError(f"No existe: {DEEP_ANALYSIS_CSV}")

    env = load_env()

    raw = pd.read_csv(RAW_MATCHES_CSV)
    deep = pd.read_csv(DEEP_ANALYSIS_CSV)

    if deep.empty:
        print("No hay análisis profundo.")
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

    text_cols = [
        "fixture_status_short",
        "fixture_status_long",
        "results_last_refresh_at",
    ]

    numeric_cols = [
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
    ]

    for col in text_cols:
        raw[col] = raw[col].astype("object")

    for col in numeric_cols:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")

    if "status" in raw.columns:
        raw["status"] = raw["status"].astype("object")

    target_fixture_ids = set(deep["fixture_id"].dropna().astype(int).tolist())
    target_dates = sorted(set(deep["date"].dropna().astype(str).tolist()))

    print("\n=== REFRESH FINISHED RESULTS BY DATE ===")
    print(f"Fechas objetivo: {target_dates}")
    print(f"Fixtures objetivo: {len(target_fixture_ids)}")

    report_rows = []
    fetched_by_date = []

    for match_date in target_dates:
        try:
            df_date, provider_used = fetch_fixtures_by_date(match_date, env)
            fetched_by_date.append(df_date)

            report_rows.append(
                {
                    "date": match_date,
                    "result": "OK",
                    "provider": provider_used,
                    "fixtures_returned": 0 if df_date.empty else len(df_date),
                }
            )

            print(f"OK date={match_date} provider={provider_used} fixtures={0 if df_date.empty else len(df_date)}")
            time.sleep(SLEEP_BETWEEN_CALLS)

        except Exception as e:
            report_rows.append(
                {
                    "date": match_date,
                    "result": "ERROR",
                    "note": str(e),
                }
            )
            print(f"ERROR date={match_date} -> {e}")

    if fetched_by_date:
        valid_frames = [x for x in fetched_by_date if not x.empty]
        fetched = pd.concat(valid_frames, ignore_index=True) if valid_frames else pd.DataFrame()
    else:
        fetched = pd.DataFrame()

    if fetched.empty:
        print("\nNo se descargaron fixtures por fecha.")
        report = pd.DataFrame(report_rows)
        report.to_csv(OUTPUT_REPORT_CSV, index=False)
        print(f"Reporte: {OUTPUT_REPORT_CSV}")
        return

    fetched = fetched.drop_duplicates(subset=["fixture_id"]).copy()
    fetched["fixture_id"] = fetched["fixture_id"].astype("Int64")

    matched = fetched[fetched["fixture_id"].isin(target_fixture_ids)].copy()

    print(f"\nFixtures encontrados por cruce de fixture_id: {len(matched)}")

    if matched.empty:
        report = pd.DataFrame(report_rows)
        report.to_csv(OUTPUT_REPORT_CSV, index=False)
        print("No hubo matches entre fixtures descargados y análisis profundo.")
        print(f"Reporte: {OUTPUT_REPORT_CSV}")
        return

    update_cols = [
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
    ]

    raw["fixture_id"] = raw["fixture_id"].astype("Int64")
    matched_idx = matched.set_index("fixture_id")

    updated_count = 0
    finished_count = 0
    now_iso = datetime.now(timezone.utc).isoformat()

    for idx, row in raw.iterrows():
        fixture_id = row["fixture_id"]
        if pd.isna(fixture_id) or fixture_id not in matched_idx.index:
            continue

        detail = matched_idx.loc[fixture_id]
        if isinstance(detail, pd.DataFrame):
            detail = detail.iloc[0]

        for col in update_cols:
            raw.loc[idx, col] = detail.get(col)

        status_short_val = detail.get("fixture_status_short")
        if "status" in raw.columns and pd.notna(status_short_val):
            raw.loc[idx, "status"] = status_short_val

        raw.loc[idx, "results_last_refresh_at"] = now_iso

        updated_count += 1
        if str(status_short_val).upper() in FINISHED_STATUSES:
            finished_count += 1

    raw.to_csv(RAW_MATCHES_CSV, index=False)

    detail_rows = []
    for _, row in matched.iterrows():
        detail_rows.append(
            {
                "date": row.get("fixture_date"),
                "fixture_id": row.get("fixture_id"),
                "result": "MATCHED",
                "status_short": row.get("fixture_status_short"),
                "home_team": row.get("home_team_name"),
                "away_team": row.get("away_team_name"),
                "score_fulltime_home": row.get("score_fulltime_home"),
                "score_fulltime_away": row.get("score_fulltime_away"),
            }
        )

    report = pd.concat(
        [
            pd.DataFrame(report_rows),
            pd.DataFrame(detail_rows),
        ],
        ignore_index=True,
        sort=False,
    )
    report.to_csv(OUTPUT_REPORT_CSV, index=False)

    print("\n=== REFRESH FINISHED RESULTS BY DATE COMPLETADO ===")
    print(f"CSV actualizado: {RAW_MATCHES_CSV}")
    print(f"Reporte: {OUTPUT_REPORT_CSV}")
    print(f"Actualizados: {updated_count}")
    print(f"Finalizados detectados: {finished_count}")

    print("\nDetalle fixtures cruzados:")
    print(pd.DataFrame(detail_rows).to_string(index=False))


if __name__ == "__main__":
    main()