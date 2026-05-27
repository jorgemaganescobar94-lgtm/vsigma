from __future__ import annotations

import argparse
import csv
import os
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path("data/processed")
DIRECT = "https://v3.football.api-sports.io"
RAPID = "https://api-football-v1.p.rapidapi.com/v3"
LIVE = {"1H", "2H", "HT", "ET", "BT", "P", "LIVE"}
FINAL = {"FT", "AET", "PEN"}
CANDIDATE = {"READY_LOW_STAKE_REVIEW", "LIVE_ONLY_WAIT_TRIGGER", "LIVE_RECHECK_ONLY"}
FIELDS = [
    "target_date","generated_at","rank","fixture_id","home_team","away_team","recheck_decision","market",
    "minutes_to_kickoff","window_status","match_status","elapsed","score","total_shots","total_sot",
    "total_corners","home_possession","away_possession","signal_score","live_trigger_decision","reason",
    "source_guard","auto_apply","production_change",
]


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def num(v: object, default: float = 0) -> float:
    s = n(v).replace("%", "")
    if not s or s.lower() == "nan": return default
    try: return float(s)
    except ValueError: return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows: w.writerow({k: r.get(k, "") for k in FIELDS})


def cfg() -> dict[str, str]:
    return {
        "direct": os.getenv("API_FOOTBALL_KEY") or os.getenv("APISPORTS_KEY") or "",
        "rapid": os.getenv("RAPIDAPI_KEY") or os.getenv("X_RAPIDAPI_KEY") or "",
        "host": os.getenv("API_FOOTBALL_HOST") or "api-football-v1.p.rapidapi.com",
    }


def api(path: str, params: dict[str, object], c: dict[str, str]) -> dict:
    if c["direct"]:
        r = requests.get(DIRECT + path, headers={"x-apisports-key": c["direct"]}, params=params, timeout=25)
        r.raise_for_status(); return r.json()
    if c["rapid"]:
        r = requests.get(RAPID + path, headers={"x-rapidapi-key": c["rapid"], "x-rapidapi-host": c["host"]}, params=params, timeout=25)
        r.raise_for_status(); return r.json()
    raise RuntimeError("API_CREDENTIALS_MISSING")


def stat(stats: list[dict], typ: str) -> tuple[float, float, float]:
    vals = []
    for team in stats[:2]:
        found = 0.0
        for item in team.get("statistics", []) or []:
            if n(item.get("type")).lower() == typ.lower():
                found = num(item.get("value")); break
        vals.append(found)
    while len(vals) < 2: vals.append(0.0)
    return vals[0], vals[1], vals[0] + vals[1]


def fixture_state(fid: str, c: dict[str, str]) -> tuple[str, float, str, float, float]:
    data = api("/fixtures", {"id": fid}, c)
    resp = (data.get("response") or [{}])[0]
    fx = resp.get("fixture", {}) or {}; st = fx.get("status", {}) or {}
    goals = resp.get("goals", {}) or {}
    status = n(st.get("short") or "UNKNOWN")
    elapsed = num(st.get("elapsed"), 0)
    hg = num(goals.get("home"), 0); ag = num(goals.get("away"), 0)
    return status, elapsed, f"{int(hg)}-{int(ag)}", hg, ag


def fixture_stats(fid: str, c: dict[str, str]) -> dict[str, float]:
    data = api("/fixtures/statistics", {"fixture": fid}, c)
    resp = data.get("response") or []
    _, _, shots = stat(resp, "Total Shots")
    _, _, sot = stat(resp, "Shots on Goal")
    _, _, corners = stat(resp, "Corner Kicks")
    hp, ap, _ = stat(resp, "Ball Possession")
    return {"shots": shots, "sot": sot, "corners": corners, "hp": hp, "ap": ap}


def window_status(status: str, elapsed: float, minutes_to_kickoff: float | None) -> str:
    if status in FINAL: return "MATCH_FINISHED"
    if status in LIVE:
        return "IN_LIVE_WINDOW" if elapsed <= 25 else "TOO_LATE"
    if minutes_to_kickoff is None: return "MATCH_NOT_LIVE"
    if minutes_to_kickoff > 15: return "TOO_EARLY"
    if minutes_to_kickoff < -25: return "TOO_LATE"
    return "IN_LIVE_WINDOW"


