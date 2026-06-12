from __future__ import annotations

import argparse
import csv
import json
import os
import re
import unicodedata
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = Path("data/modeling")
FINAL_STATUS = {"FT", "AET", "PEN"}
ROLLING_N = 8
FIELDS = [
    "fixture_id","date","season","league_id","league_name","country","home_team_id","away_team_id","home_team","away_team",
    "home_goals","away_goals","result_class","total_goals","btts","over15","over25","under35",
    "home_recent_matches","away_recent_matches",
    "home_gf_avg","home_ga_avg","away_gf_avg","away_ga_avg",
    "home_shots_for_avg","home_shots_against_avg","away_shots_for_avg","away_shots_against_avg",
    "home_sot_for_avg","home_sot_against_avg","away_sot_for_avg","away_sot_against_avg",
    "home_corners_for_avg","home_corners_against_avg","away_corners_for_avg","away_corners_against_avg",
    "home_possession_avg","away_possession_avg","home_yellows_avg","away_yellows_avg",
    "home_actual_shots","away_actual_shots","home_actual_sot","away_actual_sot","home_actual_corners","away_actual_corners","home_actual_possession","away_actual_possession","home_actual_yellows","away_actual_yellows",
]

def s(v) -> str:
    return "" if v is None else str(v).strip()

