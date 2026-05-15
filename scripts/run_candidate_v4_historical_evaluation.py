from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top
    from run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from run_today_shadow_candidate_v4 import (
        DEGRADE,
        KEEP,
        REMOVE,
        SECONDARY,
        V4_MODE_NAME,
        apply_over25_low_conversion_firewall,
        norm_upper,
    )
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top
    from scripts.run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from scripts.run_today_shadow_candidate_v4 import (
        DEGRADE,
        KEEP,
        REMOVE,
        SECONDARY,
        V4_MODE_NAME,
        apply_over25_low_conversion_firewall,
        norm_upper,
    )


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
RECENT_LAB_HISTORICAL_DIR = PROCESSED_DIR / "recent_lab_historical" / "historical"
OUTPUT_DIR = PROCESSED_DIR / "candidate_v4_historical"

SUMMARY_CSV = "vsigma_candidate_v4_historical_summary.csv"
DATE_LEDGER_CSV = "vsigma_candidate_v4_historical_by_date.csv"
DECISIONS_CSV = "vsigma_candidate_v4_historical_firewall_decisions.csv"
REPORT_TXT = "vsigma_candidate_v4_historical_report.txt"


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def date_dirs(root: Path, start_date: str, end_date: str) -> list[Path]:
    if not root.exists():
        return []
    return [path for path in sorted(root.iterdir()) if path.is_dir() and start_date <= path.name <= end_date]


def merge_deep_fields(shortlist: pd.DataFrame, deep: pd.DataFrame) -> pd.DataFrame:
    if shortlist.empty or deep.empty or "fixture_id" not in shortlist.columns or "fixture_id" not in deep.columns:
        return shortlist.copy()
    merge_cols = [
        c
        for c in [
            "fixture_id",
            "market_alt",
            "alt_model_prob",
            "alt_odds_used",
            "alt_implied_prob",
            "alt_edge",
            "projected_home_goals",
            "projected_away_goals",
            "projected_total_goals",
            "likely_scoreline",
            "odds_total_ladder_shape",
            "odds_line_aggression_flag",
            "odds_over25_support_flag",
            "odds_over15_support_flag",
        ]
        if c in deep.columns
    ]
    if len(merge_cols) <= 1:
        return shortlist.copy()
    out = shortlist.drop(columns=[c for c in merge_cols if c != "fixture_id" and c in shortlist.columns], errors="ignore")
    return out.merge(deep[merge_cols].drop_duplicates("fixture_id"), on="fixture_id", how="left")


