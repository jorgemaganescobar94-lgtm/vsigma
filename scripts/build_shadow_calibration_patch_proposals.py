from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "memory_verdict", "history_days",
    "latest_quality_gate", "usable_days", "bad_days", "blocked_days", "low_sample_days",
    "no_data_days", "avg_error_delta_mean", "proposal_decision", "proposal_priority",
    "proposal_id", "target_script", "target_function", "suggested_change", "expected_effect",
    "risk_controls", "validation_plan", "promotion_gate", "manual_review_required",
    "source_guard", "auto_apply", "production_change",
]

TARGET_SCRIPT = "scripts/build_match_stat_forecasts.py"


def s(x):
    return "" if x is None else str(x).strip()


def integer(x, default=0):
    try:
        return int(float(s(x)))
    except ValueError:
        return default


def num(x, default=0.0):
    try:
        return float(s(x)) if s(x) and s(x).lower() != "nan" else default
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
    p = d(day, "vsigma_shadow_ab_memory_summary.csv")
    rows = read(p)
    if rows:
        return rows, str(p)
    p = P / "governance" / "vsigma_shadow_ab_memory_summary.csv"
    return read(p), str(p)


def metric_patch(metric: str):
    if metric == "total_goals":
        return {
            "proposal_id": "GOAL_PRESSURE_DOWNSHIFT_V1",
            "target_function": "forecast_row: goal_nudge / total_goals_mid after odds adjustment",
            "suggested_change": "Add a guarded calibration factor that reduces total_goals_mid by 3-5% only for profiles with sustained over-estimation and non-HIGH confidence. Redistribute reduction proportionally to home_goals_mid/away_goals_mid before range_float().",
            "expected_effect": "Lower inflated goal totals and reduce false Over/BTTS translation pressure without changing strong high-confidence goal profiles.",
            "risk_controls": "Do not apply when forecast_confidence>=77, when both teams threat is strong and A/B memory is not improving, or when market odds strongly contradict the downshift.",
        }
    if metric == "total_corners":
        return {
            "proposal_id": "CORNER_VOLUME_CAP_DOWNSHIFT_V1",
            "target_function": "forecast_row: shot_corner_nudge / total_corners_mid before range_int()",
            "suggested_change": "Reduce corner inflation from shot volume by capping shot_corner_nudge high side from +0.14 toward +0.10, and optionally subtract 0.5-1.0 from total_corners_mid only when corner sample is weak or A/B memory confirms over-estimation.",
            "expected_effect": "Reduce high-corner over-projection created by tempo/shot-volume spillover while preserving genuine wide-pressure profiles.",
            "risk_controls": "Do not apply to rows with confirmed wide/corner pressure and full corner data unless memory remains improving across multiple days.",
        }
    if metric == "total_fouls":
        return {
            "proposal_id": "FOUL_BASELINE_DOWNSHIFT_V1",
            "target_function": "forecast_row: home_fouls_mid / away_fouls_mid defaults and total_fouls_mid",
            "suggested_change": "Lower foul baseline inflation by reducing default team fouls from 12.0 toward 11.0-11.3 or applying a 5-8% total_fouls_mid downshift when recent foul data is missing and A/B memory confirms over-estimation.",
            "expected_effect": "Reduce systematic foul over-estimation from default baselines and urgency context while keeping high-contact league data intact.",
            "risk_controls": "Do not apply when both teams have real recent foul data or league/ref context supports high contact.",
        }
    if metric == "total_shots":
        return {
            "proposal_id": "SHOT_VOLUME_SOFT_DOWNSHIFT_V1",
            "target_function": "forecast_row: home_shots_mid / away_shots_mid goal-linked multipliers",
            "suggested_change": "If memory confirms over-estimation, reduce goal-linked shot multiplier sensitivity by 2-4% for weak shot sample rows.",
            "expected_effect": "Reduce inflated shot volume in low-data fixtures without suppressing high-tempo confirmed profiles.",
            "risk_controls": "Only apply to weak shot-sample rows and never when high shot volume is supported by full recent stats.",
        }
    if metric == "total_sot":
        return {
            "proposal_id": "SOT_CONVERSION_GUARD_V1",
            "target_function": "forecast_row: home_sot_mid / away_sot_mid clamp",
            "suggested_change": "No production change unless memory repeatedly shows SoT conversion bias; current metric has historically been stable.",
            "expected_effect": "Preserve stable SoT calibration unless evidence changes.",
            "risk_controls": "Require multiple bad/usable memory days before any change.",
        }
    if metric == "total_cards":
        return {
            "proposal_id": "CARD_RISK_HOLD_V1",
            "target_function": "forecast_row: card urgency/fouls additions",
            "suggested_change": "No production change unless cards memory becomes consistently bad; current card signal is relatively stable.",
            "expected_effect": "Avoid unnecessary card-model changes.",
            "risk_controls": "Keep card model unchanged unless A/B memory turns directional.",
        }
    return {
        "proposal_id": "UNKNOWN_METRIC_HOLD",
        "target_function": "UNKNOWN",
        "suggested_change": "No proposal for unknown metric.",
        "expected_effect": "None.",
        "risk_controls": "Manual review required.",
    }


