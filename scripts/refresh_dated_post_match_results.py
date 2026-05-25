from __future__ import annotations

import argparse
import csv
import os
import time
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

PROCESSED = Path("data/processed")
DIRECT_BASE = "https://v3.football.api-sports.io"
RAPID_BASE = "https://api-football-v1.p.rapidapi.com/v3"
FINAL = {"FT", "AET", "PEN"}
STAT_MAP = {
    "shots on goal": "sot", "shots on target": "sot",
    "total shots": "shots", "corner kicks": "corners", "corners": "corners",
    "yellow cards": "yellow", "red cards": "red", "fouls": "fouls",
    "expected goals": "xg", "goals expected": "xg",
}
REPORT_FIELDS = ["target_date","generated_at","fixture_id","home_team","away_team","status","goals","stats_status","updated_fields","source_guard"]


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def u(v: object) -> str:
    return n(v).upper()


def to_num(v: object) -> float | None:
    if v is None: return None
    s = str(v).strip().replace("%", "")
    if not s or s.lower() == "nan": return None
    try: return float(s)
    except ValueError: return None


def fmt(v: object) -> str:
    x = to_num(v)
    if x is None: return ""
    return str(int(x)) if abs(x - round(x)) < 1e-9 else f"{x:.2f}"


def read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists(): return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rdr = csv.DictReader(f)
        return list(rdr.fieldnames or []), [dict(r) for r in rdr]


