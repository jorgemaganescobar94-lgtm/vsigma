from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
METRICS = ["total_goals", "total_corners", "total_fouls", "total_shots", "total_sot", "total_cards"]
DETAIL_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "metric",
    "proposal_id", "actual_value", "baseline_mid", "patched_mid", "baseline_error",
    "patched_error", "error_delta", "dry_run_result", "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "metric", "proposal_id", "rows_evaluated", "baseline_avg_error",
    "patched_avg_error", "avg_error_delta", "improved_rows", "worsened_rows", "unchanged_rows",
    "dry_run_verdict", "manual_review_required", "source_guard", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


def num(x):
    try:
        return float(s(x)) if s(x) and s(x).lower() != "nan" else None
    except ValueError:
        return None


def read(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day, name):
    return P / "today" / day / name


def proposals(day):
    rows = read(d(day, "vsigma_formula_patch_dry_run_diff.csv"))
    if not rows:
        rows = read(P / "governance" / "vsigma_formula_patch_dry_run_diff.csv")
    out = {}
    for r in rows:
        m = s(r.get("metric"))
        pid = s(r.get("proposal_id"))
        if m and pid and pid not in {"NO_REVIEW_PACK", "UNKNOWN"}:
            out[m] = pid
    return out


def actual_rows(day):
    actuals = {s(r.get("fixture_id")): r for r in read(d(day, "vsigma_post_match_stat_actuals.csv")) if s(r.get("fixture_id"))}
    forecasts = read(d(day, "vsigma_match_stat_forecasts.csv"))
    out = []
    if actuals:
        for f in forecasts:
            fid = s(f.get("fixture_id")); a = actuals.get(fid)
            if not a: continue
            for m in METRICS:
                actual = num(a.get(f"actual_{m}")); mid = num(f.get(f"{m}_mid"))
                if actual is None or mid is None: continue
                out.append({"fixture_id": fid, "home_team": s(f.get("home_team")) or s(a.get("home_team")), "away_team": s(f.get("away_team")) or s(a.get("away_team")), "metric": m, "actual": actual, "mid": mid, "source_guard": "FORECASTS_JOIN_ACTUALS"})
        if out: return out
    backtest = read(d(day, "vsigma_match_stat_forecast_backtest.csv"))
    fdict = {s(r.get("fixture_id")): r for r in forecasts if s(r.get("fixture_id"))}
    for b in backtest:
        fid = s(b.get("fixture_id")); f = fdict.get(fid, {})
        for m in METRICS:
            actual = num(b.get(f"actual_{m}")); mid = num(f.get(f"{m}_mid") or b.get(f"pred_{m}_mid"))
            if actual is None or mid is None: continue
            out.append({"fixture_id": fid, "home_team": s(b.get("home_team")) or s(f.get("home_team")), "away_team": s(b.get("away_team")) or s(f.get("away_team")), "metric": m, "actual": actual, "mid": mid, "source_guard": "BACKTEST_JOIN_FORECASTS"})
    return out


