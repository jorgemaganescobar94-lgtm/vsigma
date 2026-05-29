from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = ["source_name","source_type","coverage_scope","league_filter","country_filter","priority_weight","reliability_score","enabled","status","method","notes"]
DEFAULTS = [
    {"source_name":"sportsmole","source_type":"global","coverage_scope":"multi_league","league_filter":"ALL","country_filter":"ALL","priority_weight":"0.85","reliability_score":"0.72","enabled":"YES","status":"ACTIVE","method":"manual_import","notes":"Broad team-news and possible-lineup coverage; support source only."},
    {"source_name":"whoscored","source_type":"global","coverage_scope":"multi_league","league_filter":"ALL","country_filter":"ALL","priority_weight":"0.90","reliability_score":"0.78","enabled":"YES","status":"ACTIVE","method":"manual_import","notes":"Useful probable XI support where available."},
    {"source_name":"rotowire","source_type":"global","coverage_scope":"multi_league","league_filter":"ALL","country_filter":"ALL","priority_weight":"0.80","reliability_score":"0.70","enabled":"YES","status":"ACTIVE","method":"manual_import","notes":"Expected soccer lineups in covered competitions."},
    {"source_name":"guardian_predicted","source_type":"local","coverage_scope":"selected_leagues","league_filter":"Premier League","country_filter":"England","priority_weight":"0.92","reliability_score":"0.82","enabled":"YES","status":"ACTIVE","method":"manual_import","notes":"Stronger for Premier League predicted lineups/team news."},
    {"source_name":"sports_gambler","source_type":"global","coverage_scope":"multi_league","league_filter":"ALL","country_filter":"ALL","priority_weight":"0.78","reliability_score":"0.68","enabled":"YES","status":"ACTIVE","method":"manual_import","notes":"Expected lineup support; not official."},
    {"source_name":"local_media_generic","source_type":"local","coverage_scope":"league_specific","league_filter":"CONFIGURABLE","country_filter":"CONFIGURABLE","priority_weight":"0.88","reliability_score":"0.75","enabled":"YES","status":"REVIEW_ONLY","method":"manual_import","notes":"Trusted local media bucket; configure before activation."},
]


def s(x): return "" if x is None else str(x).strip()
def read(p: Path):
    if not p.exists(): return []
    with p.open("r", encoding="utf-8-sig", newline="") as f: return [dict(r) for r in csv.DictReader(f)]
def write(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows([{k:r.get(k,"") for k in FIELDS} for r in rows])

def num(x, default=0.0):
    try: return float(s(x))
    except ValueError: return default

def normalize(rows):
    if not rows: rows = DEFAULTS
    out=[]; seen=set()
    for r in rows:
        name=s(r.get("source_name")).lower().replace(" ","_")
        if not name or name in seen: continue
        seen.add(name)
        row={k:s(r.get(k)) for k in FIELDS}; row["source_name"]=name
        row["priority_weight"]=f"{max(0,min(1,num(row.get('priority_weight'),0))):.2f}"
        row["reliability_score"]=f"{max(0,min(1,num(row.get('reliability_score'),0))):.2f}"
        row["enabled"]=(row.get("enabled") or "NO").upper()
        row["status"]=(row.get("status") or "REVIEW_ONLY").upper()
        row["method"]=row.get("method") or "manual_import"
        out.append(row)
    return out

def counts(rows, field):
    c=Counter(str(r.get(field) or "UNKNOWN") for r in rows); return "; ".join(f"{k}={v}" for k,v in c.most_common()) if c else "none"

def md(day, rows):
    lines=[f"# vSIGMA Probable Lineup Source Registry - {day}","","## Summary",f"- total_sources: {len(rows)}",f"- enabled: {counts(rows,'enabled')}",f"- status: {counts(rows,'status')}",f"- source_types: {counts(rows,'source_type')}",f"- methods: {counts(rows,'method')}","- auto_apply: NO","- production_change: NO","","## Sources"]
    for r in rows:
        lines.append(f"- {r['source_name']} | enabled={r['enabled']} | status={r['status']} | scope={r['coverage_scope']} | league={r['league_filter']} | country={r['country_filter']} | priority={r['priority_weight']} | reliability={r['reliability_score']} | method={r['method']}")
    lines += ["","## Guardrails","- Registry approves sources for probable XI only, never official lineups.","- Disabled or non-active sources must not influence consensus.","- REVIEW_ONLY sources require explicit per-use review before activation."]
    return "\n".join(lines)+"\n"

def run(day,tz):
    day=date.fromisoformat(day).isoformat(); rows=normalize(read(P/"governance"/"vsigma_probable_lineup_source_registry.csv"))
    for base in [P/"governance", P/"today"/day]:
        write(base/"vsigma_probable_lineup_source_registry.csv", rows)
        (base/"vsigma_probable_lineup_source_registry.md").write_text(md(day,rows), encoding="utf-8")
    print("=== VSIGMA PROBABLE LINEUP SOURCE REGISTRY ==="); print(f"total_sources={len(rows)}"); print(f"status={counts(rows,'status')}"); print("auto_apply=NO"); print("production_change=NO")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--date", required=True); p.add_argument("--timezone", default="Atlantic/Canary"); a=p.parse_args(); run(a.date,a.timezone)
if __name__ == "__main__": main()
