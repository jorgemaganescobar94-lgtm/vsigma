from __future__ import annotations

import argparse
import csv
import os
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
ACTION_REQUIRED = {"ACTION_REQUIRED"}
REVIEW_REQUIRED = {"REVIEW_REQUIRED"}
SEVERE_CLASSIFICATIONS = {"DATA_BLOCKED", "TECHNICAL_WARNING", "BROKEN"}


@dataclass(frozen=True)
class CommandCenterVerdict:
    command_center_status: str
    daily_classification: str
    action_level: str
    operational_verdict: str
    predictive_failure: str
    next_action: str
    evidence_basis: str


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() and path.is_file() else ""


def bullet_value(text: str, key: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(key)}\s*:\s*(.*?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text or "")
    return norm(match.group(1)) if match else ""


def first_bullet_under_heading(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    match = pattern.search(text or "")
    if not match:
        return ""
    bullet = re.search(r"^\s*-\s*(.*?)\s*$", match.group("body"), re.MULTILINE)
    return norm(bullet.group(1)) if bullet else ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def count_by(rows: list[dict[str, str]], column: str) -> Counter[str]:
    values = [upper(row.get(column)) or "UNKNOWN" for row in rows]
    return Counter(values)


def format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in counter.most_common())


def source_status(path: Path) -> str:
    return "present" if path.exists() else "missing"


def build_verdict(monitoring_text: str) -> CommandCenterVerdict:
    classification = upper(bullet_value(monitoring_text, "daily_classification")) or "BROKEN"
    action_level = upper(bullet_value(monitoring_text, "action_level")) or "ACTION_REQUIRED"
    operational_verdict = upper(bullet_value(monitoring_text, "operational_verdict")) or "BROKEN"
    predictive_failure = upper(bullet_value(monitoring_text, "predictive_failure")) or "UNKNOWN"
    evidence_basis = bullet_value(monitoring_text, "evidence_basis") or "missing_monitoring_summary"
    operator_action = first_bullet_under_heading(monitoring_text, "Operator Action")

    if action_level in ACTION_REQUIRED or classification in SEVERE_CLASSIFICATIONS:
        status = "ACTION_REQUIRED"
        next_action = operator_action or "Inspect workflow logs, artifacts, data coverage, and alert issues before trusting execution."
    elif action_level in REVIEW_REQUIRED:
        status = "REVIEW_HOLD"
        next_action = operator_action or "Review the next scheduled run or wait for PRELOCK/state transition."
    elif classification == "EXECUTION_OK":
        status = "EXECUTION_READY"
        next_action = operator_action or "Review executable picks and post-result quality when scores are available."
    elif classification == "NO_BET_VALID":
        status = "NO_ACTION_REQUIRED"
        next_action = operator_action or "No execution needed; keep collecting evidence."
    else:
        status = "MONITOR"
        next_action = operator_action or "Continue monitoring."

    return CommandCenterVerdict(
        command_center_status=status,
        daily_classification=classification,
        action_level=action_level,
        operational_verdict=operational_verdict,
        predictive_failure=predictive_failure,
        next_action=next_action,
        evidence_basis=evidence_basis,
    )


def build_markdown(
    *,
    target_date: str,
    mode: str,
    generated_at: str,
    run_url: str,
    verdict: CommandCenterVerdict,
    source_map: dict[str, Path],
    decision_rows: list[dict[str, str]],
    quality_rows: list[dict[str, str]],
) -> str:
    official_actions = count_by(decision_rows, "official_action")
    family_statuses = count_by(decision_rows, "execution_family_status")
    quality_labels = count_by(quality_rows, "decision_quality_label")
    quality_buckets = count_by(quality_rows, "quality_bucket")

    source_lines = [f"- {name}: {source_status(path)} — `{path}`" for name, path in source_map.items()]
    lines = [
        f"# vSIGMA Daily Command Center - {target_date}",
        "",
        "## Executive Command",
        f"- generated_at: {generated_at}",
        f"- mode: {mode}",
        f"- command_center_status: {verdict.command_center_status}",
        f"- daily_classification: {verdict.daily_classification}",
        f"- action_level: {verdict.action_level}",
        f"- operational_verdict: {verdict.operational_verdict}",
        f"- predictive_failure: {verdict.predictive_failure}",
        f"- evidence_basis: {verdict.evidence_basis}",
        f"- run_url: {run_url or 'N/A'}",
        "",
        "## Next Operator Action",
        f"- {verdict.next_action}",
        "",
        "## Decision Snapshot",
        f"- decision_outcome_rows: {len(decision_rows)}",
        f"- official_action_counts: {format_counter(official_actions)}",
        f"- execution_family_status_counts: {format_counter(family_statuses)}",
        "",
        "## Quality Snapshot",
        f"- decision_quality_rows: {len(quality_rows)}",
        f"- decision_quality_labels: {format_counter(quality_labels)}",
        f"- quality_buckets: {format_counter(quality_buckets)}",
        "",
        "## Source Coverage",
        *source_lines,
        "",
        "## Operating Rules",
        "- ACTION_REQUIRED: inspect before trusting the day.",
        "- REVIEW_HOLD: no urgent alert, but follow the next state transition.",
        "- EXECUTION_READY: executable decision exists; review execution and post-result later.",
        "- NO_ACTION_REQUIRED: no execution needed.",
        "- No predictive formulas, thresholds, calibration, or market logic are changed by this command center.",
        "",
    ]
    return "\n".join(lines)


