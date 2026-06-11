from __future__ import annotations

import argparse
import csv
import json
import os
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = ["target_date","generated_at","fixture_id","home_team","away_team","league","country","fixture_status","fixture_date","xi_status","xi_source","home_shape","away_shape","home_prob","draw_prob","away_prob","result_forecast","scorelines","goal_profile","scenario","confidence","forecast_note","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","query_home","query_away","fixture_found","rows","next_action","auto_apply","production_change"]
DONE = {"FT","AET","PEN"}

def clean(x):
    x = unicodedata.normalize("NFKD", str(x or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", x).strip()
def slug(x): return re.sub(r"[^a-z0-9]+", "_", clean(x)).strip("_") or "fixture"
def api_key():
    for k in ["APISPORTS_KEY","API_SPORTS_KEY","API_FOOTBALL_KEY","APIFOOTBALL_KEY","API_FOOTBALL_API_KEY","RAPIDAPI_KEY","X_RAPIDAPI_KEY"]:
        if os.getenv(k): return os.getenv(k)
    return ""
def call(path, params, key):
    url = "https://v3.football.api-sports.io/" + path + "?" + urlencode(params)
    req = Request(url, headers={"x-apisports-key": key})
    with urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))
def sim(a,b):
    a=set(clean(a).split()); b=set(clean(b).split())
    return len(a & b) / max(1, len(a | b))
def find_fixture(day, home, away, key):
    data = call("fixtures", {"date": day}, key).get("response") or []
    best=None; best_score=-1
    for fx in data:
        teams=fx.get("teams") or {}; h=(teams.get("home") or {}).get("name",""); a=(teams.get("away") or {}).get("name","")
        score=max(sim(home,h)+sim(away,a), sim(home,a)+sim(away,h))
        if score>best_score:
            best=fx; best_score=score
    return best if best_score >= 0.35 else None
def implied_from_odds(fixture_id, key):
    try:
        resp = call("odds", {"fixture": fixture_id}, key).get("response") or []
    except Exception:
        return None
    vals=[]
    for item in resp:
        for book in item.get("bookmakers") or []:
            for bet in book.get("bets") or []:
                name=clean(bet.get("name"))
                if name in {"match winner", "1x2", "fulltime result"}:
                    prices={clean(v.get("value")): v.get("odd") for v in bet.get("values") or []}
                    def fl(x):
                        try: return float(x)
                        except Exception: return 0.0
                    h=fl(prices.get("home") or prices.get("1")); d=fl(prices.get("draw") or prices.get("x")); a=fl(prices.get("away") or prices.get("2"))
                    if h and d and a: vals.append((h,d,a))
    if not vals: return None
    ih=sum(1/v[0] for v in vals)/len(vals); idr=sum(1/v[1] for v in vals)/len(vals); ia=sum(1/v[2] for v in vals)/len(vals)
    total=ih+idr+ia
    return (round(ih/total,3), round(idr/total,3), round(ia/total,3))
def lineups(fixture_id, key):
    try:
        resp=call("fixtures/lineups", {"fixture": fixture_id}, key).get("response") or []
    except Exception:
        return "NO_XI", "", "", "NONE"
    if len(resp) >= 2:
        starts=[len(x.get("startXI") or []) for x in resp[:2]]
        if all(n == 11 for n in starts):
            return "OFFICIAL_XI", resp[0].get("formation") or "", resp[1].get("formation") or "", "API_OFFICIAL_LINEUPS"
    return "NO_XI", "", "", "NONE"
def probable_xi(day, home, away, base):
    file_slug=slug(home+"_vs_"+away)
    p=base/"today"/day/f"vsigma_adhoc_probable_xi_{file_slug}.csv"
    if not p.exists(): return "NO_XI", "", "", "NONE"
    with p.open("r", encoding="utf-8-sig", newline="") as h:
        rows=[dict(r) for r in csv.DictReader(h)]
    if len(rows) < 2: return "NO_XI", "", "", "NONE"
    home_row=next((r for r in rows if clean(r.get("team_side"))=="home"), rows[0])
    away_row=next((r for r in rows if clean(r.get("team_side"))=="away"), rows[1])
    status="ESTIMATED_XI" if "ESTIMATED" in str(home_row.get("xi_status")) and "ESTIMATED" in str(away_row.get("xi_status")) else "NO_XI"
    return status, home_row.get("formation", ""), away_row.get("formation", ""), "API_SQUAD_HEURISTIC"
