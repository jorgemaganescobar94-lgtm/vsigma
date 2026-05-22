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
    "sequence_rank",
    "phase_order",
    "phase_name",
    "source_issue_type",
    "severity",
    "fixture_id",
    "market_primary",
    "sequence_state",
    "sequence_reason",
    "recommended_command",
    "can_run_now",
    "auto_run",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class EvidenceClosureSequencerPaths:
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


def first_rows(processed_dir: Path, target_date: str, filename: str) -> list[dict[str, str]]:
    today = processed_dir / "today" / target_date / filename
    governance = processed_dir / "governance" / filename
    rows = read_csv_rows(today)
    return rows if rows else read_csv_rows(governance)


def command_for(phase: str, target_date: str) -> str:
    if phase == "PRELOCK_CHECK":
        return f"gh workflow run vsigma_production.yml -f mode=prelock -f date=\"{target_date}\""
    if phase == "POST_RESULTS":
        return f"gh workflow run vsigma_production.yml -f mode=post -f date=\"{target_date}\""
    if phase == "LEARNING_REBUILD":
        return f"python scripts/build_learning_ledger.py --date {target_date} --timezone Atlantic/Canary"
    if phase == "QUALITY_REVIEW":
        return f"gh workflow run vsigma_data_quality_governor.yml -f date=\"{target_date}\""
    if phase == "READINESS_REVIEW":
        return f"gh workflow run vsigma_pattern_promotion_readiness.yml -f date=\"{target_date}\""
    return "manual_review_required"


def phase_for(issue_type: str, next_action: str) -> tuple[int, str, str, str, str]:
    issue = upper(issue_type)
    action = upper(next_action)
    if issue == "PRELOCK_OPEN_ITEM" or "PRELOCK" in action:
        return 1, "PRELOCK_CHECK", "WAIT_FOR_WINDOW_OR_OPERATOR", "Prelock/lineup timing must be checked before any serious execution.", "NO"
    if issue in {"OPEN_RESULT_STATUS", "MISSING_RESULT_FILE"} or "POST" in action:
        return 2, "POST_RESULTS", "WAIT_FOR_FIXTURES_FINISHED", "Post results can only run safely after matches are finished.", "NO"
    if issue in {"NO_SIGNAL", "UNKNOWN_RISK", "UNKNOWN_FAMILY", "DUPLICATE_LEARNING_ROW", "MISSING_IDENTITY"}:
        return 3, "LEARNING_REBUILD", "WAIT_FOR_POST_RESULTS", "Learning rebuild should happen after post-result labeling.", "NO"
    return 4, "MANUAL_REVIEW", "MANUAL_REVIEW_REQUIRED", "Issue type is not mapped to a safe sequence phase.", "NO"


def make_row(target_date: str, generated_at: str, source: dict[str, str]) -> dict[str, object]:
    phase_order, phase, state, reason, can_run_now = phase_for(source.get("issue_type", ""), source.get("next_action", ""))
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "sequence_rank": 0,
        "phase_order": phase_order,
        "phase_name": phase,
        "source_issue_type": upper(source.get("issue_type")),
        "severity": upper(source.get("severity")) or "P3",
        "fixture_id": norm(source.get("fixture_id")),
        "market_primary": upper(source.get("market_primary")) or "UNKNOWN",
        "sequence_state": state,
        "sequence_reason": reason,
        "recommended_command": command_for(phase, target_date),
        "can_run_now": can_run_now,
        "auto_run": "NO",
        "production_change": "NO",
        "guardrail_status": "EVIDENCE_CLOSURE_SEQUENCE_ONLY_NO_AUTO_RUN",
    }


