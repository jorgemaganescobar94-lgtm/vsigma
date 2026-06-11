from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
FIELDS = [
    "target_date","generated_at","fixture_id","home_team","away_team","xi_status","xi_source","home_shape","away_shape",
    "impact_weighting_status","home_xi_strength","away_xi_strength","xi_edge","home_attack_index","away_attack_index","home_defense_index","away_defense_index","home_control_index","away_control_index","home_set_piece_index","away_set_piece_index","draw_risk_index","goal_suppression_index",
    "raw_home_prob","raw_draw_prob","raw_away_prob","home_prob","draw_prob","away_prob",
    "result_forecast","scorelines","goal_profile","scenario","confidence",
    "raw_home_xg","raw_away_xg","home_xg","away_xg","total_xg","home_first_half_xg","away_first_half_xg","home_second_half_xg","away_second_half_xg",
    "ht_score_forecast","ft_score_primary","first_goal_team","first_goal_window","btts_yes_pct","over_15_pct","over_25_pct","under_35_pct",
    "home_clean_sheet_pct","away_goal_pct","home_shots","away_shots","home_sot","away_sot","home_big_chances","away_big_chances",
    "home_possession_pct","away_possession_pct","home_corners","away_corners","home_fouls","away_fouls","home_yellow_cards","away_yellow_cards",
    "home_saves","away_saves","match_tempo","home_pressure_index","away_pressure_index","tactical_branch_base","danger_branch","market_logic_robust",
    "market_logic_value","market_do_not_overstretch","first_half_script","second_half_script","impact_adjustment_note","stat_confidence","note","auto_apply","production_change"
]
SUMMARY_FIELDS = ["target_date","generated_at","query_home","query_away","rows","stat_confidence","impact_weighting_status","next_action","auto_apply","production_change"]
OFFENSIVE_ROLES={"STRIKER","STRIKER_PAIR","WINGER","WIDE_MIDFIELD","ATTACKING_MIDFIELD","INTERIOR"}
DEFENSIVE_ROLES={"GOALKEEPER","CENTER_BACK","FULL_BACK","WING_BACK","DEFENSIVE_MIDFIELD"}
CONTROL_ROLES={"DEFENSIVE_MIDFIELD","CENTRAL_MIDFIELD","INTERIOR","ATTACKING_MIDFIELD"}

def s(v): return "" if v is None else str(v).strip()
def clean(v):
    v=unicodedata.normalize("NFKD", s(v)).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", v).strip()
def slug(v): return re.sub(r"[^a-z0-9]+", "_", clean(v)).strip("_") or "fixture"
def fnum(v, default=0.0):
    try: return float(s(v))
    except Exception: return default
