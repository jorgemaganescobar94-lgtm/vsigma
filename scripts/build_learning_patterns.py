from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
PATTERN_COLUMNS = [
    "target_date",
    "generated_at",
    "pattern_id",
    "pattern_type",
    "pattern_key",
    "severity",
    "sample_count",
    "wins",
    "losses",
    "voids",
    "unresolved",
    "markets",
    "learning_families",
    "learning_statuses",
    "improvement_signals",
    "recommendation",
    "guardrail_status",
]


@dataclass(frozen=True)
class LearningPatternPaths:
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
        writer = csv.DictWriter(handle, fieldnames=PATTERN_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in PATTERN_COLUMNS})


def unique_join(values: list[str]) -> str:
    clean = sorted({value for value in values if value})
    return ";".join(clean) if clean else "UNKNOWN"


def count_result(rows: list[dict[str, str]], result: str) -> int:
    return sum(1 for row in rows if upper(row.get("result_status")) == result)


def count_unresolved(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if upper(row.get("result_status")) in {"", "UNRESOLVED", "UNKNOWN"})


def severity_for(pattern_type: str, sample_count: int, losses: int, unresolved: int) -> str:
    if pattern_type in {"DATA_BLOCKED_CLUSTER", "TECHNICAL_REVIEW_CLUSTER"} and sample_count >= 1:
        return "P1"
    if pattern_type in {"EXPIRED_PRELOCK_CLUSTER", "WAITING_PRELOCK_CLUSTER"} and sample_count >= 3:
        return "P1"
    if losses >= 3:
        return "P1"
    if sample_count >= 5 and unresolved >= max(3, sample_count // 2):
        return "P2"
    if sample_count >= 3:
        return "P2"
    return "P3"


def recommendation_for(pattern_type: str) -> str:
    recommendations = {
        "SAMPLE_KEY_CLUSTER": "Keep collecting evidence; repeated sample key can feed improvement proposal only after sufficient closed results.",
        "MARKET_RISK_CLUSTER": "Monitor market/risk concentration; do not adjust model until losses and sample size clear promotion gates.",
        "WAITING_PRELOCK_CLUSTER": "Review execution timing and retry windows if waiting persists.",
        "EXPIRED_PRELOCK_CLUSTER": "Review AUTO/PRELOCK timing; exclude expired rows from predictive accuracy metrics.",
        "DATA_BLOCKED_CLUSTER": "Inspect provider coverage, odds, lineups, and data freshness before changing model logic.",
        "TECHNICAL_REVIEW_CLUSTER": "Inspect workflow/reporting health before trusting learning sample.",
        "ACTIONABLE_LOSS_CLUSTER": "Potential model-risk pattern; keep in proposal-only state until shadow/backtest evidence exists.",
        "UNRESOLVED_DOMINANCE": "Improve post-results labeling and wait for closed samples before proposing model changes.",
    }
    return recommendations.get(pattern_type, "Monitor pattern; evidence only.")


def build_pattern(pattern_type: str, pattern_key: str, rows: list[dict[str, str]], target_date: str, generated_at: str) -> dict[str, object]:
    sample_count = len(rows)
    wins = count_result(rows, "WIN")
    losses = count_result(rows, "LOSS")
    voids = count_result(rows, "VOID")
    unresolved = count_unresolved(rows)
    markets = [upper(row.get("market_primary")) for row in rows]
    families = [upper(row.get("learning_family")) for row in rows]
    statuses = [upper(row.get("learning_status")) for row in rows]
    signals = [upper(row.get("improvement_signal")) for row in rows]
    pattern_id = f"{pattern_type}::{pattern_key}".replace(" ", "_")
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "pattern_id": pattern_id,
        "pattern_type": pattern_type,
        "pattern_key": pattern_key,
        "severity": severity_for(pattern_type, sample_count, losses, unresolved),
        "sample_count": sample_count,
        "wins": wins,
        "losses": losses,
        "voids": voids,
        "unresolved": unresolved,
        "markets": unique_join(markets),
        "learning_families": unique_join(families),
        "learning_statuses": unique_join(statuses),
        "improvement_signals": unique_join(signals),
        "recommendation": recommendation_for(pattern_type),
        "guardrail_status": "EVIDENCE_ONLY_NO_MODEL_CHANGE",
    }


def group_by(rows: list[dict[str, str]], key_fn) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = key_fn(row)
        if key:
            groups[key].append(row)
    return dict(groups)


