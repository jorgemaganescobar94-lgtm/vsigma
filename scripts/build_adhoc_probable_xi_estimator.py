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
XI_FIELDS = ["target_date","generated_at","fixture_id","home_team","away_team","team_side","team_id","team_name","xi_source","xi_status","formation","confidence","player_1","player_2","player_3","player_4","player_5","player_6","player_7","player_8","player_9","player_10","player_11","unavailable_count","unavailable_names","note","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","query_home","query_away","fixture_found","official_xi_available","estimated_xi_rows","next_action","auto_apply","production_change"]

def s(v): return "" if v is None else str(v).strip()
def clean(v):
    v = unicodedata.normalize("NFKD", s(v)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", v).strip()
def slug(v): return re.sub(r"[^a-z0-9]+", "_", clean(v)).strip("_") or "fixture"
def key():
    for k in ["APISPORTS_KEY","API_SPORTS_KEY","API_FOOTBALL_KEY","APIFOOTBALL_KEY","API_FOOTBALL_API_KEY","RAPIDAPI_KEY","X_RAPIDAPI_KEY"]:
        if os.getenv(k): return os.getenv(k)
    return ""
def call(path, params, k):
    req = Request("https://v3.football.api-sports.io/" + path + "?" + urlencode(params), headers={"x-apisports-key": k})
    with urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))
def sim(a,b):
    a=set(clean(a).split()); b=set(clean(b).split())
    return len(a & b) / max(1, len(a | b))
def find_fixture(day, home, away, k):
    best=None; best_score=-1
    for fx in call("fixtures", {"date": day}, k).get("response") or []:
        teams=fx.get("teams") or {}; h=(teams.get("home") or {}).get("name",""); a=(teams.get("away") or {}).get("name","")
        score=max(sim(home,h)+sim(away,a), sim(home,a)+sim(away,h))
        if score>best_score: best=fx; best_score=score
    return best if best_score >= 0.35 else None
def api_lineups(fid,k):
    try: return call("fixtures/lineups", {"fixture": fid}, k).get("response") or []
    except Exception: return []
def api_squad(team_id,k):
    try: resp=call("players/squads", {"team": team_id}, k).get("response") or []
    except Exception: return []
    return (resp[0].get("players") or []) if resp else []
def unavailable(fid,k):
    ids=set(); names=set()
    try: resp=call("injuries", {"fixture": fid}, k).get("response") or []
    except Exception: return ids,names
    for x in resp:
        p=x.get("player") or {}
        if s(p.get("id")): ids.add(s(p.get("id")))
        if s(p.get("name")): names.add(clean(p.get("name")))
    return ids,names
def pname(p): return s((p.get("player") or p).get("name"))
def pid(p): return s((p.get("player") or p).get("id"))
def ppos(p):
    pos=clean(p.get("position"))
    if pos.startswith("goal"): return "G"
    if pos.startswith("def"): return "D"
    if pos.startswith("att") or pos.startswith("forw"): return "F"
    return "M"
def select(pool, n, used):
    out=[]
    for p in pool:
        marker=pid(p) or pname(p)
        if not marker or marker in used: continue
        used.add(marker); out.append(p)
        if len(out)==n: break
    return out
def estimate(squad):
    by={"G":[],"D":[],"M":[],"F":[]}
    for p in squad:
        if pname(p): by[ppos(p)].append(p)
    used=set(); chosen=[]
    chosen += select(by["G"],1,used)
    chosen += select(by["D"],4,used)
    chosen += select(by["M"],3,used)
    chosen += select(by["F"],3,used)
    if len(chosen)<11: chosen += select(squad, 11-len(chosen), used)
    form="4-3-3" if len(by["F"])>=3 else "4-2-3-1"
    return form,[pname(p) for p in chosen[:11] if pname(p)]
def base_row(day,now,fx):
    f=fx.get("fixture") or {}; t=fx.get("teams") or {}
    return {"target_date":day,"generated_at":now,"fixture_id":s(f.get("id")),"home_team":s((t.get("home") or {}).get("name")),"away_team":s((t.get("away") or {}).get("name")),"auto_apply":"NO","production_change":"NO"}
