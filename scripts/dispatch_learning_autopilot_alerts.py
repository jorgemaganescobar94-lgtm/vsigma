from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
LABELS = ["vsigma", "learning-autopilot"]
ALERT_COLUMNS = [
    "target_date",
    "generated_at",
    "alert_id",
    "alert_type",
    "severity",
    "source_file",
    "source_key",
    "title",
    "body",
    "should_open_issue",
    "issue_url",
    "auto_apply",
    "production_change",
    "guardrail_status",
]

PROMOTION_REVIEW_DECISIONS = {"PROMOTION_CANDIDATE_REVIEW_ONLY", "READY_FOR_REVIEW"}
PROMOTION_REJECTION_DECISIONS = {"REJECTED_WEAK_SIGNAL"}
IGNORED_PROMOTION_DECISIONS = {"NOT_READY_SAMPLE_TOO_SMALL", ""}


@dataclass(frozen=True)
class LearningAutopilotPaths:
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
        writer = csv.DictWriter(handle, fieldnames=ALERT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in ALERT_COLUMNS})


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def gh_available() -> bool:
    try:
        return run_gh(["--version"]).returncode == 0
    except FileNotFoundError:
        return False


def ensure_labels(repo: str) -> None:
    for label in LABELS:
        run_gh(["label", "create", label, "--repo", repo, "--color", "5319E7", "--description", "vSIGMA learning autopilot alert"])


def existing_issue(repo: str, title: str) -> str:
    result = run_gh(["issue", "list", "--repo", repo, "--state", "open", "--search", title, "--json", "title,url", "--limit", "100"])
    if result.returncode != 0 or not result.stdout.strip():
        return ""
    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError:
        return ""
    for issue in issues:
        if issue.get("title") == title:
            return norm(issue.get("url"))
    return ""


def dispatch_issue(repo: str, title: str, body: str, dry_run: bool = False) -> str:
    if dry_run:
        return "DRY_RUN"
    if not gh_available():
        raise RuntimeError("gh CLI is not available")
    existing = existing_issue(repo, title)
    if existing:
        return existing
    ensure_labels(repo)
    result = run_gh(["issue", "create", "--repo", repo, "--title", title, "--body", body, "--label", ",".join(LABELS)])
    if result.returncode != 0:
        raise RuntimeError(f"gh issue create failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def promotion_alerts(target_date: str, generated_at: str, rows: list[dict[str, str]], run_url: str) -> list[dict[str, object]]:
    alerts: list[dict[str, object]] = []
    for row in rows:
        decision = upper(row.get("promotion_decision"))
        if decision in IGNORED_PROMOTION_DECISIONS:
            continue
        experiment_type = upper(row.get("experiment_type")) or "UNKNOWN_EXPERIMENT"
        experiment_id = norm(row.get("experiment_id"))
        closed = norm(row.get("closed_sample_count"))
        wins = norm(row.get("wins"))
        losses = norm(row.get("losses"))
        if decision in PROMOTION_REVIEW_DECISIONS:
            alert_type = "PROMOTION_REVIEW_REQUIRED"
            severity = "P1"
            title = f"vSIGMA review gate: {experiment_type} requires review ({target_date})"
        elif decision in PROMOTION_REJECTION_DECISIONS:
            alert_type = "SHADOW_REJECTION_REVIEW"
            severity = "P2"
            title = f"vSIGMA review gate: {experiment_type} weak signal ({target_date})"
        else:
            alert_type = "PROMOTION_GATE_REVIEW"
            severity = "P2"
            title = f"vSIGMA review gate: {experiment_type} {decision} ({target_date})"
        body = "\n".join([
            f"# {title}",
            "",
            "The review decision gate produced an actionable learning state.",
            "",
            "## Evidence",
            f"- experiment_id: {experiment_id}",
            f"- experiment_type: {experiment_type}",
            f"- promotion_decision: {decision}",
            f"- closed_sample_count: {closed}",
            f"- wins: {wins}",
            f"- losses: {losses}",
            f"- run_url: {run_url or 'N/A'}",
            "",
            "## Guardrails",
            "- auto_promote: NO",
            "- production_change: NO",
            "- official picks changed: NO",
            "- model changes applied: NO",
        ])
        alerts.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "alert_id": f"{alert_type}::{experiment_id or experiment_type}",
            "alert_type": alert_type,
            "severity": severity,
            "source_file": "vsigma_promotion_gate.csv",
            "source_key": experiment_id or experiment_type,
            "title": title,
            "body": body,
            "should_open_issue": "YES",
            "issue_url": "",
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "ALERT_ONLY_NO_AUTO_CHANGE",
        })
    return alerts