def patch_mid(metric, proposal_id, mid):
    if proposal_id == "GOAL_PRESSURE_DOWNSHIFT_V1" and metric == "total_goals":
        return max(0.0, mid * 0.97)
    if proposal_id == "CORNER_VOLUME_CAP_DOWNSHIFT_V1" and metric == "total_corners":
        return max(0.0, mid - 0.75)
    if proposal_id == "FOUL_BASELINE_DOWNSHIFT_V1" and metric == "total_fouls":
        return max(0.0, mid * 0.94)
    if proposal_id == "SHOT_VOLUME_SOFT_DOWNSHIFT_V1" and metric == "total_shots":
        return max(0.0, mid * 0.97)
    return mid


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    props = proposals(day)
    rows = actual_rows(day)
    details = []
    for r in rows:
        m = r["metric"]
        if m not in props: continue
        pid = props[m]
        patched = patch_mid(m, pid, r["mid"])
        be = abs(r["actual"] - r["mid"])
        pe = abs(r["actual"] - patched)
        delta = be - pe
        details.append({
            "target_date": day, "generated_at": ts, "fixture_id": r["fixture_id"],
            "home_team": r["home_team"], "away_team": r["away_team"], "metric": m,
            "proposal_id": pid, "actual_value": f"{r['actual']:.3f}", "baseline_mid": f"{r['mid']:.3f}",
            "patched_mid": f"{patched:.3f}", "baseline_error": f"{be:.3f}", "patched_error": f"{pe:.3f}",
            "error_delta": f"{delta:.3f}", "dry_run_result": "IMPROVED" if delta > 0 else "WORSENED" if delta < 0 else "UNCHANGED",
            "source_guard": r["source_guard"], "auto_apply": "NO", "production_change": "NO",
        })
    by = defaultdict(list)
    for r in details: by[r["metric"]].append(r)
    summary = []
    if not details:
        summary.append({
            "target_date": day, "generated_at": ts, "metric": "ALL", "proposal_id": "NO_SIMULATION",
            "rows_evaluated": 0, "baseline_avg_error": "0.000", "patched_avg_error": "0.000", "avg_error_delta": "0.000",
            "improved_rows": 0, "worsened_rows": 0, "unchanged_rows": 0, "dry_run_verdict": "NO_BACKTEST_ROWS",
            "manual_review_required": "NO", "source_guard": "NO_JOINED_ACTUALS_OR_NO_PROPOSALS", "auto_apply": "NO", "production_change": "NO",
        })
        return details, summary
    for m, rs in by.items():
        b = sum(float(r["baseline_error"]) for r in rs) / len(rs)
        p = sum(float(r["patched_error"]) for r in rs) / len(rs)
        delta = b - p
        imp = sum(r["dry_run_result"] == "IMPROVED" for r in rs)
        wor = sum(r["dry_run_result"] == "WORSENED" for r in rs)
        un = len(rs) - imp - wor
        if len(rs) < 5: verdict = "WAIT_MORE_BACKTEST_SAMPLE"
        elif delta > 0 and imp >= wor: verdict = "PATCH_BACKTEST_IMPROVES"
        elif delta < 0 or wor > imp: verdict = "PATCH_BACKTEST_WORSENS"
        else: verdict = "NO_CLEAR_DRY_RUN_EDGE"
        summary.append({
            "target_date": day, "generated_at": ts, "metric": m, "proposal_id": props.get(m, "UNKNOWN"),
            "rows_evaluated": len(rs), "baseline_avg_error": f"{b:.3f}", "patched_avg_error": f"{p:.3f}",
            "avg_error_delta": f"{delta:.3f}", "improved_rows": imp, "worsened_rows": wor, "unchanged_rows": un,
            "dry_run_verdict": verdict, "manual_review_required": "YES" if verdict == "PATCH_BACKTEST_IMPROVES" else "NO",
            "source_guard": rs[0]["source_guard"], "auto_apply": "NO", "production_change": "NO",
        })
    return details, summary


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, details, summary):
    lines = [
        f"# vSIGMA Formula Patch Dry-Run Backtest - {day}", "",
        "## Summary", f"- detail_rows: {len(details)}", f"- summary_rows: {len(summary)}",
        f"- dry_run_verdicts: {counts(summary, 'dry_run_verdict')}", "- auto_apply: NO", "- production_change: NO", "",
        "## Metric Results",
    ]
    for r in summary:
        lines.append(f"- {r['metric']} | verdict={r['dry_run_verdict']} | rows={r['rows_evaluated']} | baseline_err={r['baseline_avg_error']} | patched_err={r['patched_avg_error']} | delta={r['avg_error_delta']} | improved={r['improved_rows']} | worsened={r['worsened_rows']}")
    lines += ["", "## Guardrails", "- Dry-run backtest only.", "- No production code is modified.", "- No formula, pick, or market change is applied.", "- Real patch requires manual review and post-change validation."]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    details, summary = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_formula_patch_dry_run_backtest_details.csv", details, DETAIL_FIELDS)
        write(base / "vsigma_formula_patch_dry_run_backtest_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_formula_patch_dry_run_backtest.md").write_text(md(day, details, summary), encoding="utf-8")
    print("=== VSIGMA FORMULA PATCH DRY-RUN BACKTEST ===")
    print(f"dry_run_verdicts={counts(summary, 'dry_run_verdict')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main():
    p = argparse.ArgumentParser(); p.add_argument("--date", required=True); p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args(); run(a.date, a.timezone)
if __name__ == "__main__": main()
