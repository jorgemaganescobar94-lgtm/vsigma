from __future__ import annotations

import argparse
import csv
import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
KNOWN_CLASSIFICATIONS = {
    "EXECUTION_OK",
    "NO_BET_VALID",
    "EXPIRED_PRELOCK",
    "WAITING_FOR_PRELOCK",
    "DATA_BLOCKED",
    "TECHNICAL_WARNING",
    "BROKEN",
}
ACTION_REQUIRED = {"BROKEN", "DATA_BLOCKED", "TECHNICAL_WARNING"}
REVIEW_REQUIRED = {"EXPIRED_PRELOCK", "WAITING_FOR_PRELOCK"}


@dataclass(frozen=True)
class MonitoringSources:
    decision_quality_md: Path
    system_review_md: Path
    healthcheck_md: Path
    cloud_decision_md: Path
    prelock_resolver_md: Path
    decision_outcome_csv: Path


@dataclass(frozen=True)
class MonitoringVerdict:
    daily_classification: str
    operational_verdict: str
    action_level: str
    operator_action: str
    predictive_failure: str
    evidence_basis: str
    explanation: str


def norm(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def bullet_value(text: str, key: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(key)}\s*:\s*(.*?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text or "")
    return norm(match.group(1)) if match else ""


def heading_value(text: str, key: str) -> str:
    value = bullet_value(text, key)
    if value:
        return value
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*[:=]\s*(.*?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text or "")
    return norm(match.group(1)) if match else ""


def count_csv_rows(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
    except Exception:
        return 0
    if not rows:
        return 0
    return max(len(rows) - 1, 0)


def build_sources(processed_dir: Path, target_date: str) -> MonitoringSources:
    today = processed_dir / "today" / target_date
    return MonitoringSources(
        decision_quality_md=today / "vsigma_decision_quality_review.md",
        system_review_md=today / "vsigma_system_review.md",
        healthcheck_md=today / "vsigma_healthcheck_report.md",
        cloud_decision_md=today / "vsigma_cloud_decision_summary.md",
        prelock_resolver_md=today / "vsigma_prelock_decision_resolver.md",
        decision_outcome_csv=today / "vsigma_decision_outcome_ledger.csv",
    )


def source_statuses(sources: MonitoringSources) -> dict[str, str]:
    return {
        "decision_quality_review": "present" if sources.decision_quality_md.exists() else "missing",
        "system_review": "present" if sources.system_review_md.exists() else "missing",
        "healthcheck_report": "present" if sources.healthcheck_md.exists() else "missing",
        "cloud_decision_summary": "present" if sources.cloud_decision_md.exists() else "missing",
        "prelock_decision_resolver": "present" if sources.prelock_resolver_md.exists() else "missing",
        "decision_outcome_ledger_rows": str(count_csv_rows(sources.decision_outcome_csv)),
    }


def infer_classification(
    *,
    decision_quality_text: str,
    system_review_text: str,
    healthcheck_text: str,
    source_status: dict[str, str],
) -> MonitoringVerdict:
    dq_classification = upper(bullet_value(decision_quality_text, "daily_classification"))
    dq_operational = upper(bullet_value(decision_quality_text, "operational_verdict"))
    dq_predictive_failure = upper(bullet_value(decision_quality_text, "predictive_failure"))
    dq_note = bullet_value(decision_quality_text, "operational note") or bullet_value(decision_quality_text, "explanation")

    system_verdict = upper(bullet_value(system_review_text, "Current operational verdict"))
    health_status = upper(bullet_value(system_review_text, "Healthcheck status")) or upper(bullet_value(healthcheck_text, "status"))
    official_summary = upper(bullet_value(system_review_text, "Official action summary"))

    present_sources = [name for name, status in source_status.items() if status == "present"]
    if dq_classification in KNOWN_CLASSIFICATIONS:
        classification = dq_classification
        evidence_basis = "decision_quality_review"
    elif "NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA" in system_verdict:
        classification = "DATA_BLOCKED"
        evidence_basis = "system_review"
    elif "WAITING" in system_verdict:
        classification = "WAITING_FOR_PRELOCK"
        evidence_basis = "system_review"
    elif "EXECUTION" in system_verdict and "NO_EXECUTION" not in system_verdict:
        classification = "EXECUTION_OK"
        evidence_basis = "system_review"
    elif official_summary == "NO_BET":
        classification = "NO_BET_VALID"
        evidence_basis = "system_review"
    elif health_status in {"WARNING", "FAIL", "FAILED", "ERROR", "BROKEN"}:
        classification = "TECHNICAL_WARNING"
        evidence_basis = "healthcheck"
    elif not present_sources:
        classification = "BROKEN"
        evidence_basis = "missing_sources"
    else:
        classification = "TECHNICAL_WARNING"
        evidence_basis = "partial_sources"

    if dq_operational:
        operational_verdict = dq_operational
    elif system_verdict:
        operational_verdict = system_verdict
    elif classification == "EXECUTION_OK":
        operational_verdict = "EXECUTION_AVAILABLE"
    elif classification == "NO_BET_VALID":
        operational_verdict = "NO_EXECUTION_NO_BET_VALID"
    else:
        operational_verdict = classification

    if classification in ACTION_REQUIRED:
        action_level = "ACTION_REQUIRED"
    elif classification in REVIEW_REQUIRED:
        action_level = "REVIEW_REQUIRED"
    else:
        action_level = "NO_ACTION_REQUIRED"

    if classification == "EXECUTION_OK":
        operator_action = "Review official executable picks and post-result quality once scores are labeled."
    elif classification == "NO_BET_VALID":
        operator_action = "No manual execution needed; keep collecting no-bet evidence."
    elif classification == "EXPIRED_PRELOCK":
        operator_action = "Review AUTO/PRELOCK timing; do not count the row as predictive hit-rate failure."
    elif classification == "WAITING_FOR_PRELOCK":
        operator_action = "Wait for next scheduled AUTO/PRELOCK run or rerun prelock manually if timing is critical."
    elif classification == "DATA_BLOCKED":
        operator_action = "Check provider/API coverage, odds availability, lineups, and data-gap flags before executing."
    elif classification == "TECHNICAL_WARNING":
        operator_action = "Inspect healthcheck, workflow logs, and artifacts before trusting the day."
    else:
        operator_action = "Inspect workflow logs and required daily reports; monitoring evidence is incomplete."

    predictive_failure = dq_predictive_failure if dq_predictive_failure else ("NO" if classification != "BROKEN" else "UNKNOWN")
    explanation = dq_note or f"Classification inferred from {evidence_basis}; health_status={health_status or 'UNKNOWN'}; official_summary={official_summary or 'UNKNOWN'}."

    return MonitoringVerdict(
        daily_classification=classification,
        operational_verdict=operational_verdict,
        action_level=action_level,
        operator_action=operator_action,
        predictive_failure=predictive_failure,
        evidence_basis=evidence_basis,
        explanation=explanation,
    )


def build_markdown(
    *,
    target_date: str,
    mode: str,
    generated_at: str,
    run_url: str,
    verdict: MonitoringVerdict,
    source_status: dict[str, str],
) -> str:
    source_lines = [f"- {name}: {status}" for name, status in source_status.items()]
    lines = [
        f"# vSIGMA Autonomous Monitoring Summary - {target_date}",
        "",
        "## Executive Status",
        f"- generated_at: {generated_at}",
        f"- mode: {mode}",
        f"- daily_classification: {verdict.daily_classification}",
        f"- operational_verdict: {verdict.operational_verdict}",
        f"- action_level: {verdict.action_level}",
        f"- predictive_failure: {verdict.predictive_failure}",
        f"- evidence_basis: {verdict.evidence_basis}",
        f"- run_url: {run_url or 'N/A'}",
        "",
        "## Operator Action",
        f"- {verdict.operator_action}",
        "",
        "## Explanation",
        f"- {verdict.explanation}",
        "",
        "## Source Coverage",
        *source_lines,
        "",
        "## Classification Contract",
        "- EXECUTION_OK: at least one executable decision exists.",
        "- NO_BET_VALID: no executable row and no higher-severity block.",
        "- EXPIRED_PRELOCK: candidate expired before execution; not predictive failure.",
        "- WAITING_FOR_PRELOCK: candidate waiting for configured execution window.",
        "- DATA_BLOCKED: provider/odds/lineup/data gap blocked execution.",
        "- TECHNICAL_WARNING: healthcheck or partial evidence requires inspection.",
        "- BROKEN: required monitoring evidence is missing or inconsistent.",
        "",
    ]
    return "\n".join(lines)


def write_csv(path: Path, verdict: MonitoringVerdict, target_date: str, mode: str, generated_at: str, run_url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "target_date",
                "generated_at",
                "mode",
                "daily_classification",
                "operational_verdict",
                "action_level",
                "predictive_failure",
                "evidence_basis",
                "operator_action",
                "run_url",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "mode": mode,
                "daily_classification": verdict.daily_classification,
                "operational_verdict": verdict.operational_verdict,
                "action_level": verdict.action_level,
                "predictive_failure": verdict.predictive_failure,
                "evidence_basis": verdict.evidence_basis,
                "operator_action": verdict.operator_action,
                "run_url": run_url,
            }
        )


def build_autonomous_monitoring_summary(
    target_date: str,
    mode: str,
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    timezone_name: str = "Atlantic/Canary",
    run_url: str = "",
    now: datetime | None = None,
) -> tuple[MonitoringVerdict, Path, Path]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")

    today_dir = processed_dir / "today" / target_date
    governance_dir = processed_dir / "governance"
    today_dir.mkdir(parents=True, exist_ok=True)
    governance_dir.mkdir(parents=True, exist_ok=True)

    sources = build_sources(processed_dir, target_date)
    source_status = source_statuses(sources)
    verdict = infer_classification(
        decision_quality_text=read_text(sources.decision_quality_md),
        system_review_text=read_text(sources.system_review_md),
        healthcheck_text=read_text(sources.healthcheck_md),
        source_status=source_status,
    )
    markdown = build_markdown(
        target_date=target_date,
        mode=mode,
        generated_at=generated_at,
        run_url=run_url,
        verdict=verdict,
        source_status=source_status,
    )
    today_md = today_dir / "vsigma_autonomous_monitoring_summary.md"
    today_csv = today_dir / "vsigma_autonomous_monitoring_summary.csv"
    governance_md = governance_dir / "vsigma_autonomous_monitoring_summary.md"
    governance_csv = governance_dir / "vsigma_autonomous_monitoring_summary.csv"
    today_md.write_text(markdown, encoding="utf-8")
    governance_md.write_text(markdown, encoding="utf-8")
    write_csv(today_csv, verdict, target_date, mode, generated_at, run_url)
    write_csv(governance_csv, verdict, target_date, mode, generated_at, run_url)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with Path(summary_path).open("a", encoding="utf-8") as handle:
            handle.write(markdown)
            handle.write("\n")
    return verdict, today_md, today_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA autonomous monitoring summary for GitHub Actions.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--mode", default="unknown")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--run-url", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    verdict, md_path, csv_path = build_autonomous_monitoring_summary(
        target_date=args.date,
        mode=args.mode,
        processed_dir=args.processed_dir,
        timezone_name=args.timezone,
        run_url=args.run_url,
    )
    print("=== VSIGMA AUTONOMOUS MONITORING SUMMARY ===")
    print(f"daily_classification={verdict.daily_classification}")
    print(f"operational_verdict={verdict.operational_verdict}")
    print(f"action_level={verdict.action_level}")
    print(f"markdown={md_path}")
    print(f"csv={csv_path}")


if __name__ == "__main__":
    main()
