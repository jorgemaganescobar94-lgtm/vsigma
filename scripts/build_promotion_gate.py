from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
MIN_CLOSED_SAMPLES = 30
GATE_COLUMNS = [
    "target_date",
    "generated_at",
    "experiment_id",
    "experiment_type",
    "source_pattern_key",
    "closed_sample_count",
    "wins",
    "losses",
    "voids",
    "baseline_decision_quality",
    "shadow_performance_status",
    "promotion_readiness",
    "promotion_decision",
    "decision_reason",
    "auto_promote",
    "production_change",
    "required_next_step",
    "guardrail_status",
]


@dataclass(frozen=True)
class PromotionGatePaths:
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
        writer = csv.DictWriter(handle, fieldnames=GATE_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in GATE_COLUMNS})


def as_int(value: object) -> int:
    try:
        return int(float(norm(value) or 0))
    except ValueError:
        return 0


def decision_for(row: dict[str, str]) -> tuple[str, str, str]:
    closed = as_int(row.get("closed_sample_count"))
    wins = as_int(row.get("wins"))
    losses = as_int(row.get("losses"))
    readiness = upper(row.get("promotion_readiness"))
    quality = upper(row.get("baseline_decision_quality"))

    if closed < MIN_CLOSED_SAMPLES or readiness == "NOT_READY_SAMPLE_TOO_SMALL":
        return (
            "NOT_READY_SAMPLE_TOO_SMALL",
            f"Only {closed} closed matching samples; minimum required is {MIN_CLOSED_SAMPLES}.",
            "COLLECT_MORE_CLOSED_SAMPLES",
        )

    if losses > wins:
        return (
            "REJECTED_WEAK_SIGNAL",
            "Losses exceed wins in matching closed sample.",
            "KEEP_SHADOW_OR_REJECT",
        )

    if quality == "BASELINE_WEAK_SIGNAL" and losses > 0:
        return (
            "REJECTED_WEAK_SIGNAL",
            "Baseline quality is weak and losses are present; do not promote.",
            "DEEP_AUDIT_REQUIRED",
        )

    if closed >= MIN_CLOSED_SAMPLES and wins >= losses:
        return (
            "PROMOTION_CANDIDATE_REVIEW_ONLY",
            "Sample threshold met and signal is not negative; send to human/review gate only.",
            "HUMAN_REVIEW_OR_SEPARATE_PROMOTION_PR",
        )

    return (
        "READY_FOR_REVIEW",
        "Evidence is reviewable but not promotable automatically.",
        "PROMOTION_GATE_REVIEW",
    )


def build_gate_row(row: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    decision, reason, next_step = decision_for(row)
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "experiment_id": norm(row.get("experiment_id")),
        "experiment_type": upper(row.get("experiment_type")),
        "source_pattern_key": norm(row.get("source_pattern_key")),
        "closed_sample_count": as_int(row.get("closed_sample_count")),
        "wins": as_int(row.get("wins")),
        "losses": as_int(row.get("losses")),
        "voids": as_int(row.get("voids")),
        "baseline_decision_quality": upper(row.get("baseline_decision_quality")),
        "shadow_performance_status": upper(row.get("shadow_performance_status")),
        "promotion_readiness": upper(row.get("promotion_readiness")),
        "promotion_decision": decision,
        "decision_reason": reason,
        "auto_promote": "NO",
        "production_change": "NO",
        "required_next_step": next_step,
        "guardrail_status": "PROMOTION_GATE_REVIEW_ONLY_NO_AUTO_CHANGE",
    }


def load_shadow_performance(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_shadow_performance.csv"))
    rows.extend(read_csv_rows(processed_dir / "today" / target_date / "vsigma_shadow_performance.csv"))
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = norm(row.get("experiment_id"))
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Promotion Gate - {target_date}",
        "",
        "## Executive Gate Summary",
        f"- generated_at: {generated_at}",
        f"- experiments reviewed: {len(rows)}",
        f"- promotion_decision_counts: {format_counter(counter(rows, 'promotion_decision'))}",
        f"- auto_promote_counts: {format_counter(counter(rows, 'auto_promote'))}",
        "",
        "## Gate Decisions",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:20]:
            lines.append(
                f"- {row['promotion_decision']} | {row['experiment_type']} | "
                f"closed={row['closed_sample_count']} | wins={row['wins']} | losses={row['losses']} | "
                f"auto_promote={row['auto_promote']} | production_change={row['production_change']} | "
                f"next={row['required_next_step']}"
            )

    lines.extend(
        [
            "",
            "## Guardrails",
            "- auto_promote: NO for every gate decision",
            "- production_change: NO for every gate decision",
            "- official picks changed: NO",
            "- predictive formulas changed: NO",
            "- thresholds changed: NO",
            "- calibration changed: NO",
            "- ranking changed: NO",
            "- market-selection changed: NO",
            "",
            "## Policy",
            "- This gate can classify evidence but cannot apply promotion.",
            "- Any promotion requires a separate reviewed PR and sufficient closed matching samples.",
            "",
        ]
    )
    return "\n".join(lines)


def build_promotion_gate(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], PromotionGatePaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    performance_rows = load_shadow_performance(processed_dir, target_date)
    gate_rows = [build_gate_row(row, target_date, generated_at) for row in performance_rows]

    paths = PromotionGatePaths(
        today_csv=today / "vsigma_promotion_gate.csv",
        today_md=today / "vsigma_promotion_gate.md",
        governance_csv=governance / "vsigma_promotion_gate.csv",
        governance_md=governance / "vsigma_promotion_gate.md",
    )

    markdown = build_markdown(target_date, generated_at, gate_rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, gate_rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return gate_rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA review decisions from shadow performance.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_promotion_gate(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA REVIEW DECISION GATE ===")
    print(f"reviewed={len(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