def clean(v) -> str:
    text = unicodedata.normalize("NFKD", s(v)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()

def api_key() -> str:
    for key in ["APISPORTS_KEY","API_SPORTS_KEY","API_FOOTBALL_KEY","APIFOOTBALL_KEY","API_FOOTBALL_API_KEY","RAPIDAPI_KEY","X_RAPIDAPI_KEY"]:
        if os.getenv(key):
            return os.getenv(key, "")
    return ""

def call(path: str, params: dict, key: str) -> dict:
    url = "https://v3.football.api-sports.io/" + path + "?" + urlencode(params)
    req = Request(url, headers={"x-apisports-key": key})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fnum(v, default=0.0) -> float:
    try:
        return float(s(v).replace("%", ""))
    except Exception:
        return default

def avg(values: list[float]) -> float:
    vals = [float(v) for v in values if v is not None]
    return round(sum(vals) / len(vals), 3) if vals else 0.0

def stat_value(stats: list[dict], aliases: set[str]) -> float:
    aliases = {clean(a) for a in aliases}
    for item in stats or []:
        if clean(item.get("type")) in aliases:
            return fnum(item.get("value"))
    return 0.0

def fixture_stats(fixture_id: str, team_id: str, key: str) -> dict[str, float]:
    try:
        resp = call("fixtures/statistics", {"fixture": fixture_id, "team": team_id}, key).get("response") or []
    except Exception:
        return {}
    if not resp:
        return {}
    st = resp[0].get("statistics") or []
    return {
        "shots": stat_value(st, {"Total Shots"}),
        "sot": stat_value(st, {"Shots on Goal"}),
        "corners": stat_value(st, {"Corner Kicks"}),
        "possession": stat_value(st, {"Ball Possession"}),
        "yellows": stat_value(st, {"Yellow Cards"}),
    }

def result_class(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "H"
    if away_goals > home_goals:
        return "A"
    return "D"

def snapshot(team_state: dict[str, deque]) -> dict[str, float]:
    return {
        "matches": len(team_state["gf"]),
        "gf_avg": avg(list(team_state["gf"])),
        "ga_avg": avg(list(team_state["ga"])),
        "shots_for_avg": avg(list(team_state["shots_for"])),
        "shots_against_avg": avg(list(team_state["shots_against"])),
        "sot_for_avg": avg(list(team_state["sot_for"])),
        "sot_against_avg": avg(list(team_state["sot_against"])),
        "corners_for_avg": avg(list(team_state["corners_for"])),
        "corners_against_avg": avg(list(team_state["corners_against"])),
        "possession_avg": avg(list(team_state["possession"])),
        "yellows_avg": avg(list(team_state["yellows"])),
    }

def update_team(team_state: dict[str, deque], gf: int, ga: int, stats_for: dict, stats_against: dict) -> None:
    team_state["gf"].append(float(gf))
    team_state["ga"].append(float(ga))
    team_state["shots_for"].append(fnum(stats_for.get("shots")))
    team_state["shots_against"].append(fnum(stats_against.get("shots")))
    team_state["sot_for"].append(fnum(stats_for.get("sot")))
    team_state["sot_against"].append(fnum(stats_against.get("sot")))
    team_state["corners_for"].append(fnum(stats_for.get("corners")))
    team_state["corners_against"].append(fnum(stats_against.get("corners")))
    team_state["possession"].append(fnum(stats_for.get("possession")))
    team_state["yellows"].append(fnum(stats_for.get("yellows")))

def new_team_state() -> dict[str, deque]:
    keys = ["gf","ga","shots_for","shots_against","sot_for","sot_against","corners_for","corners_against","possession","yellows"]
    return {key: deque(maxlen=ROLLING_N) for key in keys}

def build_dataset(league_id: int, season: int, max_fixtures: int, key: str) -> list[dict]:
    params = {"league": league_id, "season": season}
    fixtures = call("fixtures", params, key).get("response") or []
    finished = [fx for fx in fixtures if s(((fx.get("fixture") or {}).get("status") or {}).get("short")) in FINAL_STATUS]
    finished.sort(key=lambda x: s((x.get("fixture") or {}).get("date")))
    if max_fixtures > 0:
        finished = finished[-max_fixtures:]
    states = defaultdict(new_team_state)
    rows: list[dict] = []
    for fx in finished:
        f = fx.get("fixture") or {}
        teams = fx.get("teams") or {}
        goals = fx.get("goals") or {}
        league = fx.get("league") or {}
        fid = s(f.get("id"))
        home = teams.get("home") or {}
        away = teams.get("away") or {}
        hid = s(home.get("id")); aid = s(away.get("id"))
        if not fid or not hid or not aid or goals.get("home") is None or goals.get("away") is None:
            continue
        hg = int(goals.get("home")); ag = int(goals.get("away"))
        h_pre = snapshot(states[hid]); a_pre = snapshot(states[aid])
        h_stats = fixture_stats(fid, hid, key)
        a_stats = fixture_stats(fid, aid, key)
        row = {
            "fixture_id": fid,
            "date": s(f.get("date")),
            "season": season,
            "league_id": league_id,
            "league_name": s(league.get("name")),
            "country": s(league.get("country")),
            "home_team_id": hid,
            "away_team_id": aid,
            "home_team": s(home.get("name")),
            "away_team": s(away.get("name")),
            "home_goals": hg,
            "away_goals": ag,
            "result_class": result_class(hg, ag),
            "total_goals": hg + ag,
            "btts": int(hg > 0 and ag > 0),
            "over15": int(hg + ag >= 2),
            "over25": int(hg + ag >= 3),
            "under35": int(hg + ag <= 3),
            "home_recent_matches": h_pre["matches"],
            "away_recent_matches": a_pre["matches"],
            "home_gf_avg": h_pre["gf_avg"],
            "home_ga_avg": h_pre["ga_avg"],
            "away_gf_avg": a_pre["gf_avg"],
            "away_ga_avg": a_pre["ga_avg"],
            "home_shots_for_avg": h_pre["shots_for_avg"],
            "home_shots_against_avg": h_pre["shots_against_avg"],
            "away_shots_for_avg": a_pre["shots_for_avg"],
            "away_shots_against_avg": a_pre["shots_against_avg"],
            "home_sot_for_avg": h_pre["sot_for_avg"],
            "home_sot_against_avg": h_pre["sot_against_avg"],
            "away_sot_for_avg": a_pre["sot_for_avg"],
            "away_sot_against_avg": a_pre["sot_against_avg"],
            "home_corners_for_avg": h_pre["corners_for_avg"],
            "home_corners_against_avg": h_pre["corners_against_avg"],
            "away_corners_for_avg": a_pre["corners_for_avg"],
            "away_corners_against_avg": a_pre["corners_against_avg"],
            "home_possession_avg": h_pre["possession_avg"],
            "away_possession_avg": a_pre["possession_avg"],
            "home_yellows_avg": h_pre["yellows_avg"],
            "away_yellows_avg": a_pre["yellows_avg"],
            "home_actual_shots": h_stats.get("shots", 0.0),
            "away_actual_shots": a_stats.get("shots", 0.0),
            "home_actual_sot": h_stats.get("sot", 0.0),
            "away_actual_sot": a_stats.get("sot", 0.0),
            "home_actual_corners": h_stats.get("corners", 0.0),
            "away_actual_corners": a_stats.get("corners", 0.0),
            "home_actual_possession": h_stats.get("possession", 0.0),
            "away_actual_possession": a_stats.get("possession", 0.0),
            "home_actual_yellows": h_stats.get("yellows", 0.0),
            "away_actual_yellows": a_stats.get("yellows", 0.0),
        }
        rows.append(row)
        update_team(states[hid], hg, ag, h_stats, a_stats)
        update_team(states[aid], ag, hg, a_stats, h_stats)
    return rows

def write_dataset(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([{key: row.get(key, "") for key in FIELDS} for row in rows])

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--league-id", type=int, required=True)
    parser.add_argument("--season", type=int, required=True)
    parser.add_argument("--max-fixtures", type=int, default=300)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    key = api_key()
    if not key:
        raise SystemExit("Missing API key env var")
    rows = build_dataset(args.league_id, args.season, args.max_fixtures, key)
    out = args.out or BASE / f"api_historical_features_league_{args.league_id}_{args.season}.csv"
    write_dataset(rows, out)
    print(f"dataset_rows={len(rows)} out={out}")

if __name__ == "__main__":
    main()
