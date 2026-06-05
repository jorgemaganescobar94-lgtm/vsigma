from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date","generated_at","ledger_key","fixture_id","home_team","away_team",
    "league","country","decision_bucket","pick_outcome","quality_class","market_family",
    "goal_event_rows","home_goals","away_goals","total_goals","first_goal_minute",
    "first_goal_team","first_half_goals","second_half_goals","late_goals_75_plus",
    "early_goal_15_flag","early_goal_30_flag","nil_nil_ht_flag",
    "goal_timing_data_status","goal_timing_profile","goal_timing_learning_label",
    "timing_evidence_level","manual_review_required","recommended_action","timing_note",
    "source_guard","auto_apply","production_change",
]

EVENT_FILES = [
    "vsigma_goal_events.csv",
    "vsigma_fixture_events.csv",
    "fixture_events.csv",
    "events.csv",
    "vsigma_post_match_events.csv",
    "matches.csv",
    "vsigma_post_match_stat_actuals.csv",
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

def existing_paths(processed: Path, day: str, names: list[str]) -> list[Path]:
    paths: list[Path] = []
    for name in names:
        for path in [processed / "today" / day / name, processed / "governance" / name]:
            if path.exists():
                paths.append(path)
    return paths

def first_existing(processed: Path, day: str, names: list[str]) -> Path | None:
    paths = existing_paths(processed, day, names)
    return paths[0] if paths else None

def load_rows(processed: Path, day: str, names: list[str]) -> list[dict[str, str]]:
    path = first_existing(processed, day, names)
    return read_csv(path) if path else []

def by_key(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        key = norm(row.get(field))
        if key:
            out[key] = row
    return out

def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")

def as_int(value: object) -> int | None:
    text = norm(value)
    if not text or text.lower() == "nan":
        return None
    match = re.search(r"-?\d+", text)
    if not match:
        return None
    try:
        return int(match.group(0))
    except ValueError:
        return None

def is_diagnostic(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in ["fixture_id", "home_team", "away_team", "decision_bucket", "ledger_status", "quality_class"]
    )
    return "DIAGNOSTIC" in text or "NO_PROMOTED_RAW_CANDIDATES" in text

def merge_inputs(processed: Path, day: str) -> list[dict[str, str]]:
    ledger = load_rows(processed, day, ["vsigma_official_pick_ledger.csv", "vsigma_official_pick_ledger_daily.csv"])
    quality_by_key = by_key(
        load_rows(processed, day, ["vsigma_pick_quality_classification.csv", "vsigma_pick_quality_classification_daily.csv"]),
        "ledger_key",
    )
    translation_by_key = by_key(
        load_rows(processed, day, ["vsigma_market_translation_audit.csv", "vsigma_market_translation_audit_daily.csv"]),
        "ledger_key",
    )

    if not ledger:
        ledger = [{
            "target_date": day,
            "ledger_key": f"{day}|DIAGNOSTIC_NO_OFFICIAL_LEDGER",
            "fixture_id": "DIAGNOSTIC_NO_OFFICIAL_LEDGER",
            "home_team": "NO_OFFICIAL_LEDGER",
            "away_team": "NO_OFFICIAL_LEDGER",
            "league": "DIAGNOSTIC_NO_COMPETITION",
            "country": "DIAGNOSTIC",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "final_decision": "NO_BET",
        }]

    merged: list[dict[str, str]] = []
    for base in ledger:
        key = norm(base.get("ledger_key"))
        row = dict(base)
        for source in [quality_by_key.get(key, {}), translation_by_key.get(key, {})]:
            for field, value in source.items():
                if field in {"target_date", "generated_at"}:
                    continue
                if norm(value):
                    row[field] = value
        merged.append(row)
    return merged

def looks_like_goal(row: dict[str, str]) -> bool:
    text = " ".join(up(v) for v in row.values())
    if "GOAL" in text or "PENALTY SCORED" in text or "OWN GOAL" in text:
        if "DISALLOWED" not in text and "VAR CANCELLED" not in text:
            return True
    return any("GOAL" in up(k) and "MIN" in up(k) for k in row.keys())

def row_minute(row: dict[str, str]) -> int | None:
    for key in ["elapsed", "minute", "event_minute", "time_elapsed", "goal_minute", "first_goal_minute", "min"]:
        val = as_int(row.get(key))
        if val is not None:
            return val
    for value in row.values():
        text = norm(value)
        match = re.search(r"\b(\d{1,3})(?:\+(\d{1,2}))?\b", text)
        if match and any(token in up(value) for token in ["'", "MIN", "GOAL"]):
            base = int(match.group(1))
            added = int(match.group(2) or 0)
            return base + added
    return None

def row_team_side(row: dict[str, str], home: str, away: str) -> str:
    text = " ".join(up(v) for v in row.values())
    home_u = up(home)
    away_u = up(away)
    if home_u and home_u in text:
        return "HOME"
    if away_u and away_u in text:
        return "AWAY"
    for key in ["team_side", "side", "is_home", "team"]:
        val = up(row.get(key))
        if val in {"HOME", "LOCAL", "TRUE", "1"}:
            return "HOME"
        if val in {"AWAY", "VISITOR", "VISITANTE", "FALSE", "0"}:
            return "AWAY"
    return "UNKNOWN"

def load_goal_events(processed: Path, day: str) -> dict[str, list[dict[str, str]]]:
    events_by_fixture: dict[str, list[dict[str, str]]] = {}
    for path in existing_paths(processed, day, EVENT_FILES):
        for row in read_csv(path):
            fid = norm(row.get("fixture_id")).replace(".0", "")
            if not fid:
                continue
            has_goal_minute_field = any("GOAL" in up(k) and "MIN" in up(k) for k in row.keys())
            if path.name in {"matches.csv", "vsigma_post_match_stat_actuals.csv"} and not has_goal_minute_field:
                continue
            if looks_like_goal(row) or has_goal_minute_field:
                events_by_fixture.setdefault(fid, []).append(row)
    return events_by_fixture

def load_actuals(processed: Path, day: str) -> dict[str, dict[str, str]]:
    rows = load_rows(processed, day, ["vsigma_post_match_stat_actuals.csv", "matches.csv"])
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = norm(row.get("fixture_id")).replace(".0", "")
        if fid:
            out[fid] = row
    return out

def goal_summary(row: dict[str, str], events: list[dict[str, str]], actual: dict[str, str]) -> dict[str, object]:
    home = norm(row.get("home_team"))
    away = norm(row.get("away_team"))

    minutes: list[tuple[int, str]] = []
    for event in events:
        minute = row_minute(event)
        if minute is not None:
            minutes.append((minute, row_team_side(event, home, away)))

    minutes.sort(key=lambda item: item[0])

    home_goals = as_int(actual.get("actual_home_goals")) or as_int(actual.get("home_goals")) or as_int(row.get("actual_home_goals"))
    away_goals = as_int(actual.get("actual_away_goals")) or as_int(actual.get("away_goals")) or as_int(row.get("actual_away_goals"))
    total_goals = as_int(actual.get("actual_total_goals")) or as_int(actual.get("total_goals")) or as_int(row.get("actual_total_goals"))

    if total_goals is None and home_goals is not None and away_goals is not None:
        total_goals = home_goals + away_goals

    first_goal_minute = minutes[0][0] if minutes else None
    first_goal_team = minutes[0][1] if minutes else "UNKNOWN"
    first_half_goals = sum(1 for minute, _side in minutes if minute <= 45)
    second_half_goals = sum(1 for minute, _side in minutes if minute > 45)
    late_goals = sum(1 for minute, _side in minutes if minute >= 75)

    if not minutes and total_goals == 0:
        data_status = "HAS_ZERO_GOAL_RESULT_NO_TIMING_EVENTS"
    elif minutes:
        data_status = "HAS_GOAL_TIMING_EVENTS"
    else:
        data_status = "NO_GOAL_TIMING_DATA"

    return {
        "goal_event_rows": len(events),
        "home_goals": "" if home_goals is None else home_goals,
        "away_goals": "" if away_goals is None else away_goals,
        "total_goals": "" if total_goals is None else total_goals,
        "first_goal_minute": "" if first_goal_minute is None else first_goal_minute,
        "first_goal_team": first_goal_team,
        "first_half_goals": first_half_goals,
        "second_half_goals": second_half_goals,
        "late_goals_75_plus": late_goals,
        "early_goal_15_flag": "YES" if first_goal_minute is not None and first_goal_minute <= 15 else "NO",
        "early_goal_30_flag": "YES" if first_goal_minute is not None and first_goal_minute <= 30 else "NO",
        "nil_nil_ht_flag": "YES" if total_goals == 0 or (minutes and first_half_goals == 0) else ("UNKNOWN" if not minutes and total_goals is None else "NO"),
        "goal_timing_data_status": data_status,
    }

def classify_timing(row: dict[str, str], summary: dict[str, object]) -> tuple[str, str, str, str, str, str]:
    if is_diagnostic(row):
        return (
            "DIAGNOSTIC_NO_GOAL_TIMING_LEARNING",
            "DIAGNOSTIC_NOT_REAL_FIXTURE",
            "NONE",
            "NO",
            "NO_MODEL_CHANGE",
            "Diagnostic row; no fixture-level goal timing can be evaluated.",
        )

    status = str(summary.get("goal_timing_data_status", ""))
    outcome = up(row.get("pick_outcome"))
    market_family = up(row.get("market_family"))
    decision_bucket = up(row.get("decision_bucket"))
    early15 = summary.get("early_goal_15_flag") == "YES"
    early30 = summary.get("early_goal_30_flag") == "YES"
    nilnilht = summary.get("nil_nil_ht_flag") == "YES"
    late_goals = int(summary.get("late_goals_75_plus") or 0)

    if status == "NO_GOAL_TIMING_DATA":
        return (
            "GOAL_TIMING_DATA_MISSING",
            "NO_TIMING_SIGNAL",
            "LOW",
            "NO",
            "COLLECT_GOAL_EVENT_DATA",
            "No usable goal timing events or zero-goal result found.",
        )

    if status == "HAS_ZERO_GOAL_RESULT_NO_TIMING_EVENTS":
        if decision_bucket == "NO_BET":
            return (
                "ZERO_GOAL_NO_BET_REVIEW",
                "NO_BET_TOO_CONSERVATIVE_TIMING_CANDIDATE",
                "MEDIUM",
                "YES",
                "REVIEW_IF_SAFE_UNDER_OR_NO_BET_WAS_CORRECT",
                "0-0 final without goal events; review if No Bet missed safe under/low-event market.",
            )
        return (
            "ZERO_GOAL_MATCH_REVIEW",
            "LOW_EVENT_TIMING_PROFILE",
            "MEDIUM",
            "YES",
            "REVIEW_LOW_EVENT_MARKET_TRANSLATION",
            "0-0 final; review low-event thesis and market translation.",
        )

    if early15:
        if market_family == "TOTAL_GOALS":
            return (
                "EARLY_GOAL_TOTALS_REVIEW",
                "EARLY_GOAL_CHANGED_TOTALS_STATE",
                "HIGH",
                "YES",
                "REVIEW_TOTALS_SURVIVAL_AFTER_EARLY_GOAL",
                "First goal at or before 15'; review whether total-goals market survived early state change.",
            )
        return (
            "EARLY_GOAL_STATE_SHOCK_REVIEW",
            "EARLY_GOAL_CHANGED_MATCH_STATE",
            "HIGH",
            "YES",
            "REVIEW_EARLY_GOAL_STATE_SURVIVAL",
            "Early goal likely changed state; review whether pick/no-bet accounted for it.",
        )

    if early30:
        return (
            "FIRST_GOAL_16_30_REVIEW",
            "MODERATE_EARLY_GOAL_PROFILE",
            "MEDIUM",
            "YES" if outcome in {"RED", "NO_PICK"} else "NO",
            "REVIEW_IF_TIMING_AFFECTED_MARKET",
            "First goal before 30'; timing may have affected market survival.",
        )

    if nilnilht:
        return (
            "NIL_NIL_HT_REVIEW",
            "SLOW_START_LOW_EVENT_PROFILE",
            "MEDIUM",
            "YES",
            "REVIEW_PREMATCH_VS_LIVE_ENTRY_TIMING",
            "0-0 at halftime profile; review whether live entry was superior to prematch.",
        )

    if late_goals > 0:
        return (
            "LATE_GOAL_REVIEW",
            "LATE_GOAL_VARIANCE_OR_RESOLUTION_PROFILE",
            "MEDIUM",
            "YES",
            "REVIEW_LATE_GOAL_EFFECT_ON_PICK_QUALITY",
            "Late goal(s) after 75'; review whether result was robust or rescue/variance.",
        )

    return (
        "STANDARD_GOAL_TIMING_REVIEW",
        "STANDARD_TIMING_PROFILE",
        "LOW",
        "NO",
        "KEEP_COLLECTING_SAMPLE",
        "Goal timing available but no strong timing shock was detected.",
    )

def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    base_rows = merge_inputs(processed, day)
    events_by_fixture = load_goal_events(processed, day)
    actuals_by_fixture = load_actuals(processed, day)

    out: list[dict[str, object]] = []
    for row in base_rows:
        fid = fixture_id(row)
        events = events_by_fixture.get(fid, [])
        actual = actuals_by_fixture.get(fid, {})
        summary = goal_summary(row, events, actual)
        timing_profile, learning_label, evidence, manual, action, note = classify_timing(row, summary)

        out.append({
            "target_date": day,
            "generated_at": generated,
            "ledger_key": norm(row.get("ledger_key")),
            "fixture_id": fid,
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "decision_bucket": norm(row.get("decision_bucket")),
            "pick_outcome": norm(row.get("pick_outcome"), "NO_PICK"),
            "quality_class": norm(row.get("quality_class")),
            "market_family": norm(row.get("market_family"), "UNKNOWN_FAMILY"),
            **summary,
            "goal_timing_profile": timing_profile,
            "goal_timing_learning_label": learning_label,
            "timing_evidence_level": evidence,
            "manual_review_required": manual,
            "recommended_action": action,
            "timing_note": note,
            "source_guard": "GOAL_TIMING_LEARNING_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_goal_timing_learning_daily.csv", rows, FIELDS)
        (base / "vsigma_goal_timing_learning.md").write_text(markdown(day, rows), encoding="utf-8")

    hist = processed / "governance" / "vsigma_goal_timing_learning.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)

def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Goal Timing Learning - {day}",
        "",
        "## Summary",
        f"- goal_timing_rows: {len(rows)}",
        f"- goal_timing_data_status_counts: {fmt_counts(rows, 'goal_timing_data_status')}",
        f"- goal_timing_profile_counts: {fmt_counts(rows, 'goal_timing_profile')}",
        f"- goal_timing_learning_label_counts: {fmt_counts(rows, 'goal_timing_learning_label')}",
        f"- timing_evidence_level_counts: {fmt_counts(rows, 'timing_evidence_level')}",
        f"- manual_review_required_counts: {fmt_counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Goal Timing Rows",
    ]

    for row in rows[:120]:
        lines.append(
            "- "
            f"{row.get('goal_timing_profile', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"first_goal={row.get('first_goal_minute', '') or 'NA'} team={row.get('first_goal_team', '')} | "
            f"0-0HT={row.get('nil_nil_ht_flag', '')} early15={row.get('early_goal_15_flag', '')} late75={row.get('late_goals_75_plus', '')} | "
            f"outcome={row.get('pick_outcome', '')} | label={row.get('goal_timing_learning_label', '')} | "
            f"manual={row.get('manual_review_required', '')} | action={row.get('recommended_action', '')}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This goal timing report is advisory only and never changes picks, stake, live gates, or weights.",
        "- Missing event data is not treated as a model failure by itself.",
        "- Early/late goal labels require causal review before any lesson is accepted.",
        "- No automatic entry timing, live, source registry, or production changes are created here.",
    ]
    return "\n".join(lines) + "\n"

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA GOAL TIMING LEARNING ===")
    print(f"goal_timing_rows={len(rows)}")
    print(f"goal_timing_data_status_counts={fmt_counts(rows, 'goal_timing_data_status')}")
    print(f"goal_timing_profile_counts={fmt_counts(rows, 'goal_timing_profile')}")
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
