from __future__ import annotations

import argparse
import csv
import json
import os
import re
import unicodedata
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
STYLE_FIELDS = ["target_date","generated_at","fixture_id","team_side","team_id","team_name","style_source","matches_sample","avg_possession","avg_shots","avg_sot","avg_corners","avg_fouls","avg_yellows","avg_goals_for","avg_goals_against","usual_shape","tempo_label","attack_style","defense_style","set_piece_weight","transition_weight","style_confidence","note","auto_apply","production_change"]
PLAYER_FIELDS = ["target_date","generated_at","fixture_id","team_side","team_id","team_name","player_id","player_name","position","api_position","grid","tactical_role","formation","player_impact_score","attack_impact","defense_impact","control_impact","set_piece_impact","role_label","source_quality","note","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","query_home","query_away","fixture_found","team_rows","player_rows","home_xi_strength","away_xi_strength","xi_edge","style_confidence","next_action","auto_apply","production_change"]

POS_BASE = {"G":66,"D":64,"M":67,"F":69}
POS_ATTACK = {"G":5,"D":20,"M":48,"F":70}
POS_DEFENSE = {"G":80,"D":72,"M":50,"F":22}
POS_CONTROL = {"G":24,"D":44,"M":72,"F":42}
POS_SETPIECE = {"G":5,"D":42,"M":45,"F":40}
ROLE_MODS = {
    "GOALKEEPER": {"def":4,"ctl":0,"atk":0,"sp":0},
    "CENTER_BACK": {"def":9,"ctl":1,"atk":-3,"sp":5},
    "FULL_BACK": {"def":4,"ctl":3,"atk":5,"sp":1},
    "WING_BACK": {"def":4,"ctl":3,"atk":8,"sp":2},
    "DEFENSIVE_MIDFIELD": {"def":7,"ctl":8,"atk":-1,"sp":2},
    "CENTRAL_MIDFIELD": {"def":2,"ctl":8,"atk":2,"sp":1},
    "INTERIOR": {"def":1,"ctl":10,"atk":4,"sp":2},
    "WIDE_MIDFIELD": {"def":0,"ctl":4,"atk":8,"sp":2},
    "ATTACKING_MIDFIELD": {"def":-1,"ctl":9,"atk":9,"sp":3},
    "WINGER": {"def":-2,"ctl":3,"atk":11,"sp":2},
    "STRIKER": {"def":-3,"ctl":0,"atk":13,"sp":4},
    "STRIKER_PAIR": {"def":-2,"ctl":1,"atk":11,"sp":4},
}

def s(v): return "" if v is None else str(v).strip()
def clean(v):
    v = unicodedata.normalize("NFKD", s(v)).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", v).strip()
def slug(v): return re.sub(r"[^a-z0-9]+", "_", clean(v)).strip("_") or "fixture"
def fnum(v, default=0.0):
    try: return float(s(v).replace("%",""))
    except Exception: return default
def clamp(x, lo, hi): return max(lo, min(hi, x))
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
def read_csv(p):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def write_csv(p, rows, fields):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def stat_value(stats, names):
    for item in stats or []:
        typ=clean(item.get("type"))
        if typ in names: return fnum(item.get("value"))
    return 0.0
def recent_fixtures(team_id, key, last=6):
    try: return call("fixtures", {"team": team_id, "last": last}, key).get("response") or []
    except Exception: return []
def fixture_stats(fid, team_id, key):
    try: resp=call("fixtures/statistics", {"fixture": fid, "team": team_id}, key).get("response") or []
    except Exception: return {}
    if not resp: return {}
    stats=resp[0].get("statistics") or []
    return {"possession": stat_value(stats,{"ball possession"}),"shots": stat_value(stats,{"total shots"}),"sot": stat_value(stats,{"shots on goal"}),"corners": stat_value(stats,{"corner kicks"}),"fouls": stat_value(stats,{"fouls"}),"yellows": stat_value(stats,{"yellow cards"})}
