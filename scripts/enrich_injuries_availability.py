from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import math
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
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_injuries_availability_backup.csv"
OUTPUT_REPORT = ROOT / "data" / "processed" / "injuries_availability_enrichment_report.csv"

TARGET_MAX_TIER_RANK = 2
COVERAGE_FLAGS = {"FULL", "PARTIAL", "SPARSE", "NONE"}
SEVERITY_FLAGS = {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}


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
    # Coverage absence is data uncertainty. Only explicit official 0 disables
    # injury lookups; it never becomes team weakness.
    if value is None or pd.isna(value):
        return True
    try:
        return int(float(value)) == 1
    except Exception:
        return str(value).strip().lower() in {"1", "true", "yes"}


def cache_has_valid_injuries(client: APIFootballClient, fixture: int) -> bool:
    params_key = build_params_key("/injuries", {"fixture": fixture})
    return client._get_cached(params_key) is not None


def parse_injury_item(item: dict[str, Any]) -> dict[str, Any]:
    player = item.get("player") or {}
    team = item.get("team") or {}
    fixture = item.get("fixture") or {}
    league = item.get("league") or {}
    return {
        "fixture_id": safe_int(fixture.get("id")),
        "team_id": safe_int(team.get("id")),
        "team_name": team.get("name"),
        "player_id": safe_int(player.get("id")),
        "player_name": player.get("name"),
        "type": norm_text(player.get("type")),
        "reason": norm_text(player.get("reason")),
        "league_id": safe_int(league.get("id")),
        "season": safe_int(league.get("season")),
    }


def parse_injuries_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in payload.get("response", []) or []:
        parsed = parse_injury_item(item)
        if parsed["team_id"] is not None:
            rows.append(parsed)
    return rows


def injury_weight(row: dict[str, Any]) -> float:
    text = f"{row.get('type', '')} {row.get('reason', '')}".lower()
    if any(token in text for token in ["suspended", "suspension", "red card"]):
        return 1.0
    if any(token in text for token in ["doubt", "doubtful", "questionable", "illness", "knock"]):
        return 0.6
    if any(token in text for token in ["injury", "injured", "muscle", "knee", "ankle", "hamstring"]):
        return 1.0
    return 0.8


def severity_flag(risk_score: float | None, coverage_flag: str) -> str:
    if coverage_flag not in {"FULL", "PARTIAL", "SPARSE"} or risk_score is None or pd.isna(risk_score):
        return "UNKNOWN"
    if risk_score >= 3.0:
        return "HIGH"
    if risk_score >= 1.5:
        return "MEDIUM"
    return "LOW"


def fixture_coverage_flag(injury_rows: list[dict[str, Any]], home_team_id: int | None, away_team_id: int | None) -> str:
    if not injury_rows:
        return "NONE"
    if home_team_id is None or away_team_id is None:
        return "SPARSE"

    team_ids = {row.get("team_id") for row in injury_rows if row.get("team_id") is not None}
    if team_ids & {home_team_id, away_team_id}:
        return "FULL"
    return "SPARSE"


def team_features(
    injury_rows: list[dict[str, Any]],
    team_id: int | None,
    fixture_coverage: str,
) -> dict[str, Any]:
    if fixture_coverage == "NONE" or team_id is None:
        return {
            "injuries_count": np.nan,
            "injuries_available_flag": 0,
            "injuries_coverage_flag": "NONE",
            "absence_risk_score": np.nan,
            "absence_severity_flag": "UNKNOWN",
            "legacy_absences": np.nan,
        }

    team_rows = [row for row in injury_rows if row.get("team_id") == team_id]
    count = len(team_rows)
    risk = round(sum(injury_weight(row) for row in team_rows), 3)
    coverage = fixture_coverage if fixture_coverage in COVERAGE_FLAGS else "SPARSE"
    return {
        "injuries_count": count,
        "injuries_available_flag": 1,
        "injuries_coverage_flag": coverage,
        "absence_risk_score": risk,
        "absence_severity_flag": severity_flag(risk, coverage),
        "legacy_absences": count,
    }