def mode_top(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    if "accuracy_mode_eligible_flag" not in df.columns:
        return df.iloc[0:0].copy()
    return select_competition_top(df)


def evaluate_mode(top: pd.DataFrame, raw: pd.DataFrame, mode: str) -> pd.DataFrame:
    if top.empty:
        return pd.DataFrame()
    return evaluate_competition_picks(top, raw, mode)


def add_date_to_ledger(ledger: pd.DataFrame, match_date: str) -> pd.DataFrame:
    out = ledger.copy()
    if not out.empty:
        out.insert(0, "evaluation_date", match_date)
    return out


def aggregate_ledgers(ledgers: list[pd.DataFrame], mode: str) -> dict[str, Any]:
    ledger = concat_nonempty(ledgers)
    summary = summarize_ledger(ledger, mode)
    summary["rows"] = summary.pop("pick_count")
    decided = int(summary["wins"]) + int(summary["losses"])
    summary["hit_rate"] = round(float(summary["wins"]) / decided * 100.0, 6) if decided else pd.NA
    return summary


def concat_nonempty(frames: list[pd.DataFrame]) -> pd.DataFrame:
    nonempty = [df for df in frames if not df.empty]
    return pd.concat(nonempty, ignore_index=True) if nonempty else pd.DataFrame()


def segment_summary(ledger: pd.DataFrame, mode: str, segment: str, mask: pd.Series) -> dict[str, Any]:
    subset = ledger[mask].copy() if not ledger.empty else pd.DataFrame()
    summary = summarize_ledger(subset, f"{mode}:{segment}")
    decided = int(summary["wins"]) + int(summary["losses"])
    return {
        "mode": mode,
        "segment": segment,
        "rows": int(summary["pick_count"]),
        "settled_rows": int(summary["settled_rows"]),
        "wins": int(summary["wins"]),
        "losses": int(summary["losses"]),
        "hit_rate": round(float(summary["wins"]) / decided * 100.0, 6) if decided else pd.NA,
        "profit_units": summary["profit_units"],
        "roi_percent": summary["roi_percent"],
    }


def decision_counts(rows: pd.DataFrame) -> dict[str, int]:
    decisions = rows.get("over25_low_conversion_firewall_decision", pd.Series(dtype=object))
    return {
        "o25_firewall_kept": int(decisions.eq(KEEP).sum()),
        "o25_firewall_downgraded": int(decisions.eq(DEGRADE).sum()),
        "o25_firewall_secondary": int(decisions.eq(SECONDARY).sum()),
        "o25_firewall_removed": int(decisions.eq(REMOVE).sum()),
    }


def evaluate_range(start_date: str, end_date: str, include_live_dates: list[str] | None = None) -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline_ledgers: list[pd.DataFrame] = []
    v2_ledgers: list[pd.DataFrame] = []
    v4_ledgers: list[pd.DataFrame] = []
    by_date_rows: list[dict[str, Any]] = []
    decision_rows: list[pd.DataFrame] = []

    for base_dir in date_dirs(BASELINE_HISTORICAL_DIR, start_date, end_date):
        match_date = base_dir.name
        v2_dir = RECENT_LAB_HISTORICAL_DIR / match_date
        raw = read_csv_optional(base_dir / "matches.csv")
        baseline_source = read_csv_optional(base_dir / "vsigma_execution_shortlist_historical.csv")
        v2_source = read_csv_optional(v2_dir / "vsigma_execution_shortlist_historical.csv")
        v2_deep = read_csv_optional(v2_dir / "vsigma_deep_analysis_candidates.csv")
        if raw.empty or baseline_source.empty or v2_source.empty:
            by_date_rows.append({"date": match_date, "status": "MISSING_INPUT"})
            continue

        baseline_top = mode_top(baseline_source)
        v2_source = merge_deep_fields(v2_source, v2_deep)
        v2_top = mode_top(v2_source)
        all_v4, v4_shortlist, v4_top = apply_over25_low_conversion_firewall(v2_source, v2_top, pd.DataFrame())

        baseline_ledger = add_date_to_ledger(evaluate_mode(baseline_top, raw, "BASELINE_OFFICIAL"), match_date)
        v2_ledger = add_date_to_ledger(evaluate_mode(v2_top, raw, "SHADOW_CANDIDATE_V2"), match_date)
        v4_ledger = add_date_to_ledger(evaluate_mode(v4_top, raw, V4_MODE_NAME), match_date)
        baseline_ledgers.append(baseline_ledger)
        v2_ledgers.append(v2_ledger)
        v4_ledgers.append(v4_ledger)

        checked = all_v4[all_v4.get("over25_low_conversion_firewall_flag", 0).eq(1)].copy()
        if not checked.empty:
            checked.insert(0, "evaluation_date", match_date)
            decision_rows.append(checked)

        base_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
        v2_summary = summarize_ledger(v2_ledger, "SHADOW_CANDIDATE_V2")
        v4_summary = summarize_ledger(v4_ledger, V4_MODE_NAME)
        by_date_rows.append(
            {
                "date": match_date,
                "status": "OK",
                "baseline_rows": base_summary["pick_count"],
                "baseline_wins": base_summary["wins"],
                "baseline_losses": base_summary["losses"],
                "baseline_profit": base_summary["profit_units"],
                "baseline_roi": base_summary["roi_percent"],
                "candidate_v2_rows": v2_summary["pick_count"],
                "candidate_v2_wins": v2_summary["wins"],
                "candidate_v2_losses": v2_summary["losses"],
                "candidate_v2_profit": v2_summary["profit_units"],
                "candidate_v2_roi": v2_summary["roi_percent"],
                "candidate_v4_rows": v4_summary["pick_count"],
                "candidate_v4_wins": v4_summary["wins"],
                "candidate_v4_losses": v4_summary["losses"],
                "candidate_v4_profit": v4_summary["profit_units"],
                "candidate_v4_roi": v4_summary["roi_percent"],
                **decision_counts(checked),
            }
        )

    all_baseline = concat_nonempty(baseline_ledgers)
    all_v2 = concat_nonempty(v2_ledgers)
    all_v4 = concat_nonempty(v4_ledgers)
    decisions = pd.concat(decision_rows, ignore_index=True) if decision_rows else pd.DataFrame()

    summary_rows: list[dict[str, Any]] = []
    for mode, ledger in [
        ("BASELINE_OFFICIAL", all_baseline),
        ("SHADOW_CANDIDATE_V2", all_v2),
        (V4_MODE_NAME, all_v4),
    ]:
        overall = aggregate_ledgers([ledger], mode)
        summary_rows.append(
            {
                "mode": mode,
                "segment": "OVERALL",
                "rows": overall["rows"],
                "settled_rows": overall["settled_rows"],
                "wins": overall["wins"],
                "losses": overall["losses"],
                "hit_rate": overall["hit_rate"],
                "profit_units": overall["profit_units"],
                "roi_percent": overall["roi_percent"],
                "brier_score": pd.NA,
            }
        )
        if not ledger.empty:
            market = ledger.get("market_primary", pd.Series("", index=ledger.index)).map(norm_upper)
            risk = " ".join
            low_conversion = (
                ledger.get("accuracy_primary_risk", pd.Series("", index=ledger.index)).map(norm_upper).str.contains("LOW_CONVERSION", na=False)
                | ledger.get("pick_failure_mode", pd.Series("", index=ledger.index)).map(norm_upper).str.contains("LOW_CONVERSION", na=False)
            )
            summary_rows.append(segment_summary(ledger, mode, "OVER_2_5", market.eq("OVER_2_5")))
            summary_rows.append(segment_summary(ledger, mode, "OVER_2_5_LOW_CONVERSION", market.eq("OVER_2_5") & low_conversion))

    summary = pd.DataFrame(summary_rows)
    by_date = pd.DataFrame(by_date_rows)
    summary_path = OUTPUT_DIR / SUMMARY_CSV
    by_date_path = OUTPUT_DIR / DATE_LEDGER_CSV
    decisions_path = OUTPUT_DIR / DECISIONS_CSV
    report_path = OUTPUT_DIR / REPORT_TXT
    summary.to_csv(summary_path, index=False)
    by_date.to_csv(by_date_path, index=False)
    decisions.to_csv(decisions_path, index=False)

    lines = [
        "vSIGMA candidate v4 historical evaluation",
        "",
        f"Historical range: {start_date} through {end_date}",
        "Baseline: frozen historical outputs.",
        "Candidate v2: recent lab historical outputs.",
        "Candidate v4: candidate v2 + O2.5 Low Conversion Firewall.",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Summary",
        summary.to_string(index=False) if not summary.empty else "No summary rows.",
        "",
        "By date",
        by_date.to_string(index=False) if not by_date.empty else "No date rows.",
        "",
        "Firewall decisions",
        decisions[
            [
                c
                for c in [
                    "evaluation_date",
                    "fixture_id",
                    "home_team",
                    "away_team",
                    "over25_low_conversion_firewall_decision",
                    "over25_low_conversion_confirmation_score",
                    "over25_low_conversion_recommended_market",
                    "over25_low_conversion_firewall_reason",
                ]
                if c in decisions.columns
            ]
        ].to_string(index=False)
        if not decisions.empty
        else "No O2.5 low-conversion rows checked.",
        "",
        "Small-sample limitation: this is a shadow candidate over a short validation window; promotion requires more settled live evidence.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "summary": summary_path,
        "by_date": by_date_path,
        "decisions": decisions_path,
        "report": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate candidate v4 firewall on historical vSIGMA snapshots.")
    parser.add_argument("--start-date", default="2026-04-23")
    parser.add_argument("--end-date", default="2026-05-08")
    parser.add_argument("--live-dates", nargs="*", default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = evaluate_range(args.start_date, args.end_date, args.live_dates)
    print("\n=== CANDIDATE V4 HISTORICAL EVALUATION COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    summary = pd.read_csv(paths["summary"])
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
