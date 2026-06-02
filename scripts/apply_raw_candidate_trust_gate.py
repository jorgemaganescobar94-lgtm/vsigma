from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
INPUT_NAME = "vsigma_local_raw_fixture_discovery_candidates.csv"
OUTPUT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "fixture_datetime_utc", "source_path", "raw_trust_status", "trust_reason",
    "allowed_downstream_use", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "trusted_rows", "quarantine_rows",
    "blocked_rows", "trust_status_counts", "next_action", "auto_apply", "production_change",
]
REJECTED_SOURCE_TOKENS = ["matches_league_rejected", "rejected"]
LOW_TRUST_COMPETITION_TOKENS = [" U17", "U17", " U19", "U19", " U20", "U20", " U21", "U21", " U23", "U23", "W LEAGUE", " WOMEN", " WOMEN'S", " FEMEN", "REVELA", "ACADEM", "RESERVE", "II W"]


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


def source_rejected(row: dict[str, str]) -> bool:
    source = up(row.get("source_path"))
    return any(token.upper() in source for token in REJECTED_SOURCE_TOKENS)


def low_trust_competition(row: dict[str, str]) -> bool:
    text = " ".join([up(row.get("league")), up(row.get("home_team")), up(row.get("away_team"))])
    return any(token in text for token in LOW_TRUST_COMPETITION_TOKENS)


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    if source_rejected(row):
        return "REJECTED_SOURCE_BLOCK", "source path indicates the fixture came from rejected league/filter output", "DIAGNOSTIC_ONLY_NO_SCORING"
    if low_trust_competition(row):
        return "QUARANTINE_REVIEW", "youth/women/reserve/academy competition requires explicit whitelist before scoring", "QUARANTINE_ONLY"
    return "TRUSTED_RAW_SOURCE", "source is not rejected and competition is not low-trust by token gate", "SCORING_ALLOWED_WITH_NORMAL_GATES"


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = read_rows(processed / "today" / day / INPUT_NAME)
    out: list[dict[str, object]] = []
    for row in rows:
        status, reason, allowed = classify(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "fixture_datetime_utc": norm(row.get("fixture_datetime_utc")),
            "source_path": norm(row.get("source_path")),
            "raw_trust_status": status,
            "trust_reason": reason,
            "allowed_downstream_use": allowed,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    trusted = [row for row in out if row["raw_trust_status"] == "TRUSTED_RAW_SOURCE"]
    q = sum(1 for row in out if row["raw_trust_status"] == "QUARANTINE_REVIEW")
    blocked = sum(1 for row in out if row["raw_trust_status"] == "REJECTED_SOURCE_BLOCK")
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(out),
        "trusted_rows": len(trusted),
        "quarantine_rows": q,
        "blocked_rows": blocked,
        "trust_status_counts": counts(out, "raw_trust_status"),
        "next_action": "Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, md(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Raw Candidate Trust Gate - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- trusted_rows: {summary['trusted_rows']}",
        f"- quarantine_rows: {summary['quarantine_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- trust_status_counts: {summary['trust_status_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Rows",
    ]
    if not rows:
        lines.append("- none. No local raw fixture discovery candidates found.")
    for row in rows:
        lines.append(f"- {row['home_team']} vs {row['away_team']} | league={row['league']} | status={row['raw_trust_status']} | allowed={row['allowed_downstream_use']} | reason={row['trust_reason']} | source={row['source_path']}")
    lines += [
        "",
        "## Guardrails",
        "- Trust gate is defensive and can only restrict downstream use.",
        "- Rejected source rows cannot feed scoring without explicit future whitelist.",
        "- Youth/women/reserve/academy rows remain quarantine-only unless explicitly whitelisted.",
        "- No bets, stakes, secrets, API calls, or safety gates are changed.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz, processed)
    trusted = [row for row in rows if row["raw_trust_status"] == "TRUSTED_RAW_SOURCE"]
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_raw_candidate_trust_gate.csv", rows, OUTPUT_FIELDS)
        write_csv(base / "vsigma_raw_candidate_trust_gate_summary.csv", summary, SUMMARY_FIELDS)
        write_csv(base / "vsigma_trusted_raw_fixture_candidates.csv", trusted, OUTPUT_FIELDS)
        (base / "vsigma_raw_candidate_trust_gate.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA RAW CANDIDATE TRUST GATE ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"trusted_rows={summary[0]['trusted_rows']}")
    print(f"quarantine_rows={summary[0]['quarantine_rows']}")
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