def trigger_decision(status: str, window: str, elapsed: float, goals: float, shots: float, sot: float, corners: float, market: str) -> tuple[int, str, str]:
    if window == "MATCH_FINISHED": return 0, "MATCH_FINISHED", "match already final"
    if window == "TOO_EARLY": return 0, "TOO_EARLY", "outside useful live window"
    if window == "TOO_LATE": return 0, "TOO_LATE", "live window passed"
    if status not in LIVE: return 0, "MATCH_NOT_LIVE", "not live yet"
    score = 0
    if elapsed >= 8: score += 1
    if shots >= 6: score += 1
    if sot >= 2: score += 2
    if corners >= 2: score += 1
    if goals >= 1 and ("OVER_1_5" in market or "BTTS" in market): score += 2
    if elapsed < 8: return score, "WAIT_MORE_MINUTES", "sample too early"
    if elapsed >= 15 and shots <= 4 and sot == 0 and corners <= 1 and goals == 0:
        return score, "LIVE_TRIGGER_REJECTED", "dead low-tempo sample"
    if score >= 4: return score, "LIVE_TRIGGER_CONFIRMED", "tempo and/or score supports trigger"
    if score >= 2: return score, "WAIT_MORE_MINUTES", "partial signal only"
    return score, "LIVE_TRIGGER_REJECTED", "insufficient live signal"


def mtko(row: dict[str, str]) -> float | None:
    raw = n(row.get("minutes_to_kickoff") or row.get("min"))
    if not raw or raw.upper() == "NA": return None
    return num(raw, 0)


def build(day: str, tz: str) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = ROOT / "today" / day
    candidates = [r for r in read_csv(folder / "vsigma_prelock_live_recheck.csv") if n(r.get("recheck_decision")) in CANDIDATE]
    out: list[dict[str, object]] = []
    c = cfg()
    for i, r in enumerate(candidates, 1):
        fid = n(r.get("fixture_id")).replace(".0", "")
        market = n(r.get("primary_market") or r.get("market"))
        minutes = mtko(r)
        base = {"target_date": day, "generated_at": generated, "rank": i, "fixture_id": fid, "home_team": n(r.get("home_team")), "away_team": n(r.get("away_team")), "recheck_decision": n(r.get("recheck_decision")), "market": market, "minutes_to_kickoff": "" if minutes is None else minutes, "source_guard": "DATED_INPUT_ONLY", "auto_apply": "NO", "production_change": "NO"}
        if not fid:
            out.append({**base, "window_status": "UNKNOWN", "live_trigger_decision": "NO_FIXTURE_ID", "reason": "fixture_id missing"}); continue
        try:
            st, elapsed, scoreline, hg, ag = fixture_state(fid, c)
            win = window_status(st, elapsed, minutes)
            stats = fixture_stats(fid, c) if st in LIVE and win == "IN_LIVE_WINDOW" else {"shots": 0, "sot": 0, "corners": 0, "hp": 0, "ap": 0}
            sig, decision, reason = trigger_decision(st, win, elapsed, hg + ag, stats["shots"], stats["sot"], stats["corners"], market)
            out.append({**base, "window_status": win, "match_status": st, "elapsed": elapsed, "score": scoreline, "total_shots": stats["shots"], "total_sot": stats["sot"], "total_corners": stats["corners"], "home_possession": stats["hp"], "away_possession": stats["ap"], "signal_score": sig, "live_trigger_decision": decision, "reason": reason})
        except Exception as e:
            out.append({**base, "window_status": "UNKNOWN", "live_trigger_decision": "LIVE_NO_DATA", "reason": str(e)[:160]})
    return out


def count(rows: list[dict[str, object]], key: str) -> str:
    c = Counter(n(r.get(key)) or "NONE" for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.items()) if c else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [f"# vSIGMA Live Trigger Validator - {day}", "", "## Summary", f"- rows_validated: {len(rows)}", f"- window_counts: {count(rows, 'window_status')}", f"- live_trigger_counts: {count(rows, 'live_trigger_decision')}", "- auto_apply: NO", "- production_change: NO", "", "## Rows"]
    if not rows: lines.append("- none. No live/prelock candidates found.")
    for r in rows:
        lines.append(f"- #{r.get('rank')} | window={r.get('window_status')} | decision={r.get('live_trigger_decision')} | {r.get('home_team')} vs {r.get('away_team')} | market={r.get('market')} | status={r.get('match_status','')} | min={r.get('elapsed','')} | mtko={r.get('minutes_to_kickoff','')} | score={r.get('score','')} | shots={r.get('total_shots','')} | SoT={r.get('total_sot','')} | corners={r.get('total_corners','')} | signal={r.get('signal_score','')} | reason={r.get('reason','')}")
    lines += ["", "## Guardrails", "- Diagnostic only; no execution.", "- Manual review required for any action."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat(); rows = build(day, tz)
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write_csv(base / "vsigma_live_trigger_validator.csv", rows)
        (base / "vsigma_live_trigger_validator.md").write_text(md(day, rows), encoding="utf-8")
    print(f"rows_validated={len(rows)}")
    print(f"window_counts={count(rows, 'window_status')}")
    print(f"live_trigger_counts={count(rows, 'live_trigger_decision')}")


def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--date", required=True); p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args(); run(a.date, a.timezone)

if __name__ == "__main__": main()
