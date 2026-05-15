from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import shutil

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError, build_params_key
    from enrich_recent_fixture_statistics import (
        load_recent_fixtures_cache,
        pick_recent_fixture_bundle,
        safe_int,
        parse_dt,
        fixture_id,
    )
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError, build_params_key
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
COVERAGE_MATRIX = ROOT / "data" / "processed" / "vsigma_api_league_coverage_matrix.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_recent_fixture_anomaly_flags_backup.csv"
OUTPUT_SUMMARY = ROOT / "data" / "processed" / "vsigma_recent_anomaly_summary.csv"
OUTPUT_REPORT = ROOT / "data" / "processed" / "vsigma_recent_anomaly_report.txt"

TARGET_MAX_TIER_RANK = 2
RECENT_WINDOW = 5
EARLY_RED_MAX_MINUTE = 35
EARLY_PENALTY_MAX_MINUTE = 25
SHOCK_MAX_MINUTE = 30
EXCEPTIONAL_STATUSES = {"ABD", "AWD", "WO", "CANC", "SUSP", "INT"}


ANOMALY_NUMERIC_COLS = [
    "home_recent_anomaly_count_last5",
    "away_recent_anomaly_count_last5",
    "home_recent_clean_sample_size",
    "away_recent_clean_sample_size",
    "home_recent_anomaly_penalty",
    "away_recent_anomaly_penalty",
    "home_recent_events_checked_last5",
    "away_recent_events_checked_last5",
]

ANOMALY_TEXT_COLS = [
    "recent_sample_cleanliness_flag",
    "home_recent_event_coverage_flag",
    "away_recent_event_coverage_flag",
    "recent_fixture_anomaly_updated_at",
]


def safe_float(value: Any) -> float:
    try:
        if value is None or pd.isna(value):
            return np.nan
        return float(value)
    except Exception:
        return np.nan


def norm_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip().upper()


def event_minute(event: dict[str, Any]) -> int | None:
    time = event.get("time") or {}
    elapsed = safe_int(time.get("elapsed"))
    extra = safe_int(time.get("extra")) or 0
    if elapsed is None:
        return None
    return int(elapsed + extra)


def event_team_id(event: dict[str, Any]) -> int | None:
    return safe_int((event.get("team") or {}).get("id"))


def is_red_card(event: dict[str, Any]) -> bool:
    if norm_text(event.get("type")) != "CARD":
        return False
    detail = norm_text(event.get("detail"))
    return "RED" in detail


def is_penalty_event(event: dict[str, Any]) -> bool:
    detail = norm_text(event.get("detail"))
    event_type = norm_text(event.get("type"))
    comments = norm_text(event.get("comments"))
    return "PENALTY" in detail or (event_type == "VAR" and "PENALTY" in comments)


def is_goal_event(event: dict[str, Any]) -> bool:
    return norm_text(event.get("type")) == "GOAL" and "CANCELLED" not in norm_text(event.get("detail"))


def fixture_status(item: dict[str, Any]) -> str:
    return norm_text(((item.get("fixture") or {}).get("status") or {}).get("short"))


def parse_fixture_events_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return list(payload.get("response", []) or [])


def detect_fixture_anomalies(events: list[dict[str, Any]], fixture: dict[str, Any] | None = None) -> dict[str, Any]:
    fixture = fixture or {}
    exceptional_status = fixture_status(fixture) in EXCEPTIONAL_STATUSES
    early_red = False
    early_penalty = False
    first_half_shock = False
    team_goals: dict[int, int] = {}

    for event in events:
        minute = event_minute(event)
        if minute is None:
            continue

        if is_red_card(event) and minute <= EARLY_RED_MAX_MINUTE:
            early_red = True
        if is_penalty_event(event) and minute <= EARLY_PENALTY_MAX_MINUTE:
            early_penalty = True
        if (is_red_card(event) or is_penalty_event(event)) and minute <= 15:
            first_half_shock = True

        if is_goal_event(event):
            team_id = event_team_id(event)
            if team_id is None:
                continue
            team_goals[team_id] = team_goals.get(team_id, 0) + 1
            if minute <= SHOCK_MAX_MINUTE and team_goals[team_id] >= 2:
                first_half_shock = True

    anomaly = bool(early_red or early_penalty or first_half_shock or exceptional_status)
    return {
        "early_red_card": int(early_red),
        "early_penalty": int(early_penalty),
        "first_half_game_state_shock": int(first_half_shock),
        "exceptional_status": int(exceptional_status),
        "fixture_anomaly_flag": int(anomaly),
    }


