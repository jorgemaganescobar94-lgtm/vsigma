from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
METRICS = ["total_goals", "total_corners", "total_fouls", "total_shots", "total_sot", "total_cards"]
DETAIL_FIELDS = "target_date generated_at fixture_id home_team away_team metric actual_value baseline_mid shadow_mid baseline_abs_error shadow_abs_error error_delta shadow_result shadow_rule source_guard auto_apply production_change".split()
SUMMARY_FIELDS = "target_date generated_at metric rows_evaluated baseline_avg_error shadow_avg_error avg_error_delta improved_rows worsened_rows unchanged_rows shadow_verdict shadow_rule source_guard auto_apply production_change".split()


def s(x): return "" if x is None else str(x).strip()
def num(x):
    try: return float(s(x)) if s(x) and s(x).lower() != "nan" else None
    except ValueError: return None

def read(path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f: return [dict(r) for r in csv.DictReader(f)]

def write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k,"") for k in fields} for r in rows])

def d(day, name): return P / "today" / day / name

def qrows(day):
    rows = read(d(day, "vsigma_calibration_shadow_patch_queue.csv"))
    return rows or read(P / "governance" / "vsigma_calibration_shadow_patch_queue.csv")

def rules(day):
    out = {}
    for r in qrows(day):
        if r.get("queue_decision") in {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"}:
            out[s(r.get("metric"))] = s(r.get("bias_direction")) or "UNKNOWN"
    return out

def shift(metric, mid, bias):
    down = bias == "OVER_ESTIMATE"
    up = bias == "UNDER_ESTIMATE"
    if not (down or up): return mid, "HOLD_NO_DIRECTION"
    sign = -1 if down else 1
    if metric == "total_goals": return max(0, mid * (0.95 if down else 1.05)), "GOAL_5PCT"
    if metric == "total_corners": return max(0, mid + sign * 1.0), "CORNERS_SHIFT_1"
    if metric == "total_fouls": return max(0, mid * (0.90 if down else 1.10)), "FOULS_10PCT"
    if metric == "total_shots": return max(0, mid * (0.95 if down else 1.05)), "SHOTS_5PCT"
    if metric in {"total_sot", "total_cards"}: return max(0, mid + sign * 0.5), "MID_SHIFT_0_5"
    return mid, "UNKNOWN_HOLD"

def normalized(row, guard):
    metric = s(row.get("metric")); actual = num(row.get("actual_value")); mid = num(row.get("pred_mid") or row.get("pred_mid_value") or row.get("baseline_mid"))
    if metric not in METRICS or actual is None or mid is None: return None
    return {"fixture_id":s(row.get("fixture_id")),"home_team":s(row.get("home_team")),"away_team":s(row.get("away_team")),"metric":metric,"actual_value":actual,"pred_mid":mid,"source_guard":guard}

def from_calibration(day):
    out=[]
    for r in read(d(day,"vsigma_match_stat_forecast_calibration_details.csv")):
        x=normalized(r,"CALIBRATION_DETAILS")
        if x: out.append(x)
    return out

def from_actuals(day):
    forecasts = read(d(day,"vsigma_match_stat_forecasts.csv"))
    actuals = {s(r.get("fixture_id")):r for r in read(d(day,"vsigma_post_match_stat_actuals.csv")) if s(r.get("fixture_id"))}
    out=[]
    for f in forecasts:
        a=actuals.get(s(f.get("fixture_id")))
        if not a: continue
        for m in METRICS:
            actual=num(a.get(f"actual_{m}")); mid=num(f.get(f"{m}_mid"))
            if actual is None or mid is None: continue
            out.append({"fixture_id":s(f.get("fixture_id")),"home_team":s(f.get("home_team")),"away_team":s(f.get("away_team")),"metric":m,"actual_value":actual,"pred_mid":mid,"source_guard":"FORECASTS_JOIN_ACTUALS"})
    return out

def from_backtest(day):
    forecasts = {s(r.get("fixture_id")):r for r in read(d(day,"vsigma_match_stat_forecasts.csv")) if s(r.get("fixture_id"))}
    out=[]
    for b in read(d(day,"vsigma_match_stat_forecast_backtest.csv")):
        f = forecasts.get(s(b.get("fixture_id")), {})
        for m in METRICS:
            actual=num(b.get(f"actual_{m}")); mid=num(f.get(f"{m}_mid") or b.get(f"pred_{m}_mid"))
            if actual is None or mid is None: continue
            out.append({"fixture_id":s(b.get("fixture_id")),"home_team":s(b.get("home_team")) or s(f.get("home_team")),"away_team":s(b.get("away_team")) or s(f.get("away_team")),"metric":m,"actual_value":actual,"pred_mid":mid,"source_guard":"BACKTEST_JOIN_FORECASTS"})
    return out

def source(day):
    for rows, guard in [(from_calibration(day),"CALIBRATION_DETAILS"),(from_actuals(day),"FORECASTS_JOIN_ACTUALS"),(from_backtest(day),"BACKTEST_JOIN_FORECASTS")]:
        if rows: return rows, guard
    return [], "NO_DETAIL_DATA"

def build(day,tz):
    ts=datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds"); rr=rules(day); rows,guard=source(day); details=[]
    for r in rows:
        m=r["metric"]
        if m not in rr: continue
        shadow, rule = shift(m, r["pred_mid"], rr[m]); be=abs(r["actual_value"]-r["pred_mid"]); se=abs(r["actual_value"]-shadow); delta=be-se
        details.append({"target_date":day,"generated_at":ts,"fixture_id":r["fixture_id"],"home_team":r["home_team"],"away_team":r["away_team"],"metric":m,"actual_value":f"{r['actual_value']:.3f}","baseline_mid":f"{r['pred_mid']:.3f}","shadow_mid":f"{shadow:.3f}","baseline_abs_error":f"{be:.3f}","shadow_abs_error":f"{se:.3f}","error_delta":f"{delta:.3f}","shadow_result":"IMPROVED" if delta>0 else "WORSENED" if delta<0 else "UNCHANGED","shadow_rule":rule,"source_guard":guard,"auto_apply":"NO","production_change":"NO"})
    by=defaultdict(list)
    for r in details: by[r["metric"]].append(r)
    summary=[]
    for m,rs in by.items():
        b=sum(float(r["baseline_abs_error"]) for r in rs)/len(rs); sh=sum(float(r["shadow_abs_error"]) for r in rs)/len(rs); delta=b-sh; imp=sum(r["shadow_result"]=="IMPROVED" for r in rs); wor=sum(r["shadow_result"]=="WORSENED" for r in rs); un=len(rs)-imp-wor
        verdict="WAIT_MORE_DETAIL_SAMPLE" if len(rs)<5 else "SHADOW_BETTER_ON_SAMPLE" if delta>0 and imp>=wor else "SHADOW_WORSE_ON_SAMPLE" if delta<0 else "NO_CLEAR_AB_EDGE"
        summary.append({"target_date":day,"generated_at":ts,"metric":m,"rows_evaluated":len(rs),"baseline_avg_error":f"{b:.3f}","shadow_avg_error":f"{sh:.3f}","avg_error_delta":f"{delta:.3f}","improved_rows":imp,"worsened_rows":wor,"unchanged_rows":un,"shadow_verdict":verdict,"shadow_rule":rs[0]["shadow_rule"],"source_guard":guard,"auto_apply":"NO","production_change":"NO"})
    return details, summary, guard

def cnt(rows, field):
    c=Counter(str(r.get(field) or "UNKNOWN") for r in rows); return "; ".join(f"{k}={v}" for k,v in c.most_common()) if c else "none"

def md(day, details, summary, guard):
    lines=[f"# vSIGMA Shadow Forecast A/B Simulator - {day}","","## Summary",f"- source_guard: {guard}",f"- detail_rows: {len(details)}",f"- summary_rows: {len(summary)}",f"- shadow_verdicts: {cnt(summary,'shadow_verdict')}","- auto_apply: NO","- production_change: NO","","## Metric Results"]
    if not summary: lines.append("- none. Need calibration details, forecast+actuals, or backtest+forecast joins.")
    for r in summary: lines.append(f"- {r['metric']} | verdict={r['shadow_verdict']} | rows={r['rows_evaluated']} | baseline_err={r['baseline_avg_error']} | shadow_err={r['shadow_avg_error']} | delta={r['avg_error_delta']}")
    lines += ["","## Guardrails","- Shadow-only advisory.","- No forecast formula edits.","- No official pick changes.","- No production change."]
    return "\n".join(lines)+"\n"

def run(day,tz):
    day=date.fromisoformat(day).isoformat(); details,summary,guard=build(day,tz)
    for base in [P/"today"/day, P/"governance"]:
        write(base/"vsigma_shadow_forecast_ab_details.csv",details,DETAIL_FIELDS); write(base/"vsigma_shadow_forecast_ab_summary.csv",summary,SUMMARY_FIELDS); (base/"vsigma_shadow_forecast_ab_simulator.md").write_text(md(day,details,summary,guard),encoding="utf-8")
    print("=== VSIGMA SHADOW FORECAST A/B SIMULATOR V2 ==="); print(f"source_guard={guard}"); print(f"detail_rows={len(details)}"); print(f"summary_rows={len(summary)}"); print(f"shadow_verdicts={cnt(summary,'shadow_verdict')}"); print("auto_apply=NO"); print("production_change=NO")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--date",required=True); p.add_argument("--timezone",default="Atlantic/Canary"); a=p.parse_args(); run(a.date,a.timezone)
if __name__ == "__main__": main()