def avg(vals): return round(sum(vals)/len(vals),1) if vals else 0.0
def team_style_row(day, now, fx, side, key):
    teams=fx.get("teams") or {}; team=teams.get(side) or {}; tid=s(team.get("id")); name=s(team.get("name"))
    fixtures=recent_fixtures(tid,key,6) if tid else []
    poss=[]; shots=[]; sot=[]; corners=[]; fouls=[]; yellows=[]; gf=[]; ga=[]; shapes=[]
    for g in fixtures:
        fid=s((g.get("fixture") or {}).get("id")); st=fixture_stats(fid, tid, key) if fid else {}
        if st:
            if st.get("possession"): poss.append(st["possession"])
            if st.get("shots"): shots.append(st["shots"])
            if st.get("sot"): sot.append(st["sot"])
            if st.get("corners"): corners.append(st["corners"])
            if st.get("fouls"): fouls.append(st["fouls"])
            if st.get("yellows"): yellows.append(st["yellows"])
        goals=g.get("goals") or {}; home_team=(g.get("teams") or {}).get("home") or {}; away_team=(g.get("teams") or {}).get("away") or {}; hg=goals.get("home"); ag=goals.get("away")
        if hg is not None and ag is not None:
            if s(home_team.get("id"))==tid: gf.append(float(hg)); ga.append(float(ag))
            elif s(away_team.get("id"))==tid: gf.append(float(ag)); ga.append(float(hg))
    file_slug=slug(s((teams.get('home') or {}).get('name'))+"_vs_"+s((teams.get('away') or {}).get('name')))
    xi_rows=read_csv(BASE/"today"/day/f"vsigma_adhoc_probable_xi_{file_slug}.csv")
    cur_shape=next((r.get("formation","") for r in xi_rows if clean(r.get("team_side"))==side),"")
    usual=cur_shape or (max(set(shapes), key=shapes.count) if shapes else "UNKNOWN")
    avp,avs,avsot,avc,avf,avy,avgf,avga = avg(poss),avg(shots),avg(sot),avg(corners),avg(fouls),avg(yellows),avg(gf),avg(ga)
    tempo="HIGH" if avs>=14 or avc>=6 else ("LOW" if avs<=9 and avp<=47 else "MEDIUM")
    attack="VOLUME_ATTACK" if avs>=13 else ("LOW_VOLUME" if avs<=9 else "CONTROL_ATTACK")
    defense="COMPACT_LOW_BLOCK" if usual.startswith("5-") or avp<45 else ("FRONT_FOOT_DEFENSE" if avp>=55 else "MID_BLOCK")
    spw="HIGH" if avc>=5.5 or usual.startswith("5-") else "MEDIUM"
    trw="HIGH" if avp<45 and avs>=9 else ("LOW" if avp>=58 else "MEDIUM")
    confidence="MEDIUM" if fixtures else "LOW"
    return {"target_date":day,"generated_at":now,"fixture_id":s((fx.get("fixture") or {}).get("id")),"team_side":side,"team_id":tid,"team_name":name,"style_source":"API_RECENT_FIXTURE_STATS","matches_sample":len(fixtures),"avg_possession":avp,"avg_shots":avs,"avg_sot":avsot,"avg_corners":avc,"avg_fouls":avf,"avg_yellows":avy,"avg_goals_for":avgf,"avg_goals_against":avga,"usual_shape":usual,"tempo_label":tempo,"attack_style":attack,"defense_style":defense,"set_piece_weight":spw,"transition_weight":trw,"style_confidence":confidence,"note":"Recent API fixture statistics when available; current XI shape preferred for tactical style.","auto_apply":"NO","production_change":"NO"}
def position_from_api(pos):
    p=s(pos).upper()
    if p in {"G","GK"}: return "G"
    if p in {"D","DF"}: return "D"
    if p in {"M","MF"}: return "M"
    if p in {"F","FW","A"}: return "F"
    return "M"
def parse_grid(grid):
    try:
        a,b=s(grid).split(":"); return int(a), int(b)
    except Exception: return 0,0
def formation_lines(form):
    out=[]
    for x in s(form).split("-"):
        try: out.append(int(x))
        except Exception: pass
    return out
