from __future__ import annotations

import argparse
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

try:
    from run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from run_today_shadow_candidate_v5 import (
        BLOCK_MARKET,
        DOWNGRADE_GOALS,
        NOT_APPLIED,
        SIDE_RISK_FLAG,
        STRENGTHEN,
        V5_MODE_NAME,
        empty_v5_frame,
        first_available,
        norm_text,
        norm_upper,
    )
except ModuleNotFoundError:
    from scripts.run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from scripts.run_today_shadow_candidate_v5 import (
        BLOCK_MARKET,
        DOWNGRADE_GOALS,
        NOT_APPLIED,
        SIDE_RISK_FLAG,
        STRENGTHEN,
        V5_MODE_NAME,
        empty_v5_frame,
        first_available,
        norm_text,
        norm_upper,
    )


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_V2_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"
CANDIDATE_V5_TOP_CSV = "vsigma_today_candidate_v5_competition_top.csv"
CANDIDATE_V5_LEDGER_CSV = "vsigma_today_candidate_v5_results_ledger.csv"
CANDIDATE_V5_SUMMARY_CSV = "vsigma_today_candidate_v5_results_summary.csv"
RESULT_COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_results.csv"
RESULT_COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_results_report.txt"
SHADOW_POST_REPORT = "today_shadow_candidate_v5_post_report.csv"

EMPTY_LEDGER_COLUMNS = [
    "comparison_mode",
    "competition_pick_rank",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "resolved_home_goals",
    "resolved_away_goals",
    "ledger_result_status",
    "actionable_result",
    "actionable_profit_units",
    "primary_result",
    "primary_profit_units",
]

RESULT_COMPARISON_COLUMNS = [
    "comparison_status",
    "fixture_id",
    "fixture",
    "league",
    "baseline_rank",
    "candidate_v2_rank",
    "candidate_v5_rank",
    "baseline_market",
    "candidate_v2_market",
    "candidate_v5_market",
    "candidate_v5_original_market",
    "candidate_v5_action",
    "baseline_result",
    "candidate_v2_result",
    "candidate_v5_result",
    "baseline_profit_units",
    "candidate_v2_profit_units",
    "candidate_v5_profit_units",
]


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def empty_ledger() -> pd.DataFrame:
    return pd.DataFrame(columns=EMPTY_LEDGER_COLUMNS)


def safe_evaluate_competition_picks(picks: pd.DataFrame, raw: pd.DataFrame, mode: str) -> pd.DataFrame:
    if picks.empty:
        return empty_ledger()
    if raw.empty:
        out = picks.copy()
        for col in EMPTY_LEDGER_COLUMNS:
            if col not in out.columns:
                out[col] = pd.NA
        out["comparison_mode"] = mode
        out["ledger_result_status"] = "UNMATCHED"
        out["actionable_result"] = "UNMATCHED"
        return out
    return evaluate_competition_picks(picks, raw, mode)


def compare_key(df: pd.DataFrame) -> pd.Series:
    return df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()


def build_result_comparison(
    baseline_ledger: pd.DataFrame,
    candidate_v2_ledger: pd.DataFrame,
    candidate_v5_ledger: pd.DataFrame,
) -> pd.DataFrame:
    frames = {
        "baseline": baseline_ledger.copy(),
        "candidate_v2": candidate_v2_ledger.copy(),
        "candidate_v5": candidate_v5_ledger.copy(),
    }
    by_fixture: dict[str, dict[str, pd.Series]] = {}
    for label, df in frames.items():
        if df.empty:
            continue
        df["_fixture_key"] = compare_key(df)
        for key, row in df.drop_duplicates("_fixture_key").set_index("_fixture_key").iterrows():
            by_fixture.setdefault(key, {})[label] = row

    rows: list[dict[str, object]] = []
    for key in sorted(by_fixture):
        item = by_fixture[key]
        b = item.get("baseline", pd.Series(dtype=object))
        v2 = item.get("candidate_v2", pd.Series(dtype=object))
        v5 = item.get("candidate_v5", pd.Series(dtype=object))
        source = b if not b.empty else (v2 if not v2.empty else v5)
        rows.append(
            {
                "comparison_status": "+".join(
                    name.upper()
                    for name, row in [("baseline", b), ("candidate_v2", v2), ("candidate_v5", v5)]
                    if not row.empty
                ),
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["competition_pick_rank"]) if not b.empty else pd.NA,
                "candidate_v2_rank": first_available(v2, ["competition_pick_rank"]) if not v2.empty else pd.NA,
                "candidate_v5_rank": first_available(v5, ["competition_pick_rank"]) if not v5.empty else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if not b.empty else pd.NA,
                "candidate_v2_market": first_available(v2, ["market_primary"]) if not v2.empty else pd.NA,
                "candidate_v5_market": first_available(v5, ["market_primary"]) if not v5.empty else pd.NA,
                "candidate_v5_original_market": first_available(v5, ["player_impact_original_market"]) if not v5.empty else pd.NA,
                "candidate_v5_action": first_available(v5, ["player_impact_adjustment_action"]) if not v5.empty else pd.NA,
                "baseline_result": first_available(b, ["actionable_result"]) if not b.empty else pd.NA,
                "candidate_v2_result": first_available(v2, ["actionable_result"]) if not v2.empty else pd.NA,
                "candidate_v5_result": first_available(v5, ["actionable_result"]) if not v5.empty else pd.NA,
                "baseline_profit_units": first_available(b, ["actionable_profit_units"]) if not b.empty else pd.NA,
                "candidate_v2_profit_units": first_available(v2, ["actionable_profit_units"]) if not v2.empty else pd.NA,
                "candidate_v5_profit_units": first_available(v5, ["actionable_profit_units"]) if not v5.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows, columns=RESULT_COMPARISON_COLUMNS)


