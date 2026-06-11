from __future__ import annotations

import argparse
import csv
import os
from collections import OrderedDict
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
import json
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
DONE = {"FT", "AET", "PEN"}
RESULT_FIELDS = ["target_date","generated_at","fixture_id","home_team","away_team","status","goals","stats_status","updated_fields","source_guard"]
FINALIZER_FIELDS = ["target_date","generated_at","fixture_id","home_team","away_team","previous_status","api_status","api_goals","finalized","note","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","pending_rows","api_calls","finalized_rows","still_pending_rows","missing_key","next_action","auto_apply","production_change"]

def s(v: Any) -> str: return "" if v is None else str(v).strip()
def read_csv(p: Path) -> list[dict[str,str]]:
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as h: return [dict(r) for r in csv.DictReader(h)]
def write_csv(p: Path, rows: list[dict[str,Any]], fields: list[str]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as h:
        w=csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])
def key() -> str:
    for k in ["APISPORTS_KEY","API_SPORTS_KEY","API_FOOTBALL_KEY","APIFOOTBALL_KEY","API_FOOTBALL_API_KEY","RAPIDAPI_KEY","X_RAPIDAPI_KEY"]:
        if os.environ.get(k): return os.environ[k]
    return ""
def score_text(h: Any, a: Any) -> str:
    return f"{h}-{a}" if h is not None and a is not None else "None-None"
def api_fixture(fid: str, api_key: str) -> dict[str,Any]:
    url=f"https://v3.football.api-sports.io/fixtures?id={fid}"
    req=Request(url, headers={"x-apisports-key": api_key})
    with urlopen(req, timeout=20) as r:
        payload=json.loads(r.read().decode("utf-8"))
    resp=payload.get("response") or []
    return resp[0] if resp else {}
def load_ledger(base: Path, day: str) -> list[dict[str,str]]:
    return read_csv(base/"today"/day/"vsigma_prematch_story_accuracy_ledger.csv") or read_csv(base/"governance"/"vsigma_prematch_story_accuracy_ledger.csv")
def load_existing_results(base: Path, day: str) -> OrderedDict[str,dict[str,Any]]:
    out: OrderedDict[str,dict[str,Any]] = OrderedDict()
    for p in [base/"today"/day/"vsigma_dated_post_match_results_refresh.csv", base/"governance"/"vsigma_dated_post_match_results_refresh.csv"]:
        for r in read_csv(p):
            fid=s(r.get("fixture_id"))
            if fid and fid not in out: out[fid]=r
    return out
def make_result(day: str, now: str, row: dict[str,str], status: str, goals: str, final: bool) -> dict[str,Any]:
    return {"target_date":day,"generated_at":now,"fixture_id":s(row.get("fixture_id")),"home_team":s(row.get("home") or row.get("home_team")),"away_team":s(row.get("away") or row.get("away_team")),"status":status or "UNKNOWN","goals":goals,"stats_status":"STATS_FETCHED" if final else "NOT_FINAL","updated_fields":"pending_prematch_finalizer","source_guard":"API_DIRECT_PENDING_FINALIZER"}
def md(day: str, rows: list[dict[str,Any]], sm: dict[str,Any]) -> str:
    lines=[f"# vSIGMA Pending Prematch Prediction Finalizer - {day}","","## Summary"]
    for k in ["pending_rows","api_calls","finalized_rows","still_pending_rows","missing_key","next_action"]: lines.append(f"- {k}: {sm[k]}")
    lines += ["- auto_apply: NO","- production_change: NO","","## Rows"]
    if not rows: lines.append("- none.")
    for r in rows: lines.append(f"- {r['home_team']} vs {r['away_team']} | previous={r['previous_status']} | api={r['api_status']} | goals={r['api_goals']} | finalized={r['finalized']} | {r['note']}")
    return "\n".join(lines)+"\n"
def append_panel(base: Path, day: str, sm: dict[str,Any]) -> None:
    sec="## Pending Prematch Prediction Finalizer"
    block="\n"+"\n".join([sec,f"- pending_rows: {sm['pending_rows']}",f"- api_calls: {sm['api_calls']}",f"- finalized_rows: {sm['finalized_rows']}",f"- still_pending_rows: {sm['still_pending_rows']}",f"- next_action: {sm['next_action']}"])+"\n"
    for folder in [base/"today"/day, base/"governance"]:
        p=folder/"vsigma_consolidated_daily_operator_panel.md"
        if p.exists():
            t=p.read_text(encoding="utf-8", errors="replace")
            if sec in t:
                before=t.split(sec,1)[0].rstrip(); after=t.split(sec,1)[1]; i=after.find("\n## "); t=before+block+(after[i:] if i>=0 else "")
            else: t=t.rstrip()+block
            p.write_text(t, encoding="utf-8")
def run(day: str, tz: str, base: Path) -> None:
    day=date.fromisoformat(day).isoformat(); now=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    ledger=load_ledger(base, day); pending=[r for r in ledger if s(r.get("review_status"))=="PENDING"]
    api_key=key(); existing=load_existing_results(base, day); report=[]; calls=0; finalized=0; still=0
    for r in pending:
        fid=s(r.get("fixture_id")); prev=s(r.get("actual_status")) or "PENDING"; st=""; goals="None-None"; note=""
        if not api_key:
            st="NO_API_KEY"; note="API key not available"; still+=1
        else:
            calls+=1
            try:
                fx=api_fixture(fid, api_key); status=((fx.get("fixture") or {}).get("status") or {}).get("short") or "UNKNOWN"; g=fx.get("goals") or {}; gh=g.get("home"); ga=g.get("away"); goals=score_text(gh,ga); final=status in DONE and gh is not None and ga is not None; st=status; note="final result captured" if final else "not final yet"
                existing[fid]=make_result(day, now, r, status, goals, final)
                if final: finalized+=1
                else: still+=1
            except Exception as e:
                st="API_ERROR"; note=str(e)[:120]; still+=1
        report.append({"target_date":day,"generated_at":now,"fixture_id":fid,"home_team":s(r.get("home")),"away_team":s(r.get("away")),"previous_status":prev,"api_status":st,"api_goals":goals,"finalized":"YES" if st in DONE else "NO","note":note,"auto_apply":"NO","production_change":"NO"})
    sm={"target_date":day,"generated_at":now,"pending_rows":len(pending),"api_calls":calls,"finalized_rows":finalized,"still_pending_rows":still,"missing_key":"YES" if not api_key else "NO","next_action":"Run accuracy ledger and rolling dashboard after this finalizer.","auto_apply":"NO","production_change":"NO"}
    for folder in [base/"today"/day, base/"governance"]:
        write_csv(folder/"vsigma_pending_prematch_prediction_finalizer.csv", report, FINALIZER_FIELDS); write_csv(folder/"vsigma_pending_prematch_prediction_finalizer_summary.csv", [sm], SUMMARY_FIELDS); (folder/"vsigma_pending_prematch_prediction_finalizer.md").write_text(md(day, report, sm), encoding="utf-8"); write_csv(folder/"vsigma_dated_post_match_results_refresh.csv", list(existing.values()), RESULT_FIELDS)
    append_panel(base, day, sm)
    print("Pending prematch prediction finalizer built")
    print(f"pending_rows={len(pending)} finalized_rows={finalized} still_pending_rows={still}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--timezone", default="Atlantic/Canary"); ap.add_argument("--processed-dir", type=Path, default=BASE); a=ap.parse_args(); run(a.date,a.timezone,a.processed_dir)
