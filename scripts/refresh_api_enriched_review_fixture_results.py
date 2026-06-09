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
FINISHED_STATUSES = {"FT", "AET", "PEN"}
DIRECT_BASE = "https://v3.football.api-sports.io"
RAPID_BASE = "https://api-football-v1.p.rapidapi.com/v3"
MAX_RETRIES = 3
SLEEP_BETWEEN_CALLS = 0.25

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league", "country",
    "fixture_date_utc", "provider", "refresh_status", "refresh_note", "fixture_status_short",
    "fixture_status_long", "fixture_status_elapsed", "goals_home", "goals_away",
    "score_fulltime_home", "score_fulltime_away", "score_halftime_home", "score_halftime_away",
    "score_extratime_home", "score_extratime_away", "score_penalty_home", "score_penalty_away",
    "result_ready_for_ledger", "api_calls_planned", "api_calls_executed", "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "api_calls_planned", "api_calls_executed",
    "finished_rows", "pending_rows", "refresh_status_counts", "provider_counts",
    "next_action", "auto_apply", "production_change",
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


def load_api_review_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_enriched_review_board.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_enriched_review_board.csv")
    return rows


def load_guard(processed: Path, day: str) -> dict[str, str]:
    rows = read_rows(processed / "today" / day / "vsigma_api_subscription_guard.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_subscription_guard.csv")
    return rows[0] if rows else {}


def api_allowed(processed: Path, day: str) -> tuple[bool, str]:
    guard = load_guard(processed, day)
    if not guard:
        return True, "NO_SUBSCRIPTION_GUARD_FOUND_ALLOWING_LOW_VOLUME_REFRESH"
    allowed = up(guard.get("api_calls_allowed")) == "YES"
    reason = norm(guard.get("guard_reason")) or norm(guard.get("executor_mode")) or "subscription guard present"
    return allowed, reason


def api_credentials() -> tuple[str, str, dict[str, str]]:
    direct_key = os.getenv("API_FOOTBALL_KEY") or os.getenv("APISPORTS_KEY") or os.getenv("API_SPORTS_KEY") or os.getenv("API_FOOTBALL_API_KEY") or os.getenv("APIFOOTBALL_KEY")
    if direct_key:
        return "API-SPORTS_DIRECT", f"{DIRECT_BASE}/fixtures", {"x-apisports-key": direct_key}
    rapid_key = os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY")
    if rapid_key:
        return "RAPIDAPI", f"{RAPID_BASE}/fixtures", {
            "x-rapidapi-key": rapid_key,
            "x-rapidapi-host": os.getenv("API_FOOTBALL_HOST", "api-football-v1.p.rapidapi.com"),
        }
    return "NO_PROVIDER", "", {}


def request_fixture(fixture_id: str, provider: str, url: str, headers: dict[str, str]) -> dict:
    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, params={"id": fixture_id}, timeout=30)
            if response.status_code == 429:
                last_error = "429 Too Many Requests"
                time.sleep(min(2 ** attempt, 8))
                continue
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict) and payload.get("errors"):
                raise RuntimeError(f"{provider} API errors: {payload.get('errors')}")
            items = payload.get("response", []) if isinstance(payload, dict) else []
            if not items:
                return {"refresh_status": "NO_API_FIXTURE_RESPONSE", "refresh_note": "empty response"}
            item = items[0]
            item["refresh_status"] = "OK"
            item["refresh_note"] = "fixture fetched"
            return item
        except Exception as exc:
            last_error = str(exc)
            if attempt < MAX_RETRIES:
                time.sleep(min(2 ** attempt, 8))
    return {"refresh_status": "API_ERROR", "refresh_note": last_error}


