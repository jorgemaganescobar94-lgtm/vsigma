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
FINAL_STATUS = {"FT", "AET", "PEN"}
FIELDS = [
    "target_date","generated_at","fixture_id","home_team","away_team","match_status","actual_score","forecast_score","scoreline_grade",
    "forecast_result","actual_result","result_grade","market_robust_grade","market_value_grade",
    "raw_home_prob","raw_draw_prob","raw_away_prob","adjusted_home_prob","adjusted_draw_prob","adjusted_away_prob",
    "forecast_btts_yes_pct","actual_btts","btts_grade","forecast_over25_pct","actual_over25","over25_grade","forecast_under35_pct","actual_under35","under35_grade",
    "forecast_home_xg","forecast_away_xg","actual_home_xg","actual_away_xg","home_xg_error","away_xg_error","xg_direction_grade",
    "forecast_home_shots","actual_home_shots","home_shots_error","forecast_away_shots","actual_away_shots","away_shots_error",
    "forecast_home_sot","actual_home_sot","home_sot_error","forecast_away_sot","actual_away_sot","away_sot_error",
    "forecast_home_corners","actual_home_corners","home_corners_error","forecast_away_corners","actual_away_corners","away_corners_error",
    "forecast_home_possession","actual_home_possession","home_possession_error","forecast_away_possession","actual_away_possession","away_possession_error",
    "draw_risk_index","goal_suppression_index","unit_edge","forecast_branch_base","forecast_danger_branch","branch_grade",
    "learning_flags","learning_verdict","auto_apply","production_change"
]
SUMMARY_FIELDS = ["target_date","generated_at","query_home","query_away","rows","match_status","learning_verdict","next_action","auto_apply","production_change"]

