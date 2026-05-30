from __future__ import annotations

import argparse
import csv
import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
RAW = Path("data/raw")
OUT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "team_side", "source_name", "official_xi", "players_count", "formation", "coach_name",
    "api_status", "source_guard", "auto_apply", "production_change",
]
REPORT_FIELDS = [
    "target_date", "generated_at", "rows_processed", "eligible_fixtures", "api_calls_made", "cache_hits",
    "lineup_rows_written", "full_lineup_rows", "no_lineup_rows", "api_errors", "key_status",
    "api_status_counts", "auto_apply", "production_change",
]


def s(x) -> str:
    return "" if x is None else str(x).strip()


def n(x, default=0.0) -> float:
    try:
        t = s(x)
        return float(t) if t and t.lower() != "nan" else default
    except ValueError:
        return default


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day: str, name: str) -> Path:
    return P / "today" / day / name


def norm_name(x: str) -> str:
    x = s(x).lower()
    x = re.sub(r"\([^)]*\)", " ", x)
    x = re.sub(r"\s+", " ", x)
    x = re.sub(r"[^a-z0-9áéíóúüñçãõàèìòùâêîôû \-']", "", x)
    return x.strip()


def fixture_rows(day: str) -> list[dict[str, str]]:
    for name in ["matches_vsigma_scored_v3.csv", "vsigma_daily_execution_board.csv", "matches_league_filtered.csv"]:
        rows = read(d(day, name))
        if rows:
            return rows
    return []


def current_existing(day: str) -> list[dict[str, str]]:
    rows = []
    for path in [d(day, "vsigma_official_lineup_sources.csv"), P / "governance" / "vsigma_official_lineup_sources.csv", RAW / "official_lineup_sources.csv"]:
        rows.extend(read(path))
    return rows