def injuries_quality_flag(home_coverage: str, away_coverage: str) -> str:
    if home_coverage == "FULL" and away_coverage == "FULL":
        return "FULL"
    if home_coverage in {"FULL", "PARTIAL"} and away_coverage in {"FULL", "PARTIAL"}:
        return "PARTIAL"
    if home_coverage != "NONE" or away_coverage != "NONE":
        return "SPARSE"
    return "NONE"


def build_availability_features(
    payload: dict[str, Any],
    home_team_id: int | None,
    away_team_id: int | None,
) -> dict[str, Any]:
    injury_rows = parse_injuries_payload(payload)
    fixture_coverage = fixture_coverage_flag(injury_rows, home_team_id, away_team_id)
    home = team_features(injury_rows, home_team_id, fixture_coverage)
    away = team_features(injury_rows, away_team_id, fixture_coverage)
    quality = injuries_quality_flag(home["injuries_coverage_flag"], away["injuries_coverage_flag"])

    return {
        "home_injuries_count": home["injuries_count"],
        "away_injuries_count": away["injuries_count"],
        "home_injuries_available_flag": home["injuries_available_flag"],
        "away_injuries_available_flag": away["injuries_available_flag"],
        "home_injuries_coverage_flag": home["injuries_coverage_flag"],
        "away_injuries_coverage_flag": away["injuries_coverage_flag"],
        "home_absence_risk_score": home["absence_risk_score"],
        "away_absence_risk_score": away["absence_risk_score"],
        "home_absence_severity_flag": home["absence_severity_flag"],
        "away_absence_severity_flag": away["absence_severity_flag"],
        "injuries_quality_flag": quality,
        "home_absences": home["legacy_absences"],
        "away_absences": away["legacy_absences"],
        "injuries_availability_updated_at": datetime.now(timezone.utc).isoformat(),
    }


def ensure_output_columns(raw: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        "home_injuries_count",
        "away_injuries_count",
        "home_injuries_available_flag",
        "away_injuries_available_flag",
        "home_absence_risk_score",
        "away_absence_risk_score",
        "home_absences",
        "away_absences",
    ]
    text_cols = [
        "home_injuries_coverage_flag",
        "away_injuries_coverage_flag",
        "home_absence_severity_flag",
        "away_absence_severity_flag",
        "injuries_quality_flag",
        "injuries_availability_updated_at",
    ]
    for col in numeric_cols:
        if col not in raw.columns:
            raw[col] = np.nan
    for col in text_cols:
        if col not in raw.columns:
            raw[col] = ""
    return raw


def write_features(raw: pd.DataFrame, raw_idx: int, features: dict[str, Any]) -> None:
    for col, value in features.items():
        raw.loc[raw_idx, col] = value


def fetch_fixture_injuries(
    client: APIFootballClient,
    fixture_id: int,
    counters: dict[str, int],
) -> dict[str, Any] | None:
    if cache_has_valid_injuries(client, fixture_id):
        counters["cache_hits"] += 1
    else:
        counters["api_calls_made"] += 1

    try:
        return client.injuries(fixture=fixture_id)
    except APIFootballError as exc:
        counters["api_errors"] += 1
        if exc.is_plan_limit:
            counters["plan_limit_errors"] += 1
        return None
    except Exception:
        counters["api_errors"] += 1
        return None


