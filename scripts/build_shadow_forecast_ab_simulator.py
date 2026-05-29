from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
METRICS = ["total_goals", "total_corners", "total_fouls", "total_shots", "total_sot", "total_cards"]

DETAIL_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "metric",
    "actual_value", "baseline_mid", "shadow_mid", "baseline_abs_error", "shadow_abs_error",
    "error_delta", "shadow_result", "shadow_rule", "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "metric", "rows_evaluated", "baseline_avg_error",
    "shadow_avg_error", "avg_error_delta", "improved_rows", "worsened_rows", "unchanged_rows",
    "shadow_verdict", "shadow_rule", "source_guard", "auto_apply", "production_change",
]


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def queue_rows(day: str) -> list[dict[str, str]]:
    rows = read_csv(dated(day, "vsigma_calibration_shadow_patch_queue.csv"))
    if rows:
        return rows
    return read_csv(PROCESSED / "governance" / "vsigma_calibration_shadow_patch_queue.csv")


def active_rules(day: str) -> dict[str, tuple[str, str]]:
    rules: dict[str, tuple[str, str]] = {}
    for row in queue_rows(day):
        metric = n(row.get("metric"))
        decision = n(row.get("queue_decision"))
        if metric and decision in {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"}:
            rules[metric] = (n(row.get("bias_direction")) or "UNKNOWN", n(row.get("patch_candidate")) or "SHADOW_RULE")
    return rules


def apply_shadow(metric: str, baseline_mid: float, bias: str) -> tuple[float, str]:
    direction = "down" if bias == "OVER_ESTIMATE" else "up" if bias == "UNDER_ESTIMATE" else "hold"
    if direction == "hold":
        return baseline_mid, "HOLD_NO_DIRECTION"
    sign = -1 if direction == "down" else 1
    if metric == "total_goals":
        return max(0.0, baseline_mid * (0.95 if sign < 0 else 1.05)), "GOAL_PRESSURE_5PCT_SHADOW"
    if metric == "total_corners":
        return max(0.0, baseline_mid + sign * 1.0), "CORNER_MID_SHIFT_1_SHADOW"
    if metric == "total_fouls":
        return max(0.0, baseline_mid * (0.90 if sign < 0 else 1.10)), "FOUL_BASELINE_10PCT_SHADOW"
    if metric == "total_shots":
        return max(0.0, baseline_mid * (0.95 if sign < 0 else 1.05)), "SHOT_VOLUME_5PCT_SHADOW"
    if metric == "total_sot":
        return max(0.0, baseline_mid + sign * 0.5), "SOT_MID_SHIFT_0_5_SHADOW"
    if metric == "total_cards":
        return max(0.0, baseline_mid + sign * 0.5), "CARD_MID_SHIFT_0_5_SHADOW"
    return baseline_mid, "UNKNOWN_METRIC_HOLD"


def details_from_calibration(day: str) -> list[dict[str, str]]:
    rows = read_csv(dated(day, "vsigma_match_stat_forecast_calibration_details.csv"))
    return [row for row in rows if n(row.get("metric")) in METRICS and n(row.get("actual_value"))]


def details_from_forecasts_and_actuals(day: str) -> list[dict[str, str]]:
    forecasts = read_csv(dated(day, "vsigma_match_stat_forecasts.csv"))
    actuals = {n(row.get("fixture_id")): row for row in read_csv(dated(day, "vsigma_post_match_stat_actuals.csv")) if n(row.get("fixture_id"))}
    out: list[dict[str, str]] = []
    for forecast in forecasts:
        fixture_id = n(forecast.get("fixture_id"))
        actual = actuals.get(fixture_id)
        if not actual:
            continue
        for metric in METRICS:
            pred_col = f"{metric}_mid"
            actual_col = f"actual_{metric}"
            if pred_col not in forecast or actual_col not in actual:
                continue
            if not n(forecast.get(pred_col)) or not n(actual.get(actual_col)):
                continue
            out.append({
                "fixture_id": fixture_id,
                "home_team": n(forecast.get("home_team")) or n(actual.get("home_team")),
                "away_team": n(forecast.get("away_team")) or n(actual.get("away_team")),
                "metric": metric,
                "actual_value": n(actual.get(actual_col)),
                "pred_mid": n(forecast.get(pred_col)),
            })
    return out


def source_details(day: str) -> tuple[list[dict[str, str]], str]:
    calibration = details_from_calibration(day)
    if calibration:
        return calibration, "CALIBRATION_DETAILS"
    joined = details_from_forecasts_and_actuals(day)
    if joined:
        return joined, "FORECASTS_JOIN_ACTUALS"
    return [], "NO_DETAIL_DATA"


def build(day: str, tz: str) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rules = active_rules(day)
    source_rows, source_guard = source_details(day)
    detail_out: list[dict[str, object]] = []
    for row in source_rows:
        metric = n(row.get("metric"))
        if metric not in rules:
            continue
        bias, patch = rules[metric]
        actual = f(row.get("actual_value"))
        baseline = f(row.get("pred_mid") or row.get("pred_mid_value") or row.get("pred_mid") or row.get("pred_mid"), default=f(row.get("pred_mid")))
        if baseline == 0.0 and n(row.get("pred_mid")) == "":
            baseline = f(row.get("pred_mid") or row.get("pred_mid_value") or row.get("pred_mid"))
        if "pred_mid" not in row and "pred_mid_value" not in row and "pred_mid" not in row:
            baseline = f(row.get("pred_mid") or row.get("pred_mid_value") or row.get("pred_mid"))
        if n(row.get("pred_mid")) == "" and n(row.get("pred_mid_value")) == "" and n(row.get("pred_mid")) == "":
            baseline = f(row.get("pred_mid") or row.get("pred_mid_value") or row.get("pred_mid"))
        if "pred_mid" in row:
            baseline = f(row.get("pred_mid"))
        elif "pred_mid_value" in row:
            baseline = f(row.get("pred_mid_value"))
        elif "pred_mid" in row:
            baseline = f(row.get("pred_mid"))
        else:
            baseline = f(row.get("pred_mid"))
        if "pred_mid" not in row and "pred_mid_value" not in row:
            baseline = f(row.get("pred_mid"))
        if n(row.get("pred_mid")) == "" and n(row.get("pred_mid_value")) == "":
            baseline = f(row.get("pred_mid"))
        # Calibration details use pred_mid; joined details also normalize to pred_mid.
        baseline = f(row.get("pred_mid"))
        shadow, rule = apply_shadow(metric, baseline, bias)
        baseline_error = abs(actual - baseline)
        shadow_error = abs(actual - shadow)
        delta = baseline_error - shadow_error
        result = "IMPROVED" if delta > 0.0001 else "WORSENED" if delta < -0.0001 else "UNCHANGED"
        detail_out.append({
            "target_date": day,
            "generated_at": generated_at,
            "fixture_id": n(row.get("fixture_id")),
            "home_team": n(row.get("home_team")),
            "away_team": n(row.get("away_team")),
            "metric": metric,
            "actual_value": f"{actual:.3f}",
            "baseline_mid": f"{baseline:.3f}",
            "shadow_mid": f"{shadow:.3f}",
            "baseline_abs_error": f"{baseline_error:.3f}",
            "shadow_abs_error": f"{shadow_error:.3f}",
            "error_delta": f"{delta:.3f}",
            "shadow_result": result,
            "shadow_rule": rule,
            "source_guard": source_guard,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    summary_out: list[dict[str, object]] = []
    by_metric: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in detail_out:
        by_metric[str(row["metric"])].append(row)
    for metric, rows in by_metric.items():
        baseline_avg = sum(f(row.get("baseline_abs_error")) for row in rows) / len(rows)
        shadow_avg = sum(f(row.get("shadow_abs_error")) for row in rows) / len(rows)
        delta_avg = baseline_avg - shadow_avg
        improved = sum(1 for row in rows if row.get("shadow_result") == "IMPROVED")
        worsened = sum(1 for row in rows if row.get("shadow_result") == "WORSENED")
        unchanged = sum(1 for row in rows if row.get("shadow_result") == "UNCHANGED")
        if len(rows) < 5:
            verdict = "WAIT_MORE_DETAIL_SAMPLE"
        elif delta_avg > 0 and improved >= worsened:
            verdict = "SHADOW_BETTER_ON_SAMPLE"
        elif delta_avg < 0:
            verdict = "SHADOW_WORSE_ON_SAMPLE"
        else:
            verdict = "NO_CLEAR_AB_EDGE"
        summary_out.append({
            "target_date": day,
            "generated_at": generated_at,
            "metric": metric,
            "rows_evaluated": len(rows),
            "baseline_avg_error": f"{baseline_avg:.3f}",
            "shadow_avg_error": f"{shadow_avg:.3f}",
            "avg_error_delta": f"{delta_avg:.3f}",
            "improved_rows": improved,
            "worsened_rows": worsened,
            "unchanged_rows": unchanged,
            "shadow_verdict": verdict,
            "shadow_rule": str(rows[0].get("shadow_rule")),
            "source_guard": source_guard,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return detail_out, summary_out, source_guard


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, details: list[dict[str, object]], summary: list[dict[str, object]], source_guard: str) -> str:
    lines = [
        f"# vSIGMA Shadow Forecast A/B Simulator - {day}",
        "",
        "## Summary",
        f"- source_guard: {source_guard}",
        f"- detail_rows: {len(details)}",
        f"- summary_rows: {len(summary)}",
        f"- shadow_verdicts: {counts(summary, 'shadow_verdict')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Metric Results",
    ]
    if not summary:
        lines.append("- none. Need calibration detail rows or forecast+actual joins before A/B evaluation.")
    for row in summary:
        lines.append(
            "- "
            f"{row['metric']} | verdict={row['shadow_verdict']} | rows={row['rows_evaluated']} | "
            f"baseline_err={row['baseline_avg_error']} | shadow_err={row['shadow_avg_error']} | "
            f"delta={row['avg_error_delta']} | improved={row['improved_rows']} | worsened={row['worsened_rows']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- A/B simulator is shadow-only and advisory.",
        "- It does not edit forecast formulas.",
        "- It does not modify official picks.",
        "- Promotion still requires manual review and larger sample.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    details, summary, source_guard = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_shadow_forecast_ab_details.csv", details, DETAIL_FIELDS)
        write_csv(base / "vsigma_shadow_forecast_ab_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_shadow_forecast_ab_simulator.md").write_text(md(day, details, summary, source_guard), encoding="utf-8")
    print("=== VSIGMA SHADOW FORECAST A/B SIMULATOR ===")
    print(f"source_guard={source_guard}")
    print(f"detail_rows={len(details)}")
    print(f"summary_rows={len(summary)}")
    print(f"shadow_verdicts={counts(summary, 'shadow_verdict')}")
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
