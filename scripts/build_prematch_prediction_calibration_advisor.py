from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = ["target_date","generated_at","scope","group","sample","metric_focus","observed_rate","advice_level","recommendation","reason","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","advice_rows","watch_rows","caution_rows","hold_rows","next_action","auto_apply","production_change"]

def s(v): return "" if v is None else str(v).strip()
def num(v):
    try: return float(s(v))
    except ValueError: return None

def read_csv(p: Path):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def load(a: Path,b: Path): return read_csv(a) or read_csv(b)
def write_csv(p: Path, rows, fields):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def row(day,now,r,focus,rate,level,rec,reason):
    return {"target_date":day,"generated_at":now,"scope":s(r.get("scope")),"group":s(r.get("group")),"sample":s(r.get("sample")),"metric_focus":focus,"observed_rate":"" if rate is None else rate,"advice_level":level,"recommendation":rec,"reason":reason,"auto_apply":"NO","production_change":"NO"}
def advise(day,now,metrics):
    out=[]
    for r in metrics:
        sample=int(float(s(r.get("sample")) or 0))
        scope=s(r.get("scope")); group=s(r.get("group"))
        res=num(r.get("result_family_hit_pct")); exact=num(r.get("exact_hit_pct")); neigh=num(r.get("neighbor_or_exact_pct")); prof=num(r.get("goal_profile_hit_pct")); g3=num(r.get("goals_3plus_hit_pct")); btts=num(r.get("both_scored_hit_pct")); g2=num(r.get("goals_2plus_hit_pct"))
        if sample < 5:
            out.append(row(day,now,r,"sample_size",sample,"HOLD","OBSERVE_MORE","Sample below 5; do not change weights yet."))
        if scope=="GOAL_PROFILE" and group=="HIGH_GOALS" and sample>=1:
            if (prof is not None and prof < 60) or (g3 is not None and g3 < 50):
                out.append(row(day,now,r,"high_goals_aggression",prof,"CAUTION","DOWNGRADE_HIGH_GOALS_TO_OPEN_GOALS_REVIEW","High-goal profile is over-aggressive versus realized goal profile / 3+ goals."))
        if scope=="ALL" and group=="ALL" and sample>=1:
            if res is not None and res>=70:
                out.append(row(day,now,r,"result_family",res,"WATCH","KEEP_RESULT_FAMILY_SIGNAL","Result-family prediction is currently strong; keep monitoring."))
            if neigh is not None and neigh>=60:
                out.append(row(day,now,r,"score_neighbor",neigh,"WATCH","PRIORITIZE_SCORE_NEIGHBOR_OVER_EXACT","Neighbor score is more stable than exact score."))
            if exact is not None and exact<25 and sample>=10:
                out.append(row(day,now,r,"exact_score",exact,"CAUTION","DO_NOT_WEIGHT_EXACT_SCORE_HEAVILY","Exact score accuracy is low with enough sample."))
            if g2 is not None and g2>=65:
                out.append(row(day,now,r,"goals_2plus",g2,"WATCH","KEEP_2PLUS_GOALS_SIGNAL","2+ goals signal is strong in current sample."))
            if g3 is not None and g3<45:
                out.append(row(day,now,r,"goals_3plus",g3,"CAUTION","REQUIRE_STRONGER_EVIDENCE_FOR_3PLUS","3+ goals conversion is weak; avoid aggressive goal inflation."))
            if btts is not None and btts>=65:
                out.append(row(day,now,r,"both_scored",btts,"WATCH","KEEP_BTTS_AS_SUPPORTING_SIGNAL","Both-scored signal is strong as a supporting prediction layer."))
    return out
def md(day,rows,sm):
    lines=[f"# vSIGMA Prematch Prediction Calibration Advisor - {day}","","## Summary"]
    for k in ["advice_rows","watch_rows","caution_rows","hold_rows","next_action"]: lines.append(f"- {k}: {sm[k]}")
    lines += ["- auto_apply: NO","- production_change: NO","","## Advice"]
    if not rows: lines.append("- none.")
    for r in rows: lines.append(f"- {r['advice_level']} | {r['scope']} / {r['group']} | focus={r['metric_focus']} | sample={r['sample']} | rate={r['observed_rate']} | {r['recommendation']} | {r['reason']}")
    return "\n".join(lines)+"\n"
def append_panel(base,day,sm):
    sec="## Prematch Prediction Calibration Advisor"
    block="\n"+"\n".join([sec,f"- advice_rows: {sm['advice_rows']}",f"- watch_rows: {sm['watch_rows']}",f"- caution_rows: {sm['caution_rows']}",f"- hold_rows: {sm['hold_rows']}",f"- next_action: {sm['next_action']}"])+"\n"
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
    metrics=load(base/"today"/day/"vsigma_rolling_prematch_accuracy_dashboard.csv", base/"governance"/"vsigma_rolling_prematch_accuracy_dashboard.csv")
    rows=advise(day,now,metrics)
    sm={"target_date":day,"generated_at":now,"advice_rows":len(rows),"watch_rows":sum(1 for r in rows if r["advice_level"]=="WATCH"),"caution_rows":sum(1 for r in rows if r["advice_level"]=="CAUTION"),"hold_rows":sum(1 for r in rows if r["advice_level"]=="HOLD"),"next_action":"Review calibration advice only; keep auto_apply disabled until sample is large enough.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/"vsigma_prematch_prediction_calibration_advisor.csv",rows,FIELDS); write_csv(folder/"vsigma_prematch_prediction_calibration_advisor_summary.csv",[sm],SUMMARY_FIELDS); (folder/"vsigma_prematch_prediction_calibration_advisor.md").write_text(md(day,rows,sm),encoding="utf-8")
    append_panel(base,day,sm); print("Prematch prediction calibration advisor built")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.timezone,a.processed_dir)
