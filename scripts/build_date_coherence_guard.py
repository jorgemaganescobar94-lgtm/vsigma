from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
TODAY = ROOT / "today"
GOVERNANCE = ROOT / "governance"
TRIGGERS = Path(".vsigma/triggers")

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "component",
    "path",
    "observed_date",
    "status",
    "detail",
    "auto_apply",
    "production_change",
]
SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "overall_status",
    "board_status",
    "mismatch_count",
    "missing_core_count",
    "trigger_date_counts",
    "next_action",
    "auto_apply",
    "production_change",
]

CORE_COMPONENTS = {
    "daily_board_md",
    "daily_board_csv",
    "operator_brief_md",
    "automation_health_md",
}


def s(value: object) -> str:
    return str(value or "").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def first_date_token(text: str) -> str:
    patterns = [
        r"#\s+[^\n]*-\s*(\d{4}-\d{2}-\d{2})",
        r"target_date\s*[:,=]\s*(\d{4}-\d{2}-\d{2})",
        r"date\s*[:,=]\s*(\d{4}-\d{2}-\d{2})",
        r"\b(20\d{2}-\d{2}-\d{2})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return "UNKNOWN"


def observed_date_for(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    if path.suffix.lower() == ".csv":
        rows = read_csv(path)
        if rows:
            for field in ["target_date", "date", "match_date"]:
                value = s(rows[0].get(field))
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    return value
        return "UNKNOWN"
    text = read_text(path)
    return first_date_token(text)


def trigger_date(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    for line in read_text(path).splitlines():
        if line.startswith("date="):
            value = line.split("=", 1)[1].strip()
            if value:
                return value
    return "UNKNOWN"


def classify_component(component: str, path: Path, observed: str, target: str) -> tuple[str, str]:
    if observed == "MISSING":
        if component in CORE_COMPONENTS:
            return "MISSING_CORE", "required daily artifact is missing"
        return "MISSING_OPTIONAL", "optional artifact not found"
    if observed == "UNKNOWN":
        return "DATE_UNKNOWN", "artifact exists but date could not be parsed"
    if observed != target:
        return "DATE_MISMATCH", f"observed {observed} != target {target}"
    return "OK", "date coherent"


def add_row(rows: list[dict[str, str]], day: str, generated: str, component: str, path: Path, observed: str, status: str, detail: str) -> None:
    rows.append(
        {
            "target_date": day,
            "generated_at": generated,
            "component": component,
            "path": str(path),
            "observed_date": observed,
            "status": status,
            "detail": detail,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    )


def build(day: str, tz: str) -> tuple[list[dict[str, str]], list[dict[str, str]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = TODAY / day

    components = [
        ("daily_board_md", folder / "vsigma_daily_execution_board.md", "artifact"),
        ("daily_board_csv", folder / "vsigma_daily_execution_board.csv", "artifact"),
        ("operator_brief_md", folder / "vsigma_operator_brief.md", "artifact"),
        ("automation_health_md", folder / "vsigma_automation_health.md", "artifact"),
        ("prelock_live_recheck_md", folder / "vsigma_prelock_live_recheck.md", "artifact"),
        ("live_trigger_validator_md", folder / "vsigma_live_trigger_validator.md", "artifact"),
        ("consolidated_panel_md", folder / "vsigma_consolidated_daily_operator_panel.md", "artifact"),
        ("source_reliability_governor_md", folder / "vsigma_probable_lineup_source_reliability_governor.md", "artifact"),
        ("daily_chain_trigger", TRIGGERS / "daily_decision_chain_v2.trigger", "trigger"),
        ("prelock_recheck_trigger", TRIGGERS / "prelock_official_lineup_recheck.trigger", "trigger"),
    ]

    rows: list[dict[str, str]] = []
    for component, path, kind in components:
        observed = trigger_date(path) if kind == "trigger" else observed_date_for(path)
        status, detail = classify_component(component, path, observed, day)
        add_row(rows, day, generated, component, path, observed, status, detail)

    counts = Counter(row["status"] for row in rows)
    board_statuses = {row["component"]: row["status"] for row in rows if row["component"] in {"daily_board_md", "daily_board_csv"}}
    board_missing = any(board_statuses.get(component) == "MISSING_CORE" for component in ["daily_board_md", "daily_board_csv"])
    mismatches = counts.get("DATE_MISMATCH", 0)
    missing_core = counts.get("MISSING_CORE", 0)
    unknowns = counts.get("DATE_UNKNOWN", 0)
    trigger_counts = Counter(row["observed_date"] for row in rows if row["component"].endswith("trigger"))

    if mismatches:
        overall = "DATE_MISMATCH_BLOCK"
        next_action = "Fix trigger/artifact date mismatch before using market signals."
    elif board_missing:
        overall = "MISSING_DAILY_BOARD"
        next_action = "Run daily decision chain for target date before using prelock/live/operator outputs."
    elif missing_core:
        overall = "PARTIAL_OUTPUTS"
        next_action = "Build missing core reports before market discussion."
    elif unknowns:
        overall = "DATE_UNKNOWN_REVIEW"
        next_action = "Review artifacts with unparseable dates before trusting outputs."
    else:
        overall = "OK"
        next_action = "All dated artifacts/triggers reviewed by guard are coherent."

    summary = [
        {
            "target_date": day,
            "generated_at": generated,
            "overall_status": overall,
            "board_status": "; ".join(f"{key}={value}" for key, value in board_statuses.items()) or "UNKNOWN",
            "mismatch_count": str(mismatches),
            "missing_core_count": str(missing_core),
            "trigger_date_counts": "; ".join(f"{key}={value}" for key, value in trigger_counts.items()) or "none",
            "next_action": next_action,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    ]

    markdown = md(day, rows, summary[0])
    return rows, summary, markdown


def md(day: str, rows: list[dict[str, str]], summary: dict[str, str]) -> str:
    lines = [
        f"# vSIGMA Date Coherence Guard - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- board_status: {summary['board_status']}",
        f"- mismatch_count: {summary['mismatch_count']}",
        f"- missing_core_count: {summary['missing_core_count']}",
        f"- trigger_date_counts: {summary['trigger_date_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Component Rows",
    ]
    for row in rows:
        lines.append(
            f"- {row['component']} | status={row['status']} | observed={row['observed_date']} | path={row['path']} | detail={row['detail']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Date mismatches block market interpretation until the daily chain is coherent.",
        "- Missing daily board blocks prelock/live/operator outputs from becoming pick permission.",
        "- This guard is diagnostic only and does not execute bets.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz)
    for base in [TODAY / day, GOVERNANCE]:
        write_csv(base / "vsigma_date_coherence_guard.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_date_coherence_guard_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_date_coherence_guard.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA DATE COHERENCE GUARD ===")
    print(f"overall_status={summary[0]['overall_status']}")
    print(f"board_status={summary[0]['board_status']}")
    print(f"mismatch_count={summary[0]['mismatch_count']}")
    print(f"missing_core_count={summary[0]['missing_core_count']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
