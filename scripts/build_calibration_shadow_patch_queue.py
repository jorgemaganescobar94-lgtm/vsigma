from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
LEDGER_PATH = PROCESSED / "ledger" / "vsigma_stat_calibration_memory.csv"

FIELDS = [
    "target_date",
    "generated_at",
    "metric",
    "rows_evaluated",
    "hit_rate",
    "avg_abs_error_mid",
    "bias_direction",
    "calibration_status",
    "queue_decision",
    "shadow_priority",
    "sample_gate",
    "threshold_gate",
    "patch_candidate",
    "shadow_test_plan",
    "promotion_gate",
    "model_area",
    "operator_note",
    "auto_apply_allowed",
    "source_guard",
    "auto_apply",
    "production_change",
]

MIN_SAMPLE_FOR_PATCH = 10
MIN_SAMPLE_FOR_SHADOW = 8
MIN_SAMPLE_FOR_WATCH = 5
MIN_HIT_RATE_WEAK = 0.65
MIN_HIT_RATE_CRITICAL = 0.55
ERR_HIGH_BY_METRIC = {
    "total_goals": 0.85,
    "total_corners": 2.50,
    "total_cards": 1.75,
    "total_shots": 4.75,
    "total_sot": 2.00,
    "total_fouls": 6.50,
}
ERR_MED_BY_METRIC = {
    "total_goals": 0.70,
    "total_corners": 2.00,
    "total_cards": 1.50,
    "total_shots": 4.00,
    "total_sot": 1.75,
    "total_fouls": 5.50,
}


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


def metric_area(metric: str) -> str:
    return {
        "total_goals": "build_match_stat_forecasts.goal_model",
        "total_corners": "build_match_stat_forecasts.corner_model",
        "total_cards": "build_match_stat_forecasts.card_model",
        "total_shots": "build_match_stat_forecasts.shot_volume_model",
        "total_sot": "build_match_stat_forecasts.sot_model",
        "total_fouls": "build_match_stat_forecasts.foul_model",
    }.get(metric, f"build_match_stat_forecasts.{metric}")


def patch_text(metric: str, bias: str) -> str:
    direction = "down" if bias == "OVER_ESTIMATE" else "up" if bias == "UNDER_ESTIMATE" else "hold"
    if metric == "total_goals" and direction == "down":
        return "Shadow reduce goal-pressure weight 3-5% and tighten upper goal range only for matching high-error profiles."
    if metric == "total_goals" and direction == "up":
        return "Shadow raise goal floor only when SoT + big-chance support confirms under-projection."
    if metric == "total_corners" and direction == "down":
        return "Shadow reduce corner high-range cap by 1 and lower shot-to-corner conversion for high-tempo profiles."
    if metric == "total_corners" and direction == "up":
        return "Shadow raise corner range only for wide-pressure profiles with repeated corner support."
    if metric == "total_fouls" and direction == "down":
        return "Shadow reduce foul baseline and cap foul inflation from urgency/context until referee data confirms."
    if metric == "total_fouls" and direction == "up":
        return "Shadow raise foul baseline only for high-contact leagues with actual foul sample support."
    if metric == "total_cards" and direction == "down":
        return "Shadow reduce card baseline for low-card league/ref profiles."
    if metric == "total_cards" and direction == "up":
        return "Shadow raise cards baseline only when fouls and urgency both confirm."
    if metric == "total_shots" and direction == "down":
        return "Shadow reduce shot-volume expansion from tempo and remove broad high-range inflation."
    if metric == "total_shots" and direction == "up":
        return "Shadow raise shot floor only where pressure and possession translate into attempts."
    if metric == "total_sot" and direction == "down":
        return "Shadow reduce SoT conversion from raw shots where chance quality is weak."
    if metric == "total_sot" and direction == "up":
        return "Shadow raise SoT conversion only where shot quality and box entries are strong."
    return "Hold formula; monitor until the signal is directional and sample-safe."


def source_rows(day: str) -> tuple[list[dict[str, str]], str, str]:
    """Prefer same-day summary, then same-day ledger fallback.

    GitHub post-match refresh can occasionally return an empty same-day summary after a
    prior non-empty calibration. The ledger preserves the last valid dated rows, so use it
    as a same-date fallback instead of writing an empty shadow queue.
    """
    summary_path = dated(day, "vsigma_match_stat_forecast_calibration_summary.csv")
    summary_rows = read_csv(summary_path)
    if summary_rows:
        return summary_rows, "DATED_SUMMARY", str(summary_path)

    ledger_rows = [row for row in read_csv(LEDGER_PATH) if n(row.get("target_date")) == day]
    if ledger_rows:
        return ledger_rows, "LEDGER_DATED_FALLBACK", str(LEDGER_PATH)

    return [], "EMPTY_SOURCE", str(summary_path)


