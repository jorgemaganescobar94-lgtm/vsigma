from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import shutil
import pandas as pd
import numpy as np

from api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_recent_form_v2_backup.csv"
CACHE_PATH = ROOT / "data" / "raw" / "team_recent_fixtures_cache_v2.json"

LAST_N = 8
PULL_N = 15
TARGET_MAX_TIER_RANK = 2
MIN_MATCHES_FULL = 4
MIN_MATCHES_PARTIAL = 3


FINISHED_STATUSES = {"FT", "AET", "PEN"}


def load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_int(x):
    try:
        return int(float(x))
    except Exception:
        return None


def parse_dt(x) -> datetime | None:
    try:
        return pd.to_datetime(x, utc=True).to_pydatetime()
    except Exception:
        return None


def fixture_finished(item: dict) -> bool:
    try:
        short = item.get("fixture", {}).get("status", {}).get("short")
        return short in FINISHED_STATUSES
    except Exception:
        return False


def fetch_team_recent_fixtures(
    client: APIFootballClient,
    cache: dict,
    team_id: int,
    season: int,
    before_dt: datetime | None = None,
) -> list[dict]:
    cache_key = f"{team_id}|{season}"

    if cache_key in cache:
        fixtures = cache[cache_key]
    else:
        payload = client.request(
            "/fixtures",
            params={
                "team": team_id,
                "season": season,
                "last": PULL_N,
            },
            ttl_hours=6,
        )
        fixtures = payload.get("response", [])
        cache[cache_key] = fixtures

    filtered = []
    for item in fixtures:
        if not fixture_finished(item):
            continue

        fdt = parse_dt(item.get("fixture", {}).get("date"))
        if before_dt is not None and fdt is not None and fdt >= before_dt:
            continue

        filtered.append(item)

    filtered = sorted(
        filtered,
        key=lambda x: x.get("fixture", {}).get("timestamp", 0),
        reverse=True,
    )

    return filtered[:LAST_N]


def compute_team_metrics(fixtures: list[dict], team_id: int) -> dict:
    if not fixtures:
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

    pts = []
    gf = []
    ga = []
    scored = []
    clean = []
    btts = []
    over15 = []
    over25 = []

    for item in fixtures:
        home_id = item.get("teams", {}).get("home", {}).get("id")
        away_id = item.get("teams", {}).get("away", {}).get("id")
        g_home = item.get("goals", {}).get("home")
        g_away = item.get("goals", {}).get("away")

        if g_home is None or g_away is None:
            continue

        if team_id == home_id:
            team_gf = g_home
            team_ga = g_away
        elif team_id == away_id:
            team_gf = g_away
            team_ga = g_home
        else:
            continue

        gf.append(team_gf)
        ga.append(team_ga)
        scored.append(1 if team_gf > 0 else 0)
        clean.append(1 if team_ga == 0 else 0)
        btts.append(1 if (team_gf > 0 and team_ga > 0) else 0)

        total_goals = team_gf + team_ga
        over15.append(1 if total_goals >= 2 else 0)
        over25.append(1 if total_goals >= 3 else 0)

        if team_gf > team_ga:
            pts.append(3)
        elif team_gf == team_ga:
            pts.append(1)
        else:
            pts.append(0)

    n = len(gf)
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

    return {
        "recent_matches": n,
        "form_pts": round(float(np.mean(pts)), 3),
        "goals_for_pg": round(float(np.mean(gf)), 3),
        "goals_against_pg": round(float(np.mean(ga)), 3),
        "scored_rate": round(float(np.mean(scored)), 3),
        "clean_sheet_rate": round(float(np.mean(clean)), 3),
        "btts_rate": round(float(np.mean(btts)), 3),
        "over15_rate": round(float(np.mean(over15)), 3),
        "over25_rate": round(float(np.mean(over25)), 3),
    }


def pick_best_season_bundle(
    client: APIFootballClient,
    cache: dict,
    team_id: int,
    preferred_seasons: list[int],
    before_dt: datetime | None,
) -> tuple[list[dict], int | None]:
    seen = set()

    for season in preferred_seasons:
        if season in seen or season is None:
            continue
        seen.add(season)

        try:
            fixtures = fetch_team_recent_fixtures(
                client=client,
                cache=cache,
                team_id=team_id,
                season=season,
                before_dt=before_dt,
            )
        except APIFootballError:
            continue
        except Exception:
            continue

        if len(fixtures) >= MIN_MATCHES_PARTIAL:
            return fixtures, season

    return [], None


