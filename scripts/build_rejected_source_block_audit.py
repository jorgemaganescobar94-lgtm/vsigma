from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "fixture_datetime_utc", "source_path", "raw_trust_status", "audit_bucket", "review_priority",
    "trust_expansion_candidate", "audit_reason", "suggested_action", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "rejected_rows", "correct_reject_rows",
    "manual_review_rows", "whitelist_candidate_rows", "audit_bucket_counts", "review_priority_counts",
    "next_action", "auto_apply", "production_change",
]

LOW_TRUST_LEAGUE_TOKENS = [
    "U17", "U18", "U19", "U20", "U21", "U23", "WOMEN", "FEMEN", "RESERVE", "RESERVES",
    "YOUTH", "ACADEMY", "JUNIOR", "B", "II", "III", "IV", "FRIENDLIES", "FRIENDLY",
    "LANDESLIGA", "REGIONALLIGA", "OBERLIGA", "4. LIGA", "USL LEAGUE TWO", "1. LIGA CLASSIC",
]
LOW_TRUST_TEAM_TOKENS = [" U17", " U18", " U19", " U20", " U21", " U23", " II", " III", " B", " RESERVE", "WOMEN"]
POTENTIAL_SENIOR_TOKENS = [
    "PREMIER", "PRIMERA", "LIGUE 1", "SERIE A", "SERIE B", "COPA", "CUP", "PLAY-OFFS",
    "PLAYOFF", "DIVISION", "LEAGUE", "LIGA", "CHAMPIONSHIP", "ELITESERIEN", "ALLSVENSKAN",
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


def load_raw_trust_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_raw_candidate_trust_gate.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_raw_candidate_trust_gate.csv")
    return rows


def has_token(text: str, tokens: list[str]) -> bool:
    return any(token in text for token in tokens)


def classify(row: dict[str, str]) -> tuple[str, str, str, str, str]:
    league = up(row.get("league"))
    teams = f" {up(row.get('home_team'))} {up(row.get('away_team'))} "
    source = up(row.get("source_path"))
    fixture_id = norm(row.get("fixture_id"))
    status = up(row.get("raw_trust_status"))

    if status != "REJECTED_SOURCE_BLOCK":
        return (
            "NOT_REJECTED_CONTROL_ROW",
            "P0_NOT_APPLICABLE",
            "NO",
            "row is not REJECTED_SOURCE_BLOCK",
            "No action. This audit only reviews rejected source blocks.",
        )
    if not fixture_id:
        return (
            "CORRECT_REJECT_MISSING_IDENTITY",
            "P3_CORRECT_REJECT",
            "NO",
            "fixture identity is missing",
            "Keep rejected; identity is insufficient for scoring.",
        )
    if has_token(league, ["U17", "U18", "U19", "U20", "U21", "U23", "YOUTH", "JUNIOR", "ACADEMY"]) or has_token(teams, LOW_TRUST_TEAM_TOKENS):
        return (
            "CORRECT_REJECT_YOUTH_RESERVE",
            "P3_CORRECT_REJECT",
            "NO",
            "youth/reserve/team suffix detected",
            "Keep rejected unless a specific competition is manually whitelisted later.",
        )
    if has_token(league, ["WOMEN", "FEMEN"]):
        return (
            "CORRECT_REJECT_WOMEN_LOW_MODEL_COVERAGE",
            "P3_CORRECT_REJECT",
            "NO",
            "women competition detected outside current whitelist",
            "Keep rejected until a separate women-football model exists.",
        )
    if has_token(league, ["FRIENDLIES", "FRIENDLY"]):
        return (
            "CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY",
            "P3_CORRECT_REJECT",
            "NO",
            "friendly context is volatile and low-accountability",
            "Keep rejected or route to manual-only context review, not scoring.",
        )
    if has_token(league, ["LANDESLIGA", "REGIONALLIGA", "OBERLIGA", "4. LIGA", "USL LEAGUE TWO", "1. LIGA CLASSIC"]):
        return (
            "CORRECT_REJECT_LOW_TIER_LOW_COVERAGE",
            "P3_CORRECT_REJECT",
            "NO",
            "low-tier or low-coverage competition detected",
            "Keep rejected; do not spend enrichment unless manually selected for research.",
        )
    if "MATCHES_LEAGUE_REJECTED" in source and has_token(league, POTENTIAL_SENIOR_TOKENS):
        return (
            "MANUAL_REVIEW_POSSIBLE_WHITELIST",
            "P1_REVIEW_CANDIDATE",
            "YES_REVIEW_ONLY",
            "source was rejected but league name looks like senior/structured competition",
            "Review league, country, fixture identity and API coverage before any future whitelist; do not auto-promote.",
        )
    if "MATCHES_LEAGUE_REJECTED" in source:
        return (
            "REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION",
            "P2_REVIEW_LOW_CONFIDENCE",
            "MAYBE_REVIEW_ONLY",
            "source is rejected and no strong low-trust token or senior token was detected",
            "Keep rejected by default; sample manually only if repeated and coverage is good.",
        )
    return (
        "REVIEW_UNEXPECTED_REJECT_STATE",
        "P2_REVIEW_LOW_CONFIDENCE",
        "MAYBE_REVIEW_ONLY",
        "rejected status did not match expected source/path pattern",
        "Inspect row manually; do not auto-promote.",
    )


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = load_raw_trust_rows(processed, day)
    out = []
    for row in rows:
        if up(row.get("raw_trust_status")) != "REJECTED_SOURCE_BLOCK":
            continue
        bucket, priority, candidate, reason, action = classify(row)
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
            "raw_trust_status": norm(row.get("raw_trust_status")),
            "audit_bucket": bucket,
            "review_priority": priority,
            "trust_expansion_candidate": candidate,
            "audit_reason": reason,
            "suggested_action": action,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    correct = [r for r in out if str(r["review_priority"]).startswith("P3")]
    manual = [r for r in out if not str(r["review_priority"]).startswith("P3")]
    whitelist = [r for r in out if str(r["trust_expansion_candidate"]).startswith("YES")]
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(out),
        "rejected_rows": len(out),
        "correct_reject_rows": len(correct),
        "manual_review_rows": len(manual),
        "whitelist_candidate_rows": len(whitelist),
        "audit_bucket_counts": counts(out, "audit_bucket"),
        "review_priority_counts": counts(out, "review_priority"),
        "next_action": "Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{k}={v}" for k, v in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Rejected Source Block Audit - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- rejected_rows: {summary['rejected_rows']}",
        f"- correct_reject_rows: {summary['correct_reject_rows']}",
        f"- manual_review_rows: {summary['manual_review_rows']}",
        f"- whitelist_candidate_rows: {summary['whitelist_candidate_rows']}",
        f"- audit_bucket_counts: {summary['audit_bucket_counts']}",
        f"- review_priority_counts: {summary['review_priority_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Review Candidates",
    ]
    review_rows = [r for r in rows if not str(r["review_priority"]).startswith("P3")]
    if not review_rows:
        lines.append("- none. All rejected rows were classified as correct rejects.")
    for row in review_rows[:80]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | league={row['league']} | bucket={row['audit_bucket']} | priority={row['review_priority']} | candidate={row['trust_expansion_candidate']} | reason={row['audit_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This audit is advisory only.",
        "- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.",
        "- Any trust expansion must be implemented in a separate reviewed change after sample validation.",
    ]
    return "\n".join(lines) + "\n"


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    lines = [
        "## Rejected Source Block Audit",
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- correct_reject_rows: {summary.get('correct_reject_rows', 'UNKNOWN')}",
        f"- manual_review_rows: {summary.get('manual_review_rows', 'UNKNOWN')}",
        f"- whitelist_candidate_rows: {summary.get('whitelist_candidate_rows', 'UNKNOWN')}",
        f"- audit_bucket_counts: {summary.get('audit_bucket_counts', 'UNKNOWN')}",
        f"- review_priority_counts: {summary.get('review_priority_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    section = "## Rejected Source Block Audit"
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            if section in text:
                before = text.split(section, 1)[0].rstrip()
                after = text.split(section, 1)[1]
                next_idx = after.find("\n## ")
                tail = after[next_idx:] if next_idx >= 0 else ""
                text = before + block + tail
            else:
                text = text.rstrip() + block
            md_path.write_text(text, encoding="utf-8")


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_rejected_source_block_audit.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_rejected_source_block_audit_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_rejected_source_block_audit.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA REJECTED SOURCE BLOCK AUDIT ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"correct_reject_rows={summary[0]['correct_reject_rows']}")
    print(f"manual_review_rows={summary[0]['manual_review_rows']}")
    print(f"whitelist_candidate_rows={summary[0]['whitelist_candidate_rows']}")
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
