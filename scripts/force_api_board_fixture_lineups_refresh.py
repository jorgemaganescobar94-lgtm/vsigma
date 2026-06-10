from __future__ import annotations

import argparse
import csv
import os
import time
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

PROCESSED = Path("data/processed")
DIRECT_BASE = "https://v3.football.api-sports.io"
RAPID_BASE = "https://api-football-v1.p.rapidapi.com/v3"
MAX_RETRIES = 3
SLEEP_BETWEEN_CALLS = 0.25

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "provider",
    "api_status", "api_note", "team_side", "team_id", "team_name", "formation",
    "row_type", "player_id", "player_name", "player_number", "player_position", "player_grid",
    "api_calls_planned", "api_calls_executed", "source_guard", "lineup_permission",
    "canonical_board_permission", "pick_permission", "stake_permission", "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "fixtures_reviewed", "api_calls_planned", "api_calls_executed",
    "lineup_fixtures_found", "lineup_fixtures_missing", "lineup_rows_written", "starting_xi_rows",
    "substitute_rows", "api_status_counts", "team_side_counts", "provider_counts", "next_action",
    "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def load_board_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_daily_execution_board.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_daily_execution_board.csv")
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        fixture_id = norm(row.get("fixture_id"))
        if not fixture_id or fixture_id in seen:
            continue
        seen.add(fixture_id)
        out.append(row)
    return out


def api_credentials() -> tuple[str, str, dict[str, str]]:
    direct_key = (
        os.getenv("API_FOOTBALL_KEY")
        or os.getenv("APISPORTS_KEY")
        or os.getenv("API_SPORTS_KEY")
        or os.getenv("API_FOOTBALL_API_KEY")
        or os.getenv("APIFOOTBALL_KEY")
    )
    if direct_key:
        return "API-SPORTS_DIRECT", f"{DIRECT_BASE}/fixtures/lineups", {"x-apisports-key": direct_key}
    rapid_key = os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY")
    if rapid_key:
        return "RAPIDAPI", f"{RAPID_BASE}/fixtures/lineups", {
            "x-rapidapi-key": rapid_key,
            "x-rapidapi-host": os.getenv("API_FOOTBALL_HOST", "api-football-v1.p.rapidapi.com"),
        }
    return "NO_PROVIDER", "", {}


def request_lineups(fixture_id: str, provider: str, url: str, headers: dict[str, str]) -> tuple[str, str, list[dict]]:
    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, params={"fixture": fixture_id}, timeout=30)
            if response.status_code == 429:
                last_error = "429 Too Many Requests"
                time.sleep(min(2 ** attempt, 8))
                continue
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict) and payload.get("errors"):
                return "API_ERROR", f"{provider} API errors: {payload.get('errors')}", []
            items = payload.get("response", []) if isinstance(payload, dict) else []
            if not items:
                return "NO_LINEUPS_RETURNED_BY_API", "API returned empty response for this fixture_id", []
            return "OK", "lineups fetched directly by fixture_id", items
        except Exception as exc:
            last_error = str(exc)
            if attempt < MAX_RETRIES:
                time.sleep(min(2 ** attempt, 8))
    return "API_ERROR", last_error, []


def side_for_team(team_name: str, board_row: dict[str, str]) -> str:
    team_up = up(team_name)
    home = up(board_row.get("home_team"))
    away = up(board_row.get("away_team"))
    if team_up == home:
        return "home"
    if team_up == away:
        return "away"
    # Fallback for API aliases/diacritics: containment is only for labeling, not permission.
    if home and (home in team_up or team_up in home):
        return "home_alias"
    if away and (away in team_up or team_up in away):
        return "away_alias"
    return "unknown"


