from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date",
    "generated_at",
    "component",
    "sanity_status",
    "severity",
    "recommended_action",
    "rows_count",
    "fallback_rows",
    "guard_decision",
    "commit_allowed",
    "guard_reason",
    "source_guard",
    "auto_apply",
    "production_change",
]

BLOCK_STATUSES = {"EMPTY_WITH_VALID_FALLBACK"}
WARN_STATUSES = {"EMPTY_NO_FALLBACK", "EMPTY_BUT_NONCRITICAL_FALLBACK_EXISTS"}
CRITICAL_COMPONENTS = {
    "forecast_calibration_summary",
    "stat_calibration_governor",
    "calibration_shadow_patch_queue",
    "shadow_patch_promotion_readiness",
}


def n(value: object) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def evaluate(row: dict[str, str], day: str, generated_at: str) -> dict[str, object]:
    component = n(row.get("component"))
    status = n(row.get("sanity_status")) or "UNKNOWN"
    severity = n(row.get("severity")) or "UNKNOWN"
    action = n(row.get("recommended_action")) or "UNKNOWN"
    rows_count = n(row.get("rows_count")) or "0"
    fallback_rows = n(row.get("fallback_rows")) or "0"

    if component in CRITICAL_COMPONENTS and status in BLOCK_STATUSES:
        decision = "BLOCK_COMMIT_EMPTY_WITH_FALLBACK"
        allowed = "NO"
        reason = "Critical output is empty while same-date fallback exists; prevent committing degraded file."
    elif severity in {"ERROR", "CRITICAL"}:
        decision = "BLOCK_COMMIT_CRITICAL_SANITY"
        allowed = "NO"
        reason = "Critical sanity severity found; prevent commit until reviewed."
    elif status in WARN_STATUSES:
        decision = "WARN_ONLY"
        allowed = "YES"
        reason = "Non-blocking empty-output warning; keep workflow visible."
    else:
        decision = "PASS"
        allowed = "YES"
        reason = "No blocking empty-output condition."

    return {
        "target_date": day,
        "generated_at": generated_at,
        "component": component,
        "sanity_status": status,
        "severity": severity,
        "recommended_action": action,
        "rows_count": rows_count,
        "fallback_rows": fallback_rows,
        "guard_decision": decision,
        "commit_allowed": allowed,
        "guard_reason": reason,
        "source_guard": "EMPTY_OUTPUT_HARD_GUARD",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    sanity_rows = read_csv(dated(day, "vsigma_learning_chain_output_sanity.csv"))
    return [evaluate(row, day, generated_at) for row in sanity_rows]


def overall(rows: list[dict[str, object]]) -> tuple[str, str]:
    if any(row.get("commit_allowed") == "NO" for row in rows):
        return "BLOCK_COMMIT", "NO"
    if any(str(row.get("guard_decision")) == "WARN_ONLY" for row in rows):
        return "WARN", "YES"
    if rows:
        return "PASS", "YES"
    return "NO_SANITY_INPUT", "YES"


def md(day: str, rows: list[dict[str, object]]) -> str:
    status, allowed = overall(rows)
    lines = [
        f"# vSIGMA Learning Chain Empty Output Hard Guard - {day}",
        "",
        "## Summary",
        f"- guard_status: {status}",
        f"- commit_allowed: {allowed}",
        f"- rows_reviewed: {len(rows)}",
        f"- guard_decisions: {counts(rows, 'guard_decision')}",
        f"- auto_apply: NO",
        f"- production_change: NO",
        "",
        "## Component Guards",
    ]
    if not rows:
        lines.append("- none. Missing vsigma_learning_chain_output_sanity.csv.")
    for row in rows:
        lines.append(
            "- "
            f"{row['component']} | decision={row['guard_decision']} | commit_allowed={row['commit_allowed']} | "
            f"status={row['sanity_status']} | rows={row['rows_count']} | fallback_rows={row['fallback_rows']} | "
            f"reason={row['guard_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This guard does not modify model formulas or picks.",
        "- When --fail-on-block is used, BLOCK_COMMIT returns a non-zero exit code before the workflow commit step.",
        "- Blocks only critical empty outputs with valid same-date fallback or critical sanity severity.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, fail_on_block: bool) -> int:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_learning_chain_empty_output_guard.csv", rows)
        (base / "vsigma_learning_chain_empty_output_guard.md").write_text(md(day, rows), encoding="utf-8")
    status, allowed = overall(rows)
    print("=== VSIGMA LEARNING CHAIN EMPTY OUTPUT HARD GUARD ===")
    print(f"guard_status={status}")
    print(f"commit_allowed={allowed}")
    print(f"guard_decisions={counts(rows, 'guard_decision')}")
    print("auto_apply=NO")
    print("production_change=NO")
    if fail_on_block and allowed == "NO":
        return 2
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--fail-on-block", action="store_true")
    args = parser.parse_args()
    sys.exit(run(args.date, args.timezone, args.fail_on_block))


if __name__ == "__main__":
    main()