def proposal_alerts(target_date: str, generated_at: str, rows: list[dict[str, str]], run_url: str) -> list[dict[str, object]]:
    alerts: list[dict[str, object]] = []
    for row in rows:
        proposal_type = upper(row.get("proposal_type"))
        priority = upper(row.get("priority"))
        status = upper(row.get("proposal_status"))
        if proposal_type == "OPERATIONAL_PROPOSAL" and priority == "P1":
            alert_type = "OPERATIONAL_REVIEW_REQUIRED"
            severity = "P1"
        elif proposal_type == "DATA_QUALITY_PROPOSAL" and priority in {"P1", "P2"}:
            alert_type = "DATA_QUALITY_REVIEW_REQUIRED"
            severity = priority
        else:
            continue
        source_key = norm(row.get("source_pattern_key")) or norm(row.get("proposal_id"))
        title = f"vSIGMA learning alert: {alert_type} {source_key} ({target_date})"
        body = "\n".join([
            f"# {title}",
            "",
            "The learning autopilot found an actionable non-model review item.",
            "",
            "## Evidence",
            f"- proposal_type: {proposal_type}",
            f"- proposal_status: {status}",
            f"- priority: {priority}",
            f"- source_pattern_key: {source_key}",
            f"- recommended_action: {norm(row.get('recommended_action'))}",
            f"- run_url: {run_url or 'N/A'}",
            "",
            "## Guardrails",
            "- auto_apply: NO",
            "- production_change: NO",
            "- model changes applied: NO",
        ])
        alerts.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "alert_id": f"{alert_type}::{source_key}",
            "alert_type": alert_type,
            "severity": severity,
            "source_file": "vsigma_improvement_proposals.csv",
            "source_key": source_key,
            "title": title,
            "body": body,
            "should_open_issue": "YES",
            "issue_url": "",
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "ALERT_ONLY_NO_AUTO_CHANGE",
        })
    return alerts