def load_coverage_matrix(path: Path = COVERAGE_MATRIX) -> dict[tuple[int, int], int | None]:
    if not path.exists():
        return {}
    df = pd.read_csv(path)
    if df.empty or "league_id" not in df.columns or "season" not in df.columns:
        return {}
    out: dict[tuple[int, int], int | None] = {}
    for _, row in df.iterrows():
        league_id = safe_int(row.get("league_id"))
        season = safe_int(row.get("season"))
        if league_id is None or season is None:
            continue
        value = row.get("league_has_events_coverage", np.nan)
        if pd.isna(value):
            out[(league_id, season)] = None
        else:
            out[(league_id, season)] = 1 if safe_float(value) >= 1 else 0
    return out


def fixture_league_season(item: dict[str, Any]) -> tuple[int | None, int | None]:
    league = item.get("league") or {}
    return safe_int(league.get("id")), safe_int(league.get("season"))


def events_coverage_flag(item: dict[str, Any], coverage: dict[tuple[int, int], int | None]) -> str:
    league_id, season = fixture_league_season(item)
    if league_id is None or season is None:
        return "UNKNOWN"
    value = coverage.get((league_id, season), None)
    if value == 1:
        return "SUPPORTED"
    if value == 0:
        return "UNSUPPORTED"
    return "UNKNOWN"


def cache_has_valid_events(client: APIFootballClient, fixture: int) -> bool:
    params_key = build_params_key("/fixtures/events", {"fixture": fixture})
    return client._get_cached(params_key) is not None


def fetch_fixture_events(client: APIFootballClient, fid: int, counters: dict[str, int]) -> list[dict[str, Any]]:
    if cache_has_valid_events(client, fid):
        counters["event_cache_hits"] += 1
    else:
        counters["event_api_calls"] += 1
    counters["event_fixture_requests"] += 1
    payload = client.fixture_events(fid)
    return parse_fixture_events_payload(payload)


def cleanliness_flag(home: dict[str, Any], away: dict[str, Any]) -> str:
    checked = int(home["recent_events_checked_last5"]) + int(away["recent_events_checked_last5"])
    anomalies = int(home["recent_anomaly_count_last5"]) + int(away["recent_anomaly_count_last5"])
    if checked == 0:
        return "UNKNOWN_EVENTS"
    rate = anomalies / checked
    if anomalies == 0:
        return "CLEAN"
    if rate <= 0.25:
        return "MIXED"
    return "POLLUTED"


def team_coverage_flag(checked: int, unknown: int, unsupported: int) -> str:
    if checked >= 4:
        return "SUPPORTED"
    if checked > 0:
        return "PARTIAL"
    if unsupported > 0 and unknown == 0:
        return "UNSUPPORTED"
    return "UNKNOWN"


def compute_team_recent_anomalies(
    client: APIFootballClient,
    fixtures: list[dict[str, Any]],
    coverage: dict[tuple[int, int], int | None],
    counters: dict[str, int] | None = None,
) -> dict[str, Any]:
    counters = counters if counters is not None else {}
    for key in ["event_fixture_requests", "event_api_calls", "event_cache_hits", "event_errors", "event_coverage_unknown", "event_coverage_unsupported"]:
        counters.setdefault(key, 0)

    selected = fixtures[:RECENT_WINDOW]
    checked = 0
    anomalies = 0
    unknown = 0
    unsupported = 0

    for item in selected:
        flag = events_coverage_flag(item, coverage)
        if flag == "UNSUPPORTED":
            unsupported += 1
            counters["event_coverage_unsupported"] += 1
            continue
        if flag == "UNKNOWN":
            unknown += 1
            counters["event_coverage_unknown"] += 1
            continue

        fid = fixture_id(item)
        if fid is None:
            continue
        try:
            events = fetch_fixture_events(client, fid, counters)
        except APIFootballError:
            counters["event_errors"] += 1
            continue
        except Exception:
            counters["event_errors"] += 1
            continue

        checked += 1
        parsed = detect_fixture_anomalies(events, item)
        anomalies += int(parsed["fixture_anomaly_flag"])

    clean_sample = max(0, checked - anomalies)
    penalty = round(min(1.20, anomalies * 0.35 + max(0, 3 - clean_sample) * 0.05), 3) if checked else 0.0
    return {
        "recent_anomaly_count_last5": anomalies,
        "recent_clean_sample_size": clean_sample,
        "recent_anomaly_penalty": penalty,
        "recent_events_checked_last5": checked,
        "recent_event_coverage_flag": team_coverage_flag(checked, unknown, unsupported),
    }


def ensure_output_columns(raw: pd.DataFrame) -> pd.DataFrame:
    for col in ANOMALY_NUMERIC_COLS:
        if col not in raw.columns:
            raw[col] = np.nan
    for col in ANOMALY_TEXT_COLS:
        if col not in raw.columns:
            raw[col] = ""
    return raw


