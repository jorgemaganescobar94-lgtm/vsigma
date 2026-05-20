from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
PROPOSAL_COLUMNS = [
    "target_date",
    "generated_at",
    "proposal_id",
    "source_pattern_id",
    "source_pattern_type",
    "source_pattern_key",
    "proposal_type",
    "proposal_status",
    "auto_apply",
    "risk_class",
    "priority",
    "sample_count",
    "evidence_summary",
    "recommended_action",
    "next_engine",
    "guardrail_status",
]

OPERATIONAL_TYPES = {"WAITING_PRELOCK_CLUSTER", "EXPIRED_PRELOCK_CLUSTER"}
DATA_TYPES = {"DATA_BLOCKED_CLUSTER", "UNRESOLVED_DOMINANCE", "TECHNICAL_REVIEW_CLUSTER"}
MODEL_SHADOW_TYPES = {"MARKET_RISK_CLUSTER", "SAMPLE_KEY_CLUSTER", "ACTIONABLE_LOSS_CLUSTER"}
QUALITY_TOKENS = {"UNKNOWN_MARKET", "UNKNOWN_RISK", "UNRESOLVED", "NO_SIGNAL"}


@dataclass(frozen=True)
class ImprovementProposalPaths:
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
        writer = csv.DictWriter(handle, fieldnames=PROPOSAL_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in PROPOSAL_COLUMNS})


def has_quality_gap(pattern_key: str) -> bool:
    key = upper(pattern_key)
    return any(token in key for token in QUALITY_TOKENS)


def proposal_type_for(pattern_type: str, pattern_key: str = "") -> tuple[str, str, str]:
    if has_quality_gap(pattern_key):
        return "DATA_QUALITY_PROPOSAL", "data_quality", "data_quality_review"
    if pattern_type in OPERATIONAL_TYPES:
        return "OPERATIONAL_PROPOSAL", "operational", "operator_review"
    if pattern_type in DATA_TYPES:
        return "DATA_QUALITY_PROPOSAL", "data_quality", "data_quality_review"
    if pattern_type in MODEL_SHADOW_TYPES:
        return "MODEL_SHADOW_PROPOSAL", "predictive_shadow", "shadow_experiment_engine"
    return "MONITORING_PROPOSAL", "monitoring", "pattern_miner"


def status_for(pattern_type: str, severity: str, sample_count: int, proposal_type: str = "") -> str:
    if proposal_type == "DATA_QUALITY_PROPOSAL":
        return "PROPOSAL_ONLY"
    if pattern_type == "ACTIONABLE_LOSS_CLUSTER" and sample_count >= 3:
        return "SHADOW_CANDIDATE_REQUIRED"
    if pattern_type in MODEL_SHADOW_TYPES and severity in {"P1", "P2"} and sample_count >= 3:
        return "SHADOW_CANDIDATE_REQUIRED"
    if pattern_type in OPERATIONAL_TYPES and severity in {"P1", "P2"}:
        return "PROPOSAL_ONLY"
    if pattern_type in DATA_TYPES:
        return "PROPOSAL_ONLY"
    return "MONITOR_ONLY"


def recommended_action_for(pattern: dict[str, str], proposal_type: str, status: str) -> str:
    pattern_type = upper(pattern.get("pattern_type"))
    key = norm(pattern.get("pattern_key"))
    if has_quality_gap(key):
        return "Resolve UNKNOWN/UNRESOLVED/NO_SIGNAL evidence quality before creating any model shadow candidate."
    if proposal_type == "OPERATIONAL_PROPOSAL":
        if pattern_type == "WAITING_PRELOCK_CLUSTER":
            return "Review AUTO/PRELOCK schedule, retry windows, and whether candidates remain waiting too close to kickoff."
        if pattern_type == "EXPIRED_PRELOCK_CLUSTER":
            return "Review execution timing and exclude expired rows from predictive hit-rate metrics."
    if proposal_type == "DATA_QUALITY_PROPOSAL":
        if pattern_type == "UNRESOLVED_DOMINANCE":
            return "Improve post-results labeling coverage before approving model changes."
        if pattern_type == "DATA_BLOCKED_CLUSTER":
            return "Inspect provider coverage, odds, lineup, availability, and freshness gaps."
        if pattern_type == "TECHNICAL_REVIEW_CLUSTER":
            return "Inspect workflow/reporting health and technical-review rows."
    if proposal_type == "MODEL_SHADOW_PROPOSAL":
        return f"Create a shadow-only candidate for pattern {key}; do not change production until backtest/forward-test promotion gates pass."
    if status == "MONITOR_ONLY":
        return "Continue collecting samples until evidence clears proposal thresholds."
    return "Review pattern evidence; no automatic production change allowed."


def priority_for(severity: str, proposal_status: str, proposal_type: str = "") -> str:
    if proposal_type == "DATA_QUALITY_PROPOSAL" and severity in {"P1", "P2"}:
        return severity
    if proposal_status == "SHADOW_CANDIDATE_REQUIRED" and severity in {"P1", "P2"}:
        return "P1"
    if severity == "P1":
        return "P1"
    if severity == "P2":
        return "P2"
    return "P3"


