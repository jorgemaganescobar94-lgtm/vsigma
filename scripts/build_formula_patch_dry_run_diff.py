from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "metric", "proposal_id", "review_decision", "ready_for_diff",
    "target_script", "target_function", "dry_run_diff_status", "diff_summary", "diff_block",
    "validation_required", "manual_review_required", "source_guard", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


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


def source_rows(day):
    p = d(day, "vsigma_formula_patch_review_pack.csv")
    rows = read(p)
    if rows:
        return rows, str(p)
    p = P / "governance" / "vsigma_formula_patch_review_pack.csv"
    return read(p), str(p)


def diff_for(proposal_id: str) -> tuple[str, str]:
    if proposal_id == "GOAL_PRESSURE_DOWNSHIFT_V1":
        return (
            "Dry-run guarded 3-5% goal midpoint downshift after market goal_nudge redistribution.",
            """```diff
--- a/scripts/build_match_stat_forecasts.py
+++ b/scripts/build_match_stat_forecasts.py
@@ forecast_row(...)
     home_goals_mid = clamp(home_goals_mid + goal_nudge * home_share, 0.05, 4.5)
     away_goals_mid = clamp(away_goals_mid + goal_nudge * (1 - home_share), 0.05, 4.5)
+
+    # DRY-RUN ONLY: guarded calibration downshift proposal.
+    # Enable only after MEMORY_IMPROVING_SIGNAL + manual review.
+    # if confidence < 77 and calibration_profile == "GOAL_PRESSURE_DOWNSHIFT_V1":
+    #     home_goals_mid *= 0.97
+    #     away_goals_mid *= 0.97
     total_goals_mid = home_goals_mid + away_goals_mid
```
""",
        )
    if proposal_id == "CORNER_VOLUME_CAP_DOWNSHIFT_V1":
        return (
            "Dry-run reduction of high-side shot-to-corner spillover and optional weak-sample corner midpoint downshift.",
            """```diff
--- a/scripts/build_match_stat_forecasts.py
+++ b/scripts/build_match_stat_forecasts.py
@@ forecast_row(...)
-    shot_corner_nudge = clamp(((home_shots_mid + away_shots_mid) - 23.0) / 42.0, -0.10, 0.14)
+    # DRY-RUN ONLY: cap high-side corner inflation after manual approval.
+    # shot_corner_nudge = clamp(((home_shots_mid + away_shots_mid) - 23.0) / 42.0, -0.10, 0.10)
+    shot_corner_nudge = clamp(((home_shots_mid + away_shots_mid) - 23.0) / 42.0, -0.10, 0.14)
     home_corners_mid *= 1 + shot_corner_nudge
     away_corners_mid *= 1 + shot_corner_nudge
+
+    # Optional dry-run only for weak corner sample rows:
+    # if calibration_profile == "CORNER_VOLUME_CAP_DOWNSHIFT_V1" and "CORNER_SAMPLE_WEAK" in warnings:
+    #     home_corners_mid = max(0, home_corners_mid - 0.25)
+    #     away_corners_mid = max(0, away_corners_mid - 0.25)
```
""",
        )
    if proposal_id == "FOUL_BASELINE_DOWNSHIFT_V1":
        return (
            "Dry-run reduction of default foul baseline when real recent foul data is missing.",
            """```diff
--- a/scripts/build_match_stat_forecasts.py
+++ b/scripts/build_match_stat_forecasts.py
@@ forecast_row(...)
-    home_fouls_mid = avg([num(row.get("home_recent_fouls_pg"), 0)], 12.0)
-    away_fouls_mid = avg([num(row.get("away_recent_fouls_pg"), 0)], 12.0)
+    # DRY-RUN ONLY: lower fallback foul baseline after manual approval.
+    # home_fouls_mid = avg([num(row.get("home_recent_fouls_pg"), 0)], 11.3)
+    # away_fouls_mid = avg([num(row.get("away_recent_fouls_pg"), 0)], 11.3)
+    home_fouls_mid = avg([num(row.get("home_recent_fouls_pg"), 0)], 12.0)
+    away_fouls_mid = avg([num(row.get("away_recent_fouls_pg"), 0)], 12.0)
```
""",
        )
    if proposal_id == "SHOT_VOLUME_SOFT_DOWNSHIFT_V1":
        return (
            "Dry-run softer goal-linked shot-volume multiplier for weak shot sample rows.",
            """```diff
--- a/scripts/build_match_stat_forecasts.py
+++ b/scripts/build_match_stat_forecasts.py
@@ forecast_row(...)
     home_shots_mid *= clamp(0.90 + home_goals_mid / 11.0, 0.86, 1.14)
     away_shots_mid *= clamp(0.90 + away_goals_mid / 11.0, 0.86, 1.14)
+
+    # DRY-RUN ONLY: if SHOT_SAMPLE_WEAK and memory confirms over-estimation:
+    # home_shots_mid *= 0.97
+    # away_shots_mid *= 0.97
```
""",
        )
    return (
        "No dry-run diff generated for hold/no-action proposal.",
        "```diff\n# No formula diff proposed for this metric.\n```\n",
    )


