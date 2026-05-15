from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import math
import shutil
import unicodedata
from typing import Any

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError, build_params_key
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError, build_params_key


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
RECENT_FIXTURES_CACHE = ROOT / "data" / "raw" / "team_recent_fixtures_cache_v2.json"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_recent_fixture_statistics_backup.csv"
OUTPUT_REPORT = ROOT / "data" / "processed" / "recent_fixture_statistics_enrichment_report.csv"

FINISHED_STATUSES = {"FT", "AET", "PEN"}
TARGET_MAX_TIER_RANK = 2
RECENT_STATS_WINDOW = 5
PULL_N = 15

CANONICAL_STATS = [
    "shots",
    "sot",
    "possession",
    "corners",
    "fouls",
    "yellow",
    "offsides",
    "blocked_shots",
]

SIDE_METRIC_OUTPUTS = [
    "recent_shots_for_pg",
    "recent_shots_against_pg",
    "recent_sot_for_pg",
    "recent_sot_against_pg",
    "recent_possession_pct",
    "recent_corners_for_pg",
    "recent_corners_against_pg",
    "recent_fouls_pg",
    "recent_yellow_pg",
    "recent_offsides_pg",
    "recent_blocked_shots_pg",
]


def load_recent_fixtures_cache() -> dict[str, list[dict[str, Any]]]:
    if not RECENT_FIXTURES_CACHE.exists():
        return {}
    try:
        return json.loads(RECENT_FIXTURES_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_recent_fixtures_cache(cache: dict[str, list[dict[str, Any]]]) -> None:
    RECENT_FIXTURES_CACHE.parent.mkdir(parents=True, exist_ok=True)
    RECENT_FIXTURES_CACHE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def safe_int(value: Any) -> int | None:
    try:
        if pd.isna(value):
            return None
        return int(float(value))
    except Exception:
        return None


def safe_float(value: Any) -> float:
    try:
        if value is None or pd.isna(value):
            return np.nan
        if isinstance(value, str):
            cleaned = value.strip().replace("%", "").replace(",", ".")
            if cleaned == "":
                return np.nan
            return float(cleaned)
        return float(value)
    except Exception:
        return np.nan


def coverage_flag_allows(value: Any) -> bool:
    # Missing matrix fields mean "unknown"; only explicit official 0 disables the layer.
    if value is None or pd.isna(value):
        return True
    try:
        return int(float(value)) == 1
    except Exception:
        return str(value).strip().lower() in {"1", "true", "yes"}


def parse_dt(value: Any) -> datetime | None:
    try:
        return pd.to_datetime(value, utc=True).to_pydatetime()
    except Exception:
        return None


def normalize_label(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("_", " ").replace("-", " ")
    return " ".join(text.split())


def canonical_stat_name(raw_label: Any) -> str | None:
    label = normalize_label(raw_label)
    mapping = {
        "shots on goal": "sot",
        "shots on target": "sot",
        "total shots": "shots",
        "shots": "shots",
        "corner kicks": "corners",
        "corners": "corners",
        "ball possession": "possession",
        "possession": "possession",
        "fouls": "fouls",
        "yellow cards": "yellow",
        "yellow card": "yellow",
        "offsides": "offsides",
        "offside": "offsides",
        "blocked shots": "blocked_shots",
        "blocked shot": "blocked_shots",
    }
    return mapping.get(label)


def parse_stat_value(value: Any) -> float:
    return safe_float(value)


def normalize_team_statistics(statistics: list[dict[str, Any]]) -> dict[str, float]:
    out = {name: np.nan for name in CANONICAL_STATS}
    for item in statistics or []:
        canonical = canonical_stat_name(item.get("type"))
        if canonical is None:
            continue
        out[canonical] = parse_stat_value(item.get("value"))
    return out


def parse_fixture_statistics_payload(payload: dict[str, Any]) -> dict[int, dict[str, float]]:
    parsed: dict[int, dict[str, float]] = {}
    for team_block in payload.get("response", []) or []:
        team_id = safe_int((team_block.get("team") or {}).get("id"))
        if team_id is None:
            continue
        parsed[team_id] = normalize_team_statistics(team_block.get("statistics", []) or [])
    return parsed


def fixture_finished(item: dict[str, Any]) -> bool:
    status = (item.get("fixture") or {}).get("status") or {}
    return str(status.get("short", "")).upper() in FINISHED_STATUSES


def fixture_id(item: dict[str, Any]) -> int | None:
    return safe_int((item.get("fixture") or {}).get("id"))


def fixture_timestamp(item: dict[str, Any]) -> int:
    return safe_int((item.get("fixture") or {}).get("timestamp")) or 0


def pick_prior_completed_fixtures(
    fixtures: list[dict[str, Any]],
    target_fixture_id: int | None,
    before_dt: datetime | None,
    limit: int = RECENT_STATS_WINDOW,
) -> list[dict[str, Any]]:
    selected = []
    for item in fixtures:
        item_fixture_id = fixture_id(item)
        if target_fixture_id is not None and item_fixture_id == target_fixture_id:
            continue
        if not fixture_finished(item):
            continue
        item_dt = parse_dt((item.get("fixture") or {}).get("date"))
        if before_dt is not None and item_dt is not None and item_dt >= before_dt:
            continue
        selected.append(item)

    selected = sorted(selected, key=fixture_timestamp, reverse=True)
    return selected[:limit]


def fetch_team_recent_fixtures(
    client: APIFootballClient,
    cache: dict[str, list[dict[str, Any]]],
    team_id: int,
    season: int,
) -> list[dict[str, Any]]:
    cache_key = f"{team_id}|{season}"
    if cache_key in cache:
        return cache[cache_key]

    payload = client.request(
        "/fixtures",
        params={"team": team_id, "season": season, "last": PULL_N},
        ttl_hours=6,
    )
    fixtures = payload.get("response", []) or []
    cache[cache_key] = fixtures
    return fixtures


def season_candidates(season: int | None) -> list[int]:
    candidates: list[int] = []
    if season is not None:
        candidates.extend([season, season - 1, season - 2])
    candidates.extend([2026, 2025, 2024])

    out = []
    seen = set()
    for item in candidates:
        if item is None or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def pick_recent_fixture_bundle(
    client: APIFootballClient,
    cache: dict[str, list[dict[str, Any]]],
    team_id: int | None,
    season: int | None,
    before_dt: datetime | None,
    target_fixture_id: int | None,
) -> list[dict[str, Any]]:
    if team_id is None:
        return []

    best: list[dict[str, Any]] = []
    for candidate_season in season_candidates(season):
        try:
            fixtures = fetch_team_recent_fixtures(client, cache, team_id, candidate_season)
        except APIFootballError:
            continue
        except Exception:
            continue

        prior = pick_prior_completed_fixtures(
            fixtures=fixtures,
            target_fixture_id=target_fixture_id,
            before_dt=before_dt,
            limit=RECENT_STATS_WINDOW,
        )
        if len(prior) > len(best):
            best = prior
        if len(best) >= RECENT_STATS_WINDOW:
            break
    return best


def cache_has_valid_statistics(client: APIFootballClient, fixture: int) -> bool:
    params_key = build_params_key("/fixtures/statistics", {"fixture": fixture})
    return client._get_cached(params_key) is not None


def fetch_fixture_statistics(
    client: APIFootballClient,
    fixture: int,
    counters: dict[str, int],
) -> dict[int, dict[str, float]]:
    if cache_has_valid_statistics(client, fixture):
        counters["cache_hits"] += 1
    else:
        counters["api_calls_made"] += 1

    counters["stats_fixture_requests"] += 1
    payload = client.fixture_statistics(fixture)
    return parse_fixture_statistics_payload(payload)


def has_core_stat(stats: dict[str, float]) -> bool:
    return any(not math.isnan(stats.get(name, np.nan)) for name in ["shots", "sot", "corners", "possession"])


def mean_or_nan(values: list[float]) -> float:
    clean = [float(value) for value in values if not pd.isna(value)]
    if not clean:
        return np.nan
    return round(float(np.mean(clean)), 3)


def compute_team_rolling_stats(
    client: APIFootballClient,
    fixtures: list[dict[str, Any]],
    team_id: int | None,
    counters: dict[str, int],
) -> dict[str, Any]:
    requested = len(fixtures)
    if requested == 0 or team_id is None:
        return build_empty_team_output(requested)

    own_values = {name: [] for name in CANONICAL_STATS}
    against_values = {name: [] for name in ["shots", "sot", "corners"]}
    used = 0

    for item in fixtures:
        fid = fixture_id(item)
        if fid is None:
            continue

        try:
            stats_by_team = fetch_fixture_statistics(client, fid, counters)
        except APIFootballError as exc:
            counters["api_errors"] += 1
            if exc.is_plan_limit:
                counters["plan_limit_errors"] += 1
            continue
        except Exception:
            counters["api_errors"] += 1
            continue

        own = stats_by_team.get(int(team_id))
        if not own or not has_core_stat(own):
            continue

        opponent_stats = [
            stats for other_team_id, stats in stats_by_team.items()
            if other_team_id != int(team_id)
        ]
        opponent = opponent_stats[0] if opponent_stats else {}

        used += 1
        for name in CANONICAL_STATS:
            value = own.get(name, np.nan)
            if not pd.isna(value):
                own_values[name].append(value)

        for name in against_values:
            value = opponent.get(name, np.nan)
            if not pd.isna(value):
                against_values[name].append(value)

    output = {
        "recent_stats_matches_requested": requested,
        "recent_stats_matches_used": used,
        "recent_stats_coverage_ratio": round(used / requested, 3) if requested else 0.0,
        "recent_stats_available_flag": 1 if used > 0 else 0,
        "recent_shots_for_pg": mean_or_nan(own_values["shots"]),
        "recent_shots_against_pg": mean_or_nan(against_values["shots"]),
        "recent_sot_for_pg": mean_or_nan(own_values["sot"]),
        "recent_sot_against_pg": mean_or_nan(against_values["sot"]),
        "recent_possession_pct": mean_or_nan(own_values["possession"]),
        "recent_corners_for_pg": mean_or_nan(own_values["corners"]),
        "recent_corners_against_pg": mean_or_nan(against_values["corners"]),
        "recent_fouls_pg": mean_or_nan(own_values["fouls"]),
        "recent_yellow_pg": mean_or_nan(own_values["yellow"]),
        "recent_offsides_pg": mean_or_nan(own_values["offsides"]),
        "recent_blocked_shots_pg": mean_or_nan(own_values["blocked_shots"]),
    }
    return output


def build_empty_team_output(requested: int) -> dict[str, Any]:
    output = {
        "recent_stats_matches_requested": requested,
        "recent_stats_matches_used": 0,
        "recent_stats_coverage_ratio": 0.0,
        "recent_stats_available_flag": 0,
    }
    for col in SIDE_METRIC_OUTPUTS:
        output[col] = np.nan
    return output


def quality_flag(home_used: int, away_used: int) -> str:
    if home_used >= RECENT_STATS_WINDOW and away_used >= RECENT_STATS_WINDOW:
        return "FULL"
    if home_used >= 3 and away_used >= 3:
        return "PARTIAL"
    if home_used > 0 or away_used > 0:
        return "SPARSE"
    return "NONE"


def ensure_output_columns(raw: pd.DataFrame) -> pd.DataFrame:
    for side in ["home", "away"]:
        for col in ["recent_stats_matches_requested", "recent_stats_matches_used", "recent_stats_coverage_ratio", "recent_stats_available_flag"]:
            full_col = f"{side}_{col}"
            if full_col not in raw.columns:
                raw[full_col] = np.nan
        for col in SIDE_METRIC_OUTPUTS:
            full_col = f"{side}_{col}"
            if full_col not in raw.columns:
                raw[full_col] = np.nan

    if "recent_stats_quality_flag" not in raw.columns:
        raw["recent_stats_quality_flag"] = "NONE"
    if "recent_fixture_statistics_updated_at" not in raw.columns:
        raw["recent_fixture_statistics_updated_at"] = ""
    return raw


def write_side_output(raw: pd.DataFrame, raw_idx: int, side: str, metrics: dict[str, Any]) -> None:
    for key, value in metrics.items():
        raw.loc[raw_idx, f"{side}_{key}"] = value


def build_report(
    rows_processed: int,
    counters: dict[str, int],
    quality_counts: dict[str, int],
    raw: pd.DataFrame,
    target_fixture_ids: set[int],
) -> pd.DataFrame:
    target = raw[raw["fixture_id"].isin(target_fixture_ids)].copy() if target_fixture_ids else raw.iloc[0:0].copy()
    return pd.DataFrame(
        [
            {
                "rows_processed": rows_processed,
                "avg_home_matches_used": round(pd.to_numeric(target.get("home_recent_stats_matches_used"), errors="coerce").mean(), 3) if not target.empty else np.nan,
                "avg_away_matches_used": round(pd.to_numeric(target.get("away_recent_stats_matches_used"), errors="coerce").mean(), 3) if not target.empty else np.nan,
                "full_rows": quality_counts.get("FULL", 0),
                "partial_rows": quality_counts.get("PARTIAL", 0),
                "sparse_rows": quality_counts.get("SPARSE", 0),
                "none_rows": quality_counts.get("NONE", 0),
                "stats_fixture_requests": counters.get("stats_fixture_requests", 0),
                "api_calls_made": counters.get("api_calls_made", 0),
                "cache_hits": counters.get("cache_hits", 0),
                "api_errors": counters.get("api_errors", 0),
                "plan_limit_errors": counters.get("plan_limit_errors", 0),
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        ]
    )


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
    client = APIFootballClient()
    recent_cache = load_recent_fixtures_cache()

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= TARGET_MAX_TIER_RANK
    ].copy()

    counters = {
        "stats_fixture_requests": 0,
        "api_calls_made": 0,
        "cache_hits": 0,
        "api_errors": 0,
        "plan_limit_errors": 0,
    }
    quality_counts = {"FULL": 0, "PARTIAL": 0, "SPARSE": 0, "NONE": 0}
    rows_processed = 0
    target_fixture_ids: set[int] = set()

    print("\n=== ENRIQUECIMIENTO RECENT FIXTURE STATISTICS ===")
    print(f"Partidos filtrados totales: {len(filtered)}")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")
    print(f"Ventana deterministica: últimos {RECENT_STATS_WINDOW} fixtures completados antes del partido")

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

        if not coverage_flag_allows(match.get("league_has_fixture_stats_coverage", np.nan)):
            home_metrics = build_empty_team_output(0)
            away_metrics = build_empty_team_output(0)
            write_side_output(raw, raw_idx, "home", home_metrics)
            write_side_output(raw, raw_idx, "away", away_metrics)
            raw.loc[raw_idx, "recent_stats_quality_flag"] = "NONE"
            raw.loc[raw_idx, "recent_fixture_statistics_updated_at"] = datetime.now(timezone.utc).isoformat()
            quality_counts["NONE"] += 1
            rows_processed += 1
            print(
                f"SKIP_COVERAGE fixture={current_fixture_id} {match.get('home_team')} vs {match.get('away_team')} | "
                "official league coverage has statistics_fixtures=false"
            )
            continue

        home_fixtures = pick_recent_fixture_bundle(
            client=client,
            cache=recent_cache,
            team_id=home_team_id,
            season=season,
            before_dt=match_dt,
            target_fixture_id=current_fixture_id,
        )
        away_fixtures = pick_recent_fixture_bundle(
            client=client,
            cache=recent_cache,
            team_id=away_team_id,
            season=season,
            before_dt=match_dt,
            target_fixture_id=current_fixture_id,
        )

        home_metrics = compute_team_rolling_stats(client, home_fixtures, home_team_id, counters)
        away_metrics = compute_team_rolling_stats(client, away_fixtures, away_team_id, counters)

        write_side_output(raw, raw_idx, "home", home_metrics)
        write_side_output(raw, raw_idx, "away", away_metrics)

        flag = quality_flag(
            int(home_metrics["recent_stats_matches_used"]),
            int(away_metrics["recent_stats_matches_used"]),
        )
        raw.loc[raw_idx, "recent_stats_quality_flag"] = flag
        raw.loc[raw_idx, "recent_fixture_statistics_updated_at"] = datetime.now(timezone.utc).isoformat()

        quality_counts[flag] += 1
        rows_processed += 1

        print(
            f"{flag} fixture={current_fixture_id} {match.get('home_team')} vs {match.get('away_team')} | "
            f"home_stats={home_metrics['recent_stats_matches_used']}/{home_metrics['recent_stats_matches_requested']} "
            f"away_stats={away_metrics['recent_stats_matches_used']}/{away_metrics['recent_stats_matches_requested']}"
        )

    raw.to_csv(RAW_MATCHES, index=False)
    save_recent_fixtures_cache(recent_cache)

    report = build_report(rows_processed, counters, quality_counts, raw, target_fixture_ids)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT_REPORT, index=False)

    print("\n=== RECENT FIXTURE STATISTICS COMPLETADO ===")
    print(f"Partidos procesados: {rows_processed}")
    print(f"FULL: {quality_counts['FULL']}")
    print(f"PARTIAL: {quality_counts['PARTIAL']}")
    print(f"SPARSE: {quality_counts['SPARSE']}")
    print(f"NONE: {quality_counts['NONE']}")
    print(f"Stats fixture requests: {counters['stats_fixture_requests']}")
    print(f"API calls made: {counters['api_calls_made']}")
    print(f"Cache hits: {counters['cache_hits']}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Reporte: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