def normalize_fixture(item: dict, source_row: dict[str, str], provider: str, day: str, generated: str, calls_planned: int, calls_executed: int) -> dict[str, object]:
    fixture = item.get("fixture", {}) if isinstance(item.get("fixture"), dict) else {}
    teams = item.get("teams", {}) if isinstance(item.get("teams"), dict) else {}
    league = item.get("league", {}) if isinstance(item.get("league"), dict) else {}
    goals = item.get("goals", {}) if isinstance(item.get("goals"), dict) else {}
    score = item.get("score", {}) if isinstance(item.get("score"), dict) else {}
    status = fixture.get("status", {}) if isinstance(fixture.get("status"), dict) else {}
    fulltime = score.get("fulltime", {}) if isinstance(score.get("fulltime"), dict) else {}
    halftime = score.get("halftime", {}) if isinstance(score.get("halftime"), dict) else {}
    extratime = score.get("extratime", {}) if isinstance(score.get("extratime"), dict) else {}
    penalty = score.get("penalty", {}) if isinstance(score.get("penalty"), dict) else {}

    fixture_id = norm(fixture.get("id")) or norm(source_row.get("fixture_id"))
    home_team = norm((teams.get("home") or {}).get("name")) if isinstance(teams.get("home"), dict) else ""
    away_team = norm((teams.get("away") or {}).get("name")) if isinstance(teams.get("away"), dict) else ""
    league_name = norm(league.get("name"))
    country = norm(league.get("country"))
    short = norm(status.get("short"))
    finished = short.upper() in FINISHED_STATUSES

    return {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": fixture_id,
        "home_team": home_team or norm(source_row.get("home_team")),
        "away_team": away_team or norm(source_row.get("away_team")),
        "league": league_name or norm(source_row.get("league")),
        "country": country or norm(source_row.get("country")),
        "fixture_date_utc": norm(fixture.get("date")) or norm(source_row.get("fixture_date_utc")),
        "provider": provider,
        "refresh_status": norm(item.get("refresh_status")) or "OK",
        "refresh_note": norm(item.get("refresh_note")) or "fixture fetched",
        "fixture_status_short": short,
        "fixture_status_long": norm(status.get("long")),
        "fixture_status_elapsed": norm(status.get("elapsed")),
        "goals_home": norm(goals.get("home")),
        "goals_away": norm(goals.get("away")),
        "score_fulltime_home": norm(fulltime.get("home")),
        "score_fulltime_away": norm(fulltime.get("away")),
        "score_halftime_home": norm(halftime.get("home")),
        "score_halftime_away": norm(halftime.get("away")),
        "score_extratime_home": norm(extratime.get("home")),
        "score_extratime_away": norm(extratime.get("away")),
        "score_penalty_home": norm(penalty.get("home")),
        "score_penalty_away": norm(penalty.get("away")),
        "result_ready_for_ledger": "YES" if finished and goals.get("home") is not None and goals.get("away") is not None else "NO",
        "api_calls_planned": calls_planned,
        "api_calls_executed": calls_executed,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def unavailable_row(source_row: dict[str, str], day: str, generated: str, status: str, note: str, calls_planned: int, calls_executed: int) -> dict[str, object]:
    return {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": norm(source_row.get("fixture_id")),
        "home_team": norm(source_row.get("home_team")),
        "away_team": norm(source_row.get("away_team")),
        "league": norm(source_row.get("league")),
        "country": norm(source_row.get("country")),
        "fixture_date_utc": norm(source_row.get("fixture_date_utc")),
        "provider": "NONE",
        "refresh_status": status,
        "refresh_note": note,
        "fixture_status_short": norm(source_row.get("fixture_status")),
        "fixture_status_long": "",
        "fixture_status_elapsed": "",
        "goals_home": "",
        "goals_away": "",
        "score_fulltime_home": "",
        "score_fulltime_away": "",
        "score_halftime_home": "",
        "score_halftime_away": "",
        "score_extratime_home": "",
        "score_extratime_away": "",
        "score_penalty_home": "",
        "score_penalty_away": "",
        "result_ready_for_ledger": "NO",
        "api_calls_planned": calls_planned,
        "api_calls_executed": calls_executed,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, processed: Path, limit: int):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source_rows = load_api_review_rows(processed, day)
    seen: set[str] = set()
    unique_rows = []
    for row in source_rows:
        fixture_id = norm(row.get("fixture_id"))
        if not fixture_id or fixture_id in seen:
            continue
        seen.add(fixture_id)
        unique_rows.append(row)
    if limit > 0:
        unique_rows = unique_rows[:limit]

    allowed, guard_reason = api_allowed(processed, day)
    provider, url, headers = api_credentials()
    calls_planned = len(unique_rows) if allowed and provider != "NO_PROVIDER" else 0
    calls_executed = 0
    out = []

    if not unique_rows:
        summary = make_summary(day, generated, out, 0, 0)
        return out, summary, markdown(day, out, summary[0])

    if not allowed:
        for row in unique_rows:
            out.append(unavailable_row(row, day, generated, "BLOCKED_BY_SUBSCRIPTION_GUARD", guard_reason, 0, 0))
        summary = make_summary(day, generated, out, 0, 0)
        return out, summary, markdown(day, out, summary[0])

    if provider == "NO_PROVIDER":
        for row in unique_rows:
            out.append(unavailable_row(row, day, generated, "NO_API_KEY", "No API-Football credential found in environment", 0, 0))
        summary = make_summary(day, generated, out, 0, 0)
        return out, summary, markdown(day, out, summary[0])

    for row in unique_rows:
        fixture_id = norm(row.get("fixture_id"))
        calls_executed += 1
        item = request_fixture(fixture_id, provider, url, headers)
        out.append(normalize_fixture(item, row, provider, day, generated, calls_planned, calls_executed))
        time.sleep(SLEEP_BETWEEN_CALLS)

    summary = make_summary(day, generated, out, calls_planned, calls_executed)
    return out, summary, markdown(day, out, summary[0])


def make_summary(day: str, generated: str, rows: list[dict[str, object]], calls_planned: int, calls_executed: int) -> list[dict[str, object]]:
    finished = [row for row in rows if row.get("result_ready_for_ledger") == "YES"]
    pending = [row for row in rows if row.get("result_ready_for_ledger") != "YES"]
    return [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(rows),
        "api_calls_planned": calls_planned,
        "api_calls_executed": calls_executed,
        "finished_rows": len(finished),
        "pending_rows": len(pending),
        "refresh_status_counts": counts(rows, "refresh_status"),
        "provider_counts": counts(rows, "provider"),
        "next_action": "Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API-Enriched Fixture Results Refresh - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- api_calls_planned: {summary['api_calls_planned']}",
        f"- api_calls_executed: {summary['api_calls_executed']}",
        f"- finished_rows: {summary['finished_rows']}",
        f"- pending_rows: {summary['pending_rows']}",
        f"- refresh_status_counts: {summary['refresh_status_counts']}",
        f"- provider_counts: {summary['provider_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Result Rows",
    ]
    if not rows:
        lines.append("- none. No API-enriched review board rows available.")
    for row in rows[:120]:
        score = f"{row.get('goals_home', '')}-{row.get('goals_away', '')}" if row.get("result_ready_for_ledger") == "YES" else "pending"
        lines.append(
            f"- {row.get('home_team')} vs {row.get('away_team')} | status={row.get('fixture_status_short') or row.get('refresh_status')} | score={score} | ready={row.get('result_ready_for_ledger')} | provider={row.get('provider')} | note={row.get('refresh_note')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This refresh only stores fixture results for calibration.",
        "- It does not create picks, stake, canonical board permission, or whitelist permission.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
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
    section = "## API-Enriched Fixture Results Refresh"
    lines = [
        section,
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- api_calls_planned: {summary.get('api_calls_planned', 'UNKNOWN')}",
        f"- api_calls_executed: {summary.get('api_calls_executed', 'UNKNOWN')}",
        f"- finished_rows: {summary.get('finished_rows', 'UNKNOWN')}",
        f"- pending_rows: {summary.get('pending_rows', 'UNKNOWN')}",
        f"- refresh_status_counts: {summary.get('refresh_status_counts', 'UNKNOWN')}",
        f"- provider_counts: {summary.get('provider_counts', 'UNKNOWN')}",
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
        write_csv(base / "vsigma_api_enriched_fixture_results_refresh.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_enriched_fixture_results_refresh_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_enriched_fixture_results_refresh.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API-ENRICHED FIXTURE RESULTS REFRESH ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"api_calls_planned={summary[0]['api_calls_planned']}")
    print(f"api_calls_executed={summary[0]['api_calls_executed']}")
    print(f"finished_rows={summary[0]['finished_rows']}")
    print(f"pending_rows={summary[0]['pending_rows']}")
    print(f"refresh_status_counts={summary[0]['refresh_status_counts']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir, args.limit)


if __name__ == "__main__":
    main()
