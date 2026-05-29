from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from itertools import combinations
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
SOURCE_NAMES = ["vsigma_probable_lineup_sources.csv", "probable_lineup_sources.csv"]
FIELDS = [
    "target_date","generated_at","fixture_id","home_team","away_team",
    "home_sources","away_sources","home_consensus_players","away_consensus_players",
    "home_avg_agreement","away_avg_agreement","home_weighted_agreement","away_weighted_agreement",
    "home_probable_confidence","away_probable_confidence","accepted_home_sources","accepted_away_sources",
    "rejected_home_sources","rejected_away_sources","probable_lineup_gate","missing_reason",
    "source_registry_guard","source_guard","auto_apply","production_change",
]


def s(x): return "" if x is None else str(x).strip()
def num(x, default=0.0):
    try: return float(s(x))
    except ValueError: return default

def read(path: Path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f: return [dict(r) for r in csv.DictReader(f)]
def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def d(day,name): return P/"today"/day/name

def fixture_rows(day):
    for name in ["matches_vsigma_scored_v3.csv","vsigma_daily_execution_board.csv","matches_league_filtered.csv"]:
        rows=read(d(day,name))
        if rows: return rows, name
    return [], "NONE"

def source_rows(day):
    out=[]; used=[]
    for name in SOURCE_NAMES:
        for path in [d(day,name), P/"governance"/name, Path("data/raw")/name]:
            rows=read(path)
            if rows: out.extend(rows); used.append(str(path))
    return out, ";".join(used) if used else "NO_SOURCE_FILE"

def registry_rows(day):
    rows=read(d(day,"vsigma_probable_lineup_source_registry.csv")) or read(P/"governance"/"vsigma_probable_lineup_source_registry.csv")
    return {s(r.get("source_name")).lower().replace(" ","_"): r for r in rows if s(r.get("source_name"))}

def scope_match(reg, fixture):
    league=s(fixture.get("league")).lower(); country=s(fixture.get("country")).lower()
    lf=s(reg.get("league_filter")).lower(); cf=s(reg.get("country_filter")).lower()
    league_ok = lf in {"all","configurable",""} or lf == league
    country_ok = cf in {"all","configurable",""} or cf == country
    return league_ok and country_ok

def valid_source(row, fixture, registry):
    name=s(row.get("source_name") or row.get("source") or row.get("provider")).lower().replace(" ","_")
    reg=registry.get(name)
    if not reg: return False, name, 0.0, "not_registered"
    if s(reg.get("enabled")).upper() != "YES": return False, name, 0.0, "disabled"
    if s(reg.get("status")).upper() != "ACTIVE": return False, name, 0.0, f"status_{s(reg.get('status'))}"
    if not scope_match(reg, fixture): return False, name, 0.0, "scope_mismatch"
    weight=num(reg.get("priority_weight"),0)*num(reg.get("reliability_score"),0)
    return weight>0, name, weight, "accepted" if weight>0 else "zero_weight"

def players(row):
    raw=s(row.get("probable_xi") or row.get("players") or row.get("xi"))
    parts=re.split(r"[;|,]", raw) if raw else [s(row.get(f"player_{i}")) for i in range(1,12)]
    clean=[]
    for p in parts:
        p=re.sub(r"\s+"," ",s(p)).lower()
        p=re.sub(r"[^a-z0-9áéíóúüñçãõàèìòùâêîôû \-']","",p).strip()
        if p: clean.append(p)
    return clean[:11]
def side(row):
    v=s(row.get("team_side") or row.get("side") or row.get("team")).lower()
    if v in {"home","h","local"}: return "home"
    if v in {"away","a","visitante"}: return "away"
    return ""

def agreement(lineups):
    if len(lineups)<2: return 0.0
    vals=[]
    for a,b in combinations([x["players"] for x in lineups],2):
        sa,sb=set(a),set(b)
        if sa and sb: vals.append(len(sa&sb)/max(1,len(sa|sb)))
    return sum(vals)/len(vals) if vals else 0.0

def weighted_agreement(lineups):
    if not lineups: return 0.0
    total_weight=sum(x["weight"] for x in lineups)
    if total_weight<=0: return 0.0
    support=defaultdict(float)
    for x in lineups:
        for p in set(x["players"]): support[p]+=x["weight"]
    consensus_weight=sum(w for w in support.values() if w/total_weight>=0.5)
    return consensus_weight/max(1,total_weight*11)

def aggregate(accepted):
    grouped=defaultdict(list)
    for x in accepted: grouped[(x["fixture_id"],x["side"])].append(x)
    result={}
    for key,lineups in grouped.items():
        total_w=sum(x["weight"] for x in lineups)
        support=defaultdict(float)
        for x in lineups:
            for p in set(x["players"]): support[p]+=x["weight"]
        consensus=sum(1 for _,w in support.items() if total_w>0 and w/total_w>=0.5)
        agree=agreement(lineups); wagree=weighted_agreement(lineups); nsrc=len(lineups)
        if nsrc>=3 and consensus>=9 and wagree>=0.70: conf="HIGH_WEIGHTED"
        elif nsrc>=2 and consensus>=8 and wagree>=0.58: conf="MEDIUM_WEIGHTED"
        elif nsrc>=2 and agree<0.45: conf="CONFLICTING_SOURCES"
        else: conf="LOW_WEIGHTED"
        result[key]={"sources":nsrc,"consensus":consensus,"agreement":agree,"weighted_agreement":wagree,"confidence":conf,"names":"|".join(x["source"] for x in lineups)}
    return result

def combined(home,away):
    h=home.get("confidence","NO_APPROVED_SOURCES"); a=away.get("confidence","NO_APPROVED_SOURCES")
    if "CONFLICTING_SOURCES" in {h,a}: return "PROBABLE_LINEUP_CONFLICT"
    if h==a=="HIGH_WEIGHTED": return "PROBABLE_XI_CONSENSUS_HIGH"
    if h in {"HIGH_WEIGHTED","MEDIUM_WEIGHTED"} and a in {"HIGH_WEIGHTED","MEDIUM_WEIGHTED"}: return "PROBABLE_XI_CONSENSUS_MEDIUM"
    if h!="NO_APPROVED_SOURCES" or a!="NO_APPROVED_SOURCES": return "PROBABLE_XI_CONSENSUS_LOW"
    return "NO_PROBABLE_LINEUP_SOURCES"

def build(day,tz):
    ts=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); fixtures,fsrc=fixture_rows(day); fixtures_by={s(r.get("fixture_id")):r for r in fixtures}; src,ssrc=source_rows(day); reg=registry_rows(day)
    accepted=[]; rejected=defaultdict(list)
    for r in src:
        fid=s(r.get("fixture_id")); sd=side(r); ps=players(r); fx=fixtures_by.get(fid,{})
        ok,name,w,why=valid_source(r,fx,reg)
        if ok and fid and sd and ps: accepted.append({"fixture_id":fid,"side":sd,"players":ps,"source":name,"weight":w})
        else: rejected[(fid,sd)].append(f"{name or 'unknown'}:{why}")
    agg=aggregate(accepted); out=[]; seen=set()
    for r in fixtures:
        fid=s(r.get("fixture_id"))
        if not fid or fid in seen: continue
        seen.add(fid); home=agg.get((fid,"home"),{}); away=agg.get((fid,"away"),{}); gate=combined(home,away)
        missing="none" if gate!="NO_PROBABLE_LINEUP_SOURCES" else "no approved probable lineup sources available"
        out.append({"target_date":day,"generated_at":ts,"fixture_id":fid,"home_team":s(r.get("home_team")),"away_team":s(r.get("away_team")),"home_sources":home.get("sources",0),"away_sources":away.get("sources",0),"home_consensus_players":home.get("consensus",0),"away_consensus_players":away.get("consensus",0),"home_avg_agreement":f"{home.get('agreement',0):.3f}","away_avg_agreement":f"{away.get('agreement',0):.3f}","home_weighted_agreement":f"{home.get('weighted_agreement',0):.3f}","away_weighted_agreement":f"{away.get('weighted_agreement',0):.3f}","home_probable_confidence":home.get("confidence","NO_APPROVED_SOURCES"),"away_probable_confidence":away.get("confidence","NO_APPROVED_SOURCES"),"accepted_home_sources":home.get("names",""),"accepted_away_sources":away.get("names",""),"rejected_home_sources":"|".join(rejected.get((fid,"home"),[])),"rejected_away_sources":"|".join(rejected.get((fid,"away"),[])),"probable_lineup_gate":gate,"missing_reason":missing,"source_registry_guard":f"registry_sources={len(reg)}; accepted_rows={len(accepted)}; rejected_groups={len(rejected)}","source_guard":f"fixtures={fsrc}; probable_sources={ssrc}","auto_apply":"NO","production_change":"NO"})
    return out

