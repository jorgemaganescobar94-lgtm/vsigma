from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
DONE = {"FT", "AET", "PEN"}
FIELDS = [
    "day","created_at","fixture_id","home","away","predicted_result","predicted_scores","predicted_goal_profile",
    "actual_status","actual_score","actual_result","actual_goals","result_family_eval","score_exact_eval",
    "score_neighbor_eval","goal_profile_eval","goals_2plus_eval","goals_3plus_eval","both_scored_eval",
    "review_status","note","auto_apply","production_change",
]
SUM_FIELDS = [
    "day","created_at","rows","finished_rows","pending_rows","result_family_counts","score_exact_counts",
    "score_neighbor_counts","goal_profile_counts","goals_2plus_counts","goals_3plus_counts","both_scored_counts",
    "next_action","auto_apply","production_change",
]

def s(v): return "" if v is None else str(v).strip()
def u(v): return s(v).upper()
def read_csv(p: Path):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def load(a: Path, b: Path): return read_csv(a) or read_csv(b)
def write_csv(p: Path, rows, fields):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def cnt(rows, field):
    c=Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k,v in c.most_common()) if c else "none"
def parse_score(x):
    try:
        a,b=s(x).split("-")[:2]
        return int(a), int(b)
    except Exception:
        return None
def result_of(score):
    if not score: return "PENDING"
    h,a=score
    return "HOME" if h>a else "AWAY" if a>h else "DRAW"
def goal_profile(goals):
    if goals is None: return "PENDING"
    if goals >= 4: return "HIGH_GOALS"
    if goals >= 3: return "OPEN_GOALS"
    if goals >= 2: return "MODERATE_GOALS"
    return "LOW_GOALS"
def score_list(text):
    out=[]
    for part in s(text).split("/"):
        sc=parse_score(part.strip().split()[0] if part.strip() else "")
        if sc: out.append(sc)
    return out
def family_hit(pred, actual):
    pred=u(pred)
    if actual=="PENDING": return "PENDING"
    if pred==actual: return "HIT"
    if pred=="AWAY_OR_DRAW" and actual in {"AWAY","DRAW"}: return "HIT"
    if pred=="HOME_OR_DRAW" and actual in {"HOME","DRAW"}: return "HIT"
    return "MISS"
def neighbor_hit(pred_scores, actual):
    if not actual: return "PENDING"
    if actual in pred_scores: return "EXACT"
    ah,aa=actual
    for ph,pa in pred_scores:
        if abs(ph-ah)+abs(pa-aa) <= 1: return "NEIGHBOR"
    return "MISS"
def profile_hit(pred_profile, actual_goals):
    if actual_goals is None: return "PENDING"
    pred=u(pred_profile)
    actual=goal_profile(actual_goals)
    if pred==actual: return "HIT"
    if pred=="HIGH_GOALS" and actual_goals >= 3: return "HIT_LOOSE"
    if pred=="OPEN_GOALS" and actual_goals >= 2: return "HIT_LOOSE"
    if pred=="MODERATE_GOALS" and 2 <= actual_goals <= 3: return "HIT"
    if pred=="LOW_GOALS" and actual_goals <= 1: return "HIT"
    return "MISS"
def load_actuals(base: Path, day: str):
    rows = load(base/"today"/day/"vsigma_dated_post_match_results_refresh.csv", base/"governance"/"vsigma_dated_post_match_results_refresh.csv")
    out={}
    for r in rows:
        fid=s(r.get("fixture_id")); st=u(r.get("status")); score=parse_score(r.get("goals"))
        if fid: out[fid]={"status":st,"score":score}
    extra = load(base/"today"/day/"vsigma_api_enriched_fixture_results_refresh.csv", base/"governance"/"vsigma_api_enriched_fixture_results_refresh.csv")
    for r in extra:
        fid=s(r.get("fixture_id"))
        if not fid or fid in out: continue
        st=u(r.get("fixture_status_short")); gh=s(r.get("goals_home")); ga=s(r.get("goals_away"))
        score=parse_score(f"{gh}-{ga}") if gh and ga else None
        out[fid]={"status":st,"score":score}
    return out