def evaluate_row(row: dict[str, str], source_guard: str) -> dict[str, str]:
    metric = n(row.get("metric"))
    rows_eval = i(row.get("rows_evaluated"))
    hit_rate = f(row.get("hit_rate"))
    avg_error = f(row.get("avg_abs_error_mid"))
    bias = n(row.get("bias_direction")) or "UNKNOWN"
    status = n(row.get("calibration_status")) or "UNKNOWN"
    err_high = ERR_HIGH_BY_METRIC.get(metric, 3.0)
    err_med = ERR_MED_BY_METRIC.get(metric, max(0.0, err_high * 0.8))

    if rows_eval < MIN_SAMPLE_FOR_WATCH:
        sample_gate = "LOW_SAMPLE"
    elif rows_eval < MIN_SAMPLE_FOR_SHADOW:
        sample_gate = "WATCH_SAMPLE"
    elif rows_eval < MIN_SAMPLE_FOR_PATCH:
        sample_gate = "SHADOW_SAMPLE"
    else:
        sample_gate = "PATCH_SAMPLE"

    if status == "CALIBRATION_OK" and hit_rate >= MIN_HIT_RATE_WEAK:
        threshold_gate = "STABLE"
    elif hit_rate < MIN_HIT_RATE_CRITICAL or avg_error >= err_high:
        threshold_gate = "CRITICAL_SIGNAL"
    elif hit_rate < MIN_HIT_RATE_WEAK or avg_error >= err_med:
        threshold_gate = "WEAK_SIGNAL"
    else:
        threshold_gate = "MONITOR_SIGNAL"

    if sample_gate == "LOW_SAMPLE":
        queue_decision = "REJECT_LOW_SAMPLE"
        priority = "NONE"
        note = "Sample below minimum watch threshold; no patch candidate."
    elif threshold_gate == "STABLE":
        queue_decision = "NO_PATCH_STABLE"
        priority = "NONE"
        note = "Metric is currently stable enough; keep monitoring."
    elif sample_gate in {"WATCH_SAMPLE", "SHADOW_SAMPLE"} and threshold_gate in {"WEAK_SIGNAL", "CRITICAL_SIGNAL"}:
        queue_decision = "PROMOTE_TO_SHADOW_TEST"
        priority = "HIGH" if threshold_gate == "CRITICAL_SIGNAL" else "MEDIUM"
        note = "Signal is strong enough for shadow testing, not production tuning."
    elif sample_gate == "PATCH_SAMPLE" and threshold_gate in {"WEAK_SIGNAL", "CRITICAL_SIGNAL"}:
        queue_decision = "PATCH_CANDIDATE"
        priority = "HIGH" if threshold_gate == "CRITICAL_SIGNAL" else "MEDIUM"
        note = "Candidate can enter shadow patch queue; production change remains blocked."
    else:
        queue_decision = "WAIT_MORE_SAMPLE"
        priority = "LOW"
        note = "Calibration signal exists but is not decisive enough."

    patch = patch_text(metric, bias) if queue_decision in {"PATCH_CANDIDATE", "PROMOTE_TO_SHADOW_TEST", "WAIT_MORE_SAMPLE"} else "NONE"
    shadow_plan = (
        f"Run next 3-5 post-match days comparing baseline vs proposed {metric} adjustment; require hit-rate uplift and no new metric damage."
        if queue_decision in {"PATCH_CANDIDATE", "PROMOTE_TO_SHADOW_TEST"}
        else "NONE"
    )
    promotion_gate = (
        "Promote only after sample>=20, two consecutive days without regression, and manual review."
        if queue_decision in {"PATCH_CANDIDATE", "PROMOTE_TO_SHADOW_TEST"}
        else "No promotion path."
    )

    return {
        "metric": metric,
        "rows_evaluated": rows_eval,
        "hit_rate": f"{hit_rate:.3f}",
        "avg_abs_error_mid": f"{avg_error:.2f}",
        "bias_direction": bias,
        "calibration_status": status,
        "queue_decision": queue_decision,
        "shadow_priority": priority,
        "sample_gate": sample_gate,
        "threshold_gate": threshold_gate,
        "patch_candidate": patch,
        "shadow_test_plan": shadow_plan,
        "promotion_gate": promotion_gate,
        "model_area": metric_area(metric),
        "operator_note": note,
        "auto_apply_allowed": "NO",
        "source_guard": source_guard,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str) -> tuple[list[dict[str, object]], str, str]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    input_rows, source_guard, source_path = source_rows(day)
    out: list[dict[str, object]] = []
    for source_row in input_rows:
        row = evaluate_row(source_row, source_guard)
        row["target_date"] = day
        row["generated_at"] = generated_at
        out.append(row)
    return out, source_guard, source_path


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]], source_guard: str, source_path: str) -> str:
    lines = [
        f"# vSIGMA Calibration Shadow Patch Queue - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- queue_decisions: {counts(rows, 'queue_decision')}",
        f"- shadow_priorities: {counts(rows, 'shadow_priority')}",
        f"- threshold_gates: {counts(rows, 'threshold_gate')}",
        f"- input_source_guard: {source_guard}",
        f"- input_source_path: {source_path}",
        "- auto_apply_allowed: NO",
        "- production_change: NO",
        "",
        "## Queue",
    ]
    if not rows:
        lines.append("- none. Need calibration summary or same-date calibration memory ledger rows first.")
    for row in rows:
        lines.append(
            "- "
            f"{row['metric']} | decision={row['queue_decision']} | priority={row['shadow_priority']} | "
            f"sample={row['rows_evaluated']} | hit_rate={row['hit_rate']} | err={row['avg_abs_error_mid']} | "
            f"bias={row['bias_direction']} | threshold={row['threshold_gate']} | source={row['source_guard']} | patch={row['patch_candidate']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Shadow patch queue is advisory only; it does not edit forecast formulas.",
        "- No production change is allowed from this script.",
        "- Ledger fallback is same-date only and exists only to avoid empty-refresh downgrades.",
        "- Promotion requires larger sample, consecutive non-regression, and manual review.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, source_guard, source_path = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_calibration_shadow_patch_queue.csv", rows)
        (base / "vsigma_calibration_shadow_patch_queue.md").write_text(md(day, rows, source_guard, source_path), encoding="utf-8")
    print("=== VSIGMA CALIBRATION SHADOW PATCH QUEUE ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"queue_decisions={counts(rows, 'queue_decision')}")
    print(f"shadow_priorities={counts(rows, 'shadow_priority')}")
    print(f"input_source_guard={source_guard}")
    print(f"input_source_path={source_path}")
    print("auto_apply_allowed=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