def write(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows: w.writerow({k: r.get(k, "") for k in fields})


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def env() -> dict[str, str]:
    return {
        "direct_key": os.getenv("API_FOOTBALL_KEY") or os.getenv("APISPORTS_KEY") or "",
        "rapid_key": os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY") or "",
        "rapid_host": os.getenv("API_FOOTBALL_HOST") or "api-football-v1.p.rapidapi.com",
        "timezone": os.getenv("API_FOOTBALL_TIMEZONE") or "Atlantic/Canary",
    }


def api_get(path: str, params: dict[str, object], cfg: dict[str, str]) -> tuple[dict, str]:
    if cfg["direct_key"]:
        r = requests.get(f"{DIRECT_BASE}{path}", headers={"x-apisports-key": cfg["direct_key"]}, params=params, timeout=30)
        if r.status_code == 200:
            data = r.json()
            if not data.get("errors"):
                return data, "API_SPORTS_DIRECT"
    if cfg["rapid_key"]:
        r = requests.get(f"{RAPID_BASE}{path}", headers={"x-rapidapi-key": cfg["rapid_key"], "x-rapidapi-host": cfg["rapid_host"]}, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get("errors"):
            raise RuntimeError(str(data.get("errors")))
        return data, "RAPIDAPI"
    raise RuntimeError("Missing API_FOOTBALL_KEY/APISPORTS_KEY or RAPIDAPI_KEY")


def fixture_ids(day: str, matches: list[dict[str, str]]) -> set[str]:
    out: set[str] = set()
    for name in ["vsigma_match_stat_forecasts.csv", "vsigma_daily_execution_board.csv", "vsigma_today_execution_bets_only.csv"]:
        _, rows = read(dated(day, name))
        for r in rows:
            fid = n(r.get("fixture_id")).replace(".0", "")
            if fid: out.add(fid)
    if not out:
        for r in matches:
            fid = n(r.get("fixture_id")).replace(".0", "")
            if fid: out.add(fid)
    return out


def fixture_map(day: str, cfg: dict[str, str]) -> tuple[dict[str, dict], str]:
    data, provider = api_get("/fixtures", {"date": day, "timezone": cfg["timezone"]}, cfg)
    mp = {}
    for item in data.get("response", []) or []:
        fid = str(((item.get("fixture") or {}).get("id")))
        if fid and fid != "None": mp[fid] = item
    return mp, provider


def stat_map(fid: str, cfg: dict[str, str]) -> dict[str, dict[str, float]]:
    data, _ = api_get("/fixtures/statistics", {"fixture": fid}, cfg)
    out = {"home": {}, "away": {}}
    for idx, team_stats in enumerate(data.get("response", []) or []):
        side = "home" if idx == 0 else "away"
        for st in team_stats.get("statistics", []) or []:
            key = STAT_MAP.get(str(st.get("type") or "").strip().lower())
            val = to_num(st.get("value"))
            if key and val is not None:
                out[side][key] = val
    for side in ("home", "away"):
        y = out[side].get("yellow") or 0
        r = out[side].get("red") or 0
        if y or r: out[side]["cards"] = y + r
    return out


def add_cols(fields: list[str]) -> list[str]:
    needed = ["fixture_status_short","fixture_status_long","fixture_status_elapsed","goals_home","goals_away","score_fulltime_home","score_fulltime_away","results_last_refresh_at"]
    for metric in ["sot","shots","corners","cards","fouls","xg"]:
        needed += [f"actual_home_{metric}", f"actual_away_{metric}", f"actual_total_{metric}"]
    for col in needed:
        if col not in fields: fields.append(col)
    return fields


def update_match(row: dict[str, str], item: dict, stats: dict[str, dict[str, float]] | None, now: str) -> tuple[dict[str, str], list[str]]:
    changed = []
    fx, goals, score = item.get("fixture", {}) or {}, item.get("goals", {}) or {}, item.get("score", {}) or {}
    st = fx.get("status", {}) or {}; ft = score.get("fulltime", {}) or {}
    vals = {
        "fixture_status_short": st.get("short"), "fixture_status_long": st.get("long"), "fixture_status_elapsed": st.get("elapsed"),
        "goals_home": goals.get("home"), "goals_away": goals.get("away"),
        "score_fulltime_home": ft.get("home"), "score_fulltime_away": ft.get("away"),
        "results_last_refresh_at": now,
    }
    for k, v in vals.items():
        if v is not None:
            row[k] = fmt(v) if k not in {"fixture_status_short","fixture_status_long","results_last_refresh_at"} else str(v)
            changed.append(k)
    if stats:
        for metric in ["sot","shots","corners","cards","fouls","xg"]:
            hv, av = stats.get("home", {}).get(metric), stats.get("away", {}).get(metric)
            if hv is not None and av is not None:
                row[f"actual_home_{metric}"] = fmt(hv); row[f"actual_away_{metric}"] = fmt(av); row[f"actual_total_{metric}"] = fmt(hv + av)
                changed += [f"actual_home_{metric}", f"actual_away_{metric}", f"actual_total_{metric}"]
    return row, changed


def md(day: str, report: list[dict[str, object]]) -> str:
    c = Counter(str(r.get("status") or "UNKNOWN") for r in report)
    lines = [f"# vSIGMA Dated Post-Match Results Refresh - {day}", "", "## Summary", f"- rows_reported: {len(report)}", f"- status_counts: {'; '.join(f'{k}={v}' for k,v in c.items()) if c else 'none'}", "- source_guard: DATED_INPUT_ONLY", "- auto_apply: NO", "- production_change: NO", "", "## Rows"]
    if not report: lines.append("- none")
    for r in report:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | status={r['status']} | goals={r['goals']} | stats={r['stats_status']} | fields={r['updated_fields']}")
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    fields, rows = read(dated(day, "matches.csv"))
    if not rows: raise FileNotFoundError(f"Missing dated matches.csv for {day}")
    fields = add_cols(fields)
    cfg = env(); fmap, provider = fixture_map(day, cfg)
    targets = fixture_ids(day, rows); now = datetime.now(timezone.utc).isoformat()
    report = []
    for row in rows:
        fid = n(row.get("fixture_id")).replace(".0", "")
        if fid not in targets or fid not in fmap: continue
        item = fmap[fid]; st = u(((item.get("fixture") or {}).get("status") or {}).get("short"))
        stats = None; stats_status = "NOT_FINAL"
        if st in FINAL:
            try:
                stats = stat_map(fid, cfg); stats_status = "STATS_FETCHED"
                time.sleep(0.25)
            except Exception as e:
                stats_status = f"STATS_ERROR:{str(e)[:80]}"
        row, changed = update_match(row, item, stats, now)
        teams = item.get("teams", {}) or {}; goals = item.get("goals", {}) or {}
        report.append({"target_date": day,"generated_at": datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"),"fixture_id": fid,"home_team": n(row.get("home_team") or ((teams.get("home") or {}).get("name"))),"away_team": n(row.get("away_team") or ((teams.get("away") or {}).get("name"))),"status": st,"goals": f"{goals.get('home')}-{goals.get('away')}","stats_status": stats_status,"updated_fields": ";".join(changed),"source_guard":"DATED_INPUT_ONLY"})
    write(dated(day, "matches.csv"), fields, rows)
    for out in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write(out / "vsigma_dated_post_match_results_refresh.csv", REPORT_FIELDS, report)
        (out / "vsigma_dated_post_match_results_refresh.md").write_text(md(day, report), encoding="utf-8")
    print("=== VSIGMA DATED POST-MATCH RESULTS REFRESH ===")
    print(f"provider={provider}")
    print(f"rows_reported={len(report)}")


def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--date", required=True); p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args(); run(a.date, a.timezone)

if __name__ == "__main__": main()