def write_csv(path: Path, target_date: str, mode: str, generated_at: str, run_url: str, verdict: CommandCenterVerdict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "target_date",
                "generated_at",
                "mode",
                "command_center_status",
                "daily_classification",
                "action_level",
                "operational_verdict",
                "predictive_failure",
                "evidence_basis",
                "next_action",
                "run_url",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "mode": mode,
                "command_center_status": verdict.command_center_status,
                "daily_classification": verdict.daily_classification,
                "action_level": verdict.action_level,
                "operational_verdict": verdict.operational_verdict,
                "predictive_failure": verdict.predictive_failure,
                "evidence_basis": verdict.evidence_basis,
                "next_action": verdict.next_action,
                "run_url": run_url,
            }
        )


def build_daily_command_center(
    target_date: str,
    mode: str,
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    timezone_name: str = "Atlantic/Canary",
    run_url: str = "",
    now: datetime | None = None,
) -> tuple[CommandCenterVerdict, Path, Path]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")

    today_dir = processed_dir / "today" / target_date
    governance_dir = processed_dir / "governance"
    today_dir.mkdir(parents=True, exist_ok=True)
    governance_dir.mkdir(parents=True, exist_ok=True)

    source_map = {
        "monitoring_summary": today_dir / "vsigma_autonomous_monitoring_summary.md",
        "decision_quality_review": today_dir / "vsigma_decision_quality_review.md",
        "system_review": today_dir / "vsigma_system_review.md",
        "prelock_resolver": today_dir / "vsigma_prelock_decision_resolver.md",
        "cloud_decision_summary": today_dir / "vsigma_cloud_decision_summary.md",
        "decision_outcome_ledger": today_dir / "vsigma_decision_outcome_ledger.csv",
    }
    monitoring_text = read_text(source_map["monitoring_summary"])
    verdict = build_verdict(monitoring_text)
    decision_rows = read_csv_rows(source_map["decision_outcome_ledger"])
    quality_rows = read_csv_rows(today_dir / "vsigma_decision_quality_review.csv")

    markdown = build_markdown(
        target_date=target_date,
        mode=mode,
        generated_at=generated_at,
        run_url=run_url,
        verdict=verdict,
        source_map=source_map,
        decision_rows=decision_rows,
        quality_rows=quality_rows,
    )

    today_md = today_dir / "vsigma_daily_command_center.md"
    today_csv = today_dir / "vsigma_daily_command_center.csv"
    governance_md = governance_dir / "vsigma_daily_command_center.md"
    governance_csv = governance_dir / "vsigma_daily_command_center.csv"
    today_md.write_text(markdown, encoding="utf-8")
    governance_md.write_text(markdown, encoding="utf-8")
    write_csv(today_csv, target_date, mode, generated_at, run_url, verdict)
    write_csv(governance_csv, target_date, mode, generated_at, run_url, verdict)

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with Path(summary_file).open("a", encoding="utf-8") as handle:
            handle.write(markdown)
            handle.write("\n")
    return verdict, today_md, today_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA daily command center.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--mode", default="unknown")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--run-url", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    verdict, md_path, csv_path = build_daily_command_center(
        target_date=args.date,
        mode=args.mode,
        processed_dir=args.processed_dir,
        timezone_name=args.timezone,
        run_url=args.run_url,
    )
    print("=== VSIGMA DAILY COMMAND CENTER ===")
    print(f"command_center_status={verdict.command_center_status}")
    print(f"daily_classification={verdict.daily_classification}")
    print(f"action_level={verdict.action_level}")
    print(f"markdown={md_path}")
    print(f"csv={csv_path}")


if __name__ == "__main__":
    main()
