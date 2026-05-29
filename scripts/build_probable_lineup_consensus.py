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
    "home_avg_agreement","away_avg_agreement","home_probable_confidence","away_probable_confidence",
    "probable_lineup_gate","missing_reason","source_guard","auto_apply","production_change",
]


def s(x): return "" if x is None else str(x).strip()

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
            if rows:
                out.extend(rows); used.append(str(path))
    return out, ";".join(used) if used else "NO_SOURCE_FILE"

def players(row):
    raw=s(row.get("probable_xi") or row.get("players") or row.get("xi"))
    if raw:
        parts=re.split(r"[;|,]", raw)
    else:
        parts=[s(row.get(f"player_{i}")) for i in range(1,12)]
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
    for a,b in combinations(lineups,2):
        sa,sb=set(a),set(b)
        if not sa or not sb: continue
        vals.append(len(sa&sb)/max(1,len(sa|sb)))
    return sum(vals)/len(vals) if vals else 0.0

def conf(nsrc, consensus, agree):
    if nsrc<=0: return "NO_SOURCES"
    if nsrc>=3 and consensus>=9 and agree>=0.72: return "HIGH"
    if nsrc>=2 and consensus>=8 and agree>=0.62: return "MEDIUM"
    if nsrc>=2 and agree<0.45: return "CONFLICTING"
    return "LOW"

def aggregate(rows):
    grouped=defaultdict(list)
    for r in rows:
        fid=s(r.get("fixture_id")); sd=side(r); ps=players(r)
        if fid and sd and ps: grouped[(fid,sd)].append(ps)
    result={}
    for key,lineups in grouped.items():
        cnt=Counter(p for xi in lineups for p in set(xi))
        nsrc=len(lineups)
        consensus=sum(1 for _,c in cnt.items() if c/max(1,nsrc)>=0.5)
        agree=agreement(lineups)
        result[key]={"sources":nsrc,"consensus":consensus,"agreement":agree,"confidence":conf(nsrc,consensus,agree)}
    return result

def combined(home, away):
    h=home.get("confidence","NO_SOURCES"); a=away.get("confidence","NO_SOURCES")
    if "CONFLICTING" in {h,a}: return "PROBABLE_LINEUP_CONFLICT"
    if h==a=="HIGH": return "PROBABLE_XI_CONSENSUS_HIGH"
    if h in {"HIGH","MEDIUM"} and a in {"HIGH","MEDIUM"}: return "PROBABLE_XI_CONSENSUS_MEDIUM"
    if h!="NO_SOURCES" or a!="NO_SOURCES": return "PROBABLE_XI_CONSENSUS_LOW"
    return "NO_PROBABLE_LINEUP_SOURCES"

def build(day,tz):
    ts=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    fixtures, fsrc=fixture_rows(day); src, ssrc=source_rows(day); agg=aggregate(src); out=[]
    seen=set()
    for r in fixtures:
        fid=s(r.get("fixture_id"))
        if not fid or fid in seen: continue
        seen.add(fid)
        home=agg.get((fid,"home"),{}); away=agg.get((fid,"away"),{})
        gate=combined(home,away)
        missing="none" if gate!="NO_PROBABLE_LINEUP_SOURCES" else "no probable lineup source rows available"
        out.append({
            "target_date":day,"generated_at":ts,"fixture_id":fid,"home_team":s(r.get("home_team")),"away_team":s(r.get("away_team")),
            "home_sources":home.get("sources",0),"away_sources":away.get("sources",0),
            "home_consensus_players":home.get("consensus",0),"away_consensus_players":away.get("consensus",0),
            "home_avg_agreement":f"{home.get('agreement',0):.3f}","away_avg_agreement":f"{away.get('agreement',0):.3f}",
            "home_probable_confidence":home.get("confidence","NO_SOURCES"),"away_probable_confidence":away.get("confidence","NO_SOURCES"),
            "probable_lineup_gate":gate,"missing_reason":missing,"source_guard":f"fixtures={fsrc}; probable_sources={ssrc}","auto_apply":"NO","production_change":"NO"
        })
    return out

def counts(rows,field):
    c=Counter(str(r.get(field) or "UNKNOWN") for r in rows); return "; ".join(f"{k}={v}" for k,v in c.most_common()) if c else "none"

def md(day, rows):
    lines=[f"# vSIGMA Probable Lineup Consensus - {day}","","## Summary",f"- fixtures_reviewed: {len(rows)}",f"- probable_lineup_gates: {counts(rows,'probable_lineup_gate')}",f"- home_confidence: {counts(rows,'home_probable_confidence')}",f"- away_confidence: {counts(rows,'away_probable_confidence')}","- auto_apply: NO","- production_change: NO","","## Fixture Consensus"]
    for r in rows:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | gate={r['probable_lineup_gate']} | home={r['home_probable_confidence']}({r['home_sources']} src/{r['home_consensus_players']} consensus) | away={r['away_probable_confidence']}({r['away_sources']} src/{r['away_consensus_players']} consensus) | reason={r['missing_reason']}")
    lines += ["","## Guardrails","- Probable XI is never treated as official lineup.","- Consensus can support early shortlist/prelock planning only.","- Final stake still requires official lineup or explicit manual prelock approval.","- Missing probable sources do not fabricate lineups."]
    return "\n".join(lines)+"\n"

def run(day,tz):
    day=date.fromisoformat(day).isoformat(); rows=build(day,tz)
    for base in [P/"today"/day, P/"governance"]:
        write(base/"vsigma_probable_lineup_consensus.csv", rows, FIELDS); (base/"vsigma_probable_lineup_consensus.md").write_text(md(day,rows),encoding="utf-8")
    print("=== VSIGMA PROBABLE LINEUP CONSENSUS ==="); print(f"fixtures_reviewed={len(rows)}"); print(f"probable_lineup_gates={counts(rows,'probable_lineup_gate')}"); print("auto_apply=NO"); print("production_change=NO")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--date",required=True); p.add_argument("--timezone",default="Atlantic/Canary"); a=p.parse_args(); run(a.date,a.timezone)
if __name__ == "__main__": main()
