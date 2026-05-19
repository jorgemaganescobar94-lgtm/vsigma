from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SEVERE_CLASSIFICATIONS = {"DATA_BLOCKED", "TECHNICAL_WARNING", "BROKEN"}
SEVERE_ACTION_LEVELS = {"ACTION_REQUIRED"}
LABELS = ["vsigma", "autonomous-monitoring"]


@dataclass(frozen=True)
class MonitoringNotification:
    should_notify: bool
    title: str
    body: str
    classification: str
    action_level: str
    reason: str


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


def summary_path(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date / "vsigma_autonomous_monitoring_summary.md"


def build_notification(target_date: str, mode: str, summary_text: str, run_url: str = "") -> MonitoringNotification:
    classification = upper(bullet_value(summary_text, "daily_classification")) or "UNKNOWN"
    action_level = upper(bullet_value(summary_text, "action_level")) or "UNKNOWN"
    operational_verdict = upper(bullet_value(summary_text, "operational_verdict")) or "UNKNOWN"
    predictive_failure = upper(bullet_value(summary_text, "predictive_failure")) or "UNKNOWN"
    operator_action = first_bullet_under_heading(summary_text, "Operator Action")

    if not summary_text:
        title = f"vSIGMA BROKEN {target_date}: missing autonomous monitoring summary"
        body = f"# vSIGMA Monitoring Alert - {target_date}\n\nThe autonomous monitoring summary was missing.\n\n- mode: {mode}\n- daily_classification: BROKEN\n- action_level: ACTION_REQUIRED\n- run_url: {run_url or 'N/A'}\n"
        return MonitoringNotification(True, title, body, "BROKEN", "ACTION_REQUIRED", "summary_missing")

    should_notify = classification in SEVERE_CLASSIFICATIONS or action_level in SEVERE_ACTION_LEVELS
    if not should_notify:
        return MonitoringNotification(False, "", "", classification, action_level, "not_severe")

    title = f"vSIGMA {classification} {target_date} ({mode})"
    body = "\n".join([
        f"# vSIGMA Monitoring Alert - {target_date}",
        "",
        "A vSIGMA autonomous run requires review.",
        "",
        "## Status",
        f"- mode: {mode}",
        f"- daily_classification: {classification}",
        f"- operational_verdict: {operational_verdict}",
        f"- action_level: {action_level}",
        f"- predictive_failure: {predictive_failure}",
        f"- run_url: {run_url or 'N/A'}",
        "",
        "## Operator Action",
        f"- {operator_action or 'Inspect workflow logs, artifacts, and monitoring summary.'}",
        "",
        "## Source Summary",
        summary_text,
    ])
    return MonitoringNotification(True, title, body, classification, action_level, "severe_status")


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def gh_available() -> bool:
    try:
        return run_gh(["--version"]).returncode == 0
    except FileNotFoundError:
        return False


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


def ensure_labels(repo: str) -> None:
    for label in LABELS:
        run_gh(["label", "create", label, "--repo", repo, "--color", "0E8A16", "--description", "vSIGMA automation alert"])


def dispatch_issue(repo: str, notification: MonitoringNotification, dry_run: bool = False) -> str:
    if dry_run:
        return "DRY_RUN"
    if not gh_available():
        raise RuntimeError("gh CLI is not available")
    existing = existing_issue(repo, notification.title)
    if existing:
        return existing
    ensure_labels(repo)
    result = run_gh(["issue", "create", "--repo", repo, "--title", notification.title, "--body", notification.body, "--label", ",".join(LABELS)])
    if result.returncode != 0:
        raise RuntimeError(f"gh issue create failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def append_step_summary(notification: MonitoringNotification, issue_url: str = "") -> None:
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return
    lines = ["", "## vSIGMA Notification Dispatch", f"- should_notify: {'YES' if notification.should_notify else 'NO'}", f"- classification: {notification.classification}", f"- action_level: {notification.action_level}", f"- reason: {notification.reason}"]
    if issue_url:
        lines.append(f"- issue_url: {issue_url}")
    with Path(summary_file).open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dispatch vSIGMA autonomous monitoring notifications.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--mode", default="unknown")
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--run-url", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = date.fromisoformat(args.date).isoformat()
    notification = build_notification(target_date, args.mode, read_text(summary_path(args.processed_dir, target_date)), args.run_url)
    issue_url = ""
    if notification.should_notify:
        if not args.repo:
            raise SystemExit("ERROR: --repo or GITHUB_REPOSITORY is required")
        issue_url = dispatch_issue(args.repo, notification, args.dry_run)
    append_step_summary(notification, issue_url)
    print("=== VSIGMA NOTIFICATION DISPATCH ===")
    print(f"should_notify={'YES' if notification.should_notify else 'NO'}")
    print(f"classification={notification.classification}")
    print(f"action_level={notification.action_level}")
    print(f"reason={notification.reason}")
    if issue_url:
        print(f"issue_url={issue_url}")


if __name__ == "__main__":
    main()
