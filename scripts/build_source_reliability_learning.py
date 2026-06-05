from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date",
    "generated_at",
    "source_name",
    "current_status",
    "current_reliability_score",
    "current_priority_weight",
    "sample_rows_total",
    "evaluated_rows_total",
    "promoted_rows_total",
    "learning_only_rows_total",
    "quarantine_rows_total",
    "parser_failure_rows_total",
    "weighted_avg_accuracy",
    "promotion_rate",
    "learning_coverage_rate",
    "parser_failure_rate",
    "sample_gate",
    "source_learning_status",
    "source_utility_signal",
    "recommended_registry_action",
    "recommended_weight_action",
    "manual_review_required",
    "learning_note",
    "source_window",
    "source_guard",
    "auto_apply",
    "production_change",
]

MIN_OBSERVE_SAMPLE = 10
MIN_SOFT_SIGNAL_SAMPLE = 30
MIN_STRONG_SIGNAL_SAMPLE = 75


def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default


def up(value: object) -> str:
    return norm(value).upper()


def as_float(value: object) -> float:
    text = norm(value)
    if not text or text.lower() == "nan":
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def as_int(value: object) -> int:
    return int(round(as_float(value)))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def first_existing(processed: Path, day: str, names: list[str]) -> Path | None:
    candidates: list[Path] = []
    for name in names:
        candidates.append(processed / "governance" / name)
        candidates.append(processed / "today" / day / name)
    for path in candidates:
        if path.exists():
            return path
    return None


