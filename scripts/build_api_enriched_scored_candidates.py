from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "fixture_id",
    "home_team",
    "away_team",
    "league",
    "country",
    "api_league_id",
    "api_season",
    "fixture_date_utc",
    "fixture_status",
    "venue_name",
    "home_team_id",
    "away_team_id",
    "downstream_use",
    "executor_status",
    "scoring_eligibility_after_execution",
    "fixture_detail_available",
    "predictions_available",
    "odds_available",
    "events_available",
    "statistics_available",
    "lineups_available",
    "prediction_winner_name",
    "prediction_advice",
    "pred_home_total_pct",
    "pred_away_total_pct",
    "pred_home_form_pct",
    "pred_away_form_pct",
    "pred_home_att_pct",
    "pred_away_att_pct",
    "pred_home_def_pct",
    "pred_away_def_pct",
    "match_winner_home_odd",
    "match_winner_draw_odd",
    "match_winner_away_odd",
    "over_1_5_odd",
    "under_1_5_odd",
    "over_2_5_odd",
    "under_2_5_odd",
    "over_3_5_odd",
    "under_3_5_odd",
    "market_signal_summary",
    "scored_candidate_status",
    "normal_gate_requirement",
    "pick_permission",
    "stake_permission",
    "source_guard",
    "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "source_rows_reviewed",
    "candidate_rows_written",
    "scoring_ready_pending_gates_rows",
    "missing_required_rows",
    "coverage_only_rows",
    "diagnostic_only_rows",
    "status_counts",
    "pick_permission_counts",
    "stake_permission_counts",
    "auto_apply",
    "production_change",
]

def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default

def up(value: object) -> str:
    return norm(value).upper()

def read_csv(path: Path) -> list[dict[str, str]]:
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

def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def first_existing(processed: Path, day: str, names: list[str]) -> Path | None:
    for name in names:
        for path in [processed / "today" / day / name, processed / "governance" / name]:
            if path.exists():
                return path
    return None

def load_executor_rows(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, [
        "vsigma_max_coverage_api_enrichment_executor.csv",
    ])
    rows = read_csv(path) if path else []
    if path and path.parent.name == "governance" and rows and "target_date" in rows[0]:
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows

def parse_pct(value: object) -> str:
    text = norm(value)
    if not text:
        return ""
    match = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", "."))
    return match.group(0) if match else ""

def first_response(payload: dict) -> dict:
    response = payload.get("response")
    if isinstance(response, list) and response:
        return response[0] if isinstance(response[0], dict) else {}
    return {}

def response_has_rows(payload: dict) -> bool:
    response = payload.get("response")
    return isinstance(response, list) and len(response) > 0

def fixture_info(payload: dict) -> dict[str, object]:
    item = first_response(payload)
    fixture = item.get("fixture", {}) if isinstance(item, dict) else {}
    league = item.get("league", {}) if isinstance(item, dict) else {}
    teams = item.get("teams", {}) if isinstance(item, dict) else {}
    home = teams.get("home", {}) if isinstance(teams, dict) else {}
    away = teams.get("away", {}) if isinstance(teams, dict) else {}
    venue = fixture.get("venue", {}) if isinstance(fixture, dict) else {}
    status = fixture.get("status", {}) if isinstance(fixture, dict) else {}

    return {
        "api_league_id": league.get("id", ""),
        "api_season": league.get("season", ""),
        "league": league.get("name", ""),
        "country": league.get("country", ""),
        "fixture_date_utc": fixture.get("date", ""),
        "fixture_status": status.get("short", "") or status.get("long", ""),
        "venue_name": venue.get("name", ""),
        "home_team_id": home.get("id", ""),
        "away_team_id": away.get("id", ""),
        "home_team": home.get("name", ""),
        "away_team": away.get("name", ""),
    }

def prediction_info(payload: dict) -> dict[str, object]:
    item = first_response(payload)
    predictions = item.get("predictions", {}) if isinstance(item, dict) else {}
    comparison = item.get("comparison", {}) if isinstance(item, dict) else {}

    def comp(group: str, side: str) -> str:
        obj = comparison.get(group, {}) if isinstance(comparison, dict) else {}
        return parse_pct(obj.get(side, "")) if isinstance(obj, dict) else ""

    winner = predictions.get("winner", {}) if isinstance(predictions, dict) else {}
    if not isinstance(winner, dict):
        winner = {}

    return {
        "prediction_winner_name": winner.get("name", ""),
        "prediction_advice": predictions.get("advice", "") if isinstance(predictions, dict) else "",
        "pred_home_total_pct": comp("total", "home"),
        "pred_away_total_pct": comp("total", "away"),
        "pred_home_form_pct": comp("form", "home"),
        "pred_away_form_pct": comp("form", "away"),
        "pred_home_att_pct": comp("att", "home"),
        "pred_away_att_pct": comp("att", "away"),
        "pred_home_def_pct": comp("def", "home"),
        "pred_away_def_pct": comp("def", "away"),
    }