def write_team_metrics(raw: pd.DataFrame, raw_idx: int, side: str, metrics: dict[str, Any]) -> None:
    for key, value in metrics.items():
        raw.loc[raw_idx, f"{side}_{key}"] = value


def build_summary(raw: pd.DataFrame, target_fixture_ids: set[int], counters: dict[str, int]) -> pd.DataFrame:
    target = raw[raw["fixture_id"].isin(target_fixture_ids)].copy() if target_fixture_ids else raw.iloc[0:0].copy()
    return pd.DataFrame(
        [
            {
                "rows_processed": int(len(target)),
                "clean_rows": int(target.get("recent_sample_cleanliness_flag", pd.Series(dtype=str)).eq("CLEAN").sum()),
                "mixed_rows": int(target.get("recent_sample_cleanliness_flag", pd.Series(dtype=str)).eq("MIXED").sum()),
                "polluted_rows": int(target.get("recent_sample_cleanliness_flag", pd.Series(dtype=str)).eq("POLLUTED").sum()),
                "unknown_event_rows": int(target.get("recent_sample_cleanliness_flag", pd.Series(dtype=str)).eq("UNKNOWN_EVENTS").sum()),
                "home_anomalies": int(pd.to_numeric(target.get("home_recent_anomaly_count_last5"), errors="coerce").fillna(0).sum()) if not target.empty else 0,
                "away_anomalies": int(pd.to_numeric(target.get("away_recent_anomaly_count_last5"), errors="coerce").fillna(0).sum()) if not target.empty else 0,
                "event_fixture_requests": counters.get("event_fixture_requests", 0),
                "event_api_calls": counters.get("event_api_calls", 0),
                "event_cache_hits": counters.get("event_cache_hits", 0),
                "event_errors": counters.get("event_errors", 0),
                "event_coverage_unknown": counters.get("event_coverage_unknown", 0),
                "event_coverage_unsupported": counters.get("event_coverage_unsupported", 0),
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        ]
    )


def write_report(summary: pd.DataFrame, path: Path = OUTPUT_REPORT) -> None:
    lines = [
        "vSIGMA recent fixture anomaly lab layer",
        "",
        "Purpose: reduce trust in recent samples structurally distorted by fixture events.",
        f"Flags: early red <= {EARLY_RED_MAX_MINUTE}', early penalty <= {EARLY_PENALTY_MAX_MINUTE}', first-half shock <= {SHOCK_MAX_MINUTE}', exceptional fixture status.",
        "Activation: event API is used only when official league coverage says events are supported.",
        "Missing or unsupported event coverage is uncertainty, not weakness; it does not create a penalty.",
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
    coverage = load_coverage_matrix()
    client = APIFootballClient()

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= TARGET_MAX_TIER_RANK
    ].copy()

    counters = {
        "event_fixture_requests": 0,
        "event_api_calls": 0,
        "event_cache_hits": 0,
        "event_errors": 0,
        "event_coverage_unknown": 0,
        "event_coverage_unsupported": 0,
    }
    target_fixture_ids: set[int] = set()

    print("\n=== RECENT FIXTURE ANOMALY LAB ===")
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

        home_metrics = compute_team_recent_anomalies(client, home_fixtures, coverage, counters)
        away_metrics = compute_team_recent_anomalies(client, away_fixtures, coverage, counters)

        write_team_metrics(raw, raw_idx, "home", home_metrics)
        write_team_metrics(raw, raw_idx, "away", away_metrics)
        raw.loc[raw_idx, "recent_sample_cleanliness_flag"] = cleanliness_flag(home_metrics, away_metrics)
        raw.loc[raw_idx, "recent_fixture_anomaly_updated_at"] = datetime.now(timezone.utc).isoformat()

        print(
            f"fixture={current_fixture_id} {match.get('home_team')} vs {match.get('away_team')} | "
            f"clean={raw.loc[raw_idx, 'recent_sample_cleanliness_flag']} "
            f"home_anom={home_metrics['recent_anomaly_count_last5']}/{home_metrics['recent_events_checked_last5']} "
            f"away_anom={away_metrics['recent_anomaly_count_last5']}/{away_metrics['recent_events_checked_last5']}"
        )

    raw.to_csv(RAW_MATCHES, index=False)

    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    summary = build_summary(raw, target_fixture_ids, counters)
    summary.to_csv(OUTPUT_SUMMARY, index=False)
    write_report(summary)

    print("\n=== RECENT FIXTURE ANOMALY COMPLETADO ===")
    print(f"Partidos procesados: {len(target_fixture_ids)}")
    print(f"Event API calls: {counters['event_api_calls']}")
    print(f"Event cache hits: {counters['event_cache_hits']}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Summary: {OUTPUT_SUMMARY}")
    print(f"Report: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