def decision(row):
    verdict = s(row.get("memory_verdict")) or "UNKNOWN"
    days = integer(row.get("history_days"))
    usable = integer(row.get("usable_days"))
    bad = integer(row.get("bad_days"))
    blocked = integer(row.get("blocked_days"))
    delta = num(row.get("avg_error_delta_mean"))

    if verdict == "MEMORY_BAD_SIGNAL" or bad > 0 and bad >= usable:
        return "REJECT_SHADOW_PATCH", "HIGH", "NO", "Bad historical A/B signal blocks this patch."
    if verdict == "MEMORY_IMPROVING_SIGNAL" and days >= 2 and usable >= 2 and bad == 0 and delta > 0:
        return "PATCH_PROPOSAL_MANUAL_REVIEW", "HIGH", "YES", "Memory supports a directional patch proposal, but manual review is required."
    if verdict == "MEMORY_PROMOTION_BLOCKED_SAMPLE" or blocked > 0:
        return "HOLD_MORE_SAMPLE", "MEDIUM", "NO", "Signal is positive or blocked by sample; keep accumulating evidence."
    if verdict == "MEMORY_WAIT_MORE_DATA":
        return "WAIT_MORE_DATA", "LOW", "NO", "Insufficient data for formula proposal."
    if verdict == "MEMORY_NO_CLEAR_SIGNAL":
        return "NO_PATCH_PROPOSAL", "LOW", "NO", "No clear historical A/B direction."
    return "NO_DATA", "NONE", "NO", "No usable memory verdict."


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source = source_rows(day)
    if not rows:
        rows = [{"metric": "ALL", "memory_verdict": "NO_MEMORY", "history_days": 0}]
    out = []
    for r in rows:
        metric = s(r.get("metric")) or "UNKNOWN"
        patch = metric_patch(metric)
        proposal_decision, priority, manual, reason = decision(r)
        validation_plan = "Run shadow A/B for at least 3-5 additional post-match days; require no MEMORY_BAD_SIGNAL and stable positive avg_error_delta before any production PR."
        promotion_gate = "Production formula change requires explicit manual approval, reviewed diff, and post-change backtest."
        out.append({
            "target_date": day,
            "generated_at": ts,
            "metric": metric,
            "memory_verdict": s(r.get("memory_verdict")) or "UNKNOWN",
            "history_days": s(r.get("history_days")) or "0",
            "latest_quality_gate": s(r.get("latest_quality_gate")) or "UNKNOWN",
            "usable_days": s(r.get("usable_days")) or "0",
            "bad_days": s(r.get("bad_days")) or "0",
            "blocked_days": s(r.get("blocked_days")) or "0",
            "low_sample_days": s(r.get("low_sample_days")) or "0",
            "no_data_days": s(r.get("no_data_days")) or "0",
            "avg_error_delta_mean": s(r.get("avg_error_delta_mean")) or "0.000",
            "proposal_decision": proposal_decision,
            "proposal_priority": priority,
            "proposal_id": patch["proposal_id"],
            "target_script": TARGET_SCRIPT,
            "target_function": patch["target_function"],
            "suggested_change": patch["suggested_change"],
            "expected_effect": patch["expected_effect"],
            "risk_controls": patch["risk_controls"],
            "validation_plan": validation_plan,
            "promotion_gate": promotion_gate,
            "manual_review_required": manual,
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
        f"# vSIGMA Shadow Calibration Patch Proposals - {day}",
        "",
        "## Summary",
        f"- proposals_reviewed: {len(rows)}",
        f"- proposal_decisions: {counts(rows, 'proposal_decision')}",
        f"- priorities: {counts(rows, 'proposal_priority')}",
        f"- manual_review_required: {counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Proposals",
    ]
    for r in rows:
        lines.append(
            f"- {r['metric']} | decision={r['proposal_decision']} | priority={r['proposal_priority']} | "
            f"proposal={r['proposal_id']} | memory={r['memory_verdict']} | manual_review={r['manual_review_required']} | "
            f"target={r['target_script']}::{r['target_function']} | change={r['suggested_change']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This engine generates proposals only.",
        "- It does not edit forecast formulas.",
        "- It does not change official picks or markets.",
        "- Production changes require manual review and explicit approval.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_shadow_calibration_patch_proposals.csv", rows, FIELDS)
        (base / "vsigma_shadow_calibration_patch_proposals.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA SHADOW CALIBRATION PATCH PROPOSALS ===")
    print(f"proposal_decisions={counts(rows, 'proposal_decision')}")
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
