from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

ROW_FIELDS = [
    "target_date", "generated_at", "review_rank", "fixture_id", "league", "country",
    "home_team", "away_team", "fixture_datetime_utc", "source_path", "audit_bucket",
    "review_priority", "trust_expansion_candidate", "audit_reason", "suggested_action",
    "manual_review_status", "manual_decision", "decision_required", "risk_label",
    "whitelist_permission", "canonical_board_permission", "scoring_permission",
    "api_enrichment_permission", "pick_permission", "stake_permission", "operator_note",
    "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "review_rows", "p1_review_rows", "p2_review_rows",
    "manual_review_status_counts", "manual_decision_counts", "risk_label_counts",
    "whitelist_permission_counts", "canonical_board_permission_counts", "scoring_permission_counts",
    "api_enrichment_permission_counts", "pick_permission_counts", "stake_permission_counts",
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


def load_audit_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_rejected_source_block_audit.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_rejected_source_block_audit.csv")
    return rows


def include_for_manual_board(row: dict[str, str]) -> bool:
    priority = up(row.get("review_priority"))
    candidate = up(row.get("trust_expansion_candidate"))
    return priority == "P1_REVIEW_CANDIDATE" or candidate.startswith("YES")


def risk_label(row: dict[str, str]) -> str:
    bucket = up(row.get("audit_bucket"))
    reason = up(row.get("audit_reason"))
    if "UNKNOWN" in bucket or "UNKNOWN" in reason:
        return "HIGH_REVIEW_UNKNOWN_COMPETITION"
    if "POSSIBLE_WHITELIST" in bucket:
        return "MEDIUM_REVIEW_POSSIBLE_WHITELIST"
    return "MEDIUM_REVIEW_TRUST_EXPANSION"


def operator_note(row: dict[str, str]) -> str:
    return (
        "Review competition identity, country, fixture identity, repeated coverage, source reliability, "
        "and postmatch sample before any separate whitelist change. This row is review-only and cannot score, promote, create picks, or create stake."
    )


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    review_candidates = [row for row in load_audit_rows(processed, day) if include_for_manual_board(row)]
    out: list[dict[str, object]] = []

    for rank, row in enumerate(review_candidates, start=1):
        out.append({
            "target_date": day,
            "generated_at": generated,
            "review_rank": rank,
            "fixture_id": norm(row.get("fixture_id")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "fixture_datetime_utc": norm(row.get("fixture_datetime_utc")),
            "source_path": norm(row.get("source_path")),
            "audit_bucket": norm(row.get("audit_bucket")),
            "review_priority": norm(row.get("review_priority")),
            "trust_expansion_candidate": norm(row.get("trust_expansion_candidate")),
            "audit_reason": norm(row.get("audit_reason")),
            "suggested_action": norm(row.get("suggested_action")),
            "manual_review_status": "PENDING_OPERATOR_REVIEW" if review_candidates else "NO_ROWS",
            "manual_decision": "NO_DECISION_REVIEW_ONLY",
            "decision_required": "YES_SEPARATE_REVIEW_REQUIRED",
            "risk_label": risk_label(row),
            "whitelist_permission": "NO_WHITELIST_PERMISSION",
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "scoring_permission": "NO_SCORING_PERMISSION",
            "api_enrichment_permission": "NO_API_ENRICHMENT_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "operator_note": operator_note(row),
            "auto_apply": "NO",
            "production_change": "NO",
        })

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "review_rows": len(out),
        "p1_review_rows": sum(1 for row in out if row.get("review_priority") == "P1_REVIEW_CANDIDATE"),
        "p2_review_rows": sum(1 for row in out if str(row.get("review_priority", "")).startswith("P2")),
        "manual_review_status_counts": counts(out, "manual_review_status"),
        "manual_decision_counts": counts(out, "manual_decision"),
        "risk_label_counts": counts(out, "risk_label"),
        "whitelist_permission_counts": counts(out, "whitelist_permission"),
        "canonical_board_permission_counts": counts(out, "canonical_board_permission"),
        "scoring_permission_counts": counts(out, "scoring_permission"),
        "api_enrichment_permission_counts": counts(out, "api_enrichment_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "next_action": "Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Manual Whitelist Review Board - {day}",
        "",
        "## Summary",
        f"- review_rows: {summary['review_rows']}",
        f"- p1_review_rows: {summary['p1_review_rows']}",
        f"- p2_review_rows: {summary['p2_review_rows']}",
        f"- manual_review_status_counts: {summary['manual_review_status_counts']}",
        f"- manual_decision_counts: {summary['manual_decision_counts']}",
        f"- risk_label_counts: {summary['risk_label_counts']}",
        f"- whitelist_permission_counts: {summary['whitelist_permission_counts']}",
        f"- canonical_board_permission_counts: {summary['canonical_board_permission_counts']}",
        f"- scoring_permission_counts: {summary['scoring_permission_counts']}",
        f"- api_enrichment_permission_counts: {summary['api_enrichment_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Review Rows",
    ]
    if not rows:
        lines.append("- none. No P1 whitelist candidates were produced by rejected source block audit.")
    for row in rows[:80]:
        lines.append(
            f"- #{row['review_rank']} | {row['home_team']} vs {row['away_team']} | league={row['league']} | country={row['country']} | priority={row['review_priority']} | risk={row['risk_label']} | whitelist={row['whitelist_permission']} | canonical={row['canonical_board_permission']} | scoring={row['scoring_permission']} | pick={row['pick_permission']} | stake={row['stake_permission']} | reason={row['audit_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This board is manual-review only.",
        "- It does not whitelist sources, promote candidates, score fixtures, call APIs, create picks, or create stake permission.",
        "- Every row remains NO_WHITELIST_PERMISSION, NO_CANONICAL_BOARD_PERMISSION, NO_SCORING_PERMISSION, NO_API_ENRICHMENT_PERMISSION, NO_PICK_PERMISSION and NO_STAKE_PERMISSION.",
        "- Any future whitelist must be an explicit separate code change after sample validation.",
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
    section = "## Manual Whitelist Review Board"
    lines = [
        section,
        f"- review_rows: {summary.get('review_rows', 'UNKNOWN')}",
        f"- p1_review_rows: {summary.get('p1_review_rows', 'UNKNOWN')}",
        f"- p2_review_rows: {summary.get('p2_review_rows', 'UNKNOWN')}",
        f"- manual_review_status_counts: {summary.get('manual_review_status_counts', 'UNKNOWN')}",
        f"- risk_label_counts: {summary.get('risk_label_counts', 'UNKNOWN')}",
        f"- whitelist_permission_counts: {summary.get('whitelist_permission_counts', 'UNKNOWN')}",
        f"- canonical_board_permission_counts: {summary.get('canonical_board_permission_counts', 'UNKNOWN')}",
        f"- scoring_permission_counts: {summary.get('scoring_permission_counts', 'UNKNOWN')}",
        f"- api_enrichment_permission_counts: {summary.get('api_enrichment_permission_counts', 'UNKNOWN')}",
        f"- pick_permission_counts: {summary.get('pick_permission_counts', 'UNKNOWN')}",
        f"- stake_permission_counts: {summary.get('stake_permission_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            text = replace_or_append_section(text, section, block)
            md_path.write_text(text, encoding="utf-8")


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_manual_whitelist_review_board.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_manual_whitelist_review_board_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_manual_whitelist_review_board.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA MANUAL WHITELIST REVIEW BOARD ===")
    print(f"review_rows={summary[0]['review_rows']}")
    print(f"p1_review_rows={summary[0]['p1_review_rows']}")
    print(f"whitelist_permission_counts={summary[0]['whitelist_permission_counts']}")
    print(f"pick_permission_counts={summary[0]['pick_permission_counts']}")
    print(f"stake_permission_counts={summary[0]['stake_permission_counts']}")
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
