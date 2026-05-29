from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "proposal_id", "proposal_decision",
    "review_decision", "review_priority", "ready_for_diff", "target_script", "target_function",
    "code_anchor", "diff_strategy", "safety_constraints", "validation_required",
    "rollback_plan", "operator_note", "source_guard", "auto_apply", "production_change",
]

CODE_ANCHORS = {
    "total_goals": "goal_nudge block and total_goals_mid calculation in forecast_row()",
    "total_corners": "shot_corner_nudge and total_corners_mid calculation in forecast_row()",
    "total_fouls": "home_fouls_mid/away_fouls_mid defaults and total_fouls_mid calculation in forecast_row()",
    "total_shots": "home_shots_mid/away_shots_mid goal-linked multipliers in forecast_row()",
    "total_sot": "home_sot_mid/away_sot_mid conversion and clamp in forecast_row()",
    "total_cards": "home_cards_mid/away_cards_mid urgency/foul additions in forecast_row()",
}

DIFF_STRATEGIES = {
    "GOAL_PRESSURE_DOWNSHIFT_V1": "Introduce guarded calibration factor after goal_nudge redistribution: if eligible, multiply home_goals_mid and away_goals_mid by 0.95-0.97 before total_goals_mid. Eligibility: non-HIGH confidence + improving memory + no bad A/B signal.",
    "CORNER_VOLUME_CAP_DOWNSHIFT_V1": "Cap positive shot_corner_nudge from 0.14 to 0.10 and optionally apply -0.5 total corner midpoint adjustment for weak corner sample rows only.",
    "FOUL_BASELINE_DOWNSHIFT_V1": "Reduce fallback foul baseline from 12.0 toward 11.0-11.3 only when recent foul data is missing; do not touch rows with real foul data.",
    "SHOT_VOLUME_SOFT_DOWNSHIFT_V1": "Reduce goal-linked shot multiplier sensitivity only for SHOT_SAMPLE_WEAK rows if memory confirms sustained over-estimation.",
    "SOT_CONVERSION_GUARD_V1": "Hold. Do not edit SoT formula unless future memory turns directional.",
    "CARD_RISK_HOLD_V1": "Hold. Do not edit card formula unless future memory turns directional.",
}


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


def source_rows(day):
    p = d(day, "vsigma_shadow_calibration_patch_proposals.csv")
    rows = read(p)
    if rows:
        return rows, str(p)
    p = P / "governance" / "vsigma_shadow_calibration_patch_proposals.csv"
    return read(p), str(p)


def review_decision(row):
    proposal = s(row.get("proposal_decision"))
    manual = s(row.get("manual_review_required"))
    memory = s(row.get("memory_verdict"))
    bad_days = s(row.get("bad_days"))

    if proposal == "PATCH_PROPOSAL_MANUAL_REVIEW" and manual == "YES":
        return "READY_FOR_MANUAL_DIFF", "HIGH", "YES", "Proposal has enough shadow memory to prepare a reviewed diff, but must not be auto-applied."
    if proposal in {"HOLD_MORE_SAMPLE", "WAIT_MORE_DATA"}:
        return "WAIT", "MEDIUM" if proposal == "HOLD_MORE_SAMPLE" else "LOW", "NO", "Keep accumulating A/B memory before touching formula code."
    if proposal == "REJECT_SHADOW_PATCH" or memory == "MEMORY_BAD_SIGNAL" or bad_days not in {"", "0"}:
        return "REJECT", "HIGH", "NO", "Historical A/B memory contains bad signal; do not prepare formula diff."
    if proposal in {"NO_PATCH_PROPOSAL", "NO_DATA"}:
        return "NO_ACTION", "LOW", "NO", "No evidence-backed formula change available."
    return "WAIT", "LOW", "NO", "Unclear proposal state; wait for cleaner evidence."


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source = source_rows(day)
    if not rows:
        rows = [{"metric": "ALL", "proposal_id": "NO_PROPOSALS", "proposal_decision": "NO_DATA"}]
    out = []
    for r in rows:
        metric = s(r.get("metric")) or "UNKNOWN"
        proposal_id = s(r.get("proposal_id")) or "UNKNOWN"
        decision, priority, ready, note = review_decision(r)
        safety = "Diff must preserve auto_apply=NO/prod governance, include before/after backtest, and avoid changing high-confidence rows unless explicitly approved."
        validation = "Run full post-match learning chain, shadow A/B simulator, A/B quality gate, and compare at least 3-5 additional days before promotion."
        rollback = "Revert only the formula patch commit; shadow/governance ledgers remain for audit."
        out.append({
            "target_date": day,
            "generated_at": ts,
            "metric": metric,
            "proposal_id": proposal_id,
            "proposal_decision": s(r.get("proposal_decision")) or "UNKNOWN",
            "review_decision": decision,
            "review_priority": priority,
            "ready_for_diff": ready,
            "target_script": s(r.get("target_script")) or "scripts/build_match_stat_forecasts.py",
            "target_function": s(r.get("target_function")) or "forecast_row",
            "code_anchor": CODE_ANCHORS.get(metric, "UNKNOWN"),
            "diff_strategy": DIFF_STRATEGIES.get(proposal_id, s(r.get("suggested_change")) or "No diff strategy."),
            "safety_constraints": safety,
            "validation_required": validation,
            "rollback_plan": rollback,
            "operator_note": note,
            "source_guard": source,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, rows):
    lines = [
        f"# vSIGMA Formula Patch Review Pack - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- review_decisions: {counts(rows, 'review_decision')}",
        f"- ready_for_diff: {counts(rows, 'ready_for_diff')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Review Items",
    ]
    for r in rows:
        lines += [
            f"### {r['metric']} — {r['review_decision']}",
            f"- proposal_id: {r['proposal_id']}",
            f"- priority: {r['review_priority']}",
            f"- target: {r['target_script']} :: {r['target_function']}",
            f"- code_anchor: {r['code_anchor']}",
            f"- diff_strategy: {r['diff_strategy']}",
            f"- safety_constraints: {r['safety_constraints']}",
            f"- validation_required: {r['validation_required']}",
            f"- rollback_plan: {r['rollback_plan']}",
            f"- note: {r['operator_note']}",
            "",
        ]
    lines += [
        "## Guardrails",
        "- This review pack does not edit production formulas.",
        "- READY_FOR_MANUAL_DIFF only means a human-reviewed diff may be prepared.",
        "- No formula patch should be merged without post-change backtest and manual approval.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_formula_patch_review_pack.csv", rows, FIELDS)
        (base / "vsigma_formula_patch_review_pack.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA FORMULA PATCH REVIEW PACK ===")
    print(f"review_decisions={counts(rows, 'review_decision')}")
    print(f"ready_for_diff={counts(rows, 'ready_for_diff')}")
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
