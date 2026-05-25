from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "gate_rank", "fixture_id", "league", "home_team", "away_team",
    "market_primary", "base_final_recommendation", "objective_status", "availability_status",
    "lineup_status", "gate_decision", "gate_reason", "recommended_action", "home_urgency_score",
    "away_urgency_score", "home_rank", "away_rank", "lineup_activation_state",
    "lineup_minutes_to_kickoff", "availability_known_risk_score", "availability_attack_penalty",
    "home_absence_risk_score", "away_absence_risk_score", "pick_failure_mode", "auto_apply",
    "production_change", "guardrail_status"
]
SIDE_HOME = {"HOME_WIN", "HOME_DNB", "HOME_TEAM_TOTAL", "HOME_OVER_0_5", "HOME_OVER_1_5"}
SIDE_AWAY = {"AWAY_WIN", "AWAY_DNB", "AWAY_TEAM_TOTAL", "AWAY_OVER_0_5", "AWAY_OVER_1_5"}
GOAL_MARKETS = {"OVER_1_5", "OVER_2_5", "BTTS_YES"}


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
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def source(processed: Path, target_date: str) -> Path | None:
    for filename in ("vsigma_today_execution_bets_only.csv", "vsigma_today_execution_shortlist.csv"):
        p = processed / "today" / target_date / filename
        if p.exists():
            return p
    return None


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day_rows(data: list[dict[str, str]], target_date: str) -> list[dict[str, str]]:
    return [r for r in data if row_day(r) in {"", target_date}]


def chosen_side(market: str) -> str:
    m = up(market)
    if m in SIDE_HOME:
        return "HOME"
    if m in SIDE_AWAY:
        return "AWAY"
    if m in GOAL_MARKETS:
        return "BOTH"
    return "UNKNOWN"


def objective_status(row: dict[str, str]) -> tuple[str, str]:
    h = num(row.get("home_urgency_score"), 0)
    a = num(row.get("away_urgency_score"), 0)
    side = chosen_side(row.get("market_primary"))
    if side == "HOME":
        if h > a:
            return "OBJECTIVE_SUPPORTS_PICK", "home urgency is stronger than away urgency"
        if a > h:
            return "OBJECTIVE_CONFLICT", "away urgency is stronger than selected home-side market"
        return "OBJECTIVE_NEUTRAL_OR_UNKNOWN", "home and away urgency are similar or unknown"
    if side == "AWAY":
        if a > h:
            return "OBJECTIVE_SUPPORTS_PICK", "away urgency is stronger than home urgency"
        if h > a:
            return "OBJECTIVE_CONFLICT", "home urgency is stronger than selected away-side market"
        return "OBJECTIVE_NEUTRAL_OR_UNKNOWN", "home and away urgency are similar or unknown"
    if side == "BOTH":
        if h > 0 or a > 0:
            return "OBJECTIVE_SUPPORTS_TEMPO", "at least one team has table urgency that can support tempo"
        return "OBJECTIVE_NEUTRAL_OR_UNKNOWN", "no strong urgency signal for tempo market"
    return "OBJECTIVE_PROXY_ONLY", "market side cannot be mapped to a clean objective signal"


def lineup_status(row: dict[str, str]) -> tuple[str, str]:
    state = up(row.get("lineup_activation_state"))
    minutes = num(row.get("lineup_minutes_to_kickoff"), 9999)
    hxi = num(row.get("home_lineup_known_starters_count"), 0)
    axi = num(row.get("away_lineup_known_starters_count"), 0)
    if hxi >= 10 and axi >= 10:
        return "LINEUPS_CONFIRMED", "both starting XIs mostly known"
    if state == "INACTIVE" and minutes > 90:
        return "WAIT_PRELOCK", "lineups are inactive and fixture is outside prelock window"
    if state == "INACTIVE":
        return "LINEUPS_NOT_CONFIRMED", "lineups are still inactive"
    return "LINEUP_PROXY_ONLY", "lineup status is partial or proxy-only"


def availability_status(row: dict[str, str]) -> tuple[str, str]:
    total_risk = num(row.get("availability_known_risk_score"), 0)
    attack_penalty = num(row.get("availability_attack_penalty"), 0)
    home_abs = num(row.get("home_absence_risk_score"), 0)
    away_abs = num(row.get("away_absence_risk_score"), 0)
    market = up(row.get("market_primary"))
    side = chosen_side(market)
    if attack_penalty >= 2 and market in GOAL_MARKETS:
        return "AVAILABILITY_CONFLICT", "attacking availability penalty conflicts with goals market"
    if side == "HOME" and home_abs >= 10:
        return "AVAILABILITY_RISK_ON_PICK_SIDE", "home-side market has high home absence risk"
    if side == "AWAY" and away_abs >= 10:
        return "AVAILABILITY_RISK_ON_PICK_SIDE", "away-side market has high away absence risk"
    if total_risk >= 20:
        return "AVAILABILITY_ELEVATED_BOTH", "combined availability risk is elevated"
    if home_abs or away_abs or total_risk:
        return "AVAILABILITY_REPORTED_ADVISORY", "availability risk exists but is not a hard contradiction"
    return "AVAILABILITY_UNKNOWN_OR_CLEAN", "no strong availability contradiction detected"


