from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
SUMMARY_FIELDS = [
    "target_date", "generated_at", "base_profit_units", "adjusted_profit_units",
    "net_adjustment_delta_units", "avoided_loss_units", "missed_win_units",
    "calibration_verdict", "recommended_policy", "min_samples_before_rule_change",
    "auto_apply", "production_change", "guardrail_status"
]
DETAIL_FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team", "market_primary",
    "base_result", "adjusted_status", "audit_label", "audit_effect_units", "calibration_label",
    "calibration_note", "suggested_future_treatment"
]
MIN_SAMPLES = 20


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def num(v: object, default: float = 0.0) -> float:
    try:
        text = norm(v)
        if not text or text.lower() == "nan":
            return default
        return float(text)
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({field: r.get(field, "") for field in fields})


def file_for(processed: Path, target_date: str, filename: str) -> Path:
    p = processed / "today" / target_date / filename
    if p.exists():
        return p
    return processed / "governance" / filename


def classify_detail(row: dict[str, str]) -> tuple[str, str, str]:
    label = up(row.get("audit_label"))
    adjusted = up(row.get("adjusted_status"))
    result = up(row.get("base_result"))
    if label == "AVOIDED_LOSS":
        return (
            "CONTEXT_FILTER_VALIDATED_CASE",
            "Context downgrade avoided a losing base BET.",
            "Keep as downgrade candidate; do not restore automatically."
        )
    if label == "MISSED_WIN" and adjusted == "BET_DOWNGRADED_TO_REVIEW":
        return (
            "SOFTEN_CONTEXT_DOWNGRADE_CANDIDATE",
            "Context downgrade missed a winning base BET; single sample is not enough for reversal.",
            "Future similar rows should be soft-review or reduced-stake, not automatic hard no-bet, until larger sample confirms."
        )
    if label == "KEPT_WIN":
        return (
            "SHADOW_KEEP_VALIDATED_CASE",
            "Adjusted portfolio kept a winner despite shadow risk.",
            "Keep as low/symbolic or live-confirmation candidate."
        )
    if result == "LOSS" and adjusted in {"BET_KEEP", "BET_REVIEW", "SHADOW_RISK_ONLY"}:
        return (
            "FILTER_FAILED_TO_REMOVE_LOSS",
            "Adjusted portfolio still counted a losing candidate.",
            "Review whether this status needs stricter gating."
        )
    return (
        "MONITOR_ONLY",
        "No strong calibration signal.",
        "Collect more samples."
    )


def build(target_date: str, timezone: str, processed: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    audit = read_rows(file_for(processed, target_date, "vsigma_context_adjustment_result_auditor.csv"))
    details_source = read_rows(file_for(processed, target_date, "vsigma_context_adjustment_result_auditor_details.csv"))
    audit_row = audit[0] if audit else {}

    detail_rows: list[dict[str, object]] = []
    for i, row in enumerate(details_source, start=1):
        c_label, note, treatment = classify_detail(row)
        detail_rows.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "rank": norm(row.get("rank")) or i,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "market_primary": up(row.get("market_primary")),
            "base_result": up(row.get("base_result")),
            "adjusted_status": up(row.get("adjusted_status")),
            "audit_label": up(row.get("audit_label")),
            "audit_effect_units": num(row.get("audit_effect_units"), 0),
            "calibration_label": c_label,
            "calibration_note": note,
            "suggested_future_treatment": treatment,
        })

    base_profit = num(audit_row.get("base_profit_units"), 0)
    adjusted_profit = num(audit_row.get("adjusted_profit_units"), 0)
    delta = num(audit_row.get("net_adjustment_delta_units"), adjusted_profit - base_profit)
    avoided = num(audit_row.get("avoided_loss_units"), 0)
    missed = num(audit_row.get("missed_win_units"), 0)

    if delta > 0 and missed > 0:
        verdict = "FILTER_IMPROVED_BUT_TOO_COARSE"
        policy = "Keep context filter, but split hard downgrade vs reduced-stake review; do not auto-veto all context downgrades from one day."
    elif delta > 0:
        verdict = "FILTER_IMPROVED_DAY"
        policy = "Keep context filter as review gate; collect larger sample before promotion."
    elif missed > avoided:
        verdict = "FILTER_TOO_CONSERVATIVE"
        policy = "Soften context downgrades; require stronger contradiction before hard veto."
    else:
        verdict = "MIXED_MONITOR"
        policy = "Keep monitoring; no rule change from this sample."

    summary = {
        "target_date": target_date,
        "generated_at": generated_at,
        "base_profit_units": round(base_profit, 6),
        "adjusted_profit_units": round(adjusted_profit, 6),
        "net_adjustment_delta_units": round(delta, 6),
        "avoided_loss_units": round(avoided, 6),
        "missed_win_units": round(missed, 6),
        "calibration_verdict": verdict,
        "recommended_policy": policy,
        "min_samples_before_rule_change": MIN_SAMPLES,
        "auto_apply": "NO",
        "production_change": "NO",
        "guardrail_status": "CONTEXT_FILTER_CALIBRATION_ADVISOR_REPORT_ONLY",
    }
    return summary, detail_rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, summary: dict[str, object], details: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Context Filter Calibration Advisor - {target_date}",
        "",
        "## Executive Calibration",
        f"- calibration_verdict: {summary['calibration_verdict']}",
        f"- base_profit_units: {summary['base_profit_units']}",
        f"- adjusted_profit_units: {summary['adjusted_profit_units']}",
        f"- net_adjustment_delta_units: {summary['net_adjustment_delta_units']}",
        f"- avoided_loss_units: {summary['avoided_loss_units']}",
        f"- missed_win_units: {summary['missed_win_units']}",
        f"- recommended_policy: {summary['recommended_policy']}",
        f"- min_samples_before_rule_change: {summary['min_samples_before_rule_change']}",
        f"- calibration_label_counts: {counts(details, 'calibration_label')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Detail Rows",
    ]
    if not details:
        lines.append("- none")
    for d in details:
        lines.append(f"- #{d['rank']} | {d['calibration_label']} | {d['home_team']} vs {d['away_team']} | market={d['market_primary']} | audit={d['audit_label']} | note={d['calibration_note']}")
    lines += ["", "## Guardrails", "- This advisor does not change production behavior.", "- It only recommends how to calibrate context filters after repeated samples."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    summary, details = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_context_filter_calibration_advisor.csv", [summary], SUMMARY_FIELDS)
        write_rows(base / "vsigma_context_filter_calibration_advisor_details.csv", details, DETAIL_FIELDS)
        (base / "vsigma_context_filter_calibration_advisor.md").write_text(md(target_date, summary, details), encoding="utf-8")
    print("=== VSIGMA CONTEXT FILTER CALIBRATION ADVISOR ===")
    print(f"calibration_verdict={summary['calibration_verdict']}")
    print(f"recommended_policy={summary['recommended_policy']}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