def counts(rows,field):
    c=Counter(str(r.get(field) or "UNKNOWN") for r in rows); return "; ".join(f"{k}={v}" for k,v in c.most_common()) if c else "none"
def md(day,rows):
    lines=[f"# vSIGMA Probable Lineup Consensus v2 - {day}","","## Summary",f"- fixtures_reviewed: {len(rows)}",f"- probable_lineup_gates: {counts(rows,'probable_lineup_gate')}",f"- home_confidence: {counts(rows,'home_probable_confidence')}",f"- away_confidence: {counts(rows,'away_probable_confidence')}","- auto_apply: NO","- production_change: NO","","## Fixture Consensus"]
    for r in rows: lines.append(f"- {r['home_team']} vs {r['away_team']} | gate={r['probable_lineup_gate']} | home={r['home_probable_confidence']}({r['home_sources']} src/{r['home_consensus_players']} consensus/w={r['home_weighted_agreement']}) | away={r['away_probable_confidence']}({r['away_sources']} src/{r['away_consensus_players']} consensus/w={r['away_weighted_agreement']}) | accepted={r['accepted_home_sources']} / {r['accepted_away_sources']} | rejected={r['rejected_home_sources']} / {r['rejected_away_sources']}")
    lines += ["","## Guardrails","- Registry-approved probable XI is never treated as official lineup.","- Disabled, unregistered, out-of-scope, or review-only sources are rejected.","- Weighted consensus can support early shortlist/prelock planning only.","- Final stake still requires official lineup or explicit manual prelock approval."]
    return "\n".join(lines)+"\n"
def run(day,tz):
    day=date.fromisoformat(day).isoformat(); rows=build(day,tz)
    for base in [P/"today"/day,P/"governance"]:
        write(base/"vsigma_probable_lineup_consensus.csv",rows,FIELDS); (base/"vsigma_probable_lineup_consensus.md").write_text(md(day,rows),encoding="utf-8")
    print("=== VSIGMA PROBABLE LINEUP CONSENSUS V2 ==="); print(f"fixtures_reviewed={len(rows)}"); print(f"probable_lineup_gates={counts(rows,'probable_lineup_gate')}"); print("auto_apply=NO"); print("production_change=NO")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--date",required=True); p.add_argument("--timezone",default="Atlantic/Canary"); a=p.parse_args(); run(a.date,a.timezone)
if __name__=="__main__": main()
