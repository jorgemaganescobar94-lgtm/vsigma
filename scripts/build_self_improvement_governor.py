from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_PROCESSED_DIR = Path("data/processed")
MIN_PROMOTION_REVIEW_SAMPLE = 30

GOVERNOR_COLUMNS = [
    "target_date",
    "generated_at",
    "governor_id",
    "source_type",
    "source_id",
    "source_key",
    "priority",
    "sample_count",
    "status_input",
    "governor_decision",
    "governor_reason",
    "next_action",
    "required_evidence",
    "allowed_engine",
    "auto_apply",
    "production_change",
    "shadow_allowed",
    "promotion_pr_allowed",
    "guardrail_status",
]


@dataclass(frozen=True)
class SelfImprovementGovernorPaths:
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GOVERNOR_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in GOVERNOR_COLUMNS})


def first_existing_rows(processed_dir: Path, target_date: str, filename: str) -> list[dict[str, str]]:
    today_rows = read_csv_rows(processed_dir / "today" / target_date / filename)
    governance_rows = read_csv_rows(processed_dir / "governance" / filename)
    return today_rows or governance_rows


def dedupe_by(rows: list[dict[str, str]], keys: list[str]) -> list[dict[str, str]]:
    seen: set[tuple[str, ...]] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        key = tuple(norm(row.get(name)) for name in keys)
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def load_proposals(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows = first_existing_rows(processed_dir, target_date, "vsigma_improvement_proposals.csv")
    return dedupe_by(rows, ["proposal_id"])


def load_shadow_candidates(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows = first_existing_rows(processed_dir, target_date, "vsigma_shadow_candidates.csv")
    return dedupe_by(rows, ["fixture_id", "market_primary", "experiment_id"])


def load_promotion_gate(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows = first_existing_rows(processed_dir, target_date, "vsigma_promotion_gate.csv")
    return dedupe_by(rows, ["experiment_id"])


def priority_rank(priority: str) -> int:
    return {"P1": 0, "P2": 1, "P3": 2}.get(upper(priority), 9)


def governor_row(
    target_date: str,
    generated_at: str,
    source_type: str,
    source_id: str,
    source_key: str,
    priority: str,
    sample_count: int,
    status_input: str,
    decision: str,
    reason: str,
    next_action: str,
    required_evidence: str,
    allowed_engine: str,
    shadow_allowed: str,
    promotion_pr_allowed: str,
) -> dict[str, object]:
    governor_id = f"{source_type}::{source_id or source_key}".replace(" ", "_")
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "governor_id": governor_id,
        "source_type": source_type,
        "source_id": source_id,
        "source_key": source_key,
        "priority": priority or "P3",
        "sample_count": sample_count,
        "status_input": status_input,
        "governor_decision": decision,
        "governor_reason": reason,
        "next_action": next_action,
        "required_evidence": required_evidence,
        "allowed_engine": allowed_engine,
        "auto_apply": "NO",
        "production_change": "NO",
        "shadow_allowed": shadow_allowed,
        "promotion_pr_allowed": promotion_pr_allowed,
        "guardrail_status": "SELF_IMPROVEMENT_REVIEW_ONLY_NO_AUTO_PRODUCTION_CHANGE",
    }


def decision_for_proposal(row: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    proposal_type = upper(row.get("proposal_type"))
    proposal_status = upper(row.get("proposal_status"))
    priority = upper(row.get("priority")) or "P3"
    sample_count = as_int(row.get("sample_count"))
    proposal_id = norm(row.get("proposal_id"))
    key = norm(row.get("source_pattern_key"))

    if proposal_type == "DATA_QUALITY_PROPOSAL":
        return governor_row(
            target_date,
            generated_at,
            "IMPROVEMENT_PROPOSAL",
            proposal_id,
            key,
            priority,
            sample_count,
            proposal_status,
            "DATA_QUALITY_FIRST",
            "Evidence quality gap must be resolved before any model/shadow promotion path.",
            "OPEN_DATA_QUALITY_REVIEW",
            "Resolved UNKNOWN/UNRESOLVED/NO_SIGNAL rows and complete post-result labeling.",
            "data_quality_review",
            "NO",
            "NO",
        )

    if proposal_type == "OPERATIONAL_PROPOSAL":
        return governor_row(
            target_date,
            generated_at,
            "IMPROVEMENT_PROPOSAL",
            proposal_id,
            key,
            priority,
            sample_count,
            proposal_status,
            "OPERATIONAL_REVIEW_REQUIRED",
            "Operational timing/freshness issue affects execution quality, not production model logic.",
            "OPEN_OPERATIONAL_REVIEW",
            "Stable PRE/AUTO/PRELOCK/POST behavior across repeated scheduled runs.",
            "operator_review",
            "NO",
            "NO",
        )

    if proposal_type == "MODEL_SHADOW_PROPOSAL" and proposal_status == "SHADOW_CANDIDATE_REQUIRED":
        return governor_row(
            target_date,
            generated_at,
            "IMPROVEMENT_PROPOSAL",
            proposal_id,
            key,
            priority,
            sample_count,
            proposal_status,
            "SHADOW_FACTORY_ALLOWED",
            "Pattern has enough proposal evidence to create/continue a shadow-only candidate, not to modify production.",
            "CREATE_OR_CONTINUE_SHADOW_CANDIDATE",
            "Backtest plus forward-test evidence against official baseline.",
            "shadow_candidate_factory",
            "YES",
            "NO",
        )

    return governor_row(
        target_date,
        generated_at,
        "IMPROVEMENT_PROPOSAL",
        proposal_id,
        key,
        priority,
        sample_count,
        proposal_status,
        "MONITOR_MORE_EVIDENCE",
        "Proposal does not clear the threshold for shadow creation or operational/data-quality escalation.",
        "KEEP_MONITORING",
        "More closed samples and cleaner evidence.",
        "pattern_miner",
        "NO",
        "NO",
    )


def decision_for_shadow_candidate(row: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    decision = upper(row.get("shadow_decision")) or "SHADOW_MONITOR_ONLY"
    experiment_id = norm(row.get("experiment_id"))
    key = norm(row.get("source_pattern_key"))
    return governor_row(
        target_date,
        generated_at,
        "SHADOW_CANDIDATE",
        experiment_id,
        key,
        "P2" if "DOWNGRADE" in decision else "P3",
        1,
        decision,
        "SHADOW_TRACKING_ACTIVE",
        "Shadow candidate may be monitored against baseline, but production remains unchanged.",
        "TRACK_SHADOW_OUTCOME",
        "Closed shadow outcomes with ROI, hit-rate, Brier/quality, drawdown, and baseline comparison.",
        "shadow_performance_tracker",
        "YES",
        "NO",
    )


def decision_for_promotion_gate(row: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    promotion_decision = upper(row.get("promotion_decision"))
    experiment_id = norm(row.get("experiment_id"))
    key = norm(row.get("source_pattern_key"))
    closed = as_int(row.get("closed_sample_count"))

    if promotion_decision == "PROMOTION_CANDIDATE_REVIEW_ONLY":
        return governor_row(
            target_date,
            generated_at,
            "PROMOTION_GATE",
            experiment_id,
            key,
            "P1",
            closed,
            promotion_decision,
            "HUMAN_PROMOTION_REVIEW_REQUIRED",
            "Promotion gate considers this reviewable, but auto-promotion remains forbidden.",
            "OPEN_SEPARATE_PROMOTION_PR_FOR_REVIEW",
            f"At least {MIN_PROMOTION_REVIEW_SAMPLE} closed samples, positive baseline comparison, stable CLV/quality and no data-quality veto.",
            "human_review_or_separate_promotion_pr",
            "YES",
            "YES_REVIEW_ONLY",
        )

    if promotion_decision == "NOT_READY_SAMPLE_TOO_SMALL":
        return governor_row(
            target_date,
            generated_at,
            "PROMOTION_GATE",
            experiment_id,
            key,
            "P2",
            closed,
            promotion_decision,
            "COLLECT_MORE_SAMPLES",
            "Promotion evidence is too small for production consideration.",
            "CONTINUE_FORWARD_TEST",
            f"Reach at least {MIN_PROMOTION_REVIEW_SAMPLE} closed matching samples.",
            "shadow_performance_tracker",
            "YES",
            "NO",
        )

    if promotion_decision == "REJECTED_WEAK_SIGNAL":
        return governor_row(
            target_date,
            generated_at,
            "PROMOTION_GATE",
            experiment_id,
            key,
            "P2",
            closed,
            promotion_decision,
            "REJECT_OR_KEEP_SHADOW",
            "Promotion evidence is weak or negative.",
            "KEEP_SHADOW_OR_RETIRE_CANDIDATE",
            "Recovered edge versus baseline across a larger closed sample.",
            "shadow_governance",
            "YES",
            "NO",
        )

    return governor_row(
        target_date,
        generated_at,
        "PROMOTION_GATE",
        experiment_id,
        key,
        "P3",
        closed,
        promotion_decision,
        "GATE_MONITOR_ONLY",
        "Promotion gate is not asking for a production review.",
        "KEEP_MONITORING",
        "More evidence or a stronger gate status.",
        "promotion_gate",
        "YES" if experiment_id else "NO",
        "NO",
    )


def dedupe_governor_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    out: list[dict[str, object]] = []
    for row in rows:
        key = str(row.get("governor_id"))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    decision_rank = {
        "HUMAN_PROMOTION_REVIEW_REQUIRED": 0,
        "DATA_QUALITY_FIRST": 1,
        "OPERATIONAL_REVIEW_REQUIRED": 2,
        "SHADOW_FACTORY_ALLOWED": 3,
        "SHADOW_TRACKING_ACTIVE": 4,
        "COLLECT_MORE_SAMPLES": 5,
        "REJECT_OR_KEEP_SHADOW": 6,
        "MONITOR_MORE_EVIDENCE": 7,
        "GATE_MONITOR_ONLY": 8,
    }
    return sorted(
        out,
        key=lambda row: (
            decision_rank.get(str(row.get("governor_decision")), 99),
            priority_rank(str(row.get("priority"))),
            -int(row.get("sample_count") or 0),
            str(row.get("governor_id")),
        ),
    )


def build_governor_rows(
    target_date: str,
    generated_at: str,
    proposals: list[dict[str, str]],
    shadow_candidates: list[dict[str, str]],
    promotion_gate: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rows.extend(decision_for_proposal(row, target_date, generated_at) for row in proposals)
    rows.extend(decision_for_shadow_candidate(row, target_date, generated_at) for row in shadow_candidates)
    rows.extend(decision_for_promotion_gate(row, target_date, generated_at) for row in promotion_gate)
    return dedupe_governor_rows(rows)


def count(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in counter.most_common())


def executive_status(rows: list[dict[str, object]]) -> str:
    decisions = {str(row.get("governor_decision")) for row in rows}
    if "HUMAN_PROMOTION_REVIEW_REQUIRED" in decisions:
        return "PROMOTION_REVIEW_REQUIRED"
    if "DATA_QUALITY_FIRST" in decisions:
        return "DATA_QUALITY_BLOCKS_MODEL_CHANGE"
    if "OPERATIONAL_REVIEW_REQUIRED" in decisions:
        return "OPERATIONAL_REVIEW_REQUIRED"
    if "SHADOW_FACTORY_ALLOWED" in decisions:
        return "SHADOW_TESTING_REQUIRED"
    if "SHADOW_TRACKING_ACTIVE" in decisions:
        return "SHADOW_MONITORING_ACTIVE"
    return "MONITORING_ONLY"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    status = executive_status(rows)
    lines = [
        f"# vSIGMA Self-Improvement Governor - {target_date}",
        "",
        "## Executive Governor Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {status}",
        f"- decisions: {len(rows)}",
        f"- decision_counts: {format_counter(count(rows, 'governor_decision'))}",
        f"- source_counts: {format_counter(count(rows, 'source_type'))}",
        f"- auto_apply: NO",
        f"- production_change: NO",
        "",
        "## Top Governor Decisions",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:30]:
            lines.append(
                f"- {row['priority']} | {row['governor_decision']} | {row['source_type']} | "
                f"sample={row['sample_count']} | shadow_allowed={row['shadow_allowed']} | "
                f"promotion_pr_allowed={row['promotion_pr_allowed']} | next={row['next_action']} | "
                f"reason={row['governor_reason']}"
            )

    lines.extend(
        [
            "",
            "## Hard Guardrails",
            "- Production model changes applied: NO",
            "- Prediction formulas changed: NO",
            "- Thresholds changed: NO",
            "- Calibration changed: NO",
            "- Ranking changed: NO",
            "- Market-selection changed: NO",
            "- Auto-apply allowed: NO",
            "- Promotion requires a separate reviewed PR even when promotion_pr_allowed=YES_REVIEW_ONLY.",
            "",
            "## Interpretation",
            "- DATA_QUALITY_FIRST blocks model changes until evidence quality improves.",
            "- SHADOW_FACTORY_ALLOWED means experiment only; official picks remain unchanged.",
            "- HUMAN_PROMOTION_REVIEW_REQUIRED means open a separate PR/review path; no automatic activation.",
            "",
        ]
    )
    return "\n".join(lines)


def build_self_improvement_governor(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], SelfImprovementGovernorPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")

    proposals = load_proposals(processed_dir, target_date)
    shadow_candidates = load_shadow_candidates(processed_dir, target_date)
    promotion_gate = load_promotion_gate(processed_dir, target_date)
    rows = build_governor_rows(target_date, generated_at, proposals, shadow_candidates, promotion_gate)

    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    paths = SelfImprovementGovernorPaths(
        today_csv=today / "vsigma_self_improvement_governor.csv",
        today_md=today / "vsigma_self_improvement_governor.md",
        governance_csv=governance / "vsigma_self_improvement_governor.csv",
        governance_md=governance / "vsigma_self_improvement_governor.md",
    )

    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA self-improvement governor decisions.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_self_improvement_governor(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA SELF-IMPROVEMENT GOVERNOR ===")
    print(f"decisions={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
