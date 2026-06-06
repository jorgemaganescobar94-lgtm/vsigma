from __future__ import annotations

import argparse
import csv
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
    "fixture_date_utc",
    "fixture_status",
    "candidate_signal_score",
    "candidate_signal_band",
    "market_signal_summary",
    "adapter_status",
    "allowed_downstream_use",
    "review_priority",
    "review_board_status",
    "review_reason",
    "manual_review_required",
    "canonical_board_permission",
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
    "review_rows_written",
    "ready_for_manual_review_rows",
    "blocked_rows",
    "review_priority_counts",
    "review_board_status_counts",
    "canonical_board_permission_counts",
    "pick_permission_counts",
    "stake_permission_counts",
    "auto_apply",
    "production_change",
]

def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default

def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0

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

def first_existing(processed: Path, day: str, names: list[str]) -> Path | None:
    for name in names:
        for path in [processed / "today" / day / name, processed / "governance" / name]:
            if path.exists():
                return path
    return None

def load_promoted(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_promoted_api_enriched_candidates.csv"])
    rows = read_csv(path) if path else []
    if path and path.parent.name == "governance" and rows and "target_date" in rows[0]:
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows

def priority(score: int, band: str) -> str:
    if score >= 75 or band == "HIGH_SIGNAL_REVIEW":
        return "P1_MANUAL_REVIEW"
    if score >= 55 or band == "MEDIUM_SIGNAL_REVIEW":
        return "P2_MANUAL_REVIEW"
    return "P3_WATCH_ONLY_REVIEW"

def classify(row: dict[str, str]) -> tuple[str, str, str]:
    adapter_status = norm(row.get("adapter_status"))
    allowed = norm(row.get("allowed_downstream_use"))

    if adapter_status != "API_ENRICHED_PROMOTION_REVIEW_READY":
        return (
            "BLOCKED_NOT_ADAPTER_READY",
            "Adapter did not mark this row as review-ready.",
            "NO_CANONICAL_BOARD_PERMISSION",
        )

    if allowed != "SCORING_REVIEW_ONLY_WITH_NORMAL_GATES":
        return (
            "BLOCKED_NO_SCORING_REVIEW_ROUTE",
            "Allowed downstream use is not review-only scoring with normal gates.",
            "NO_CANONICAL_BOARD_PERMISSION",
        )

    return (
        "API_ENRICHED_REVIEW_READY",
        "Candidate is ready for manual review panel only; canonical board remains blocked.",
        "NO_CANONICAL_BOARD_PERMISSION",
    )

def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source_rows = load_promoted(processed, day)

    rows: list[dict[str, object]] = []
    for row in source_rows:
        score = as_int(row.get("candidate_signal_score"))
        band = norm(row.get("candidate_signal_band"))
        board_status, reason, canonical_permission = classify(row)

        rows.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "fixture_date_utc": norm(row.get("fixture_date_utc")),
            "fixture_status": norm(row.get("fixture_status")),
            "candidate_signal_score": score,
            "candidate_signal_band": band,
            "market_signal_summary": norm(row.get("market_signal_summary")),
            "adapter_status": norm(row.get("adapter_status")),
            "allowed_downstream_use": norm(row.get("allowed_downstream_use")),
            "review_priority": priority(score, band),
            "review_board_status": board_status,
            "review_reason": reason,
            "manual_review_required": "YES",
            "canonical_board_permission": canonical_permission,
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "source_guard": "API_ENRICHED_REVIEW_BOARD_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    ready = [row for row in rows if row["review_board_status"] == "API_ENRICHED_REVIEW_READY"]
    blocked = [row for row in rows if row["review_board_status"] != "API_ENRICHED_REVIEW_READY"]

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "source_rows_reviewed": len(source_rows),
        "review_rows_written": len(rows),
        "ready_for_manual_review_rows": len(ready),
        "blocked_rows": len(blocked),
        "review_priority_counts": counts(rows, "review_priority"),
        "review_board_status_counts": counts(rows, "review_board_status"),
        "canonical_board_permission_counts": counts(rows, "canonical_board_permission"),
        "pick_permission_counts": counts(rows, "pick_permission"),
        "stake_permission_counts": counts(rows, "stake_permission"),
        "auto_apply": "NO",
        "production_change": "NO",
    }]

    return rows, summary, markdown(day, rows, summary[0])

def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API-Enriched Review Board - {day}",
        "",
        "## Summary",
        f"- source_rows_reviewed: {summary['source_rows_reviewed']}",
        f"- review_rows_written: {summary['review_rows_written']}",
        f"- ready_for_manual_review_rows: {summary['ready_for_manual_review_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- review_priority_counts: {summary['review_priority_counts']}",
        f"- review_board_status_counts: {summary['review_board_status_counts']}",
        f"- canonical_board_permission_counts: {summary['canonical_board_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Review Rows",
    ]

    if not rows:
        lines.append("- none")

    for row in rows[:120]:
        lines.append(
            f"- {row['review_priority']} | {row['home_team']} vs {row['away_team']} | "
            f"status={row['review_board_status']} | score={row['candidate_signal_score']} | "
            f"summary={row['market_signal_summary']} | canonical={row['canonical_board_permission']} | "
            f"pick={row['pick_permission']} | stake={row['stake_permission']}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This review board is separate from the canonical daily execution board.",
        "- It does not create picks, stake permission, market recommendations, or execution permission.",
        "- Manual review is mandatory before any future scoring/promotion integration.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]], summary: list[dict[str, object]], md: str) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_enriched_review_board.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_enriched_review_board_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_enriched_review_board.md").write_text(md, encoding="utf-8")

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    write_outputs(processed, day, rows, summary, md)
    s = summary[0]
    print("=== VSIGMA API-ENRICHED REVIEW BOARD ===")
    print(f"review_rows_written={s['review_rows_written']}")
    print(f"ready_for_manual_review_rows={s['ready_for_manual_review_rows']}")
    print(f"pick_permission_counts={s['pick_permission_counts']}")
    print(f"stake_permission_counts={s['stake_permission_counts']}")
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
