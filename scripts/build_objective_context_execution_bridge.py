from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date", "generated_at", "execution_rank", "fixture_id", "country", "league", "home_team", "away_team",
    "market_primary", "final_recommendation", "execution_verdict", "execution_score", "primary_edge",
    "primary_model_prob", "pick_failure_mode", "home_urgency_score", "away_urgency_score", "home_rank",
    "away_rank", "lineup_activation_state", "lineup_minutes_to_kickoff", "home_lineup_known_starters_count",
    "away_lineup_known_starters_count", "availability_known_risk_score", "availability_attack_penalty",
    "home_absence_risk_score", "away_absence_risk_score", "projected_home_goals", "projected_away_goals",
    "league_data_reliability_score", "recent_stats_quality_flag", "lineup_quality_flag",
    "odds_bookmaker_support_count", "odds_imp_over25", "odds_imp_over15", "odds_imp_under35",
    "home_recent_shots_for_pg", "away_recent_shots_for_pg", "home_recent_shots_against_pg",
    "away_recent_shots_against_pg", "home_recent_sot_for_pg", "away_recent_sot_for_pg",
    "home_recent_sot_against_pg", "away_recent_sot_against_pg", "home_recent_corners_for_pg",
    "away_recent_corners_for_pg", "home_recent_corners_against_pg", "away_recent_corners_against_pg",
    "home_recent_yellow_pg", "away_recent_yellow_pg", "home_recent_fouls_pg", "away_recent_fouls_pg",
    "bridge_source", "auto_apply", "production_change", "guardrail_status",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in FIELDS} for row in rows])