def official_rows(day,now,fx,lineups):
    b=base_row(day,now,fx); rows=[]
    for i,l in enumerate(lineups[:2]):
        players=[s((x.get("player") or {}).get("name")) for x in (l.get("startXI") or [])]
        team=l.get("team") or {}; r=dict(b)
        r.update({"team_side":"home" if i==0 else "away","team_id":s(team.get("id")),"team_name":s(team.get("name")),"xi_source":"API_OFFICIAL_LINEUPS","xi_status":"OFFICIAL_XI","formation":s(l.get("formation")),"confidence":"HIGH" if len(players)==11 else "MEDIUM","unavailable_count":"","unavailable_names":"","note":"Official API lineup. Safe for final forecast update."})
        for n in range(11): r[f"player_{n+1}"]=players[n] if n<len(players) else ""
        rows.append(r)
    return rows
def estimated_rows(day,now,fx,k):
    b=base_row(day,now,fx); teams=fx.get("teams") or {}; fid=b["fixture_id"]; ids,names=unavailable(fid,k); rows=[]
    for side in ["home","away"]:
        team=teams.get(side) or {}; tid=s(team.get("id")); squad=[]
        for p in api_squad(tid,k):
            if pid(p) in ids or clean(pname(p)) in names: continue
            squad.append(p)
        form,players=estimate(squad); r=dict(b)
        r.update({"team_side":side,"team_id":tid,"team_name":s(team.get("name")),"xi_source":"API_SQUAD_HEURISTIC","xi_status":"ESTIMATED_XI" if len(players)==11 else "ESTIMATED_POOL_INCOMPLETE","formation":form if len(players)==11 else "","confidence":"LOW","unavailable_count":len(ids|names),"unavailable_names":"; ".join(sorted(names)),"note":"Estimated XI from API squad pool and unavailable-player filter. Not official; use only before confirmed lineups."})
        for n in range(11): r[f"player_{n+1}"]=players[n] if n<len(players) else ""
        rows.append(r)
    return rows
def write_csv(p,rows,fields):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def md(day,summary,rows):
    out=[f"# vSIGMA Ad Hoc Probable XI Estimator - {day}","","## Summary",f"- fixture_found: {summary['fixture_found']}",f"- official_xi_available: {summary['official_xi_available']}",f"- estimated_xi_rows: {summary['estimated_xi_rows']}","- auto_apply: NO","- production_change: NO","","## Teams"]
    if not rows: out.append("- none. Fixture not found or API key missing.")
    for r in rows:
        ps=[r.get(f"player_{i}","") for i in range(1,12) if r.get(f"player_{i}","")]
        out += [f"### {r['team_name']} ({r['team_side']})",f"- xi_status: {r['xi_status']}",f"- xi_source: {r['xi_source']}",f"- formation: {r['formation']}",f"- confidence: {r['confidence']}",f"- players: {', '.join(ps) if ps else 'none'}",f"- note: {r['note']}",""]
    return "\n".join(out).rstrip()+"\n"
def run(day,home,away,tz,base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); k=key(); fx=find_fixture(day,home,away,k) if k else None; rows=[]; official="NO"
    if fx:
        fid=s((fx.get("fixture") or {}).get("id")); ls=api_lineups(fid,k)
        if len(ls)>=2 and all(len(x.get("startXI") or [])==11 for x in ls[:2]): rows=official_rows(day,now,fx,ls); official="YES"
        else: rows=estimated_rows(day,now,fx,k)
    summary={"target_date":day,"generated_at":now,"query_home":home,"query_away":away,"fixture_found":"YES" if fx else "NO","official_xi_available":official,"estimated_xi_rows":len(rows),"next_action":"Use estimated XI only until official lineups are available.","auto_apply":"NO","production_change":"NO"}
    file_slug=slug(home+"_vs_"+away)
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/f"vsigma_adhoc_probable_xi_{file_slug}.csv",rows,XI_FIELDS); write_csv(folder/f"vsigma_adhoc_probable_xi_{file_slug}_summary.csv",[summary],SUMMARY_FIELDS); (folder/f"vsigma_adhoc_probable_xi_{file_slug}.md").write_text(md(day,summary,rows),encoding="utf-8")
    print(f"Ad hoc probable XI built fixture_found={summary['fixture_found']} official_xi_available={official} rows={len(rows)}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--home",required=True); ap.add_argument("--away",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.home,a.away,a.timezone,a.processed_dir)