def load_governor_rows(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(
        processed,
        day,
        [
            "vsigma_probable_lineup_source_reliability_governor.csv",
            "vsigma_source_reliability_governor.csv",
        ],
    )
    return read_csv(path) if path else []


def sample_gate(evaluated: int) -> str:
    if evaluated >= MIN_STRONG_SIGNAL_SAMPLE:
        return "STRONG_SAMPLE"
    if evaluated >= MIN_SOFT_SIGNAL_SAMPLE:
        return "SOFT_SIGNAL_SAMPLE"
    if evaluated >= MIN_OBSERVE_SAMPLE:
        return "OBSERVE_ONLY_SAMPLE"
    return "INSUFFICIENT_SAMPLE"


def rate(num: int, den: int) -> str:
    if den <= 0:
        return ""
    return f"{(num / den) * 100:.1f}%"


def score_float(value: float) -> str:
    return f"{value:.3f}"


def classify_source(
    evaluated: int,
    promoted: int,
    learning_only: int,
    parser_failures: int,
    weighted_accuracy: float,
    current_status: str,
) -> tuple[str, str, str, str, str, str]:
    gate = sample_gate(evaluated)
    if gate == "INSUFFICIENT_SAMPLE":
        return (
            gate,
            "HOLD_SAMPLE",
            "NO_WEIGHT_CHANGE",
            "KEEP_ACTIVE_COLLECT_MORE_DATA",
            "NO",
            "Sample below minimum; keep collecting before changing registry or weights.",
        )

    parser_rate = parser_failures / evaluated if evaluated else 0.0
    promotion_rate = promoted / evaluated if evaluated else 0.0
    learning_rate = learning_only / evaluated if evaluated else 0.0

    if gate == "OBSERVE_ONLY_SAMPLE":
        return (
            gate,
            "OBSERVE_ONLY",
            "NO_WEIGHT_CHANGE",
            "KEEP_ACTIVE_COLLECT_MORE_DATA",
            "NO",
            "Source has observable sample but not enough for registry movement.",
        )

    if weighted_accuracy >= 0.78 and parser_rate <= 0.10 and promotion_rate >= 0.20:
        return (
            gate,
            "POSITIVE_SOURCE_SIGNAL_CANDIDATE",
            "UPWEIGHT_CANDIDATE_REQUIRES_REVIEW",
            "KEEP_ACTIVE_REVIEW_FOR_PRIORITY_INCREASE",
            "YES",
            "Source shows high accuracy and useful promotion rate; require manual review and larger context before upweight.",
        )

    if weighted_accuracy <= 0.45 and parser_rate >= 0.25:
        return (
            gate,
            "NEGATIVE_SOURCE_SIGNAL_CANDIDATE",
            "DOWNWEIGHT_CANDIDATE_REQUIRES_REVIEW",
            "KEEP_ACTIVE_REVIEW_FOR_RESTRICTION",
            "YES",
            "Source has low accuracy and elevated parser failures; require causal review before restriction.",
        )

    if parser_rate >= 0.40:
        return (
            gate,
            "PARSER_RELIABILITY_REVIEW",
            "NO_WEIGHT_CHANGE_PARSER_REVIEW_FIRST",
            "KEEP_ACTIVE_FIX_PARSER_OR_MAPPING_FIRST",
            "YES",
            "Parser failure rate is high; do not downweight source until extraction quality is reviewed.",
        )

    if learning_rate > 0.0 and promotion_rate == 0.0:
        return (
            gate,
            "LEARNING_ONLY_SOURCE_SIGNAL",
            "NO_WEIGHT_CHANGE",
            "KEEP_ACTIVE_LEARNING_ONLY_REVIEW",
            "YES" if gate != "OBSERVE_ONLY_SAMPLE" else "NO",
            "Source contributes learning-only data but no promotions; review whether it should remain diagnostic/coverage-only.",
        )

    return (
        gate,
        "NEUTRAL_SOURCE_SIGNAL",
        "KEEP_CURRENT_WEIGHT",
        "KEEP_ACTIVE_COLLECT_MORE_DATA",
        "NO",
        "No strong reliability signal; keep current source settings and collect more samples.",
    )


def aggregate_sources(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = load_governor_rows(processed, day)
    if not rows:
        rows = [{
            "target_date": day,
            "source_name": "DIAGNOSTIC_NO_SOURCE_GOVERNOR",
            "current_status": "UNKNOWN",
            "current_reliability_score": "",
            "current_priority_weight": "",
            "evaluated_rows": "0",
            "promoted_rows": "0",
            "learning_only_rows": "0",
            "quarantine_rows": "0",
            "parser_failure_rows": "0",
            "avg_accuracy": "0.000",
        }]

    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        source = norm(row.get("source_name"), "UNKNOWN_SOURCE")
        by_source[source].append(row)

    out: list[dict[str, object]] = []
    for source, source_rows in sorted(by_source.items()):
        current_status = norm(source_rows[-1].get("current_status"), "UNKNOWN")
        current_reliability = norm(source_rows[-1].get("current_reliability_score"))
        current_weight = norm(source_rows[-1].get("current_priority_weight"))
        evaluated = sum(as_int(row.get("evaluated_rows")) for row in source_rows)
        promoted = sum(as_int(row.get("promoted_rows")) for row in source_rows)
        learning_only = sum(as_int(row.get("learning_only_rows")) for row in source_rows)
        quarantine = sum(as_int(row.get("quarantine_rows")) for row in source_rows)
        parser_failures = sum(as_int(row.get("parser_failure_rows")) for row in source_rows)
        accuracy_weighted_num = 0.0
        accuracy_weighted_den = 0
        for row in source_rows:
            row_eval = as_int(row.get("evaluated_rows"))
            if row_eval > 0:
                accuracy_weighted_num += as_float(row.get("avg_accuracy")) * row_eval
                accuracy_weighted_den += row_eval
        weighted_accuracy = accuracy_weighted_num / accuracy_weighted_den if accuracy_weighted_den else 0.0
        gate, status, weight_action, registry_action, manual, note = classify_source(
            evaluated,
            promoted,
            learning_only,
            parser_failures,
            weighted_accuracy,
            current_status,
        )
        out.append({
            "target_date": day,
            "generated_at": generated,
            "source_name": source,
            "current_status": current_status,
            "current_reliability_score": current_reliability,
            "current_priority_weight": current_weight,
            "sample_rows_total": len(source_rows),
            "evaluated_rows_total": evaluated,
            "promoted_rows_total": promoted,
            "learning_only_rows_total": learning_only,
            "quarantine_rows_total": quarantine,
            "parser_failure_rows_total": parser_failures,
            "weighted_avg_accuracy": score_float(weighted_accuracy),
            "promotion_rate": rate(promoted, evaluated),
            "learning_coverage_rate": rate(learning_only, evaluated),
            "parser_failure_rate": rate(parser_failures, evaluated),
            "sample_gate": gate,
            "source_learning_status": status,
            "source_utility_signal": status,
            "recommended_registry_action": registry_action,
            "recommended_weight_action": weight_action,
            "manual_review_required": manual,
            "learning_note": note,
            "source_window": "GOVERNANCE_CUMULATIVE_WITH_DAILY_FALLBACK",
            "source_guard": "SOURCE_RELIABILITY_LEARNING_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_source_reliability_learning_daily.csv", rows, FIELDS)
        (base / "vsigma_source_reliability_learning.md").write_text(markdown(day, rows), encoding="utf-8")
    hist = processed / "governance" / "vsigma_source_reliability_learning.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Source Reliability Learning - {day}",
        "",
        "## Summary",
        f"- source_rows: {len(rows)}",
        f"- sample_gate_counts: {fmt_counts(rows, 'sample_gate')}",
        f"- source_learning_status_counts: {fmt_counts(rows, 'source_learning_status')}",
        f"- recommended_weight_action_counts: {fmt_counts(rows, 'recommended_weight_action')}",
        f"- manual_review_required_counts: {fmt_counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Source Rows",
    ]
    for row in rows[:100]:
        lines.append(
            "- "
            f"{row.get('source_name', '')} | status={row.get('current_status', '')} | "
            f"eval={row.get('evaluated_rows_total', '')} promoted={row.get('promoted_rows_total', '')} learning={row.get('learning_only_rows_total', '')} | "
            f"avg={row.get('weighted_avg_accuracy', '')} | gate={row.get('sample_gate', '')} | "
            f"signal={row.get('source_learning_status', '')} | action={row.get('recommended_weight_action', '')} | "
            f"manual={row.get('manual_review_required', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This source learning report is advisory only and never edits source registry or weights.",
        "- Parser failures alone cannot downgrade a source; parser/mapping review comes first.",
        "- Upweight/downweight candidates require sufficient sample and manual confirmation.",
        "- No picks, stakes, production changes, or whitelist changes are created here.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = aggregate_sources(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA SOURCE RELIABILITY LEARNING ===")
    print(f"source_rows={len(rows)}")
    print(f"sample_gate_counts={fmt_counts(rows, 'sample_gate')}")
    print(f"source_learning_status_counts={fmt_counts(rows, 'source_learning_status')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
