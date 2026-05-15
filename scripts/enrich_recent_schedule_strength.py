from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import math
import shutil

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError
    from enrich_recent_fixture_statistics import (
        load_recent_fixtures_cache,
        pick_recent_fixture_bundle,
        safe_int,
        parse_dt,
        fixture_id,
    )
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError
    from scripts.enrich_recent_fixture_statistics import (
        load_recent_fixtures_cache,
        pick_recent_fixture_bundle,
        safe_int,
        parse_dt,
        fixture_id,
    )


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_recent_schedule_strength_backup.csv"
STANDINGS_CACHE = ROOT / "data" / "raw" / "recent_schedule_standings_cache.json"
OUTPUT_SUMMARY = ROOT / "data" / "processed" / "vsigma_schedule_strength_summary.csv"
OUTPUT_REPORT = ROOT / "data" / "processed" / "vsigma_schedule_strength_report.txt"

TARGET_MAX_TIER_RANK = 2
RECENT_WINDOW = 5


SCHEDULE_NUMERIC_COLS = [
    "home_recent_opponent_strength_avg",
    "away_recent_opponent_strength_avg",
    "home_recent_schedule_difficulty_score",
    "away_recent_schedule_difficulty_score",
    "recent_schedule_balance_delta",
    "home_recent_schedule_matches_used",
    "away_recent_schedule_matches_used",
]

SCHEDULE_TEXT_COLS = [
    "home_recent_schedule_quality_flag",
    "away_recent_schedule_quality_flag",
    "recent_schedule_strength_updated_at",
]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_float(value: Any) -> float:
    try:
        if value is None or pd.isna(value):
            return np.nan
        return float(value)
    except Exception:
        return np.nan


def clip(value: float, low: float, high: float) -> float:
    if pd.isna(value):
        return np.nan
    return max(low, min(high, float(value)))


