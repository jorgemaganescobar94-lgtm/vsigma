from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "rows_evaluated", "hit_rate", "avg_abs_error_mid",
    "bias_direction", "calibration_status", "severity", "recommended_adjustment", "model_area",
    "auto_apply_allowed", "operator_note", "source_guard", "auto_apply", "production_change",
]


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def f(v: object, default: float = 0.0) -> float:
    try:
        t = n(v)
        if not t or t.lower() == "nan": return default
        return float(t)
    except ValueError:
        return default


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(r) for r in csv.DictReader(file)]


def write(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        w = csv.DictWriter(file, fieldnames=FIELDS)
        w.writeheader()
        for r in rows: w.writerow({k: r.get(k, "") for k in FIELDS})


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def adjustment(metric: str, status: str, bias: str, hit_rate: float, rows: int, err: float) -> tuple[str, str, str, str]:
    if rows < 3:
        return "LOW_SAMPLE", "Hold. Need at least 3 evaluated rows before tuning.", "sample_control", "No change; sample too small."
    severity = "HIGH" if hit_rate < 0.35 or err >= 3.0 else "MEDIUM" if hit_rate < 0.60 else "LOW"
    if status == "CALIBRATION_OK":
        return "LOW", "Keep current calibration.", metric, "Metric is inside acceptable range."
    if metric == "total_goals" and bias == "OVER_ESTIMATE":
        return severity, "Reduce goal projection pressure: lower goal_nudge and/or reduce projected-goals weight by 5-10% for similar profiles.", "build_match_stat_forecasts.goal_model", "Model is overestimating total goals."
    if metric == "total_goals" and bias == "UNDER_ESTIMATE":
        return severity, "Increase goal floor slightly where SoT floor is strong; avoid broad change until more sample.", "build_match_stat_forecasts.goal_model", "Model is underestimating total goals."
    if metric == "total_corners" and bias == "OVER_ESTIMATE":
        return severity, "Reduce corner projection: lower shot_corner_nudge cap and reduce corner range high by 1 for high-tempo profiles.", "build_match_stat_forecasts.corner_model", "Model is overestimating corners."
    if metric == "total_corners" and bias == "UNDER_ESTIMATE":
        return severity, "Increase corner projection only for wide-pressure profiles with real corner sample support.", "build_match_stat_forecasts.corner_model", "Model is underestimating corners."
    if metric == "total_cards" and bias == "UNDER_ESTIMATE":
        return severity, "Raise cards baseline: add card-risk bump for high-foul/high-urgency matches and widen upper card range.", "build_match_stat_forecasts.card_model", "Model is underestimating cards."
    if metric == "total_cards" and bias == "OVER_ESTIMATE":
        return severity, "Reduce card baseline for leagues/ref profiles with low historical cards.", "build_match_stat_forecasts.card_model", "Model is overestimating cards."
    if metric in {"total_sot", "total_shots", "total_fouls"} and status == "CALIBRATION_OK":
        return "LOW", "Keep current calibration and monitor sample growth.", f"build_match_stat_forecasts.{metric}", "Metric is stable."
    return severity, "Review metric-specific formula after more post-match samples.", f"build_match_stat_forecasts.{metric}", "Mixed calibration signal."


def build(day: str, tz: str) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = read(dated(day, "vsigma_match_stat_forecast_calibration_summary.csv"))
    out = []
    for r in rows:
        metric = n(r.get("metric"))
        rows_eval = int(f(r.get("rows_evaluated"), 0))
        hit_rate = f(r.get("hit_rate"), 0)
        err = f(r.get("avg_abs_error_mid"), 0)
        bias = n(r.get("bias_direction"))
        status = n(r.get("calibration_status"))
        sev, rec, area, note = adjustment(metric, status, bias, hit_rate, rows_eval, err)
        out.append({
            "target_date": day,
            "generated_at": generated_at,
            "metric": metric,
            "rows_evaluated": rows_eval,
            "hit_rate": f"{hit_rate:.3f}",
            "avg_abs_error_mid": f"{err:.2f}",
            "bias_direction": bias,
            "calibration_status": status,
            "severity": sev,
            "recommended_adjustment": rec,
            "model_area": area,
            "auto_apply_allowed": "NO",
            "operator_note": note,
            "source_guard": "DATED_INPUT_ONLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [f"# vSIGMA Stat Calibration Governor - {day}", "", "## Summary", f"- rows_reviewed: {len(rows)}", f"- severity_counts: {counts(rows, 'severity')}", "- auto_apply_allowed: NO", "- source_guard: DATED_INPUT_ONLY", "- production_change: NO", "", "## Recommendations"]
    if not rows: lines.append("- none. Need calibration summary first.")
    for r in rows:
        lines.append(f"- {r['metric']} | severity={r['severity']} | status={r['calibration_status']} | hit_rate={r['hit_rate']} | bias={r['bias_direction']} | recommendation={r['recommended_adjustment']}")
    lines += ["", "## Guardrails", "- This governor proposes model changes only; it does not edit forecast formulas automatically.", "- Low-sample recommendations must be validated across more days before production tuning."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write(base / "vsigma_stat_calibration_governor.csv", rows)
        (base / "vsigma_stat_calibration_governor.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA STAT CALIBRATION GOVERNOR ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"severity_counts={counts(rows, 'severity')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)

if __name__ == "__main__": main()
