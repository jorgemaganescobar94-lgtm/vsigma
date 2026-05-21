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
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "final_recommendation",
    "baseline_status",
    "experiment_id",
    "experiment_type",
    "source_pattern_key",
    "shadow_decision",
    "shadow_reason",
    "baseline_policy",
    "candidate_policy",
    "production_impact",
    "auto_apply",
    "guardrail_status",
]

CANDIDATE_FILES = [
    "vsigma_today_prelock_competition_top.csv",
    "vsigma_today_execution_bets_only.csv",
    "vsigma_today_execution_shortlist.csv",
]


@dataclass(frozen=True)
class ShadowCandidatePaths:
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


def load_shadow_experiments(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    today = processed_dir / "today" / target_date / "vsigma_shadow_experiments.csv"
    governance = processed_dir / "governance" / "vsigma_shadow_experiments.csv"
    rows = read_csv_rows(today) or read_csv_rows(governance)
    return [row for row in rows if upper(row.get("shadow_status")) == "ACTIVE_SHADOW_ONLY"]


def load_candidates(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    today_dir = processed_dir / "today" / target_date
    rows: list[dict[str, str]] = []
    for filename in CANDIDATE_FILES:
        batch = read_csv_rows(today_dir / filename)
        if batch:
            rows.extend(batch)
            break
    if not rows:
        for filename in CANDIDATE_FILES:
            batch = read_csv_rows(processed_dir / filename)
            if batch:
                rows.extend(batch)
                break

    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (norm(row.get("fixture_id")), upper(row.get("market_primary")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def candidate_matches_experiment(candidate: dict[str, str], experiment: dict[str, str]) -> bool:
    pattern_key = upper(experiment.get("source_pattern_key"))
    market = upper(candidate.get("market_primary"))
    risk = upper(
        candidate.get("accuracy_primary_risk")
        or candidate.get("pick_primary_risk")
        or candidate.get("pick_failure_mode")
    )
    haystack = "::".join([
        market,
        risk,
        upper(candidate.get("pick_failure_mode")),
        upper(candidate.get("accuracy_mode_reason")),
    ])
    parts = [part for part in pattern_key.split("::") if part]
    if not parts:
        return False
    return all(part in haystack for part in parts)


def build_shadow_row(
    candidate: dict[str, str],
    experiment: dict[str, str],
    target_date: str,
    generated_at: str,
) -> dict[str, object]:
    market = upper(candidate.get("market_primary"))
    if "LOW_CONVERSION" in upper(experiment.get("experiment_type")):
        decision = "SHADOW_DOWNGRADE_REVIEW"
        reason = (
            "Candidate matches low-conversion shadow experiment; require stronger conversion evidence "
            "before premium treatment."
        )
    else:
        decision = "SHADOW_MONITOR_ONLY"
        reason = "Candidate matches active shadow experiment; monitor against baseline only."

    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "fixture_id": norm(candidate.get("fixture_id")),
        "home_team": norm(candidate.get("home_team")),
        "away_team": norm(candidate.get("away_team")),
        "market_primary": market,
        "final_recommendation": upper(candidate.get("final_recommendation")),
        "baseline_status": "OFFICIAL_BASELINE_UNCHANGED",
        "experiment_id": norm(experiment.get("experiment_id")),
        "experiment_type": upper(experiment.get("experiment_type")),
        "source_pattern_key": norm(experiment.get("source_pattern_key")),
        "shadow_decision": decision,
        "shadow_reason": reason,
        "baseline_policy": norm(experiment.get("baseline_policy")) or "CURRENT_PRODUCTION_LOGIC_UNCHANGED",
        "candidate_policy": norm(experiment.get("candidate_policy")),
        "production_impact": "NONE",
        "auto_apply": "NO",
        "guardrail_status": "SHADOW_CANDIDATE_ONLY_NO_PRODUCTION_CHANGE",
    }


def build_shadow_candidate_rows(
    target_date: str,
    generated_at: str,
    experiments: list[dict[str, str]],
    candidates: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        for experiment in experiments:
            if candidate_matches_experiment(candidate, experiment):
                rows.append(build_shadow_row(candidate, experiment, target_date, generated_at))
    return rows


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in values.most_common())


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Shadow Candidates - {target_date}",
        "",
        "## Executive Shadow Candidate Summary",
        f"- generated_at: {generated_at}",
        f"- shadow_candidates: {len(rows)}",
        f"- shadow_decision_counts: {format_counter(counter(rows, 'shadow_decision'))}",
        f"- experiment_type_counts: {format_counter(counter(rows, 'experiment_type'))}",
        "",
        "## Shadow Candidate Decisions",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:30]:
            lines.append(
                f"- {row['shadow_decision']} | {row['home_team']} vs {row['away_team']} | "
                f"market={row['market_primary']} | experiment={row['experiment_type']} | "
                f"production_impact={row['production_impact']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- official picks changed: NO",
        "- production logic changed: NO",
        "- auto_apply: NO",
        "- predictive formulas changed: NO",
        "- thresholds changed: NO",
        "- calibration changed: NO",
        "- ranking changed: NO",
        "- market-selection changed: NO",
        "",
    ])
    return "\n".join(lines)


def build_shadow_candidates(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], ShadowCandidatePaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")

    experiments = load_shadow_experiments(processed_dir, target_date)
    candidates = load_candidates(processed_dir, target_date)
    rows = build_shadow_candidate_rows(target_date, generated_at, experiments, candidates)

    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    paths = ShadowCandidatePaths(
        today_csv=today / "vsigma_shadow_candidates.csv",
        today_md=today / "vsigma_shadow_candidates.md",
        governance_csv=governance / "vsigma_shadow_candidates.csv",
        governance_md=governance / "vsigma_shadow_candidates.md",
    )

    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA shadow candidate decisions.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_shadow_candidates(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA SHADOW CANDIDATES ===")
    print(f"shadow_candidates={len(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