def forecast(probs, xi_status, hs, aw):
    hp,dp,ap=probs
    if hp >= ap + 0.12:
        result="HOME_OR_DRAW"; scores="1-0 / 1-1 / 2-0"
    elif ap >= hp + 0.12:
        result="AWAY_OR_DRAW"; scores="0-1 / 1-1 / 0-2"
    else:
        result="DRAW_LEAN"; scores="1-1 / 0-0 / 1-0"
    if max(hp,ap) >= 0.55 and dp <= 0.28:
        goal="MODERATE_GOALS"; scen="FAVORITE_CONTROL_GAME"
    elif dp >= 0.32:
        goal="LOW_TO_MODERATE_GOALS"; scen="TIGHT_BALANCED_GAME"
    else:
        goal="MODERATE_GOALS"; scen="CONTROLLED_GAME"
    if xi_status in {"OFFICIAL_XI","ESTIMATED_XI"} and hs.endswith("-2") and aw.endswith("-2"):
        goal="OPEN_GOALS" if goal == "MODERATE_GOALS" else goal
        scen="MORE_OPEN_FROM_SHAPES" if xi_status == "OFFICIAL_XI" else "ESTIMATED_MORE_OPEN_FROM_SHAPES"
    if xi_status == "OFFICIAL_XI":
        conf="HIGH" if max(hp,dp,ap) >= 0.55 else "MEDIUM"
    elif xi_status == "ESTIMATED_XI":
        conf="MEDIUM" if max(hp,dp,ap) >= 0.55 else "LOW"
    else:
        conf="MEDIUM" if max(hp,dp,ap) >= 0.42 else "LOW"
    return result,scores,goal,scen,conf
def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def md(row, summary):
    lines=[f"# vSIGMA Ad Hoc Fixture Forecast - {row.get('target_date')}","","## Summary",f"- fixture_found: {summary['fixture_found']}",f"- query: {summary['query_home']} vs {summary['query_away']}","- auto_apply: NO","- production_change: NO","","## Forecast"]
    if summary["fixture_found"] != "YES":
        lines.append("- none. Fixture not found by API search.")
    else:
        lines += [f"- fixture: {row['home_team']} vs {row['away_team']}",f"- competition: {row['country']} / {row['league']}",f"- status: {row['fixture_status']} | date: {row['fixture_date']}",f"- XI: {row['xi_status']} | source={row['xi_source']} | shapes={row['home_shape']}/{row['away_shape']}",f"- probabilities: home={row['home_prob']} draw={row['draw_prob']} away={row['away_prob']}",f"- result_forecast: {row['result_forecast']}",f"- scorelines: {row['scorelines']}",f"- goal_profile: {row['goal_profile']}",f"- scenario: {row['scenario']}",f"- confidence: {row['confidence']}",f"- note: {row['forecast_note']}"]
    return "\n".join(lines)+"\n"
def run(day, home, away, tz, base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); key=api_key(); fixture=None
    if key: fixture=find_fixture(day, home, away, key)
    out=[]
    if fixture:
        fx=fixture.get("fixture") or {}; teams=fixture.get("teams") or {}; league=fixture.get("league") or {}; fid=str(fx.get("id")); hpdpap=implied_from_odds(fid, key) or (0.50,0.29,0.21)
        xi,hs,aw,xi_source=lineups(fid,key)
        if xi == "NO_XI": xi,hs,aw,xi_source=probable_xi(day, home, away, base)
        res,scores,goal,scen,conf=forecast(hpdpap,xi,hs,aw)
        note="Ad hoc fixture forecast from API fixture search, market-implied baseline, and lineup status. Not part of daily board."
        if xi == "ESTIMATED_XI": note += " XI is estimated from squad pool; not official."
        out.append({"target_date":day,"generated_at":now,"fixture_id":fid,"home_team":(teams.get("home") or {}).get("name",""),"away_team":(teams.get("away") or {}).get("name",""),"league":league.get("name",""),"country":league.get("country",""),"fixture_status":(fx.get("status") or {}).get("short",""),"fixture_date":fx.get("date",""),"xi_status":xi,"xi_source":xi_source,"home_shape":hs,"away_shape":aw,"home_prob":hpdpap[0],"draw_prob":hpdpap[1],"away_prob":hpdpap[2],"result_forecast":res,"scorelines":scores,"goal_profile":goal,"scenario":scen,"confidence":conf,"forecast_note":note,"auto_apply":"NO","production_change":"NO"})
    summary={"target_date":day,"generated_at":now,"query_home":home,"query_away":away,"fixture_found":"YES" if out else "NO","rows":len(out),"next_action":"Review as ad hoc forecast only; do not mix with daily board.","auto_apply":"NO","production_change":"NO"}
    file_slug=slug(home+"_vs_"+away)
    for folder in [base/"today"/day, base/"governance"]:
        row=out[0] if out else {"target_date":day}
        write_csv(folder/f"vsigma_adhoc_fixture_forecast_{file_slug}.csv", out, FIELDS)
        write_csv(folder/f"vsigma_adhoc_fixture_forecast_{file_slug}_summary.csv", [summary], SUMMARY_FIELDS)
        (folder/f"vsigma_adhoc_fixture_forecast_{file_slug}.md").write_text(md(row,summary), encoding="utf-8")
    print("Ad hoc fixture forecast built")
    print(f"fixture_found={summary['fixture_found']} rows={summary['rows']}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--home",required=True); ap.add_argument("--away",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.home,a.away,a.timezone,a.processed_dir)
