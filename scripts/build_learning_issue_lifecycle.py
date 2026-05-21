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
LIFECYCLE_COLUMNS = [
    "target_date",
    "generated_at",
    "issue_number",
    "title",
    "url",
    "lifecycle_status",
    "recommended_action",
    "reason",
    "auto_close",
    "production_change",
    "guardrail_status",
]

ACTIVE_CONSOLIDATED_PREFIXES = (
    "vSIGMA OPERATIONAL_REVIEW_REQUIRED",
    "vSIGMA DATA_QUALITY_REVIEW_REQUIRED",
    "vSIGMA PROMOTION_REVIEW_REQUIRED",
    "vSIGMA SHADOW_REJECTION_REVIEW",
)
OLD_UNCONSOLIDATED_PREFIX = "vSIGMA learning alert:"


@dataclass(frozen=True)
class LearningIssueLifecyclePaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def gh_available() -> bool:
    try:
        return run_gh(["--version"]).returncode == 0
    except FileNotFoundError:
        return False


def fetch_open_learning_issues(repo: str) -> list[dict[str, object]]:
    if not repo or not gh_available():
        return []
    result = run_gh([
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--label",
        "learning-autopilot",
        "--json",
        "number,title,url,updatedAt",
        "--limit",
        "200",
    ])
    if result.returncode != 0 or not result.stdout.strip():
        return []
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    return [dict(item) for item in data]


def classify_issue(issue: dict[str, object], target_date: str) -> dict[str, str]:
    title = norm(issue.get("title"))
    url = norm(issue.get("url"))
    number = norm(issue.get("number"))

    if title.startswith(ACTIVE_CONSOLIDATED_PREFIXES) and target_date in title:
        status = "KEEP_OPEN_CURRENT_CONSOLIDATED"
        action = "KEEP_OPEN"
        reason = "Current consolidated learning alert for this date/category."
    elif title.startswith(ACTIVE_CONSOLIDATED_PREFIXES):
        status = "STALE_CONSOLIDATED_REVIEW"
        action = "REVIEW_FOR_MANUAL_CLOSE"
        reason = "Consolidated alert from another date; keep unless a newer category issue supersedes it."
    elif title.startswith(OLD_UNCONSOLIDATED_PREFIX):
        status = "OLD_UNCONSOLIDATED_DUPLICATE"
        action = "CLOSE_IF_SUPERSEDED"
        reason = "Pre-consolidation issue; should be closed when matching consolidated issue exists."
    else:
        status = "UNKNOWN_LEARNING_ALERT_SHAPE"
        action = "REVIEW"
        reason = "Issue title does not match expected consolidated or pre-consolidation format."

    return {
        "issue_number": number,
        "title": title,
        "url": url,
        "lifecycle_status": status,
        "recommended_action": action,
        "reason": reason,
        "auto_close": "NO",
        "production_change": "NO",
        "guardrail_status": "LIFECYCLE_REPORT_ONLY_NO_AUTO_CLOSE",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LIFECYCLE_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in LIFECYCLE_COLUMNS})


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Learning Issue Lifecycle - {target_date}",
        "",
        "## Executive Lifecycle Summary",
        f"- generated_at: {generated_at}",
        f"- open_learning_issues_reviewed: {len(rows)}",
        f"- lifecycle_status_counts: {format_counter(counter(rows, 'lifecycle_status'))}",
        f"- recommended_action_counts: {format_counter(counter(rows, 'recommended_action'))}",
        "",
        "## Issue Lifecycle Decisions",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:50]:
            lines.append(
                f"- #{row['issue_number']} | {row['lifecycle_status']} | action={row['recommended_action']} | auto_close={row['auto_close']} | {row['title']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- auto_close: NO for every row",
        "- production_change: NO",
        "- official picks changed: NO",
        "- model changes applied: NO",
        "",
        "## Policy",
        "- This phase reports lifecycle status only.",
        "- Automatic closure can be enabled later only after report behavior is validated.",
        "",
    ])
    return "\n".join(lines)


def build_learning_issue_lifecycle(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    repo: str = "",
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], LearningIssueLifecyclePaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    issues = fetch_open_learning_issues(repo)
    rows: list[dict[str, object]] = []
    for issue in issues:
        row = classify_issue(issue, target_date)
        row["target_date"] = target_date
        row["generated_at"] = generated_at
        rows.append(row)

    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = LearningIssueLifecyclePaths(
        today_csv=today / "vsigma_learning_issue_lifecycle.csv",
        today_md=today / "vsigma_learning_issue_lifecycle.md",
        governance_csv=governance / "vsigma_learning_issue_lifecycle.csv",
        governance_md=governance / "vsigma_learning_issue_lifecycle.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA learning issue lifecycle report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_learning_issue_lifecycle(args.date, args.timezone, args.processed_dir, args.repo)
    print("=== VSIGMA LEARNING ISSUE LIFECYCLE ===")
    print(f"reviewed={len(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
