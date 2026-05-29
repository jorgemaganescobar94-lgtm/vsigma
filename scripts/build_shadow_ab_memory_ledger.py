from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
LEDGER = P / "ledger" / "vsigma_shadow_ab_memory.csv"
LEDGER_FIELDS = [
    "target_date", "generated_at", "metric", "quality_gate", "quality_priority",
    "rows_evaluated", "shadow_verdict", "avg_error_delta", "improved_rows", "worsened_rows",
    "manual_review_required", "promotion_allowed", "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "metric", "history_days", "latest_quality_gate",
    "usable_days", "bad_days", "blocked_days", "low_sample_days", "no_data_days",
    "avg_error_delta_mean", "net_improved_rows", "net_worsened_rows", "memory_verdict",
    "memory_reason", "auto_apply", "production_change",
]


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


def current_rows(day):
    rows = read(d(day, "vsigma_shadow_ab_quality_gate.csv"))
    if rows:
        return rows, str(d(day, "vsigma_shadow_ab_quality_gate.csv"))
    path = P / "governance" / "vsigma_shadow_ab_quality_gate.csv"
    return read(path), str(path)


def normalize_current(day, ts, source_path):
    out = []
    for r in current_rows(day)[0]:
        out.append({
            "target_date": day,
            "generated_at": ts,
            "metric": s(r.get("metric")) or "UNKNOWN",
            "quality_gate": s(r.get("quality_gate")) or "UNKNOWN",
            "quality_priority": s(r.get("quality_priority")) or "UNKNOWN",
            "rows_evaluated": s(r.get("rows_evaluated")) or "0",
            "shadow_verdict": s(r.get("shadow_verdict")) or "UNKNOWN",
            "avg_error_delta": s(r.get("avg_error_delta")) or "0.000",
            "improved_rows": s(r.get("improved_rows")) or "0",
            "worsened_rows": s(r.get("worsened_rows")) or "0",
            "manual_review_required": s(r.get("manual_review_required")) or "NO",
            "promotion_allowed": s(r.get("promotion_allowed")) or "NO",
            "source_guard": source_path,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def upsert_ledger(day, current):
    existing = [r for r in read(LEDGER) if s(r.get("target_date")) != day]
    merged = existing + current
    merged.sort(key=lambda r: (s(r.get("target_date")), s(r.get("metric"))))
    return merged


def recent_by_metric(ledger_rows, limit=10):
    grouped = defaultdict(list)
    for r in ledger_rows:
        grouped[s(r.get("metric")) or "UNKNOWN"].append(r)
    out = {}
    for metric, rows in grouped.items():
        rows.sort(key=lambda r: s(r.get("target_date")))
        out[metric] = rows[-limit:]
    return out


def summarize(day, ts, ledger_rows):
    summary = []
    for metric, rows in recent_by_metric(ledger_rows).items():
        gates = Counter(s(r.get("quality_gate")) or "UNKNOWN" for r in rows)
        latest = s(rows[-1].get("quality_gate")) or "UNKNOWN"
        usable = gates.get("USABLE_SHADOW_SIGNAL", 0)
        bad = gates.get("BAD_SHADOW_SIGNAL", 0)
        blocked = gates.get("PROMOTION_BLOCKED", 0)
        low = gates.get("LOW_SAMPLE", 0)
        nodata = gates.get("NO_DATA", 0)
        delta_mean = sum(num(r.get("avg_error_delta")) for r in rows) / len(rows) if rows else 0.0
        net_imp = sum(integer(r.get("improved_rows")) for r in rows)
        net_wor = sum(integer(r.get("worsened_rows")) for r in rows)

        if bad > 0 and bad >= usable:
            verdict = "MEMORY_BAD_SIGNAL"
            reason = "Bad A/B days are present and not outweighed by usable days."
        elif usable >= 2 and bad == 0 and delta_mean > 0:
            verdict = "MEMORY_IMPROVING_SIGNAL"
            reason = "Multiple usable A/B days with positive average delta and no bad days."
        elif blocked > 0 and bad == 0:
            verdict = "MEMORY_PROMOTION_BLOCKED_SAMPLE"
            reason = "Improvement exists but recent history remains sample-blocked."
        elif low > 0 or nodata > 0:
            verdict = "MEMORY_WAIT_MORE_DATA"
            reason = "Recent history has low sample or no-data days."
        else:
            verdict = "MEMORY_NO_CLEAR_SIGNAL"
            reason = "Recent history does not show a decisive A/B direction."

        summary.append({
            "target_date": day,
            "generated_at": ts,
            "metric": metric,
            "history_days": len(rows),
            "latest_quality_gate": latest,
            "usable_days": usable,
            "bad_days": bad,
            "blocked_days": blocked,
            "low_sample_days": low,
            "no_data_days": nodata,
            "avg_error_delta_mean": f"{delta_mean:.3f}",
            "net_improved_rows": net_imp,
            "net_worsened_rows": net_wor,
            "memory_verdict": verdict,
            "memory_reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    summary.sort(key=lambda r: str(r.get("metric")))
    return summary


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, summary):
    lines = [
        f"# vSIGMA Shadow A/B Historical Memory - {day}",
        "",
        "## Summary",
        f"- metrics_reviewed: {len(summary)}",
        f"- memory_verdicts: {counts(summary, 'memory_verdict')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Metric Memory",
    ]
    if not summary:
        lines.append("- none. Need shadow A/B quality gate rows first.")
    for r in summary:
        lines.append(
            f"- {r['metric']} | verdict={r['memory_verdict']} | latest={r['latest_quality_gate']} | "
            f"days={r['history_days']} | usable={r['usable_days']} | bad={r['bad_days']} | "
            f"blocked={r['blocked_days']} | delta_mean={r['avg_error_delta_mean']} | reason={r['memory_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Historical memory is advisory only.",
        "- No forecast formula changes are made.",
        "- No official pick changes are made.",
        "- Manual review is required before any promotion.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source_path = current_rows(day)
    current = normalize_current(day, ts, source_path)
    ledger = upsert_ledger(day, current)
    summary = summarize(day, ts, ledger)
    write(LEDGER, ledger, LEDGER_FIELDS)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_shadow_ab_memory_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_shadow_ab_memory_summary.md").write_text(md(day, summary), encoding="utf-8")
    print("=== VSIGMA SHADOW AB MEMORY LEDGER ===")
    print(f"ledger_rows={len(ledger)}")
    print(f"memory_verdicts={counts(summary, 'memory_verdict')}")
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
