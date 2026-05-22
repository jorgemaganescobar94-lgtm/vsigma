from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_PROCESSED_DIR = Path("data/processed")
OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "cleaner_rank",
    "source_issue_type",
    "severity",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "source_file",
    "field_to_clean",
    "current_value",
    "cleaner_action",
    "recommended_command",
    "auto_fix",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class EvidenceCleanerPaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except Exception:
        return []


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in OUTPUT_COLUMNS})


def first_rows(processed_dir: Path, target_date: str, filename: str) -> tuple[list[dict[str, str]], Path]:
    today = processed_dir / "today" / target_date / filename
    governance = processed_dir / "governance" / filename
    rows = read_csv_rows(today)
    if rows:
        return rows, today
    return read_csv_rows(governance), governance


def unknown(value: object) -> bool:
    return upper(value) in {"", "UNKNOWN", "UNRESOLVED", "NO_SIGNAL", "UNKNOWN_RISK", "UNKNOWN_MARKET", "PENDING"}


def command_for(action: str, target_date: str) -> str:
    if action == "POST_RESULT_LABELING":
        return f".\\.venv\\Scripts\\python.exe scripts\\run_daily_competition_controller.py --date {target_date} --timezone Atlantic/Canary --mode post"
    if action == "PRELOCK_REBUILD":
        return f".\\.venv\\Scripts\\python.exe scripts\\run_daily_competition_controller.py --date {target_date} --timezone Atlantic/Canary --mode prelock --window-minutes 90"
    if action == "REBUILD_LEARNING":
        return f".\\.venv\\Scripts\\python.exe scripts\\build_learning_ledger.py --date {target_date} --timezone Atlantic/Canary"
    return "manual_review_required"


def make_row(target_date: str, generated_at: str, issue_type: str, severity: str, source_file: Path, row: dict[str, str], field: str, action: str) -> dict[str, object]:
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "cleaner_rank": 0,
        "source_issue_type": issue_type,
        "severity": severity,
        "fixture_id": norm(row.get("fixture_id")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_primary": upper(row.get("market_primary")) or "UNKNOWN",
        "source_file": str(source_file),
        "field_to_clean": field,
        "current_value": norm(row.get(field)) or "EMPTY",
        "cleaner_action": action,
        "recommended_command": command_for(action, target_date),
        "auto_fix": "NO",
        "production_change": "NO",
        "guardrail_status": "EVIDENCE_CLEANER_PLAN_ONLY_NO_AUTO_CHANGE",
    }


