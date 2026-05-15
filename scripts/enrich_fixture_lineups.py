from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import shutil

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError, build_params_key
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError, build_params_key


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_fixture_lineups_backup.csv"
OUTPUT_REPORT = ROOT / "data" / "processed" / "fixture_lineups_enrichment_report.csv"

TARGET_MAX_TIER_RANK = 2
LINEUP_QUALITY_FLAGS = {"FULL", "PARTIAL", "NONE"}
LINEUP_ACTIVATION_WINDOW_MINUTES = 90
LINEUP_ACTIVATION_STATES = {"ACTIVE", "ADVISORY_ONLY", "INACTIVE"}


NUMERIC_OUTPUT_COLS = [
    "home_lineup_available_flag",
    "away_lineup_available_flag",
    "home_lineup_known_starters_count",
    "away_lineup_known_starters_count",
    "home_lineup_bench_known_flag",
    "away_lineup_bench_known_flag",
    "home_lineup_attacker_count",
    "away_lineup_attacker_count",
    "home_lineup_defender_count",
    "away_lineup_defender_count",
    "home_lineup_midfielder_count",
    "away_lineup_midfielder_count",
    "home_lineup_goalkeeper_known_flag",
    "away_lineup_goalkeeper_known_flag",
    "home_lineup_attack_continuity_score",
    "away_lineup_attack_continuity_score",
    "home_lineup_defense_continuity_score",
    "away_lineup_defense_continuity_score",
    "lineup_confirmation_score",
    "lineup_uncertainty_penalty",
    "lineup_activation_window_minutes",
    "lineup_minutes_to_kickoff",
    "lineup_timing_eligible_flag",
    "lineup_structural_confidence_flag",
]

TEXT_OUTPUT_COLS = [
    "home_lineup_quality_flag",
    "away_lineup_quality_flag",
    "lineup_quality_flag",
    "lineup_activation_state",
    "fixture_lineups_updated_at",
]


def safe_int(value: Any) -> int | None:
    try:
        if pd.isna(value):
            return None
        return int(float(value))
    except Exception:
        return None


def norm_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def coverage_flag_allows(value: Any) -> bool:
    # Missing matrix fields mean unknown. Explicit official 0 keeps lineups
    # inactive/advisory without implying team weakness.
    if value is None or pd.isna(value):
        return True
    try:
        return int(float(value)) == 1
    except Exception:
        return str(value).strip().lower() in {"1", "true", "yes"}


def norm_name(value: Any) -> str:
    return " ".join(norm_text(value).lower().split())


def parse_datetime_utc(value: Any) -> datetime | None:
    if value is None or pd.isna(value):
        return None
    try:
        dt = pd.to_datetime(value, utc=True, errors="coerce")
    except Exception:
        return None
    if pd.isna(dt):
        return None
    return dt.to_pydatetime()


def fixture_datetime_from_row(row: pd.Series) -> datetime | None:
    for col in ["fixture_datetime_utc", "fixture_date_utc", "fixture_datetime"]:
        if col in row.index:
            parsed = parse_datetime_utc(row.get(col))
            if parsed is not None:
                return parsed

    timestamp = row.get("fixture_timestamp") if "fixture_timestamp" in row.index else None
    try:
        if timestamp is not None and not pd.isna(timestamp):
            return datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
    except Exception:
        return None

    return None


def cache_has_valid_lineups(client: APIFootballClient, fixture: int) -> bool:
    params_key = build_params_key("/fixtures/lineups", {"fixture": fixture})
    return client._get_cached(params_key) is not None


def role_bucket(position: Any) -> str:
    text = norm_text(position).lower()
    if not text:
        return "UNKNOWN"
    if text.startswith("g") or "keeper" in text or "goal" in text:
        return "GK"
    if text.startswith("d") or "defend" in text or "back" in text:
        return "DEF"
    if text.startswith("m") or "mid" in text:
        return "MID"
    if text.startswith(("f", "a")) or any(token in text for token in ["forward", "wing", "striker", "attacker"]):
        return "ATT"
    return "UNKNOWN"


