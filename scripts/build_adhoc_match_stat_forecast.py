from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = ["target_date","generated_at","fixture_id","home_team","away_team","xi_status","xi_source","home_shape","away_shape","result_forecast","scorelines","goal_profile","scenario","confidence","home_prob","draw_prob","away_prob","home_xg","away_xg","total_xg","home_shots","away_shots","home_sot","away_sot","home_big_chances","away_big_chances","home_possession_pct","away_possession_pct","home_corners","away_corners","home_fouls","away_fouls","home_yellow_cards","away_yellow_cards","home_saves","away_saves","first_half_script","second_half_script","stat_confidence","note","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","query_home","query_away","rows","stat_confidence","next_action","auto_apply","production_change"]

def s(v): return "" if v is None else str(v).strip()
def clean(v):
    v = unicodedata.normalize("NFKD", s(v)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", v).strip()
def slug(v): return re.sub(r"[^a-z0-9]+", "_", clean(v)).strip("_") or "fixture"
def fnum(v, default=0.0):
    try: return float(s(v))
    except Exception: return default
def read_csv(path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def clamp(x, lo, hi): return max(lo, min(hi, x))
def stat_model(r):
    hp=fnum(r.get("home_prob")); dp=fnum(r.get("draw_prob")); ap=fnum(r.get("away_prob"))
    fav_gap=hp-ap
    goal=s(r.get("goal_profile")); scen=s(r.get("scenario")); xi=s(r.get("xi_status")); hs=s(r.get("home_shape")); aw=s(r.get("away_shape"))
    total_xg=2.35
    if "LOW" in goal: total_xg=2.05
    if "MODERATE" in goal: total_xg=2.35
    if "OPEN" in goal: total_xg=2.75
    if "HIGH" in goal: total_xg=3.15
    if "OPEN" in scen: total_xg += 0.15
    if xi == "OFFICIAL_XI": total_xg += 0.03
    if xi == "ESTIMATED_XI": total_xg += 0.00
    share=0.50 + clamp(fav_gap, -0.45, 0.45) * 0.42
    if "HOME" in s(r.get("result_forecast")): share += 0.04
    if hs.startswith("4-3-3") or hs.startswith("4-2-3-1"): share += 0.02
    if aw.startswith("4-3-3") and fav_gap > 0.25: share += 0.01
    share=clamp(share,0.38,0.72)
    hxg=round(total_xg*share,2); axg=round(total_xg-hxg,2); total_xg=round(hxg+axg,2)
    home_shots=round(7.5 + hxg*4.2 + max(0,fav_gap)*4.0)
    away_shots=round(6.0 + axg*4.0 + max(0,-fav_gap)*3.0)
    home_sot=clamp(round(hxg*2.7),1,8); away_sot=clamp(round(axg*2.6),1,6)
    home_bc=clamp(round(hxg*1.35),0,4); away_bc=clamp(round(axg*1.20),0,3)
    home_pos=round(clamp(50 + fav_gap*24 + (4 if "FAVORITE_CONTROL" in scen else 0),42,66)); away_pos=100-home_pos
    home_corners=clamp(round(3.0 + home_shots*0.18 + max(0,fav_gap)*2.0),2,9); away_corners=clamp(round(2.5 + away_shots*0.16),1,7)
    home_fouls=round(11.5 + max(0,-fav_gap)*5 + (1 if away_pos>48 else 0)); away_fouls=round(12.0 + max(0,fav_gap)*5 + (1 if home_pos>55 else 0))
    home_yc=clamp(round(home_fouls/7.5),1,4); away_yc=clamp(round(away_fouls/6.8),1,5)
    home_saves=clamp(away_sot-1,0,5); away_saves=clamp(home_sot-1,0,7)
    if "FAVORITE_CONTROL" in scen:
        fh="Mexico control, South Africa compact; first goal value high; HT likely 0-0 or 1-0."
        sh="If Mexico scores first, game management; if 0-0 after 60', South Africa draw equity rises."
    elif "OPEN" in scen:
        fh="Higher exchange risk from both shapes; early transitions matter."
        sh="Second half more stretched; BTTS and 2+ goals become stronger."
    else:
        fh="Tight early rhythm; low tempo if no early goal."
        sh="Late subs can decide; draw branch remains alive."
    stat_conf="MEDIUM" if xi in {"OFFICIAL_XI","ESTIMATED_XI"} else "LOW"
    if xi == "ESTIMATED_XI": stat_conf="LOW_TO_MEDIUM"
    return {
        "home_xg":hxg,"away_xg":axg,"total_xg":total_xg,
        "home_shots":home_shots,"away_shots":away_shots,
        "home_sot":home_sot,"away_sot":away_sot,
        "home_big_chances":home_bc,"away_big_chances":away_bc,
        "home_possession_pct":home_pos,"away_possession_pct":away_pos,
        "home_corners":home_corners,"away_corners":away_corners,
        "home_fouls":home_fouls,"away_fouls":away_fouls,
        "home_yellow_cards":home_yc,"away_yellow_cards":away_yc,
        "home_saves":home_saves,"away_saves":away_saves,
        "first_half_script":fh,"second_half_script":sh,"stat_confidence":stat_conf,
    }
def md(row, summary):
    out=[f"# vSIGMA Ad Hoc Match Stat Forecast - {row.get('target_date')}","","## Summary",f"- rows: {summary['rows']}",f"- stat_confidence: {summary['stat_confidence']}","- auto_apply: NO","- production_change: NO","","## Fixture"]
    if not row:
        out.append("- none. No ad hoc fixture forecast available.")
        return "\n".join(out)+"\n"
    out += [f"- fixture: {row['home_team']} vs {row['away_team']}",f"- XI: {row['xi_status']} | source={row['xi_source']} | shapes={row['home_shape']}/{row['away_shape']}",f"- result_forecast: {row['result_forecast']}",f"- scorelines: {row['scorelines']}",f"- goal_profile: {row['goal_profile']}",f"- scenario: {row['scenario']}","","## Predicted Match Stats",f"- xG: {row['home_team']} {row['home_xg']} - {row['away_xg']} {row['away_team']} | total={row['total_xg']}",f"- shots: {row['home_team']} {row['home_shots']} - {row['away_shots']} {row['away_team']}",f"- shots_on_target: {row['home_team']} {row['home_sot']} - {row['away_sot']} {row['away_team']}",f"- big_chances: {row['home_team']} {row['home_big_chances']} - {row['away_big_chances']} {row['away_team']}",f"- possession: {row['home_team']} {row['home_possession_pct']}% - {row['away_possession_pct']}% {row['away_team']}",f"- corners: {row['home_team']} {row['home_corners']} - {row['away_corners']} {row['away_team']}",f"- fouls: {row['home_team']} {row['home_fouls']} - {row['away_fouls']} {row['away_team']}",f"- yellow_cards: {row['home_team']} {row['home_yellow_cards']} - {row['away_yellow_cards']} {row['away_team']}",f"- saves: {row['home_team']} {row['home_saves']} - {row['away_saves']} {row['away_team']}","","## Script By Phase",f"- first_half: {row['first_half_script']}",f"- second_half: {row['second_half_script']}","","## Note",f"- {row['note']}"]
    return "\n".join(out)+"\n"
def run(day,home,away,tz,base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); file_slug=slug(home+"_vs_"+away)
    fpath=base/"today"/day/f"vsigma_adhoc_fixture_forecast_{file_slug}.csv"
    forecast_rows=read_csv(fpath)
    out=[]
    if forecast_rows:
        r=dict(forecast_rows[0]); stats=stat_model(r); r.update(stats); r["generated_at"]=now; r["note"]="Stat forecast derived from ad hoc fixture forecast, probabilities, scenario and XI status. Diagnostic only; not a betting instruction."; out=[r]
    summary={"target_date":day,"generated_at":now,"query_home":home,"query_away":away,"rows":len(out),"stat_confidence":out[0].get("stat_confidence","") if out else "NONE","next_action":"Use as match-stat forecast only; rerun after official XI.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        row=out[0] if out else {"target_date":day}
        write_csv(folder/f"vsigma_adhoc_match_stat_forecast_{file_slug}.csv",out,FIELDS); write_csv(folder/f"vsigma_adhoc_match_stat_forecast_{file_slug}_summary.csv",[summary],SUMMARY_FIELDS); (folder/f"vsigma_adhoc_match_stat_forecast_{file_slug}.md").write_text(md(row,summary),encoding="utf-8")
    print(f"Ad hoc match stat forecast built rows={len(out)}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--home",required=True); ap.add_argument("--away",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.home,a.away,a.timezone,a.processed_dir)
