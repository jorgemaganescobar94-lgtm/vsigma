from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
LEDGER_DIR = PROCESSED / "ledger"
LEDGER_PATH = LEDGER_DIR / "vsigma_stat_calibration_memory.csv"
LEDGER_FIELDS = [
    "target_date", "generated_at", "metric", "rows_evaluated", "hit_rate", "avg_abs_error_mid",
    "bias_direction", "calibration_status", "severity", "recommended_adjustment", "model_area",
    "auto_apply_allowed", "operator_note", "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "generated_at", "metric", "days_observed", "total_rows_evaluated", "weighted_hit_rate",
    "weighted_avg_abs_error_mid", "dominant_bias", "dominant_bias_days", "latest_status",
    "latest_severity", "memory_decision", "patch_candidate", "recommended_next_action",
    "auto_apply_allowed", "source_guard", "production_change",
]


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def f(v: object, default: float = 0.0) -> float:
    try:
        t = n(v)
        if not t or t.lower() == "nan":
            return default
        return float(t)
    except ValueError:
        return default


def i(v: object, default: int = 0) -> int:
    return int(round(f(v, float(default))))


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(r) for r in csv.DictReader(file)]


def write(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def row_day(row: dict[str, str]) -> str:
    return n(row.get("target_date"))[:10]


def normalize_daily(row: dict[str, str], day: str, generated_at: str) -> dict[str, object]:
    return {
        "target_date": n(row.get("target_date"))[:10] or day,
        "generated_at": n(row.get("generated_at")) or generated_at,
        "metric": n(row.get("metric")),
        "rows_evaluated": i(row.get("rows_evaluated")),
        "hit_rate": f"{f(row.get('hit_rate')):.3f}",
        "avg_abs_error_mid": f"{f(row.get('avg_abs_error_mid')):.2f}",
        "bias_direction": n(row.get("bias_direction")),
        "calibration_status": n(row.get("calibration_status")),
        "severity": n(row.get("severity")),
        "recommended_adjustment": n(row.get("recommended_adjustment")),
        "model_area": n(row.get("model_area")),
        "auto_apply_allowed": "NO",
        "operator_note": n(row.get("operator_note")),
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def upsert_ledger(day: str, generated_at: str) -> list[dict[str, object]]:
    existing = read(LEDGER_PATH)
    daily = read(dated(day, "vsigma_stat_calibration_governor.csv"))
    keys_today = {f"{day}|{n(r.get('metric'))}" for r in daily}
    kept = [r for r in existing if f"{row_day(r)}|{n(r.get('metric'))}" not in keys_today]
    added = [normalize_daily(r, day, generated_at) for r in daily if n(r.get("metric"))]
    ledger = kept + added
    ledger.sort(key=lambda r: (n(r.get("metric")), n(r.get("target_date"))))
    return ledger


def weighted(values: list[tuple[float, int]]) -> float:
    total = sum(w for _, w in values)
    if total <= 0:
        return 0.0
    return sum(v * w for v, w in values) / total


def summarize(ledger: list[dict[str, object]], generated_at: str) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in ledger:
        metric = n(row.get("metric"))
        if metric:
            groups[metric].append(row)
    out: list[dict[str, object]] = []
    for metric, rows in sorted(groups.items()):
        rows_sorted = sorted(rows, key=lambda r: n(r.get("target_date")))
        days = {n(r.get("target_date")) for r in rows_sorted if n(r.get("target_date"))}
        total_rows = sum(i(r.get("rows_evaluated")) for r in rows_sorted)
        hit = weighted([(f(r.get("hit_rate")), i(r.get("rows_evaluated"))) for r in rows_sorted])
        err = weighted([(f(r.get("avg_abs_error_mid")), i(r.get("rows_evaluated"))) for r in rows_sorted])
        bias_counter = Counter(n(r.get("bias_direction")) for r in rows_sorted if n(r.get("bias_direction")) not in {"", "BALANCED_OR_ON_RANGE"})
        dominant_bias, dominant_days = (bias_counter.most_common(1)[0] if bias_counter else ("BALANCED_OR_ON_RANGE", 0))
        latest = rows_sorted[-1]
        latest_status = n(latest.get("calibration_status"))
        latest_severity = n(latest.get("severity"))

        if total_rows < 10 or len(days) < 2:
            decision = "ACCUMULATE_MORE_SAMPLE"
            patch = "NO"
            action = "Keep collecting post-match calibration. Minimum gate: >=10 evaluated rows across >=2 days."
        elif hit >= 0.60:
            decision = "CALIBRATION_STABLE"
            patch = "NO"
            action = "Keep current model calibration and continue monitoring."
        elif hit < 0.55 and dominant_days >= 2 and dominant_bias != "BALANCED_OR_ON_RANGE":
            decision = "PATCH_CANDIDATE_REVIEW"
            patch = "YES_REVIEW_ONLY"
            if dominant_bias == "OVER_ESTIMATE":
                action = f"Review lowering {metric} projection/range for matching profiles; do not auto-apply."
            else:
                action = f"Review raising {metric} projection/range for matching profiles; do not auto-apply."
        else:
            decision = "MIXED_CALIBRATION_REVIEW"
            patch = "NO"
            action = "Signal is mixed. Wait for more sample or segment by league/profile."

        out.append({
            "generated_at": generated_at,
            "metric": metric,
            "days_observed": len(days),
            "total_rows_evaluated": total_rows,
            "weighted_hit_rate": f"{hit:.3f}",
            "weighted_avg_abs_error_mid": f"{err:.2f}",
            "dominant_bias": dominant_bias,
            "dominant_bias_days": dominant_days,
            "latest_status": latest_status,
            "latest_severity": latest_severity,
            "memory_decision": decision,
            "patch_candidate": patch,
            "recommended_next_action": action,
            "auto_apply_allowed": "NO",
            "source_guard": "DATED_INPUT_ONLY",
            "production_change": "NO",
        })
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(n(r.get(field)) or "UNKNOWN" for r in rows)
    return "; ".join(f"{k}={v}" for k, v in counter.most_common()) if counter else "none"


def md(day: str, ledger: list[dict[str, object]], summary: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Calibration Memory Ledger - {day}", "", "## Summary",
        f"- ledger_rows_total: {len(ledger)}",
        f"- metrics_tracked: {len(summary)}",
        f"- memory_decision_counts: {counts(summary, 'memory_decision')}",
        "- auto_apply_allowed: NO",
        "- source_guard: DATED_INPUT_ONLY",
        "- production_change: NO", "", "## Metric Memory",
    ]
    if not summary:
        lines.append("- none. Need stat calibration governor rows first.")
    for row in summary:
        lines.append(
            f"- {row['metric']} | days={row['days_observed']} | rows={row['total_rows_evaluated']} | "
            f"hit_rate={row['weighted_hit_rate']} | bias={row['dominant_bias']} | decision={row['memory_decision']} | "
            f"patch={row['patch_candidate']} | next={row['recommended_next_action']}"
        )
    lines += [
        "", "## Governance Rules",
        "- Never auto-apply calibration changes from one day or low sample.",
        "- Patch candidates require >=10 evaluated rows, >=2 days, hit_rate < 0.55 and repeated same-direction bias.",
        "- All changes remain review-only until manually accepted.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    ledger = upsert_ledger(day, generated_at)
    summary = summarize(ledger, generated_at)
    write(LEDGER_PATH, LEDGER_FIELDS, ledger)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write(base / "vsigma_calibration_memory_ledger.csv", LEDGER_FIELDS, ledger)
        write(base / "vsigma_calibration_memory_summary.csv", SUMMARY_FIELDS, summary)
        (base / "vsigma_calibration_memory_ledger.md").write_text(md(day, ledger, summary), encoding="utf-8")
    print("=== VSIGMA CALIBRATION MEMORY LEDGER ===")
    print(f"ledger_rows_total={len(ledger)}")
    print(f"memory_decision_counts={counts(summary, 'memory_decision')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)

if __name__ == "__main__": main()