def parse_lineup_player(item: dict[str, Any]) -> dict[str, Any]:
    player = item.get("player") or {}
    return {
        "player_id": safe_int(player.get("id")),
        "player_name": norm_text(player.get("name")),
        "position": norm_text(player.get("pos")),
        "role": role_bucket(player.get("pos")),
    }


def parse_team_lineup(block: dict[str, Any]) -> dict[str, Any]:
    team = block.get("team") or {}
    starters = [parse_lineup_player(item) for item in block.get("startXI", []) or []]
    bench = [parse_lineup_player(item) for item in block.get("substitutes", []) or []]
    return {
        "team_id": safe_int(team.get("id")),
        "team_name": norm_text(team.get("name")),
        "formation": norm_text(block.get("formation")),
        "starters": starters,
        "bench": bench,
    }


def parse_lineups_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for block in payload.get("response", []) or []:
        parsed = parse_team_lineup(block)
        if parsed["team_id"] is not None or parsed["team_name"]:
            rows.append(parsed)
    return rows


def find_team_lineup(
    lineups: list[dict[str, Any]],
    team_id: int | None,
    team_name: Any = "",
) -> dict[str, Any] | None:
    if team_id is not None:
        for lineup in lineups:
            if lineup.get("team_id") == team_id:
                return lineup

    wanted_name = norm_name(team_name)
    if wanted_name:
        for lineup in lineups:
            if norm_name(lineup.get("team_name")) == wanted_name:
                return lineup

    return None


def lineup_quality_flag(starters_count: int | None) -> str:
    if starters_count is None or starters_count <= 0:
        return "NONE"
    if starters_count >= 11:
        return "FULL"
    return "PARTIAL"


def fixture_quality_flag(home_quality: str, away_quality: str) -> str:
    if home_quality == "FULL" and away_quality == "FULL":
        return "FULL"
    if home_quality != "NONE" or away_quality != "NONE":
        return "PARTIAL"
    return "NONE"


def attack_continuity_score(starters_count: int, attackers: int, midfielders: int, quality: str) -> float:
    score = 0.0
    if quality == "FULL":
        score += 0.12
    if starters_count >= 10:
        score += 0.08
    if attackers >= 2:
        score += 0.20
    elif attackers == 1:
        score -= 0.08
    else:
        score -= 0.28
    if midfielders >= 3:
        score += 0.10
    elif midfielders <= 1:
        score -= 0.08
    return round(float(np.clip(score, -0.35, 0.45)), 3)


def defense_continuity_score(starters_count: int, defenders: int, goalkeeper_known: int, quality: str) -> float:
    score = 0.0
    if quality == "FULL":
        score += 0.10
    if starters_count >= 10:
        score += 0.06
    if goalkeeper_known:
        score += 0.18
    else:
        score -= 0.28
    if defenders >= 3:
        score += 0.16
    elif defenders <= 2:
        score -= 0.14
    return round(float(np.clip(score, -0.40, 0.45)), 3)


def empty_team_features(prefix: str) -> dict[str, Any]:
    return {
        f"{prefix}_lineup_available_flag": 0,
        f"{prefix}_lineup_quality_flag": "NONE",
        f"{prefix}_lineup_known_starters_count": np.nan,
        f"{prefix}_lineup_bench_known_flag": np.nan,
        f"{prefix}_lineup_attacker_count": np.nan,
        f"{prefix}_lineup_defender_count": np.nan,
        f"{prefix}_lineup_midfielder_count": np.nan,
        f"{prefix}_lineup_goalkeeper_known_flag": np.nan,
        f"{prefix}_lineup_attack_continuity_score": np.nan,
        f"{prefix}_lineup_defense_continuity_score": np.nan,
    }


