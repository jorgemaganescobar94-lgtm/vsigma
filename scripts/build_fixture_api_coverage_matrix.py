from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "home_team", "away_team",
    "league_coverage", "recent_stats_coverage", "lineup_coverage", "injuries_coverage",
    "standings_coverage", "odds_coverage", "context_coverage", "forecast_coverage",
    "coverage_score", "missing_blocks", "api_readiness_gate", "execution_policy",
    "operator_note", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


def n(x, default=0.0):
    try:
        t = s(x)
        return float(t) if t and t.lower() != "nan" else default
    except ValueError:
        return default


def yes(x) -> bool:
    return s(x).upper() in {"1", "1.0", "TRUE", "YES", "FULL", "OK", "OK_FULL_STATS", "COVERAGE_RICH"}


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
    for name in ["matches_vsigma_scored_v3.csv", "vsigma_top_candidates_v3.csv", "matches_league_filtered.csv"]:
        rows = read(d(day, name))
        if rows:
            return rows, name
    return [], "NONE"


def status_full_partial(home_flag, away_flag, full_label="FULL", partial_label="PARTIAL", none_label="NONE"):
    h = yes(home_flag)
    a = yes(away_flag)
    if h and a:
        return full_label
    if h or a:
        return partial_label
    return none_label


def classify(row):
    league = "FULL" if yes(row.get("league_coverage_rich_flag")) or n(row.get("league_data_reliability_score")) >= 0.75 else "PARTIAL" if n(row.get("league_data_reliability_score")) > 0 else "NONE"
    stats = "FULL" if s(row.get("recent_stats_quality_flag")).upper() in {"FULL", "OK_FULL_STATS"} else status_full_partial(row.get("home_recent_stats_available_flag"), row.get("away_recent_stats_available_flag"))
    lineups = status_full_partial(row.get("home_lineup_available_flag"), row.get("away_lineup_available_flag"))
    injuries = "FULL" if s(row.get("injuries_quality_flag")).upper() == "FULL" else status_full_partial(row.get("home_injuries_available_flag"), row.get("away_injuries_available_flag"))
    standings = "FULL" if s(row.get("home_rank")) and s(row.get("away_rank")) and s(row.get("league_team_count")) else "PARTIAL" if s(row.get("home_rank")) or s(row.get("away_rank")) else "NONE"
    odds = "FULL" if s(row.get("odds_context_v3_status")).upper() == "OK" and n(row.get("odds_values_count_v3")) > 0 else "PARTIAL" if n(row.get("odds_values_count_v3")) > 0 else "NONE"
    context = "FULL" if s(row.get("vsigma_pre_score")) and s(row.get("market_family_hint")) else "PARTIAL" if s(row.get("vsigma_priority")) else "NONE"
    forecast = "FULL" if n(row.get("data_quality_score")) > 0 or s(row.get("data_warning")) else "PARTIAL" if s(row.get("market_family_hint")) else "NONE"
    return league, stats, lineups, injuries, standings, odds, context, forecast


def score(statuses):
    weights = {
        "league_coverage": 10,
        "recent_stats_coverage": 20,
        "lineup_coverage": 20,
        "injuries_coverage": 15,
        "standings_coverage": 15,
        "odds_coverage": 10,
        "context_coverage": 5,
        "forecast_coverage": 5,
    }
    total = 0.0
    missing = []
    for key, st in statuses.items():
        w = weights[key]
        if st == "FULL":
            total += w
        elif st == "PARTIAL":
            total += w * 0.5
            missing.append(f"{key}=PARTIAL")
        else:
            missing.append(f"{key}=NONE")
    return round(total, 1), missing


def gate(score_value, statuses):
    if statuses["lineup_coverage"] == "NONE":
        return "WAIT_LINEUPS_OR_LIVE_ONLY", "No prematch stake; require lineups or live validation."
    if statuses["recent_stats_coverage"] == "NONE" or statuses["odds_coverage"] == "NONE":
        return "LOW_COVERAGE_NO_BET", "Missing core stats or market data."
    if score_value >= 85 and statuses["injuries_coverage"] != "NONE" and statuses["standings_coverage"] != "NONE":
        return "API_READY", "Coverage is strong enough for normal model evaluation."
    if score_value >= 65:
        return "PARTIAL_DATA_REVIEW", "Coverage is usable but must remain cautious."
    return "LOW_COVERAGE_NO_BET", "Coverage is too weak for reliable execution."


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, src = source_rows(day)
    out = []
    for r in rows:
        league, stats, lineups, injuries, standings, odds, context, forecast = classify(r)
        statuses = {
            "league_coverage": league,
            "recent_stats_coverage": stats,
            "lineup_coverage": lineups,
            "injuries_coverage": injuries,
            "standings_coverage": standings,
            "odds_coverage": odds,
            "context_coverage": context,
            "forecast_coverage": forecast,
        }
        sc, missing = score(statuses)
        g, policy = gate(sc, statuses)
        out.append({
            "target_date": day, "generated_at": ts, "fixture_id": s(r.get("fixture_id")),
            "league": s(r.get("league")), "home_team": s(r.get("home_team")), "away_team": s(r.get("away_team")),
            **statuses,
            "coverage_score": sc,
            "missing_blocks": "; ".join(missing) if missing else "none",
            "api_readiness_gate": g,
            "execution_policy": policy,
            "operator_note": f"source={src}; extract all available API blocks; unavailable blocks must gate stake.",
            "auto_apply": "NO", "production_change": "NO",
        })
    return out


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, rows):
    lines = [
        f"# vSIGMA Fixture API Coverage Matrix - {day}", "", "## Summary",
        f"- fixtures_reviewed: {len(rows)}",
        f"- api_readiness_gates: {counts(rows, 'api_readiness_gate')}",
        f"- lineup_coverage: {counts(rows, 'lineup_coverage')}",
        f"- recent_stats_coverage: {counts(rows, 'recent_stats_coverage')}",
        f"- injuries_coverage: {counts(rows, 'injuries_coverage')}",
        f"- standings_coverage: {counts(rows, 'standings_coverage')}",
        f"- odds_coverage: {counts(rows, 'odds_coverage')}",
        "- auto_apply: NO", "- production_change: NO", "", "## Fixture Coverage",
    ]
    for r in rows:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | gate={r['api_readiness_gate']} | score={r['coverage_score']} | stats={r['recent_stats_coverage']} | lineups={r['lineup_coverage']} | injuries={r['injuries_coverage']} | standings={r['standings_coverage']} | odds={r['odds_coverage']} | missing={r['missing_blocks']}")
    lines += ["", "## Guardrails", "- Matrix is diagnostic and gating-oriented.", "- It does not execute bets.", "- It does not fabricate unavailable API data.", "- Missing lineups or low coverage must prevent strong prematch execution."]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_fixture_api_coverage_matrix.csv", rows, FIELDS)
        (base / "vsigma_fixture_api_coverage_matrix.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA FIXTURE API COVERAGE MATRIX ===")
    print(f"fixtures_reviewed={len(rows)}")
    print(f"api_readiness_gates={counts(rows, 'api_readiness_gate')}")
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