def dedupe_alerts(alerts: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    deduped: list[dict[str, object]] = []
    rank = {"P1": 0, "P2": 1, "P3": 2}
    for alert in sorted(alerts, key=lambda row: (rank.get(str(row.get("severity")), 9), str(row.get("alert_id")))):
        key = str(alert.get("alert_id"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(alert)
    return deduped


def consolidated_title(alert_type: str, target_date: str) -> str:
    return f"vSIGMA {alert_type} {target_date}"


def consolidate_alerts(alerts: list[dict[str, object]], target_date: str, generated_at: str) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = {}
    for alert in alerts:
        alert_type = str(alert.get("alert_type") or "UNKNOWN_ALERT")
        groups.setdefault(alert_type, []).append(alert)

    severity_rank = {"P1": 0, "P2": 1, "P3": 2}
    consolidated: list[dict[str, object]] = []

    for alert_type, group in groups.items():
        severity = sorted(
            [str(row.get("severity") or "P3") for row in group],
            key=lambda item: severity_rank.get(item, 9),
        )[0]
        source_keys = [
            str(row.get("source_key") or "").strip()
            for row in group
            if str(row.get("source_key") or "").strip()
        ]
        source_files = sorted({
            str(row.get("source_file") or "").strip()
            for row in group
            if str(row.get("source_file") or "").strip()
        })

        title = consolidated_title(alert_type, target_date)

        body_lines = [
            f"# {title}",
            "",
            f"Consolidated vSIGMA learning autopilot alert for {target_date}.",
            "",
            "## Summary",
            f"- alert_type: {alert_type}",
            f"- severity: {severity}",
            f"- source_count: {len(group)}",
            f"- source_files: {';'.join(source_files) or 'UNKNOWN'}",
            "",
            "## Sources",
        ]

        for row in group:
            body_lines.append(
                f"- {str(row.get('source_key') or 'UNKNOWN')} :: {str(row.get('alert_type') or 'UNKNOWN')} :: {str(row.get('severity') or 'UNKNOWN')}"
            )

        body_lines.extend([
            "",
            "## Guardrails",
            "- auto_apply: NO",
            "- production_change: NO",
            "- official picks changed: NO",
            "- model changes applied: NO",
        ])

        consolidated.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "alert_id": f"{alert_type}::{target_date}",
            "alert_type": alert_type,
            "severity": severity,
            "source_file": ";".join(source_files),
            "source_key": ";".join(source_keys),
            "title": title,
            "body": "\n".join(body_lines),
            "should_open_issue": "YES",
            "issue_url": "",
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "ALERT_ONLY_NO_AUTO_CHANGE",
        })

    return sorted(
        consolidated,
        key=lambda row: (severity_rank.get(str(row.get("severity")), 9), str(row.get("alert_type"))),
    )


def dispatch_alerts(alerts: list[dict[str, object]], repo: str, dry_run: bool) -> list[dict[str, object]]:
    if not repo and any(alert.get("should_open_issue") == "YES" for alert in alerts):
        raise RuntimeError("repo is required to open GitHub issues")
    updated: list[dict[str, object]] = []
    for alert in alerts:
        row = dict(alert)
        if row.get("should_open_issue") == "YES":
            row["issue_url"] = dispatch_issue(repo, str(row["title"]), str(row["body"]), dry_run=dry_run)
        updated.append(row)
    return updated


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, alerts: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Learning Autopilot Alerts - {target_date}",
        "",
        "## Executive Alert Summary",
        f"- generated_at: {generated_at}",
        f"- alerts generated: {len(alerts)}",
        f"- alert_type_counts: {format_counter(counter(alerts, 'alert_type'))}",
        f"- severity_counts: {format_counter(counter(alerts, 'severity'))}",
        f"- issues_opened_or_existing: {sum(1 for alert in alerts if norm(alert.get('issue_url')))}",
        "",
        "## Alerts",
    ]
    if not alerts:
        lines.append("- none")
    else:
        for alert in alerts[:20]:
            lines.append(
                f"- {alert['severity']} | {alert['alert_type']} | sources={len([item for item in str(alert.get('source_key') or '').split(';') if item])} | "
                f"issue={alert.get('issue_url') or 'N/A'} | auto_apply={alert['auto_apply']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- auto_apply: NO for every alert",
        "- production_change: NO for every alert",
        "- official picks changed: NO",
        "- model changes applied: NO",
        "",
    ])
    return "\n".join(lines)


def write_outputs(processed_dir: Path, target_date: str, markdown: str, alerts: list[dict[str, object]]) -> LearningAutopilotPaths:
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = LearningAutopilotPaths(
        today_csv=today / "vsigma_learning_autopilot_alerts.csv",
        today_md=today / "vsigma_learning_autopilot_alerts.md",
        governance_csv=governance / "vsigma_learning_autopilot_alerts.csv",
        governance_md=governance / "vsigma_learning_autopilot_alerts.md",
    )
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, alerts)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return paths


@dataclass(frozen=True)
class LearningAutopilotPaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def build_learning_autopilot_alerts(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    repo: str = "",
    run_url: str = "",
    dry_run: bool = False,
    dispatch: bool = False,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], LearningAutopilotPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    proposals = read_csv_rows(today / "vsigma_improvement_proposals.csv") or read_csv_rows(governance / "vsigma_improvement_proposals.csv")
    gates = read_csv_rows(today / "vsigma_promotion_gate.csv") or read_csv_rows(governance / "vsigma_promotion_gate.csv")
    raw_alerts = dedupe_alerts([
        *proposal_alerts(target_date, generated_at, proposals, run_url),
        *promotion_alerts(target_date, generated_at, gates, run_url),
    ])
    alerts = consolidate_alerts(raw_alerts, target_date, generated_at)
    if dispatch and alerts:
        alerts = dispatch_alerts(alerts, repo, dry_run)
    markdown = build_markdown(target_date, generated_at, alerts)
    paths = write_outputs(processed_dir, target_date, markdown, alerts)
    return alerts, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and optionally dispatch vSIGMA learning autopilot alerts.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--run-url", default="")
    parser.add_argument("--dispatch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    alerts, paths = build_learning_autopilot_alerts(
        args.date,
        args.timezone,
        args.processed_dir,
        repo=args.repo,
        run_url=args.run_url,
        dry_run=args.dry_run,
        dispatch=args.dispatch,
    )
    print("=== VSIGMA LEARNING AUTOPILOT ALERTS ===")
    print(f"alerts={len(alerts)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
