from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
DETAIL_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league", "forecast_confidence",
    "metric", "actual_value", "pred_low", "pred_mid", "pred_high", "range_hit", "abs_error_mid",
    "direction_error", "forecast_warning", "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "metric", "rows_evaluated", "hit_count", "miss_count", "hit_rate",
    "avg_abs_error_mid", "bias_direction", "calibration_status", "source_guard", "auto_apply", "production_change",
]
METRICS = {
    "total_goals": ("actual_total_goals", "total_goals_low", "total_goals_mid", "total_goals_high"),
    "total_sot": ("actual_total_sot", "total_sot_low", "total_sot_mid", "total_sot_high"),
    "total_shots": ("actual_total_shots", "total_shots_low", "total_shots_mid", "total_shots_high"),
    "total_corners": ("actual_total_corners", "total_corners_low", "total_corners_mid", "total_corners_high"),
    "total_cards": ("actual_total_cards", "total_cards_low", "total_cards_mid", "total_cards_high"),
    "total_fouls": ("actual_total_fouls", "total_fouls_low", "total_fouls_mid", "total_fouls_high"),
}


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def x(v: object) -> float | None:
    t = n(v)
    if not t or t.lower() == "nan": return None
    try: return float(t)
    except ValueError: return None


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows: w.writerow({k: r.get(k, "") for k in fields})


def dated(base: Path, day: str, name: str) -> Path:
    return base / "today" / day / name


def row_day(r: dict[str, str]) -> str:
    for k in ("target_date", "date"):
        v = n(r.get(k))[:10]
        if v: return v
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [r for r in rows if row_day(r) in {"", day}]


def ix(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out = {}
    for r in rows:
        fid = n(r.get("fixture_id")).replace(".0", "")
        if fid and fid not in out: out[fid] = r
    return out


def detail(day: str, gen: str, forecast: dict[str, str], actual: dict[str, str], metric: str) -> dict[str, object] | None:
    actual_col, low_col, mid_col, high_col = METRICS[metric]
    av, lo, mid, hi = x(actual.get(actual_col)), x(forecast.get(low_col)), x(forecast.get(mid_col)), x(forecast.get(high_col))
    if av is None or lo is None or mid is None or hi is None:
        return None
    hit = lo <= av <= hi
    direction = "ON_RANGE" if hit else "OVER_ESTIMATE" if av < lo else "UNDER_ESTIMATE"
    return {
        "target_date": day, "generated_at": gen, "fixture_id": n(forecast.get("fixture_id")),
        "home_team": n(forecast.get("home_team")), "away_team": n(forecast.get("away_team")), "league": n(forecast.get("league")),
        "forecast_confidence": n(forecast.get("forecast_confidence")), "metric": metric,
        "actual_value": f"{av:.2f}", "pred_low": f"{lo:.2f}", "pred_mid": f"{mid:.2f}", "pred_high": f"{hi:.2f}",
        "range_hit": "HIT" if hit else "MISS", "abs_error_mid": f"{abs(av-mid):.2f}", "direction_error": direction,
        "forecast_warning": n(forecast.get("forecast_warning")), "source_guard": "DATED_INPUT_ONLY", "auto_apply": "NO", "production_change": "NO",
    }


def summarize(day: str, gen: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    by_metric: dict[str, list[dict[str, object]]] = defaultdict(list)
    for r in rows: by_metric[str(r["metric"])].append(r)
    for metric, data in sorted(by_metric.items()):
        hits = sum(1 for r in data if r["range_hit"] == "HIT")
        misses = sum(1 for r in data if r["range_hit"] == "MISS")
        errors = [float(str(r["abs_error_mid"])) for r in data]
        dirs = Counter(str(r["direction_error"]) for r in data if r["direction_error"] != "ON_RANGE")
        hit_rate = hits / len(data) if data else 0
        bias = dirs.most_common(1)[0][0] if dirs else "BALANCED_OR_ON_RANGE"
        if len(data) < 3:
            status = "LOW_SAMPLE_HOLD"
        elif hit_rate >= 0.70:
            status = "CALIBRATION_OK"
        elif bias == "OVER_ESTIMATE":
            status = "MODEL_OVER_ESTIMATING"
        elif bias == "UNDER_ESTIMATE":
            status = "MODEL_UNDER_ESTIMATING"
        else:
            status = "MIXED_CALIBRATION_REVIEW"
        out.append({
            "target_date": day, "generated_at": gen, "metric": metric, "rows_evaluated": len(data),
            "hit_count": hits, "miss_count": misses, "hit_rate": f"{hit_rate:.3f}",
            "avg_abs_error_mid": f"{sum(errors)/len(errors):.2f}" if errors else "",
            "bias_direction": bias, "calibration_status": status,
            "source_guard": "DATED_INPUT_ONLY", "auto_apply": "NO", "production_change": "NO",
        })
    return out


def build(day: str, tz: str, base: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    gen = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    forecasts = same_day(read(dated(base, day, "vsigma_match_stat_forecasts.csv")), day)
    actuals = ix(same_day(read(dated(base, day, "vsigma_post_match_stat_actuals.csv")), day))
    details = []
    for f in forecasts:
        fid = n(f.get("fixture_id")).replace(".0", "")
        a = actuals.get(fid)
        if not a: continue
        for metric in METRICS:
            d = detail(day, gen, f, a, metric)
            if d: details.append(d)
    return details, summarize(day, gen, details)


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, details: list[dict[str, object]], summary: list[dict[str, object]]) -> str:
    lines = [f"# vSIGMA Match Stat Forecast Calibration - {day}", "", "## Summary", f"- detail_rows: {len(details)}", f"- calibration_status_counts: {counts(summary, 'calibration_status')}", "- source_guard: DATED_INPUT_ONLY", "- auto_apply: NO", "- production_change: NO", "", "## Metric Summary"]
    if not summary: lines.append("- none. Need final post-match actuals first.")
    for r in summary:
        lines.append(f"- {r['metric']} | rows={r['rows_evaluated']} | hit_rate={r['hit_rate']} | avg_error={r['avg_abs_error_mid']} | bias={r['bias_direction']} | status={r['calibration_status']}")
    lines += ["", "## Guardrails", "- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.", "- Low sample metrics are held and not used for automatic model changes."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    details, summary = build(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write(out_base / "vsigma_match_stat_forecast_calibration_details.csv", details, DETAIL_FIELDS)
        write(out_base / "vsigma_match_stat_forecast_calibration_summary.csv", summary, SUMMARY_FIELDS)
        (out_base / "vsigma_match_stat_forecast_calibration.md").write_text(md(day, details, summary), encoding="utf-8")
    print("=== VSIGMA MATCH STAT FORECAST CALIBRATION ===")
    print(f"detail_rows={len(details)}")
    print(f"calibration_status_counts={counts(summary, 'calibration_status')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__": main()
