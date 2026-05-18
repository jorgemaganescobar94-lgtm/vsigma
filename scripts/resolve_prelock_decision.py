from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows


ROOT = Path(__file__).resolve().parents[1]

OFFICIAL_TOP = "vsigma_today_competition_top.csv"
PRELOCK_TOP = "vsigma_today_prelock_competition_top.csv"
PRELOCK_AUDIT = "vsigma_prelock_exclusion_audit.csv"
PRELOCK_REPORT = "vsigma_today_prelock_report.txt"
MATCHES = "matches.csv"
CLOUD_SUMMARY = "vsigma_cloud_decision_summary.csv"
RESOLVER_CSV = "vsigma_prelock_decision_resolver.csv"
RESOLVER_MD = "vsigma_prelock_decision_resolver.md"
LATEST_MD = "vsigma_prelock_decision_resolver_latest.md"

OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "fixture_datetime",
    "minutes_to_kickoff",
    "official_action",
    "executable_now",
    "final_block_reason",
    "retry_allowed",
    "next_retry_time",
    "data_gap_flags",
    "execution_family_status",
    "decision_source",
    "prelock_retained",
    "prelock_decision",
    "prelock_decision_reason",
    "exclusion_reason",
    "prelock_lineup_state",
    "prelock_odds_state",
    "prelock_availability_state",
]

BLOCKING_PRELOCK_DECISIONS = {"PRELOCK_REMOVED", "PRELOCK_DOWNGRADED", "PRELOCK_NOT_AVAILABLE"}


@dataclass(frozen=True)
class ResolverPaths:
    csv_path: Path
    md_path: Path
    latest_md_path: Path


def norm_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def read_text_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def read_fresh_csv(path: Path, target_date: str) -> pd.DataFrame:
    df = read_csv_lenient(path)
    if df.empty:
        return df
    fresh, _stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    return fresh.reset_index(drop=True)


def first_available(row: pd.Series | None, columns: Iterable[str]) -> object:
    if row is None:
        return ""
    for column in columns:
        if column in row.index and norm_text(row.get(column)):
            return row.get(column)
    return ""


