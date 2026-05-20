from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
EXPERIMENT_COLUMNS = [
    "target_date",
    "generated_at",
    "experiment_id",
    "source_proposal_id",
    "source_pattern_type",
    "source_pattern_key",
    "experiment_type",
    "shadow_status",
    "activation_scope",
    "baseline_policy",
    "candidate_policy",
    "expected_effect",
    "sample_requirements",
    "promotion_gate",
    "production_impact",
    "auto_apply",
    "guardrail_status",
]

QUALITY_TOKENS = {"UNKNOWN_MARKET", "UNKNOWN_RISK", "UNRESOLVED", "NO_SIGNAL"}
OPERATIONAL_TOKENS = {"WAITING_PRELOCK", "WAIT_FOR_POST_RESULTS", "EXPIRED_PRELOCK", "DATA_BLOCKED", "TECHNICAL_REVIEW"}


@dataclass(frozen=True)
class ShadowExperimentPaths:
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
        writer = csv.DictWriter(handle, fieldnames=EXPERIMENT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in EXPERIMENT_COLUMNS})


def has_quality_gap(value: str) -> bool:
    text = upper(value)
    return any(token in text for token in QUALITY_TOKENS)


def has_operational_gap(value: str) -> bool:
    text = upper(value)
    return any(token in text for token in OPERATIONAL_TOKENS)


def is_pure_predictive_shadow_key(value: str) -> bool:
    key = upper(value)
    if not key or has_quality_gap(key) or has_operational_gap(key):
        return False
    return "LOW_CONVERSION" in key or "ACTIONABLE_LOSS" in key


def is_shadow_eligible(proposal: dict[str, str]) -> bool:
    if upper(proposal.get("proposal_type")) != "MODEL_SHADOW_PROPOSAL":
        return False
    if upper(proposal.get("proposal_status")) != "SHADOW_CANDIDATE_REQUIRED":
        return False
    if upper(proposal.get("auto_apply")) != "NO":
        return False
    pattern_key = norm(proposal.get("source_pattern_key"))
    if not is_pure_predictive_shadow_key(pattern_key):
        return False
    return True


def candidate_policy_for(proposal: dict[str, str]) -> tuple[str, str, str]:
    key = upper(proposal.get("source_pattern_key"))
    pattern_type = upper(proposal.get("source_pattern_type"))
    if "LOW_CONVERSION" in key and "OVER_1_5" in key:
        return (
            "LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW",
            "For matching candidates, apply a shadow-only downgrade/check requiring stronger conversion evidence before treating OVER_1_5 as premium.",
            "Reduce false positives in OVER_1_5 low-conversion clusters while preserving official baseline picks.",
        )
    if "LOW_CONVERSION" in key and "OVER_2_5" in key:
        return (
            "LOW_CONVERSION_OVER25_SHRINKAGE_SHADOW",
            "For matching candidates, apply a shadow-only stricter conversion requirement before approving OVER_2_5.",
            "Reduce high-line total risk when conversion dependency is repeated.",
        )
    if pattern_type == "ACTIONABLE_LOSS_CLUSTER":
        return (
            "ACTIONABLE_LOSS_PATTERN_SHADOW",
            "Shadow-test a downgrade on candidates matching the actionable-loss pattern.",
            "Check whether loss-pattern downgrades improve closed-pick quality without increasing missed winners.",
        )
    return (
        "GENERIC_MODEL_RISK_SHADOW",
        "Shadow-test a conservative downgrade for this repeated model-risk pattern.",
        "Measure whether a conservative treatment improves quality metrics against baseline.",
    )


