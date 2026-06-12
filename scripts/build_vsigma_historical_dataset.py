from __future__ import annotations

import argparse
import csv
import json
import os
import time
import unicodedata
import re
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = Path("data/modeling")
FINAL_STATUS = {"FT", "AET", "PEN"}
STAT_ALIASES = {
    "shots": {"total shots"},
    "sot": {"shots on goal"},
    "corners": {"corner kicks"},
    "possession": {"ball possession"},
    "fouls": {"fouls"},
    "yellows": {"yellow cards"},
    "xg": {"expected goals", "expected_goals", "xg"},
}


def clean(v: object) -> str:
    t = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def fnum(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).replace("%", "").strip())
    except Exception:
        return default


def api_key() -> str:
    for key in ["APISPORTS_KEY", "API_SPORTS_KEY", "API_FOOTBALL_KEY", "APIFOOTBALL_KEY", "API_FOOTBALL_API_KEY", "RAPIDAPI_KEY", "X_RAPIDAPI_KEY"]:
        value = os.getenv(key)
        if value:
            return value
    return ""


def call(path: str, params: dict[str, object], key: str) -> dict:
    url = "https://v3.football.api-sports.io/" + path + "?" + urlencode(params)
    req = Request(url, headers={"x-apisports-key": key})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def stat_value(stats: list[dict], aliases: set[str]) -> float | None:
    aliases = {clean(a) for a in aliases}
    for item in stats or []:
        if clean(item.get("type")) in aliases:
            value = item.get("value")
            if value is None or str(value).strip() == "":
                return None
            return fnum(value)
    return None


def fixture_stats(fixture_id: str, key: str, sleep_s: float) -> dict[str, dict[str, float | None]]:
    try:
        response = call("fixtures/statistics", {"fixture": fixture_id}, key).get("response") or []
        if sleep_s:
            time.sleep(sleep_s)
    except Exception:
        return {}
    out: dict[str, dict[str, float | None]] = {}
    for team_block in response:
        team = team_block.get("team") or {}
        tid = str(team.get("id") or "")
        stats = team_block.get("statistics") or []
        out[tid] = {name: stat_value(stats, aliases) for name, aliases in STAT_ALIASES.items()}
    return out


def implied_from_odds(fixture_id: str, key: str, sleep_s: float) -> tuple[float, float, float] | None:
    try:
        response = call("odds", {"fixture": fixture_id}, key).get("response") or []
        if sleep_s:
            time.sleep(sleep_s)
    except Exception:
        return None
    odds: list[tuple[float, float, float]] = []
    for item in response:
        for bookmaker in item.get("bookmakers") or []:
            for bet in bookmaker.get("bets") or []:
                name = clean(bet.get("name"))
                if name not in {"match winner", "1x2", "fulltime result"}:
                    continue
                values = {clean(v.get("value")): v.get("odd") for v in bet.get("values") or []}
                h = fnum(values.get("home") or values.get("1"), 0.0)
                d = fnum(values.get("draw") or values.get("x"), 0.0)
                a = fnum(values.get("away") or values.get("2"), 0.0)
                if h > 1 and d > 1 and a > 1:
                    odds.append((h, d, a))
    if not odds:
        return None
    ih = sum(1 / h for h, _, _ in odds) / len(odds)
    idr = sum(1 / d for _, d, _ in odds) / len(odds)
    ia = sum(1 / a for _, _, a in odds) / len(odds)
    total = ih + idr + ia
    return round(ih / total, 5), round(idr / total, 5), round(ia / total, 5)


