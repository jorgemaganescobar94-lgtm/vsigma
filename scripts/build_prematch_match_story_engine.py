from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = ["day","created_at","fixture_id","home","away","xi_ok","home_shape","away_shape","scores","main_result","goal_band","scenario","confidence","note"]
SUM_FIELDS = ["day","created_at","rows","xi_ok_rows","scenario_counts","result_counts"]

def s(v): return "" if v is None else str(v).strip()
def u(v): return s(v).upper()
def num(v):
    try: return float(s(v) or 0)
    except ValueError: return 0.0

def rows(p):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def load(a,b): return rows(a) or rows(b)
def write(p, rs, fs):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fs); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fs} for r in rs])
def cnt(rs,k):
    c=Counter(str(r.get(k) or "UNKNOWN") for r in rs)
    return "; ".join(f"{a}={b}" for a,b in c.most_common()) if c else "none"
def side(ls,fid,side): return [r for r in ls if s(r.get("fixture_id"))==fid and u(r.get("row_type"))=="START_XI" and u(r.get("team_side")).startswith(u(side))]
def first(rs,k):
    for r in rs:
        if s(r.get(k)): return s(r.get(k))
    return ""
def score_result(score):
    try:
        a,b=score.split("-"); a=int(a); b=int(b)
        if a>b: return "HOME"
        if b>a: return "AWAY"
        return "DRAW"
    except Exception: return "UNKNOWN"
def result_from_scores(text):
    parts=[p.strip() for p in s(text).split("/") if p.strip()]
    c=Counter(score_result(p.split()[0]) for p in parts)
    if not c: return "UNKNOWN"
    top=c.most_common(1)[0][0]
    if top=="AWAY" and c.get("DRAW",0)>0: return "AWAY_OR_DRAW"
    if top=="HOME" and c.get("DRAW",0)>0: return "HOME_OR_DRAW"
    return top
def goal_band(mid):
    if mid>=3.25: return "HIGH_GOALS"
    if mid>=2.65: return "OPEN_GOALS"
    if mid>=2.25: return "MODERATE_GOALS"
    return "LOW_GOALS"
def story(board, fc, ls, day, now):
    fid=s(board.get("fixture_id")); h=side(ls,fid,"home"); a=side(ls,fid,"away")
    xi=len(h)==11 and len(a)==11
    hs=first(h,"formation"); av=first(a,"formation")
    scores=s(fc.get("modal_scoreline")) or "NO_SCORE"
    mid=num(fc.get("total_goals_mid")); sot=num(fc.get("total_sot_mid"))
    both=u(fc.get("both_teams_threat_level"))=="BOTH_TEAMS_THREAT"
    bump=0.0
    if xi: bump+=0.05
    if hs.endswith("-2") and av.endswith("-2"): bump+=0.20
    if both: bump+=0.10
    if sot>=8: bump+=0.05
    adj=mid+bump
    scen="BALANCED_OPEN_GAME" if both and adj>=2.65 else ("OPEN_GAME" if adj>=2.65 else "CONTROLLED_GAME")
    return {"day":day,"created_at":now,"fixture_id":fid,"home":s(board.get("home_team")),"away":s(board.get("away_team")),"xi_ok":"YES" if xi else "NO","home_shape":hs,"away_shape":av,"scores":scores,"main_result":result_from_scores(scores),"goal_band":goal_band(adj),"scenario":scen,"confidence":s(fc.get("forecast_confidence") or board.get("forecast_confidence")),"note":f"base_mid={mid:.2f}; lineup_adj={bump:.2f}; adjusted_mid={adj:.2f}"}
def md(day, rs, sm):
    out=[f"# Prematch Match Story Engine - {day}","","## Summary",f"- rows: {sm['rows']}",f"- xi_ok_rows: {sm['xi_ok_rows']}",f"- scenario_counts: {sm['scenario_counts']}",f"- result_counts: {sm['result_counts']}","","## Matches"]
    for r in rs: out.append(f"- {r['home']} vs {r['away']} | XI={r['xi_ok']} | shapes={r['home_shape']}/{r['away_shape']} | result={r['main_result']} | scores={r['scores']} | goals={r['goal_band']} | scenario={r['scenario']} | {r['note']}")
    return "\n".join(out)+"\n"
def run(day,tz,base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    b=load(base/"today"/day/"vsigma_daily_execution_board_lineup_bridged.csv", base/"governance"/"vsigma_daily_execution_board_lineup_bridged.csv") or load(base/"today"/day/"vsigma_daily_execution_board.csv", base/"governance"/"vsigma_daily_execution_board.csv")
    l=load(base/"today"/day/"vsigma_forced_api_board_fixture_lineups.csv", base/"governance"/"vsigma_forced_api_board_fixture_lineups.csv")
    f={s(r.get("fixture_id")):r for r in load(base/"today"/day/"vsigma_match_stat_forecasts.csv", base/"governance"/"vsigma_match_stat_forecasts.csv")}
    out=[story(r,f.get(s(r.get("fixture_id")),{}),l,day,now) for r in b]
    sm={"day":day,"created_at":now,"rows":len(out),"xi_ok_rows":sum(1 for r in out if r["xi_ok"]=="YES"),"scenario_counts":cnt(out,"scenario"),"result_counts":cnt(out,"main_result")}
    for p in [base/"today"/day, base/"governance"]:
        write(p/"vsigma_prematch_match_story_engine.csv", out, FIELDS); write(p/"vsigma_prematch_match_story_engine_summary.csv", [sm], SUM_FIELDS); (p/"vsigma_prematch_match_story_engine.md").write_text(md(day,out,sm), encoding="utf-8")
    print("Prematch story engine built")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.timezone,a.processed_dir)