def build_experiment(proposal: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    experiment_type, candidate_policy, expected_effect = candidate_policy_for(proposal)
    pattern_key = norm(proposal.get("source_pattern_key"))
    proposal_id = norm(proposal.get("proposal_id"))
    experiment_id = f"SHADOW::{experiment_type}::{pattern_key}".replace(" ", "_")
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "experiment_id": experiment_id,
        "source_proposal_id": proposal_id,
        "source_pattern_type": upper(proposal.get("source_pattern_type")),
        "source_pattern_key": pattern_key,
        "experiment_type": experiment_type,
        "shadow_status": "ACTIVE_SHADOW_ONLY",
        "activation_scope": "MATCHING_FUTURE_CANDIDATES_ONLY",
        "baseline_policy": "CURRENT_PRODUCTION_LOGIC_UNCHANGED",
        "candidate_policy": candidate_policy,
        "expected_effect": expected_effect,
        "sample_requirements": "Minimum 30 closed matching samples before promotion review; preferably 50+ if variance is high.",
        "promotion_gate": "Promotion requires better decision quality, no worse drawdown, no increased missed winners, and separate promotion gate approval.",
        "production_impact": "NONE",
        "auto_apply": "NO",
        "guardrail_status": "SHADOW_ONLY_NO_PRODUCTION_CHANGE",
    }


def load_proposals(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_improvement_proposals.csv"))
    rows.extend(read_csv_rows(processed_dir / "today" / target_date / "vsigma_improvement_proposals.csv"))
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = norm(row.get("proposal_id")) or "::".join([norm(row.get("source_pattern_type")), norm(row.get("source_pattern_key"))])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def build_experiments(proposals: list[dict[str, str]], target_date: str, generated_at: str) -> list[dict[str, object]]:
    experiments = [build_experiment(proposal, target_date, generated_at) for proposal in proposals if is_shadow_eligible(proposal)]
    seen: set[str] = set()
    deduped: list[dict[str, object]] = []
    for experiment in experiments:
        key = str(experiment.get("experiment_id"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(experiment)
    return sorted(deduped, key=lambda row: str(row.get("experiment_id")))


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, experiments: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Shadow Experiments - {target_date}",
        "",
        "## Executive Shadow Summary",
        f"- generated_at: {generated_at}",
        f"- shadow_experiments: {len(experiments)}",
        f"- experiment_type_counts: {format_counter(counter(experiments, 'experiment_type'))}",
        f"- shadow_status_counts: {format_counter(counter(experiments, 'shadow_status'))}",
        "",
        "## Active Shadow Experiments",
    ]
    if not experiments:
        lines.append("- none")
    else:
        for experiment in experiments[:20]:
            lines.append(
                f"- {experiment['shadow_status']} | {experiment['experiment_type']} | "
                f"pattern={experiment['source_pattern_key']} | production_impact={experiment['production_impact']} | "
                f"auto_apply={experiment['auto_apply']}"
            )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- production logic changed: NO",
            "- official picks changed: NO",
            "- predictive formulas changed: NO",
            "- thresholds changed: NO",
            "- calibration changed: NO",
            "- ranking changed: NO",
            "- market-selection changed: NO",
            "- auto_apply: NO for every experiment",
            "",
            "## Promotion Path",
            "- Shadow experiments are evaluated only after enough closed matching samples exist.",
            "- Promotion requires a separate promotion gate and is never applied by this engine.",
            "",
        ]
    )
    return "\n".join(lines)


def build_shadow_experiments(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], ShadowExperimentPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    proposals = load_proposals(processed_dir, target_date)
    experiments = build_experiments(proposals, target_date, generated_at)
    paths = ShadowExperimentPaths(
        today_csv=today / "vsigma_shadow_experiments.csv",
        today_md=today / "vsigma_shadow_experiments.md",
        governance_csv=governance / "vsigma_shadow_experiments.csv",
        governance_md=governance / "vsigma_shadow_experiments.md",
    )
    markdown = build_markdown(target_date, generated_at, experiments)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, experiments)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return experiments, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA shadow experiments from improvement proposals.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiments, paths = build_shadow_experiments(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA SHADOW EXPERIMENTS ===")
    print(f"experiments={len(experiments)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
