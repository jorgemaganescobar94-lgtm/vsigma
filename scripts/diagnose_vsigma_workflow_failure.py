from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

LABELS = ["vsigma", "failure-doctor", "workflow-failure"]
MAX_LOG_CHARS = 60000
MAX_EVIDENCE_LINES = 30

CLASSIFICATION_PATTERNS: list[tuple[str, list[str], str]] = [
    (
        "SECRET_MISSING",
        ["Missing secret VSIGMA_ENV_B64", "VSIGMA_ENV_B64"],
        "Restore or rotate the VSIGMA_ENV_B64 repository secret before rerunning.",
    ),
    (
        "DATE_SCOPED_SNAPSHOT_MISMATCH",
        ["Execution shortlist dates", "do not match requested date", "No date-scoped execution shortlist found"],
        "Check date-scoped snapshots under data/processed/today/<date>/ and avoid using rolling files for past dates.",
    ),
    (
        "ROLLING_SNAPSHOT_CONTAMINATION",
        ["Execution ledger rows", "do not equal shortlist rows"],
        "Stage date-scoped post inputs before building the ledger, then restore rolling files.",
    ),
    (
        "MISSING_DATE_SCOPED_INPUT",
        ["Missing required date-scoped input for post-results", "Missing date-scoped snapshot directory"],
        "Run PRE for that date or restore the missing snapshot files before post-results.",
    ),
    (
        "API_RATE_LIMIT",
        ["429 Too Many Requests", "rate limit"],
        "Retry later, reduce API burst, or use cache/backoff for the affected provider call.",
    ),
    (
        "API_PROVIDER_ERROR",
        ["API errors ->", "No encontré credenciales válidas", "404 Not Found"],
        "Inspect API credentials/provider response and isolate whether the failure is auth, endpoint, or upstream data.",
    ),
    (
        "NO_UPCOMING_FIXTURES",
        ["No upcoming fixtures found"],
        "Treat as a no-fixture day or verify date/timezone and league filters.",
    ),
    (
        "MISSING_FILE",
        ["FileNotFoundError", "Missing ", "No existe:"],
        "Identify the missing file and determine whether it should be generated, restored from snapshot, or treated as optional.",
    ),
    (
        "DEPENDENCY_INSTALL",
        ["pip install", "Could not find a version", "No matching distribution", "Failed building wheel"],
        "Pin/repair requirements and rerun the workflow after dependency resolution.",
    ),
    (
        "PYTHON_EXCEPTION",
        ["Traceback (most recent call last):", "ValueError:", "RuntimeError:"],
        "Inspect the Python traceback and add a narrow regression test for the failing path.",
    ),
]


@dataclass(frozen=True)
class Diagnosis:
    classification: str
    severity: str
    confidence: str
    suggested_action: str
    matched_patterns: list[str]
    evidence_lines: list[str]


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def gh_json(args: list[str]) -> dict:
    result = run_gh(args)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout or "{}")


def norm_line(line: str) -> str:
    line = re.sub(r"\x1b\[[0-9;]*m", "", line)
    line = re.sub(r"^.*?Z\s+", "", line)
    line = re.sub(r"^[^\t]+\t[^\t]+\t", "", line)
    return line.strip()


def failed_log(repo: str, run_id: str) -> str:
    result = run_gh(["run", "view", run_id, "--repo", repo, "--log-failed"])
    text = (result.stdout or "") + "\n" + (result.stderr or "")
    return text[-MAX_LOG_CHARS:]


def relevant_evidence(log_text: str, patterns: list[str]) -> list[str]:
    lines = []
    needles = [p.lower() for p in patterns]
    generic_needles = ["::error::", "traceback", "valueerror", "runtimeerror", "filenotfounderror", "process completed with exit code"]
    for raw_line in log_text.splitlines():
        clean = norm_line(raw_line)
        lower = clean.lower()
        if any(needle.lower() in lower for needle in needles) or any(needle in lower for needle in generic_needles):
            if clean and clean not in lines:
                lines.append(clean)
        if len(lines) >= MAX_EVIDENCE_LINES:
            break
    return lines


def classify(log_text: str) -> Diagnosis:
    lower_log = log_text.lower()
    for classification, patterns, action in CLASSIFICATION_PATTERNS:
        matched = [pattern for pattern in patterns if pattern.lower() in lower_log]
        if matched:
            return Diagnosis(
                classification=classification,
                severity="P1" if classification not in {"NO_UPCOMING_FIXTURES"} else "P3",
                confidence="HIGH" if len(matched) >= 2 else "MEDIUM",
                suggested_action=action,
                matched_patterns=matched,
                evidence_lines=relevant_evidence(log_text, patterns),
            )
    return Diagnosis(
        classification="UNKNOWN_WORKFLOW_FAILURE",
        severity="P1",
        confidence="LOW",
        suggested_action="Inspect failed workflow logs and add a new Failure Doctor classifier once the root cause is known.",
        matched_patterns=[],
        evidence_lines=relevant_evidence(log_text, []),
    )