def build_report(rows_processed: int, counters: dict[str, int], target: pd.DataFrame) -> pd.DataFrame:
    quality = target.get("injuries_quality_flag", pd.Series(dtype="object")).fillna("NONE").astype(str)
    known_counts = pd.concat(
        [
            pd.to_numeric(target.get("home_injuries_count"), errors="coerce"),
            pd.to_numeric(target.get("away_injuries_count"), errors="coerce"),
        ],
        ignore_index=True,
    )
    return pd.DataFrame(
        [
            {
                "rows_processed": rows_processed,
                "full_rows": int(quality.eq("FULL").sum()),
                "partial_rows": int(quality.eq("PARTIAL").sum()),
                "sparse_rows": int(quality.eq("SPARSE").sum()),
                "none_rows": int(quality.eq("NONE").sum()),
                "api_calls_made": counters.get("api_calls_made", 0),
                "cache_hits": counters.get("cache_hits", 0),
                "api_errors": counters.get("api_errors", 0),
                "plan_limit_errors": counters.get("plan_limit_errors", 0),
                "avg_injuries_count_known": round(float(known_counts.dropna().mean()), 3)
                if not known_counts.dropna().empty
                else np.nan,
                "unknown_coverage_rows": int(quality.eq("NONE").sum()),
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

    targets = filtered[
        pd.to_numeric(filtered["league_tier_rank"], errors="coerce") <= TARGET_MAX_TIER_RANK
    ].copy()

    counters = {
        "api_calls_made": 0,
        "cache_hits": 0,
        "api_errors": 0,
        "plan_limit_errors": 0,
    }
    target_fixture_ids: set[int] = set()
    rows_processed = 0

    print("\n=== ENRIQUECIMIENTO INJURIES / AVAILABILITY ===")
    print(f"Partidos filtrados totales: {len(filtered)}")
    print(f"Partidos objetivo TIER_1/TIER_2: {len(targets)}")
    print("Modo: /injuries por fixture; respuesta vacia se conserva como cobertura NONE")

    for _, match in targets.iterrows():
        fixture_id = safe_int(match.get("fixture_id"))
        if fixture_id is None:
            continue
        raw_idx_list = raw.index[raw["fixture_id"] == fixture_id].tolist()
        if not raw_idx_list:
            continue

        raw_idx = raw_idx_list[0]
        target_fixture_ids.add(fixture_id)
        rows_processed += 1

        if not coverage_flag_allows(match.get("league_has_injuries_coverage", np.nan)):
            payload = {"response": []}
            features = build_availability_features(payload, None, None)
            features["injuries_quality_flag"] = "NONE"
            features["injuries_availability_updated_at"] = datetime.now(timezone.utc).isoformat()
            write_features(raw, raw_idx, features)
            print(
                f"SKIP_COVERAGE fixture={fixture_id} {match.get('home_team')} vs {match.get('away_team')} | "
                "official league coverage has injuries=false"
            )
            continue

        payload = fetch_fixture_injuries(client, fixture_id, counters)
        if payload is None:
            features = build_availability_features({"response": []}, None, None)
        else:
            features = build_availability_features(
                payload=payload,
                home_team_id=safe_int(match.get("home_team_id")),
                away_team_id=safe_int(match.get("away_team_id")),
            )
        write_features(raw, raw_idx, features)

        print(
            f"{features['injuries_quality_flag']} fixture={fixture_id} "
            f"{match.get('home_team')} vs {match.get('away_team')} | "
            f"home={features['home_injuries_count']} {features['home_absence_severity_flag']} "
            f"away={features['away_injuries_count']} {features['away_absence_severity_flag']}"
        )

    raw.to_csv(RAW_MATCHES, index=False)

    target = raw[raw["fixture_id"].isin(target_fixture_ids)].copy() if target_fixture_ids else raw.iloc[0:0].copy()
    report = build_report(rows_processed, counters, target)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT_REPORT, index=False)

    print("\n=== INJURIES / AVAILABILITY COMPLETADO ===")
    print(f"Partidos procesados: {rows_processed}")
    print(f"FULL: {int(report.loc[0, 'full_rows'])}")
    print(f"PARTIAL: {int(report.loc[0, 'partial_rows'])}")
    print(f"SPARSE: {int(report.loc[0, 'sparse_rows'])}")
    print(f"NONE: {int(report.loc[0, 'none_rows'])}")
    print(f"API calls made: {counters['api_calls_made']}")
    print(f"Cache hits: {counters['cache_hits']}")
    print(f"CSV actualizado: {RAW_MATCHES}")
    print(f"Reporte: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
