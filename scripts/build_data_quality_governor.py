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
    "quality_issue_id",
    "issue_type",
    "severity",
    "sample_count",
    "evidence_key",
    "affected_markets",
    "remediation_action",
    "next_engine",
    "blocks_model_change",
    "auto_fix",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class DataQualityGovernorPaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        return int(float(norm(value) or 0))
    except ValueError:
        return 0


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except Exception:
        return []


def read_rows(processed_dir: Path, target_date: str, filename: str) -> tuple[list[dict[str, str]], str]:
    today = processed_dir / "today" / target_date / filename
    governance = processed_dir / "governance" / filename
    rows = read_csv_rows(today)
    if rows:
        return rows, str(today)
    return read_csv_rows(governance), str(governance)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in OUTPUT_COLUMNS})


def severity(issue_type: str, n: int) -> str:
    if issue_type in {"DATA_QUALITY_BLOCKER", "UNRESOLVED_RESULTS"} and n >= 5:
        return "P1"
    if issue_type in {"UNKNOWN_MARKET", "UNKNOWN_RISK", "NO_SIGNAL"} and n >= 5:
        return "P1"
    if n >= 3:
        return "P2"
    return "P3"


def unique_markets(rows: list[dict[str, str]]) -> str:
    markets = sorted({upper(row.get("market_primary")) for row in rows if upper(row.get("market_primary"))})
    return ";".join(markets) if markets else "UNKNOWN"


def make_issue(target_date: str, generated_at: str, issue_type: str, key: str, rows: list[dict[str, str]], action: str, engine: str) -> dict[str, object]:
    n = max(1, len(rows))
    sev = severity(issue_type, n)
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "quality_issue_id": f"{issue_type}::{key}".replace(" ", "_"),
        "issue_type": issue_type,
        "severity": sev,
        "sample_count": n,
        "evidence_key": key,
        "affected_markets": unique_markets(rows),
        "remediation_action": action,
        "next_engine": engine,
        "blocks_model_change": "YES" if sev in {"P1", "P2"} else "REVIEW",
        "auto_fix": "NO",
        "production_change": "NO",
        "guardrail_status": "DATA_QUALITY_REVIEW_ONLY_NO_AUTO_CHANGE",
    }


def group_by(rows: list[dict[str, str]], key_name: str) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = upper(row.get(key_name)) or "UNKNOWN"
        groups[key].append(row)
    return dict(groups)


def quarantine_clears_model_change(processed_dir: Path, target_date: str) -> bool:
    rows, _ = read_rows(processed_dir, target_date, "vsigma_learning_residual_quarantine.csv")
    if not rows:
        return False
    usable = any(upper(row.get("counts_for_learning")) == "YES" for row in rows)
    blockers = any(upper(row.get("blocks_model_change")) == "YES" for row in rows)
    return usable and not blockers


