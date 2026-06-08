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
    "home_team", "away_team", "fixture_datetime_utc", "review_status", "review_priority",
    "candidate_signal_score", "candidate_signal_band", "allowed_downstream_use",
    "inspector_bucket", "risk_label", "inspector_reason", "suggested_next_action",
    "canonical_board_permission", "pick_permission", "stake_permission",
    "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "review_rows", "bucket_counts", "risk_label_counts",
    "canonical_board_permission_counts", "pick_permission_counts", "stake_permission_counts",
    "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0


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


def load_review_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_enriched_review_board.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_enriched_review_board.csv")
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{k}={v}" for k, v in counter.most_common()) if counter else "none"


def row_text_blob(row: dict[str, str]) -> str:
    return " | ".join(
        norm(v) for k, v in row.items()
        if k not in {"generated_at", "target_date"}
    ).upper()


def candidate_score(row: dict[str, str]) -> int:
    return as_int(
        row.get("candidate_signal_score")
        or row.get("score")
        or row.get("review_score")
        or row.get("composite_score")
    )


def candidate_band(row: dict[str, str]) -> str:
    return norm(row.get("candidate_signal_band") or row.get("review_signal_band") or row.get("signal_band"))


def downstream_use(row: dict[str, str]) -> str:
    return norm(row.get("allowed_downstream_use") or row.get("downstream_use"))


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    text = row_text_blob(row)
    priority = up(row.get("review_priority"))
    score = candidate_score(row)
    band = up(candidate_band(row))
    downstream = up(downstream_use(row))

    if any(token in text for token in [
        "LOW_TRUST", "REJECTED_SOURCE_BLOCK", "UNKNOWN_COMPETITION",
        "LOW_MODEL_COVERAGE", "RESERVE", "ACADEMY", "YOUTH",
    ]):
        return (
            "BLOCKED_LOW_TRUST",
            "HIGH",
            "Source/trust pattern still looks low-trust or unsupported. Keep review-only.",
        )

    if any(token in text for token in [
        "BAD OR INCOMPLETE LINEUPS", "INSUFFICIENT_CONTEXT", "NO_CLEAR_STAT_MARKET",
    ]):
        return (
            "BLOCKED_INSUFFICIENT_CONTEXT",
            "HIGH",
            "Context/lineup/stat information is incomplete. Keep blocked.",
        )

    if "SCORING_REVIEW_ONLY" not in downstream:
        return (
            "BLOCKED_INSUFFICIENT_CONTEXT",
            "HIGH",
            "API row is not explicitly marked as scoring-review-only downstream use. Keep blocked.",
        )

    if priority.startswith("P1") and (score >= 85 or "HIGH_SIGNAL" in band):
        return (
            "P1_REVIEW_STRONG_SIGNAL",
            "MEDIUM",
            "Strong API-enriched review signal. Human review may inspect first, but no promotion is allowed.",
        )

    if (priority.startswith("P1") and score >= 70) or (priority.startswith("P2") and score >= 80):
        return (
            "P2_REVIEW_MEDIUM_SIGNAL",
            "MEDIUM",
            "Decent API-enriched review signal, but not strong enough for any promotion.",
        )

    if score >= 55 or "MEDIUM_SIGNAL" in band:
        return (
            "P3_REVIEW_LOW_SIGNAL",
            "LOW",
            "Low/medium review signal. Keep as low-priority manual inspection only.",
        )

    return (
        "BLOCKED_INSUFFICIENT_CONTEXT",
        "HIGH",
        "Review row exists but does not have enough strength/context for useful manual triage.",
    )


def suggested_next_action(bucket: str) -> str:
    if bucket == "P1_REVIEW_STRONG_SIGNAL":
        return "Inspect manually first: verify source quality, competition quality, lineup context, and postmatch repeatability. No promotion."
    if bucket == "P2_REVIEW_MEDIUM_SIGNAL":
        return "Secondary manual review only. Do not promote or score from this row."
    if bucket == "P3_REVIEW_LOW_SIGNAL":
        return "Low-priority manual review. No operational change."
    if bucket == "BLOCKED_LOW_TRUST":
        return "Keep blocked. Do not promote, score, pick, or stake."
    return "Keep blocked due to insufficient context. No operational change."


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source_rows = load_review_rows(processed, day)

    out: list[dict[str, object]] = []
    for rank, row in enumerate(source_rows, start=1):
        bucket, risk, reason = classify(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "review_rank": rank,
            "fixture_id": norm(row.get("fixture_id")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "fixture_datetime_utc": norm(row.get("fixture_datetime_utc") or row.get("fixture_date_utc")),
            "review_status": norm(row.get("review_status") or row.get("review_board_status") or row.get("status") or "API_ENRICHED_REVIEW_READY"),
            "review_priority": norm(row.get("review_priority") or row.get("review_bucket")),
            "candidate_signal_score": candidate_score(row),
            "candidate_signal_band": candidate_band(row),
            "allowed_downstream_use": downstream_use(row),
            "inspector_bucket": bucket,
            "risk_label": risk,
            "inspector_reason": reason,
            "suggested_next_action": suggested_next_action(bucket),
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "review_rows": len(out),
        "bucket_counts": counts(out, "inspector_bucket"),
        "risk_label_counts": counts(out, "risk_label"),
        "canonical_board_permission_counts": counts(out, "canonical_board_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "next_action": "Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API-Enriched Manual Review Inspector - {day}",
        "",
        "## Summary",
        f"- review_rows: {summary['review_rows']}",
        f"- bucket_counts: {summary['bucket_counts']}",
        f"- risk_label_counts: {summary['risk_label_counts']}",
        f"- canonical_board_permission_counts: {summary['canonical_board_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Inspector Rows",
    ]
    if not rows:
        lines.append("- none. No API-enriched review rows available.")
    for row in rows[:120]:
        lines.append(
            f"- #{row['review_rank']} | {row['home_team']} vs {row['away_team']} | "
            f"priority={row['review_priority']} | signal_score={row['candidate_signal_score']} | "
            f"signal_band={row['candidate_signal_band']} | bucket={row['inspector_bucket']} | risk={row['risk_label']} | "
            f"pick={row['pick_permission']} | stake={row['stake_permission']} | "
            f"reason={row['inspector_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This inspector is triage-only.",
        "- It does not promote to canonical board.",
        "- It does not create picks or stake permission.",
        "- All rows remain NO_CANONICAL_BOARD_PERMISSION, NO_PICK_PERMISSION, NO_STAKE_PERMISSION.",
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
    section = "## API-Enriched Manual Review Inspector"
    lines = [
        section,
        f"- review_rows: {summary.get('review_rows', 'UNKNOWN')}",
        f"- bucket_counts: {summary.get('bucket_counts', 'UNKNOWN')}",
        f"- risk_label_counts: {summary.get('risk_label_counts', 'UNKNOWN')}",
        f"- canonical_board_permission_counts: {summary.get('canonical_board_permission_counts', 'UNKNOWN')}",
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
        write_csv(base / "vsigma_api_enriched_manual_review_inspector.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_enriched_manual_review_inspector_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_enriched_manual_review_inspector.md").write_text(md, encoding="utf-8")

    append_panel(processed, day, summary[0])

    print("=== VSIGMA API-ENRICHED MANUAL REVIEW INSPECTOR ===")
    print(f"review_rows={summary[0]['review_rows']}")
    print(f"bucket_counts={summary[0]['bucket_counts']}")
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