def player_rows(
    day: str,
    generated: str,
    board_row: dict[str, str],
    provider: str,
    api_status: str,
    api_note: str,
    team_item: dict,
    row_type: str,
    players: list,
    calls_planned: int,
    calls_executed: int,
) -> list[dict[str, object]]:
    team = team_item.get("team", {}) if isinstance(team_item.get("team"), dict) else {}
    team_name = norm(team.get("name"))
    team_id = norm(team.get("id"))
    formation = norm(team_item.get("formation"))
    side = side_for_team(team_name, board_row)
    out: list[dict[str, object]] = []
    for entry in players or []:
        player = entry.get("player", {}) if isinstance(entry, dict) and isinstance(entry.get("player"), dict) else {}
        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(board_row.get("fixture_id")),
            "home_team": norm(board_row.get("home_team")),
            "away_team": norm(board_row.get("away_team")),
            "provider": provider,
            "api_status": api_status,
            "api_note": api_note,
            "team_side": side,
            "team_id": team_id,
            "team_name": team_name,
            "formation": formation,
            "row_type": row_type,
            "player_id": norm(player.get("id")),
            "player_name": norm(player.get("name")),
            "player_number": norm(player.get("number")),
            "player_position": norm(player.get("pos")),
            "player_grid": norm(player.get("grid")),
            "api_calls_planned": calls_planned,
            "api_calls_executed": calls_executed,
            "source_guard": "BOARD_FIXTURE_ID_DIRECT_API_LINEUPS",
            "lineup_permission": "API_LINEUP_SNAPSHOT_ONLY",
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def unavailable_row(
    day: str,
    generated: str,
    board_row: dict[str, str],
    provider: str,
    api_status: str,
    api_note: str,
    calls_planned: int,
    calls_executed: int,
) -> dict[str, object]:
    return {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": norm(board_row.get("fixture_id")),
        "home_team": norm(board_row.get("home_team")),
        "away_team": norm(board_row.get("away_team")),
        "provider": provider,
        "api_status": api_status,
        "api_note": api_note,
        "team_side": "none",
        "team_id": "",
        "team_name": "",
        "formation": "",
        "row_type": "NO_LINEUP",
        "player_id": "",
        "player_name": "",
        "player_number": "",
        "player_position": "",
        "player_grid": "",
        "api_calls_planned": calls_planned,
        "api_calls_executed": calls_executed,
        "source_guard": "BOARD_FIXTURE_ID_DIRECT_API_LINEUPS",
        "lineup_permission": "NO_LINEUP_FROM_API",
        "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
        "pick_permission": "NO_PICK_PERMISSION",
        "stake_permission": "NO_STAKE_PERMISSION",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, processed: Path, limit: int):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    board_rows = load_board_rows(processed, day)
    if limit > 0:
        board_rows = board_rows[:limit]
    provider, url, headers = api_credentials()
    calls_planned = len(board_rows) if provider != "NO_PROVIDER" else 0
    calls_executed = 0
    out: list[dict[str, object]] = []

    if not board_rows:
        summary = make_summary(day, generated, out, 0, 0)
        return out, summary, markdown(day, out, summary[0])

    if provider == "NO_PROVIDER":
        for row in board_rows:
            out.append(unavailable_row(day, generated, row, provider, "NO_API_KEY", "No API-Football credential found in environment", 0, 0))
        summary = make_summary(day, generated, out, 0, 0)
        return out, summary, markdown(day, out, summary[0])

    for row in board_rows:
        calls_executed += 1
        fixture_id = norm(row.get("fixture_id"))
        api_status, api_note, lineups = request_lineups(fixture_id, provider, url, headers)
        if api_status != "OK" or not lineups:
            out.append(unavailable_row(day, generated, row, provider, api_status, api_note, calls_planned, calls_executed))
        else:
            for team_item in lineups:
                start_xi = team_item.get("startXI", []) if isinstance(team_item, dict) else []
                substitutes = team_item.get("substitutes", []) if isinstance(team_item, dict) else []
                out.extend(player_rows(day, generated, row, provider, api_status, api_note, team_item, "START_XI", start_xi, calls_planned, calls_executed))
                out.extend(player_rows(day, generated, row, provider, api_status, api_note, team_item, "SUBSTITUTE", substitutes, calls_planned, calls_executed))
        time.sleep(SLEEP_BETWEEN_CALLS)

    summary = make_summary(day, generated, out, calls_planned, calls_executed)
    return out, summary, markdown(day, out, summary[0])


