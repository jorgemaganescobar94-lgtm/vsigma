from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league",
    "promotion_status", "gap_status", "gap_stage", "scored_row_found", "scored_row_status",
    "gap_reason", "recommended_fix", "allowed_downstream_use", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "missing_scored_rows", "no_data_blocked_rows",
    "not_trusted_rows", "promoted_rows", "gap_status_counts", "next_action", "auto_apply", "production_change",
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
    return [row for row in rows if row_day(row) in {"", day}]


def scored_index(processed: Path, day: str) -> dict[str, dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in [processed / "today" / day / "matches_vsigma_scored_v3.csv", processed / "matches_vsigma_scored_v3.csv"]:
        rows.extend(same_day(read_rows(path), day))
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = fixture_id(row)
        if fid and fid not in out:
            out[fid] = row
    return out


def scored_status(row: dict[str, str] | None) -> str:
    if not row:
        return "MISSING"
    text = " ".join(up(value) for value in row.values())
    if "NO_DATA_BLOCKED" in text:
        return "NO_DATA_BLOCKED"
    if "LOW_COVERAGE_NO_BET" in text:
        return "LOW_COVERAGE_NO_BET"
    if any(token in text for token in ["NO_BET", "NO_STAKE", "BLOCKED"]):
        return "BLOCKED"
    return "SCORED_AVAILABLE"


def classify(row: dict[str, str], scored: dict[str, dict[str, str]]) -> tuple[str, str, str, str, str, str]:
    status = up(row.get("promotion_status"))
    fid = fixture_id(row)
    scored_row = scored.get(fid)
    s_status = scored_status(scored_row)
    if status == "TRUSTED_SOURCE_BUT_NO_SCORED_ROW":
        return (
            "MISSING_SCORED_ROW",
            "SCORING_NOT_RUN_FOR_TRUSTED_RAW",
            "false",
            s_status,
            "trusted raw candidate has no matching scored row",
            "Run/repair scoring enrichment over trusted raw fixture candidates before market translation.",
        )
    if status == "TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED":
        return (
            "SCORED_ROW_NO_DATA_BLOCKED",
            "SCORING_ENRICHMENT_BLOCKED",
            "true",
            s_status,
            "matching scored row exists but is NO_DATA_BLOCKED",
            "Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.",
        )
    if status == "PROMOTED_TO_SCORING_INPUT":
        return (
            "PROMOTED",
            "SCORING_ALLOWED",
            "true" if scored_row else "false",
            s_status,
            "raw candidate was promoted to normal scoring flow",
            "Proceed through normal scoring, translator, board and prelock gates.",
        )
    if status == "NOT_TRUSTED_NO_PROMOTION":
        return (
            "NOT_TRUSTED_SKIPPED",
            "RAW_TRUST_GATE_BLOCK",
            "true" if scored_row else "false",
            s_status,
            "raw candidate was not trusted, so scoring gap is intentionally ignored",
            "Keep diagnostic only unless future whitelist changes source trust.",
        )
    return (
        "UNKNOWN_PROMOTION_STATE",
        "PROMOTION_GATE_UNKNOWN",
        "true" if scored_row else "false",
        s_status,
        "promotion gate state not recognized",
        "Inspect promotion gate output manually.",
    )


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    promotion_rows = same_day(read_rows(processed / "today" / day / "vsigma_trusted_raw_candidate_promotion_gate.csv"), day)
    scored = scored_index(processed, day)
    out: list[dict[str, object]] = []
    for row in promotion_rows:
        gap_status, gap_stage, found, s_status, reason, fix = classify(row, scored)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": fixture_id(row),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "promotion_status": up(row.get("promotion_status")),
            "gap_status": gap_status,
            "gap_stage": gap_stage,
            "scored_row_found": found,
            "scored_row_status": s_status,
            "gap_reason": reason,
            "recommended_fix": fix,
            "allowed_downstream_use": norm(row.get("allowed_downstream_use")),
            "auto_apply": "NO",
            "production_change": "NO",
        })
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(out),
        "missing_scored_rows": sum(1 for row in out if row["gap_status"] == "MISSING_SCORED_ROW"),
        "no_data_blocked_rows": sum(1 for row in out if row["gap_status"] == "SCORED_ROW_NO_DATA_BLOCKED"),
        "not_trusted_rows": sum(1 for row in out if row["gap_status"] == "NOT_TRUSTED_SKIPPED"),
        "promoted_rows": sum(1 for row in out if row["gap_status"] == "PROMOTED"),
        "gap_status_counts": counts(out, "gap_status"),
        "next_action": "Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, md(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Scoring Gap Explainer - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- missing_scored_rows: {summary['missing_scored_rows']}",
        f"- no_data_blocked_rows: {summary['no_data_blocked_rows']}",
        f"- not_trusted_rows: {summary['not_trusted_rows']}",
        f"- promoted_rows: {summary['promoted_rows']}",
        f"- gap_status_counts: {summary['gap_status_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Gap Rows",
    ]
    if not rows:
        lines.append("- none. Promotion gate output missing or empty.")
    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | promotion={row['promotion_status']} | gap={row['gap_status']} | stage={row['gap_stage']} | scored={row['scored_row_status']} | fix={row['recommended_fix']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Scoring gap explainer is diagnostic only.",
        "- It does not call APIs, create picks, create stake permission, or bypass gates.",
        "- Missing scored rows must be repaired upstream before translator/board discussion.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_scoring_gap_explainer.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_scoring_gap_explainer_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_scoring_gap_explainer.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA SCORING GAP EXPLAINER ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"gap_status_counts={summary[0]['gap_status_counts']}")
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