def build_proposal(pattern: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    pattern_type = upper(pattern.get("pattern_type"))
    pattern_key = norm(pattern.get("pattern_key"))
    severity = upper(pattern.get("severity")) or "P3"
    sample_count = int(float(norm(pattern.get("sample_count")) or 0))
    proposal_type, risk_class, next_engine = proposal_type_for(pattern_type, pattern_key)
    proposal_status = status_for(pattern_type, severity, sample_count, proposal_type)
    priority = priority_for(severity, proposal_status, proposal_type)
    proposal_id = f"{proposal_type}::{pattern_type}::{pattern_key}".replace(" ", "_")
    evidence_summary = (
        f"pattern={pattern_type}; key={pattern_key}; "
        f"severity={severity}; n={sample_count}; wins={norm(pattern.get('wins'))}; "
        f"losses={norm(pattern.get('losses'))}; unresolved={norm(pattern.get('unresolved'))}; "
        f"markets={norm(pattern.get('markets'))}"
    )
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "proposal_id": proposal_id,
        "source_pattern_id": norm(pattern.get("pattern_id")),
        "source_pattern_type": pattern_type,
        "source_pattern_key": pattern_key,
        "proposal_type": proposal_type,
        "proposal_status": proposal_status,
        "auto_apply": "NO",
        "risk_class": risk_class,
        "priority": priority,
        "sample_count": sample_count,
        "evidence_summary": evidence_summary,
        "recommended_action": recommended_action_for(pattern, proposal_type, proposal_status),
        "next_engine": next_engine,
        "guardrail_status": "PROPOSAL_ONLY_NO_MODEL_CHANGE",
    }


def dedupe_proposals(proposals: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    deduped: list[dict[str, object]] = []
    for proposal in proposals:
        key = str(proposal.get("proposal_id"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(proposal)
    priority_rank = {"P1": 0, "P2": 1, "P3": 2}
    status_rank = {"SHADOW_CANDIDATE_REQUIRED": 0, "PROPOSAL_ONLY": 1, "MONITOR_ONLY": 2}
    return sorted(
        deduped,
        key=lambda row: (
            priority_rank.get(str(row.get("priority")), 9),
            status_rank.get(str(row.get("proposal_status")), 9),
            -int(row.get("sample_count") or 0),
            str(row.get("proposal_id")),
        ),
    )


def build_proposals(pattern_rows: list[dict[str, str]], target_date: str, generated_at: str) -> list[dict[str, object]]:
    proposals = [build_proposal(pattern, target_date, generated_at) for pattern in pattern_rows]
    return dedupe_proposals(proposals)


def load_patterns(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_learning_patterns.csv"))
    rows.extend(read_csv_rows(processed_dir / "today" / target_date / "vsigma_learning_patterns.csv"))
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (norm(row.get("pattern_type")), norm(row.get("pattern_key")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, proposals: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Improvement Proposals - {target_date}",
        "",
        "## Executive Proposal Summary",
        f"- generated_at: {generated_at}",
        f"- proposals generated: {len(proposals)}",
        f"- proposal_type_counts: {format_counter(counter(proposals, 'proposal_type'))}",
        f"- proposal_status_counts: {format_counter(counter(proposals, 'proposal_status'))}",
        f"- priority_counts: {format_counter(counter(proposals, 'priority'))}",
        "",
        "## Top Proposals",
    ]
    if not proposals:
        lines.append("- none")
    else:
        for proposal in proposals[:20]:
            lines.append(
                f"- {proposal['priority']} | {proposal['proposal_status']} | {proposal['proposal_type']} | "
                f"{proposal['source_pattern_type']} | n={proposal['sample_count']} | auto_apply={proposal['auto_apply']} | "
                f"action={proposal['recommended_action']}"
            )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- auto_apply: NO for every proposal",
            "- predictive changes applied: NO",
            "- threshold changes applied: NO",
            "- calibration changes applied: NO",
            "- ranking changes applied: NO",
            "- market-selection changes applied: NO",
            "",
            "## Next Engine",
            "- OPERATIONAL_PROPOSAL rows feed operator/workflow review.",
            "- DATA_QUALITY_PROPOSAL rows feed data coverage and post-result labeling improvement.",
            "- MODEL_SHADOW_PROPOSAL rows feed the future shadow experiment engine only.",
            "",
        ]
    )
    return "\n".join(lines)


def build_improvement_proposals(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], ImprovementProposalPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    pattern_rows = load_patterns(processed_dir, target_date)
    proposals = build_proposals(pattern_rows, target_date, generated_at)
    paths = ImprovementProposalPaths(
        today_csv=today / "vsigma_improvement_proposals.csv",
        today_md=today / "vsigma_improvement_proposals.md",
        governance_csv=governance / "vsigma_improvement_proposals.csv",
        governance_md=governance / "vsigma_improvement_proposals.md",
    )
    markdown = build_markdown(target_date, generated_at, proposals)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, proposals)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return proposals, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA improvement proposals from learning patterns.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    proposals, paths = build_improvement_proposals(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA IMPROVEMENT PROPOSALS ===")
    print(f"proposals={len(proposals)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
