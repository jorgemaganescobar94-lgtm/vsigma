from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = ["scope","group","sample","result_family_hit_pct","exact_hit_pct","neighbor_or_exact_pct","goal_profile_hit_pct","goals_2plus_hit_pct","goals_3plus_hit_pct","both_scored_hit_pct","pending_rows","note"]
SUMMARY_FIELDS = ["day","created_at","finished_rows","pending_rows","overall_result_family_hit_pct","overall_exact_hit_pct","overall_neighbor_or_exact_pct","overall_goal_profile_hit_pct","next_action","auto_apply","production_change"]

def s(v): return "" if v is None else str(v).strip()
def read_csv(p: Path):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def write_csv(p: Path, rows, fields):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def pct(hit, total): return "" if total <= 0 else round(100*hit/total, 1)
def is_hit(v): return s(v) in {"HIT","HIT_LOOSE","EXACT","NEIGHBOR"}
def exact(v): return s(v) == "HIT"
def finished(r): return s(r.get("review_status")) == "FINISHED"
def pending(r): return s(r.get("review_status")) == "PENDING"
def collect(base: Path):
    out=[]
    for p in sorted((base/"today").glob("*/vsigma_prematch_story_accuracy_ledger.csv")):
        day=p.parent.name
        for r in read_csv(p):
            r["_day"]=day; out.append(r)
    return out
def calc(scope, group, rows):
    fin=[r for r in rows if finished(r)]; pend=sum(1 for r in rows if pending(r)); n=len(fin)
    return {"scope":scope,"group":group,"sample":n,"result_family_hit_pct":pct(sum(is_hit(r.get("result_family_eval")) for r in fin),n),"exact_hit_pct":pct(sum(exact(r.get("score_exact_eval")) for r in fin),n),"neighbor_or_exact_pct":pct(sum(s(r.get("score_neighbor_eval")) in {"EXACT","NEIGHBOR"} for r in fin),n),"goal_profile_hit_pct":pct(sum(is_hit(r.get("goal_profile_eval")) for r in fin),n),"goals_2plus_hit_pct":pct(sum(is_hit(r.get("goals_2plus_eval")) for r in fin),n),"goals_3plus_hit_pct":pct(sum(is_hit(r.get("goals_3plus_eval")) for r in fin),n),"both_scored_hit_pct":pct(sum(is_hit(r.get("both_scored_eval")) for r in fin),n),"pending_rows":pend,"note":"accuracy from finished prematch story ledger rows"}
def grouped(rows, key):
    d=defaultdict(list)
    for r in rows: d[s(r.get(key)) or "UNKNOWN"].append(r)
    return d
def recent(rows, n):
    return sorted(rows, key=lambda r:(s(r.get("_day")), s(r.get("fixture_id"))))[-n:]
def md(day, rows, sm):
    lines=[f"# vSIGMA Rolling Prematch Accuracy Dashboard - {day}","","## Summary"]
    for k in ["finished_rows","pending_rows","overall_result_family_hit_pct","overall_exact_hit_pct","overall_neighbor_or_exact_pct","overall_goal_profile_hit_pct","next_action"]: lines.append(f"- {k}: {sm[k]}")
    lines += ["- auto_apply: NO","- production_change: NO","","## Accuracy Rows"]
    for r in rows:
        lines.append(f"- {r['scope']} / {r['group']} | sample={r['sample']} | result={r['result_family_hit_pct']}% | exact={r['exact_hit_pct']}% | neighbor={r['neighbor_or_exact_pct']}% | profile={r['goal_profile_hit_pct']}% | 2plus={r['goals_2plus_hit_pct']}% | 3plus={r['goals_3plus_hit_pct']}% | BTTS={r['both_scored_hit_pct']}% | pending={r['pending_rows']}")
    return "\n".join(lines)+"\n"
def append_panel(base, day, sm):
    sec="## Rolling Prematch Accuracy Dashboard"
    block="\n"+"\n".join([sec,f"- finished_rows: {sm['finished_rows']}",f"- pending_rows: {sm['pending_rows']}",f"- result_family_hit_pct: {sm['overall_result_family_hit_pct']}",f"- neighbor_or_exact_pct: {sm['overall_neighbor_or_exact_pct']}",f"- goal_profile_hit_pct: {sm['overall_goal_profile_hit_pct']}",f"- next_action: {sm['next_action']}"])+"\n"
    for folder in [base/"today"/day, base/"governance"]:
        p=folder/"vsigma_consolidated_daily_operator_panel.md"
        if p.exists():
            t=p.read_text(encoding="utf-8",errors="replace")
            if sec in t:
                before=t.split(sec,1)[0].rstrip(); after=t.split(sec,1)[1]; i=after.find("\n## "); t=before+block+(after[i:] if i>=0 else "")
            else: t=t.rstrip()+block
            p.write_text(t,encoding="utf-8")
def run(day,tz,base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows=collect(base); fin=[r for r in rows if finished(r)]; pend=sum(1 for r in rows if pending(r))
    out=[calc("ALL","ALL",rows), calc("RECENT","LAST_20",recent(rows,20)), calc("RECENT","LAST_50",recent(rows,50))]
    for k,v in grouped(rows,"predicted_result").items(): out.append(calc("PREDICTED_RESULT",k,v))
    for k,v in grouped(rows,"predicted_goal_profile").items(): out.append(calc("GOAL_PROFILE",k,v))
    overall=calc("ALL","ALL",rows)
    sm={"day":day,"created_at":now,"finished_rows":len(fin),"pending_rows":pend,"overall_result_family_hit_pct":overall["result_family_hit_pct"],"overall_exact_hit_pct":overall["exact_hit_pct"],"overall_neighbor_or_exact_pct":overall["neighbor_or_exact_pct"],"overall_goal_profile_hit_pct":overall["goal_profile_hit_pct"],"next_action":"Use rolling accuracy to calibrate prematch prediction families.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/"vsigma_rolling_prematch_accuracy_dashboard.csv",out,FIELDS); write_csv(folder/"vsigma_rolling_prematch_accuracy_dashboard_summary.csv",[sm],SUMMARY_FIELDS); (folder/"vsigma_rolling_prematch_accuracy_dashboard.md").write_text(md(day,out,sm),encoding="utf-8")
    append_panel(base,day,sm); print("Rolling prematch accuracy dashboard built")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.timezone,a.processed_dir)
