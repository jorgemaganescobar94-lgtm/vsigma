from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import shutil
import pandas as pd
import numpy as np

from api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_standings_context_backup.csv"

MAX_TIER_RANK_TO_ENRICH = 2


def flatten_standings_response(payload: dict) -> list[dict]:
    out = []

    for league_block in payload.get("response", []):
        league = league_block.get("league", {})
        standings_groups = league.get("standings", [])

        for group in standings_groups:
            for team_row in group:
                team = team_row.get("team", {})
                all_stats = team_row.get("all", {})

                out.append({
                    "league_id": league.get("id"),
                    "league_name": league.get("name"),
                    "season": league.get("season"),
                    "team_id": team.get("id"),
                    "team_name": team.get("name"),
                    "rank": team_row.get("rank"),
                    "points": team_row.get("points"),
                    "goals_diff": team_row.get("goalsDiff"),
                    "played": all_stats.get("played"),
                    "win": all_stats.get("win"),
                    "draw": all_stats.get("draw"),
                    "lose": all_stats.get("lose"),
                    "goals_for": (all_stats.get("goals") or {}).get("for"),
                    "goals_against": (all_stats.get("goals") or {}).get("against"),
                })

    return out


def compute_urgency(rank, n_teams):
    if pd.isna(rank) or pd.isna(n_teams):
        return np.nan

    rank = int(rank)
    n_teams = int(n_teams)

    if n_teams <= 0:
        return np.nan

    top_zone = max(2, round(n_teams * 0.15))
    bottom_zone = max(2, round(n_teams * 0.20))

    if rank <= top_zone:
        return 1.0

    if rank > n_teams - bottom_zone:
        return 1.0

    if rank <= top_zone + 2 or rank > n_teams - bottom_zone - 2:
        return 0.5

    return 0.0


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

    unique_leagues = (
        targets[["league_id", "season"]]
        .drop_duplicates()
        .sort_values(["league_id", "season"])
    )

    standings_map = {}
    league_sizes = {}

    print("\n=== ENRIQUECIMIENTO STANDINGS CONTEXT ===")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")
    print(f"Ligas únicas a consultar: {len(unique_leagues)}")

    for _, row in unique_leagues.iterrows():
        league_id = int(row["league_id"])
        season = int(row["season"])

        try:
            payload = client.standings(league=league_id, season=season)
            rows = flatten_standings_response(payload)

            if not rows:
                print(f"NO_DATA standings league={league_id} season={season}")
                continue

            df_st = pd.DataFrame(rows)

            n_teams = df_st["team_id"].nunique()
            league_sizes[(league_id, season)] = n_teams

            for _, st in df_st.iterrows():
                standings_map[(league_id, season, st["team_id"])] = st.to_dict()

            print(f"OK standings league={league_id} season={season} teams={n_teams}")

        except APIFootballError as e:
            print(f"API_ERROR standings league={league_id} season={season} -> {e}")
        except Exception as e:
            print(f"ERROR standings league={league_id} season={season} -> {e}")

    enriched = 0

    for _, match in targets.iterrows():
        fixture_id = match["fixture_id"]
        league_id = int(match["league_id"])
        season = int(match["season"])
        home_team_id = int(match["home_team_id"])
        away_team_id = int(match["away_team_id"])

        raw_idx_list = raw.index[raw["fixture_id"] == fixture_id].tolist()
        if not raw_idx_list:
            continue

        raw_idx = raw_idx_list[0]

        home_key = (league_id, season, home_team_id)
        away_key = (league_id, season, away_team_id)

        home_st = standings_map.get(home_key)
        away_st = standings_map.get(away_key)

        n_teams = league_sizes.get((league_id, season), np.nan)

        if home_st:
            raw.loc[raw_idx, "home_rank"] = home_st.get("rank")
            raw.loc[raw_idx, "home_points"] = home_st.get("points")
            raw.loc[raw_idx, "home_goals_diff"] = home_st.get("goals_diff")
            raw.loc[raw_idx, "home_played"] = home_st.get("played")
            raw.loc[raw_idx, "home_table_goals_for"] = home_st.get("goals_for")
            raw.loc[raw_idx, "home_table_goals_against"] = home_st.get("goals_against")
            raw.loc[raw_idx, "home_urgency_score"] = compute_urgency(home_st.get("rank"), n_teams)

        if away_st:
            raw.loc[raw_idx, "away_rank"] = away_st.get("rank")
            raw.loc[raw_idx, "away_points"] = away_st.get("points")
            raw.loc[raw_idx, "away_goals_diff"] = away_st.get("goals_diff")
            raw.loc[raw_idx, "away_played"] = away_st.get("played")
            raw.loc[raw_idx, "away_table_goals_for"] = away_st.get("goals_for")
            raw.loc[raw_idx, "away_table_goals_against"] = away_st.get("goals_against")
            raw.loc[raw_idx, "away_urgency_score"] = compute_urgency(away_st.get("rank"), n_teams)

        raw.loc[raw_idx, "league_team_count"] = n_teams
        raw.loc[raw_idx, "standings_context_updated_at"] = datetime.now(timezone.utc).isoformat()

        if home_st or away_st:
            enriched += 1

    raw.to_csv(RAW_MATCHES, index=False)

    print("\n=== STANDINGS CONTEXT COMPLETADO ===")
    print(f"Partidos enriquecidos con tabla: {enriched}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Backup: {BACKUP_MATCHES}")

    preview_cols = [
        "date", "country", "league", "home_team", "away_team",
        "home_rank", "away_rank",
        "home_points", "away_points",
        "home_goals_diff", "away_goals_diff",
        "home_urgency_score", "away_urgency_score",
    ]
    existing = [c for c in preview_cols if c in raw.columns]

    preview = raw[raw["fixture_id"].isin(targets["fixture_id"])].copy()

    print("\nVista previa standings context:")
    if not preview.empty:
        print(preview[existing].head(20).to_string(index=False))
    else:
        print("Vacío")


if __name__ == "__main__":
    main()