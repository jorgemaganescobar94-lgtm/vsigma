from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "proposal_decision", "review_decision",
    "dry_run_diff_status", "backtest_verdict", "decision_gate", "ready_for_code_review",
    "manual_review_required", "overall_status", "overall_priority", "next_action",
    "blocking_reason", "source_guard", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


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


def g(name):
    return P / "governance" / name


def source(day, filename):
    p = d(day, filename)
    rows = read(p)
    if rows:
        return rows, str(p)
    p = g(filename)
    return read(p), str(p)


def keyed(rows):
    return {s(r.get("metric")) or "UNKNOWN": r for r in rows}


def all_metrics(*maps):
    out = []
    for mp in maps:
        for m in mp:
            if m not in out:
                out.append(m)
    return out or ["ALL"]


def decide(proposal, review, diff, backtest, gate):
    proposal_decision = s(proposal.get("proposal_decision")) or "UNKNOWN"
    review_decision = s(review.get("review_decision")) or "UNKNOWN"
    diff_status = s(diff.get("dry_run_diff_status")) or "UNKNOWN"
    backtest_verdict = s(backtest.get("dry_run_verdict")) or "UNKNOWN"
    decision_gate = s(gate.get("decision_gate")) or "UNKNOWN"
    ready = s(gate.get("ready_for_code_review")) or "NO"

    if decision_gate == "READY_FOR_CODE_REVIEW" and ready == "YES":
        return "READY_FOR_MANUAL_CODE_REVIEW", "HIGH", "Prepare a small manual PR/diff with rollback plan.", "No blocker; manual review still mandatory."
    if decision_gate == "REJECT" or backtest_verdict == "PATCH_BACKTEST_WORSENS" or proposal_decision == "REJECT_SHADOW_PATCH":
        return "REJECT_PATCH_PATH", "HIGH", "Do not touch production formula for this patch path.", "Dry-run/backtest/proposal rejected or worsened."
    if decision_gate == "DO_NOT_TOUCH":
        return "DO_NOT_TOUCH", "MEDIUM", "Wait for valid backtest rows before any formula discussion.", "No valid dry-run backtest evidence."
    if decision_gate == "WAIT_MORE_SAMPLE" or review_decision == "WAIT" or proposal_decision in {"HOLD_MORE_SAMPLE", "WAIT_MORE_DATA"}:
        return "WAIT_MORE_SAMPLE", "MEDIUM", "Accumulate more A/B and dry-run backtest sample.", "Evidence is not strong enough for code review."
    if review_decision == "NO_ACTION" or proposal_decision in {"NO_PATCH_PROPOSAL", "NO_DATA"}:
        return "NO_ACTION", "LOW", "No formula work required now.", "No evidence-backed proposal."
    if diff_status == "DRY_RUN_DIFF_HELD":
        return "DIFF_HELD", "LOW", "Keep diff as reference only; do not prepare PR.", "Dry-run diff is held by review gate."
    return "WAIT", "LOW", "Keep monitoring until gates align.", "Mixed or incomplete governance state."


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    proposal_rows, proposal_src = source(day, "vsigma_shadow_calibration_patch_proposals.csv")
    review_rows, review_src = source(day, "vsigma_formula_patch_review_pack.csv")
    diff_rows, diff_src = source(day, "vsigma_formula_patch_dry_run_diff.csv")
    backtest_rows, backtest_src = source(day, "vsigma_formula_patch_dry_run_backtest_summary.csv")
    gate_rows, gate_src = source(day, "vsigma_formula_patch_dry_run_decision_gate.csv")

    pm = keyed(proposal_rows)
    rm = keyed(review_rows)
    dm = keyed(diff_rows)
    bm = keyed(backtest_rows)
    gm = keyed(gate_rows)
    rows = []
    src = f"proposal={proposal_src}; review={review_src}; diff={diff_src}; backtest={backtest_src}; gate={gate_src}"
    for metric in all_metrics(pm, rm, dm, bm, gm):
        proposal = pm.get(metric, {})
        review = rm.get(metric, {})
        diff = dm.get(metric, {})
        backtest = bm.get(metric, {})
        gate = gm.get(metric, {})
        overall, priority, action, blocker = decide(proposal, review, diff, backtest, gate)
        rows.append({
            "target_date": day,
            "generated_at": ts,
            "metric": metric,
            "proposal_decision": s(proposal.get("proposal_decision")) or "UNKNOWN",
            "review_decision": s(review.get("review_decision")) or "UNKNOWN",
            "dry_run_diff_status": s(diff.get("dry_run_diff_status")) or "UNKNOWN",
            "backtest_verdict": s(backtest.get("dry_run_verdict")) or "UNKNOWN",
            "decision_gate": s(gate.get("decision_gate")) or "UNKNOWN",
            "ready_for_code_review": s(gate.get("ready_for_code_review")) or "NO",
            "manual_review_required": "YES" if overall == "READY_FOR_MANUAL_CODE_REVIEW" else "NO",
            "overall_status": overall,
            "overall_priority": priority,
            "next_action": action,
            "blocking_reason": blocker,
            "source_guard": src,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    rows.sort(key=lambda r: (str(r.get("overall_priority")), str(r.get("metric"))))
    return rows


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, rows):
    lines = [
        f"# vSIGMA Formula Patch Governance Dashboard - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- overall_status: {counts(rows, 'overall_status')}",
        f"- ready_for_code_review: {counts(rows, 'ready_for_code_review')}",
        f"- manual_review_required: {counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Patch Governance",
    ]
    for r in rows:
        lines.append(
            f"- {r['metric']} | status={r['overall_status']} | priority={r['overall_priority']} | "
            f"proposal={r['proposal_decision']} | review={r['review_decision']} | diff={r['dry_run_diff_status']} | "
            f"backtest={r['backtest_verdict']} | gate={r['decision_gate']} | ready={r['ready_for_code_review']} | "
            f"next={r['next_action']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Dashboard is read-only governance.",
        "- It does not edit formulas or generate production PRs.",
        "- READY_FOR_MANUAL_CODE_REVIEW still requires explicit human approval.",
        "- No formula, pick, market, or workflow behavior is changed.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_formula_patch_governance_dashboard.csv", rows, FIELDS)
        (base / "vsigma_formula_patch_governance_dashboard.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA FORMULA PATCH GOVERNANCE DASHBOARD ===")
    print(f"overall_status={counts(rows, 'overall_status')}")
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
