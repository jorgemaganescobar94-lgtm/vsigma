from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
PERFORMANCE_COLUMNS = [
    "target_date",
    "generated_at",
    "experiment_id",
    "experiment_type",
    "source_pattern_key",
    "shadow_status",
    "baseline_policy",
    "candidate_policy",
    "matching_sample_count",
    "closed_sample_count",
    "wins",
    "losses",
    "voids",
    "unresolved",
    "baseline_decision_quality",
    "shadow_performance_status",
    "promotion_readiness",
    "recommended_next_step",
    "production_impact",
    "auto_apply",
    "guardrail_status",
]

QUALITY_GOOD_LABELS = {"ACTIONABLE_WIN", "NO_BET_CORRECT_AVOIDED_LOSS"}
QUALITY_BAD_LABELS = {"ACTIONABLE_LOSS", "NO_BET_MISSED_WIN", "WAIT_MISSED_WIN"}
MIN_CLOSED_SAMPLES = 30


@dataclass(frozen=True)
class ShadowPerformancePaths:
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
        writer = csv.DictWriter(handle, fieldnames=PERFORMANCE_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in PERFORMANCE_COLUMNS})


def load_experiments(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_shadow_experiments.csv"))
    rows.extend(read_csv_rows(processed_dir / "today" / target_date / "vsigma_shadow_experiments.csv"))
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = norm(row.get("experiment_id"))
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def load_learning_rows(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_learning_ledger_all.csv"))
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_learning_ledger.csv"))
    rows.extend(read_csv_rows(processed_dir / "today" / target_date / "vsigma_learning_ledger.csv"))
    seen: set[tuple[str, str, str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (
            norm(row.get("target_date")),
            norm(row.get("fixture_id")),
            upper(row.get("market_primary")),
            upper(row.get("official_action")),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def match_experiment_rows(experiment: dict[str, str], learning_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    pattern = upper(experiment.get("source_pattern_key"))
    if not pattern:
        return []
    parts = [part for part in pattern.split("::") if part]
    matches: list[dict[str, str]] = []
    for row in learning_rows:
        haystack = "::".join(
            [
                upper(row.get("sample_key")),
                upper(row.get("market_primary")),
                upper(row.get("accuracy_primary_risk")),
                upper(row.get("improvement_signal")),
                upper(row.get("learning_family")),
            ]
        )
        if all(part in haystack for part in parts):
            matches.append(row)
    return matches


def closed_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if upper(row.get("result_status")) in {"WIN", "LOSS", "VOID"}]


def baseline_quality(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "NO_CLOSED_SAMPLE"
    labels = Counter(upper(row.get("decision_quality_label")) for row in rows)
    good = sum(labels[label] for label in QUALITY_GOOD_LABELS)
    bad = sum(labels[label] for label in QUALITY_BAD_LABELS)
    if bad and bad >= good:
        return "BASELINE_WEAK_SIGNAL"
    if good and good > bad:
        return "BASELINE_POSITIVE_SIGNAL"
    return "BASELINE_MIXED_OR_UNKNOWN"


def promotion_readiness(closed_count: int, losses: int) -> tuple[str, str, str]:
    if closed_count < MIN_CLOSED_SAMPLES:
        return (
            "NOT_READY_SAMPLE_TOO_SMALL",
            "COLLECT_MORE_CLOSED_SAMPLES",
            f"Need at least {MIN_CLOSED_SAMPLES} closed matching samples before promotion review.",
        )
    if losses == 0:
        return (
            "REVIEW_READY_BUT_NO_AUTO_PROMOTION",
            "PROMOTION_GATE_REVIEW",
            "Sample threshold met; send to separate promotion gate. No automatic promotion here.",
        )
    return (
        "REVIEW_READY_REQUIRES_DEEP_AUDIT",
        "PROMOTION_GATE_REVIEW",
        "Sample threshold met but losses exist; requires drawdown/missed-winner audit before any promotion.",
    )


def build_performance_row(experiment: dict[str, str], learning_rows: list[dict[str, str]], target_date: str, generated_at: str) -> dict[str, object]:
    matches = match_experiment_rows(experiment, learning_rows)
    closed = closed_rows(matches)
    wins = sum(1 for row in closed if upper(row.get("result_status")) == "WIN")
    losses = sum(1 for row in closed if upper(row.get("result_status")) == "LOSS")
    voids = sum(1 for row in closed if upper(row.get("result_status")) == "VOID")
    unresolved = len(matches) - len(closed)
    readiness, next_step, recommended = promotion_readiness(len(closed), losses)
    quality = baseline_quality(closed)
    status = "TRACKING_ACTIVE_INSUFFICIENT_SAMPLE"
    if len(closed) >= MIN_CLOSED_SAMPLES:
        status = "TRACKING_READY_FOR_PROMOTION_GATE"
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "experiment_id": norm(experiment.get("experiment_id")),
        "experiment_type": upper(experiment.get("experiment_type")),
        "source_pattern_key": norm(experiment.get("source_pattern_key")),
        "shadow_status": upper(experiment.get("shadow_status")),
        "baseline_policy": norm(experiment.get("baseline_policy")),
        "candidate_policy": norm(experiment.get("candidate_policy")),
        "matching_sample_count": len(matches),
        "closed_sample_count": len(closed),
        "wins": wins,
        "losses": losses,
        "voids": voids,
        "unresolved": unresolved,
        "baseline_decision_quality": quality,
        "shadow_performance_status": status,
        "promotion_readiness": readiness,
        "recommended_next_step": f"{next_step}: {recommended}",
        "production_impact": "NONE",
        "auto_apply": "NO",
        "guardrail_status": "PERFORMANCE_TRACKING_ONLY_NO_PROMOTION",
    }


def build_shadow_performance(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], ShadowPerformancePaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    experiments = load_experiments(processed_dir, target_date)
    learning_rows = load_learning_rows(processed_dir, target_date)
    rows = [build_performance_row(experiment, learning_rows, target_date, generated_at) for experiment in experiments]
    paths = ShadowPerformancePaths(
        today_csv=today / "vsigma_shadow_performance.csv",
        today_md=today / "vsigma_shadow_performance.md",
        governance_csv=governance / "vsigma_shadow_performance.csv",
        governance_md=governance / "vsigma_shadow_performance.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Shadow Performance - {target_date}",
        "",
        "## Executive Shadow Performance Summary",
        f"- generated_at: {generated_at}",
        f"- experiments tracked: {len(rows)}",
        f"- performance_status_counts: {format_counter(counter(rows, 'shadow_performance_status'))}",
        f"- promotion_readiness_counts: {format_counter(counter(rows, 'promotion_readiness'))}",
        "",
        "## Experiment Tracking",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:20]:
            lines.append(
                f"- {row['shadow_performance_status']} | {row['experiment_type']} | "
                f"closed={row['closed_sample_count']} | wins={row['wins']} | losses={row['losses']} | "
                f"promotion={row['promotion_readiness']} | production_impact={row['production_impact']}"
            )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- production logic changed: NO",
            "- official picks changed: NO",
            "- promotion applied: NO",
            "- predictive formulas changed: NO",
            "- thresholds changed: NO",
            "- calibration changed: NO",
            "- ranking changed: NO",
            "- market-selection changed: NO",
            "- auto_apply: NO for every tracked experiment",
            "",
            "## Promotion Path",
            "- This tracker measures evidence only.",
            "- Promotion requires a separate promotion gate and enough closed matching samples.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track vSIGMA shadow experiment performance.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_shadow_performance(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA SHADOW PERFORMANCE ===")
    print(f"tracked={len(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