def s(v): return "" if v is None else str(v).strip()
def clean(v):
    v = unicodedata.normalize("NFKD", s(v)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", v).strip()
def slug(v): return re.sub(r"[^a-z0-9]+", "_", clean(v)).strip("_") or "fixture"
def fnum(v, default=0.0):
    try: return float(s(v).replace("%", ""))
    except Exception: return default
def maybe_num(v):
    try:
        if s(v)=="": return ""
        return round(float(s(v).replace("%", "")), 2)
    except Exception: return ""
def api_key():
    for k in ["APISPORTS_KEY","API_SPORTS_KEY","API_FOOTBALL_KEY","APIFOOTBALL_KEY","API_FOOTBALL_API_KEY","RAPIDAPI_KEY","X_RAPIDAPI_KEY"]:
        if os.getenv(k): return os.getenv(k)
    return ""
def call(path, params, key):
    req = Request("https://v3.football.api-sports.io/" + path + "?" + urlencode(params), headers={"x-apisports-key": key})
    with urlopen(req, timeout=25) as r: return json.loads(r.read().decode("utf-8"))
def sim(a,b):
    a=set(clean(a).split()); b=set(clean(b).split())
    return len(a & b) / max(1, len(a | b))
def find_fixture(day, home, away, key):
    best=None; best_score=-1
    for fx in call("fixtures", {"date": day}, key).get("response") or []:
        teams=fx.get("teams") or {}; h=(teams.get("home") or {}).get("name",""); a=(teams.get("away") or {}).get("name","")
        score=max(sim(home,h)+sim(away,a), sim(home,a)+sim(away,h))
        if score>best_score: best=fx; best_score=score
    return best if best_score >= 0.35 else None
def read_csv(path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def stat_value(stats, aliases):
    aliases={clean(a) for a in aliases}
    for item in stats or []:
        if clean(item.get("type")) in aliases:
            return maybe_num(item.get("value"))
    return ""
def fixture_stats(fid, team_id, key):
    try: resp=call("fixtures/statistics", {"fixture": fid, "team": team_id}, key).get("response") or []
    except Exception: return {}
    if not resp: return {}
    st=resp[0].get("statistics") or []
    return {
        "shots": stat_value(st, {"Total Shots"}),
        "sot": stat_value(st, {"Shots on Goal"}),
        "corners": stat_value(st, {"Corner Kicks"}),
        "possession": stat_value(st, {"Ball Possession"}),
        "fouls": stat_value(st, {"Fouls"}),
        "yellows": stat_value(st, {"Yellow Cards"}),
        "xg": stat_value(st, {"Expected Goals", "expected_goals", "xG", "Expected goals"}),
    }
def actual_result(hg, ag):
    if hg > ag: return "HOME"
    if ag > hg: return "AWAY"
    return "DRAW"
def result_grade(forecast, actual):
    f=s(forecast).upper()
    if f == actual: return "PASS"
    if f == "HOME_OR_DRAW" and actual in {"HOME","DRAW"}: return "PASS"
    if f == "AWAY_OR_DRAW" and actual in {"AWAY","DRAW"}: return "PASS"
    if f == "BALANCED": return "NEUTRAL"
    return "MISS"
def split_score(score):
    try:
        a,b=s(score).split("-"); return int(a.strip()), int(b.strip())
    except Exception: return None, None
def score_grade(forecast_score, hg, ag):
    fh,fa=split_score(forecast_score)
    if fh is None: return "NO_FORECAST_SCORE"
    if fh==hg and fa==ag: return "EXACT"
    if abs(fh-hg)+abs(fa-ag) <= 1: return "NEIGHBOR"
    if abs((fh-fa)-(hg-ag)) <= 1: return "SCRIPT_NEIGHBOR"
    return "MISS"
def bool_grade(prob_yes, actual_yes, threshold=50.0):
    pred_yes=fnum(prob_yes) >= threshold
    return "PASS" if pred_yes == actual_yes else "MISS"
def err(pred, actual):
    if actual == "" or s(actual)=="": return ""
    return round(fnum(actual) - fnum(pred), 2)
def branch_grade(row, hg, ag, status):
    if status not in FINAL_STATUS: return "NOT_FINAL"
    total=hg+ag
    under35 = total <= 3
    home_not_loss = hg >= ag
    if home_not_loss and under35: return "BASE_BRANCH_PASS"
    if hg == ag and total <= 2: return "DRAW_DANGER_BRANCH_REALIZED"
    if ag > hg: return "ADVERSE_BRANCH_REALIZED"
    if total >= 4: return "GOAL_SUPPRESSION_FAIL"
    return "MIXED_BRANCH"
def learning(row, hg, ag, stats_home, stats_away, status):
    flags=[]
    if status not in FINAL_STATUS:
        return "NOT_FINAL", "Match not final; rerun after FT."
    total=hg+ag
    if result_grade(row.get("result_forecast"), actual_result(hg,ag)) != "PASS": flags.append("RESULT_MISS")
    sg=score_grade(row.get("ft_score_primary"), hg, ag)
    if sg not in {"EXACT","NEIGHBOR"}: flags.append("SCORELINE_MISS")
    if bool_grade(row.get("btts_yes_pct"), hg>0 and ag>0) != "PASS": flags.append("BTTS_MISS")
    if bool_grade(row.get("over_25_pct"), total>=3) != "PASS": flags.append("OVER25_MISS")
    if bool_grade(row.get("under_35_pct"), total<=3, threshold=50) != "PASS": flags.append("UNDER35_MISS")
    if stats_home.get("shots") != "" and abs(err(row.get("home_shots"), stats_home.get("shots"))) >= 5: flags.append("HOME_SHOTS_ERROR")
    if stats_away.get("shots") != "" and abs(err(row.get("away_shots"), stats_away.get("shots"))) >= 5: flags.append("AWAY_SHOTS_ERROR")
    if stats_home.get("sot") != "" and abs(err(row.get("home_sot"), stats_home.get("sot"))) >= 3: flags.append("HOME_SOT_ERROR")
    if stats_away.get("sot") != "" and abs(err(row.get("away_sot"), stats_away.get("sot"))) >= 3: flags.append("AWAY_SOT_ERROR")
    if not flags: verdict="CLEAN_HIT"
    elif len(flags) <= 2 and "RESULT_MISS" not in flags: verdict="PARTIAL_HIT"
    elif "RESULT_MISS" in flags: verdict="CORE_RESULT_FAIL"
    else: verdict="MIXED_OR_STATS_FAIL"
    return " | ".join(flags) if flags else "NONE", verdict
def robust_grade(row, hg, ag):
    robust=clean(row.get("market_logic_robust"))
    total=hg+ag
    home_or_draw=hg>=ag; under35=total<=3
    if "under 3 5" in robust and home_or_draw and under35: return "PASS"
    if "under 3 5" in robust and not under35: return "MISS_UNDER"
    if "draw" in robust and not home_or_draw: return "MISS_SIDE"
    return "NOT_EVALUATED"
def value_grade(row, hg, ag):
    value=clean(row.get("market_logic_value")); home_goals=hg; home_not_loss=hg>=ag
    if "dnb" in value and home_not_loss: return "PASS_OR_PUSH"
    if "team over 0 5" in value and home_goals>=1: return "PASS"
    if "dnb" in value and not home_not_loss: return "MISS"
    return "NOT_EVALUATED"
def xg_direction(row, ahxg, aaxg):
    if ahxg=="" or aaxg=="": return "NO_ACTUAL_XG"
    pred_home_edge=fnum(row.get("home_xg"))-fnum(row.get("away_xg"))
    actual_home_edge=fnum(ahxg)-fnum(aaxg)
    if pred_home_edge == 0 or actual_home_edge == 0: return "NEUTRAL"
    return "PASS" if (pred_home_edge > 0) == (actual_home_edge > 0) else "MISS"
def build_row(day, now, home, away, base, key):
    file_slug=slug(home+"_vs_"+away)
    forecasts=read_csv(base/"today"/day/f"vsigma_adhoc_match_stat_forecast_{file_slug}.csv")
    if not forecasts:
        return {"target_date":day,"generated_at":now,"home_team":home,"away_team":away,"match_status":"FORECAST_MISSING","learning_verdict":"NO_FORECAST","auto_apply":"NO","production_change":"NO"}
    row=forecasts[0]
    fx=find_fixture(day, home, away, key) if key else None
    if not fx:
        return {**{k:row.get(k,"") for k in row},"target_date":day,"generated_at":now,"match_status":"FIXTURE_NOT_FOUND","learning_verdict":"NO_ACTUAL_FIXTURE","auto_apply":"NO","production_change":"NO"}
    fid=s((fx.get("fixture") or {}).get("id")); teams=fx.get("teams") or {}; home_id=s((teams.get("home") or {}).get("id")); away_id=s((teams.get("away") or {}).get("id"))
    status=s(((fx.get("fixture") or {}).get("status") or {}).get("short"))
    goals=fx.get("goals") or {}; hg=int(goals.get("home") or 0); ag=int(goals.get("away") or 0)
    stats_h=fixture_stats(fid, home_id, key) if key and fid and home_id else {}; stats_a=fixture_stats(fid, away_id, key) if key and fid and away_id else {}
    ar=actual_result(hg,ag); flags, verdict=learning(row,hg,ag,stats_h,stats_a,status)
    actual_btts=hg>0 and ag>0; actual_over25=(hg+ag)>=3; actual_under35=(hg+ag)<=3
    out={"target_date":day,"generated_at":now,"fixture_id":fid,"home_team":s((teams.get("home") or {}).get("name")) or home,"away_team":s((teams.get("away") or {}).get("name")) or away,"match_status":status,"actual_score":f"{hg}-{ag}","forecast_score":row.get("ft_score_primary",""),"scoreline_grade":score_grade(row.get("ft_score_primary"),hg,ag),"forecast_result":row.get("result_forecast",""),"actual_result":ar,"result_grade":result_grade(row.get("result_forecast"),ar),"market_robust_grade":robust_grade(row,hg,ag),"market_value_grade":value_grade(row,hg,ag),"raw_home_prob":row.get("raw_home_prob",row.get("home_prob","")),"raw_draw_prob":row.get("raw_draw_prob",row.get("draw_prob","")),"raw_away_prob":row.get("raw_away_prob",row.get("away_prob","")),"adjusted_home_prob":row.get("home_prob",""),"adjusted_draw_prob":row.get("draw_prob",""),"adjusted_away_prob":row.get("away_prob",""),"forecast_btts_yes_pct":row.get("btts_yes_pct",""),"actual_btts":actual_btts,"btts_grade":bool_grade(row.get("btts_yes_pct"),actual_btts),"forecast_over25_pct":row.get("over_25_pct",""),"actual_over25":actual_over25,"over25_grade":bool_grade(row.get("over_25_pct"),actual_over25),"forecast_under35_pct":row.get("under_35_pct",""),"actual_under35":actual_under35,"under35_grade":bool_grade(row.get("under_35_pct"),actual_under35),"forecast_home_xg":row.get("home_xg",""),"forecast_away_xg":row.get("away_xg",""),"actual_home_xg":stats_h.get("xg",""),"actual_away_xg":stats_a.get("xg",""),"home_xg_error":err(row.get("home_xg",""),stats_h.get("xg","")),"away_xg_error":err(row.get("away_xg",""),stats_a.get("xg","")),"xg_direction_grade":xg_direction(row,stats_h.get("xg",""),stats_a.get("xg","")),"forecast_home_shots":row.get("home_shots",""),"actual_home_shots":stats_h.get("shots",""),"home_shots_error":err(row.get("home_shots",""),stats_h.get("shots","")),"forecast_away_shots":row.get("away_shots",""),"actual_away_shots":stats_a.get("shots",""),"away_shots_error":err(row.get("away_shots",""),stats_a.get("shots","")),"forecast_home_sot":row.get("home_sot",""),"actual_home_sot":stats_h.get("sot",""),"home_sot_error":err(row.get("home_sot",""),stats_h.get("sot","")),"forecast_away_sot":row.get("away_sot",""),"actual_away_sot":stats_a.get("sot",""),"away_sot_error":err(row.get("away_sot",""),stats_a.get("sot","")),"forecast_home_corners":row.get("home_corners",""),"actual_home_corners":stats_h.get("corners",""),"home_corners_error":err(row.get("home_corners",""),stats_h.get("corners","")),"forecast_away_corners":row.get("away_corners",""),"actual_away_corners":stats_a.get("corners",""),"away_corners_error":err(row.get("away_corners",""),stats_a.get("corners","")),"forecast_home_possession":row.get("home_possession_pct",""),"actual_home_possession":stats_h.get("possession",""),"home_possession_error":err(row.get("home_possession_pct",""),stats_h.get("possession","")),"forecast_away_possession":row.get("away_possession_pct",""),"actual_away_possession":stats_a.get("possession",""),"away_possession_error":err(row.get("away_possession_pct",""),stats_a.get("possession","")),"draw_risk_index":row.get("draw_risk_index",""),"goal_suppression_index":row.get("goal_suppression_index",""),"unit_edge":row.get("unit_edge",""),"forecast_branch_base":row.get("tactical_branch_base",""),"forecast_danger_branch":row.get("danger_branch",""),"branch_grade":branch_grade(row,hg,ag,status),"learning_flags":flags,"learning_verdict":verdict,"auto_apply":"NO","production_change":"NO"}
    return out
def md(row):
    out=[f"# vSIGMA Ad Hoc Post-Match Learning Ledger - {row.get('target_date')}","","## Summary",f"- fixture: {row.get('home_team')} vs {row.get('away_team')}",f"- status: {row.get('match_status')}",f"- actual_score: {row.get('actual_score')}",f"- forecast_score: {row.get('forecast_score')}",f"- learning_verdict: {row.get('learning_verdict')}",f"- learning_flags: {row.get('learning_flags')}","- auto_apply: NO","- production_change: NO","","## Result Audit",f"- result_grade: {row.get('result_grade')}",f"- scoreline_grade: {row.get('scoreline_grade')}",f"- branch_grade: {row.get('branch_grade')}",f"- market_robust_grade: {row.get('market_robust_grade')}",f"- market_value_grade: {row.get('market_value_grade')}","","## Market/Goal Family Audit",f"- BTTS: forecast_yes={row.get('forecast_btts_yes_pct')} | actual={row.get('actual_btts')} | grade={row.get('btts_grade')}",f"- Over 2.5: forecast={row.get('forecast_over25_pct')} | actual={row.get('actual_over25')} | grade={row.get('over25_grade')}",f"- Under 3.5: forecast={row.get('forecast_under35_pct')} | actual={row.get('actual_under35')} | grade={row.get('under35_grade')}","","## xG Audit",f"- forecast_xG: {row.get('home_team')} {row.get('forecast_home_xg')} - {row.get('forecast_away_xg')} {row.get('away_team')}",f"- actual_xG: {row.get('home_team')} {row.get('actual_home_xg')} - {row.get('actual_away_xg')} {row.get('away_team')}",f"- xg_error: home={row.get('home_xg_error')} | away={row.get('away_xg_error')} | direction={row.get('xg_direction_grade')}","","## Stats Audit",f"- shots: forecast {row.get('forecast_home_shots')}-{row.get('forecast_away_shots')} | actual {row.get('actual_home_shots')}-{row.get('actual_away_shots')} | error {row.get('home_shots_error')}/{row.get('away_shots_error')}",f"- shots_on_target: forecast {row.get('forecast_home_sot')}-{row.get('forecast_away_sot')} | actual {row.get('actual_home_sot')}-{row.get('actual_away_sot')} | error {row.get('home_sot_error')}/{row.get('away_sot_error')}",f"- corners: forecast {row.get('forecast_home_corners')}-{row.get('forecast_away_corners')} | actual {row.get('actual_home_corners')}-{row.get('actual_away_corners')} | error {row.get('home_corners_error')}/{row.get('away_corners_error')}",f"- possession: forecast {row.get('forecast_home_possession')}-{row.get('forecast_away_possession')} | actual {row.get('actual_home_possession')}-{row.get('actual_away_possession')} | error {row.get('home_possession_error')}/{row.get('away_possession_error')}","","## Model Learning",f"- draw_risk_index: {row.get('draw_risk_index')}",f"- goal_suppression_index: {row.get('goal_suppression_index')}",f"- unit_edge: {row.get('unit_edge')}",f"- base_branch: {row.get('forecast_branch_base')}",f"- danger_branch: {row.get('forecast_danger_branch')}","","## Note","- Diagnostic ledger only. It does not modify production rules automatically."]
    return "\n".join(out)+"\n"
def run(day, home, away, tz, base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); key=api_key(); file_slug=slug(home+"_vs_"+away)
    row=build_row(day, now, home, away, base, key)
    summary={"target_date":day,"generated_at":now,"query_home":home,"query_away":away,"rows":1,"match_status":row.get("match_status",""),"learning_verdict":row.get("learning_verdict",""),"next_action":"Review ledger and decide whether to promote lessons manually.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/f"vsigma_adhoc_postmatch_learning_{file_slug}.csv",[row],FIELDS)
        write_csv(folder/f"vsigma_adhoc_postmatch_learning_{file_slug}_summary.csv",[summary],SUMMARY_FIELDS)
        (folder/f"vsigma_adhoc_postmatch_learning_{file_slug}.md").write_text(md(row),encoding="utf-8")
    print(f"Ad hoc postmatch learning ledger built status={row.get('match_status')} verdict={row.get('learning_verdict')}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--home",required=True); ap.add_argument("--away",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.home,a.away,a.timezone,a.processed_dir)