def add_followup_phases(rows: list[dict[str, object]], target_date: str, generated_at: str) -> None:
    if any(row["phase_name"] == "LEARNING_REBUILD" for row in rows):
        rows.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "sequence_rank": 0,
            "phase_order": 4,
            "phase_name": "QUALITY_REVIEW",
            "source_issue_type": "FOLLOWUP",
            "severity": "P3",
            "fixture_id": "",
            "market_primary": "UNKNOWN",
            "sequence_state": "WAIT_FOR_LEARNING_REBUILD",
            "sequence_reason": "Quality review should be rerun after learning evidence is rebuilt.",
            "recommended_command": command_for("QUALITY_REVIEW", target_date),
            "can_run_now": "NO",
            "auto_run": "NO",
            "production_change": "NO",
            "guardrail_status": "EVIDENCE_CLOSURE_SEQUENCE_ONLY_NO_AUTO_RUN",
        })
        rows.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "sequence_rank": 0,
            "phase_order": 5,
            "phase_name": "READINESS_REVIEW",
            "source_issue_type": "FOLLOWUP",
            "severity": "P3",
            "fixture_id": "",
            "market_primary": "UNKNOWN",
            "sequence_state": "WAIT_FOR_QUALITY_REVIEW",
            "sequence_reason": "Readiness should be reviewed only after data quality is refreshed.",
            "recommended_command": command_for("READINESS_REVIEW", target_date),
            "can_run_now": "NO",
            "auto_run": "NO",
            "production_change": "NO",
            "guardrail_status": "EVIDENCE_CLOSURE_SEQUENCE_ONLY_NO_AUTO_RUN",
        })


def build_rows(target_date: str, generated_at: str, processed_dir: Path) -> list[dict[str, object]]:
    closer_rows = first_rows(processed_dir, target_date, "vsigma_learning_evidence_closer.csv")
    rows = [make_row(target_date, generated_at, row) for row in closer_rows]
    add_followup_phases(rows, target_date, generated_at)
    seen: set[tuple[object, ...]] = set()
    deduped: list[dict[str, object]] = []
    for row in rows:
        key = (row["phase_name"], row["source_issue_type"], row["fixture_id"], row["market_primary"], row["recommended_command"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    severity_rank = {"P1": 0, "P2": 1, "P3": 2}
    deduped.sort(key=lambda item: (int(item["phase_order"]), severity_rank.get(str(item["severity"]), 9), str(item["fixture_id"]), str(item["source_issue_type"])))
    for idx, row in enumerate(deduped, start=1):
        row["sequence_rank"] = idx
    return deduped


def executive_status(rows: list[dict[str, object]]) -> str:
    phases = {str(row.get("phase_name")) for row in rows}
    if "PRELOCK_CHECK" in phases:
        return "PRELOCK_FIRST"
    if "POST_RESULTS" in phases:
        return "POST_RESULTS_FIRST"
    if "LEARNING_REBUILD" in phases:
        return "LEARNING_REBUILD_PENDING"
    return "NO_SEQUENCE_ACTIONS" if not rows else "MANUAL_REVIEW"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Evidence Closure Sequencer - {target_date}",
        "",
        "## Executive Sequence Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- sequence_items: {len(rows)}",
        f"- phase_counts: {fmt_counter(counter(rows, 'phase_name'))}",
        f"- can_run_now_counts: {fmt_counter(counter(rows, 'can_run_now'))}",
        "- auto_run: NO",
        "- production_change: NO",
        "",
        "## Safe Sequence",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:60]:
            lines.append(
                f"- #{row['sequence_rank']} | phase={row['phase_name']} | state={row['sequence_state']} | "
                f"fixture={row['fixture_id'] or 'N/A'} | market={row['market_primary']} | command=`{row['recommended_command']}` | reason={row['sequence_reason']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- This sequencer does not run commands.",
        "- It only orders safe phases for operator or future controlled automation.",
        "- Correct order: PRELOCK when timed, POST after fixtures, rebuild learning, rerun quality/readiness.",
    ])
    return "\n".join(lines)


def build_evidence_closure_sequencer(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], EvidenceClosureSequencerPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_rows(target_date, generated_at, processed_dir)
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = EvidenceClosureSequencerPaths(
        today_csv=today / "vsigma_evidence_closure_sequencer.csv",
        today_md=today / "vsigma_evidence_closure_sequencer.md",
        governance_csv=governance / "vsigma_evidence_closure_sequencer.csv",
        governance_md=governance / "vsigma_evidence_closure_sequencer.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA evidence closure sequence report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_evidence_closure_sequencer(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA EVIDENCE CLOSURE SEQUENCER ===")
    print(f"sequence_items={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
