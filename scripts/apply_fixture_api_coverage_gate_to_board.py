from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
BOARD_FIELDS = [
    "target_date", "generated_at", "board_rank", "fixture_id", "home_team", "away_team",
    "final_decision", "board_bucket", "primary_market", "secondary_market", "stake_band",
    "execution_permission", "portfolio_status", "context_level", "forecast_confidence",
    "forecast_warning", "translation_score", "kill_switch", "stat_profile", "key_stat_forecast",
    "prelock_trigger", "live_trigger", "cancel_trigger", "operator_note", "source_guard",
    "auto_apply", "production_change",
]
REPORT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "api_readiness_gate",
    "coverage_score", "original_final_decision", "final_decision", "original_execution_permission",
    "execution_permission", "gate_action", "gate_reason", "missing_blocks", "auto_apply", "production_change",
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


def by_fixture(rows):
    return {s(r.get("fixture_id")): r for r in rows if s(r.get("fixture_id"))}


def append_note(old, note):
    old = s(old)
    if not old:
        return note
    if note in old:
        return old
    return old + "; " + note


def apply_gate(row, cov):
    original_decision = s(row.get("final_decision"))
    original_perm = s(row.get("execution_permission"))
    gate = s(cov.get("api_readiness_gate")) or "UNKNOWN"
    score = s(cov.get("coverage_score"))
    missing = s(cov.get("missing_blocks")) or "unknown"
    action = "PASS"
    reason = "API coverage allows current board state."

    if gate == "LOW_COVERAGE_NO_BET":
        if original_decision != "NO_BET":
            row["final_decision"] = "NO_BET"
            row["board_bucket"] = "BLOCKED"
            row["stake_band"] = "NO_STAKE"
            row["execution_permission"] = "NO"
            row["portfolio_status"] = "API_LOW_COVERAGE_BLOCKED"
            row["kill_switch"] = append_note(row.get("kill_switch"), "API_LOW_COVERAGE")
            action = "DOWNGRADED_TO_NO_BET"
        else:
            row["execution_permission"] = "NO"
            action = "NO_BET_CONFIRMED"
        reason = "API coverage is too weak for reliable execution."
    elif gate == "WAIT_LINEUPS_OR_LIVE_ONLY":
        row["execution_permission"] = "LIVE_ONLY" if original_decision == "LIVE_ONLY" else "NO_PREMATCH"
        row["stake_band"] = "SYMBOLIC_ONLY" if original_decision == "LIVE_ONLY" else "NO_STAKE_OR_SYMBOLIC"
        row["portfolio_status"] = append_note(row.get("portfolio_status"), "WAIT_LINEUPS_OR_LIVE_ONLY")
        row["forecast_warning"] = append_note(row.get("forecast_warning"), "API_LINEUPS_MISSING")
        row["cancel_trigger"] = append_note(row.get("cancel_trigger"), "api coverage gate: wait lineups or live only")
        if original_decision not in {"NO_BET", "LIVE_ONLY", "STAT_WATCH_ONLY", "NO_BET_OR_WATCH"}:
            row["final_decision"] = "LIVE_ONLY"
            row["board_bucket"] = "LIVE_CANDIDATE"
            action = "DOWNGRADED_TO_LIVE_ONLY"
        else:
            action = "PREMATCH_BLOCKED_KEEP_WATCH"
        reason = "Lineups unavailable inside required window; prematch execution blocked."
    elif gate == "EARLY_CANDIDATE_PRELOCK_REQUIRED":
        if original_decision == "NO_BET":
            row["execution_permission"] = "NO"
            action = "NO_BET_UNCHANGED_EARLY"
        else:
            row["execution_permission"] = "PRELOCK_REQUIRED"
            row["stake_band"] = "NO_STAKE_PRELOCK"
            row["portfolio_status"] = append_note(row.get("portfolio_status"), "EARLY_CANDIDATE_PRELOCK_REQUIRED")
            row["forecast_warning"] = append_note(row.get("forecast_warning"), "LINEUPS_NOT_DUE_YET")
            row["prelock_trigger"] = append_note(row.get("prelock_trigger"), "mandatory lineup/availability recheck before lock")
            action = "EARLY_PRELOCK_REQUIRED"
        reason = "Lineups are not due yet; early candidate may be planned but not locked."
    elif gate == "EARLY_WATCH_MORE_DATA_REQUIRED":
        row["execution_permission"] = "NO_PREMATCH"
        row["stake_band"] = "NO_STAKE_OR_SYMBOLIC"
        row["portfolio_status"] = append_note(row.get("portfolio_status"), "EARLY_WATCH_MORE_DATA_REQUIRED")
        row["forecast_warning"] = append_note(row.get("forecast_warning"), "API_EARLY_LOW_SUPPORT")
        action = "EARLY_WATCH_ONLY"
        reason = "Early-day data is not strong enough beyond missing lineups."
    elif gate == "PARTIAL_DATA_REVIEW":
        if original_perm not in {"NO", "NO_PREMATCH", "STAT_WATCH_ONLY", "LIVE_ONLY"}:
            row["execution_permission"] = "MANUAL_REVIEW_ONLY"
        row["forecast_warning"] = append_note(row.get("forecast_warning"), "API_PARTIAL_COVERAGE")
        row["operator_note"] = append_note(row.get("operator_note"), "API partial coverage: require manual review before any stake.")
        action = "MANUAL_REVIEW_ONLY"
        reason = "API coverage is usable but incomplete."
    elif gate == "API_READY":
        action = "API_READY_PASS"
        reason = "API coverage is strong enough for normal model evaluation."
    else:
        row["execution_permission"] = "NO"
        row["stake_band"] = "NO_STAKE"
        row["forecast_warning"] = append_note(row.get("forecast_warning"), "API_COVERAGE_UNKNOWN")
        action = "UNKNOWN_COVERAGE_BLOCK"
        reason = "API coverage matrix missing or unknown for fixture."

    row["operator_note"] = append_note(row.get("operator_note"), f"api_gate={gate}; coverage_score={score}; missing={missing}")
    row["source_guard"] = append_note(row.get("source_guard"), "API_COVERAGE_GATE")
    row["auto_apply"] = "NO"
    row["production_change"] = "NO"
    return original_decision, original_perm, action, reason


