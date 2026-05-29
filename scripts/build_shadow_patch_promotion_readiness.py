from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
LEDGER_PATH = PROCESSED / "ledger" / "vsigma_stat_calibration_memory.csv"

FIELDS = [
    "target_date",
    "generated_at",
    "metric",
    "current_queue_decision",
    "current_shadow_priority",
    "current_rows_evaluated",
    "current_hit_rate",
    "current_avg_abs_error_mid",
    "current_bias_direction",
    "current_threshold_gate",
    "history_days",
    "history_latest_rows",
    "history_bias_consistency",
    "history_status_consistency",
    "history_avg_hit_rate",
    "history_avg_error",
    "readiness_decision",
    "readiness_priority",
    "manual_review_required",
    "readiness_reason",
    "promotion_gate",
    "source_guard",
    "auto_apply",
    "production_change",
]

MIN_HISTORY_DAYS = 3
MIN_PROMOTION_SAMPLE = 20
MIN_HISTORY_BIAS_CONSISTENCY = 0.67
MIN_HISTORY_STATUS_CONSISTENCY = 0.67


def n(value: object) -> str:
    return "" if value is None else str(value).strip()


def f(value: object, default: float = 0.0) -> float:
    try:
        text = n(value)
        if not text or text.lower() == "nan":
            return default
        return float(text)
    except ValueError:
        return default


def i(value: object, default: int = 0) -> int:
    try:
        return int(float(n(value)))
    except ValueError:
        return default


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


def queue_rows(day: str) -> tuple[list[dict[str, str]], str]:
    path = dated(day, "vsigma_calibration_shadow_patch_queue.csv")
    rows = read_csv(path)
    if rows:
        return rows, str(path)
    path = PROCESSED / "governance" / "vsigma_calibration_shadow_patch_queue.csv"
    return read_csv(path), str(path)


def history_by_metric() -> dict[str, list[dict[str, str]]]:
    by_metric: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(LEDGER_PATH):
        metric = n(row.get("metric"))
        if metric:
            by_metric[metric].append(row)
    for metric in by_metric:
        by_metric[metric].sort(key=lambda r: (n(r.get("target_date")), n(r.get("generated_at"))))
    return by_metric


def consistency(rows: list[dict[str, str]], field: str, value: str) -> float:
    if not rows:
        return 0.0
    hits = sum(1 for row in rows if n(row.get(field)) == value)
    return hits / len(rows)


def avg(rows: list[dict[str, str]], field: str) -> float:
    if not rows:
        return 0.0
    return sum(f(row.get(field)) for row in rows) / len(rows)


def recent_unique_days(rows: list[dict[str, str]], limit: int = 5) -> list[dict[str, str]]:
    by_day: dict[str, dict[str, str]] = {}
    for row in rows:
        day = n(row.get("target_date"))
        if day:
            by_day[day] = row
    return [by_day[day] for day in sorted(by_day.keys())[-limit:]]