def tactical_role(pos, grid, formation):
    p=position_from_api(pos); row,col=parse_grid(grid); lines=formation_lines(formation)
    if p=="G" or row==1: return "GOALKEEPER"
    if p=="D":
        defenders=lines[0] if lines else 4
        if defenders>=5: return "WING_BACK" if col in {1,defenders} else "CENTER_BACK"
        if defenders==4: return "FULL_BACK" if col in {1,4} else "CENTER_BACK"
        return "CENTER_BACK"
    if p=="M":
        if len(lines)>=4 and row==3 and lines[1] <= 2: return "DEFENSIVE_MIDFIELD"
        if len(lines)>=4 and row==4:
            line_count=lines[2] if len(lines)>2 else 3
            return "WIDE_MIDFIELD" if col in {1,line_count} and line_count>=4 else "INTERIOR"
        if len(lines)==3 and row==3:
            line_count=lines[1] if len(lines)>1 else 3
            return "WIDE_MIDFIELD" if col in {1,line_count} and line_count>=4 else "CENTRAL_MIDFIELD"
        return "CENTRAL_MIDFIELD"
    if p=="F":
        forwards=lines[-1] if lines else 1
        if forwards==1: return "STRIKER"
        if forwards==2: return "STRIKER_PAIR"
        if forwards>=3: return "WINGER" if col in {1,forwards} else "STRIKER"
        return "STRIKER"
def api_lineup_role_lookup(fx, key):
    fid=s((fx.get("fixture") or {}).get("id"))
    try: lineups=call("fixtures/lineups", {"fixture": fid}, key).get("response") or []
    except Exception: lineups=[]
    lookup=defaultdict(dict)
    teams=fx.get("teams") or {}; home_id=s((teams.get("home") or {}).get("id")); away_id=s((teams.get("away") or {}).get("id"))
    for lu in lineups:
        team=lu.get("team") or {}; tid=s(team.get("id")); side="home" if tid==home_id else ("away" if tid==away_id else clean(team.get("name")))
        formation=s(lu.get("formation"))
        for x in lu.get("startXI") or []:
            p=x.get("player") or {}; name=s(p.get("name"));
            if not name: continue
            api_pos=s(p.get("pos")); grid=s(p.get("grid")); role=tactical_role(api_pos,grid,formation)
            lookup[side][clean(name)]={"player_id":s(p.get("id")),"api_position":api_pos,"grid":grid,"position":position_from_api(api_pos),"tactical_role":role,"formation":formation,"source":"API_OFFICIAL_LINEUPS_GRID"}
    return lookup
def fallback_role_from_order(i, formation):
    lines=formation_lines(formation)
    if not lines: return "M","CENTRAL_MIDFIELD"
    if i==1: return "G","GOALKEEPER"
    defenders=lines[0]
    if 2 <= i <= 1+defenders:
        col=i-1
        role="WING_BACK" if defenders>=5 and col in {1,defenders} else ("FULL_BACK" if defenders==4 and col in {1,4} else "CENTER_BACK")
        return "D",role
    mids=sum(lines[1:-1]) if len(lines)>2 else (lines[1] if len(lines)>1 else 3)
    mid_start=2+defenders
    if mid_start <= i < mid_start+mids:
        return "M","CENTRAL_MIDFIELD"
    return "F","STRIKER_PAIR" if lines[-1]==2 else "STRIKER"
def impact_score(pos, role, team_style, name):
    base=POS_BASE.get(pos,65); attack=POS_ATTACK.get(pos,45); defense=POS_DEFENSE.get(pos,45); control=POS_CONTROL.get(pos,45); setp=POS_SETPIECE.get(pos,35)
    mods=ROLE_MODS.get(role,{})
    attack += mods.get("atk",0); defense += mods.get("def",0); control += mods.get("ctl",0); setp += mods.get("sp",0)
    if team_style.get("attack_style") == "VOLUME_ATTACK": attack += 4
    if team_style.get("defense_style") == "COMPACT_LOW_BLOCK": defense += 4
    if team_style.get("tempo_label") == "HIGH": attack += 2; control -= 1
    if team_style.get("usual_shape","").startswith("5-") and role in {"CENTER_BACK","WING_BACK"}: defense += 4; setp += 2
    if team_style.get("usual_shape","").startswith("4-1-4-1") and role in {"DEFENSIVE_MIDFIELD","INTERIOR","CENTRAL_MIDFIELD"}: control += 5
    full=clean(name)
    if any(x in full for x in ["jimenez","foster","rayners"]): attack += 5
    if any(x in full for x in ["mokoena","fidalgo","alvarez"]): control += 5; setp += 3
    if any(x in full for x in ["montes","vasquez","sibisi","mbokazi"]): defense += 4; setp += 2
    if pos=="G": score=base*0.42+defense*0.48+control*0.10
    elif role in {"CENTER_BACK","FULL_BACK","WING_BACK"}: score=base*0.32+defense*0.38+control*0.13+attack*0.07+setp*0.10
    elif role in {"DEFENSIVE_MIDFIELD","CENTRAL_MIDFIELD","INTERIOR","WIDE_MIDFIELD","ATTACKING_MIDFIELD"}: score=base*0.28+control*0.34+attack*0.20+defense*0.12+setp*0.06
    else: score=base*0.33+attack*0.43+control*0.10+setp*0.10+defense*0.04
    return round(clamp(score,45,92),1), round(clamp(attack,0,100),1), round(clamp(defense,0,100),1), round(clamp(control,0,100),1), round(clamp(setp,0,100),1)
