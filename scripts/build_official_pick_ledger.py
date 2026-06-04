from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
TODAY = PROCESSED / "today"
GOVERNANCE = PROCESSED / "governance"

EXECUTABLE_DECISIONS = {
    "READY_LOW_STAKE_REVIEW",
    "REVIEW_LOW_STAKE",
    "PRELOCK_REVIEW",
    "ACTION_REVIEW_NOW",
    "EXECUTABLE_PREMATCH",
    "PREMATCH_CORE",
    "CORE_PREMATCH",
}
LIVE_DECISIONS = {
    "LIVE_ONLY",
    "LIVE_ONLY_WAIT_TRIGGER",
    "LIVE_RECHECK_ONLY",
}
WATCH_DECISIONS = {
    "STAT_WATCH_ONLY",
    "NO_BET_OR_WATCH",
    "WATCH_ONLY",
    "WEAK_WATCH",
}
NO_BET_DECISIONS = {
    "NO_BET",
    "CANCELLED_NO_BET",
    "BLOCKED",
}

FIELDS = [
    "target_date",
    "generated_at",
    "ledger_key",
    "fixture_id",
    "home_team",
    "away_team",
    "league",
    "country",
    "board_rank",
    "final_decision",
    "decision_bucket",
    "board_bucket",
    "primary_market",
    "secondary_market",
    "stake_band",
    "execution_permission",
    "portfolio_status",
    "context_level",
    "forecast_confidence",
    "forecast_warning",
    "translation_score",
    "kill_switch",
    "stat_profile",
    "prelock_trigger",
    "live_trigger",
    "cancel_trigger",
    "source_guard",
    "operator_action_level",
    "operator_final_decision",
    "operator_risk_label",
    "operator_health_status",
    "ledger_status",
    "official_pick_permission",
    "pick_tracking_required",
    "postmatch_audit_required",
    "result_status",
    "postmatch_quality_label",
    "postmatch_quality_score",
    "learning_status",
    "operator_note",
    "auto_apply",
    "production_change",
]


def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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


def meta(text: str, key: str) -> str:
    match = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return match.group(1).strip() if match else "UNKNOWN"


def row_value(row: dict[str, str], *names: str, default: str = "") -> str:
    for name in names:
        value = norm(row.get(name))
        if value:
            return value
    return default


def decision_of(row: dict[str, str]) -> str:
    return row_value(row, "final_decision", "recheck_decision", "base_decision", default="UNKNOWN")


def fixture_id(row: dict[str, str]) -> str:
    value = row_value(row, "fixture_id", default="")
    return value.replace(".0", "").strip()


def team_line(row: dict[str, str]) -> str:
    home = row_value(row, "home_team", default="UNKNOWN_HOME")
    away = row_value(row, "away_team", default="UNKNOWN_AWAY")
    return f"{home} vs {away}"


