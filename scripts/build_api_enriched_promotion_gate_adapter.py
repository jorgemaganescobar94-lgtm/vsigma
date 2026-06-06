from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
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
    "promotion_input_status",
    "promotion_permission",
    "adapter_status",
    "adapter_reason",
    "allowed_downstream_use",
    "promotion_candidate_type",
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
    "adapter_rows_written",
    "adapter_promoted_review_only_rows",
    "adapter_blocked_rows",
    "adapter_status_counts",
    "allowed_downstream_use_counts",
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

def load_bridge(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_promotion_input_bridge.csv"])
    rows = read_csv(path) if path else []
    if path and path.parent.name == "governance" and rows and "target_date" in rows[0]:
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows

def classify(row: dict[str, str]) -> tuple[str, str, str]:
    status = norm(row.get("promotion_input_status"))
    permission = norm(row.get("promotion_permission"))
    signal_score = as_int(row.get("candidate_signal_score"))

    if status != "PROMOTION_INPUT_READY_REVIEW_ONLY":
        return (
            "ADAPTER_BLOCKED_NOT_READY",
            "Promotion input is not ready for review-only adapter.",
            "NO_DOWNSTREAM_USE",
        )

    if permission != "REVIEW_ONLY_PROMOTION_INPUT":
        return (
            "ADAPTER_BLOCKED_NO_REVIEW_PERMISSION",
            "Promotion input does not carry review-only permission.",
            "NO_DOWNSTREAM_USE",
        )

    if signal_score < 55:
        return (
            "ADAPTER_BLOCKED_WEAK_SIGNAL",
            "Signal score below review-only adapter threshold.",
            "NO_DOWNSTREAM_USE",
        )

    return (
        "API_ENRICHED_PROMOTION_REVIEW_READY",
        "API-enriched candidate may be reviewed by normal scoring/promotion gates; no pick permission.",
        "SCORING_REVIEW_ONLY_WITH_NORMAL_GATES",
    )

def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source_rows = load_bridge(processed, day)

    rows: list[dict[str, object]] = []
    for row in source_rows:
        adapter_status, adapter_reason, downstream = classify(row)
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
            "candidate_signal_score": norm(row.get("candidate_signal_score")),
            "candidate_signal_band": norm(row.get("candidate_signal_band")),
            "market_signal_summary": norm(row.get("market_signal_summary")),
            "promotion_input_status": norm(row.get("promotion_input_status")),
            "promotion_permission": norm(row.get("promotion_permission")),
            "adapter_status": adapter_status,
            "adapter_reason": adapter_reason,
            "allowed_downstream_use": downstream,
            "promotion_candidate_type": "API_ENRICHED_REVIEW_ONLY",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "source_guard": "PROMOTION_GATE_ADAPTER_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    promoted = [row for row in rows if row["adapter_status"] == "API_ENRICHED_PROMOTION_REVIEW_READY"]
    blocked = [row for row in rows if row["adapter_status"] != "API_ENRICHED_PROMOTION_REVIEW_READY"]

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "source_rows_reviewed": len(source_rows),
        "adapter_rows_written": len(rows),
        "adapter_promoted_review_only_rows": len(promoted),
        "adapter_blocked_rows": len(blocked),
        "adapter_status_counts": counts(rows, "adapter_status"),
        "allowed_downstream_use_counts": counts(rows, "allowed_downstream_use"),
        "pick_permission_counts": counts(rows, "pick_permission"),
        "stake_permission_counts": counts(rows, "stake_permission"),
        "auto_apply": "NO",
        "production_change": "NO",
    }]

    return rows, promoted, summary, markdown(day, rows, summary[0])

def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API-Enriched Promotion Gate Adapter - {day}",
        "",
        "## Summary",
        f"- source_rows_reviewed: {summary['source_rows_reviewed']}",
        f"- adapter_rows_written: {summary['adapter_rows_written']}",
        f"- adapter_promoted_review_only_rows: {summary['adapter_promoted_review_only_rows']}",
        f"- adapter_blocked_rows: {summary['adapter_blocked_rows']}",
        f"- adapter_status_counts: {summary['adapter_status_counts']}",
        f"- allowed_downstream_use_counts: {summary['allowed_downstream_use_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Adapter Rows",
    ]

    if not rows:
        lines.append("- none")

    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | adapter={row['adapter_status']} | "
            f"allowed={row['allowed_downstream_use']} | score={row['candidate_signal_score']} | "
            f"summary={row['market_signal_summary']} | pick={row['pick_permission']} | stake={row['stake_permission']}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This adapter creates review-only promotion candidates, not picks.",
        "- It does not write to the canonical daily execution board.",
        "- It does not create stake permission, market recommendations, or execution permission.",
        "- Normal scoring, promotion, market translation, and operator gates remain mandatory.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]], promoted: list[dict[str, object]], summary: list[dict[str, object]], md: str) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_enriched_promotion_gate_adapter.csv", rows, FIELDS)
        write_csv(base / "vsigma_api_enriched_promotion_gate_adapter_summary.csv", summary, SUMMARY_FIELDS)
        write_csv(base / "vsigma_promoted_api_enriched_candidates.csv", promoted, FIELDS)
        (base / "vsigma_api_enriched_promotion_gate_adapter.md").write_text(md, encoding="utf-8")

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, promoted, summary, md = build(day, tz, processed)
    write_outputs(processed, day, rows, promoted, summary, md)
    s = summary[0]
    print("=== VSIGMA API-ENRICHED PROMOTION GATE ADAPTER ===")
    print(f"adapter_rows_written={s['adapter_rows_written']}")
    print(f"adapter_promoted_review_only_rows={s['adapter_promoted_review_only_rows']}")
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