def result_class(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "HOME"
    if away_goals > home_goals:
        return "AWAY"
    return "DRAW"


def avg(values: list[float]) -> float:
    vals = [v for v in values if v is not None]
    return round(sum(vals) / len(vals), 4) if vals else 0.0


def rolling_features(history: deque[dict], prefix: str, window: int) -> dict[str, float]:
    recent = list(history)[-window:]
    return {
        f"feat_{prefix}_last{window}_games": float(len(recent)),
        f"feat_{prefix}_last{window}_gf": avg([x["gf"] for x in recent]),
        f"feat_{prefix}_last{window}_ga": avg([x["ga"] for x in recent]),
        f"feat_{prefix}_last{window}_points": avg([x["points"] for x in recent]),
        f"feat_{prefix}_last{window}_shots_for": avg([x.get("shots_for", 0.0) for x in recent]),
        f"feat_{prefix}_last{window}_shots_against": avg([x.get("shots_against", 0.0) for x in recent]),
        f"feat_{prefix}_last{window}_sot_for": avg([x.get("sot_for", 0.0) for x in recent]),
        f"feat_{prefix}_last{window}_sot_against": avg([x.get("sot_against", 0.0) for x in recent]),
        f"feat_{prefix}_last{window}_corners_for": avg([x.get("corners_for", 0.0) for x in recent]),
        f"feat_{prefix}_last{window}_corners_against": avg([x.get("corners_against", 0.0) for x in recent]),
        f"feat_{prefix}_last{window}_possession": avg([x.get("possession", 0.0) for x in recent]),
    }


def update_history(history: dict[str, deque], home_id: str, away_id: str, hg: int, ag: int, h_stats: dict, a_stats: dict, window_cap: int) -> None:
    hp = 3 if hg > ag else (1 if hg == ag else 0)
    ap = 3 if ag > hg else (1 if hg == ag else 0)
    history[home_id].append({
        "gf": float(hg), "ga": float(ag), "points": float(hp),
        "shots_for": fnum(h_stats.get("shots")), "shots_against": fnum(a_stats.get("shots")),
        "sot_for": fnum(h_stats.get("sot")), "sot_against": fnum(a_stats.get("sot")),
        "corners_for": fnum(h_stats.get("corners")), "corners_against": fnum(a_stats.get("corners")),
        "possession": fnum(h_stats.get("possession")),
    })
    history[away_id].append({
        "gf": float(ag), "ga": float(hg), "points": float(ap),
        "shots_for": fnum(a_stats.get("shots")), "shots_against": fnum(h_stats.get("shots")),
        "sot_for": fnum(a_stats.get("sot")), "sot_against": fnum(h_stats.get("sot")),
        "corners_for": fnum(a_stats.get("corners")), "corners_against": fnum(h_stats.get("corners")),
        "possession": fnum(a_stats.get("possession")),
    })
    while len(history[home_id]) > window_cap:
        history[home_id].popleft()
    while len(history[away_id]) > window_cap:
        history[away_id].popleft()


def build(league_seasons: list[str], out_path: Path, window: int, max_fixtures: int, include_odds: bool, sleep_s: float) -> None:
    key = api_key()
    if not key:
        raise RuntimeError("No API key found in environment")
    rows: list[dict[str, object]] = []
    coverage = {"fixtures": 0, "with_stats": 0, "with_odds": 0}
    for item in league_seasons:
        league_id, season = item.split(":", 1)
        fixtures = call("fixtures", {"league": league_id, "season": season}, key).get("response") or []
        if sleep_s:
            time.sleep(sleep_s)
        fixtures = [fx for fx in fixtures if (((fx.get("fixture") or {}).get("status") or {}).get("short") in FINAL_STATUS)]
        fixtures.sort(key=lambda fx: ((fx.get("fixture") or {}).get("date") or ""))
        history: dict[str, deque] = defaultdict(deque)
        for fx in fixtures:
            if max_fixtures and len(rows) >= max_fixtures:
                break
            fixture = fx.get("fixture") or {}
            teams = fx.get("teams") or {}
            league = fx.get("league") or {}
            goals = fx.get("goals") or {}
            fid = str(fixture.get("id") or "")
            home = teams.get("home") or {}
            away = teams.get("away") or {}
            home_id = str(home.get("id") or "")
            away_id = str(away.get("id") or "")
            if not fid or not home_id or not away_id or goals.get("home") is None or goals.get("away") is None:
                continue
            hg, ag = int(goals["home"]), int(goals["away"])
            stats = fixture_stats(fid, key, sleep_s)
            h_stats = stats.get(home_id, {})
            a_stats = stats.get(away_id, {})
            if h_stats or a_stats:
                coverage["with_stats"] += 1
            odds = implied_from_odds(fid, key, sleep_s) if include_odds else None
            if odds:
                coverage["with_odds"] += 1
            if not odds:
                odds = (0.50, 0.29, 0.21)
            row = {
                "fixture_id": fid,
                "fixture_date": fixture.get("date", ""),
                "league_id": league_id,
                "league_name": league.get("name", ""),
                "country": league.get("country", ""),
                "season": season,
                "home_team_id": home_id,
                "away_team_id": away_id,
                "home_team": home.get("name", ""),
                "away_team": away.get("name", ""),
                "target_home_goals": hg,
                "target_away_goals": ag,
                "target_total_goals": hg + ag,
                "target_result_class": result_class(hg, ag),
                "target_btts": int(hg > 0 and ag > 0),
                "target_over25": int(hg + ag >= 3),
                "target_under35": int(hg + ag <= 3),
                "target_home_shots": fnum(h_stats.get("shots")),
                "target_away_shots": fnum(a_stats.get("shots")),
                "target_home_sot": fnum(h_stats.get("sot")),
                "target_away_sot": fnum(a_stats.get("sot")),
                "target_home_corners": fnum(h_stats.get("corners")),
                "target_away_corners": fnum(a_stats.get("corners")),
                "target_home_possession": fnum(h_stats.get("possession")),
                "target_away_possession": fnum(a_stats.get("possession")),
                "feat_market_home_prob": odds[0],
                "feat_market_draw_prob": odds[1],
                "feat_market_away_prob": odds[2],
                "feat_home_advantage": 1.0,
            }
            row.update(rolling_features(history[home_id], "home", window))
            row.update(rolling_features(history[away_id], "away", window))
            rows.append(row)
            update_history(history, home_id, away_id, hg, ag, h_stats, a_stats, max(window, 10))
            coverage["fixtures"] += 1
        if max_fixtures and len(rows) >= max_fixtures:
            break
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        fields = sorted({k for row in rows for k in row.keys()})
        core = ["fixture_id", "fixture_date", "league_id", "season", "home_team", "away_team", "target_home_goals", "target_away_goals", "target_result_class"]
        fields = core + [f for f in fields if f not in core]
        with out_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    summary_path = out_path.with_name(out_path.stem + "_summary.json")
    summary_path.write_text(json.dumps({"rows": len(rows), "coverage": coverage, "league_seasons": league_seasons}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Historical dataset rows={len(rows)} path={out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--league-season", action="append", required=True, help="Format: league_id:season, example 39:2025")
    parser.add_argument("--out", type=Path, default=BASE / "vsigma_historical_dataset.csv")
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--max-fixtures", type=int, default=0)
    parser.add_argument("--include-odds", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.15)
    args = parser.parse_args()
    build(args.league_season, args.out, args.window, args.max_fixtures, args.include_odds, args.sleep)