def team_features(prefix: str, lineup: dict[str, Any] | None) -> dict[str, Any]:
    if lineup is None:
        return empty_team_features(prefix)

    starters = lineup.get("starters", []) or []
    starter_count = len(starters)
    quality = lineup_quality_flag(starter_count)
    if quality == "NONE":
        return empty_team_features(prefix)

    roles = [player.get("role", "UNKNOWN") for player in starters]
    attackers = roles.count("ATT")
    defenders = roles.count("DEF")
    midfielders = roles.count("MID")
    goalkeeper_known = 1 if roles.count("GK") >= 1 else 0
    bench_known = 1 if len(lineup.get("bench", []) or []) > 0 else 0

    return {
        f"{prefix}_lineup_available_flag": 1,
        f"{prefix}_lineup_quality_flag": quality,
        f"{prefix}_lineup_known_starters_count": starter_count,
        f"{prefix}_lineup_bench_known_flag": bench_known,
        f"{prefix}_lineup_attacker_count": attackers,
        f"{prefix}_lineup_defender_count": defenders,
        f"{prefix}_lineup_midfielder_count": midfielders,
        f"{prefix}_lineup_goalkeeper_known_flag": goalkeeper_known,
        f"{prefix}_lineup_attack_continuity_score": attack_continuity_score(
            starter_count,
            attackers,
            midfielders,
            quality,
        ),
        f"{prefix}_lineup_defense_continuity_score": defense_continuity_score(
            starter_count,
            defenders,
            goalkeeper_known,
            quality,
        ),
    }


def build_lineup_features(
    payload: dict[str, Any],
    home_team_id: int | None,
    away_team_id: int | None,
    home_team_name: Any = "",
    away_team_name: Any = "",
    fixture_datetime_utc: Any = None,
    reference_datetime_utc: Any = None,
    activation_window_minutes: int = LINEUP_ACTIVATION_WINDOW_MINUTES,
) -> dict[str, Any]:
    lineups = parse_lineups_payload(payload)
    home_lineup = find_team_lineup(lineups, home_team_id, home_team_name)
    away_lineup = find_team_lineup(lineups, away_team_id, away_team_name)

    features: dict[str, Any] = {}
    features.update(team_features("home", home_lineup))
    features.update(team_features("away", away_lineup))

    quality = fixture_quality_flag(
        features["home_lineup_quality_flag"],
        features["away_lineup_quality_flag"],
    )
    available_scores = [
        features.get("home_lineup_attack_continuity_score"),
        features.get("away_lineup_attack_continuity_score"),
        features.get("home_lineup_defense_continuity_score"),
        features.get("away_lineup_defense_continuity_score"),
    ]
    known_scores = [float(value) for value in available_scores if not pd.isna(value)]
    if known_scores:
        confirmation = round(float(np.clip(np.mean(known_scores), -0.35, 0.45)), 3)
    else:
        confirmation = np.nan

    features["lineup_quality_flag"] = quality
    features["lineup_confirmation_score"] = confirmation
    features["lineup_uncertainty_penalty"] = {"FULL": 0.0, "PARTIAL": 0.08, "NONE": 0.12}.get(quality, 0.12)
    features.update(
        lineup_activation_features(
            features,
            fixture_datetime_utc=fixture_datetime_utc,
            reference_datetime_utc=reference_datetime_utc,
            activation_window_minutes=activation_window_minutes,
        )
    )
    features["fixture_lineups_updated_at"] = datetime.now(timezone.utc).isoformat()
    return features


