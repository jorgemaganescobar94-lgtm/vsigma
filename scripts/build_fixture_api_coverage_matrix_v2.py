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
    "minutes_to_kickoff", "league_coverage", "recent_stats_coverage", "lineup_coverage",
    "injuries_coverage", "standings_coverage", "odds_coverage", "context_coverage",
    "forecast_coverage", "coverage_score", "missing_blocks", "api_readiness_gate",
    "execution_policy", "operator_note", "auto_apply", "production_change",
]
EARLY_LINEUP_THRESHOLD_MINUTES = 180.0


def s(x): return "" if x is None else str(x).strip()
def num(x, default=0.0):
    try:
        t = s(x)
        return float(t) if t and t.lower() != "nan" else default
    except ValueError:
        return default

def yes(x): return s(x).upper() in {"1", "1.0", "TRUE", "YES", "FULL", "OK", "OK_FULL_STATS", "COVERAGE_RICH"}

def read(path: Path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f: return [dict(r) for r in csv.DictReader(f)]

def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])

def d(day, name): return P / "today" / day / name

def source_rows(day):
    for name in ["matches_vsigma_scored_v3.csv", "vsigma_top_candidates_v3.csv", "matches_league_filtered.csv"]:
        rows = read(d(day, name))
        if rows: return rows, name
    return [], "NONE"

def full_partial(a, b):
    aa, bb = yes(a), yes(b)
    return "FULL" if aa and bb else "PARTIAL" if aa or bb else "NONE"

def lineup_status(row):
    raw = full_partial(row.get("home_lineup_available_flag"), row.get("away_lineup_available_flag"))
    mins = num(row.get("lineup_minutes_to_kickoff"), -9999)
    if raw == "NONE" and mins > EARLY_LINEUP_THRESHOLD_MINUTES:
        return "NOT_DUE_YET"
    return raw

def classify(row):
    league = "FULL" if yes(row.get("league_coverage_rich_flag")) or num(row.get("league_data_reliability_score")) >= .75 else "PARTIAL" if num(row.get("league_data_reliability_score")) > 0 else "NONE"
    stats = "FULL" if s(row.get("recent_stats_quality_flag")).upper() in {"FULL", "OK_FULL_STATS"} else full_partial(row.get("home_recent_stats_available_flag"), row.get("away_recent_stats_available_flag"))
    lineups = lineup_status(row)
    injuries = "FULL" if s(row.get("injuries_quality_flag")).upper() == "FULL" else full_partial(row.get("home_injuries_available_flag"), row.get("away_injuries_available_flag"))
    standings = "FULL" if s(row.get("home_rank")) and s(row.get("away_rank")) and s(row.get("league_team_count")) else "PARTIAL" if s(row.get("home_rank")) or s(row.get("away_rank")) else "NONE"
    odds = "FULL" if s(row.get("odds_context_v3_status")).upper() == "OK" and num(row.get("odds_values_count_v3")) > 0 else "PARTIAL" if num(row.get("odds_values_count_v3")) > 0 else "NONE"
    context = "FULL" if s(row.get("vsigma_pre_score")) and s(row.get("market_family_hint")) else "PARTIAL" if s(row.get("vsigma_priority")) else "NONE"
    forecast = "FULL" if num(row.get("data_quality_score")) > 0 or s(row.get("data_warning")) else "PARTIAL" if s(row.get("market_family_hint")) else "NONE"
    return {"league_coverage":league,"recent_stats_coverage":stats,"lineup_coverage":lineups,"injuries_coverage":injuries,"standings_coverage":standings,"odds_coverage":odds,"context_coverage":context,"forecast_coverage":forecast}

def score(statuses):
    weights = {"league_coverage":10,"recent_stats_coverage":20,"lineup_coverage":20,"injuries_coverage":15,"standings_coverage":15,"odds_coverage":10,"context_coverage":5,"forecast_coverage":5}
    total, missing = 0.0, []
    for k, st in statuses.items():
        w = weights[k]
        if st == "FULL": total += w
        elif st == "PARTIAL": total += w*.5; missing.append(f"{k}=PARTIAL")
        elif st == "NOT_DUE_YET": total += w*.75; missing.append(f"{k}=NOT_DUE_YET")
        else: missing.append(f"{k}=NONE")
    return round(total, 1), missing