def classify_decision(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    decision = decision_of(row)
    fid = fixture_id(row)
    board_bucket = row_value(row, "board_bucket", default="")
    source_guard = row_value(row, "source_guard", default="")

    is_diagnostic = fid.startswith("DIAGNOSTIC") or "DIAGNOSTIC" in source_guard or "DIAGNOSTIC" in board_bucket
    if is_diagnostic:
        return (
            "DIAGNOSTIC_NO_PICK",
            "DIAGNOSTIC_ONLY",
            "NO_PICK_NO_STAKE",
            "NO",
            "NO",
            "DIAGNOSTIC_NO_FIXTURE",
        )

    if decision in EXECUTABLE_DECISIONS:
        return (
            "OFFICIAL_REVIEW_REQUIRED",
            "EXECUTABLE_PREMATCH",
            "MANUAL_REVIEW_ONLY_NO_STAKE",
            "YES",
            "YES",
            "PENDING_RESULT",
        )
    if decision in LIVE_DECISIONS:
        return (
            "LIVE_REVIEW_REQUIRED",
            "LIVE_ONLY",
            "MANUAL_REVIEW_ONLY_NO_STAKE",
            "YES",
            "YES",
            "PENDING_RESULT",
        )
    if decision in WATCH_DECISIONS:
        return (
            "WATCH_ONLY",
            "WATCHLIST",
            "NO_PICK_NO_STAKE",
            "YES",
            "YES",
            "PENDING_WATCH_AUDIT",
        )
    if decision in NO_BET_DECISIONS:
        return (
            "OFFICIAL_NO_BET",
            "NO_BET",
            "NO_PICK_NO_STAKE",
            "YES",
            "YES",
            "PENDING_NO_BET_AUDIT",
        )
    return (
        "UNKNOWN_DECISION_REVIEW",
        "UNKNOWN",
        "NO_PICK_NO_STAKE",
        "YES",
        "YES",
        "PENDING_MANUAL_REVIEW",
    )


def operator_context(folder: Path) -> dict[str, str]:
    brief = read_text(folder / "vsigma_operator_brief.md")
    return {
        "operator_action_level": meta(brief, "action_level"),
        "operator_final_decision": meta(brief, "compact_final_decision"),
        "operator_risk_label": meta(brief, "risk_label"),
        "operator_health_status": meta(brief, "health_status"),
    }


def make_key(day: str, row: dict[str, str], idx: int) -> str:
    fid = fixture_id(row)
    market = row_value(row, "primary_market", "market", default="NO_MARKET")
    if fid:
        return f"{day}|{fid}|{market}"
    return f"{day}|ROW_{idx}|{team_line(row)}|{market}"


def build_rows(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = processed / "today" / day
    board_rows = read_csv(folder / "vsigma_daily_execution_board.csv")
    op = operator_context(folder)

    if not board_rows:
        board_rows = [{
            "fixture_id": "DIAGNOSTIC_NO_BOARD",
            "home_team": "NO_DAILY_BOARD",
            "away_team": "NO_DAILY_BOARD",
            "final_decision": "NO_BET",
            "board_bucket": "DIAGNOSTIC_NO_BOARD",
            "primary_market": "NO_MARKET",
            "execution_permission": "NO_BET",
            "source_guard": "OFFICIAL_PICK_LEDGER_DIAGNOSTIC_ONLY",
            "operator_note": "daily execution board missing; no pick permission",
            "auto_apply": "NO",
            "production_change": "NO",
        }]

    out: list[dict[str, object]] = []
    for idx, row in enumerate(board_rows, start=1):
        ledger_status, decision_bucket, permission, tracking, postmatch, result = classify_decision(row)
        enriched = {
            "target_date": day,
            "generated_at": generated,
            "ledger_key": make_key(day, row, idx),
            "fixture_id": fixture_id(row),
            "home_team": row_value(row, "home_team", default="UNKNOWN_HOME"),
            "away_team": row_value(row, "away_team", default="UNKNOWN_AWAY"),
            "league": row_value(row, "league", default=""),
            "country": row_value(row, "country", default=""),
            "board_rank": row_value(row, "board_rank", "rank", default=str(idx)),
            "final_decision": decision_of(row),
            "decision_bucket": decision_bucket,
            "board_bucket": row_value(row, "board_bucket", default=""),
            "primary_market": row_value(row, "primary_market", "market", default="NO_MARKET"),
            "secondary_market": row_value(row, "secondary_market", default=""),
            "stake_band": row_value(row, "stake_band", default="NO_STAKE"),
            "execution_permission": row_value(row, "execution_permission", default="NO_BET"),
            "portfolio_status": row_value(row, "portfolio_status", default=""),
            "context_level": row_value(row, "context_level", default=""),
            "forecast_confidence": row_value(row, "forecast_confidence", default=""),
            "forecast_warning": row_value(row, "forecast_warning", default=""),
            "translation_score": row_value(row, "translation_score", default=""),
            "kill_switch": row_value(row, "kill_switch", default=""),
            "stat_profile": row_value(row, "stat_profile", default=""),
            "prelock_trigger": row_value(row, "prelock_trigger", default=""),
            "live_trigger": row_value(row, "live_trigger", default=""),
            "cancel_trigger": row_value(row, "cancel_trigger", default=""),
            "source_guard": row_value(row, "source_guard", default=""),
            **op,
            "ledger_status": ledger_status,
            "official_pick_permission": permission,
            "pick_tracking_required": tracking,
            "postmatch_audit_required": postmatch,
            "result_status": result,
            "postmatch_quality_label": "PENDING",
            "postmatch_quality_score": "",
            "learning_status": "PENDING_POSTMATCH" if postmatch == "YES" else "DIAGNOSTIC_ONLY_NO_LEARNING",
            "operator_note": row_value(row, "operator_note", default=""),
            "auto_apply": "NO",
            "production_change": "NO",
        }
        out.append(enriched)
    return out


def update_historical_ledger(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    path = processed / "governance" / "vsigma_official_pick_ledger.csv"
    existing = read_csv(path)
    existing = [row for row in existing if row.get("target_date") != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(path, existing, FIELDS)


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    buckets = Counter(str(row.get("decision_bucket", "UNKNOWN")) for row in rows)
    statuses = Counter(str(row.get("ledger_status", "UNKNOWN")) for row in rows)
    permissions = Counter(str(row.get("official_pick_permission", "UNKNOWN")) for row in rows)
    tracking = Counter(str(row.get("postmatch_audit_required", "UNKNOWN")) for row in rows)

    lines = [
        f"# vSIGMA Official Pick Ledger - {day}",
        "",
        "## Summary",
        f"- ledger_rows: {len(rows)}",
        f"- decision_bucket_counts: {fmt_counts(buckets)}",
        f"- ledger_status_counts: {fmt_counts(statuses)}",
        f"- official_pick_permission_counts: {fmt_counts(permissions)}",
        f"- postmatch_audit_required_counts: {fmt_counts(tracking)}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Ledger Rows",
    ]
    for row in rows[:60]:
        lines.append(
            "- "
            f"{row.get('board_rank', '')} | {row.get('ledger_status', '')} | "
            f"{row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"market={row.get('primary_market', '')} | "
            f"decision={row.get('final_decision', '')} | "
            f"permission={row.get('official_pick_permission', '')} | "
            f"audit={row.get('postmatch_audit_required', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This ledger records official daily decisions; it does not create picks.",
        "- NO_BET rows are first-class learning objects, not failures by default.",
        "- No row creates stake permission or betting execution.",
        "- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.",
    ]
    return "\n".join(lines) + "\n"


def fmt_counts(counter: Counter[str]) -> str:
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build_rows(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_official_pick_ledger_daily.csv", rows, FIELDS)
        (base / "vsigma_official_pick_ledger.md").write_text(markdown(day, rows), encoding="utf-8")
    update_historical_ledger(processed, day, rows)

    buckets = Counter(str(row.get("decision_bucket", "UNKNOWN")) for row in rows)
    permissions = Counter(str(row.get("official_pick_permission", "UNKNOWN")) for row in rows)
    print("=== VSIGMA OFFICIAL PICK LEDGER ===")
    print(f"ledger_rows={len(rows)}")
    print(f"decision_bucket_counts={fmt_counts(buckets)}")
    print(f"official_pick_permission_counts={fmt_counts(permissions)}")
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