def role_label(pos, role, attack, defense, control):
    if role=="GOALKEEPER": return "GOALKEEPER_STABILITY"
    if role=="CENTER_BACK": return "CENTER_BACK_ANCHOR"
    if role=="FULL_BACK": return "FULL_BACK_WIDTH"
    if role=="WING_BACK": return "WING_BACK_TWO_WAY"
    if role=="DEFENSIVE_MIDFIELD": return "PIVOT_SCREEN"
    if role in {"CENTRAL_MIDFIELD","INTERIOR"}: return "CONTROL_HUB" if control>=70 else "MIDFIELD_CONNECTOR"
    if role in {"WIDE_MIDFIELD","WINGER"}: return "WIDE_THREAT" if attack>=70 else "WIDE_BALANCE"
    if role=="ATTACKING_MIDFIELD": return "BETWEEN_LINES_CREATOR"
    if role in {"STRIKER","STRIKER_PAIR"}: return "PRIMARY_ATTACK_THREAT" if attack>=72 else "BOX_THREAT"
    return "STRUCTURE_PLAYER"
def player_rows(day, now, fx, styles, key):
    teams=fx.get("teams") or {}; file_slug=slug(s((teams.get('home') or {}).get('name'))+"_vs_"+s((teams.get('away') or {}).get('name')))
    xi_rows=read_csv(BASE/"today"/day/f"vsigma_adhoc_probable_xi_{file_slug}.csv")
    role_lookup=api_lineup_role_lookup(fx,key)
    rows=[]; style_by_side={r["team_side"]:r for r in styles}
    for xr in xi_rows:
        side=clean(xr.get("team_side")); style=style_by_side.get(side,{})
        formation=s(xr.get("formation"))
        for i in range(1,12):
            name=s(xr.get(f"player_{i}"));
            if not name: continue
            meta=role_lookup.get(side,{}).get(clean(name),{})
            if meta:
                pos=meta["position"]; role=meta["tactical_role"]; api_pos=meta["api_position"]; grid=meta["grid"]; player_id=meta["player_id"]; source="OFFICIAL_GRID_ROLE"
            else:
                pos,role=fallback_role_from_order(i,formation); api_pos=""; grid=""; player_id=""; source="ORDER_FORMATION_FALLBACK"
            score,atk,dfn,ctl,setp=impact_score(pos,role,style,name)
            rows.append({"target_date":day,"generated_at":now,"fixture_id":xr.get("fixture_id",""),"team_side":side,"team_id":xr.get("team_id",""),"team_name":xr.get("team_name",""),"player_id":player_id,"player_name":name,"position":pos,"api_position":api_pos,"grid":grid,"tactical_role":role,"formation":formation,"player_impact_score":score,"attack_impact":atk,"defense_impact":dfn,"control_impact":ctl,"set_piece_impact":setp,"role_label":role_label(pos,role,atk,dfn,ctl),"source_quality":xr.get("xi_status","") + "/" + source,"note":"Functional vSIGMA score from real API position/grid when available, tactical role, team style and light role heuristics; not market value.","auto_apply":"NO","production_change":"NO"})
    return rows