def build(day, tz):
    ts = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows, source = source_rows(day)
    if not rows:
        rows = [{"metric": "ALL", "proposal_id": "NO_REVIEW_PACK", "review_decision": "NO_ACTION", "ready_for_diff": "NO"}]
    out = []
    for r in rows:
        proposal_id = s(r.get("proposal_id")) or "UNKNOWN"
        summary, diff = diff_for(proposal_id)
        ready = s(r.get("ready_for_diff")) or "NO"
        review_decision = s(r.get("review_decision")) or "UNKNOWN"
        status = "READY_DRY_RUN_DIFF" if ready == "YES" and review_decision == "READY_FOR_MANUAL_DIFF" else "DRY_RUN_DIFF_HELD"
        out.append({
            "target_date": day,
            "generated_at": ts,
            "metric": s(r.get("metric")) or "UNKNOWN",
            "proposal_id": proposal_id,
            "review_decision": review_decision,
            "ready_for_diff": ready,
            "target_script": s(r.get("target_script")) or "scripts/build_match_stat_forecasts.py",
            "target_function": s(r.get("target_function")) or "forecast_row",
            "dry_run_diff_status": status,
            "diff_summary": summary,
            "diff_block": diff,
            "validation_required": s(r.get("validation_required")) or "Manual review + post-change backtest required.",
            "manual_review_required": "YES" if status == "READY_DRY_RUN_DIFF" else "NO",
            "source_guard": source,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def counts(rows, field):
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day, rows):
    lines = [
        f"# vSIGMA Formula Patch Dry-Run Diff - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- dry_run_status: {counts(rows, 'dry_run_diff_status')}",
        f"- manual_review_required: {counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Dry-Run Diffs",
    ]
    for r in rows:
        lines += [
            f"### {r['metric']} — {r['dry_run_diff_status']}",
            f"- proposal_id: {r['proposal_id']}",
            f"- review_decision: {r['review_decision']}",
            f"- target: {r['target_script']} :: {r['target_function']}",
            f"- summary: {r['diff_summary']}",
            f"- validation_required: {r['validation_required']}",
            "",
            str(r["diff_block"]).rstrip(),
            "",
        ]
    lines += [
        "## Guardrails",
        "- This file is a dry-run proposal only.",
        "- It does not edit production code.",
        "- No formula, pick, market, or workflow behavior is changed.",
        "- Any real patch requires manual review, explicit approval, and post-change backtest.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_formula_patch_dry_run_diff.csv", rows, FIELDS)
        (base / "vsigma_formula_patch_dry_run_diff.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA FORMULA PATCH DRY-RUN DIFF ===")
    print(f"dry_run_status={counts(rows, 'dry_run_diff_status')}")
    print(f"manual_review_required={counts(rows, 'manual_review_required')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