def dedupe_patterns(patterns: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, object]] = []
    for pattern in patterns:
        key = (str(pattern.get("pattern_type")), str(pattern.get("pattern_key")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(pattern)
    severity_rank = {"P1": 0, "P2": 1, "P3": 2}
    return sorted(deduped, key=lambda row: (severity_rank.get(str(row.get("severity")), 9), -int(row.get("sample_count") or 0), str(row.get("pattern_id"))))


def mine_patterns(rows: list[dict[str, str]], target_date: str, generated_at: str) -> list[dict[str, object]]:
    patterns: list[dict[str, object]] = []
    if not rows:
        return patterns

    for sample_key, group in group_by(rows, lambda row: norm(row.get("sample_key"))).items():
        if len(group) >= 2:
            patterns.append(build_pattern("SAMPLE_KEY_CLUSTER", sample_key, group, target_date, generated_at))

    for market_risk, group in group_by(rows, lambda row: "::".join([upper(row.get("market_primary")) or "UNKNOWN_MARKET", upper(row.get("accuracy_primary_risk")) or "UNKNOWN_RISK"])).items():
        if len(group) >= 2:
            patterns.append(build_pattern("MARKET_RISK_CLUSTER", market_risk, group, target_date, generated_at))

    family_to_type = {
        "WAITING_PRELOCK": "WAITING_PRELOCK_CLUSTER",
        "EXPIRED_PRELOCK": "EXPIRED_PRELOCK_CLUSTER",
        "DATA_BLOCKED": "DATA_BLOCKED_CLUSTER",
        "TECHNICAL_REVIEW": "TECHNICAL_REVIEW_CLUSTER",
    }
    for family, pattern_type in family_to_type.items():
        group = [row for row in rows if upper(row.get("learning_family")) == family]
        if len(group) >= 1:
            patterns.append(build_pattern(pattern_type, family, group, target_date, generated_at))

    actionable_losses = [row for row in rows if upper(row.get("learning_family")) == "ACTIONABLE_RESULT" and upper(row.get("result_status")) == "LOSS"]
    if actionable_losses:
        for market, group in group_by(actionable_losses, lambda row: upper(row.get("market_primary")) or "UNKNOWN_MARKET").items():
            patterns.append(build_pattern("ACTIONABLE_LOSS_CLUSTER", market, group, target_date, generated_at))

    unresolved_rows = [row for row in rows if upper(row.get("result_status")) in {"", "UNRESOLVED", "UNKNOWN"}]
    if len(unresolved_rows) >= max(3, len(rows) // 2):
        patterns.append(build_pattern("UNRESOLVED_DOMINANCE", "UNRESOLVED_RESULTS", unresolved_rows, target_date, generated_at))

    return dedupe_patterns(patterns)


def load_learning_rows(processed_dir: Path, target_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_learning_ledger_all.csv"))
    rows.extend(read_csv_rows(processed_dir / "governance" / "vsigma_learning_ledger.csv"))
    rows.extend(read_csv_rows(processed_dir / "today" / target_date / "vsigma_learning_ledger.csv"))
    seen: set[tuple[str, str, str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (norm(row.get("target_date")), norm(row.get("fixture_id")), upper(row.get("market_primary")), upper(row.get("official_action")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def build_markdown(target_date: str, generated_at: str, patterns: list[dict[str, object]]) -> str:
    type_counts = Counter(str(pattern.get("pattern_type")) for pattern in patterns)
    severity_counts = Counter(str(pattern.get("severity")) for pattern in patterns)
    lines = [
        f"# vSIGMA Learning Patterns - {target_date}",
        "",
        "## Executive Pattern Summary",
        f"- generated_at: {generated_at}",
        f"- patterns detected: {len(patterns)}",
        f"- pattern_type_counts: {', '.join(f'{key}={value}' for key, value in type_counts.most_common()) if type_counts else 'none'}",
        f"- severity_counts: {', '.join(f'{key}={value}' for key, value in severity_counts.most_common()) if severity_counts else 'none'}",
        "",
        "## Top Patterns",
    ]
    if patterns:
        for pattern in patterns[:20]:
            lines.extend(
                [
                    f"- {pattern['severity']} | {pattern['pattern_type']} | {pattern['pattern_key']} | n={pattern['sample_count']} | recommendation={pattern['recommendation']}",
                ]
            )
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Learning Use",
            "- Pattern mining is evidence-only.",
            "- Repeated P1/P2 patterns should feed a future improvement proposal engine.",
            "- No model, threshold, calibration, ranking, or market-selection change is applied here.",
            "",
            "## Guardrails",
            "- predictive changes applied: NO",
            "- threshold changes applied: NO",
            "- calibration changes applied: NO",
            "- ranking changes applied: NO",
            "- market-selection changes applied: NO",
            "",
        ]
    )
    return "\n".join(lines)


def build_learning_patterns(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, object]], LearningPatternPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    rows = load_learning_rows(processed_dir, target_date)
    patterns = mine_patterns(rows, target_date, generated_at)
    paths = LearningPatternPaths(
        today_csv=today / "vsigma_learning_patterns.csv",
        today_md=today / "vsigma_learning_patterns.md",
        governance_csv=governance / "vsigma_learning_patterns.csv",
        governance_md=governance / "vsigma_learning_patterns.md",
    )
    markdown = build_markdown(target_date, generated_at, patterns)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, patterns)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return patterns, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mine vSIGMA learning ledger patterns.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    patterns, paths = build_learning_patterns(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA LEARNING PATTERNS ===")
    print(f"patterns={len(patterns)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