def one(row, actual, day, now):
    fid=s(row.get("fixture_id")); pred_res=s(row.get("main_result")); pred_scores=s(row.get("scores")); pred_prof=s(row.get("goal_band"))
    st=actual.get("status","PENDING"); sc=actual.get("score")
    finished=st in DONE and sc is not None
    actual_res=result_of(sc) if finished else "PENDING"
    goals=(sc[0]+sc[1]) if finished else None
    ps=score_list(pred_scores)
    exact="PENDING" if not finished else "HIT" if sc in ps else "MISS"
    neigh=neighbor_hit(ps, sc) if finished else "PENDING"
    return {"day":day,"created_at":now,"fixture_id":fid,"home":s(row.get("home")),"away":s(row.get("away")),"predicted_result":pred_res,"predicted_scores":pred_scores,"predicted_goal_profile":pred_prof,"actual_status":st,"actual_score":f"{sc[0]}-{sc[1]}" if finished else "PENDING","actual_result":actual_res,"actual_goals":goals if goals is not None else "","result_family_eval":family_hit(pred_res, actual_res),"score_exact_eval":exact,"score_neighbor_eval":neigh,"goal_profile_eval":profile_hit(pred_prof, goals),"goals_2plus_eval":"PENDING" if goals is None else "HIT" if goals>=2 else "MISS","goals_3plus_eval":"PENDING" if goals is None else "HIT" if goals>=3 else "MISS","both_scored_eval":"PENDING" if not finished else "HIT" if sc[0]>0 and sc[1]>0 else "MISS","review_status":"FINISHED" if finished else "PENDING","note":"prediction accuracy review only","auto_apply":"NO","production_change":"NO"}
def md(day, rows, sm):
    lines=[f"# vSIGMA Prematch Story Accuracy Ledger - {day}","","## Summary"]
    for k in ["rows","finished_rows","pending_rows","result_family_counts","score_exact_counts","score_neighbor_counts","goal_profile_counts","goals_2plus_counts","goals_3plus_counts","both_scored_counts","next_action"]: lines.append(f"- {k}: {sm[k]}")
    lines += ["- auto_apply: NO","- production_change: NO","","## Rows"]
    for r in rows: lines.append(f"- {r['home']} vs {r['away']} | pred={r['predicted_result']} | scores={r['predicted_scores']} | profile={r['predicted_goal_profile']} | actual={r['actual_score']} | result_eval={r['result_family_eval']} | exact={r['score_exact_eval']} | neighbor={r['score_neighbor_eval']} | profile_eval={r['goal_profile_eval']}")
    return "\n".join(lines)+"\n"
def append_panel(base, day, sm):
    sec="## Prematch Story Accuracy Ledger"
    block="\n"+"\n".join([sec,f"- rows: {sm['rows']}",f"- finished_rows: {sm['finished_rows']}",f"- pending_rows: {sm['pending_rows']}",f"- result_family_counts: {sm['result_family_counts']}",f"- score_neighbor_counts: {sm['score_neighbor_counts']}",f"- goal_profile_counts: {sm['goal_profile_counts']}",f"- next_action: {sm['next_action']}"])+"\n"
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
    preds=load(base/"today"/day/"vsigma_prematch_match_story_engine.csv", base/"governance"/"vsigma_prematch_match_story_engine.csv")
    actuals=load_actuals(base,day); out=[one(r,actuals.get(s(r.get("fixture_id")),{}),day,now) for r in preds]
    sm={"day":day,"created_at":now,"rows":len(out),"finished_rows":sum(1 for r in out if r["review_status"]=="FINISHED"),"pending_rows":sum(1 for r in out if r["review_status"]=="PENDING"),"result_family_counts":cnt(out,"result_family_eval"),"score_exact_counts":cnt(out,"score_exact_eval"),"score_neighbor_counts":cnt(out,"score_neighbor_eval"),"goal_profile_counts":cnt(out,"goal_profile_eval"),"goals_2plus_counts":cnt(out,"goals_2plus_eval"),"goals_3plus_counts":cnt(out,"goals_3plus_eval"),"both_scored_counts":cnt(out,"both_scored_eval"),"next_action":"Track completed rows and calibrate prematch prediction families.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/"vsigma_prematch_story_accuracy_ledger.csv", out, FIELDS); write_csv(folder/"vsigma_prematch_story_accuracy_ledger_summary.csv", [sm], SUM_FIELDS); (folder/"vsigma_prematch_story_accuracy_ledger.md").write_text(md(day,out,sm),encoding="utf-8")
    append_panel(base,day,sm)
    print("Prematch story accuracy ledger built")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.timezone,a.processed_dir)