def make_summary(day: str, generated: str, rows: list[dict[str, object]], calls_planned: int, calls_executed: int) -> list[dict[str, object]]:
    fixture_ids = {norm(row.get("fixture_id")) for row in rows if norm(row.get("fixture_id"))}
    found_fixtures = {norm(row.get("fixture_id")) for row in rows if row.get("row_type") in {"START_XI", "SUBSTITUTE"}}
    no_lineup_fixtures = {norm(row.get("fixture_id")) for row in rows if row.get("row_type") == "NO_LINEUP"}
    starting = sum(1 for row in rows if row.get("row_type") == "START_XI")
    subs = sum(1 for row in rows if row.get("row_type") == "SUBSTITUTE")
    return [{
        "target_date": day,
        "generated_at": generated,
        "fixtures_reviewed": len(fixture_ids),
        "api_calls_planned": calls_planned,
        "api_calls_executed": calls_executed,
        "lineup_fixtures_found": len(found_fixtures),
        "lineup_fixtures_missing": len(no_lineup_fixtures),
        "lineup_rows_written": len(rows),
        "starting_xi_rows": starting,
        "substitute_rows": subs,
        "api_status_counts": counts(rows, "api_status"),
        "team_side_counts": counts(rows, "team_side"),
        "provider_counts": counts(rows, "provider"),
        "next_action": "Use direct board fixture_id API lineups as a prelock input only. No automatic pick or stake permission.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Forced API Board Fixture Lineups Refresh - {day}",
        "",
        "## Summary",
        f"- fixtures_reviewed: {summary['fixtures_reviewed']}",
        f"- api_calls_planned: {summary['api_calls_planned']}",
        f"- api_calls_executed: {summary['api_calls_executed']}",
        f"- lineup_fixtures_found: {summary['lineup_fixtures_found']}",
        f"- lineup_fixtures_missing: {summary['lineup_fixtures_missing']}",
        f"- starting_xi_rows: {summary['starting_xi_rows']}",
        f"- substitute_rows: {summary['substitute_rows']}",
        f"- api_status_counts: {summary['api_status_counts']}",
        f"- team_side_counts: {summary['team_side_counts']}",
        f"- provider_counts: {summary['provider_counts']}",
        "- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION",
        "- pick_permission: NO_PICK_PERMISSION",
        "- stake_permission: NO_STAKE_PERMISSION",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Fixture Lineup Status",
    ]
    fixture_map: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        fixture_map.setdefault(norm(row.get("fixture_id")), []).append(row)
    if not fixture_map:
        lines.append("- none. No board fixtures available.")
    for fixture_id, fixture_rows in fixture_map.items():
        sample = fixture_rows[0]
        start_count = sum(1 for row in fixture_rows if row.get("row_type") == "START_XI")
        sub_count = sum(1 for row in fixture_rows if row.get("row_type") == "SUBSTITUTE")
        status = norm(sample.get("api_status"))
        note = norm(sample.get("api_note"))
        lines.append(f"- {sample.get('home_team')} vs {sample.get('away_team')} | fixture_id={fixture_id} | status={status} | starters={start_count} | subs={sub_count} | note={note}")
    lines += ["", "## Starting XI Rows"]
    starters = [row for row in rows if row.get("row_type") == "START_XI"]
    if not starters:
        lines.append("- none.")
    for row in starters[:120]:
        lines.append(f"- {row.get('team_side')} | {row.get('team_name')} | {row.get('formation')} | #{row.get('player_number')} {row.get('player_name')} | pos={row.get('player_position')} | grid={row.get('player_grid')}")
    lines += [
        "",
        "## Guardrails",
        "- This is a direct API-Football lineup snapshot using canonical board fixture_id.",
        "- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.",
        "- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.",
    ]
    return "\n".join(lines) + "\n"


def replace_or_append_section(text: str, section: str, block: str) -> str:
    if section not in text:
        return text.rstrip() + block
    before = text.split(section, 1)[0].rstrip()
    after = text.split(section, 1)[1]
    next_idx = after.find("\n## ")
    tail = after[next_idx:] if next_idx >= 0 else ""
    return before + block + tail


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    section = "## Forced API Board Fixture Lineups Refresh"
    lines = [
        section,
        f"- fixtures_reviewed: {summary.get('fixtures_reviewed', 'UNKNOWN')}",
        f"- api_calls_executed: {summary.get('api_calls_executed', 'UNKNOWN')}",
        f"- lineup_fixtures_found: {summary.get('lineup_fixtures_found', 'UNKNOWN')}",
        f"- lineup_fixtures_missing: {summary.get('lineup_fixtures_missing', 'UNKNOWN')}",
        f"- starting_xi_rows: {summary.get('starting_xi_rows', 'UNKNOWN')}",
        f"- substitute_rows: {summary.get('substitute_rows', 'UNKNOWN')}",
        f"- api_status_counts: {summary.get('api_status_counts', 'UNKNOWN')}",
        f"- pick_permission: NO_PICK_PERMISSION",
        f"- stake_permission: NO_STAKE_PERMISSION",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            md_path.write_text(replace_or_append_section(text, section, block), encoding="utf-8")


def run(day: str, tz: str, processed: Path, limit: int) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed, limit)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_forced_api_board_fixture_lineups.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_forced_api_board_fixture_lineups_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_forced_api_board_fixture_lineups.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA FORCED API BOARD FIXTURE LINEUPS REFRESH ===")
    print(f"fixtures_reviewed={summary[0]['fixtures_reviewed']}")
    print(f"api_calls_executed={summary[0]['api_calls_executed']}")
    print(f"lineup_fixtures_found={summary[0]['lineup_fixtures_found']}")
    print(f"lineup_fixtures_missing={summary[0]['lineup_fixtures_missing']}")
    print(f"pick_permission=NO_PICK_PERMISSION")
    print(f"stake_permission=NO_STAKE_PERMISSION")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir, args.limit)


if __name__ == "__main__":
    main()