def md(day, summary, styles, players):
    out=[f"# vSIGMA Ad Hoc Team Style + Player Impact - {day}","","## Summary",f"- fixture_found: {summary['fixture_found']}",f"- team_rows: {summary['team_rows']}",f"- player_rows: {summary['player_rows']}",f"- home_xi_strength: {summary['home_xi_strength']}",f"- away_xi_strength: {summary['away_xi_strength']}",f"- xi_edge: {summary['xi_edge']}","- auto_apply: NO","- production_change: NO","","## Team Style"]
    if not styles: out.append("- none. Fixture not found or no API data.")
    for r in styles:
        out += [f"### {r['team_name']} ({r['team_side']})",f"- shape: {r['usual_shape']}",f"- sample: {r['matches_sample']}",f"- avg_possession: {r['avg_possession']}%",f"- avg_shots: {r['avg_shots']} | avg_sot: {r['avg_sot']} | avg_corners: {r['avg_corners']}",f"- avg_fouls: {r['avg_fouls']} | avg_yellows: {r['avg_yellows']}",f"- goals_for/against: {r['avg_goals_for']} / {r['avg_goals_against']}",f"- tempo: {r['tempo_label']}",f"- attack_style: {r['attack_style']}",f"- defense_style: {r['defense_style']}",f"- set_piece_weight: {r['set_piece_weight']} | transition_weight: {r['transition_weight']}",""]
    out += ["## Player Impact Scores"]
    by=defaultdict(list)
    for p in players: by[p["team_side"]].append(p)
    for side in ["home","away"]:
        ps=sorted(by.get(side,[]), key=lambda x: float(x["player_impact_score"]), reverse=True)
        if not ps: continue
        out.append(f"### {ps[0]['team_name']} ({side})")
        for p in ps:
            out.append(f"- {p['player_name']} | pos={p['position']} | role={p['tactical_role']} | api_pos={p['api_position']} | grid={p['grid']} | score={p['player_impact_score']} | atk={p['attack_impact']} def={p['defense_impact']} ctl={p['control_impact']} sp={p['set_piece_impact']} | label={p['role_label']}")
        out.append("")
    out += ["## Interpretation", "- Player scores are functional match-impact ratings, not market values.", "- Role resolution uses API position + API grid + formation when available; otherwise it falls back to formation/order."]
    return "\n".join(out).rstrip()+"\n"
def run(day,home,away,tz,base):
    global BASE; BASE=base
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); k=api_key(); fx=find_fixture(day,home,away,k) if k else None
    styles=[]; players=[]
    if fx:
        styles=[team_style_row(day,now,fx,"home",k), team_style_row(day,now,fx,"away",k)]
        players=player_rows(day,now,fx,styles,k)
    home_scores=[float(p["player_impact_score"]) for p in players if p["team_side"]=="home"]
    away_scores=[float(p["player_impact_score"]) for p in players if p["team_side"]=="away"]
    h_strength=round(sum(home_scores)/len(home_scores),1) if home_scores else 0.0
    a_strength=round(sum(away_scores)/len(away_scores),1) if away_scores else 0.0
    summary={"target_date":day,"generated_at":now,"query_home":home,"query_away":away,"fixture_found":"YES" if fx else "NO","team_rows":len(styles),"player_rows":len(players),"home_xi_strength":h_strength,"away_xi_strength":a_strength,"xi_edge":round(h_strength-a_strength,1),"style_confidence":"MEDIUM" if styles else "NONE","next_action":"Use for style and player-impact weighting; not market value.","auto_apply":"NO","production_change":"NO"}
    file_slug=slug(home+"_vs_"+away)
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/f"vsigma_adhoc_team_style_{file_slug}.csv",styles,STYLE_FIELDS)
        write_csv(folder/f"vsigma_adhoc_player_impact_{file_slug}.csv",players,PLAYER_FIELDS)
        write_csv(folder/f"vsigma_adhoc_team_style_player_impact_{file_slug}_summary.csv",[summary],SUMMARY_FIELDS)
        (folder/f"vsigma_adhoc_team_style_player_impact_{file_slug}.md").write_text(md(day,summary,styles,players),encoding="utf-8")
    print(f"Team style + player impact built teams={len(styles)} players={len(players)}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date",required=True); ap.add_argument("--home",required=True); ap.add_argument("--away",required=True); ap.add_argument("--timezone",default="Atlantic/Canary"); ap.add_argument("--processed-dir",type=Path,default=BASE); a=ap.parse_args(); run(a.date,a.home,a.away,a.timezone,a.processed_dir)
