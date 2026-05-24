from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "final_rank", "fixture_id", "league", "home_team", "away_team",
    "market_primary", "base_final_recommendation", "base_execution_verdict", "base_execution_score",
    "base_primary_edge", "base_model_prob", "context_gate_decision", "objective_override_status",
    "context_objective_edge", "objective_availability_decision", "lineup_status", "availability_status",
    "pick_failure_mode", "adjusted_final_status", "adjusted_reason", "recommended_action",
    "stake_band", "auto_apply", "production_change", "guardrail_status"
]


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


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow({field: r.get(field, "") for field in FIELDS})


def file_for(processed: Path, target_date: str, filename: str) -> Path:
    p = processed / "today" / target_date / filename
    if p.exists():
        return p
    return processed / "governance" / filename


def bets_path(processed: Path, target_date: str) -> Path:
    p = processed / "today" / target_date / "vsigma_today_execution_bets_only.csv"
    if p.exists():
        return p
    p = processed / "today" / target_date / "vsigma_today_execution_shortlist.csv"
    if p.exists():
        return p
    return processed / "vsigma_today_execution_bets_only.csv"


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for r in rows:
        fid = norm(r.get("fixture_id")).replace(".0", "")
        if fid and fid not in out:
            out[fid] = r
    return out


def decide(base: dict[str, str], real: dict[str, str] | None, obj: dict[str, str] | None) -> tuple[str, str, str, str]:
    real_decision = up((real or {}).get("context_gate_decision"))
    obj_decision = up((obj or {}).get("gate_decision"))
    failure = up(base.get("pick_failure_mode"))
    edge = num(base.get("primary_edge"), 0)
    score = num(base.get("execution_score"), 0)
    reasons: list[str] = []

    if real_decision == "CONTEXT_DOWNGRADE":
        reasons.append("real objective context downgraded the base BET")
        return "BET_DOWNGRADED_TO_REVIEW", "; ".join(reasons), "Do not execute as premium; require manual/live context confirmation", "NO_STAKE_OR_SYMBOLIC"

    if obj_decision == "WAIT_PRELOCK":
        reasons.append("objective/availability gate requires prelock or lineup confirmation")
        return "WAIT_PRELOCK", "; ".join(reasons), "Wait for prelock before execution", "NO_PREMATCH_STAKE"

    if obj_decision in {"DOWNGRADE_TO_REVIEW", "CONTEXT_REVIEW_REQUIRED"}:
        reasons.append("objective/availability gate found contradiction or review requirement")
        return "BET_DOWNGRADED_TO_REVIEW", "; ".join(reasons), "Manual review required before any stake", "NO_STAKE_OR_SYMBOLIC"

    if "LOW_CONVERSION" in failure:
        reasons.append("shadow risk: low-conversion pattern")
        return "SHADOW_RISK_ONLY", "; ".join(reasons), "Only execute with stronger live/prelock confirmation", "LOW_OR_SYMBOLIC"

    if up(base.get("final_recommendation")) != "BET":
        reasons.append("base row is not BET")
        return "NO_BET_BASE", "; ".join(reasons), "No action", "NO_STAKE"

    if edge >= 0.18 and score >= 120:
        reasons.append("strong base edge and execution score with no context downgrade")
        return "BET_KEEP", "; ".join(reasons), "Eligible after normal prelock checks", "NORMAL_IF_PRELOCK_OK"

    if edge >= 0.08:
        reasons.append("base edge remains positive but not premium after context checks")
        return "BET_REVIEW", "; ".join(reasons), "Review price/timing before execution", "LOW"

    reasons.append("edge insufficient after context adjustment")
    return "NO_BET_CONTEXT", "; ".join(reasons), "No action", "NO_STAKE"


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    base_rows = [r for r in read_rows(bets_path(processed, target_date)) if up(r.get("final_recommendation")) == "BET"]
    real_rows = index_by_fixture(read_rows(file_for(processed, target_date, "vsigma_real_objective_context_gate.csv")))
    obj_rows = index_by_fixture(read_rows(file_for(processed, target_date, "vsigma_objective_availability_gate.csv")))
    out: list[dict[str, object]] = []

    for base in base_rows:
        fid = norm(base.get("fixture_id")).replace(".0", "")
        real = real_rows.get(fid)
        obj = obj_rows.get(fid)
        status, reason, action, stake = decide(base, real, obj)
        out.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "final_rank": 0,
            "fixture_id": fid,
            "league": norm(base.get("league")),
            "home_team": norm(base.get("home_team")),
            "away_team": norm(base.get("away_team")),
            "market_primary": up(base.get("market_primary")),
            "base_final_recommendation": up(base.get("final_recommendation")),
            "base_execution_verdict": up(base.get("execution_verdict")),
            "base_execution_score": norm(base.get("execution_score")),
            "base_primary_edge": norm(base.get("primary_edge")),
            "base_model_prob": norm(base.get("primary_model_prob")),
            "context_gate_decision": up((real or {}).get("context_gate_decision")),
            "objective_override_status": up((real or {}).get("objective_override_status")),
            "context_objective_edge": up((real or {}).get("objective_edge")),
            "objective_availability_decision": up((obj or {}).get("gate_decision")),
            "lineup_status": up((obj or {}).get("lineup_status")),
            "availability_status": up((obj or {}).get("availability_status")),
            "pick_failure_mode": up(base.get("pick_failure_mode")),
            "adjusted_final_status": status,
            "adjusted_reason": reason,
            "recommended_action": action,
            "stake_band": stake,
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "CONTEXT_ADJUSTED_FINAL_PICKS_REPORT_ONLY",
        })

    priority = {
        "BET_KEEP": 0,
        "BET_REVIEW": 1,
        "SHADOW_RISK_ONLY": 2,
        "WAIT_PRELOCK": 3,
        "BET_DOWNGRADED_TO_REVIEW": 4,
        "NO_BET_CONTEXT": 5,
        "NO_BET_BASE": 6,
    }
    out.sort(key=lambda r: (priority.get(str(r["adjusted_final_status"]), 99), -num(r["base_primary_edge"]), -num(r["base_execution_score"])))
    for i, r in enumerate(out, start=1):
        r["final_rank"] = i
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Context Adjusted Final Picks - {target_date}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- adjusted_status_counts: {counts(rows, 'adjusted_final_status')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Final Adjusted Picks",
    ]
    if not rows:
        lines.append("- none")
    for r in rows:
        lines.append(f"- #{r['final_rank']} | {r['adjusted_final_status']} | {r['home_team']} vs {r['away_team']} | market={r['market_primary']} | stake={r['stake_band']} | reason={r['adjusted_reason']}")
    lines += ["", "## Guardrails", "- This report does not alter production picks automatically.", "- Real objective context and availability gates override base ranking when present."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_context_adjusted_final_picks.csv", rows)
        (base / "vsigma_context_adjusted_final_picks.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA CONTEXT ADJUSTED FINAL PICKS ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"adjusted_status_counts={counts(rows, 'adjusted_final_status')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
