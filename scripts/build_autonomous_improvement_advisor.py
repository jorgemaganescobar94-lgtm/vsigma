from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
FIELDS = ["target_date","generated_at","priority","area","status","evidence","recommendation","safe_auto_pr","auto_merge","source_guard"]
RANK = {"CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "INFO": 1}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def meta(text: str, key: str) -> str:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def add(rows: list[dict[str, str]], day: str, generated: str, priority: str, area: str, status: str, evidence: str, rec: str, safe_pr: str = "NO", merge: str = "NO") -> None:
    rows.append({
        "target_date": day,
        "generated_at": generated,
        "priority": priority,
        "area": area,
        "status": status,
        "evidence": evidence,
        "recommendation": rec,
        "safe_auto_pr": safe_pr,
        "auto_merge": merge,
        "source_guard": "DATED_INPUT_ONLY",
    })


def calibration_rows() -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(ROOT / "ledger" / "vsigma_stat_calibration_memory.csv"):
        grouped[row.get("metric", "")].append(row)
    return grouped


def add_calibration_findings(out: list[dict[str, str]], day: str, generated: str) -> None:
    for metric, rows in calibration_rows().items():
        if not metric: continue
        days = {r.get("target_date", "") for r in rows if r.get("target_date")}
        total = 0
        hits = []
        biases = []
        statuses = []
        for r in rows:
            try: total += int(float(r.get("rows_evaluated") or 0))
            except ValueError: pass
            try: hits.append(float(r.get("hit_rate") or 0))
            except ValueError: pass
            b = r.get("bias_direction", "")
            if b and b != "BALANCED_OR_ON_RANGE": biases.append(b)
            statuses.append(r.get("calibration_status", ""))
        avg_hit = sum(hits) / len(hits) if hits else 0
        dominant = Counter(biases).most_common(1)[0][0] if biases else "BALANCED_OR_ON_RANGE"
        evidence = f"days={len(days)}; total_rows={total}; avg_hit={avg_hit:.3f}; dominant_bias={dominant}; statuses={';'.join(statuses)}"
        if len(days) >= 2 and total >= 10 and dominant != "BALANCED_OR_ON_RANGE" and avg_hit < 0.55:
            add(out, day, generated, "HIGH", f"calibration/{metric}", "PATCH_CANDIDATE_REVIEW", evidence, "Open manual review for metric-specific formula adjustment. No auto-apply.")
        elif dominant != "BALANCED_OR_ON_RANGE":
            add(out, day, generated, "LOW", f"calibration/{metric}", "ACCUMULATE_MORE_SAMPLE", evidence, "Keep collecting evidence before formula changes.")


def build(day: str, tz: str) -> list[dict[str, str]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = ROOT / "today" / day
    out: list[dict[str, str]] = []
    operator = read(folder / "vsigma_operator_brief.md")
    health = read(folder / "vsigma_automation_health.md")
    issue = read(folder / "vsigma_issue_alert_status.md")

    if not operator:
        add(out, day, generated, "CRITICAL", "operator_brief", "MISSING", "vsigma_operator_brief.md missing", "Run operator brief workflow after daily chain.")
    else:
        op = meta(operator, "operator_status")
        active = meta(operator, "active_candidates")
        if meta(operator, "health_status") == "UNKNOWN":
            add(out, day, generated, "MEDIUM", "workflow_order", "OPERATOR_BEFORE_HEALTH", "operator brief health_status=UNKNOWN", "Schedule health monitor before operator brief.", "YES", "NO")
        if "## Blocked / Watch Only" in operator and operator.count("NO_BET_OR_WATCH") + operator.count("NO_BET |") > 8:
            add(out, day, generated, "MEDIUM", "operator_brief", "COMPACT_VIEW_CANDIDATE", "Blocked/Watch section remains long", "Implement compact grouped view: one fixture per line, split Watch Only and No Bet.", "YES", "NO")
        if op == "ACTION_REVIEW_NOW":
            add(out, day, generated, "HIGH", "operator_status", op, f"active_candidates={active}", "Review current live confirmation manually.")

    if health:
        hs = meta(health, "system_status")
        if hs == "BROKEN":
            add(out, day, generated, "CRITICAL", "health", "BROKEN", "health monitor reports BROKEN", "Fix broken component before using outputs.")
    else:
        add(out, day, generated, "MEDIUM", "health", "MISSING", "vsigma_automation_health.md missing", "Run health monitor before issue/brief workflows.", "YES", "NO")

    if issue and meta(issue, "notify_required") == "true":
        add(out, day, generated, "LOW", "issue_alert", "MATERIAL_ALERT_CHANGE", "notify_required=true", "Review vsigma-alert issue.")

    add_calibration_findings(out, day, generated)
    if not out:
        add(out, day, generated, "INFO", "advisor", "NO_ACTION", "no safe improvement candidates detected", "Keep monitoring.")
    return sorted(out, key=lambda r: RANK.get(r["priority"], 0), reverse=True)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)


def markdown(day: str, rows: list[dict[str, str]]) -> str:
    issue_required = any(RANK.get(r["priority"], 0) >= 3 for r in rows)
    top = rows[0]["priority"] if rows else "INFO"
    lines = [
        f"# vSIGMA Autonomous Improvement Advisor - {day}", "",
        "## Summary",
        f"- top_priority: {top}",
        f"- rows: {len(rows)}",
        f"- issue_required: {'YES' if issue_required else 'NO'}",
        "- auto_apply: NO",
        "- production_change: NO", "",
        "## Recommendations",
    ]
    for r in rows:
        lines.append(f"- {r['priority']} | {r['area']} | {r['status']} | evidence={r['evidence']} | recommendation={r['recommendation']} | safe_auto_pr={r['safe_auto_pr']} | auto_merge={r['auto_merge']}")
    lines += ["", "## Guardrails", "- Advisor proposes only; it does not change formulas, thresholds or stakes.", "- safe_auto_pr=YES is only for reporting/ops cleanup, never prediction logic.", "- auto_merge remains NO."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    body = markdown(day, rows)
    issue_required = any(RANK.get(r["priority"], 0) >= 3 for r in rows)
    title = f"[vSIGMA IMPROVEMENT] {day} - {rows[0]['priority'] if rows else 'INFO'}"
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write_csv(base / "vsigma_autonomous_improvement_advisor.csv", rows)
        write(base / "vsigma_autonomous_improvement_advisor.md", body)
        write(base / "vsigma_improvement_issue_required.txt", str(issue_required).lower() + "\n")
        write(base / "vsigma_improvement_issue_title.txt", title + "\n")
        write(base / "vsigma_improvement_issue_body.md", body)
    print(f"top_priority={rows[0]['priority'] if rows else 'INFO'}")
    print(f"issue_required={str(issue_required).lower()}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args(); run(a.date, a.timezone)


if __name__ == "__main__": main()