def existing_cache(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    out: dict[tuple[str, str], dict[str, str]] = {}
    for r in rows:
        fid = s(r.get("fixture_id"))
        side = s(r.get("team_side")).lower()
        count = int(n(r.get("players_count"), 0))
        if fid and side in {"home", "away"} and count >= 8:
            out[(fid, side)] = r
    return out


def key_config() -> tuple[str, str]:
    api_sports = (
        os.environ.get("APISPORTS_KEY")
        or os.environ.get("API_SPORTS_KEY")
        or os.environ.get("API_FOOTBALL_KEY")
        or os.environ.get("APIFOOTBALL_KEY")
        or os.environ.get("API_FOOTBALL_API_KEY")
        or ""
    )
    rapid = os.environ.get("RAPIDAPI_KEY") or os.environ.get("X_RAPIDAPI_KEY") or ""
    if api_sports:
        return "API_SPORTS", api_sports
    if rapid:
        return "RAPIDAPI", rapid
    return "NO_API_KEY", ""


def fetch_lineups(fixture_id: str, provider: str, key: str) -> tuple[str, list[dict]]:
    if provider == "NO_API_KEY" or not key:
        return "NO_API_KEY", []
    try:
        if provider == "API_SPORTS":
            url = "https://v3.football.api-sports.io/fixtures/lineups?" + urllib.parse.urlencode({"fixture": fixture_id})
            headers = {"x-apisports-key": key, "User-Agent": "vSIGMA official-lineup-importer"}
        else:
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups?" + urllib.parse.urlencode({"fixture": fixture_id})
            headers = {
                "x-rapidapi-key": key,
                "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
                "User-Agent": "vSIGMA official-lineup-importer",
            }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            payload = json.loads(r.read().decode("utf-8", "replace"))
        errors = payload.get("errors")
        if errors:
            return "API_ERROR", []
        response = payload.get("response") or []
        if not response:
            return "NO_LINEUPS_RETURNED", []
        return "OK", response
    except Exception:
        return "FETCH_FAILED", []


def eligible(row: dict[str, str], now_ts: float, window_minutes: float) -> bool:
    fid = s(row.get("fixture_id"))
    if not fid:
        return False
    status = s(row.get("fixture_status_short") or row.get("status")).upper()
    if status and status not in {"NS", "TBD", "PST", "POSTP", "CANC", "CANCELLED"}:
        return True
    ts = n(row.get("fixture_timestamp"), 0)
    if ts > 0:
        minutes = (ts - now_ts) / 60.0
        return minutes <= window_minutes
    minutes_to = n(row.get("lineup_minutes_to_kickoff"), 99999)
    return minutes_to <= window_minutes


def player_names_from_api(team_payload: dict) -> list[str]:
    out = []
    for item in team_payload.get("startXI") or []:
        player = item.get("player") or {}
        name = norm_name(player.get("name"))
        if name and name not in out:
            out.append(name)
    return out[:11]


def team_side_for_payload(payload: dict, fixture: dict[str, str]) -> str:
    team = payload.get("team") or {}
    team_id = s(team.get("id"))
    team_name = norm_name(team.get("name"))
    home_id = s(fixture.get("home_team_id"))
    away_id = s(fixture.get("away_team_id"))
    if team_id and home_id and team_id == home_id:
        return "home"
    if team_id and away_id and team_id == away_id:
        return "away"
    if team_name and team_name == norm_name(fixture.get("home_team")):
        return "home"
    if team_name and team_name == norm_name(fixture.get("away_team")):
        return "away"
    return ""


def rows_from_payload(day: str, generated: str, fixture: dict[str, str], status: str, payloads: list[dict]) -> list[dict[str, str]]:
    rows = []
    for payload in payloads:
        side = team_side_for_payload(payload, fixture)
        players = player_names_from_api(payload)
        if side not in {"home", "away"} or not players:
            continue
        coach = payload.get("coach") or {}
        rows.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": s(fixture.get("fixture_id")),
            "league": s(fixture.get("league")),
            "country": s(fixture.get("country")),
            "home_team": s(fixture.get("home_team")),
            "away_team": s(fixture.get("away_team")),
            "team_side": side,
            "source_name": "api_football_official_lineups",
            "official_xi": ";".join(players),
            "players_count": str(len(players)),
            "formation": s(payload.get("formation")),
            "coach_name": s(coach.get("name")),
            "api_status": status,
            "source_guard": "official_api_snapshot",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return rows


def merge_rows(existing: list[dict[str, str]], new_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[tuple[str, str], dict[str, str]] = {}
    for r in existing + new_rows:
        fid = s(r.get("fixture_id"))
        side = s(r.get("team_side")).lower()
        if fid and side in {"home", "away"}:
            current = merged.get((fid, side))
            if current is None or int(n(r.get("players_count"), 0)) >= int(n(current.get("players_count"), 0)):
                merged[(fid, side)] = r
    return list(merged.values())


def md(day: str, rows: list[dict[str, str]], report: list[dict[str, str]]) -> str:
    lines = [f"# vSIGMA Official Lineup Snapshot Import - {day}", "", "## Summary"]
    if report:
        r = report[0]
        lines += [
            f"- rows_processed: {r['rows_processed']}",
            f"- eligible_fixtures: {r['eligible_fixtures']}",
            f"- api_calls_made: {r['api_calls_made']}",
            f"- cache_hits: {r['cache_hits']}",
            f"- lineup_rows_written: {r['lineup_rows_written']}",
            f"- full_lineup_rows: {r['full_lineup_rows']}",
            f"- no_lineup_rows: {r['no_lineup_rows']}",
            f"- api_errors: {r['api_errors']}",
            f"- key_status: {r['key_status']}",
            f"- api_status_counts: {r['api_status_counts']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Imported Official Rows"]
    if not rows:
        lines.append("- none. Official lineups not available or no eligible fixtures.")
    for row in rows[:80]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | side={row['team_side']} | players={row['players_count']} "
            f"| formation={row['formation']} | status={row['api_status']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Official lineup importer only reads API/player snapshots; it never fabricates players.",
        "- Output feeds the probable XI accuracy ledger only.",
        "- No stake or model-weight change is applied here.",
        "- API failures degrade to report status and do not fail the daily chain.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    now_ts = datetime.now(timezone.utc).timestamp()
    window_minutes = n(os.environ.get("VSIGMA_OFFICIAL_LINEUP_FETCH_WINDOW_MINUTES"), 180)
    max_calls = int(n(os.environ.get("VSIGMA_MAX_OFFICIAL_LINEUP_API_CALLS"), 20))
    fixtures = fixture_rows(day)
    provider, key = key_config()
    existing = current_existing(day)
    cache = existing_cache(existing)
    new_rows: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    eligible_count = 0
    calls = 0
    cache_hits = 0
    api_errors = 0

    for fixture in fixtures:
        fid = s(fixture.get("fixture_id"))
        if not eligible(fixture, now_ts, window_minutes):
            continue
        eligible_count += 1
        if (fid, "home") in cache and (fid, "away") in cache:
            cache_hits += 1
            continue
        if calls >= max_calls:
            status_counts["CALL_LIMIT_REACHED"] += 1
            break
        status, payloads = fetch_lineups(fid, provider, key)
        calls += 1 if provider != "NO_API_KEY" else 0
        status_counts[status] += 1
        if status not in {"OK", "NO_LINEUPS_RETURNED", "NO_API_KEY"}:
            api_errors += 1
        if status == "OK":
            new_rows.extend(rows_from_payload(day, generated, fixture, status, payloads))

    merged = merge_rows(existing, new_rows)
    today = P / "today" / day
    report = [{
        "target_date": day,
        "generated_at": generated,
        "rows_processed": str(len(fixtures)),
        "eligible_fixtures": str(eligible_count),
        "api_calls_made": str(calls),
        "cache_hits": str(cache_hits),
        "lineup_rows_written": str(len(merged)),
        "full_lineup_rows": str(sum(1 for r in merged if int(n(r.get("players_count"), 0)) >= 11)),
        "no_lineup_rows": str(max(0, eligible_count * 2 - len(merged))),
        "api_errors": str(api_errors),
        "key_status": provider,
        "api_status_counts": "; ".join(f"{k}={v}" for k, v in status_counts.items()) if status_counts else "none",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    for base in [today, P / "governance"]:
        write(base / "vsigma_official_lineup_sources.csv", merged, OUT_FIELDS)
        write(base / "official_lineup_sources.csv", merged, OUT_FIELDS)
        write(base / "vsigma_official_lineup_snapshot_report.csv", report, REPORT_FIELDS)
        (base / "vsigma_official_lineup_snapshot_report.md").write_text(md(day, merged, report), encoding="utf-8")

    print("=== VSIGMA OFFICIAL LINEUP SNAPSHOT IMPORT ===")
    print(f"rows_processed={len(fixtures)}")
    print(f"eligible_fixtures={eligible_count}")
    print(f"api_calls_made={calls}")
    print(f"lineup_rows_written={len(merged)}")
    print(f"key_status={provider}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