def odds_info(payload: dict) -> dict[str, object]:
    out: dict[str, object] = {
        "match_winner_home_odd": "",
        "match_winner_draw_odd": "",
        "match_winner_away_odd": "",
        "over_1_5_odd": "",
        "under_1_5_odd": "",
        "over_2_5_odd": "",
        "under_2_5_odd": "",
        "over_3_5_odd": "",
        "under_3_5_odd": "",
    }

    item = first_response(payload)
    bookmakers = item.get("bookmakers", []) if isinstance(item, dict) else []
    if not isinstance(bookmakers, list):
        return out

    for bookmaker in bookmakers:
        bets = bookmaker.get("bets", []) if isinstance(bookmaker, dict) else []
        if not isinstance(bets, list):
            continue

        for bet in bets:
            name = up(bet.get("name"))
            values = bet.get("values", [])
            if not isinstance(values, list):
                continue

            if name == "MATCH WINNER":
                for value in values:
                    side = up(value.get("value"))
                    odd = norm(value.get("odd"))
                    if side == "HOME":
                        out["match_winner_home_odd"] = odd
                    elif side == "DRAW":
                        out["match_winner_draw_odd"] = odd
                    elif side == "AWAY":
                        out["match_winner_away_odd"] = odd

            if "OVER/UNDER" in name or name == "GOALS OVER/UNDER":
                for value in values:
                    label = up(value.get("value"))
                    odd = norm(value.get("odd"))
                    if label == "OVER 1.5":
                        out["over_1_5_odd"] = odd
                    elif label == "UNDER 1.5":
                        out["under_1_5_odd"] = odd
                    elif label == "OVER 2.5":
                        out["over_2_5_odd"] = odd
                    elif label == "UNDER 2.5":
                        out["under_2_5_odd"] = odd
                    elif label == "OVER 3.5":
                        out["over_3_5_odd"] = odd
                    elif label == "UNDER 3.5":
                        out["under_3_5_odd"] = odd

        # v1: first bookmaker with useful lines is enough.
        if any(out.values()):
            break

    return out

def build_signal_summary(row: dict[str, object]) -> str:
    parts: list[str] = []
    if row.get("prediction_winner_name"):
        parts.append(f"prediction_winner={row.get('prediction_winner_name')}")
    if row.get("pred_home_total_pct") or row.get("pred_away_total_pct"):
        parts.append(f"pred_total_home_away={row.get('pred_home_total_pct')}/{row.get('pred_away_total_pct')}")
    if row.get("match_winner_home_odd") or row.get("match_winner_away_odd"):
        parts.append(f"1x2={row.get('match_winner_home_odd')}/{row.get('match_winner_draw_odd')}/{row.get('match_winner_away_odd')}")
    if row.get("over_2_5_odd") or row.get("under_2_5_odd"):
        parts.append(f"ou2.5={row.get('over_2_5_odd')}/{row.get('under_2_5_odd')}")
    return " | ".join(parts)

def classify(row: dict[str, str], fixture_available: bool, predictions_available: bool, odds_available: bool) -> tuple[str, str]:
    downstream = norm(row.get("downstream_use"))
    if downstream == "COVERAGE_GATE_ONLY":
        return "COVERAGE_ONLY_NO_SCORING", "Coverage-only row cannot feed scoring."
    if downstream == "DIAGNOSTIC_ONLY_NO_SCORING":
        return "DIAGNOSTIC_ONLY_NO_SCORING", "Diagnostic-only row cannot feed scoring."
    if downstream != "SCORING_ALLOWED_WITH_NORMAL_GATES":
        return "UNKNOWN_DOWNSTREAM_NO_SCORING", "Unknown downstream permission."

    if fixture_available and (predictions_available or odds_available):
        return "API_ENRICHED_SCORING_READY_PENDING_GATES", "Requires normal scoring/promotion gates; no pick permission."

    return "MISSING_REQUIRED_API_DATA", "Needs fixture_detail plus predictions or odds before scoring."