def gate(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    obj, obj_reason = objective_status(row)
    lin, lin_reason = lineup_status(row)
    av, av_reason = availability_status(row)
    failure = up(row.get("pick_failure_mode"))
    market = up(row.get("market_primary"))
    reasons = [obj_reason, lin_reason, av_reason]
    if lin == "WAIT_PRELOCK":
        return obj, av, lin, "WAIT_PRELOCK", "; ".join(reasons), "Wait for lineups/prelock before execution"
    if obj == "OBJECTIVE_CONFLICT" and av in {"AVAILABILITY_RISK_ON_PICK_SIDE", "AVAILABILITY_ELEVATED_BOTH"}:
        return obj, av, lin, "DOWNGRADE_TO_REVIEW", "; ".join(reasons), "Do not execute as premium without manual context check"
    if obj == "OBJECTIVE_CONFLICT":
        return obj, av, lin, "CONTEXT_REVIEW_REQUIRED", "; ".join(reasons), "Verify objective truth before execution"
    if av == "AVAILABILITY_CONFLICT":
        return obj, av, lin, "DOWNGRADE_TO_REVIEW", "; ".join(reasons), "Availability contradicts market thesis"
    if "LOW_CONVERSION" in failure and market in GOAL_MARKETS:
        return obj, av, lin, "SHADOW_RISK_REVIEW", "; ".join(reasons), "Allow only with stronger live/prelock confirmation"
    if obj.startswith("OBJECTIVE_SUPPORTS") and lin in {"LINEUPS_CONFIRMED", "LINEUPS_NOT_CONFIRMED", "LINEUP_PROXY_ONLY"}:
        return obj, av, lin, "OBJECTIVE_SUPPORTED_KEEP", "; ".join(reasons), "Keep candidate, but respect prelock/lineup confirmation"
    return obj, av, lin, "KEEP_MONITOR", "; ".join(reasons), "No hard objective or availability contradiction found"


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    src = source(processed, target_date)
    if src is None:
        return []
    rows = [
        r for r in same_day_rows(read_rows(src), target_date)
        if up(r.get("final_recommendation")) == "BET"
    ]
    out: list[dict[str, object]] = []
    for r in rows:
        obj, av, lin, decision, reason, action = gate(r)
        out.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "gate_rank": norm(r.get("execution_rank")) or len(out) + 1,
            "fixture_id": norm(r.get("fixture_id")),
            "league": norm(r.get("league")),
            "home_team": norm(r.get("home_team")),
            "away_team": norm(r.get("away_team")),
            "market_primary": up(r.get("market_primary")),
            "base_final_recommendation": up(r.get("final_recommendation")),
            "objective_status": obj,
            "availability_status": av,
            "lineup_status": lin,
            "gate_decision": decision,
            "gate_reason": reason,
            "recommended_action": action,
            "home_urgency_score": norm(r.get("home_urgency_score")),
            "away_urgency_score": norm(r.get("away_urgency_score")),
            "home_rank": norm(r.get("home_rank")),
            "away_rank": norm(r.get("away_rank")),
            "lineup_activation_state": up(r.get("lineup_activation_state")),
            "lineup_minutes_to_kickoff": norm(r.get("lineup_minutes_to_kickoff")),
            "availability_known_risk_score": norm(r.get("availability_known_risk_score")),
            "availability_attack_penalty": norm(r.get("availability_attack_penalty")),
            "home_absence_risk_score": norm(r.get("home_absence_risk_score")),
            "away_absence_risk_score": norm(r.get("away_absence_risk_score")),
            "pick_failure_mode": up(r.get("pick_failure_mode")),
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "DATED_SOURCE_ONLY_OBJECTIVE_AVAILABILITY_GATE",
        })
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Objective Availability Gate - {target_date}", "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- gate_decision_counts: {counts(rows, 'gate_decision')}",
        f"- objective_status_counts: {counts(rows, 'objective_status')}",
        f"- availability_status_counts: {counts(rows, 'availability_status')}",
        "- source_guard: DATED_INPUT_ONLY",
        "- auto_apply: NO",
        "- production_change: NO", "",
        "## Gate Rows",
    ]
    if not rows:
        lines.append("- none. Missing dated execution source or no same-date BET rows; root fallback refused.")
    for r in rows:
        lines.append(f"- #{r['gate_rank']} | {r['gate_decision']} | {r['home_team']} vs {r['away_team']} | market={r['market_primary']} | objective={r['objective_status']} | availability={r['availability_status']} | lineup={r['lineup_status']} | action={r['recommended_action']}")
    lines += ["", "## Guardrails", "- This gate refuses root-level execution fallback.", "- This gate does not change production picks automatically.", "- Objective and availability conflicts require prelock/manual review before premium execution."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_objective_availability_gate.csv", rows)
        (base / "vsigma_objective_availability_gate.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA OBJECTIVE AVAILABILITY GATE ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"gate_decision_counts={counts(rows, 'gate_decision')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