def key_for_row(row: pd.Series | dict[str, object]) -> tuple[str, str]:
    return (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")))


def index_by_key(df: pd.DataFrame) -> dict[tuple[str, str], pd.Series]:
    rows: dict[tuple[str, str], pd.Series] = {}
    if df.empty:
        return rows
    for _, row in df.iterrows():
        key = key_for_row(row)
        if key[0] and key not in rows:
            rows[key] = row
    return rows


def lookup_row(index: dict[tuple[str, str], pd.Series], row: pd.Series) -> pd.Series | None:
    key = key_for_row(row)
    if key in index:
        return index[key]
    fixture_id = key[0]
    if not fixture_id:
        return None
    matches = [value for candidate_key, value in index.items() if candidate_key[0] == fixture_id]
    return matches[0] if matches else None


def parse_datetime(value: object, tz: ZoneInfo) -> datetime | None:
    text = norm_text(value)
    if not text or (len(text) == 10 and text.count("-") == 2):
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def parse_timestamp(value: object, tz: ZoneInfo) -> datetime | None:
    text = norm_text(value)
    if not text:
        return None
    try:
        return datetime.fromtimestamp(float(text), tz)
    except (TypeError, ValueError, OSError):
        return None


def kickoff_for(candidate: pd.Series, audit_row: pd.Series | None, prelock_row: pd.Series | None, match_row: pd.Series | None, tz: ZoneInfo) -> datetime | None:
    for row, columns in [
        (audit_row, ["fixture_datetime", "fixture_datetime_utc"]),
        (prelock_row, ["fixture_datetime", "fixture_datetime_utc"]),
        (candidate, ["fixture_datetime", "fixture_datetime_utc"]),
        (match_row, ["fixture_datetime", "fixture_datetime_utc"]),
    ]:
        parsed = parse_datetime(first_available(row, columns), tz)
        if parsed is not None:
            return parsed
    for row in [match_row, prelock_row, candidate]:
        parsed = parse_timestamp(first_available(row, ["fixture_timestamp"]), tz)
        if parsed is not None:
            return parsed
    return None


def fmt_dt(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.isoformat(timespec="minutes")


def useful_prelock_slots(kickoff: datetime, window_minutes: int, tz: ZoneInfo) -> list[datetime]:
    window_start = kickoff - timedelta(minutes=window_minutes)
    slots: list[datetime] = []
    for hour in range(10, 24):
        slot = datetime.combine(kickoff.date(), time(hour=hour), tzinfo=tz)
        if window_start <= slot < kickoff:
            slots.append(slot)
    return slots


def next_retry_slot(kickoff: datetime | None, now: datetime, window_minutes: int, tz: ZoneInfo) -> datetime | None:
    if kickoff is None or kickoff <= now:
        return None
    for slot in useful_prelock_slots(kickoff, window_minutes, tz):
        if slot > now:
            return slot
    return None


def source_candidates(official: pd.DataFrame, summary: pd.DataFrame, audit: pd.DataFrame, target_date: str) -> tuple[pd.DataFrame, str]:
    for frame, source in [(official, OFFICIAL_TOP), (summary, CLOUD_SUMMARY), (audit, PRELOCK_AUDIT)]:
        if frame.empty or "fixture_id" not in frame.columns:
            continue
        current = frame[frame["fixture_id"].fillna("").astype(str).str.strip().ne("")].copy()
        if "target_date" in current.columns:
            current = current[current["target_date"].astype(str).str[:10].eq(target_date)]
        if not current.empty:
            key_columns = [column for column in ["fixture_id", "market_primary"] if column in current.columns]
            return current.drop_duplicates(key_columns or None).reset_index(drop=True), source
    return pd.DataFrame(), "NO_CANDIDATES"


def state_missing_flags(lineup_state: str, odds_state: str, availability_state: str, reason_text: str = "") -> list[str]:
    flags: list[str] = []
    lineup = norm_upper(lineup_state)
    odds = norm_upper(odds_state)
    availability = norm_upper(availability_state)
    reason = reason_text.lower()

    if odds in {"ODDS_NOT_AVAILABLE", "ODDS_UNKNOWN"} or ("odds" in reason and "not available" in reason):
        flags.append("ODDS_MISSING")
    if lineup in {"LINEUPS_NOT_AVAILABLE", "LINEUPS_UNKNOWN"} or ("lineup" in reason and "not available" in reason):
        flags.append("LINEUPS_MISSING")
    if availability in {"AVAILABILITY_NOT_AVAILABLE", "AVAILABILITY_UNKNOWN"} or ("availability" in reason and "not available" in reason):
        flags.append("AVAILABILITY_MISSING")
    return flags


def final_reason_from_flags(flags: list[str]) -> str:
    reason_by_flag = {
        "ODDS_MISSING": "ODDS_NOT_AVAILABLE",
        "LINEUPS_MISSING": "LINEUPS_NOT_AVAILABLE",
        "AVAILABILITY_MISSING": "AVAILABILITY_NOT_AVAILABLE",
    }
    return ";".join(reason_by_flag[flag] for flag in flags if flag in reason_by_flag)


def resolve_row(
    candidate: pd.Series,
    *,
    target_date: str,
    generated_at: str,
    now: datetime,
    timezone: ZoneInfo,
    window_minutes: int,
    decision_source: str,
    prelock_row: pd.Series | None,
    audit_row: pd.Series | None,
    match_row: pd.Series | None,
    report_text: str,
) -> dict[str, object]:
    kickoff = kickoff_for(candidate, audit_row, prelock_row, match_row, timezone)
    minutes = round((kickoff - now).total_seconds() / 60.0, 2) if kickoff is not None else pd.NA
    retry_slot = next_retry_slot(kickoff, now, window_minutes, timezone)
    next_retry_time = fmt_dt(retry_slot)

    retained = prelock_row is not None or norm_upper(first_available(audit_row, ["prelock_retained"])) == "YES"
    prelock_decision = norm_upper(first_available(prelock_row, ["prelock_decision"]) or first_available(audit_row, ["prelock_decision"]))
    prelock_reason = norm_text(first_available(prelock_row, ["prelock_decision_reason"]) or first_available(audit_row, ["prelock_decision_reason"]))
    exclusion_reason = norm_upper(first_available(audit_row, ["exclusion_reason"]))
    lineup_state = norm_upper(first_available(prelock_row, ["prelock_lineup_state"]) or first_available(audit_row, ["prelock_lineup_state"]))
    odds_state = norm_upper(first_available(prelock_row, ["prelock_odds_state"]) or first_available(audit_row, ["prelock_odds_state"]))
    availability_state = norm_upper(first_available(prelock_row, ["prelock_availability_state"]) or first_available(audit_row, ["prelock_availability_state"]))
    flags = state_missing_flags(lineup_state, odds_state, availability_state, f"{prelock_reason} {report_text}")

    official_action = "TECHNICAL_REVIEW"
    executable_now = "NO"
    final_block_reason = "PRELOCK_STATE_UNCLASSIFIED"
    retry_allowed = "NO"
    execution_family_status = "TECHNICAL_REVIEW"

    if kickoff is None:
        final_block_reason = "MISSING_KICKOFF_DATETIME"
        execution_family_status = "TECHNICAL_REVIEW"
    elif kickoff <= now:
        official_action = "NO_BET"
        final_block_reason = "KICKOFF_ALREADY_PASSED"
        execution_family_status = "EXPIRED"
    else:
        in_window = 0 <= float(minutes) <= window_minutes
        if not in_window:
            official_action = "WAIT"
            final_block_reason = "OUTSIDE_PRELOCK_WINDOW"
            retry_allowed = "YES" if retry_slot is not None else "NO"
            execution_family_status = "WAITING_FOR_WINDOW"
        elif exclusion_reason == "IN_WINDOW_BUT_NOT_RETAINED":
            official_action = "NO_BET"
            final_block_reason = "PRELOCK_GOVERNANCE_NOT_RETAINED"
            retry_allowed = "YES" if retry_slot is not None else "NO"
            execution_family_status = "PRELOCK_NOT_RETAINED"
        elif prelock_decision == "PRELOCK_NOT_AVAILABLE" or exclusion_reason == "PRELOCK_NOT_AVAILABLE":
            if flags:
                final_block_reason = final_reason_from_flags(flags)
                retry_allowed = "YES" if retry_slot is not None else "NO"
                if "ODDS_MISSING" in flags:
                    official_action = "NO_BET"
                    execution_family_status = "DATA_GAP_BLOCKED"
                else:
                    official_action = "WAIT" if retry_slot is not None else "NO_BET"
                    execution_family_status = "WAITING_FOR_PRELOCK_DATA" if retry_slot is not None else "DATA_GAP_BLOCKED"
            else:
                official_action = "TECHNICAL_REVIEW"
                final_block_reason = "PRELOCK_NOT_AVAILABLE_UNCLASSIFIED"
                retry_allowed = "NO"
                execution_family_status = "TECHNICAL_REVIEW"
        elif retained and prelock_decision not in BLOCKING_PRELOCK_DECISIONS:
            official_action = "EXECUTABLE"
            executable_now = "YES"
            final_block_reason = "NONE"
            retry_allowed = "NO"
            next_retry_time = ""
            execution_family_status = "PRELOCK_CONFIRMED"
        elif prelock_decision in {"PRELOCK_REMOVED", "PRELOCK_DOWNGRADED"}:
            official_action = "NO_BET"
            final_block_reason = prelock_decision
            retry_allowed = "NO"
            execution_family_status = "PRELOCK_REJECTED"
        else:
            official_action = "TECHNICAL_REVIEW"
            final_block_reason = "PRELOCK_STATE_UNCLASSIFIED"
            retry_allowed = "NO"
            execution_family_status = "TECHNICAL_REVIEW"

    if retry_allowed == "NO":
        next_retry_time = ""

    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "fixture_id": norm_text(candidate.get("fixture_id")),
        "league": norm_text(first_available(audit_row, ["league"]) or first_available(prelock_row, ["league"]) or first_available(candidate, ["league"]) or first_available(match_row, ["league"])),
        "home_team": norm_text(first_available(audit_row, ["home_team"]) or first_available(prelock_row, ["home_team"]) or first_available(candidate, ["home_team"]) or first_available(match_row, ["home_team"])),
        "away_team": norm_text(first_available(audit_row, ["away_team"]) or first_available(prelock_row, ["away_team"]) or first_available(candidate, ["away_team"]) or first_available(match_row, ["away_team"])),
        "market_primary": norm_upper(first_available(candidate, ["market_primary"]) or first_available(prelock_row, ["market_primary"]) or first_available(audit_row, ["market_primary"])),
        "fixture_datetime": fmt_dt(kickoff),
        "minutes_to_kickoff": minutes,
        "official_action": official_action,
        "executable_now": executable_now,
        "final_block_reason": final_block_reason,
        "retry_allowed": retry_allowed,
        "next_retry_time": next_retry_time,
        "data_gap_flags": ";".join(flags),
        "execution_family_status": execution_family_status,
        "decision_source": decision_source,
        "prelock_retained": "YES" if retained else "NO",
        "prelock_decision": prelock_decision,
        "prelock_decision_reason": prelock_reason,
        "exclusion_reason": exclusion_reason,
        "prelock_lineup_state": lineup_state,
        "prelock_odds_state": odds_state,
        "prelock_availability_state": availability_state,
    }


def official_action_summary(resolver: pd.DataFrame) -> str:
    if resolver.empty or "official_action" not in resolver.columns:
        return "NO_BET"
    actions = [norm_upper(value) for value in resolver["official_action"].tolist() if norm_upper(value)]
    if not actions:
        return "NO_BET"
    unique = set(actions)
    if len(unique) == 1:
        return actions[0]
    if "TECHNICAL_REVIEW" in unique:
        return "TECHNICAL_REVIEW"
    return "MIXED"


def write_markdown(resolver: pd.DataFrame, paths: ResolverPaths, target_date: str) -> None:
    candidates = 0 if resolver["final_block_reason"].astype(str).eq("NO_CANDIDATES").all() else len(resolver)
    executable = int(resolver["official_action"].astype(str).eq("EXECUTABLE").sum())
    waiting = int(resolver["official_action"].astype(str).eq("WAIT").sum())
    no_bet = int(resolver["official_action"].astype(str).eq("NO_BET").sum())
    technical = int(resolver["official_action"].astype(str).eq("TECHNICAL_REVIEW").sum())
    retry_values = [value for value in resolver["next_retry_time"].dropna().astype(str).tolist() if value.strip()]
    next_retry = min(retry_values) if retry_values else "NONE"
    gap_series = resolver["data_gap_flags"].fillna("").astype(str)
    odds_missing = int(gap_series.str.contains("ODDS_MISSING", regex=False).sum())
    lineups_missing = int(gap_series.str.contains("LINEUPS_MISSING", regex=False).sum())
    availability_missing = int(gap_series.str.contains("AVAILABILITY_MISSING", regex=False).sum())

    actions = resolver.copy()
    actions["fixture"] = actions["home_team"].fillna("").astype(str) + " vs " + actions["away_team"].fillna("").astype(str)
    lines = [
        f"# vSIGMA PRELOCK Decision Resolver - {target_date}",
        "",
        "## Summary",
        f"- Candidates reviewed: {candidates}",
        f"- Executable now: {executable}",
        f"- Waiting: {waiting}",
        f"- No bet: {no_bet}",
        f"- Technical review: {technical}",
        f"- Next automatic retry: {next_retry}",
        f"- OFFICIAL_ACTION_SUMMARY: {official_action_summary(resolver)}",
        "",
        "## Official Actions",
        format_markdown_table(
            actions,
            [
                "fixture",
                "market_primary",
                "fixture_datetime",
                "minutes_to_kickoff",
                "official_action",
                "executable_now",
                "final_block_reason",
                "next_retry_time",
            ],
            max_rows=100,
        ),
        "",
        "## Data Gaps",
        f"- odds missing: {odds_missing}",
        f"- lineups missing: {lineups_missing}",
        f"- availability missing: {availability_missing}",
        "",
        "## Notes",
        "This resolver does not change predictions, thresholds, calibration, probability formulas, or base selection. It only translates PRELOCK state into an operational execution decision.",
        "",
    ]
    markdown = "\n".join(lines)
    paths.md_path.write_text(markdown, encoding="utf-8")
    paths.latest_md_path.write_text(markdown, encoding="utf-8")


def resolve_prelock_decisions(
    *,
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    window_minutes: int = 90,
    processed_dir: Path = PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[pd.DataFrame, ResolverPaths]:
    target_date = pd.Timestamp(target_date).date().isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now is not None else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    snap = snapshot_dir(processed_dir, target_date)
    governance_dir = processed_dir / "governance"
    snap.mkdir(parents=True, exist_ok=True)
    governance_dir.mkdir(parents=True, exist_ok=True)

    official = read_fresh_csv(snap / OFFICIAL_TOP, target_date)
    prelock = read_fresh_csv(snap / PRELOCK_TOP, target_date)
    audit = read_fresh_csv(snap / PRELOCK_AUDIT, target_date)
    matches = read_csv_lenient(snap / MATCHES)
    summary = read_fresh_csv(snap / CLOUD_SUMMARY, target_date)
    report_text = read_text_optional(snap / PRELOCK_REPORT)

    candidates, decision_source = source_candidates(official, summary, audit, target_date)
    prelock_index = index_by_key(prelock)
    audit_index = index_by_key(audit)
    match_index = index_by_key(matches)

    rows: list[dict[str, object]] = []
    if candidates.empty:
        rows.append(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "fixture_id": "",
                "league": "",
                "home_team": "",
                "away_team": "",
                "market_primary": "",
                "fixture_datetime": "",
                "minutes_to_kickoff": "",
                "official_action": "NO_BET",
                "executable_now": "NO",
                "final_block_reason": "NO_CANDIDATES",
                "retry_allowed": "NO",
                "next_retry_time": "",
                "data_gap_flags": "",
                "execution_family_status": "NO_CANDIDATES",
                "decision_source": decision_source,
                "prelock_retained": "NO",
                "prelock_decision": "",
                "prelock_decision_reason": "",
                "exclusion_reason": "",
                "prelock_lineup_state": "",
                "prelock_odds_state": "",
                "prelock_availability_state": "",
            }
        )
    else:
        for _, candidate in candidates.iterrows():
            rows.append(
                resolve_row(
                    candidate,
                    target_date=target_date,
                    generated_at=generated_at,
                    now=now,
                    timezone=timezone,
                    window_minutes=window_minutes,
                    decision_source=decision_source,
                    prelock_row=lookup_row(prelock_index, candidate),
                    audit_row=lookup_row(audit_index, candidate),
                    match_row=lookup_row(match_index, candidate),
                    report_text=report_text,
                )
            )

    resolver = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
    paths = ResolverPaths(
        csv_path=snap / RESOLVER_CSV,
        md_path=snap / RESOLVER_MD,
        latest_md_path=governance_dir / LATEST_MD,
    )
    resolver.to_csv(paths.csv_path, index=False)
    write_markdown(resolver, paths, target_date)
    return resolver, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve vSIGMA PRELOCK state into final operational decisions.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--window-minutes", type=int, default=90)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    resolver, paths = resolve_prelock_decisions(
        target_date=args.date,
        timezone_name=args.timezone,
        window_minutes=args.window_minutes,
        processed_dir=args.processed_dir,
    )
    print("=== VSIGMA PRELOCK DECISION RESOLVER ===")
    print(f"target_date={pd.Timestamp(args.date).date().isoformat()}")
    print(f"rows={len(resolver)}")
    print(f"official_action_summary={official_action_summary(resolver)}")
    print(f"csv={paths.csv_path}")
    print(f"md={paths.md_path}")
    print(f"latest_md={paths.latest_md_path}")


if __name__ == "__main__":
    main()