def md(day, report):
    c = Counter(r["gate_action"] for r in report)
    lines = [
        f"# vSIGMA API Coverage Gate Applied to Board - {day}", "", "## Summary",
        f"- rows_reviewed: {len(report)}",
        "- gate_actions: " + ("; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"),
        "- auto_apply: NO", "- production_change: NO", "", "## Gate Rows",
    ]
    for r in report:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | api_gate={r['api_readiness_gate']} | action={r['gate_action']} | decision={r['original_final_decision']}->{r['final_decision']} | permission={r['original_execution_permission']}->{r['execution_permission']} | missing={r['missing_blocks']}")
    lines += ["", "## Guardrails", "- Gate blocks or downgrades execution when API coverage is incomplete.", "- Early missing lineups can allow PRELOCK_REQUIRED planning, but never lock.", "- It does not create new picks.", "- It does not execute bets.", "- It does not fabricate unavailable API data."]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    board = read(d(day, "vsigma_daily_execution_board.csv"))
    cov = by_fixture(read(d(day, "vsigma_fixture_api_coverage_matrix.csv")))
    report = []
    for row in board:
        fixture = s(row.get("fixture_id"))
        c = cov.get(fixture, {})
        od, op, action, reason = apply_gate(row, c)
        report.append({
            "target_date": day, "generated_at": ts, "fixture_id": fixture,
            "home_team": s(row.get("home_team")), "away_team": s(row.get("away_team")),
            "api_readiness_gate": s(c.get("api_readiness_gate")) or "UNKNOWN",
            "coverage_score": s(c.get("coverage_score")),
            "original_final_decision": od, "final_decision": s(row.get("final_decision")),
            "original_execution_permission": op, "execution_permission": s(row.get("execution_permission")),
            "gate_action": action, "gate_reason": reason, "missing_blocks": s(c.get("missing_blocks")) or "unknown",
            "auto_apply": "NO", "production_change": "NO",
        })
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_daily_execution_board.csv", board, BOARD_FIELDS)
        write(base / "vsigma_api_coverage_gate_report.csv", report, REPORT_FIELDS)
        (base / "vsigma_api_coverage_gate_report.md").write_text(md(day, report), encoding="utf-8")
    print("=== VSIGMA API COVERAGE GATE TO BOARD ===")
    print(f"rows_reviewed={len(report)}")
    print("gate_actions=" + ("; ".join(f"{k}={v}" for k, v in Counter(r['gate_action'] for r in report).most_common()) if report else "none"))
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