def lineup_activation_features(
    features: dict[str, Any],
    fixture_datetime_utc: Any = None,
    reference_datetime_utc: Any = None,
    activation_window_minutes: int = LINEUP_ACTIVATION_WINDOW_MINUTES,
) -> dict[str, Any]:
    quality = norm_text(features.get("lineup_quality_flag")).upper()
    home_available = safe_int(features.get("home_lineup_available_flag")) == 1
    away_available = safe_int(features.get("away_lineup_available_flag")) == 1
    home_starters = safe_int(features.get("home_lineup_known_starters_count"))
    away_starters = safe_int(features.get("away_lineup_known_starters_count"))
    home_gk = safe_int(features.get("home_lineup_goalkeeper_known_flag"))
    away_gk = safe_int(features.get("away_lineup_goalkeeper_known_flag"))
    structural_confident = (
        quality == "FULL"
        and home_available
        and away_available
        and home_starters is not None
        and away_starters is not None
        and home_starters >= 11
        and away_starters >= 11
        and home_gk == 1
        and away_gk == 1
    )

    fixture_dt = parse_datetime_utc(fixture_datetime_utc)
    reference_dt = parse_datetime_utc(reference_datetime_utc) or datetime.now(timezone.utc)
    minutes_to_kickoff = np.nan
    timing_eligible = 0
    if fixture_dt is not None:
        minutes_to_kickoff = round((fixture_dt - reference_dt).total_seconds() / 60.0, 2)
        timing_eligible = int(0 <= minutes_to_kickoff <= activation_window_minutes)

    if quality == "NONE" or not (home_available and away_available):
        activation_state = "INACTIVE"
    elif structural_confident and timing_eligible:
        activation_state = "ACTIVE"
    else:
        activation_state = "ADVISORY_ONLY"

    return {
        "lineup_activation_state": activation_state,
        "lineup_activation_window_minutes": activation_window_minutes,
        "lineup_minutes_to_kickoff": minutes_to_kickoff,
        "lineup_timing_eligible_flag": timing_eligible,
        "lineup_structural_confidence_flag": int(structural_confident),
    }


def ensure_output_columns(raw: pd.DataFrame) -> pd.DataFrame:
    missing = {
        **{col: np.nan for col in NUMERIC_OUTPUT_COLS if col not in raw.columns},
        **{col: "" for col in TEXT_OUTPUT_COLS if col not in raw.columns},
    }
    if missing:
        raw = pd.concat([raw, pd.DataFrame(missing, index=raw.index)], axis=1)
    return raw


def write_features(raw: pd.DataFrame, raw_idx: int, features: dict[str, Any]) -> None:
    for col, value in features.items():
        raw.loc[raw_idx, col] = value


def fetch_fixture_lineups(
    client: APIFootballClient,
    fixture_id: int,
    counters: dict[str, int],
) -> dict[str, Any] | None:
    if cache_has_valid_lineups(client, fixture_id):
        counters["cache_hits"] += 1
    else:
        counters["api_calls_made"] += 1

    try:
        return client.fixture_lineups(fixture_id)
    except APIFootballError as exc:
        counters["api_errors"] += 1
        if exc.is_plan_limit:
            counters["plan_limit_errors"] += 1
        return None
    except Exception:
        counters["api_errors"] += 1
        return None


