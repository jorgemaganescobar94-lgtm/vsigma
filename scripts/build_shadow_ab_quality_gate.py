from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "rows_evaluated", "shadow_verdict",
    "avg_error_delta", "improved_rows", "worsened_rows", "quality_gate",
    "quality_priority", "promotion_allowed", "manual_review_required",
    "quality_reason", "source_guard", "auto_apply", "production_change",
]
MIN_USABLE_ROWS = 5
MIN_PROMOTION_ROWS = 20
MIN_DELTA_EDGE = 0.05


def s(x):
    return "" if x is None else str(x).strip()


def num(x, default=0.0):
    try:
        return float(s(x)) if s(x) and s(x).lower() != "nan" else default
    except ValueError:
        return default


def integer(x, default=0):
    try:
        return int(float(s(x)))
    except ValueError:
        return default


def read(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day, name):
    return P / "today" / day / name


def source_rows(day):
    rows = read(d(day, "vsigma_shadow_forecast_ab_summary.csv"))
    if rows:
        return rows, str(d(day, "vsigma_shadow_forecast_ab_summary.csv"))
    path = P / "governance" / "vsigma_shadow_forecast_ab_summary.csv"
    return read(path), str(path)


def evaluate(row, day, ts, source_path):
    metric = s(row.get("metric")) or "UNKNOWN"
    rows = integer(row.get("rows_evaluated"))
    verdict = s(row.get("shadow_verdict")) or "UNKNOWN"
    delta = num(row.get("avg_error_delta"))
    improved = integer(row.get("improved_rows"))
    worsened = integer(row.get("worsened_rows"))

    if rows <= 0 or verdict == "UNKNOWN":
        gate = "NO_DATA"
        priority = "NONE"
        reason = "No A/B rows available for this metric."
    elif rows < MIN_USABLE_ROWS or verdict == "WAIT_MORE_DETAIL_SAMPLE":
        gate = "LOW_SAMPLE"
        priority = "LOW"
        reason = "A/B sample is below usable threshold."
    elif verdict == "SHADOW_WORSE_ON_SAMPLE" or delta < -MIN_DELTA_EDGE or worsened > improved:
        gate = "BAD_SHADOW_SIGNAL"
        priority = "HIGH"
        reason = "Shadow rule worsens error or worsens more rows than it improves."
    elif verdict == "SHADOW_BETTER_ON_SAMPLE" and delta >= MIN_DELTA_EDGE and improved >= worsened:
        if rows >= MIN_PROMOTION_ROWS:
            gate = "USABLE_SHADOW_SIGNAL"
            priority = "HIGH"
            reason = "Shadow improves sample and has enough rows for manual promotion review."
        else:
            gate = "PROMOTION_BLOCKED"
            priority = "MEDIUM"
            reason = "Shadow improves sample, but promotion is blocked until larger sample."
    else:
        gate = "NO_CLEAR_AB_EDGE"
        priority = "LOW"
        reason = "A/B result does not show a clear usable edge."

    manual = "YES" if gate == "USABLE_SHADOW_SIGNAL" else "NO"
    promotion = "YES_MANUAL_ONLY" if gate == "USABLE_SHADOW_SIGNAL" else "NO"
    return {
        "target_date": day,
        "generated_at": ts,
        "metric": metric,
        "rows_evaluated": rows,
        "shadow_verdict": verdict,
        "avg_error_delta": f"{delta:.3f}",
        "improved_rows": improved,
        "worsened_rows": worsened,
        "quality_gate": gate,
        "quality_priority": priority,
        "promotion_allowed": promotion,
        "manual_review_required": manual,
        "quality_reason": reason,
        "source_guard": source_path,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source_path = source_rows(day)
    if not rows:
        return [{
            "target_date": day, "generated_at": ts, "metric": "ALL", "rows_evaluated": 0,
            "shadow_verdict": "NO_AB_SUMMARY", "avg_error_delta": "0.000", "improved_rows": 0,
            "worsened_rows": 0, "quality_gate": "NO_DATA", "quality_priority": "NONE",
            "promotion_allowed": "NO", "manual_review_required": "NO",
            "quality_reason": "No A/B summary found.", "source_guard": source_path,
            "auto_apply": "NO", "production_change": "NO",
        }]
    return [evaluate(r, day, ts, source_path) for r in rows]


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, rows):
    lines = [
        f"# vSIGMA Shadow A/B Result Quality Gate - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- quality_gates: {counts(rows, 'quality_gate')}",
        f"- priorities: {counts(rows, 'quality_priority')}",
        f"- manual_review_required: {counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Metric Gates",
    ]
    for r in rows:
        lines.append(
            f"- {r['metric']} | gate={r['quality_gate']} | priority={r['quality_priority']} | "
            f"rows={r['rows_evaluated']} | verdict={r['shadow_verdict']} | delta={r['avg_error_delta']} | "
            f"manual_review={r['manual_review_required']} | reason={r['quality_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Quality gate is advisory only.",
        "- No production change is allowed.",
        "- No formula or pick changes are made.",
        "- USABLE_SHADOW_SIGNAL still requires explicit manual review.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_shadow_ab_quality_gate.csv", rows, FIELDS)
        (base / "vsigma_shadow_ab_quality_gate.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA SHADOW AB QUALITY GATE ===")
    print(f"quality_gates={counts(rows, 'quality_gate')}")
    print(f"manual_review_required={counts(rows, 'manual_review_required')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