def build_rows(target_date: str, generated_at: str, processed_dir: Path) -> list[dict[str, object]]:
    dq_rows, _ = first_rows(processed_dir, target_date, "vsigma_data_quality_governor.csv")
    ledger_rows, ledger_path = first_rows(processed_dir, target_date, "vsigma_learning_ledger.csv")
    market_rows, market_path = first_rows(processed_dir, target_date, "vsigma_market_results_labeled.csv")
    execution_rows, execution_path = first_rows(processed_dir, target_date, "vsigma_today_execution_shortlist.csv")

    active_issue_types = {upper(row.get("issue_type")) for row in dq_rows}
    rows: list[dict[str, object]] = []

    if "UNRESOLVED_LEDGER_ROWS" in active_issue_types or "UNRESOLVED_RESULTS" in active_issue_types:
        for row in ledger_rows:
            if upper(row.get("result_status")) in {"", "UNKNOWN", "UNRESOLVED"}:
                rows.append(make_row(target_date, generated_at, "UNRESOLVED_LEDGER_ROWS", "P2", ledger_path, row, "result_status", "POST_RESULT_LABELING"))

    if "PENDING_MARKET_RESULTS" in active_issue_types:
        for row in market_rows:
            if upper(row.get("primary_result")) in {"", "PENDING"}:
                rows.append(make_row(target_date, generated_at, "PENDING_MARKET_RESULTS", "P2", market_path, row, "primary_result", "POST_RESULT_LABELING"))
            if upper(row.get("actionable_result")) in {"", "PENDING"}:
                rows.append(make_row(target_date, generated_at, "PENDING_MARKET_RESULTS", "P2", market_path, row, "actionable_result", "POST_RESULT_LABELING"))

    if "UNKNOWN_MARKET" in active_issue_types:
        for row in ledger_rows:
            if unknown(row.get("market_primary")):
                rows.append(make_row(target_date, generated_at, "UNKNOWN_MARKET", "P3", ledger_path, row, "market_primary", "REBUILD_LEARNING"))

    if "UNKNOWN_RISK" in active_issue_types or "DATA_QUALITY_BLOCKER" in active_issue_types:
        for row in ledger_rows:
            if unknown(row.get("accuracy_primary_risk")):
                rows.append(make_row(target_date, generated_at, "UNKNOWN_RISK", "P3", ledger_path, row, "accuracy_primary_risk", "REBUILD_LEARNING"))

    if "NO_SIGNAL" in active_issue_types:
        for row in ledger_rows:
            if unknown(row.get("improvement_signal")):
                rows.append(make_row(target_date, generated_at, "NO_SIGNAL", "P3", ledger_path, row, "improvement_signal", "REBUILD_LEARNING"))

    for row in execution_rows:
        if upper(row.get("lineup_activation_state")) == "INACTIVE" and upper(row.get("final_recommendation")) == "BET":
            rows.append(make_row(target_date, generated_at, "PRELOCK_CONFIRMATION_REQUIRED", "P2", execution_path, row, "lineup_activation_state", "PRELOCK_REBUILD"))

    seen = set()
    deduped: list[dict[str, object]] = []
    for row in rows:
        key = (row["source_file"], row["fixture_id"], row["market_primary"], row["field_to_clean"], row["cleaner_action"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    rank = {"P1": 0, "P2": 1, "P3": 2}
    deduped.sort(key=lambda row: (rank.get(str(row["severity"]), 9), str(row["source_issue_type"]), str(row["fixture_id"]), str(row["field_to_clean"])))
    for idx, row in enumerate(deduped, start=1):
        row["cleaner_rank"] = idx
    return deduped


def executive_status(rows: list[dict[str, object]]) -> str:
    if any(row.get("severity") == "P1" for row in rows):
        return "P1_EVIDENCE_CLEANING_REQUIRED"
    if any(row.get("severity") == "P2" for row in rows):
        return "P2_EVIDENCE_CLEANING_REQUIRED"
    if rows:
        return "P3_EVIDENCE_CLEANING_RECOMMENDED"
    return "EVIDENCE_CLEAN"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Evidence Cleaner - {target_date}",
        "",
        "## Executive Cleaner Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- cleaner_actions: {len(rows)}",
        f"- severity_counts: {fmt_counter(counter(rows, 'severity'))}",
        f"- action_counts: {fmt_counter(counter(rows, 'cleaner_action'))}",
        f"- source_issue_counts: {fmt_counter(counter(rows, 'source_issue_type'))}",
        "- auto_fix: NO",
        "- production_change: NO",
        "",
        "## Prioritized Cleaning Plan",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:40]:
            lines.append(
                f"- #{row['cleaner_rank']} | {row['severity']} | {row['source_issue_type']} | "
                f"fixture={row['fixture_id'] or 'N/A'} | market={row['market_primary']} | "
                f"field={row['field_to_clean']} | action={row['cleaner_action']} | command=`{row['recommended_command']}`"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- No auto-fix is applied.",
        "- No production model behavior is changed.",
        "- This report only tells the operator or next automation what should be cleaned first.",
    ])
    return "\n".join(lines)


def build_evidence_cleaner(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], EvidenceCleanerPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_rows(target_date, generated_at, processed_dir)

    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = EvidenceCleanerPaths(
        today_csv=today / "vsigma_evidence_cleaner.csv",
        today_md=today / "vsigma_evidence_cleaner.md",
        governance_csv=governance / "vsigma_evidence_cleaner.csv",
        governance_md=governance / "vsigma_evidence_cleaner.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA evidence cleaner plan.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_evidence_cleaner(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA EVIDENCE CLEANER ===")
    print(f"cleaner_actions={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