def gate(sc, st):
    if st["recent_stats_coverage"] == "NONE" or st["odds_coverage"] == "NONE":
        return "LOW_COVERAGE_NO_BET", "Missing core stats or market data."
    if st["lineup_coverage"] == "NONE":
        return "WAIT_LINEUPS_OR_LIVE_ONLY", "Lineups should be checked before prematch execution."
    if st["lineup_coverage"] == "NOT_DUE_YET":
        if sc >= 70 and st["standings_coverage"] != "NONE" and st["injuries_coverage"] != "NONE":
            return "EARLY_CANDIDATE_PRELOCK_REQUIRED", "Early-day candidate allowed; final lock requires prelock lineup/availability recheck."
        return "EARLY_WATCH_MORE_DATA_REQUIRED", "Early-day watch only; missing supporting data beyond lineups."
    if sc >= 85 and st["injuries_coverage"] != "NONE" and st["standings_coverage"] != "NONE":
        return "API_READY", "Coverage is strong enough for normal model evaluation."
    if sc >= 65:
        return "PARTIAL_DATA_REVIEW", "Coverage is usable but incomplete."
    return "LOW_COVERAGE_NO_BET", "Coverage is too weak for reliable execution."

def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, src = source_rows(day); out=[]
    for r in rows:
        st = classify(r); sc, miss = score(st); g, pol = gate(sc, st)
        out.append({"target_date":day,"generated_at":ts,"fixture_id":s(r.get("fixture_id")),"league":s(r.get("league")),"home_team":s(r.get("home_team")),"away_team":s(r.get("away_team")),"minutes_to_kickoff":num(r.get("lineup_minutes_to_kickoff"), -1),**st,"coverage_score":sc,"missing_blocks":"; ".join(miss) if miss else "none","api_readiness_gate":g,"execution_policy":pol,"operator_note":f"source={src}; lineups are time-aware: NOT_DUE_YET does not hard-block early-day shortlist.","auto_apply":"NO","production_change":"NO"})
    return out

def counts(rows, field):
    c=Counter(str(r.get(field) or "UNKNOWN") for r in rows); return "; ".join(f"{k}={v}" for k,v in c.most_common()) if c else "none"

def md(day, rows):
    lines=[f"# vSIGMA Fixture API Coverage Matrix v2 - {day}","","## Summary",f"- fixtures_reviewed: {len(rows)}",f"- api_readiness_gates: {counts(rows,'api_readiness_gate')}",f"- lineup_coverage: {counts(rows,'lineup_coverage')}",f"- recent_stats_coverage: {counts(rows,'recent_stats_coverage')}",f"- injuries_coverage: {counts(rows,'injuries_coverage')}",f"- standings_coverage: {counts(rows,'standings_coverage')}",f"- odds_coverage: {counts(rows,'odds_coverage')}","- auto_apply: NO","- production_change: NO","","## Fixture Coverage"]
    for r in rows: lines.append(f"- {r['home_team']} vs {r['away_team']} | gate={r['api_readiness_gate']} | score={r['coverage_score']} | mins_to_kickoff={r['minutes_to_kickoff']} | stats={r['recent_stats_coverage']} | lineups={r['lineup_coverage']} | injuries={r['injuries_coverage']} | standings={r['standings_coverage']} | odds={r['odds_coverage']} | missing={r['missing_blocks']}")
    lines += ["","## Guardrails","- Matrix is diagnostic and gating-oriented.","- It does not execute bets.","- It does not fabricate unavailable API data.","- Early-day missing lineups become NOT_DUE_YET, not automatic hard block.","- Final lock still requires prelock lineup/availability recheck."]
    return "\n".join(lines)+"\n"

def run(day,tz):
    day=date.fromisoformat(day).isoformat(); rows=build(day,tz)
    for base in [P/"today"/day, P/"governance"]:
        write(base/"vsigma_fixture_api_coverage_matrix.csv", rows, FIELDS); (base/"vsigma_fixture_api_coverage_matrix.md").write_text(md(day,rows),encoding="utf-8")
    print("=== VSIGMA FIXTURE API COVERAGE MATRIX V2 ==="); print(f"fixtures_reviewed={len(rows)}"); print(f"api_readiness_gates={counts(rows,'api_readiness_gate')}"); print("auto_apply=NO"); print("production_change=NO")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--date",required=True); p.add_argument("--timezone",default="Atlantic/Canary"); a=p.parse_args(); run(a.date,a.timezone)
if __name__ == "__main__": main()