def build_report(rows_processed: int, counters: dict[str, int], target: pd.DataFrame) -> pd.DataFrame:
    quality = target.get("lineup_quality_flag", pd.Series(dtype="object")).fillna("NONE").astype(str).str.upper()
    activation = target.get("lineup_activation_state", pd.Series(dtype="object")).fillna("INACTIVE").astype(str).str.upper()
    timing_eligible = pd.to_numeric(target.get("lineup_timing_eligible_flag"), errors="coerce").fillna(0)
    known_counts = pd.concat(
        [
            pd.to_numeric(target.get("home_lineup_known_starters_count"), errors="coerce"),
            pd.to_numeric(target.get("away_lineup_known_starters_count"), errors="coerce"),
        ],
        ignore_index=True,
    )
    return pd.DataFrame(
        [
            {
                "rows_processed": rows_processed,
                "full_rows": int(quality.eq("FULL").sum()),
                "partial_rows": int(quality.eq("PARTIAL").sum()),
                "none_rows": int(quality.eq("NONE").sum()),
                "active_rows": int(activation.eq("ACTIVE").sum()),
                "advisory_only_rows": int(activation.eq("ADVISORY_ONLY").sum()),
                "inactive_rows": int(activation.eq("INACTIVE").sum()),
                "timing_eligible_rows": int(timing_eligible.eq(1).sum()),
                "timing_ineligible_rows": int(timing_eligible.ne(1).sum()),
                "lineup_available_rows": int(quality.ne("NONE").sum()),
                "lineup_unavailable_rows": int(quality.eq("NONE").sum()),
                "api_calls_made": counters.get("api_calls_made", 0),
                "cache_hits": counters.get("cache_hits", 0),
                "api_errors": counters.get("api_errors", 0),
                "plan_limit_errors": counters.get("plan_limit_errors", 0),
                "avg_known_starters_count": round(float(known_counts.dropna().mean()), 3)
                if not known_counts.dropna().empty
                else np.nan,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        ]
    )


def select_target_rows(raw: pd.DataFrame, filtered: pd.DataFrame) -> pd.DataFrame:
    if filtered.empty:
        return filtered
    target = filtered.copy()
    if "league_tier_rank" in target.columns:
        ranks = pd.to_numeric(target["league_tier_rank"], errors="coerce")
        target = target[ranks.le(TARGET_MAX_TIER_RANK)].copy()
    if "fixture_id" in target.columns:
        target = target[target["fixture_id"].notna()].drop_duplicates("fixture_id").copy()
    return target


def main() -> None:
    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe raw matches: {RAW_MATCHES}")
    if not FILTERED_MATCHES.exists():
        raise FileNotFoundError(f"No existe filtered matches: {FILTERED_MATCHES}")

    raw = pd.read_csv(RAW_MATCHES)
    filtered = pd.read_csv(FILTERED_MATCHES)
    raw = ensure_output_columns(raw)
    target = select_target_rows(raw, filtered)

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RAW_MATCHES.parent.mkdir(parents=True, exist_ok=True)
    if RAW_MATCHES.exists():
        shutil.copy2(RAW_MATCHES, BACKUP_MATCHES)

    counters = {
        "api_calls_made": 0,
        "cache_hits": 0,
        "api_errors": 0,
        "plan_limit_errors": 0,
    }

    if target.empty:
        build_report(0, counters, raw.iloc[0:0]).to_csv(OUTPUT_REPORT, index=False)
        raw.to_csv(RAW_MATCHES, index=False)
        print("\n=== FIXTURE LINEUPS ENRICHMENT COMPLETADO ===")
        print("Target rows: 0")
        print(f"Reporte: {OUTPUT_REPORT}")
        return

    client = APIFootballClient()
    raw_fixture_ids = raw["fixture_id"].apply(safe_int) if "fixture_id" in raw.columns else pd.Series(dtype="object")
    processed_fixture_ids: set[int] = set()

    for _, row in target.iterrows():
        fixture_id = safe_int(row.get("fixture_id"))
        if fixture_id is None or fixture_id in processed_fixture_ids:
            continue
        processed_fixture_ids.add(fixture_id)

        if not coverage_flag_allows(row.get("league_has_lineups_coverage", np.nan)):
            payload = {"response": []}
        else:
            payload = fetch_fixture_lineups(client, fixture_id, counters)
        if payload is None:
            payload = {"response": []}

        features = build_lineup_features(
            payload,
            safe_int(row.get("home_team_id")),
            safe_int(row.get("away_team_id")),
            row.get("home_team", ""),
            row.get("away_team", ""),
            fixture_datetime_utc=fixture_datetime_from_row(row),
        )

        raw_indexes = raw.index[raw_fixture_ids == fixture_id].tolist()
        for raw_idx in raw_indexes:
            write_features(raw, raw_idx, features)

    raw.to_csv(RAW_MATCHES, index=False)
    target_after = raw[raw["fixture_id"].apply(safe_int).isin(processed_fixture_ids)].copy()
    build_report(len(processed_fixture_ids), counters, target_after).to_csv(OUTPUT_REPORT, index=False)

    print("\n=== FIXTURE LINEUPS ENRICHMENT COMPLETADO ===")
    print(f"Target rows: {len(processed_fixture_ids)}")
    print(f"API calls: {counters['api_calls_made']} | cache hits: {counters['cache_hits']}")
    print(f"API errors: {counters['api_errors']} | plan limit: {counters['plan_limit_errors']}")
    print(f"Raw actualizado: {RAW_MATCHES}")
    print(f"Reporte: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
