from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, time
from pathlib import Path
from zoneinfo import ZoneInfo


def read_csv(path: Path):
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, reader.fieldnames or []


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.exists():
            return p
    return None


def parse_dt(value: str | None, tz: ZoneInfo):
    if not value:
        return None

    value = str(value).strip()
    if not value:
        return None

    # A plain YYYY-MM-DD date is not enough for prelock timing.
    if len(value) == 10 and value.count("-") == 2:
        return None

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)

    return dt.astimezone(tz)


def parse_timestamp(value: str | None, tz: ZoneInfo):
    if not value:
        return None
    try:
        return datetime.fromtimestamp(int(float(str(value))), tz)
    except Exception:
        return None


def useful_prelock_slots(kickoff: datetime, window_minutes: int, tz: ZoneInfo):
    window_start = kickoff - timedelta(minutes=window_minutes)
    slots = []

    # Hourly production schedule: 10:00 through 23:00 Atlantic/Canary.
    for hour in range(10, 24):
        slot = datetime.combine(kickoff.date(), time(hour=hour), tzinfo=tz)
        if window_start <= slot < kickoff:
            slots.append(slot)

    return slots


def fmt_dt(dt: datetime | None) -> str:
    if not dt:
        return ""
    return dt.isoformat(timespec="minutes")


def fmt_slot_list(slots: list[datetime]) -> str:
    return ";".join(s.isoformat(timespec="minutes") for s in slots)