def same_day(rows: list[dict[str, str]], target_date: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        day = norm(row.get("target_date") or row.get("date"))[:10]
        if day in {"", target_date}:
            out.append(row)
    return out


def is_proxy(row: dict[str, str]) -> bool:
    marker = " ".join([up(row.get("bridge_source")), up(row.get("guardrail_status")), up(row.get("candidate_origin"))])
    return "BASE_PROXY_FROM_OBJECTIVE_GATE" in marker or "OBJECTIVE_PROXY" in marker or "DIAGNOSTIC_PROXY" in marker


def has_real_shortlist(processed: Path, target_date: str) -> bool:
    candidates = [
        processed / "today" / target_date / "vsigma_real_today_execution_shortlist.csv",
        processed / "today" / target_date / "vsigma_today_execution_shortlist.csv",
    ]
    for path in candidates:
        rows = same_day(read_rows(path), target_date)
        real_rows = [row for row in rows if not is_proxy(row) and up(row.get("final_recommendation")) in {"BET", "WATCH", "REVIEW"}]
        if real_rows:
            return True
    return False


def market_to_projection(market: str) -> tuple[str, str, str, str, str]:
    m = up(market)
    if m == "OVER_2_5":
        return "1.45", "1.20", "0.56", "0.82", "0.64"
    if m == "OVER_1_5":
        return "1.25", "1.05", "0.48", "0.80", "0.70"
    if m == "BTTS_YES":
        return "1.22", "1.14", "0.50", "0.79", "0.66"
    return "1.15", "0.95", "0.45", "0.76", "0.68"


def bridge_row(row: dict[str, str], target_date: str, generated_at: str, rank: int) -> dict[str, str]:
    market = up(row.get("market_primary")) or "UNKNOWN"
    home_goals, away_goals, over25, over15, under35 = market_to_projection(market)
    objective_edge = up(row.get("objective_edge"))
    base_recommendation = up(row.get("base_recommendation")) or "BET"
    final_recommendation = "BET" if base_recommendation == "BET" else "REVIEW"
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "execution_rank": norm(row.get("rank")) or str(rank),
        "fixture_id": norm(row.get("fixture_id")),
        "country": norm(row.get("country")),
        "league": norm(row.get("league")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_primary": market,
        "final_recommendation": final_recommendation,
        "execution_verdict": "OBJECTIVE_CONTEXT_PROXY",
        "execution_score": "62" if final_recommendation == "BET" else "35",
        "primary_edge": "0.09" if final_recommendation == "BET" else "0.02",
        "primary_model_prob": "",
        "pick_failure_mode": "PROXY_CONTEXT_ONLY",
        "home_urgency_score": norm(row.get("home_urgency_score")) or "0",
        "away_urgency_score": norm(row.get("away_urgency_score")) or "0",
        "home_rank": norm(row.get("home_rank")),
        "away_rank": norm(row.get("away_rank")),
        "lineup_activation_state": "INACTIVE",
        "lineup_minutes_to_kickoff": "9999",
        "home_lineup_known_starters_count": "0",
        "away_lineup_known_starters_count": "0",
        "availability_known_risk_score": "0",
        "availability_attack_penalty": "0",
        "home_absence_risk_score": "0",
        "away_absence_risk_score": "0",
        "projected_home_goals": home_goals,
        "projected_away_goals": away_goals,
        "league_data_reliability_score": "0.62",
        "recent_stats_quality_flag": "PROXY",
        "lineup_quality_flag": "PROXY",
        "odds_bookmaker_support_count": "0",
        "odds_imp_over25": over25,
        "odds_imp_over15": over15,
        "odds_imp_under35": under35,
        "home_recent_shots_for_pg": "11.5",
        "away_recent_shots_for_pg": "10.5",
        "home_recent_shots_against_pg": "11.0",
        "away_recent_shots_against_pg": "11.5",
        "home_recent_sot_for_pg": "3.8",
        "away_recent_sot_for_pg": "3.3",
        "home_recent_sot_against_pg": "3.4",
        "away_recent_sot_against_pg": "3.7",
        "home_recent_corners_for_pg": "4.8",
        "away_recent_corners_for_pg": "4.2",
        "home_recent_corners_against_pg": "4.4",
        "away_recent_corners_against_pg": "4.6",
        "home_recent_yellow_pg": "2.1",
        "away_recent_yellow_pg": "2.2",
        "home_recent_fouls_pg": "12.0",
        "away_recent_fouls_pg": "12.0",
        "bridge_source": "vsigma_real_objective_context_gate.csv",
        "auto_apply": "NO",
        "production_change": "NO",
        "guardrail_status": f"BASE_PROXY_FROM_OBJECTIVE_GATE_{objective_edge or 'UNKNOWN'}",
    }


def build(target_date: str, timezone: str, processed: Path) -> tuple[list[dict[str, str]], str]:
    if has_real_shortlist(processed, target_date):
        return [], "REAL_SHORTLIST_PRESENT_SKIP_PROXY_WRITE"
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    source = processed / "today" / target_date / "vsigma_real_objective_context_gate.csv"
    rows = same_day(read_rows(source), target_date)
    out = [bridge_row(row, target_date, generated_at, i) for i, row in enumerate(rows, start=1)]
    return [row for row in out if row.get("fixture_id") and row.get("home_team") and row.get("away_team")], "PROXY_BRIDGE_WRITTEN"


def md(target_date: str, rows: list[dict[str, str]], mode: str) -> str:
    lines = [
        f"# vSIGMA Objective Context Execution Bridge - {target_date}",
        "",
        "## Summary",
        f"- rows_bridged: {len(rows)}",
        "- source: vsigma_real_objective_context_gate.csv",
        "- output: vsigma_today_execution_shortlist.csv only if no real shortlist exists",
        f"- bridge_mode: {mode}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Bridge Rows",
    ]
    if not rows:
        lines.append("- none. Either real shortlist is present or real objective context gate has no bridgeable rows.")
    for row in rows:
        lines.append(
            f"- #{row['execution_rank']} | {row['home_team']} vs {row['away_team']} | market={row['market_primary']} | recommendation={row['final_recommendation']} | guard={row['guardrail_status']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This bridge creates diagnostic/proxy shortlist rows only; it does not create stake permission.",
        "- If a real shortlist exists, proxy writing is skipped to preserve the real candidate path.",
        "- Proxy rows keep lineups inactive and reliability moderate so execution cannot become premium from this bridge alone.",
    ]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows, mode = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        if rows:
            write_rows(base / "vsigma_today_execution_shortlist.csv", rows)
        write_rows(base / "vsigma_objective_context_execution_bridge.csv", rows)
        (base / "vsigma_objective_context_execution_bridge.md").write_text(md(target_date, rows, mode), encoding="utf-8")
    print("=== VSIGMA OBJECTIVE CONTEXT EXECUTION BRIDGE ===")
    print(f"rows_bridged={len(rows)}")
    print(f"bridge_mode={mode}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
