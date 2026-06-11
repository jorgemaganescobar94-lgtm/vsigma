from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = ["target_date","generated_at","scope","group","metric_focus","recommendation","advice_level","sample","observed_rate","repeat_days","gate_status","gate_reason","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","rows","candidate_rows","blocked_sample_rows","blocked_history_rows","hold_rows","min_sample","min_repeat_days","next_action","auto_apply","production_change"]

def s(v): return "" if v is None else str(v).strip()
def n(v):
    try: return int(float(s(v) or 0))
    except ValueError: return 0

def read_csv(p: Path):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def load(a: Path,b: Path): return read_csv(a) or read_csv(b)
def write_csv(p: Path, rows, fields):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def advice_key(r): return (s(r.get("scope")), s(r.get("group")), s(r.get("metric_focus")), s(r.get("recommendation")))
def history(base: Path):
    days=defaultdict(set)
    for p in sorted((base/"today").glob("*/vsigma_prematch_prediction_calibration_advisor.csv")):
        d=p.parent.name
        for r in read_csv(p):
            days[advice_key(r)].add(d)
    return {k:len(v) for k,v in days.items()}
def gate_one(day,now,r,repeats,min_sample,min_repeat):
    sample=n(r.get("sample")); level=s(r.get("advice_level")); rep=repeats.get(advice_key(r),0)
    if level=="HOLD": status="HOLD_ONLY"; reason="Advisor requested observation only."
    elif sample < min_sample: status="BLOCKED_SAMPLE"; reason=f"sample {sample} below minimum {min_sample}."
    elif rep < min_repeat: status="BLOCKED_HISTORY"; reason=f"repeat_days {rep} below minimum {min_repeat}."
    else:
        status="RULE_CANDIDATE_REVIEW" if level=="CAUTION" else "STABLE_SIGNAL_REVIEW"
        reason="Minimum sample and repeat-day gates passed; review manually before any implementation."
    return {"target_date":day,"generated_at":now,"scope":s(r.get("scope")),"group":s(r.get("group")),"metric_focus":s(r.get("metric_focus")),"recommendation":s(r.get("recommendation")),"advice_level":level,"sample":sample,"observed_rate":s(r.get("observed_rate")),"repeat_days":rep,"gate_status":status,"gate_reason":reason,"auto_apply":"NO","production_change":"NO"}
def md(day,rows,sm):
    lines=[f"# vSIGMA Prematch Calibration Rule Gate - {day}","","## Summary"]
    for k in ["rows","candidate_rows","blocked_sample_rows","blocked_history_rows","hold_rows","min_sample","min_repeat_days","next_action"]: lines.append(f"- {k}: {sm[k]}")
    lines += ["- auto_apply: NO","- production_change: NO","","## Gate Rows"]
    if not rows: lines.append("- none.")
    for r in rows: lines.append(f"- {r['gate_status']} | {r['scope']} / {r['group']} | focus={r['metric_focus']} | sample={r['sample']} | repeat_days={r['repeat_days']} | {r['recommendation']} | {r['gate_reason']}")
    return "\n".join(lines)+"\n"
def append_panel(base,day,sm):
    sec="## Prematch Calibration Rule Gate"
    block="\n"+"\n".join([sec,f"- rows: {sm['rows']}",f"- candidate_rows: {sm['candidate_rows']}",f"- blocked_sample_rows: {sm['blocked_sample_rows']}",f"- blocked_history_rows: {sm['blocked_history_rows']}",f"- hold_rows: {sm['hold_rows']}",f"- next_action: {sm['next_action']}"])+"\n"
    for folder in [base/"today"/day, base/"governance"]:
        p=folder/"vsigma_consolidated_daily_operator_panel.md"
        if p.exists():
            t=p.read_text(encoding="utf-8",errors="replace")
            if sec in t:
                before=t.split(sec,1)[0].rstrip(); after=t.split(sec,1)[1]; i=after.find("\n## "); t=before+block+(after[i:] if i>=0 else "")
            else: t=t.rstrip()+block
            p.write_text(t,encoding="utf-8")
def run(day,tz,base,min_sample,min_repeat):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    advisor=load(base/"today"/day/"vsigma_prematch_prediction_calibration_advisor.csv", base/"governance"/"vsigma_prematch_prediction_calibration_advisor.csv")
    repeats=history(base)
    rows=[gate_one(day,now,r,repeats,min_sample,min_repeat) for r in advisor]
    c=Counter(r["gate_status"] for r in rows)
    sm={"target_date":day,"generated_at":now,"rows":len(rows),"candidate_rows":c.get("RULE_CANDIDATE_REVIEW",0)+c.get("STABLE_SIGNAL_REVIEW",0),"blocked_sample_rows":c.get("BLOCKED_SAMPLE",0),"blocked_history_rows":c.get("BLOCKED_HISTORY",0),"hold_rows":c.get("HOLD_ONLY",0),"min_sample":min_sample,"min_repeat_days":min_repeat,"next_action":"No automatic rule changes; review candidates only after sample and history gates pass.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/"vsigma_prematch_calibration_rule_gate.csv",rows,FIELDS); write_csv(folder/"vsigma_prematch_calibration_rule_gate_summary.csv",[sm],SUMMARY_FIELDS); (folder/"vsigma_prematch_calibration_rule_gate.md").write_text(md(day,rows,sm),encoding="utf-8")
    append_panel(base,day,sm); print("Prematch calibration rule gate built")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); ap.add_argument("--min-sample",type=int,default=20); ap.add_argument("--min-repeat-days",type=int,default=3); a=ap.parse_args(); run(a.date,a.timezone,a.processed_dir,a.min_sample,a.min_repeat_days)
