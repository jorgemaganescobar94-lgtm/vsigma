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
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_tie_context_backup.csv"
CACHE_PATH = ROOT / "data" / "raw" / "tie_context_cache.json"

TWO_LEG_LEAGUES = {
    "uefa europa league",
    "uefa europa conference league",
    "uefa champions league",
    "conmebol libertadores",
    "conmebol sudamericana",
}


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
        if pd.isna(x):
            return None
        return int(float(x))
    except Exception:
        return None


def parse_dt(x):
    try:
        return pd.to_datetime(x, utc=True).to_pydatetime()
    except Exception:
        return None


def norm(s: str) -> str:
    return str(s).strip().lower()


def get_h2h_fixtures(client: APIFootballClient, cache: dict, home_team_id: int, away_team_id: int) -> list[dict]:
    a, b = sorted([int(home_team_id), int(away_team_id)])
    key = f"{a}-{b}"
    if key in cache:
        return cache[key]

    payload = client.request(
        "/fixtures/headtohead",
        params={"h2h": f"{a}-{b}", "last": 10},
        ttl_hours=12,
    )
    fixtures = payload.get("response", [])
    cache[key] = fixtures
    return fixtures


def find_first_leg(
    fixtures: list[dict],
    current_fixture_id: int,
    current_league_id: int | None,
    current_season: int | None,
    current_dt: datetime | None,
) -> dict | None:
    candidates = []

    for item in fixtures:
        fixture_id = safe_int(item.get("fixture", {}).get("id"))
        league_id = safe_int(item.get("league", {}).get("id"))
        season = safe_int(item.get("league", {}).get("season"))
        dt = parse_dt(item.get("fixture", {}).get("date"))

        if fixture_id == current_fixture_id:
            continue
        if current_league_id is not None and league_id != current_league_id:
            continue
        if current_season is not None and season != current_season:
            continue
        if current_dt is not None and dt is not None and dt >= current_dt:
            continue

        candidates.append(item)

    if not candidates:
        return None

    candidates = sorted(
        candidates,
        key=lambda x: x.get("fixture", {}).get("timestamp", 0),
        reverse=True,
    )
    return candidates[0]


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

    targets = filtered[filtered["league"].astype(str).str.lower().isin(TWO_LEG_LEAGUES)].copy()

    print("\n=== ENRIQUECIMIENTO TIE CONTEXT ===")
    print(f"Partidos objetivo eliminatoria ida/vuelta: {len(targets)}")

    ok = 0
    no_first_leg = 0
    errors = 0

    for _, row in targets.iterrows():
        fixture_id = safe_int(row.get("fixture_id"))
        league_id = safe_int(row.get("league_id"))
        season = safe_int(row.get("season"))
        home_team_id = safe_int(row.get("home_team_id"))
        away_team_id = safe_int(row.get("away_team_id"))
        league_name = str(row.get("league", ""))
        match_dt = parse_dt(row.get("date"))

        idxs = raw.index[raw["fixture_id"] == fixture_id].tolist()
        if not idxs:
            continue
        raw_idx = idxs[0]

        raw.loc[raw_idx, "is_two_leg_tie"] = 1
        raw.loc[raw_idx, "tie_context_status"] = "INIT"

        try:
            h2h = get_h2h_fixtures(client, cache, home_team_id, away_team_id)
            first_leg = find_first_leg(
                fixtures=h2h,
                current_fixture_id=fixture_id,
                current_league_id=league_id,
                current_season=season,
                current_dt=match_dt,
            )

            if first_leg is None:
                raw.loc[raw_idx, "tie_context_status"] = "NO_FIRST_LEG_FOUND"
                no_first_leg += 1
                print(f"NO_FIRST_LEG {fixture_id}: {row['home_team']} vs {row['away_team']}")
                continue

            fl_home_id = safe_int(first_leg.get("teams", {}).get("home", {}).get("id"))
            fl_away_id = safe_int(first_leg.get("teams", {}).get("away", {}).get("id"))
            fl_home_goals = safe_int(first_leg.get("goals", {}).get("home"))
            fl_away_goals = safe_int(first_leg.get("goals", {}).get("away"))
            fl_fixture_id = safe_int(first_leg.get("fixture", {}).get("id"))

            if fl_home_goals is None or fl_away_goals is None:
                raw.loc[raw_idx, "tie_context_status"] = "FIRST_LEG_NO_SCORE"
                no_first_leg += 1
                print(f"NO_SCORE {fixture_id}: {row['home_team']} vs {row['away_team']}")
                continue

            # Aggregate BEFORE second leg, from current home/away perspective
            if home_team_id == fl_home_id:
                tie_home_agg_before = fl_home_goals
                tie_away_agg_before = fl_away_goals
            elif home_team_id == fl_away_id:
                tie_home_agg_before = fl_away_goals
                tie_away_agg_before = fl_home_goals
            else:
                raw.loc[raw_idx, "tie_context_status"] = "TEAM_MAPPING_ERROR"
                errors += 1
                print(f"MAPPING_ERROR {fixture_id}: {row['home_team']} vs {row['away_team']}")
                continue

            tie_home_delta = tie_home_agg_before - tie_away_agg_before
            tie_away_delta = tie_away_agg_before - tie_home_agg_before

            home_trailing = 1 if tie_home_delta < 0 else 0
            away_trailing = 1 if tie_away_delta < 0 else 0
            tie_level = 1 if tie_home_delta == 0 else 0

            raw.loc[raw_idx, "first_leg_fixture_id"] = fl_fixture_id
            raw.loc[raw_idx, "first_leg_home_goals"] = fl_home_goals
            raw.loc[raw_idx, "first_leg_away_goals"] = fl_away_goals
            raw.loc[raw_idx, "tie_home_agg_before"] = tie_home_agg_before
            raw.loc[raw_idx, "tie_away_agg_before"] = tie_away_agg_before
            raw.loc[raw_idx, "tie_home_delta"] = tie_home_delta
            raw.loc[raw_idx, "tie_away_delta"] = tie_away_delta
            raw.loc[raw_idx, "home_trailing_in_tie"] = home_trailing
            raw.loc[raw_idx, "away_trailing_in_tie"] = away_trailing
            raw.loc[raw_idx, "tie_level_before_second_leg"] = tie_level

            if home_trailing:
                label = "HOME_TRAILING"
            elif away_trailing:
                label = "AWAY_TRAILING"
            else:
                label = "LEVEL_TIE"

            raw.loc[raw_idx, "tie_state_label"] = label
            raw.loc[raw_idx, "tie_context_status"] = "OK"

            ok += 1
            print(
                f"OK {fixture_id}: {row['home_team']} vs {row['away_team']} | "
                f"first_leg={tie_home_agg_before}-{tie_away_agg_before} | state={label}"
            )

        except APIFootballError as e:
            raw.loc[raw_idx, "tie_context_status"] = "API_ERROR"
            raw.loc[raw_idx, "tie_context_error"] = str(e)
            errors += 1
            print(f"API_ERROR {fixture_id}: {row['home_team']} vs {row['away_team']} -> {e}")
        except Exception as e:
            raw.loc[raw_idx, "tie_context_status"] = "ERROR"
            raw.loc[raw_idx, "tie_context_error"] = str(e)
            errors += 1
            print(f"ERROR {fixture_id}: {row['home_team']} vs {row['away_team']} -> {e}")

    raw.to_csv(RAW_MATCHES, index=False)
    save_cache(cache)

    print("\n=== TIE CONTEXT COMPLETADO ===")
    print(f"OK: {ok}")
    print(f"NO_FIRST_LEG_FOUND: {no_first_leg}")
    print(f"ERRORS: {errors}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")
    print(f"Cache: {CACHE_PATH}")


if __name__ == "__main__":
    main()