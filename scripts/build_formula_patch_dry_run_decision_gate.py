from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "proposal_id", "rows_evaluated",
    "dry_run_verdict", "avg_error_delta", "improved_rows", "worsened_rows",
    "decision_gate", "decision_priority", "ready_for_code_review", "manual_review_required",
    "decision_reason", "next_action", "source_guard", "auto_apply", "production_change",
]
MIN_ROWS_FOR_CODE_REVIEW = 8
MIN_STRONG_DELTA = 0.05


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
    p = d(day, "vsigma_formula_patch_dry_run_backtest_summary.csv")
    rows = read(p)
    if rows:
        return rows, str(p)
    p = P / "governance" / "vsigma_formula_patch_dry_run_backtest_summary.csv"
    return read(p), str(p)


def evaluate(r, day, ts, source):
    metric = s(r.get("metric")) or "UNKNOWN"
    proposal_id = s(r.get("proposal_id")) or "UNKNOWN"
    rows = integer(r.get("rows_evaluated"))
    verdict = s(r.get("dry_run_verdict")) or "UNKNOWN"
    delta = num(r.get("avg_error_delta"))
    improved = integer(r.get("improved_rows"))
    worsened = integer(r.get("worsened_rows"))

    if verdict == "NO_BACKTEST_ROWS" or rows <= 0:
        gate = "DO_NOT_TOUCH"
        priority = "NONE"
        ready = "NO"
        reason = "No dry-run backtest rows exist for this patch."
        next_action = "Wait for actuals/backtest rows before considering formula changes."
    elif verdict == "PATCH_BACKTEST_WORSENS" or delta < 0 or worsened > improved:
        gate = "REJECT"
        priority = "HIGH"
        ready = "NO"
        reason = "Dry-run patch worsens forecast error or worsens more rows than it improves."
        next_action = "Reject this patch path unless later memory materially changes."
    elif verdict == "WAIT_MORE_BACKTEST_SAMPLE" or rows < MIN_ROWS_FOR_CODE_REVIEW:
        gate = "WAIT_MORE_SAMPLE"
        priority = "MEDIUM"
        ready = "NO"
        reason = "Patch may have signal, but dry-run sample is below review threshold."
        next_action = "Accumulate more post-match backtest rows."
    elif verdict == "PATCH_BACKTEST_IMPROVES" and delta >= MIN_STRONG_DELTA and improved >= worsened:
        gate = "READY_FOR_CODE_REVIEW"
        priority = "HIGH"
        ready = "YES"
        reason = "Dry-run improves average error with enough sample; code review may be prepared manually."
        next_action = "Prepare a small manual PR/diff with rollback plan and post-change backtest."
    else:
        gate = "WAIT_MORE_SAMPLE"
        priority = "LOW"
        ready = "NO"
        reason = "Dry-run result is not decisive enough for code review."
        next_action = "Continue shadow/backtest accumulation."

    return {
        "target_date": day,
        "generated_at": ts,
        "metric": metric,
        "proposal_id": proposal_id,
        "rows_evaluated": rows,
        "dry_run_verdict": verdict,
        "avg_error_delta": f"{delta:.3f}",
        "improved_rows": improved,
        "worsened_rows": worsened,
        "decision_gate": gate,
        "decision_priority": priority,
        "ready_for_code_review": ready,
        "manual_review_required": "YES" if ready == "YES" else "NO",
        "decision_reason": reason,
        "next_action": next_action,
        "source_guard": source,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source = source_rows(day)
    if not rows:
        rows = [{"metric": "ALL", "proposal_id": "NO_BACKTEST", "rows_evaluated": 0, "dry_run_verdict": "NO_BACKTEST_ROWS"}]
    return [evaluate(r, day, ts, source) for r in rows]


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, rows):
    lines = [
        f"# vSIGMA Formula Patch Dry-Run Decision Gate - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- decision_gates: {counts(rows, 'decision_gate')}",
        f"- ready_for_code_review: {counts(rows, 'ready_for_code_review')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Patch Decisions",
    ]
    for r in rows:
        lines.append(
            f"- {r['metric']} | gate={r['decision_gate']} | priority={r['decision_priority']} | "
            f"proposal={r['proposal_id']} | rows={r['rows_evaluated']} | verdict={r['dry_run_verdict']} | "
            f"delta={r['avg_error_delta']} | ready={r['ready_for_code_review']} | next={r['next_action']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This gate does not modify production code.",
        "- READY_FOR_CODE_REVIEW still requires manual PR/review and rollback plan.",
        "- No formula, pick, market, or workflow behavior is changed.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_formula_patch_dry_run_decision_gate.csv", rows, FIELDS)
        (base / "vsigma_formula_patch_dry_run_decision_gate.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA FORMULA PATCH DRY-RUN DECISION GATE ===")
    print(f"decision_gates={counts(rows, 'decision_gate')}")
    print(f"ready_for_code_review={counts(rows, 'ready_for_code_review')}")
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