def evaluate(row: dict[str, str], hist_rows: list[dict[str, str]]) -> dict[str, object]:
    metric = n(row.get("metric"))
    queue_decision = n(row.get("queue_decision")) or "UNKNOWN"
    shadow_priority = n(row.get("shadow_priority")) or "UNKNOWN"
    current_rows = i(row.get("rows_evaluated"))
    current_hit = f(row.get("hit_rate"))
    current_err = f(row.get("avg_abs_error_mid"))
    current_bias = n(row.get("bias_direction")) or "UNKNOWN"
    current_threshold = n(row.get("threshold_gate")) or "UNKNOWN"

    recent = recent_unique_days(hist_rows, limit=5)
    hist_days = len(recent)
    latest_rows = max([i(r.get("rows_evaluated")) for r in recent], default=0)
    bias_consistency = consistency(recent, "bias_direction", current_bias)
    status_consistency = consistency(recent, "calibration_status", n(row.get("calibration_status")))
    avg_hit = avg(recent, "hit_rate")
    avg_error = avg(recent, "avg_abs_error_mid")

    if queue_decision == "NO_PATCH_STABLE":
        decision = "NO_PROMOTION_STABLE"
        priority = "NONE"
        manual = "NO"
        reason = "Current queue is stable; no promotion path."
    elif queue_decision in {"REJECT_LOW_SAMPLE", "WAIT_MORE_SAMPLE"}:
        decision = "WAIT_MORE_SAMPLE"
        priority = "LOW"
        manual = "NO"
        reason = "Current queue is not strong enough for promotion review."
    elif hist_days < MIN_HISTORY_DAYS:
        decision = "KEEP_SHADOW_TEST"
        priority = "MEDIUM" if shadow_priority == "HIGH" else "LOW"
        manual = "NO"
        reason = "Need more historical days before promotion review."
    elif bias_consistency < MIN_HISTORY_BIAS_CONSISTENCY:
        decision = "KEEP_SHADOW_TEST"
        priority = "MEDIUM"
        manual = "NO"
        reason = "Bias signal is not consistent enough across recent history."
    elif status_consistency < MIN_HISTORY_STATUS_CONSISTENCY:
        decision = "KEEP_SHADOW_TEST"
        priority = "MEDIUM"
        manual = "NO"
        reason = "Calibration status is not consistent enough across recent history."
    elif latest_rows < MIN_PROMOTION_SAMPLE or current_rows < MIN_PROMOTION_SAMPLE:
        decision = "KEEP_SHADOW_TEST"
        priority = "HIGH" if shadow_priority == "HIGH" else "MEDIUM"
        manual = "NO"
        reason = "Signal is consistent but sample is still below manual-promotion threshold."
    elif queue_decision == "PATCH_CANDIDATE":
        decision = "PROMOTION_CANDIDATE_MANUAL_REVIEW"
        priority = "HIGH"
        manual = "YES"
        reason = "Sample and consistency gates are met; manual review required before any production change."
    else:
        decision = "KEEP_SHADOW_TEST"
        priority = "HIGH" if shadow_priority == "HIGH" else "MEDIUM"
        manual = "NO"
        reason = "Shadow signal remains active but promotion is not allowed yet."

    promotion_gate = (
        "Manual promotion requires sample>=20, stable bias/status across recent days, no cross-metric regression, and explicit human approval."
        if decision in {"KEEP_SHADOW_TEST", "PROMOTION_CANDIDATE_MANUAL_REVIEW"}
        else "No promotion gate active."
    )

    return {
        "metric": metric,
        "current_queue_decision": queue_decision,
        "current_shadow_priority": shadow_priority,
        "current_rows_evaluated": current_rows,
        "current_hit_rate": f"{current_hit:.3f}",
        "current_avg_abs_error_mid": f"{current_err:.2f}",
        "current_bias_direction": current_bias,
        "current_threshold_gate": current_threshold,
        "history_days": hist_days,
        "history_latest_rows": latest_rows,
        "history_bias_consistency": f"{bias_consistency:.3f}",
        "history_status_consistency": f"{status_consistency:.3f}",
        "history_avg_hit_rate": f"{avg_hit:.3f}",
        "history_avg_error": f"{avg_error:.2f}",
        "readiness_decision": decision,
        "readiness_priority": priority,
        "manual_review_required": manual,
        "readiness_reason": reason,
        "promotion_gate": promotion_gate,
        "source_guard": "SHADOW_QUEUE_PLUS_LEDGER_HISTORY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str) -> tuple[list[dict[str, object]], str]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source_path = queue_rows(day)
    history = history_by_metric()
    out: list[dict[str, object]] = []
    for row in rows:
        evaluated = evaluate(row, history.get(n(row.get("metric")), []))
        evaluated["target_date"] = day
        evaluated["generated_at"] = generated_at
        out.append(evaluated)
    return out, source_path


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]], source_path: str) -> str:
    lines = [
        f"# vSIGMA Shadow Patch Promotion Readiness - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- readiness_decisions: {counts(rows, 'readiness_decision')}",
        f"- readiness_priorities: {counts(rows, 'readiness_priority')}",
        f"- manual_review_required: {counts(rows, 'manual_review_required')}",
        f"- input_source_path: {source_path}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Readiness Queue",
    ]
    if not rows:
        lines.append("- none. Need vsigma_calibration_shadow_patch_queue.csv first.")
    for row in rows:
        lines.append(
            "- "
            f"{row['metric']} | decision={row['readiness_decision']} | priority={row['readiness_priority']} | "
            f"manual_review={row['manual_review_required']} | current={row['current_queue_decision']} | "
            f"history_days={row['history_days']} | latest_rows={row['history_latest_rows']} | "
            f"bias_consistency={row['history_bias_consistency']} | status_consistency={row['history_status_consistency']} | "
            f"reason={row['readiness_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Promotion readiness is advisory only.",
        "- No production change is allowed from this script.",
        "- PROMOTION_CANDIDATE_MANUAL_REVIEW still requires explicit human approval.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, source_path = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_shadow_patch_promotion_readiness.csv", rows)
        (base / "vsigma_shadow_patch_promotion_readiness.md").write_text(md(day, rows, source_path), encoding="utf-8")
    print("=== VSIGMA SHADOW PATCH PROMOTION READINESS ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"readiness_decisions={counts(rows, 'readiness_decision')}")
    print(f"manual_review_required={counts(rows, 'manual_review_required')}")
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