def main() -> None:
    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES}")
    if not FILTERED_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {FILTERED_MATCHES}")

    raw = pd.read_csv(RAW_MATCHES)
    filtered = pd.read_csv(FILTERED_MATCHES)

    if not BACKUP_MATCHES.exists():
        shutil.copy2(RAW_MATCHES, BACKUP_MATCHES)

    client = APIFootballClient()
    cache = load_cache()

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= TARGET_MAX_TIER_RANK
    ].copy()

    print("\n=== ENRIQUECIMIENTO RECENT FORM v2 ===")
    print(f"Partidos filtrados totales: {len(filtered)}")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")
    print(f"Últimos partidos por equipo: {LAST_N}")
    print("Modo: TEAM + SEASON (sin filtrar por league)")

    ok_full = 0
    ok_partial = 0
    no_data = 0
    errors = 0

    for _, match in targets.iterrows():
        fixture_id = match["fixture_id"]
        raw_idx_list = raw.index[raw["fixture_id"] == fixture_id].tolist()
        if not raw_idx_list:
            continue
        raw_idx = raw_idx_list[0]

        home_team_id = safe_int(match.get("home_team_id"))
        away_team_id = safe_int(match.get("away_team_id"))
        season = safe_int(match.get("season"))
        match_dt = parse_dt(match.get("date"))

        season_fallbacks = []
        if season is not None:
            season_fallbacks.extend([season, season - 1, season - 2])
        season_fallbacks.extend([2026, 2025, 2024])

        try:
            home_fixtures, home_season_used = pick_best_season_bundle(
                client, cache, home_team_id, season_fallbacks, match_dt
            )
            away_fixtures, away_season_used = pick_best_season_bundle(
                client, cache, away_team_id, season_fallbacks, match_dt
            )

            home_metrics = compute_team_metrics(home_fixtures, home_team_id)
            away_metrics = compute_team_metrics(away_fixtures, away_team_id)

            raw.loc[raw_idx, "home_recent_matches"] = home_metrics["recent_matches"]
            raw.loc[raw_idx, "away_recent_matches"] = away_metrics["recent_matches"]

            raw.loc[raw_idx, "home_form_pts"] = home_metrics["form_pts"]
            raw.loc[raw_idx, "away_form_pts"] = away_metrics["form_pts"]

            raw.loc[raw_idx, "home_goals_for_pg"] = home_metrics["goals_for_pg"]
            raw.loc[raw_idx, "away_goals_for_pg"] = away_metrics["goals_for_pg"]

            raw.loc[raw_idx, "home_goals_against_pg"] = home_metrics["goals_against_pg"]
            raw.loc[raw_idx, "away_goals_against_pg"] = away_metrics["goals_against_pg"]

            raw.loc[raw_idx, "home_scored_rate"] = home_metrics["scored_rate"]
            raw.loc[raw_idx, "away_scored_rate"] = away_metrics["scored_rate"]

            raw.loc[raw_idx, "home_clean_sheet_rate"] = home_metrics["clean_sheet_rate"]
            raw.loc[raw_idx, "away_clean_sheet_rate"] = away_metrics["clean_sheet_rate"]

            raw.loc[raw_idx, "home_btts_rate"] = home_metrics["btts_rate"]
            raw.loc[raw_idx, "away_btts_rate"] = away_metrics["btts_rate"]

            raw.loc[raw_idx, "home_over15_rate"] = home_metrics["over15_rate"]
            raw.loc[raw_idx, "away_over15_rate"] = away_metrics["over15_rate"]

            raw.loc[raw_idx, "home_over25_rate"] = home_metrics["over25_rate"]
            raw.loc[raw_idx, "away_over25_rate"] = away_metrics["over25_rate"]

            raw.loc[raw_idx, "home_stats_season_used"] = home_season_used
            raw.loc[raw_idx, "away_stats_season_used"] = away_season_used

            home_n = home_metrics["recent_matches"]
            away_n = away_metrics["recent_matches"]

            if home_n >= MIN_MATCHES_FULL and away_n >= MIN_MATCHES_FULL:
                level = "TEAM_LAST_8_ALL_COMPETITIONS"
                ok_full += 1
                tag = "OK"
            elif home_n >= MIN_MATCHES_PARTIAL or away_n >= MIN_MATCHES_PARTIAL:
                level = "PARTIAL_TEAM_LAST_8_ALL_COMPETITIONS"
                ok_partial += 1
                tag = "PARTIAL"
            else:
                level = "NO_AVAILABLE_TEAM_FORM_DATA"
                no_data += 1
                tag = "NO_DATA"

            raw.loc[raw_idx, "data_enrichment_level"] = level

            print(
                f"{tag} {fixture_id}: {match['home_team']} vs {match['away_team']} | "
                f"home_n={home_n} home_season={home_season_used} | "
                f"away_n={away_n} away_season={away_season_used}"
            )

        except Exception as e:
            raw.loc[raw_idx, "data_enrichment_level"] = "ERROR_TEAM_FORM_ENRICH"
            raw.loc[raw_idx, "recent_form_error"] = str(e)
            errors += 1
            print(f"ERROR {fixture_id}: {match['home_team']} vs {match['away_team']} -> {e}")

    raw.to_csv(RAW_MATCHES, index=False)
    save_cache(cache)

    print("\n=== ENRIQUECIMIENTO COMPLETADO ===")
    print(f"Partidos enriquecidos completos: {ok_full}")
    print(f"Partidos parciales: {ok_partial}")
    print(f"Sin datos: {no_data}")
    print(f"Fallos: {errors}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")
    print(f"Cache: {CACHE_PATH}")


if __name__ == "__main__":
    main()