def write_result_report(
    path: Path,
    baseline_summary: dict[str, object],
    candidate_v2_summary: dict[str, object],
    candidate_v5_summary: dict[str, object],
    comparison: pd.DataFrame,
    candidate_v5_top: pd.DataFrame,
) -> None:
    actions = candidate_v5_top.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper)
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 VS CANDIDATE V5 RESULTS",
        "",
    ]
    if int(candidate_v5_summary.get("pick_count", 0)) == 0:
        lines.extend(["CANDIDATE_V5_NO_BET", "reason: candidate v5 top empty", ""])
    lines.extend(
        [
            "Mode summary",
            pd.DataFrame([baseline_summary, candidate_v2_summary, candidate_v5_summary]).to_string(index=False),
            "",
            f"Candidate v5 adjusted top picks: {int(actions.ne(NOT_APPLIED).sum()) if len(actions) else 0}",
            "",
            "Pick result comparison",
            comparison.to_string(index=False) if not comparison.empty else "No compared picks.",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_candidate_v5_post_results(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    match_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
) -> dict[str, Path]:
    match_date = match_date or date.today().isoformat()
    raw = read_csv_optional(RAW_MATCHES_CSV)
    baseline_top = read_csv_optional(processed_dir / BASELINE_TOP_CSV)
    candidate_v2_top = read_csv_optional(processed_dir / CANDIDATE_V2_TOP_CSV)
    candidate_v5_top = read_csv_optional(processed_dir / CANDIDATE_V5_TOP_CSV)
    if candidate_v5_top.empty:
        candidate_v5_top = empty_v5_frame(candidate_v2_top)

    baseline_ledger = safe_evaluate_competition_picks(baseline_top, raw, "BASELINE_OFFICIAL")
    candidate_v2_ledger = safe_evaluate_competition_picks(candidate_v2_top, raw, "SHADOW_CANDIDATE_V2")
    candidate_v5_ledger = safe_evaluate_competition_picks(candidate_v5_top, raw, V5_MODE_NAME)
    baseline_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
    candidate_v2_summary = summarize_ledger(candidate_v2_ledger, "SHADOW_CANDIDATE_V2")
    candidate_v5_summary = summarize_ledger(candidate_v5_ledger, V5_MODE_NAME)
    comparison = build_result_comparison(baseline_ledger, candidate_v2_ledger, candidate_v5_ledger)

    ledger_path = processed_dir / CANDIDATE_V5_LEDGER_CSV
    summary_path = processed_dir / CANDIDATE_V5_SUMMARY_CSV
    comparison_path = processed_dir / RESULT_COMPARISON_CSV
    comparison_report_path = processed_dir / RESULT_COMPARISON_REPORT
    shadow_post_path = processed_dir / SHADOW_POST_REPORT

    candidate_v5_ledger.to_csv(ledger_path, index=False)
    pd.DataFrame([candidate_v5_summary]).to_csv(summary_path, index=False)
    comparison.to_csv(comparison_path, index=False)
    write_result_report(
        comparison_report_path,
        baseline_summary,
        candidate_v2_summary,
        candidate_v5_summary,
        comparison,
        candidate_v5_top,
    )

    actions = candidate_v5_top.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper)
    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "baseline_pick_count": baseline_summary["pick_count"],
                "candidate_v2_pick_count": candidate_v2_summary["pick_count"],
                "candidate_v5_pick_count": candidate_v5_summary["pick_count"],
                "overlap_three_way_picks": int(comparison["comparison_status"].eq("BASELINE+CANDIDATE_V2+CANDIDATE_V5").sum()) if not comparison.empty else 0,
                "candidate_v5_strengthened_rows": int(actions.eq(STRENGTHEN).sum()) if len(actions) else 0,
                "candidate_v5_downgraded_rows": int(actions.eq(DOWNGRADE_GOALS).sum()) if len(actions) else 0,
                "candidate_v5_blocked_rows": int(actions.eq(BLOCK_MARKET).sum()) if len(actions) else 0,
                "candidate_v5_side_risk_rows": int(actions.eq(SIDE_RISK_FLAG).sum()) if len(actions) else 0,
                "baseline_wins": baseline_summary["wins"],
                "baseline_losses": baseline_summary["losses"],
                "baseline_profit_units": baseline_summary["profit_units"],
                "baseline_roi_percent": baseline_summary["roi_percent"],
                "candidate_v2_wins": candidate_v2_summary["wins"],
                "candidate_v2_losses": candidate_v2_summary["losses"],
                "candidate_v2_profit_units": candidate_v2_summary["profit_units"],
                "candidate_v2_roi_percent": candidate_v2_summary["roi_percent"],
                "candidate_v5_wins": candidate_v5_summary["wins"],
                "candidate_v5_losses": candidate_v5_summary["losses"],
                "candidate_v5_profit_units": candidate_v5_summary["profit_units"],
                "candidate_v5_roi_percent": candidate_v5_summary["roi_percent"],
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(shadow_post_path, index=False)

    snapshot_dir = today_dir / match_date
    for path in [ledger_path, summary_path, comparison_path, comparison_report_path, shadow_post_path]:
        copy_if_exists(path, snapshot_dir)

    return {
        "candidate_v5_results_ledger": ledger_path,
        "candidate_v5_results_summary": summary_path,
        "result_comparison_csv": comparison_path,
        "result_comparison_report": comparison_report_path,
        "shadow_post_report": shadow_post_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate candidate v5 shadow picks after today's post-results refresh.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = build_candidate_v5_post_results(PROCESSED_DIR, TODAY_DIR, match_date, args.timezone)
    print("\n=== TODAY SHADOW CANDIDATE V5 POST-RESULTS COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