def flatten_standings_response(payload: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for league_block in payload.get("response", []) or []:
        league = league_block.get("league") or {}
        for group in league.get("standings", []) or []:
            for team_row in group or []:
                team = team_row.get("team") or {}
                all_stats = team_row.get("all") or {}
                out.append(
                    {
                        "league_id": league.get("id"),
                        "league_name": league.get("name"),
                        "season": league.get("season"),
                        "team_id": team.get("id"),
                        "team_name": team.get("name"),
                        "rank": team_row.get("rank"),
                        "points": team_row.get("points"),
                        "goals_diff": team_row.get("goalsDiff"),
                        "played": all_stats.get("played"),
                    }
                )
    return out


def rank_strength(rank: Any, team_count: Any) -> float:
    rank_value = safe_float(rank)
    count_value = safe_float(team_count)
    if pd.isna(rank_value) or pd.isna(count_value) or count_value <= 1:
        return np.nan
    return clip(1.0 - ((rank_value - 1.0) / (count_value - 1.0)), 0.0, 1.0)


def points_per_game_strength(points: Any, played: Any) -> float:
    points_value = safe_float(points)
    played_value = safe_float(played)
    if pd.isna(points_value) or pd.isna(played_value) or played_value <= 0:
        return np.nan
    return clip((points_value / played_value) / 2.25, 0.0, 1.0)


def standing_team_strength(team_row: dict[str, Any] | None, team_count: int | None) -> float:
    if not team_row or not team_count:
        return np.nan
    rank_component = rank_strength(team_row.get("rank"), team_count)
    ppg_component = points_per_game_strength(team_row.get("points"), team_row.get("played"))
    values = []
    if not pd.isna(rank_component):
        values.append(("rank", rank_component, 0.70))
    if not pd.isna(ppg_component):
        values.append(("ppg", ppg_component, 0.30))
    if not values:
        return np.nan
    weight_total = sum(weight for _, _, weight in values)
    return round(sum(value * weight for _, value, weight in values) / weight_total, 3)


def fixture_league_season(item: dict[str, Any]) -> tuple[int | None, int | None]:
    league = item.get("league") or {}
    return safe_int(league.get("id")), safe_int(league.get("season"))


def opponent_id_for_fixture(item: dict[str, Any], team_id: int) -> int | None:
    teams = item.get("teams") or {}
    home_id = safe_int((teams.get("home") or {}).get("id"))
    away_id = safe_int((teams.get("away") or {}).get("id"))
    if team_id == home_id:
        return away_id
    if team_id == away_id:
        return home_id
    return None


def standings_key(league_id: int, season: int) -> str:
    return f"{league_id}|{season}"


def fetch_standings_bundle(
    client: APIFootballClient,
    cache: dict[str, Any],
    league_id: int | None,
    season: int | None,
    counters: dict[str, int],
) -> tuple[dict[int, dict[str, Any]], int | None]:
    if league_id is None or season is None:
        return {}, None

    key = standings_key(league_id, season)
    if key in cache:
        rows = cache[key]
        counters["standings_cache_hits"] += 1
    else:
        try:
            payload = client.standings(league=league_id, season=season)
            rows = flatten_standings_response(payload)
            cache[key] = rows
            counters["standings_api_calls"] += 1
        except APIFootballError:
            counters["standings_errors"] += 1
            return {}, None
        except Exception:
            counters["standings_errors"] += 1
            return {}, None

    if not rows:
        return {}, None
    frame = pd.DataFrame(rows)
    if frame.empty or "team_id" not in frame.columns:
        return {}, None

    team_count = int(frame["team_id"].nunique())
    out: dict[int, dict[str, Any]] = {}
    for _, row in frame.iterrows():
        team_id = safe_int(row.get("team_id"))
        if team_id is not None:
            out[team_id] = row.to_dict()
    return out, team_count


def schedule_quality_flag(used: int, requested: int) -> str:
    if used >= min(RECENT_WINDOW, requested) and used >= 4:
        return "FULL"
    if used >= 3:
        return "PARTIAL"
    if used > 0:
        return "SPARSE"
    return "UNKNOWN"


def compute_team_schedule_strength(
    client: APIFootballClient,
    standings_cache: dict[str, Any],
    fixtures: list[dict[str, Any]],
    team_id: int | None,
    counters: dict[str, int] | None = None,
) -> dict[str, Any]:
    counters = counters if counters is not None else {}
    counters.setdefault("standings_api_calls", 0)
    counters.setdefault("standings_cache_hits", 0)
    counters.setdefault("standings_errors", 0)

    selected = fixtures[:RECENT_WINDOW]
    requested = len(selected)
    strengths: list[float] = []

    if team_id is None or not selected:
        return {
            "recent_opponent_strength_avg": np.nan,
            "recent_schedule_difficulty_score": np.nan,
            "recent_schedule_matches_used": 0,
            "recent_schedule_quality_flag": "UNKNOWN",
        }

    for item in selected:
        opponent_id = opponent_id_for_fixture(item, int(team_id))
        league_id, season = fixture_league_season(item)
        standings, team_count = fetch_standings_bundle(
            client=client,
            cache=standings_cache,
            league_id=league_id,
            season=season,
            counters=counters,
        )
        strength = standing_team_strength(standings.get(opponent_id), team_count)
        if not pd.isna(strength):
            strengths.append(float(strength))

    used = len(strengths)
    avg = round(float(np.mean(strengths)), 3) if strengths else np.nan
    difficulty = round(clip((avg - 0.50) * 2.0, -1.0, 1.0), 3) if not pd.isna(avg) else np.nan
    return {
        "recent_opponent_strength_avg": avg,
        "recent_schedule_difficulty_score": difficulty,
        "recent_schedule_matches_used": used,
        "recent_schedule_quality_flag": schedule_quality_flag(used, requested),
    }


def ensure_output_columns(raw: pd.DataFrame) -> pd.DataFrame:
    for col in SCHEDULE_NUMERIC_COLS:
        if col not in raw.columns:
            raw[col] = np.nan
    for col in SCHEDULE_TEXT_COLS:
        if col not in raw.columns:
            raw[col] = ""
    return raw


def write_team_metrics(raw: pd.DataFrame, raw_idx: int, side: str, metrics: dict[str, Any]) -> None:
    for key, value in metrics.items():
        raw.loc[raw_idx, f"{side}_{key}"] = value


def build_summary(raw: pd.DataFrame, target_fixture_ids: set[int], counters: dict[str, int]) -> pd.DataFrame:
    target = raw[raw["fixture_id"].isin(target_fixture_ids)].copy() if target_fixture_ids else raw.iloc[0:0].copy()
    rows = [
        {
            "summary_scope": "overall",
            "rows_processed": int(len(target)),
            "home_full_or_partial": int(target.get("home_recent_schedule_quality_flag", pd.Series(dtype=str)).isin(["FULL", "PARTIAL"]).sum()),
            "away_full_or_partial": int(target.get("away_recent_schedule_quality_flag", pd.Series(dtype=str)).isin(["FULL", "PARTIAL"]).sum()),
            "avg_home_opponent_strength": round(pd.to_numeric(target.get("home_recent_opponent_strength_avg"), errors="coerce").mean(), 3) if not target.empty else np.nan,
            "avg_away_opponent_strength": round(pd.to_numeric(target.get("away_recent_opponent_strength_avg"), errors="coerce").mean(), 3) if not target.empty else np.nan,
            "standings_api_calls": counters.get("standings_api_calls", 0),
            "standings_cache_hits": counters.get("standings_cache_hits", 0),
            "standings_errors": counters.get("standings_errors", 0),
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    ]
    for side in ["home", "away"]:
        col = f"{side}_recent_schedule_quality_flag"
        if col in target.columns:
            counts = target[col].fillna("UNKNOWN").astype(str).value_counts()
            for flag, count in counts.items():
                rows.append({"summary_scope": f"{side}_quality_flag", "flag": flag, "rows": int(count)})
    return pd.DataFrame(rows)


def write_report(summary: pd.DataFrame, path: Path = OUTPUT_REPORT) -> None:
    lines = [
        "vSIGMA recent schedule-strength lab layer",
        "",
        "Purpose: adjust trust in recent form/process samples for opponent difficulty.",
        "Method: last five prior completed team fixtures; opponent strength from API standings rank plus points-per-game.",
        "Activation: neutral when standings context is missing; no hard vetoes.",
        "",
        summary.to_string(index=False) if not summary.empty else "No rows processed.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES}")
    if not FILTERED_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {FILTERED_MATCHES}")

    raw = pd.read_csv(RAW_MATCHES)
    filtered = pd.read_csv(FILTERED_MATCHES)
    if not BACKUP_MATCHES.exists():
        shutil.copy2(RAW_MATCHES, BACKUP_MATCHES)

    raw = ensure_output_columns(raw)
    recent_cache = load_recent_fixtures_cache()
    standings_cache = load_json(STANDINGS_CACHE)
    client = APIFootballClient()

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= TARGET_MAX_TIER_RANK
    ].copy()

    counters = {"standings_api_calls": 0, "standings_cache_hits": 0, "standings_errors": 0}
    target_fixture_ids: set[int] = set()

    print("\n=== RECENT SCHEDULE STRENGTH LAB ===")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")
    print(f"Ventana: ultimos {RECENT_WINDOW} fixtures completados por equipo")

    for _, match in targets.iterrows():
        current_fixture_id = safe_int(match.get("fixture_id"))
        if current_fixture_id is None:
            continue
        raw_idx_list = raw.index[raw["fixture_id"] == current_fixture_id].tolist()
        if not raw_idx_list:
            continue
        raw_idx = raw_idx_list[0]
        target_fixture_ids.add(current_fixture_id)

        season = safe_int(match.get("season"))
        match_dt = parse_dt(match.get("date"))
        home_team_id = safe_int(match.get("home_team_id"))
        away_team_id = safe_int(match.get("away_team_id"))

        home_fixtures = pick_recent_fixture_bundle(client, recent_cache, home_team_id, season, match_dt, current_fixture_id)
        away_fixtures = pick_recent_fixture_bundle(client, recent_cache, away_team_id, season, match_dt, current_fixture_id)

        home_metrics = compute_team_schedule_strength(client, standings_cache, home_fixtures, home_team_id, counters)
        away_metrics = compute_team_schedule_strength(client, standings_cache, away_fixtures, away_team_id, counters)

        write_team_metrics(raw, raw_idx, "home", home_metrics)
        write_team_metrics(raw, raw_idx, "away", away_metrics)
        raw.loc[raw_idx, "recent_schedule_balance_delta"] = (
            safe_float(home_metrics["recent_opponent_strength_avg"])
            - safe_float(away_metrics["recent_opponent_strength_avg"])
        )
        if pd.isna(raw.loc[raw_idx, "recent_schedule_balance_delta"]):
            raw.loc[raw_idx, "recent_schedule_balance_delta"] = np.nan
        else:
            raw.loc[raw_idx, "recent_schedule_balance_delta"] = round(float(raw.loc[raw_idx, "recent_schedule_balance_delta"]), 3)
        raw.loc[raw_idx, "recent_schedule_strength_updated_at"] = datetime.now(timezone.utc).isoformat()

        print(
            f"fixture={current_fixture_id} {match.get('home_team')} vs {match.get('away_team')} | "
            f"home={home_metrics['recent_schedule_quality_flag']} avg={home_metrics['recent_opponent_strength_avg']} | "
            f"away={away_metrics['recent_schedule_quality_flag']} avg={away_metrics['recent_opponent_strength_avg']}"
        )

    raw.to_csv(RAW_MATCHES, index=False)
    save_json(STANDINGS_CACHE, standings_cache)

    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    summary = build_summary(raw, target_fixture_ids, counters)
    summary.to_csv(OUTPUT_SUMMARY, index=False)
    write_report(summary)

    print("\n=== RECENT SCHEDULE STRENGTH COMPLETADO ===")
    print(f"Partidos procesados: {len(target_fixture_ids)}")
    print(f"Standings API calls: {counters['standings_api_calls']}")
    print(f"Standings cache hits: {counters['standings_cache_hits']}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print(f"Report: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
