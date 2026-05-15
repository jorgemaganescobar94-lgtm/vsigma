from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import pandas as pd

from api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "processed"
OUTPUT_JSON = OUTPUT_DIR / "api_plan_report.json"
OUTPUT_CSV = OUTPUT_DIR / "api_plan_report.csv"

TEST_LEAGUE_ID = 39          # Premier League
TEST_CURRENT_SEASON = datetime.now(timezone.utc).year
TEST_ALLOWED_SEASON = 2024


def count_response(payload: dict) -> int:
    response = payload.get("response")
    if isinstance(response, list):
        return len(response)
    if response is None:
        return 0
    return 1


def safe_first_fixture_id(payload: dict) -> int | None:
    response = payload.get("response", [])
    if not response:
        return None

    first = response[0]
    return first.get("fixture", {}).get("id")


def run_check(name: str, fn):
    try:
        payload = fn()
        return {
            "check_name": name,
            "result": "OK",
            "response_count": count_response(payload),
            "note": "",
        }, payload
    except APIFootballError as e:
        return {
            "check_name": name,
            "result": "PLAN_LIMIT" if e.is_plan_limit else "API_ERROR",
            "response_count": 0,
            "note": str(e),
        }, None
    except Exception as e:
        return {
            "check_name": name,
            "result": "ERROR",
            "response_count": 0,
            "note": str(e),
        }, None


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = APIFootballClient(default_ttl_hours=24 * 7)

    rows = []
    payloads = {}

    status_row, status_payload = run_check(
        "status_endpoint",
        lambda: client.status()
    )
    rows.append(status_row)
    payloads["status_endpoint"] = status_payload

    leagues_2024_row, leagues_2024_payload = run_check(
        "leagues_allowed_season_2024",
        lambda: client.leagues(id=TEST_LEAGUE_ID, season=TEST_ALLOWED_SEASON)
    )
    rows.append(leagues_2024_row)
    payloads["leagues_allowed_season_2024"] = leagues_2024_payload

    leagues_current_row, leagues_current_payload = run_check(
        f"leagues_current_season_{TEST_CURRENT_SEASON}",
        lambda: client.leagues(id=TEST_LEAGUE_ID, season=TEST_CURRENT_SEASON)
    )
    rows.append(leagues_current_row)
    payloads[f"leagues_current_season_{TEST_CURRENT_SEASON}"] = leagues_current_payload

    fixtures_2024_row, fixtures_2024_payload = run_check(
        "fixtures_allowed_season_2024_last1",
        lambda: client.fixtures(league=TEST_LEAGUE_ID, season=TEST_ALLOWED_SEASON, last=1)
    )
    rows.append(fixtures_2024_row)
    payloads["fixtures_allowed_season_2024_last1"] = fixtures_2024_payload

    fixtures_current_row, fixtures_current_payload = run_check(
        f"fixtures_current_season_{TEST_CURRENT_SEASON}_last1",
        lambda: client.fixtures(league=TEST_LEAGUE_ID, season=TEST_CURRENT_SEASON, last=1)
    )
    rows.append(fixtures_current_row)
    payloads[f"fixtures_current_season_{TEST_CURRENT_SEASON}_last1"] = fixtures_current_payload

    team_last_row, team_last_payload = run_check(
        "team_recent_fixtures_2024_last8",
        lambda: client.fixtures(team=33, league=TEST_LEAGUE_ID, season=TEST_ALLOWED_SEASON, last=8)
    )
    rows.append(team_last_row)
    payloads["team_recent_fixtures_2024_last8"] = team_last_payload

    standings_row, standings_payload = run_check(
        "standings_2024",
        lambda: client.standings(league=TEST_LEAGUE_ID, season=TEST_ALLOWED_SEASON)
    )
    rows.append(standings_row)
    payloads["standings_2024"] = standings_payload

    last_finished_fixture_id = safe_first_fixture_id(fixtures_2024_payload) if fixtures_2024_payload else None

    if last_finished_fixture_id is not None:
        stats_row, stats_payload = run_check(
            f"fixture_statistics_{last_finished_fixture_id}",
            lambda: client.fixture_statistics(last_finished_fixture_id)
        )
        rows.append(stats_row)
        payloads[f"fixture_statistics_{last_finished_fixture_id}"] = stats_payload

        lineups_row, lineups_payload = run_check(
            f"fixture_lineups_{last_finished_fixture_id}",
            lambda: client.fixture_lineups(last_finished_fixture_id)
        )
        rows.append(lineups_row)
        payloads[f"fixture_lineups_{last_finished_fixture_id}"] = lineups_payload
    else:
        rows.append({
            "check_name": "fixture_statistics_check",
            "result": "SKIPPED",
            "response_count": 0,
            "note": "No pude obtener fixture_id de una fixture histórica permitida.",
        })
        rows.append({
            "check_name": "fixture_lineups_check",
            "result": "SKIPPED",
            "response_count": 0,
            "note": "No pude obtener fixture_id de una fixture histórica permitida.",
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "test_league_id": TEST_LEAGUE_ID,
        "test_allowed_season": TEST_ALLOWED_SEASON,
        "test_current_season": TEST_CURRENT_SEASON,
        "checks": rows,
        "derived_flags": {
            "can_use_status": bool(((df["check_name"] == "status_endpoint") & (df["result"] == "OK")).any()),
            "can_use_leagues_2024": bool(((df["check_name"] == "leagues_allowed_season_2024") & (df["result"] == "OK")).any()),
            "can_use_leagues_current": bool((((df["check_name"] == f"leagues_current_season_{TEST_CURRENT_SEASON}") & (df["result"] == "OK")).any())),
            "can_use_fixtures_2024": bool(((df["check_name"] == "fixtures_allowed_season_2024_last1") & (df["result"] == "OK")).any()),
            "can_use_fixtures_current": bool((((df["check_name"] == f"fixtures_current_season_{TEST_CURRENT_SEASON}_last1") & (df["result"] == "OK")).any())),
            "can_use_team_recent_last8_2024": bool(((df["check_name"] == "team_recent_fixtures_2024_last8") & (df["result"] == "OK")).any()),
            "can_use_standings_2024": bool(((df["check_name"] == "standings_2024") & (df["result"] == "OK")).any()),
            "current_season_blocked": bool((((df["check_name"] == f"fixtures_current_season_{TEST_CURRENT_SEASON}_last1") & (df["result"] == "PLAN_LIMIT")).any())),
        },
    }

    OUTPUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== CHECK API PLAN COMPLETADO ===")
    print(f"Reporte CSV: {OUTPUT_CSV}")
    print(f"Reporte JSON: {OUTPUT_JSON}")
    print("\nResultados:")
    print(df.to_string(index=False))

    print("\nFlags derivados:")
    for key, value in summary["derived_flags"].items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()