def issue_title(run: dict, diagnosis: Diagnosis) -> str:
    run_id = str(run.get("databaseId") or run.get("id") or "unknown")
    name = str(run.get("displayTitle") or run.get("name") or "vSIGMA workflow")
    return f"vSIGMA Failure Doctor: {diagnosis.classification} in {name} run {run_id}"


def markdown_list(values: list[str]) -> str:
    if not values:
        return "- None captured."
    return "\n".join(f"- `{value}`" for value in values)


def jobs_table(run: dict) -> str:
    jobs = run.get("jobs") or []
    if not jobs:
        return "_No job metadata available._"
    rows = ["| job | status | conclusion |", "| --- | --- | --- |"]
    for job in jobs:
        rows.append(
            f"| {job.get('name', '')} | {job.get('status', '')} | {job.get('conclusion', '')} |"
        )
    return "\n".join(rows)


def build_issue_body(run: dict, diagnosis: Diagnosis, run_url: str) -> str:
    created_at = run.get("createdAt", "")
    updated_at = run.get("updatedAt", "")
    return "\n".join(
        [
            f"# vSIGMA Failure Doctor - {diagnosis.classification}",
            "",
            "## Diagnosis",
            f"- classification: {diagnosis.classification}",
            f"- severity: {diagnosis.severity}",
            f"- confidence: {diagnosis.confidence}",
            f"- suggested_action: {diagnosis.suggested_action}",
            f"- run_url: {run_url}",
            "",
            "## Run Metadata",
            f"- display_title: {run.get('displayTitle', '')}",
            f"- event: {run.get('event', '')}",
            f"- status: {run.get('status', '')}",
            f"- conclusion: {run.get('conclusion', '')}",
            f"- created_at: {created_at}",
            f"- updated_at: {updated_at}",
            f"- generated_at: {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Matched Patterns",
            markdown_list(diagnosis.matched_patterns),
            "",
            "## Evidence Lines",
            markdown_list(diagnosis.evidence_lines),
            "",
            "## Jobs",
            jobs_table(run),
            "",
            "## Guardrail",
            "This issue is diagnostic only. Do not change production model behavior from this issue without a separate PR, tests, and promotion/governance review.",
        ]
    )


def ensure_labels(repo: str, extra_labels: list[str]) -> None:
    for label in [*LABELS, *extra_labels]:
        run_gh(["label", "create", label, "--repo", repo, "--color", "BFDADC", "--description", "vSIGMA failure doctor"])


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
            return str(issue.get("url") or "")
    return ""


def create_issue(repo: str, title: str, body: str, labels: list[str], dry_run: bool) -> str:
    if dry_run:
        return "DRY_RUN"
    existing = existing_issue(repo, title)
    if existing:
        return existing
    ensure_labels(repo, labels)
    result = run_gh(["issue", "create", "--repo", repo, "--title", title, "--body", body, "--label", ",".join([*LABELS, *labels])])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def append_step_summary(diagnosis: Diagnosis, issue_url: str, run_url: str) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    lines = [
        "## vSIGMA Failure Doctor",
        f"- classification: {diagnosis.classification}",
        f"- severity: {diagnosis.severity}",
        f"- confidence: {diagnosis.confidence}",
        f"- run_url: {run_url}",
        f"- issue_url: {issue_url or 'N/A'}",
    ]
    Path(summary_path).open("a", encoding="utf-8").write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose failed vSIGMA workflow runs and optionally open an issue.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--dispatch", action="store_true", help="Create or reuse a GitHub issue for the diagnosis.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run = gh_json([
        "run",
        "view",
        args.run_id,
        "--repo",
        args.repo,
        "--json",
        "databaseId,status,conclusion,displayTitle,event,createdAt,updatedAt,url,jobs",
    ])
    run_url = str(run.get("url") or f"https://github.com/{args.repo}/actions/runs/{args.run_id}")
    log_text = failed_log(args.repo, args.run_id)
    diagnosis = classify(log_text)
    title = issue_title(run, diagnosis)
    body = build_issue_body(run, diagnosis, run_url)
    issue_url = ""
    if args.dispatch:
        issue_url = create_issue(
            args.repo,
            title,
            body,
            [f"failure:{diagnosis.classification.lower()}"],
            args.dry_run,
        )
    append_step_summary(diagnosis, issue_url, run_url)
    print("=== VSIGMA FAILURE DOCTOR ===")
    print(f"classification={diagnosis.classification}")
    print(f"severity={diagnosis.severity}")
    print(f"confidence={diagnosis.confidence}")
    print(f"run_url={run_url}")
    if issue_url:
        print(f"issue_url={issue_url}")
    print("suggested_action=" + diagnosis.suggested_action)


if __name__ == "__main__":
    main()