def md_cell(value) -> str:
    return str(value or "").replace("|", "/")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--window-minutes", type=int, default=90)
    args = parser.parse_args()

    root = Path(".")
    target_date = args.date
    tz = ZoneInfo(args.timezone)
    now = datetime.now(tz)

    today_dir = root / "data" / "processed" / "today" / target_date
    today_dir.mkdir(parents=True, exist_ok=True)

    candidate_path = first_existing(
        [
            today_dir / "vsigma_today_competition_top.csv",
            root / "data" / "processed" / "vsigma_today_competition_top.csv",
        ]
    )

    prelock_path = today_dir / "vsigma_today_prelock_competition_top.csv"

    matches_path = first_existing(
        [
            today_dir / "matches.csv",
            root / "data" / "processed" / "matches_league_filtered.csv",
            root / "data" / "raw" / "matches.csv",
        ]
    )

    candidate_rows, _ = read_csv(candidate_path) if candidate_path else ([], [])
    prelock_rows, _ = read_csv(prelock_path)
    match_rows, _ = read_csv(matches_path) if matches_path else ([], [])

    # Keep only current target date when the column exists.
    filtered_candidates = []
    for row in candidate_rows:
        row_date = (row.get("target_date") or row.get("date") or "").strip()
        if row_date and row_date != target_date:
            continue
        filtered_candidates.append(row)

    match_by_id = {str(r.get("fixture_id", "")).strip(): r for r in match_rows}
    prelock_by_id = {str(r.get("fixture_id", "")).strip(): r for r in prelock_rows}

    audit_rows = []

    for c in filtered_candidates:
        fixture_id = str(c.get("fixture_id", "")).strip()
        m = match_by_id.get(fixture_id, {})
        p = prelock_by_id.get(fixture_id, {})

        kickoff = (
            parse_dt(m.get("fixture_datetime_utc"), tz)
            or parse_dt(c.get("fixture_datetime_utc"), tz)
            or parse_timestamp(m.get("fixture_timestamp"), tz)
            or parse_timestamp(c.get("fixture_timestamp"), tz)
        )

        minutes_to_kickoff = ""
        in_window_now = "NO"
        prelock_window_start = ""
        useful_slots = []
        next_useful_slot = ""

        if kickoff:
            minutes = (kickoff - now).total_seconds() / 60
            minutes_to_kickoff = f"{minutes:.2f}"
            in_window_now = "YES" if 0 <= minutes <= args.window_minutes else "NO"
            prelock_window_start = fmt_dt(kickoff - timedelta(minutes=args.window_minutes))
            useful_slots = useful_prelock_slots(kickoff, args.window_minutes, tz)

            future_slots = [s for s in useful_slots if s >= now]
            if future_slots:
                next_useful_slot = fmt_dt(future_slots[0])

        prelock_retained = "YES" if fixture_id in prelock_by_id else "NO"

        if prelock_retained == "YES":
            exclusion_reason = p.get("prelock_decision") or "RETAINED_IN_PRELOCK_OUTPUT"
            next_action = "REVIEW_PRELOCK_DECISION"
        elif not kickoff:
            exclusion_reason = "MISSING_KICKOFF_DATETIME"
            next_action = "FIX_FIXTURE_TIME_FIELDS"
        elif float(minutes_to_kickoff) < 0:
            exclusion_reason = "KICKOFF_ALREADY_PASSED"
            next_action = "WAIT_FOR_POST_RESULTS"
        elif in_window_now == "NO":
            exclusion_reason = "OUTSIDE_90_MIN_PRELOCK_WINDOW"
            next_action = (
                f"WAIT_UNTIL_{next_useful_slot}"
                if next_useful_slot
                else "NO_REMAINING_USEFUL_PRELOCK_SLOT"
            )
        else:
            exclusion_reason = "IN_WINDOW_BUT_NOT_RETAINED"
            next_action = "CHECK_ODDS_LINEUPS_AVAILABILITY_OR_V7_GOVERNANCE"

        audit_rows.append(
            {
                "target_date": target_date,
                "generated_at": now.isoformat(timespec="seconds"),
                "fixture_id": fixture_id,
                "league": c.get("league") or m.get("league", ""),
                "home_team": c.get("home_team") or m.get("home_team", ""),
                "away_team": c.get("away_team") or m.get("away_team", ""),
                "market_primary": c.get("market_primary", ""),
                "competition_calibrated_prob": c.get("competition_calibrated_prob", ""),
                "accuracy_confidence_score": c.get("accuracy_confidence_score", ""),
                "accuracy_primary_risk": c.get("accuracy_primary_risk", ""),
                "fixture_datetime": fmt_dt(kickoff),
                "minutes_to_kickoff": minutes_to_kickoff,
                "prelock_window_minutes": str(args.window_minutes),
                "prelock_window_start": prelock_window_start,
                "useful_prelock_slots": fmt_slot_list(useful_slots),
                "next_useful_prelock_slot": next_useful_slot,
                "in_window_now": in_window_now,
                "prelock_retained": prelock_retained,
                "prelock_decision": p.get("prelock_decision", ""),
                "prelock_decision_reason": p.get("prelock_decision_reason", ""),
                "prelock_lineup_state": p.get("prelock_lineup_state", ""),
                "prelock_odds_state": p.get("prelock_odds_state", ""),
                "prelock_availability_state": p.get("prelock_availability_state", ""),
                "exclusion_reason": exclusion_reason,
                "next_action": next_action,
            }
        )

    fields = [
        "target_date",
        "generated_at",
        "fixture_id",
        "league",
        "home_team",
        "away_team",
        "market_primary",
        "competition_calibrated_prob",
        "accuracy_confidence_score",
        "accuracy_primary_risk",
        "fixture_datetime",
        "minutes_to_kickoff",
        "prelock_window_minutes",
        "prelock_window_start",
        "useful_prelock_slots",
        "next_useful_prelock_slot",
        "in_window_now",
        "prelock_retained",
        "prelock_decision",
        "prelock_decision_reason",
        "prelock_lineup_state",
        "prelock_odds_state",
        "prelock_availability_state",
        "exclusion_reason",
        "next_action",
    ]

    csv_path = today_dir / "vsigma_prelock_exclusion_audit.csv"
    md_path = today_dir / "vsigma_prelock_exclusion_audit.md"

    write_csv(csv_path, audit_rows, fields)

    retained_count = sum(1 for r in audit_rows if r["prelock_retained"] == "YES")
    in_window_count = sum(1 for r in audit_rows if r["in_window_now"] == "YES")

    md_lines = [
        f"# vSIGMA PRELOCK Exclusion Audit - {target_date}",
        "",
        f"- Generated at: {now.isoformat(timespec='seconds')}",
        f"- Timezone: {args.timezone}",
        f"- Candidates reviewed: {len(audit_rows)}",
        f"- In current 90-minute window: {in_window_count}",
        f"- Retained by PRELOCK output: {retained_count}",
        "",
        "## Audit",
        "",
        "| fixture_id | fixture | market | kickoff | min_to_ko | in_window | retained | exclusion_reason | next_action |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]

    for r in audit_rows:
        fixture = f"{r['home_team']} vs {r['away_team']}"
        md_lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(r["fixture_id"]),
                    md_cell(fixture),
                    md_cell(r["market_primary"]),
                    md_cell(r["fixture_datetime"]),
                    md_cell(r["minutes_to_kickoff"]),
                    md_cell(r["in_window_now"]),
                    md_cell(r["prelock_retained"]),
                    md_cell(r["exclusion_reason"]),
                    md_cell(r["next_action"]),
                ]
            )
            + " |"
        )

    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("=== PRELOCK EXCLUSION AUDIT ===")
    print(f"target_date={target_date}")
    print(f"candidates_reviewed={len(audit_rows)}")
    print(f"in_window_now={in_window_count}")
    print(f"prelock_retained={retained_count}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
