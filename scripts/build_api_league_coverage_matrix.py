from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_MATRIX = OUTPUT_DIR / "vsigma_api_league_coverage_matrix.csv"
OUTPUT_SUMMARY = OUTPUT_DIR / "vsigma_api_league_coverage_summary.csv"
OUTPUT_REPORT = OUTPUT_DIR / "vsigma_api_league_coverage_report.txt"

CORE_FAMILY_COLUMNS = [
    "league_has_fixtures_coverage",
    "league_has_standings_coverage",
    "league_has_odds_coverage",
    "league_has_fixture_stats_coverage",
    "league_has_injuries_coverage",
    "league_has_lineups_coverage",
]

COVERAGE_OUTPUT_COLUMNS = [
    "league_coverage_class",
    "league_has_odds_coverage",
    "league_has_fixture_stats_coverage",
    "league_has_injuries_coverage",
    "league_has_lineups_coverage",
    "league_has_predictions_coverage",
    "league_coverage_rich_flag",
    "league_data_reliability_score",
    "league_coverage_source_status",
    "league_coverage_note",
]

MATRIX_OUTPUT_COLUMNS = [
    "league_id",
    "league",
    "country",
    "season",
    "league_type",
    "coverage_season_current",
    "coverage_season_start",
    "coverage_season_end",
    "league_has_fixtures_coverage",
    "league_has_standings_coverage",
    "league_has_odds_coverage",
    "league_has_events_coverage",
    "league_has_lineups_coverage",
    "league_has_fixture_stats_coverage",
    "league_has_player_stats_coverage",
    "league_has_players_coverage",
    "league_has_injuries_coverage",
    "league_has_predictions_coverage",
    "league_has_top_scorers_coverage",
    "league_has_top_assists_coverage",
    "league_has_top_cards_coverage",
    "league_coverage_class",
    "league_coverage_rich_flag",
    "league_data_reliability_score",
    "league_coverage_source_status",
    "league_coverage_note",
    "coverage_matrix_generated_at_utc",
]


def safe_int(value: Any) -> int | None:
    try:
        if value is None or pd.isna(value):
            return None
        return int(float(value))
    except Exception:
        return None


def safe_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    if isinstance(value, (int, float)):
        return bool(int(value))
    text = str(value).strip().lower()
    return text in {"1", "true", "yes", "y", "si", "sí"}


def norm_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def coverage_class_from_flags(flags: dict[str, bool]) -> tuple[str, float]:
    # Weighted only by families vSIGMA currently uses or can use directly.
    weights = {
        "league_has_fixtures_coverage": 2.0,
        "league_has_standings_coverage": 1.0,
        "league_has_odds_coverage": 1.25,
        "league_has_fixture_stats_coverage": 2.0,
        "league_has_injuries_coverage": 1.0,
        "league_has_lineups_coverage": 1.0,
    }
    score = sum(weight for col, weight in weights.items() if flags.get(col, False))

    if score >= 7.0:
        return "COVERAGE_RICH", 0.95
    if score >= 5.5:
        return "COVERAGE_GOOD", 0.85
    if score >= 3.5:
        return "COVERAGE_PARTIAL", 0.70
    if score >= 2.0:
        return "COVERAGE_THIN", 0.55
    return "COVERAGE_MINIMAL", 0.40


def pick_season(seasons: list[dict[str, Any]], requested_season: int | None) -> dict[str, Any] | None:
    if not seasons:
        return None
    if requested_season is not None:
        for season in seasons:
            if safe_int(season.get("year")) == requested_season:
                return season
    for season in seasons:
        if safe_bool(season.get("current")):
            return season
    return sorted(seasons, key=lambda item: safe_int(item.get("year")) or 0, reverse=True)[0]


