from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_PROCESSED_DIR = Path("data/processed")
OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "close_rank",
    "issue_type",
    "severity",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "field_name",
    "current_value",
    "close_state",
    "close_reason",
    "next_action",
    "source_file",
    "auto_fix",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class EvidenceCloserPaths:
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


def blankish(value: object) -> bool:
    return upper(value) in {"", "UNKNOWN", "UNRESOLVED", "NO_SIGNAL", "UNKNOWN_RISK", "UNKNOWN_MARKET", "PENDING"}


def make_row(target_date: str, generated_at: str, issue_type: str, severity: str, row: dict[str, str], field_name: str, close_state: str, reason: str, next_action: str, source: Path) -> dict[str, object]:
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "close_rank": 0,
        "issue_type": issue_type,
        "severity": severity,
        "fixture_id": norm(row.get("fixture_id")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_primary": upper(row.get("market_primary")) or "UNKNOWN",
        "field_name": field_name,
        "current_value": norm(row.get(field_name)) or "EMPTY",
        "close_state": close_state,
        "close_reason": reason,
        "next_action": next_action,
        "source_file": str(source),
        "auto_fix": "NO",
        "production_change": "NO",
        "guardrail_status": "EVIDENCE_CLOSER_REPORT_ONLY_NO_AUTO_WRITE",
    }


def duplicate_keys(rows: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        key = (norm(row.get("fixture_id")), upper(row.get("market_primary")), upper(row.get("result_status")))
        if key[0] and key[1]:
            counts[key] += 1
    return {key for key, count in counts.items() if count > 1}


def build_rows(target_date: str, generated_at: str, processed_dir: Path) -> list[dict[str, object]]:
    ledger_rows, ledger_path = first_rows(processed_dir, target_date, "vsigma_learning_ledger.csv")
    market_rows, market_path = first_rows(processed_dir, target_date, "vsigma_market_results_labeled.csv")
    execution_rows, execution_path = first_rows(processed_dir, target_date, "vsigma_today_execution_shortlist.csv")
    output: list[dict[str, object]] = []

    dupes = duplicate_keys(ledger_rows)
    for row in ledger_rows:
        fixture_id = norm(row.get("fixture_id"))
        market = upper(row.get("market_primary"))
        result_status = upper(row.get("result_status"))
        if not fixture_id or not market:
            output.append(make_row(target_date, generated_at, "MISSING_IDENTITY", "P2", row, "fixture_id", "NEEDS_SOURCE_IDENTITY", "Learning row is missing fixture_id or market_primary.", "REBUILD_FROM_EXECUTION_AND_RESULT_SOURCES", ledger_path))
        if result_status in {"", "UNKNOWN", "UNRESOLVED", "PENDING"}:
            output.append(make_row(target_date, generated_at, "OPEN_RESULT_STATUS", "P2", row, "result_status", "WAIT_POST_RESULT_LABELING", "Outcome cannot close until post-result labeling is available.", "RUN_POST_THEN_REBUILD_LEARNING", ledger_path))
        for field_name, issue in [("improvement_signal", "NO_SIGNAL"), ("accuracy_primary_risk", "UNKNOWN_RISK"), ("learning_family", "UNKNOWN_FAMILY")]:
            if blankish(row.get(field_name)):
                output.append(make_row(target_date, generated_at, issue, "P3", row, field_name, "ENRICH_AFTER_POST", f"{field_name} is empty or unresolved.", "REBUILD_LEARNING_AFTER_POST", ledger_path))
        if (fixture_id, market, result_status) in dupes:
            output.append(make_row(target_date, generated_at, "DUPLICATE_LEARNING_ROW", "P3", row, "sample_key", "DEDUP_REVIEW", "Multiple learning rows share fixture, market and result status.", "DEDUPLICATE_REBUILT_LEDGER", ledger_path))

    if not market_rows:
        blank = {"fixture_id": "", "market_primary": ""}
        output.append(make_row(target_date, generated_at, "MISSING_RESULT_FILE", "P2", blank, "result_status", "WAIT_POST_RESULT_LABELING", "No dated market result file exists yet.", "RUN_POST_RESULTS_PIPELINE", market_path))

    for row in execution_rows:
        if upper(row.get("final_recommendation")) == "BET" and upper(row.get("lineup_activation_state")) == "INACTIVE":
            output.append(make_row(target_date, generated_at, "PRELOCK_OPEN_ITEM", "P2", row, "lineup_activation_state", "WAIT_PRELOCK", "BET row still needs prelock/lineup timing confirmation.", "RUN_PRELOCK_IN_WINDOW", execution_path))

    seen: set[tuple[str, str, str, str, str]] = set()
    deduped: list[dict[str, object]] = []
    for row in output:
        key = (str(row["issue_type"]), str(row["fixture_id"]), str(row["market_primary"]), str(row["field_name"]), str(row["source_file"]))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    severity_rank = {"P1": 0, "P2": 1, "P3": 2}
    deduped.sort(key=lambda item: (severity_rank.get(str(item["severity"]), 9), str(item["issue_type"]), str(item["fixture_id"]), str(item["field_name"])))
    for idx, row in enumerate(deduped, start=1):
        row["close_rank"] = idx
    return deduped


def executive_status(rows: list[dict[str, object]]) -> str:
    issues = {str(row.get("issue_type")) for row in rows}
    if "MISSING_RESULT_FILE" in issues or "OPEN_RESULT_STATUS" in issues:
        return "POST_RESULT_LABELING_REQUIRED"
    if "MISSING_IDENTITY" in issues:
        return "IDENTITY_REPAIR_REQUIRED"
    if rows:
        return "EVIDENCE_ENRICHMENT_REQUIRED"
    return "EVIDENCE_CLOSED"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Learning Evidence Closer - {target_date}",
        "",
        "## Executive Evidence Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- close_items: {len(rows)}",
        f"- severity_counts: {fmt_counter(counter(rows, 'severity'))}",
        f"- issue_counts: {fmt_counter(counter(rows, 'issue_type'))}",
        "- auto_fix: NO",
        "- production_change: NO",
        "",
        "## Close Plan",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:60]:
            lines.append(
                f"- #{row['close_rank']} | {row['severity']} | {row['issue_type']} | fixture={row['fixture_id'] or 'N/A'} | "
                f"market={row['market_primary']} | field={row['field_name']} | state={row['close_state']} | next={row['next_action']} | reason={row['close_reason']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- No ledger rows are changed by this report.",
        "- No production behavior is changed.",
        "- Safe closing requires POST first, then learning rebuild, then readiness review.",
    ])
    return "\n".join(lines)


def build_learning_evidence_closer(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], EvidenceCloserPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_rows(target_date, generated_at, processed_dir)
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = EvidenceCloserPaths(
        today_csv=today / "vsigma_learning_evidence_closer.csv",
        today_md=today / "vsigma_learning_evidence_closer.md",
        governance_csv=governance / "vsigma_learning_evidence_closer.csv",
        governance_md=governance / "vsigma_learning_evidence_closer.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA learning evidence closer report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_learning_evidence_closer(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA LEARNING EVIDENCE CLOSER ===")
    print(f"close_items={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
