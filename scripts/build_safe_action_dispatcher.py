from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_PROCESSED_DIR = Path("data/processed")
OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "dispatch_rank",
    "route_rank",
    "route_decision",
    "gate_status",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "dispatch_status",
    "dispatch_allowed",
    "dispatch_reason",
    "manual_command",
    "safe_execution_phase",
    "auto_run",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class SafeActionDispatcherPaths:
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
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in OUTPUT_COLUMNS})


def first_rows(processed_dir: Path, target_date: str, filename: str) -> tuple[list[dict[str, str]], Path]:
    today = processed_dir / "today" / target_date / filename
    governance = processed_dir / "governance" / filename
    rows = read_csv_rows(today)
    if rows:
        return rows, today
    return read_csv_rows(governance), governance


def dispatch_status_for(route_decision: str) -> tuple[str, str, str, str]:
    decision = upper(route_decision)
    if decision == "RUN_PRELOCK_NOW":
        return (
            "READY_FOR_MANUAL_PRELOCK_DISPATCH",
            "MANUAL_ONLY",
            "Route is ready, but dispatcher is report-only; operator must launch prelock manually.",
            "prelock",
        )
    if decision == "WAIT_FOR_PRELOCK_WINDOW":
        return (
            "WAIT_TIME_GATE",
            "NO",
            "PRELOCK time gate is not open yet.",
            "wait_prelock_window",
        )
    if decision == "WAIT_FOR_POST_RESULTS":
        return (
            "WAIT_POST_RESULTS",
            "NO",
            "Post-result command is not safe until fixtures are finished.",
            "post_results",
        )
    if decision == "REBUILD_AFTER_POST":
        return (
            "WAIT_POST_DEPENDENCY",
            "NO",
            "Learning rebuild depends on post-result labeling first.",
            "after_post_results",
        )
    if decision == "PRELOCK_EXPIRED":
        return (
            "NO_DISPATCH_EXPIRED",
            "NO",
            "Prelock opportunity has expired; do not execute as if it were live.",
            "expired_review",
        )
    if decision == "PRELOCK_CONTEXT_MISSING":
        return (
            "MANUAL_TIMING_REVIEW_REQUIRED",
            "NO",
            "Daily run plan lacks timing context; operator must inspect before dispatch.",
            "manual_timing_review",
        )
    return (
        "MANUAL_REVIEW_REQUIRED",
        "NO",
        "Unknown route decision; manual review required.",
        "manual_review",
    )


def build_dispatch_row(target_date: str, generated_at: str, row: dict[str, str]) -> dict[str, object]:
    status, allowed, reason, phase = dispatch_status_for(row.get("route_decision", ""))
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "dispatch_rank": 0,
        "route_rank": norm(row.get("route_rank")),
        "route_decision": upper(row.get("route_decision")),
        "gate_status": upper(row.get("gate_status")),
        "fixture_id": norm(row.get("fixture_id")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_primary": upper(row.get("market_primary")) or "UNKNOWN",
        "dispatch_status": status,
        "dispatch_allowed": allowed,
        "dispatch_reason": reason,
        "manual_command": norm(row.get("recommended_command")),
        "safe_execution_phase": phase,
        "auto_run": "NO",
        "production_change": "NO",
        "guardrail_status": "SAFE_ACTION_DISPATCHER_REPORT_ONLY_NO_AUTO_RUN",
    }


def build_rows(target_date: str, generated_at: str, processed_dir: Path) -> list[dict[str, object]]:
    router_rows, _ = first_rows(processed_dir, target_date, "vsigma_evidence_action_router.csv")
    rows = [build_dispatch_row(target_date, generated_at, row) for row in router_rows]
    status_rank = {
        "READY_FOR_MANUAL_PRELOCK_DISPATCH": 0,
        "WAIT_TIME_GATE": 1,
        "WAIT_POST_RESULTS": 2,
        "WAIT_POST_DEPENDENCY": 3,
        "MANUAL_TIMING_REVIEW_REQUIRED": 4,
        "NO_DISPATCH_EXPIRED": 5,
        "MANUAL_REVIEW_REQUIRED": 6,
    }
    rows.sort(key=lambda row: (status_rank.get(str(row.get("dispatch_status")), 99), str(row.get("fixture_id")), str(row.get("route_rank"))))
    for idx, row in enumerate(rows, start=1):
        row["dispatch_rank"] = idx
    return rows


def executive_status(rows: list[dict[str, object]]) -> str:
    statuses = {str(row.get("dispatch_status")) for row in rows}
    if "READY_FOR_MANUAL_PRELOCK_DISPATCH" in statuses:
        return "MANUAL_PRELOCK_READY"
    if "WAIT_TIME_GATE" in statuses:
        return "WAITING_FOR_PRELOCK_WINDOW"
    if "WAIT_POST_RESULTS" in statuses:
        return "WAITING_FOR_POST_RESULTS"
    if rows:
        return "DISPATCH_REVIEW_ONLY"
    return "NO_DISPATCH_ACTIONS"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Safe Action Dispatcher - {target_date}",
        "",
        "## Executive Dispatcher Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- dispatch_actions: {len(rows)}",
        f"- dispatch_status_counts: {fmt_counter(counter(rows, 'dispatch_status'))}",
        f"- dispatch_allowed_counts: {fmt_counter(counter(rows, 'dispatch_allowed'))}",
        "- auto_run: NO",
        "- production_change: NO",
        "",
        "## Dispatch Queue",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:40]:
            lines.append(
                f"- #{row['dispatch_rank']} | {row['dispatch_status']} | allowed={row['dispatch_allowed']} | "
                f"fixture={row['fixture_id'] or 'N/A'} | market={row['market_primary']} | "
                f"phase={row['safe_execution_phase']} | command=`{row['manual_command']}` | reason={row['dispatch_reason']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- This dispatcher never auto-runs commands.",
        "- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.",
        "- NO means the command is blocked by timing, dependency, missing context, or safety state.",
        "- No production model behavior is changed.",
    ])
    return "\n".join(lines)


def build_safe_action_dispatcher(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], SafeActionDispatcherPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_rows(target_date, generated_at, processed_dir)
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = SafeActionDispatcherPaths(
        today_csv=today / "vsigma_safe_action_dispatcher.csv",
        today_md=today / "vsigma_safe_action_dispatcher.md",
        governance_csv=governance / "vsigma_safe_action_dispatcher.csv",
        governance_md=governance / "vsigma_safe_action_dispatcher.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA safe action dispatcher report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_safe_action_dispatcher(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA SAFE ACTION DISPATCHER ===")
    print(f"dispatch_actions={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
