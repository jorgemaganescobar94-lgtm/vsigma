from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date",
    "generated_at",
    "execution_rank",
    "fixture_id",
    "country",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "final_recommendation",
    "execution_verdict",
    "execution_score",
    "primary_edge",
    "primary_model_prob",
    "pick_failure_mode",
    "home_urgency_score",
    "away_urgency_score",
    "home_rank",
    "away_rank",
    "lineup_activation_state",
    "lineup_minutes_to_kickoff",
    "home_lineup_known_starters_count",
    "away_lineup_known_starters_count",
    "availability_known_risk_score",
    "availability_attack_penalty",
    "home_absence_risk_score",
    "away_absence_risk_score",
    "projected_home_goals",
    "projected_away_goals",
    "league_data_reliability_score",
    "recent_stats_quality_flag",
    "lineup_quality_flag",
    "odds_bookmaker_support_count",
    "odds_imp_over25",
    "odds_imp_over15",
    "odds_imp_under35",
    "home_recent_shots_for_pg",
    "away_recent_shots_for_pg",
    "home_recent_shots_against_pg",
    "away_recent_shots_against_pg",
    "home_recent_sot_for_pg",
    "away_recent_sot_for_pg",
    "home_recent_sot_against_pg",
    "away_recent_sot_against_pg",
    "home_recent_corners_for_pg",
    "away_recent_corners_for_pg",
    "home_recent_corners_against_pg",
    "away_recent_corners_against_pg",
    "home_recent_yellow_pg",
    "away_recent_yellow_pg",
    "home_recent_fouls_pg",
    "away_recent_fouls_pg",
    "bridge_source",
    "auto_apply",
    "production_change",
    "guardrail_status",
]
DIAG_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league",
    "source_status", "selector_status", "reason", "vsigma_priority", "market_family_hint",
    "data_quality_score", "league_data_reliability_score", "recent_stats_quality_flag",
    "odds_bookmaker_support_count", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "source_rows", "same_day_rows", "real_shortlist_rows",
    "real_bets_rows", "selector_status_counts", "next_action", "auto_apply", "production_change",
]
BLOCK_TOKENS = {"NO_DATA_BLOCKED", "BLOCKED", "MAX_BLOCK", "HARD_DOWN", "NO_BET"}


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def num(value: object, default: float = 0.0) -> float:
    try:
        text = norm(value)
        if not text or text.lower() == "nan":
            return default
        return float(text)
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_rows(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date", "fixture_datetime_utc"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [row for row in rows if row_day(row) == day]


def choose_market(row: dict[str, str]) -> str:
    for field in ("vsigma_priority", "market_family_hint", "odds_market_translation_hint"):
        value = up(row.get(field))
        if value and value not in {"NO_DATA_BLOCKED", "UNKNOWN", "NONE"}:
            if "OVER" in value:
                return "OVER_1_5" if "1_5" in value or "OVER15" in value else "OVER_2_5"
            if "BTTS" in value:
                return "BTTS_YES"
            if "UNDER" in value:
                return "UNDER_3_5"
            if "HOME" in value and "WIN" in value:
                return "HOME_WIN"
            if "AWAY" in value and "WIN" in value:
                return "AWAY_WIN"
    if num(row.get("odds_imp_over25"), 0) >= 0.56:
        return "OVER_2_5"
    if num(row.get("odds_imp_over15"), 0) >= 0.78:
        return "OVER_1_5"
    return "UNKNOWN"


def is_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(up(row.get(field)) for field in ["vsigma_priority", "market_family_hint", "data_warning", "odds_structure_depth_status"])
    return any(token in joined for token in BLOCK_TOKENS)


def has_sufficient_real_data(row: dict[str, str]) -> tuple[bool, str]:
    if is_blocked(row):
        return False, "blocked by scoring/data warning"
    reliability = num(row.get("league_data_reliability_score"), 0)
    data_quality = num(row.get("data_quality_score"), 0)
    odds_count = num(row.get("odds_bookmaker_support_count"), 0)
    recent_quality = up(row.get("recent_stats_quality_flag"))
    if reliability < 0.70:
        return False, "league reliability below selector floor"
    if data_quality and data_quality < 55:
        return False, "data quality score below selector floor"
    if recent_quality not in {"FULL", "OK_FULL", ""}:
        return False, "recent stats are not full-quality"
    if odds_count < 2:
        return False, "insufficient bookmaker support"
    market = choose_market(row)
    if market == "UNKNOWN":
        return False, "no market family survived source translation"
    return True, "real scored row passed selector floors"


def recommendation(row: dict[str, str]) -> tuple[str, str, str, str]:
    ok, reason = has_sufficient_real_data(row)
    if not ok:
        return "NO_REAL_SHORTLIST", "NO_BET", "0", reason
    reliability = num(row.get("league_data_reliability_score"), 0)
    odds_count = num(row.get("odds_bookmaker_support_count"), 0)
    score = int(55 + min(20, (reliability - 0.70) * 50) + min(10, odds_count * 2))
    if score >= 75:
        return "REAL_SHORTLIST_REVIEW", "BET", str(score), "real scored row reached review floor"
    return "REAL_SHORTLIST_WATCH", "WATCH", str(score), "real scored row reached watch floor only"


def out_row(row: dict[str, str], day: str, generated: str, rank: int, status: str, final: str, score: str, reason: str) -> dict[str, object]:
    market = choose_market(row)
    return {
        "target_date": day,
        "generated_at": generated,
        "execution_rank": rank,
        "fixture_id": norm(row.get("fixture_id")),
        "country": norm(row.get("country")),
        "league": norm(row.get("league")),
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "market_primary": market,
        "final_recommendation": final,
        "execution_verdict": status,
        "execution_score": score,
        "primary_edge": "",
        "primary_model_prob": "",
        "pick_failure_mode": "REAL_SELECTOR_REVIEW_ONLY" if final == "BET" else "REAL_SELECTOR_WATCH_OR_BLOCKED",
        "home_urgency_score": norm(row.get("home_urgency_score")),
        "away_urgency_score": norm(row.get("away_urgency_score")),
        "home_rank": norm(row.get("home_rank")),
        "away_rank": norm(row.get("away_rank")),
        "lineup_activation_state": up(row.get("lineup_activation_state")) or "UNKNOWN",
        "lineup_minutes_to_kickoff": norm(row.get("lineup_minutes_to_kickoff")),
        "home_lineup_known_starters_count": norm(row.get("home_lineup_known_starters_count")),
        "away_lineup_known_starters_count": norm(row.get("away_lineup_known_starters_count")),
        "availability_known_risk_score": norm(row.get("availability_known_risk_score")),
        "availability_attack_penalty": norm(row.get("availability_attack_penalty")),
        "home_absence_risk_score": norm(row.get("home_absence_risk_score")),
        "away_absence_risk_score": norm(row.get("away_absence_risk_score")),
        "projected_home_goals": norm(row.get("projected_home_goals")),
        "projected_away_goals": norm(row.get("projected_away_goals")),
        "league_data_reliability_score": norm(row.get("league_data_reliability_score")),
        "recent_stats_quality_flag": up(row.get("recent_stats_quality_flag")),
        "lineup_quality_flag": up(row.get("lineup_quality_flag")),
        "odds_bookmaker_support_count": norm(row.get("odds_bookmaker_support_count")),
        "odds_imp_over25": norm(row.get("odds_imp_over25")),
        "odds_imp_over15": norm(row.get("odds_imp_over15")),
        "odds_imp_under35": norm(row.get("odds_imp_under35")),
        "home_recent_shots_for_pg": norm(row.get("home_recent_shots_for_pg")),
        "away_recent_shots_for_pg": norm(row.get("away_recent_shots_for_pg")),
        "home_recent_shots_against_pg": norm(row.get("home_recent_shots_against_pg")),
        "away_recent_shots_against_pg": norm(row.get("away_recent_shots_against_pg")),
        "home_recent_sot_for_pg": norm(row.get("home_recent_sot_for_pg")),
        "away_recent_sot_for_pg": norm(row.get("away_recent_sot_for_pg")),
        "home_recent_sot_against_pg": norm(row.get("home_recent_sot_against_pg")),
        "away_recent_sot_against_pg": norm(row.get("away_recent_sot_against_pg")),
        "home_recent_corners_for_pg": norm(row.get("home_recent_corners_for_pg")),
        "away_recent_corners_for_pg": norm(row.get("away_recent_corners_for_pg")),
        "home_recent_corners_against_pg": norm(row.get("home_recent_corners_against_pg")),
        "away_recent_corners_against_pg": norm(row.get("away_recent_corners_against_pg")),
        "home_recent_yellow_pg": norm(row.get("home_recent_yellow_pg")),
        "away_recent_yellow_pg": norm(row.get("away_recent_yellow_pg")),
        "home_recent_fouls_pg": norm(row.get("home_recent_fouls_pg")),
        "away_recent_fouls_pg": norm(row.get("away_recent_fouls_pg")),
        "bridge_source": "REAL_SCORED_SELECTOR",
        "auto_apply": "NO",
        "production_change": "NO",
        "guardrail_status": f"REAL_SELECTOR_{status}; reason={reason}",
    }


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    root = processed / "matches_vsigma_scored_v3.csv"
    dated = processed / "today" / day / "matches_vsigma_scored_v3.csv"
    source = dated if dated.exists() else root
    rows = same_day(read_rows(source), day)
    shortlist: list[dict[str, object]] = []
    bets: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for idx, row in enumerate(rows, start=1):
        status, final, score, reason = recommendation(row)
        if final in {"BET", "WATCH"}:
            item = out_row(row, day, generated, len(shortlist) + 1, status, final, score, reason)
            shortlist.append(item)
            if final == "BET":
                bets.append(item)
        diagnostics.append(
            {
                "target_date": day,
                "generated_at": generated,
                "fixture_id": norm(row.get("fixture_id")),
                "home_team": norm(row.get("home_team")),
                "away_team": norm(row.get("away_team")),
                "league": norm(row.get("league")),
                "source_status": "DATED" if source == dated else "ROOT",
                "selector_status": status,
                "reason": reason,
                "vsigma_priority": up(row.get("vsigma_priority")),
                "market_family_hint": up(row.get("market_family_hint")),
                "data_quality_score": norm(row.get("data_quality_score")),
                "league_data_reliability_score": norm(row.get("league_data_reliability_score")),
                "recent_stats_quality_flag": up(row.get("recent_stats_quality_flag")),
                "odds_bookmaker_support_count": norm(row.get("odds_bookmaker_support_count")),
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )
    summary = {
        "target_date": day,
        "generated_at": generated,
        "source_rows": len(read_rows(source)) if source.exists() else 0,
        "same_day_rows": len(rows),
        "real_shortlist_rows": len(shortlist),
        "real_bets_rows": len(bets),
        "selector_status_counts": counts(diagnostics, "selector_status"),
        "next_action": "No real shortlist rows; keep proxy bridge capped at NO_BET." if not shortlist else "Real shortlist rows created; downstream gates still required.",
        "auto_apply": "NO",
        "production_change": "NO",
    }
    return shortlist, bets, diagnostics, summary


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in c.most_common()) if c else "none"


def md(day: str, summary: dict[str, object], diagnostics: list[dict[str, object]], shortlist: list[dict[str, object]], bets: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Scored-to-Real Shortlist Builder - {day}",
        "",
        "## Summary",
        f"- source_rows: {summary['source_rows']}",
        f"- same_day_rows: {summary['same_day_rows']}",
        f"- real_shortlist_rows: {summary['real_shortlist_rows']}",
        f"- real_bets_rows: {summary['real_bets_rows']}",
        f"- selector_status_counts: {summary['selector_status_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Selector Diagnostics",
    ]
    if not diagnostics:
        lines.append("- none. No same-day scored rows found.")
    for row in diagnostics:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | status={row['selector_status']} | priority={row['vsigma_priority']} | market_hint={row['market_family_hint']} | reason={row['reason']}"
        )
    lines += [
        "",
        "## Real Shortlist Rows",
    ]
    if not shortlist:
        lines.append("- none. No real scored row passed selector floors.")
    for row in shortlist:
        lines.append(f"- {row['home_team']} vs {row['away_team']} | market={row['market_primary']} | final={row['final_recommendation']} | score={row['execution_score']}")
    lines += [
        "",
        "## Real Bets Rows",
    ]
    if not bets:
        lines.append("- none. No row reached real BET floor.")
    for row in bets:
        lines.append(f"- {row['home_team']} vs {row['away_team']} | market={row['market_primary']} | score={row['execution_score']}")
    lines += [
        "",
        "## Guardrails",
        "- This builder only selects real scored rows; it does not use objective proxy rows.",
        "- NO_DATA_BLOCKED or insufficient-data rows are refused.",
        "- Real shortlist rows still require downstream objective, availability, forecast, translator, board and prelock gates.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    shortlist, bets, diagnostics, summary = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_rows(base / "vsigma_real_today_execution_shortlist.csv", shortlist, FIELDS)
        write_rows(base / "vsigma_real_today_execution_bets_only.csv", bets, FIELDS)
        write_rows(base / "vsigma_scored_to_real_shortlist_diagnostic.csv", diagnostics, DIAG_FIELDS)
        write_rows(base / "vsigma_scored_to_real_shortlist_summary.csv", [summary], SUMMARY_FIELDS)
        (base / "vsigma_scored_to_real_shortlist.md").write_text(md(day, summary, diagnostics, shortlist, bets), encoding="utf-8")
        if shortlist:
            write_rows(base / "vsigma_today_execution_shortlist.csv", shortlist, FIELDS)
        if bets:
            write_rows(base / "vsigma_today_execution_bets_only.csv", bets, FIELDS)
    print("=== VSIGMA SCORED TO REAL SHORTLIST ===")
    print(f"same_day_rows={summary['same_day_rows']}")
    print(f"real_shortlist_rows={summary['real_shortlist_rows']}")
    print(f"real_bets_rows={summary['real_bets_rows']}")
    print(f"selector_status_counts={summary['selector_status_counts']}")
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