def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    executor_rows = load_executor_rows(processed, day)

    out: list[dict[str, object]] = []
    for row in executor_rows:
        fixture_id = norm(row.get("fixture_id"))
        base = processed / "today" / day / "api_enrichment" / fixture_id

        fixture_payload = read_json(base / "fixture_detail.json")
        predictions_payload = read_json(base / "predictions.json")
        odds_payload = read_json(base / "odds.json")
        events_payload = read_json(base / "events.json")
        statistics_payload = read_json(base / "statistics.json")
        lineups_payload = read_json(base / "lineups.json")

        fixture_available = response_has_rows(fixture_payload)
        predictions_available = response_has_rows(predictions_payload)
        odds_available = response_has_rows(odds_payload)
        events_available = response_has_rows(events_payload)
        statistics_available = response_has_rows(statistics_payload)
        lineups_available = response_has_rows(lineups_payload)

        fixture = fixture_info(fixture_payload)
        pred = prediction_info(predictions_payload)
        odds = odds_info(odds_payload)

        status, requirement = classify(row, fixture_available, predictions_available, odds_available)

        out_row: dict[str, object] = {
            "target_date": day,
            "generated_at": generated,
            "fixture_id": fixture_id,
            "home_team": fixture.get("home_team") or norm(row.get("home_team")),
            "away_team": fixture.get("away_team") or norm(row.get("away_team")),
            "league": fixture.get("league") or norm(row.get("league")),
            "country": fixture.get("country") or norm(row.get("country")),
            "api_league_id": fixture.get("api_league_id", ""),
            "api_season": fixture.get("api_season", ""),
            "fixture_date_utc": fixture.get("fixture_date_utc", ""),
            "fixture_status": fixture.get("fixture_status", ""),
            "venue_name": fixture.get("venue_name", ""),
            "home_team_id": fixture.get("home_team_id", ""),
            "away_team_id": fixture.get("away_team_id", ""),
            "downstream_use": norm(row.get("downstream_use")),
            "executor_status": norm(row.get("executor_status")),
            "scoring_eligibility_after_execution": norm(row.get("scoring_eligibility_after_execution")),
            "fixture_detail_available": "YES" if fixture_available else "NO",
            "predictions_available": "YES" if predictions_available else "NO",
            "odds_available": "YES" if odds_available else "NO",
            "events_available": "YES" if events_available else "NO",
            "statistics_available": "YES" if statistics_available else "NO",
            "lineups_available": "YES" if lineups_available else "NO",
            **pred,
            **odds,
            "scored_candidate_status": status,
            "normal_gate_requirement": requirement,
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "source_guard": "API_ENRICHED_SCORED_CANDIDATES_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        }
        out_row["market_signal_summary"] = build_signal_summary(out_row)
        out.append(out_row)

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "source_rows_reviewed": len(executor_rows),
        "candidate_rows_written": len(out),
        "scoring_ready_pending_gates_rows": sum(1 for row in out if row["scored_candidate_status"] == "API_ENRICHED_SCORING_READY_PENDING_GATES"),
        "missing_required_rows": sum(1 for row in out if row["scored_candidate_status"] == "MISSING_REQUIRED_API_DATA"),
        "coverage_only_rows": sum(1 for row in out if row["scored_candidate_status"] == "COVERAGE_ONLY_NO_SCORING"),
        "diagnostic_only_rows": sum(1 for row in out if row["scored_candidate_status"] == "DIAGNOSTIC_ONLY_NO_SCORING"),
        "status_counts": counts(out, "scored_candidate_status"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "auto_apply": "NO",
        "production_change": "NO",
    }]

    return out, summary, markdown(day, out, summary[0])

def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API-Enriched Scored Candidates - {day}",
        "",
        "## Summary",
        f"- source_rows_reviewed: {summary['source_rows_reviewed']}",
        f"- candidate_rows_written: {summary['candidate_rows_written']}",
        f"- scoring_ready_pending_gates_rows: {summary['scoring_ready_pending_gates_rows']}",
        f"- missing_required_rows: {summary['missing_required_rows']}",
        f"- coverage_only_rows: {summary['coverage_only_rows']}",
        f"- diagnostic_only_rows: {summary['diagnostic_only_rows']}",
        f"- status_counts: {summary['status_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Candidate Rows",
    ]

    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | status={row['scored_candidate_status']} | "
            f"fixture={row['fixture_detail_available']} pred={row['predictions_available']} odds={row['odds_available']} | "
            f"summary={row['market_signal_summary']} | pick={row['pick_permission']} | stake={row['stake_permission']}"
        )

    lines += [
        "",
        "## Guardrails",
        "- These are scored-candidate inputs only; they do not create picks or stake permission.",
        "- Every row still requires normal scoring, promotion, market translation, and operator gates.",
        "- API enrichment alone is never enough to recommend a market.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]], summary: list[dict[str, object]], md: str) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_enriched_scored_candidates.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_enriched_scored_candidates_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_enriched_scored_candidates.md").write_text(md, encoding="utf-8")

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    write_outputs(processed, day, rows, summary, md)
    s = summary[0]
    print("=== VSIGMA API-ENRICHED SCORED CANDIDATES ===")
    print(f"candidate_rows_written={s['candidate_rows_written']}")
    print(f"scoring_ready_pending_gates_rows={s['scoring_ready_pending_gates_rows']}")
    print(f"pick_permission_counts={s['pick_permission_counts']}")
    print("auto_apply=NO")
    print("production_change=NO")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)

if __name__ == "__main__":
    main()