def normalize_league_coverage_item(
    item: dict[str, Any],
    requested_season: int | None = None,
    source_status: str = "OFFICIAL_API",
    note: str = "",
) -> dict[str, Any]:
    league = item.get("league") or {}
    country = item.get("country") or {}
    season = pick_season(item.get("seasons") or [], requested_season) or {}
    coverage = season.get("coverage") or {}
    fixture_coverage = coverage.get("fixtures") or {}

    flags = {
        "league_has_fixtures_coverage": bool(season),
        "league_has_standings_coverage": safe_bool(coverage.get("standings")),
        "league_has_odds_coverage": safe_bool(coverage.get("odds")),
        "league_has_events_coverage": safe_bool(fixture_coverage.get("events")),
        "league_has_lineups_coverage": safe_bool(fixture_coverage.get("lineups")),
        "league_has_fixture_stats_coverage": safe_bool(fixture_coverage.get("statistics_fixtures")),
        "league_has_player_stats_coverage": safe_bool(fixture_coverage.get("statistics_players")),
        "league_has_players_coverage": safe_bool(coverage.get("players")),
        "league_has_injuries_coverage": safe_bool(coverage.get("injuries")),
        "league_has_predictions_coverage": safe_bool(coverage.get("predictions")),
        "league_has_top_scorers_coverage": safe_bool(coverage.get("top_scorers")),
        "league_has_top_assists_coverage": safe_bool(coverage.get("top_assists")),
        "league_has_top_cards_coverage": safe_bool(coverage.get("top_cards")),
    }
    coverage_class, reliability = coverage_class_from_flags(flags)

    row = {
        "league_id": safe_int(league.get("id")),
        "league": norm_text(league.get("name")),
        "country": norm_text(country.get("name")),
        "season": safe_int(season.get("year")) or requested_season,
        "league_type": norm_text(league.get("type")),
        "coverage_season_current": int(safe_bool(season.get("current"))),
        "coverage_season_start": norm_text(season.get("start")),
        "coverage_season_end": norm_text(season.get("end")),
        **{col: int(value) for col, value in flags.items()},
        "league_coverage_class": coverage_class,
        "league_coverage_rich_flag": int(coverage_class in {"COVERAGE_RICH", "COVERAGE_GOOD"}),
        "league_data_reliability_score": reliability,
        "league_coverage_source_status": source_status,
        "league_coverage_note": note,
        "coverage_matrix_generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    return row


def unknown_coverage_row(match: pd.Series, status: str, note: str) -> dict[str, Any]:
    flags = {col: False for col in CORE_FAMILY_COLUMNS}
    coverage_class, reliability = coverage_class_from_flags(flags)
    row = {
        "league_id": safe_int(match.get("league_id")),
        "league": norm_text(match.get("league")),
        "country": norm_text(match.get("country")),
        "season": safe_int(match.get("season")),
        "league_type": "",
        "coverage_season_current": 0,
        "coverage_season_start": "",
        "coverage_season_end": "",
        "league_has_events_coverage": 0,
        "league_has_player_stats_coverage": 0,
        "league_has_players_coverage": 0,
        "league_has_top_scorers_coverage": 0,
        "league_has_top_assists_coverage": 0,
        "league_has_top_cards_coverage": 0,
        **{col: 0 for col in CORE_FAMILY_COLUMNS},
        "league_has_predictions_coverage": 0,
        "league_coverage_class": coverage_class,
        "league_coverage_rich_flag": 0,
        "league_data_reliability_score": reliability,
        "league_coverage_source_status": status,
        "league_coverage_note": note,
        "coverage_matrix_generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    return row


def normalize_leagues_payload(
    payload: dict[str, Any],
    requested_league_id: int | None = None,
    requested_season: int | None = None,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in payload.get("response", []) or []:
        row = normalize_league_coverage_item(item, requested_season=requested_season)
        if requested_league_id is not None and row["league_id"] != requested_league_id:
            continue
        rows.append(row)
    return pd.DataFrame(rows, columns=MATRIX_OUTPUT_COLUMNS)


def read_target_leagues(path: Path = FILTERED_MATCHES) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing filtered matches for coverage matrix: {path}")
    matches = pd.read_csv(path)
    if matches.empty:
        return pd.DataFrame(columns=["league_id", "season", "league", "country"])

    needed = ["league_id", "season", "league", "country"]
    for col in needed:
        if col not in matches.columns:
            matches[col] = pd.NA
    targets = matches[needed].drop_duplicates().copy()
    targets["_league_id_sort"] = pd.to_numeric(targets["league_id"], errors="coerce")
    targets["_season_sort"] = pd.to_numeric(targets["season"], errors="coerce")
    return targets.sort_values(["_league_id_sort", "_season_sort", "country", "league"]).drop(
        columns=["_league_id_sort", "_season_sort"],
    )


def build_matrix_for_targets(targets: pd.DataFrame, client: APIFootballClient) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, target in targets.iterrows():
        league_id = safe_int(target.get("league_id"))
        season = safe_int(target.get("season"))
        if league_id is None:
            rows.append(unknown_coverage_row(target, "MISSING_LEAGUE_ID", "No league_id available for /leagues lookup."))
            continue

        try:
            payload = client.leagues(id=league_id, season=season) if season is not None else client.leagues(id=league_id)
            normalized = normalize_leagues_payload(payload, league_id, season)
            if normalized.empty and season is not None:
                payload = client.leagues(id=league_id)
                normalized = normalize_leagues_payload(payload, league_id, season)

            if normalized.empty:
                rows.append(
                    unknown_coverage_row(
                        target,
                        "OFFICIAL_API_NO_SEASON_MATCH",
                        "Official /leagues metadata returned no matching league/season.",
                    )
                )
            else:
                rows.append(normalized.iloc[0].to_dict())
        except APIFootballError as exc:
            rows.append(
                unknown_coverage_row(
                    target,
                    "OFFICIAL_API_ERROR",
                    f"/leagues error: {str(exc)}",
                )
            )
        except Exception as exc:
            rows.append(
                unknown_coverage_row(
                    target,
                    "COVERAGE_MATRIX_ERROR",
                    f"Coverage lookup failed: {exc}",
                )
            )

    return pd.DataFrame(rows, columns=MATRIX_OUTPUT_COLUMNS)


def build_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    rows.append({"summary_scope": "overall", "metric": "leagues_total", "rows_total": int(len(matrix))})
    for col in [
        "league_coverage_class",
        "league_has_standings_coverage",
        "league_has_odds_coverage",
        "league_has_fixture_stats_coverage",
        "league_has_injuries_coverage",
        "league_has_lineups_coverage",
        "league_has_predictions_coverage",
    ]:
        if matrix.empty or col not in matrix.columns:
            continue
        grouped = matrix.groupby(col, dropna=False).size().reset_index(name="rows_total")
        for _, row in grouped.iterrows():
            rows.append(
                {
                    "summary_scope": f"by_{col}",
                    "metric": col,
                    col: row[col],
                    "rows_total": int(row["rows_total"]),
                }
            )
    return pd.DataFrame(rows)


def write_report(matrix: pd.DataFrame, path: Path = OUTPUT_REPORT) -> None:
    lines = [
        "vSIGMA API league coverage matrix",
        "",
        "Source: official API-Football /leagues coverage metadata. Historical runs use current retrieved metadata for the requested season and do not claim exact coverage drift.",
        "",
    ]
    if matrix.empty:
        lines.append("No accepted leagues were available for coverage classification.")
    else:
        display = matrix.sort_values(["league_coverage_class", "country", "league"])[
            [
                "country",
                "league",
                "season",
                "league_coverage_class",
                "league_data_reliability_score",
                "league_has_fixture_stats_coverage",
                "league_has_odds_coverage",
                "league_has_injuries_coverage",
                "league_has_lineups_coverage",
                "league_coverage_source_status",
            ]
        ]
        rich = display[display["league_coverage_class"].isin(["COVERAGE_RICH", "COVERAGE_GOOD"])]
        thin = display[display["league_coverage_class"].isin(["COVERAGE_THIN", "COVERAGE_MINIMAL"])]
        partial = display[display["league_coverage_class"].eq("COVERAGE_PARTIAL")]

        lines.append("Data-rich / good leagues:")
        lines.append(rich.to_string(index=False) if not rich.empty else "None")
        lines.extend(["", "Partial leagues:"])
        lines.append(partial.to_string(index=False) if not partial.empty else "None")
        lines.extend(["", "Thin / minimal leagues:"])
        lines.append(thin.to_string(index=False) if not thin.empty else "None")

    path.write_text("\n".join(lines), encoding="utf-8")


def merge_coverage_into_matches(matches: pd.DataFrame, matrix: pd.DataFrame) -> pd.DataFrame:
    if matches.empty:
        return matches.copy()

    out = matches.copy()
    for col in COVERAGE_OUTPUT_COLUMNS:
        out = out.drop(columns=[col], errors="ignore")

    matrix_cols = ["league_id", "season", *COVERAGE_OUTPUT_COLUMNS]
    joinable = matrix[matrix_cols].copy() if not matrix.empty else pd.DataFrame(columns=matrix_cols)
    out["_league_id_key"] = pd.to_numeric(out.get("league_id"), errors="coerce").astype("Int64")
    out["_season_key"] = pd.to_numeric(out.get("season"), errors="coerce").astype("Int64")
    joinable["_league_id_key"] = pd.to_numeric(joinable.get("league_id"), errors="coerce").astype("Int64")
    joinable["_season_key"] = pd.to_numeric(joinable.get("season"), errors="coerce").astype("Int64")

    merged = out.merge(
        joinable.drop(columns=["league_id", "season"]),
        on=["_league_id_key", "_season_key"],
        how="left",
    )

    merged["league_coverage_class"] = merged["league_coverage_class"].fillna("COVERAGE_UNKNOWN")
    merged["league_data_reliability_score"] = pd.to_numeric(
        merged["league_data_reliability_score"],
        errors="coerce",
    ).fillna(1.0)
    merged["league_coverage_rich_flag"] = pd.to_numeric(
        merged["league_coverage_rich_flag"],
        errors="coerce",
    ).fillna(0).astype(int)
    for col in [
        "league_has_odds_coverage",
        "league_has_fixture_stats_coverage",
        "league_has_injuries_coverage",
        "league_has_lineups_coverage",
        "league_has_predictions_coverage",
    ]:
        merged[col] = pd.to_numeric(merged[col], errors="coerce")
    merged["league_coverage_source_status"] = merged["league_coverage_source_status"].fillna("COVERAGE_NOT_LOADED")
    merged["league_coverage_note"] = merged["league_coverage_note"].fillna("")

    return merged.drop(columns=["_league_id_key", "_season_key"], errors="ignore")


def update_active_match_files(matrix: pd.DataFrame) -> None:
    for path in [RAW_MATCHES, FILTERED_MATCHES]:
        if not path.exists():
            continue
        matches = pd.read_csv(path)
        merged = merge_coverage_into_matches(matches, matrix)
        merged.to_csv(path, index=False)


def build_api_league_coverage_matrix(
    filtered_matches_path: Path = FILTERED_MATCHES,
    output_dir: Path = OUTPUT_DIR,
    update_matches: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)
    targets = read_target_leagues(filtered_matches_path)
    client = APIFootballClient(default_ttl_hours=24 * 7)
    matrix = build_matrix_for_targets(targets, client)
    matrix = matrix.drop_duplicates(["league_id", "season", "league", "country"], keep="last")
    summary = build_summary(matrix)

    matrix.to_csv(output_dir / OUTPUT_MATRIX.name, index=False)
    summary.to_csv(output_dir / OUTPUT_SUMMARY.name, index=False)
    write_report(matrix, output_dir / OUTPUT_REPORT.name)
    if update_matches:
        update_active_match_files(matrix)
    return matrix, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build official API-Football league coverage matrix for active vSIGMA leagues.")
    parser.add_argument("--filtered-matches", default=str(FILTERED_MATCHES))
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    parser.add_argument("--no-update-matches", action="store_true")
    args = parser.parse_args()

    matrix, summary = build_api_league_coverage_matrix(
        filtered_matches_path=Path(args.filtered_matches),
        output_dir=Path(args.output_dir),
        update_matches=not args.no_update_matches,
    )

    print("\n=== API LEAGUE COVERAGE MATRIX COMPLETADO ===")
    print(f"Leagues classified: {len(matrix)}")
    print(f"Matrix: {Path(args.output_dir) / OUTPUT_MATRIX.name}")
    print(f"Summary: {Path(args.output_dir) / OUTPUT_SUMMARY.name}")
    print(f"Report: {Path(args.output_dir) / OUTPUT_REPORT.name}")
    if not matrix.empty:
        cols = ["country", "league", "season", "league_coverage_class", "league_data_reliability_score"]
        print("\nCurrent accepted league coverage:")
        print(matrix[cols].sort_values(["country", "league"]).to_string(index=False))
    print("\nSummary:")
    print(summary.to_string(index=False) if not summary.empty else "No summary rows")


if __name__ == "__main__":
    main()
