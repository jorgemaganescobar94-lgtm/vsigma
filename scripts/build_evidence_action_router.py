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
    "route_rank",
    "source_cleaner_rank",
    "source_issue_type",
    "severity",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "cleaner_action",
    "route_decision",
    "route_reason",
    "gate_status",
    "earliest_safe_phase",
    "recommended_command",
    "auto_run",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class EvidenceActionRouterPaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def as_float(value: object) -> float | None:
    try:
        text = norm(value)
        if not text:
            return None
        return float(text)
    except ValueError:
        return None


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


def index_run_plan(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fixture_id = norm(row.get("fixture_id"))
        if fixture_id and fixture_id not in out:
            out[fixture_id] = row
    return out


def route_prelock(row: dict[str, str], plan_by_fixture: dict[str, dict[str, str]]) -> tuple[str, str, str, str]:
    fixture_id = norm(row.get("fixture_id"))
    plan = plan_by_fixture.get(fixture_id, {})
    if not plan:
        return (
            "PRELOCK_CONTEXT_MISSING",
            "No daily_run_plan row found for this fixture; operator must inspect timing before execution.",
            "MANUAL_TIMING_REVIEW",
            "prelock_context_review",
        )
    status = upper(plan.get("prelock_status"))
    minutes = as_float(plan.get("minutes_to_kickoff"))
    if status == "INSIDE_PRELOCK_WINDOW" or (minutes is not None and 0 <= minutes <= 90):
        return (
            "RUN_PRELOCK_NOW",
            "Fixture is inside the configured PRELOCK window or close enough for confirmation.",
            "TIME_GATE_OPEN",
            "prelock",
        )
    if minutes is not None and minutes > 90:
        return (
            "WAIT_FOR_PRELOCK_WINDOW",
            "Fixture is still outside the configured 90-minute PRELOCK window.",
            "TIME_GATE_CLOSED",
            f"prelock_window_start={norm(plan.get('prelock_window_start'))}",
        )
    if minutes is not None and minutes < 0:
        return (
            "PRELOCK_EXPIRED",
            "Kickoff has already passed; do not treat this as a predictive failure.",
            "TIME_GATE_EXPIRED",
            "post_or_no_action",
        )
    return (
        "WAIT_FOR_PRELOCK_WINDOW",
        "PRELOCK timing could not be fully resolved; wait or inspect manually.",
        "TIME_GATE_UNKNOWN",
        "prelock_manual_review",
    )


def route_action(row: dict[str, str], plan_by_fixture: dict[str, dict[str, str]]) -> tuple[str, str, str, str]:
    action = upper(row.get("cleaner_action"))
    if action == "PRELOCK_REBUILD":
        return route_prelock(row, plan_by_fixture)
    if action == "POST_RESULT_LABELING":
        return (
            "WAIT_FOR_POST_RESULTS",
            "Post-result labeling is only safe after matches are finished.",
            "POST_RESULTS_REQUIRED",
            "post",
        )
    if action == "REBUILD_LEARNING":
        return (
            "REBUILD_AFTER_POST",
            "Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.",
            "DEPENDENCY_WAIT_POST",
            "after_post_results",
        )
    return (
        "MANUAL_REVIEW",
        "Cleaner action is not known to the router.",
        "MANUAL_REVIEW_REQUIRED",
        "manual_review",
    )


def build_route_row(target_date: str, generated_at: str, row: dict[str, str], plan_by_fixture: dict[str, dict[str, str]]) -> dict[str, object]:
    decision, reason, gate, phase = route_action(row, plan_by_fixture)
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "route_rank": 0,
        "source_cleaner_rank": norm(row.get("cleaner_rank")),
        "source_issue_type": upper(row.get("source_issue_type")),
        "severity": upper(row.get("severity")) or "P3",
        "fixture_id": norm(row.get("fixture_id")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_primary": upper(row.get("market_primary")) or "UNKNOWN",
        "cleaner_action": upper(row.get("cleaner_action")),
        "route_decision": decision,
        "route_reason": reason,
        "gate_status": gate,
        "earliest_safe_phase": phase,
        "recommended_command": norm(row.get("recommended_command")),
        "auto_run": "NO",
        "production_change": "NO",
        "guardrail_status": "ACTION_ROUTER_PLAN_ONLY_NO_AUTO_EXECUTION",
    }


def build_rows(target_date: str, generated_at: str, processed_dir: Path) -> list[dict[str, object]]:
    cleaner_rows, _ = first_rows(processed_dir, target_date, "vsigma_evidence_cleaner.csv")
    run_plan_rows, _ = first_rows(processed_dir, target_date, "daily_run_plan.csv")
    plan_by_fixture = index_run_plan(run_plan_rows)
    routed = [build_route_row(target_date, generated_at, row, plan_by_fixture) for row in cleaner_rows]
    decision_rank = {
        "RUN_PRELOCK_NOW": 0,
        "WAIT_FOR_PRELOCK_WINDOW": 1,
        "WAIT_FOR_POST_RESULTS": 2,
        "REBUILD_AFTER_POST": 3,
        "PRELOCK_CONTEXT_MISSING": 4,
        "PRELOCK_EXPIRED": 5,
        "MANUAL_REVIEW": 6,
    }
    severity_rank = {"P1": 0, "P2": 1, "P3": 2}
    routed.sort(
        key=lambda row: (
            decision_rank.get(str(row.get("route_decision")), 99),
            severity_rank.get(str(row.get("severity")), 9),
            str(row.get("fixture_id")),
            str(row.get("source_cleaner_rank")),
        )
    )
    for idx, row in enumerate(routed, start=1):
        row["route_rank"] = idx
    return routed


def executive_status(rows: list[dict[str, object]]) -> str:
    decisions = {str(row.get("route_decision")) for row in rows}
    if "RUN_PRELOCK_NOW" in decisions:
        return "PRELOCK_ACTION_READY"
    if "WAIT_FOR_PRELOCK_WINDOW" in decisions:
        return "WAITING_FOR_PRELOCK_WINDOW"
    if "WAIT_FOR_POST_RESULTS" in decisions:
        return "POST_RESULTS_PENDING"
    if rows:
        return "ROUTED_REVIEW_ONLY"
    return "NO_CLEANER_ACTIONS"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Evidence Action Router - {target_date}",
        "",
        "## Executive Action Routing Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- routed_actions: {len(rows)}",
        f"- route_decision_counts: {fmt_counter(counter(rows, 'route_decision'))}",
        f"- gate_status_counts: {fmt_counter(counter(rows, 'gate_status'))}",
        "- auto_run: NO",
        "- production_change: NO",
        "",
        "## Routed Actions",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:40]:
            lines.append(
                f"- #{row['route_rank']} | {row['route_decision']} | fixture={row['fixture_id'] or 'N/A'} | "
                f"market={row['market_primary']} | gate={row['gate_status']} | phase={row['earliest_safe_phase']} | "
                f"command=`{row['recommended_command']}` | reason={row['route_reason']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- No command is auto-run by this router.",
        "- No production model behavior is changed.",
        "- The router only determines safe timing/order for future operator or automation steps.",
    ])
    return "\n".join(lines)


def build_evidence_action_router(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], EvidenceActionRouterPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_rows(target_date, generated_at, processed_dir)
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = EvidenceActionRouterPaths(
        today_csv=today / "vsigma_evidence_action_router.csv",
        today_md=today / "vsigma_evidence_action_router.md",
        governance_csv=governance / "vsigma_evidence_action_router.csv",
        governance_md=governance / "vsigma_evidence_action_router.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA evidence action router plan.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_evidence_action_router(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA EVIDENCE ACTION ROUTER ===")
    print(f"routed_actions={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