def pct(x): return round(max(0, min(100, x)), 1)
def clamp(x, lo, hi): return max(lo, min(hi, x))
def exp_neg(x): return 2.718281828 ** (-x)
def read_csv(path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def primary_score(scorelines): return (s(scorelines).split("/")[0]).strip() if s(scorelines) else ""
def split_score(score):
    try:
        a,b=score.split("-"); return int(a.strip()), int(b.strip())
    except Exception: return 1,0
def avg(vals): return round(sum(vals)/len(vals),1) if vals else 0.0
def normalize_probs(h,d,a):
    h=max(0.02,h); d=max(0.02,d); a=max(0.02,a); tot=h+d+a
    return h/tot,d/tot,a/tot
def impact_context(day, base, file_slug):
    player_rows=read_csv(base/"today"/day/f"vsigma_adhoc_player_impact_{file_slug}.csv")
    style_rows=read_csv(base/"today"/day/f"vsigma_adhoc_team_style_{file_slug}.csv")
    summary_rows=read_csv(base/"today"/day/f"vsigma_adhoc_team_style_player_impact_{file_slug}_summary.csv")
    if not player_rows:
        return {"impact_weighting_status":"NO_PLAYER_IMPACT_DATA","home_xi_strength":0,"away_xi_strength":0,"xi_edge":0,"home_attack_index":0,"away_attack_index":0,"home_defense_index":0,"away_defense_index":0,"home_control_index":0,"away_control_index":0,"home_set_piece_index":0,"away_set_piece_index":0,"draw_risk_index":50,"goal_suppression_index":50,"home_compact_block":False,"away_compact_block":False,"note":"No player-impact file available; forecast uses base model only."}
    by={"home":[],"away":[]}
    for r in player_rows:
        side=clean(r.get("team_side"));
        if side in by: by[side].append(r)
    def idx(side, field, roles=None):
        vals=[]
        for p in by[side]:
            if roles and s(p.get("tactical_role")) not in roles: continue
            vals.append(fnum(p.get(field)))
        return avg(vals or [fnum(p.get(field)) for p in by[side]])
    def strength(side): return avg([fnum(p.get("player_impact_score")) for p in by[side]])
    h_str=strength("home"); a_str=strength("away"); edge=round(h_str-a_str,1)
    h_atk=idx("home","attack_impact",OFFENSIVE_ROLES); a_atk=idx("away","attack_impact",OFFENSIVE_ROLES)
    h_def=idx("home","defense_impact",DEFENSIVE_ROLES); a_def=idx("away","defense_impact",DEFENSIVE_ROLES)
    h_ctl=idx("home","control_impact",CONTROL_ROLES); a_ctl=idx("away","control_impact",CONTROL_ROLES)
    h_sp=idx("home","set_piece_impact"); a_sp=idx("away","set_piece_impact")
    style={clean(r.get("team_side")):r for r in style_rows}
    home_compact="COMPACT" in s(style.get("home",{}).get("defense_style")) or s(style.get("home",{}).get("usual_shape")).startswith("5-")
    away_compact="COMPACT" in s(style.get("away",{}).get("defense_style")) or s(style.get("away",{}).get("usual_shape")).startswith("5-")
    draw_risk=50 + (a_def-h_atk)*0.45 + max(0,-edge)*1.1 + (8 if away_compact else 0) + (3 if a_sp>h_sp+3 else 0)
    suppression=50 + (a_def-h_atk)*0.50 + (8 if away_compact else 0) - max(0,h_atk-70)*0.25
    return {"impact_weighting_status":"PLAYER_IMPACT_WEIGHTED","home_xi_strength":h_str,"away_xi_strength":a_str,"xi_edge":edge,"home_attack_index":h_atk,"away_attack_index":a_atk,"home_defense_index":h_def,"away_defense_index":a_def,"home_control_index":h_ctl,"away_control_index":a_ctl,"home_set_piece_index":h_sp,"away_set_piece_index":a_sp,"draw_risk_index":round(clamp(draw_risk,20,90),1),"goal_suppression_index":round(clamp(suppression,20,90),1),"home_compact_block":home_compact,"away_compact_block":away_compact,"note":"Forecast adjusted by XI strength, role-resolved player impact and team style."}
def choose_score(hxg, axg, hp, dp, ap, under35, scorelines):
    if hxg >= 1.45 and axg <= 0.75 and hp >= 0.58 and under35 >= 72: return "1-0"
    if hxg >= 1.75 and axg <= 0.70 and hp >= 0.64: return "2-0"
    if dp >= 0.27 and axg >= 0.70: return "1-1"
    if hxg < 1.15 and axg < 0.75: return "0-0 / 1-0"
    return primary_score(scorelines)
def stat_model(r, impact):
    raw_hp=fnum(r.get("home_prob")); raw_dp=fnum(r.get("draw_prob")); raw_ap=fnum(r.get("away_prob"))
    hp,dp,ap=raw_hp,raw_dp,raw_ap
    fav_gap=hp-ap
    goal=s(r.get("goal_profile")); scen=s(r.get("scenario")); xi=s(r.get("xi_status")); hs=s(r.get("home_shape")); aw=s(r.get("away_shape"))
    result=s(r.get("result_forecast")); scorelines=s(r.get("scorelines"))
    total_xg=2.35
    if "LOW" in goal: total_xg=2.05
    if "MODERATE" in goal: total_xg=2.35
    if "OPEN" in goal: total_xg=2.75
    if "HIGH" in goal: total_xg=3.15
    if "OPEN" in scen: total_xg += 0.15
    if xi == "OFFICIAL_XI": total_xg += 0.03
    share=0.50 + clamp(fav_gap, -0.45, 0.45) * 0.42
    if "HOME" in result: share += 0.04
    if hs.startswith("4-3-3") or hs.startswith("4-2-3-1"): share += 0.02
    if hs.startswith("4-1-4-1") and aw.startswith("5-"): share += 0.04
    if aw.startswith("4-3-3") and fav_gap > 0.25: share += 0.01
    if aw.startswith("5-"): total_xg -= 0.08
    share=clamp(share,0.38,0.72)
    raw_hxg=round(total_xg*share,2); raw_axg=round(total_xg-raw_hxg,2)

    if impact.get("impact_weighting_status") == "PLAYER_IMPACT_WEIGHTED":
        edge=fnum(impact.get("xi_edge")); h_atk=fnum(impact.get("home_attack_index")); a_atk=fnum(impact.get("away_attack_index")); h_def=fnum(impact.get("home_defense_index")); a_def=fnum(impact.get("away_defense_index")); draw_risk=fnum(impact.get("draw_risk_index")); suppression=fnum(impact.get("goal_suppression_index"))
        home_prob_delta=clamp(edge*0.003 + (h_atk-a_def)*0.0010, -0.035, 0.035)
        away_prob_delta=clamp(-edge*0.0012 + (a_atk-h_def)*0.0008, -0.025, 0.025)
        draw_delta=clamp((draw_risk-55)*0.0020, -0.025, 0.045)
        hp,dp,ap=normalize_probs(hp+home_prob_delta, dp+draw_delta, ap+away_prob_delta)
        hxg_delta=clamp((h_atk-a_def)*0.006 + edge*0.010, -0.20, 0.18)
        axg_delta=clamp((a_atk-h_def)*0.005 - edge*0.004, -0.12, 0.15)
        total_xg_delta=clamp((50-suppression)*0.004, -0.18, 0.10)
        hxg=max(0.25, round(raw_hxg+hxg_delta+total_xg_delta/2,2)); axg=max(0.20, round(raw_axg+axg_delta+total_xg_delta/2,2))
    else:
        hxg,axg=raw_hxg,raw_axg
    total_xg=round(hxg+axg,2); fav_gap=hp-ap

    home_first=round(hxg*0.44,2); away_first=round(axg*0.42,2); home_second=round(hxg-home_first,2); away_second=round(axg-away_first,2)
    btts=pct(100*(1-exp_neg(hxg))*(1-exp_neg(axg)))
    over15=pct(100*(1-exp_neg(total_xg)*(1+total_xg)))
    over25=pct(100*(1-exp_neg(total_xg)*(1+total_xg+(total_xg**2)/2)))
    under35=pct(100*(exp_neg(total_xg)*(1+total_xg+(total_xg**2)/2+(total_xg**3)/6)))
    home_cs=pct(100*exp_neg(axg)); away_goal=pct(100*(1-exp_neg(axg)))
    ft_primary=choose_score(hxg,axg,hp,dp,ap,under35,scorelines)
    if total_xg < 2.15: goal_profile="LOW_TO_MODERATE_GOALS"
    elif total_xg < 2.55: goal_profile="MODERATE_GOALS"
    else: goal_profile="OPEN_GOALS"
    result_forecast="HOME_OR_DRAW" if hp>=ap and hp+dp>=0.76 else ("AWAY_OR_DRAW" if ap>hp and ap+dp>=0.70 else "BALANCED")

    home_shots=round(7.5 + hxg*4.2 + max(0,fav_gap)*4.0); away_shots=round(6.0 + axg*4.0 + max(0,-fav_gap)*3.0)
    home_sot=clamp(round(hxg*2.7),1,8); away_sot=clamp(round(axg*2.6),1,6)
    home_bc=clamp(round(hxg*1.35),0,4); away_bc=clamp(round(axg*1.20),0,3)
    home_pos=round(clamp(50 + fav_gap*24 + (4 if "FAVORITE_CONTROL" in scen else 0) + (3 if aw.startswith("5-") else 0) + (fnum(impact.get("home_control_index"))-fnum(impact.get("away_control_index")))*0.10,42,70)); away_pos=100-home_pos
    home_corners=clamp(round(3.0 + home_shots*0.18 + max(0,fav_gap)*2.0),2,10); away_corners=clamp(round(2.5 + away_shots*0.16),1,7)
    home_fouls=round(11.5 + max(0,-fav_gap)*5 + (1 if away_pos>48 else 0)); away_fouls=round(12.0 + max(0,fav_gap)*5 + (1 if home_pos>55 else 0) + (1 if aw.startswith("5-") else 0))
    home_yc=clamp(round(home_fouls/7.5),1,4); away_yc=clamp(round(away_fouls/6.8),1,5); home_saves=clamp(away_sot-1,0,5); away_saves=clamp(home_sot-1,0,7)
    if home_first + away_first < 1.0: ht="0-0 / 1-0"
    elif home_first > away_first + 0.30: ht="1-0"
    else: ht="0-0 / 1-1"
    first_team = r.get("home_team") if hp >= ap + 0.15 else (r.get("away_team") if ap >= hp + 0.15 else "NO_CLEAR_EDGE")
    first_window = "25-55" if first_team != "NO_CLEAR_EDGE" else "NO_CLEAR_WINDOW"
    tempo = "CONTROLLED" if total_xg < 2.55 and home_pos >= 58 else ("OPEN" if total_xg >= 2.75 else "MEDIUM")
    home_pressure=round((home_pos/100)*35 + home_shots*2.0 + home_corners*3.0 + home_bc*8.0,1); away_pressure=round((away_pos/100)*35 + away_shots*2.0 + away_corners*3.0 + away_bc*8.0,1)
    if "FAVORITE_CONTROL" in scen:
        fh="Home control, away compact; first goal value high; HT likely 0-0 or 1-0."
        sh="If home scores first, game management; if 0-0 after 60', draw branch rises sharply."
        base_branch="Home territorial control against compact away block."
        danger_branch="0-0 after 60' or away transition/set-piece keeps draw alive."
    else:
        fh="Tight early rhythm; low-to-medium tempo if no early goal."; sh="Late subs and conversion quality decide; draw branch remains alive."; base_branch="Balanced low-to-medium tempo script."; danger_branch="Low conversion or late mistake decides."
    if impact.get("impact_weighting_status") == "PLAYER_IMPACT_WEIGHTED":
        if fnum(impact.get("draw_risk_index")) >= 65:
            danger_branch += " Player-impact layer raises draw risk due to away defensive structure/XI balance."
        if fnum(impact.get("goal_suppression_index")) >= 65:
            no_stretch="Avoid handicap/goleada; player-impact layer suppresses blowout path unless early goal + sustained xG pressure confirms."
        else:
            no_stretch="Avoid handicap/goleada unless early goal + sustained xG pressure confirms."
    else:
        no_stretch="Avoid handicap/goleada unless early goal + sustained xG pressure confirms."
    robust=f"{r.get('home_team')} or draw / under 3.5"; value=f"{r.get('home_team')} DNB / {r.get('home_team')} team over 0.5"
    stat_conf="MEDIUM_HIGH" if xi == "OFFICIAL_XI" else ("LOW_TO_MEDIUM" if xi == "ESTIMATED_XI" else "LOW")
    impact_note=impact.get("note","")
    return {**impact,"raw_home_prob":round(raw_hp,4),"raw_draw_prob":round(raw_dp,4),"raw_away_prob":round(raw_ap,4),"home_prob":round(hp,4),"draw_prob":round(dp,4),"away_prob":round(ap,4),"result_forecast":result_forecast,"goal_profile":goal_profile,"raw_home_xg":raw_hxg,"raw_away_xg":raw_axg,"home_xg":hxg,"away_xg":axg,"total_xg":total_xg,"home_first_half_xg":home_first,"away_first_half_xg":away_first,"home_second_half_xg":home_second,"away_second_half_xg":away_second,"ht_score_forecast":ht,"ft_score_primary":ft_primary,"first_goal_team":first_team,"first_goal_window":first_window,"btts_yes_pct":btts,"over_15_pct":over15,"over_25_pct":over25,"under_35_pct":under35,"home_clean_sheet_pct":home_cs,"away_goal_pct":away_goal,"home_shots":home_shots,"away_shots":away_shots,"home_sot":home_sot,"away_sot":away_sot,"home_big_chances":home_bc,"away_big_chances":away_bc,"home_possession_pct":home_pos,"away_possession_pct":away_pos,"home_corners":home_corners,"away_corners":away_corners,"home_fouls":home_fouls,"away_fouls":away_fouls,"home_yellow_cards":home_yc,"away_yellow_cards":away_yc,"home_saves":home_saves,"away_saves":away_saves,"match_tempo":tempo,"home_pressure_index":home_pressure,"away_pressure_index":away_pressure,"tactical_branch_base":base_branch,"danger_branch":danger_branch,"market_logic_robust":robust,"market_logic_value":value,"market_do_not_overstretch":no_stretch,"first_half_script":fh,"second_half_script":sh,"impact_adjustment_note":impact_note,"stat_confidence":stat_conf}
def md(row, summary):
    out=[f"# vSIGMA Ad Hoc Full Match Projection - {row.get('target_date')}","","## Summary",f"- rows: {summary['rows']}",f"- stat_confidence: {summary['stat_confidence']}",f"- impact_weighting_status: {summary.get('impact_weighting_status','')}","- auto_apply: NO","- production_change: NO","","## Fixture"]
    if not row:
        out.append("- none. No ad hoc fixture forecast available."); return "\n".join(out)+"\n"
    out += [f"- fixture: {row['home_team']} vs {row['away_team']}",f"- XI: {row['xi_status']} | source={row['xi_source']} | shapes={row['home_shape']}/{row['away_shape']}",f"- result_forecast: {row['result_forecast']}",f"- primary_score: {row['ft_score_primary']}",f"- scorelines_base: {row['scorelines']}",f"- adjusted_goal_profile: {row['goal_profile']}",f"- scenario: {row['scenario']}",f"- tempo: {row['match_tempo']}","","## Player Impact Weighting",f"- status: {row['impact_weighting_status']}",f"- XI strength: {row['home_team']} {row['home_xi_strength']} - {row['away_xi_strength']} {row['away_team']} | edge={row['xi_edge']}",f"- attack_index: {row['home_team']} {row['home_attack_index']} - {row['away_attack_index']} {row['away_team']}",f"- defense_index: {row['home_team']} {row['home_defense_index']} - {row['away_defense_index']} {row['away_team']}",f"- control_index: {row['home_team']} {row['home_control_index']} - {row['away_control_index']} {row['away_team']}",f"- set_piece_index: {row['home_team']} {row['home_set_piece_index']} - {row['away_set_piece_index']} {row['away_team']}",f"- draw_risk_index: {row['draw_risk_index']}",f"- goal_suppression_index: {row['goal_suppression_index']}",f"- adjustment_note: {row['impact_adjustment_note']}","","## Probability Layer",f"- raw 1X2: {row['home_team']} {float(row['raw_home_prob'])*100:.1f}% | draw {float(row['raw_draw_prob'])*100:.1f}% | {row['away_team']} {float(row['raw_away_prob'])*100:.1f}%",f"- adjusted 1X2: {row['home_team']} {float(row['home_prob'])*100:.1f}% | draw {float(row['draw_prob'])*100:.1f}% | {row['away_team']} {float(row['away_prob'])*100:.1f}%",f"- BTTS yes: {row['btts_yes_pct']}%",f"- Over 1.5: {row['over_15_pct']}%",f"- Over 2.5: {row['over_25_pct']}%",f"- Under 3.5: {row['under_35_pct']}%",f"- {row['home_team']} clean sheet: {row['home_clean_sheet_pct']}%",f"- {row['away_team']} to score: {row['away_goal_pct']}%","","## Expected Goals By Phase",f"- raw_xG: {row['home_team']} {row['raw_home_xg']} - {row['raw_away_xg']} {row['away_team']}",f"- adjusted full_match_xG: {row['home_team']} {row['home_xg']} - {row['away_xg']} {row['away_team']} | total={row['total_xg']}",f"- first_half_xG: {row['home_team']} {row['home_first_half_xg']} - {row['away_first_half_xg']} {row['away_team']}",f"- second_half_xG: {row['home_team']} {row['home_second_half_xg']} - {row['away_second_half_xg']} {row['away_team']}",f"- HT score forecast: {row['ht_score_forecast']}",f"- first goal: {row['first_goal_team']} | window={row['first_goal_window']}","","## Predicted Match Stats",f"- shots: {row['home_team']} {row['home_shots']} - {row['away_shots']} {row['away_team']}",f"- shots_on_target: {row['home_team']} {row['home_sot']} - {row['away_sot']} {row['away_team']}",f"- big_chances: {row['home_team']} {row['home_big_chances']} - {row['away_big_chances']} {row['away_team']}",f"- possession: {row['home_team']} {row['home_possession_pct']}% - {row['away_possession_pct']}% {row['away_team']}",f"- corners: {row['home_team']} {row['home_corners']} - {row['away_corners']} {row['away_team']}",f"- fouls: {row['home_team']} {row['home_fouls']} - {row['away_fouls']} {row['away_team']}",f"- yellow_cards: {row['home_team']} {row['home_yellow_cards']} - {row['away_yellow_cards']} {row['away_team']}",f"- saves: {row['home_team']} {row['home_saves']} - {row['away_saves']} {row['away_team']}",f"- pressure_index: {row['home_team']} {row['home_pressure_index']} - {row['away_pressure_index']} {row['away_team']}","","## Branch Map",f"- base_branch: {row['tactical_branch_base']}",f"- danger_branch: {row['danger_branch']}",f"- first_half: {row['first_half_script']}",f"- second_half: {row['second_half_script']}","","## Market Logic Translation",f"- robust: {row['market_logic_robust']}",f"- value_expression: {row['market_logic_value']}",f"- do_not_overstretch: {row['market_do_not_overstretch']}","","## Note",f"- {row['note']}"]
    return "\n".join(out)+"\n"
def run(day,home,away,tz,base):
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); file_slug=slug(home+"_vs_"+away)
    forecast_rows=read_csv(base/"today"/day/f"vsigma_adhoc_fixture_forecast_{file_slug}.csv")
    impact=impact_context(day,base,file_slug); out=[]
    if forecast_rows:
        r=dict(forecast_rows[0]); stats=stat_model(r,impact); r.update(stats); r["generated_at"]=now; r["note"]="Full match projection derived from ad hoc fixture forecast, official/estimated XI, market-implied probabilities, team style and player-impact weighting. Diagnostic only; not a betting instruction."; out=[r]
    summary={"target_date":day,"generated_at":now,"query_home":home,"query_away":away,"rows":len(out),"stat_confidence":out[0].get("stat_confidence","") if out else "NONE","impact_weighting_status":impact.get("impact_weighting_status",""),"next_action":"Use as impact-weighted full match projection only; rerun after official XI or material news.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        row=out[0] if out else {"target_date":day}
        write_csv(folder/f"vsigma_adhoc_match_stat_forecast_{file_slug}.csv",out,FIELDS)
        write_csv(folder/f"vsigma_adhoc_match_stat_forecast_{file_slug}_summary.csv",[summary],SUMMARY_FIELDS)
        (folder/f"vsigma_adhoc_match_stat_forecast_{file_slug}.md").write_text(md(row,summary),encoding="utf-8")
    print(f"Ad hoc impact-weighted full match projection built rows={len(out)}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--home",required=True); ap.add_argument("--away",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.home,a.away,a.timezone,a.processed_dir)