def build_issues(processed_dir: Path, target_date: str, generated_at: str) -> list[dict[str, object]]:
    if quarantine_clears_model_change(processed_dir, target_date):
        return []

    governor, _ = read_rows(processed_dir, target_date, "vsigma_self_improvement_governor.csv")
    proposals, _ = read_rows(processed_dir, target_date, "vsigma_improvement_proposals.csv")
    ledger, _ = read_rows(processed_dir, target_date, "vsigma_learning_ledger.csv")
    market_results, _ = read_rows(processed_dir, target_date, "vsigma_market_results_labeled.csv")

    issues: list[dict[str, object]] = []

    dq_governor = [row for row in governor if upper(row.get("governor_decision")) == "DATA_QUALITY_FIRST"]
    for key, group in group_by(dq_governor, "source_key").items():
        issues.append(make_issue(target_date, generated_at, "DATA_QUALITY_BLOCKER", key, group, "Resolve this evidence blocker before model/shadow promotion.", "data_quality_review"))

    dq_proposals = [row for row in proposals if upper(row.get("proposal_type")) == "DATA_QUALITY_PROPOSAL"]
    for key, group in group_by(dq_proposals, "source_pattern_key").items():
        issue_type = "UNRESOLVED_RESULTS" if "UNRESOLVED" in key else "DATA_QUALITY_PROPOSAL"
        issues.append(make_issue(target_date, generated_at, issue_type, key, group, "Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.", "evidence_cleaner"))

    unresolved = [row for row in ledger if upper(row.get("result_status")) in {"", "UNKNOWN", "UNRESOLVED"}]
    if unresolved:
        issues.append(make_issue(target_date, generated_at, "UNRESOLVED_LEDGER_ROWS", "RESULT_STATUS_UNRESOLVED", unresolved, "Run/verify post-result labeling until learning rows close.", "post_result_labeling"))

    for token, action in {
        "UNKNOWN_MARKET": "Normalize missing market_primary before pattern mining.",
        "UNKNOWN_RISK": "Populate accuracy_primary_risk before pattern mining.",
        "NO_SIGNAL": "Populate improvement_signal or classify as monitor-only.",
    }.items():
        matched = [row for row in ledger if token in "::".join([upper(row.get("sample_key")), upper(row.get("market_primary")), upper(row.get("accuracy_primary_risk")), upper(row.get("improvement_signal"))])]
        if matched:
            issues.append(make_issue(target_date, generated_at, token, token, matched, action, "learning_ledger_enrichment"))

    pending = [row for row in market_results if upper(row.get("primary_result")) in {"", "PENDING"} or upper(row.get("actionable_result")) in {"", "PENDING"}]
    if pending:
        issues.append(make_issue(target_date, generated_at, "PENDING_MARKET_RESULTS", "MARKET_RESULTS_PENDING", pending, "Refresh finished fixtures and relabel market results.", "market_result_labeler"))

    seen = set()
    deduped = []
    for issue in issues:
        key = str(issue["quality_issue_id"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(issue)
    rank = {"P1": 0, "P2": 1, "P3": 2}
    return sorted(deduped, key=lambda row: (rank.get(str(row["severity"]), 9), -as_int(row["sample_count"]), str(row["quality_issue_id"])))


def executive_status(rows: list[dict[str, object]]) -> str:
    if any(row.get("blocks_model_change") == "YES" for row in rows):
        return "DATA_QUALITY_BLOCKS_MODEL_CHANGE"
    if rows:
        return "DATA_QUALITY_REVIEW_REQUIRED"
    return "DATA_QUALITY_CLEAR"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Data Quality Governor - {target_date}",
        "",
        "## Executive Data Quality Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- issues: {len(rows)}",
        f"- severity_counts: {fmt_counter(counter(rows, 'severity'))}",
        f"- issue_type_counts: {fmt_counter(counter(rows, 'issue_type'))}",
        "- auto_fix: NO",
        "- production_change: NO",
        "",
        "## Prioritized Issues",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:30]:
            lines.append(f"- {row['severity']} | {row['issue_type']} | n={row['sample_count']} | key={row['evidence_key']} | action={row['remediation_action']}")
    lines.extend([
        "",
        "## Guardrails",
        "- Model changes applied: NO",
        "- Shadow promotions applied: NO",
        "- Production changes applied: NO",
        "- Auto-fix applied: NO",
        "- P1/P2 data-quality issues block promotion and threshold/calibration changes until resolved.",
    ])
    return "\n".join(lines)


def build_data_quality_governor(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], DataQualityGovernorPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_issues(processed_dir, target_date, generated_at)
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = DataQualityGovernorPaths(
        today_csv=today / "vsigma_data_quality_governor.csv",
        today_md=today / "vsigma_data_quality_governor.md",
        governance_csv=governance / "vsigma_data_quality_governor.csv",
        governance_md=governance / "vsigma_data_quality_governor.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA data quality governor report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_data_quality_governor(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA DATA QUALITY GOVERNOR ===")
    print(f"issues={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
