from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
TRUSTED_INPUT = "vsigma_raw_candidate_trust_gate.csv"
PROMOTION_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "fixture_datetime_utc", "promotion_status", "promotion_reason", "source_path", "allowed_downstream_use",
    "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "promoted_rows", "blocked_rows", "quarantine_rows",
    "promotion_status_counts", "next_action", "auto_apply", "production_change",
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


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date", "fixture_datetime_utc", "generated_at"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [row for row in rows if row_day(row) == day]


def scored_index(processed: Path, day: str) -> dict[str, dict[str, str]]:
    rows = []
    for path in [processed / "today" / day / "matches_vsigma_scored_v3.csv", processed / "matches_vsigma_scored_v3.csv"]:
        rows.extend(same_day(read_rows(path), day))
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = fixture_id(row)
        if fid and fid not in out:
            out[fid] = row
    return out


def is_no_data_blocked(row: dict[str, str]) -> bool:
    return "NO_DATA_BLOCKED" in " ".join(up(v) for v in row.values())


def has_core_data(row: dict[str, str]) -> bool:
    text = " ".join(up(row.get(field)) for field in [
        "recent_stats_quality_flag", "odds_structure_depth_status", "injuries_quality_flag",
        "league_coverage_class", "lineup_quality_flag", "data_warning"
    ])
    return "NO_DATA_BLOCKED" not in text and any(token in text for token in ["OK_FULL", "COVERAGE_RICH", "FULL"])


def classify(row: dict[str, str], scored: dict[str, dict[str, str]]) -> tuple[str, str, str]:
    if up(row.get("raw_trust_status")) != "TRUSTED_RAW_SOURCE":
        return "NOT_TRUSTED_NO_PROMOTION", "raw candidate is not TRUSTED_RAW_SOURCE", "DIAGNOSTIC_ONLY"
    fid = fixture_id(row)
    scored_row = scored.get(fid)
    if not scored_row:
        return "TRUSTED_SOURCE_BUT_NO_SCORED_ROW", "trusted raw candidate has no matching scored row", "WAIT_SCORING"
    if is_no_data_blocked(scored_row):
        return "TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED", "matching scored row is NO_DATA_BLOCKED", "NO_PROMOTION_NO_BET"
    if not has_core_data(scored_row):
        return "TRUSTED_SOURCE_BUT_LOW_CORE_DATA", "matching scored row lacks core usable data", "NO_PROMOTION_NO_BET"
    return "PROMOTED_TO_SCORING_INPUT", "trusted source has matching scored row without blocking data warnings", "SCORING_ALLOWED_WITH_NORMAL_GATES"


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    trust_rows = same_day(read_rows(processed / "today" / day / TRUSTED_INPUT), day)
    scored = scored_index(processed, day)
    rows: list[dict[str, object]] = []
    for row in trust_rows:
        status, reason, allowed = classify(row, scored)
        rows.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": fixture_id(row),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "fixture_datetime_utc": norm(row.get("fixture_datetime_utc")),
            "promotion_status": status,
            "promotion_reason": reason,
            "source_path": norm(row.get("source_path")),
            "allowed_downstream_use": allowed,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    promoted = [row for row in rows if row["promotion_status"] == "PROMOTED_TO_SCORING_INPUT"]
    blocked = sum(1 for row in rows if "NO_PROMOTION" in str(row.get("allowed_downstream_use")) or "NO_DATA_BLOCKED" in str(row.get("promotion_status")))
    quarantine = sum(1 for row in rows if "QUARANTINE" in str(row.get("promotion_status")) or "WAIT" in str(row.get("allowed_downstream_use")))
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(rows),
        "promoted_rows": len(promoted),
        "blocked_rows": blocked,
        "quarantine_rows": quarantine,
        "promotion_status_counts": counts(rows, "promotion_status"),
        "next_action": "No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows." if not promoted else "Promoted rows may feed normal scoring gates only.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return rows, summary, md(day, rows, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Trusted Raw Candidate Promotion Gate - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- promoted_rows: {summary['promoted_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- quarantine_rows: {summary['quarantine_rows']}",
        f"- promotion_status_counts: {summary['promotion_status_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Rows",
    ]
    if not rows:
        lines.append("- none. No raw trust gate rows found.")
    for row in rows:
        lines.append(f"- {row['home_team']} vs {row['away_team']} | status={row['promotion_status']} | allowed={row['allowed_downstream_use']} | reason={row['promotion_reason']} | source={row['source_path']}")
    lines += [
        "",
        "## Guardrails",
        "- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.",
        "- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.",
        "- NO_DATA_BLOCKED scored rows cannot be promoted.",
        "- Normal downstream gates remain mandatory even after promotion.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz, processed)
    promoted = [row for row in rows if row["promotion_status"] == "PROMOTED_TO_SCORING_INPUT"]
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_trusted_raw_candidate_promotion_gate.csv", rows, PROMOTION_FIELDS)
        write_csv(base / "vsigma_trusted_raw_candidate_promotion_summary.csv", summary, SUMMARY_FIELDS)
        write_csv(base / "vsigma_promoted_raw_fixture_candidates.csv", promoted, PROMOTION_FIELDS)
        (base / "vsigma_trusted_raw_candidate_promotion_gate.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA TRUSTED RAW CANDIDATE PROMOTION GATE ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"promoted_rows={summary[0]['promoted_rows']}")
    print(f"blocked_rows={summary[0]['blocked_rows']}")
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
