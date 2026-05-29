from __future__ import annotations

import argparse
import csv
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
ALLOWED_AREAS = ("operator_brief", "workflow_order", "health", "automation_health", "issue_alert")
BLOCKED_AREAS = ("calibration", "goal", "corner", "shot", "sot", "stake", "market", "odds", "prediction", "translator", "live_trigger")
PRIORITY_RANK = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO": 0}
FIELDS = ["target_date", "generated_at", "priority", "area", "status", "evidence", "recommendation", "safe_auto_pr", "auto_merge", "pr_action"]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:50] or "safe-pr"


def is_allowed(row: dict[str, str]) -> bool:
    area = (row.get("area") or "").lower()
    priority = row.get("priority", "INFO").upper()
    if row.get("safe_auto_pr", "NO").upper() != "YES":
        return False
    if row.get("auto_merge", "NO").upper() == "YES":
        return False
    if PRIORITY_RANK.get(priority, 0) < PRIORITY_RANK["MEDIUM"]:
        return False
    if any(blocked in area for blocked in BLOCKED_AREAS):
        return False
    return any(area.startswith(allowed) for allowed in ALLOWED_AREAS)


def load_advisor_rows(day: str) -> list[dict[str, str]]:
    today = ROOT / "today" / day / "vsigma_autonomous_improvement_advisor.csv"
    governance = ROOT / "governance" / "vsigma_autonomous_improvement_advisor.csv"
    return read_csv(today) or read_csv(governance)


def build(day: str, tz: str) -> tuple[list[dict[str, str]], str, str, str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    candidates = [r for r in load_advisor_rows(day) if is_allowed(r)]
    out: list[dict[str, str]] = []
    for r in candidates:
        out.append({
            "target_date": day,
            "generated_at": generated,
            "priority": r.get("priority", "MEDIUM"),
            "area": r.get("area", ""),
            "status": r.get("status", ""),
            "evidence": r.get("evidence", ""),
            "recommendation": r.get("recommendation", ""),
            "safe_auto_pr": "YES",
            "auto_merge": "NO",
            "pr_action": "CREATE_REVIEW_ONLY_PR_PLAN",
        })
    top = out[0]["priority"] if out else "INFO"
    title = f"[vSIGMA SAFE PR] {day} - {top} reporting/ops improvements"
    branch = f"vsigma-safe-auto-pr-{day}-{slug(out[0]['area']) if out else 'none'}"
    body = markdown(day, out, title)
    return out, title, branch, body


def markdown(day: str, rows: list[dict[str, str]], title: str) -> str:
    lines = [
        f"# {title}", "",
        "## Summary",
        f"- target_date: {day}",
        f"- safe_candidates: {len(rows)}",
        "- auto_merge: NO",
        "- production_change: NO", "",
        "## Allowed Scope",
        "- Reporting/brief cleanup",
        "- Workflow ordering/diagnostics",
        "- Health/issue reporting",
        "", "## Forbidden Scope",
        "- Prediction formulas",
        "- Stake logic",
        "- Market selection",
        "- Odds/price thresholds",
        "- Calibration auto-apply",
        "", "## Candidate Improvements",
    ]
    if not rows:
        lines.append("- none")
    for r in rows:
        lines.append(f"- {r['priority']} | {r['area']} | {r['status']} | evidence={r['evidence']} | recommendation={r['recommendation']}")
    lines += ["", "## Review Instructions", "- This PR is review-only.", "- Do not merge if it changes prediction, stake, market or calibration logic.", "- If the proposal is accepted, implement in a separate reviewed commit/PR unless the patch is purely reporting/formatting."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, title, branch, body = build(day, tz)
    required = bool(rows)
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write_csv(base / "vsigma_safe_auto_pr_plan.csv", rows)
        write(base / "vsigma_safe_auto_pr_plan.md", body)
        write(base / "vsigma_safe_auto_pr_required.txt", str(required).lower() + "\n")
        write(base / "vsigma_safe_auto_pr_title.txt", title + "\n")
        write(base / "vsigma_safe_auto_pr_branch.txt", branch + "\n")
        write(base / "vsigma_safe_auto_pr_body.md", body)
    print(f"safe_auto_pr_required={str(required).lower()}")
    print(f"title={title}")
    print(f"branch={branch}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args(); run(a.date, a.timezone)


if __name__ == "__main__":
    main()
