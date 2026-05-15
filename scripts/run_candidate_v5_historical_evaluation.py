from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top
    from run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from run_today_shadow_candidate_v5 import V5_MODE_NAME, apply_player_impact_layer, norm_upper
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top
    from scripts.run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from scripts.run_today_shadow_candidate_v5 import V5_MODE_NAME, apply_player_impact_layer, norm_upper


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
RECENT_LAB_HISTORICAL_DIR = PROCESSED_DIR / "recent_lab_historical" / "historical"
OUTPUT_DIR = PROCESSED_DIR / "candidate_v5_historical"

SUMMARY_CSV = "vsigma_candidate_v5_historical_summary.csv"
DATE_LEDGER_CSV = "vsigma_candidate_v5_historical_by_date.csv"
ADJUSTMENTS_CSV = "vsigma_candidate_v5_historical_player_impact_adjustments.csv"
REPORT_TXT = "vsigma_candidate_v5_historical_report.txt"


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
    player_cols = [
        c
        for c in deep.columns
        if c == "fixture_id"
        or "lineup" in c
        or "injur" in c
        or "absence" in c
        or c in {"market_alt", "alt_model_prob", "alt_odds_used", "alt_implied_prob", "alt_edge"}
    ]
    if len(player_cols) <= 1:
        return shortlist.copy()
    out = shortlist.drop(columns=[c for c in player_cols if c != "fixture_id" and c in shortlist.columns], errors="ignore")
    return out.merge(deep[player_cols].drop_duplicates("fixture_id"), on="fixture_id", how="left")


def mode_top(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "accuracy_mode_eligible_flag" not in df.columns:
        return pd.DataFrame()
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


def concat_nonempty(frames: list[pd.DataFrame]) -> pd.DataFrame:
    nonempty = [df for df in frames if not df.empty]
    return pd.concat(nonempty, ignore_index=True) if nonempty else pd.DataFrame()


def brier_score(ledger: pd.DataFrame) -> Any:
    if ledger.empty:
        return pd.NA
    result = ledger.get("actionable_result", pd.Series("", index=ledger.index)).map(norm_upper)
    probs = pd.to_numeric(
        ledger.get("competition_calibrated_prob", ledger.get("primary_model_prob", pd.Series(index=ledger.index))),
        errors="coerce",
    )
    mask = result.isin({"WIN", "LOSS"}) & probs.notna()
    if not mask.any():
        return pd.NA
    y = result[mask].eq("WIN").astype(float)
    return round(float(((probs[mask] - y) ** 2).mean()), 6)


def market_mix(ledger: pd.DataFrame) -> str:
    if ledger.empty or "market_primary" not in ledger.columns:
        return ""
    return ";".join(f"{market}:{count}" for market, count in ledger["market_primary"].map(norm_upper).value_counts().sort_index().items())


def aggregate_ledger(ledger: pd.DataFrame, mode: str) -> dict[str, Any]:
    summary = summarize_ledger(ledger, mode)
    decided = int(summary["wins"]) + int(summary["losses"])
    return {
        "mode": mode,
        "rows": int(summary["pick_count"]),
        "settled_rows": int(summary["settled_rows"]),
        "wins": int(summary["wins"]),
        "losses": int(summary["losses"]),
        "hit_rate": round(float(summary["wins"]) / decided * 100.0, 6) if decided else pd.NA,
        "profit_units": summary["profit_units"],
        "roi_percent": summary["roi_percent"],
        "brier_score": brier_score(ledger),
        "market_mix": market_mix(ledger),
    }


def action_counts(rows: pd.DataFrame) -> dict[str, int]:
    actions = rows.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper)
    return {
        "player_impact_adjusted_rows": int(actions.ne("NOT_APPLIED").sum()) if len(actions) else 0,
        "player_impact_strengthened_rows": int(actions.eq("PLAYER_IMPACT_STRENGTHEN").sum()) if len(actions) else 0,
        "player_impact_downgraded_rows": int(actions.eq("PLAYER_IMPACT_DOWNGRADE_GOALS").sum()) if len(actions) else 0,
        "player_impact_blocked_rows": int(actions.eq("PLAYER_IMPACT_BLOCK_MARKET").sum()) if len(actions) else 0,
    }


def evaluate_range(start_date: str, end_date: str) -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline_ledgers: list[pd.DataFrame] = []
    v2_ledgers: list[pd.DataFrame] = []
    v5_ledgers: list[pd.DataFrame] = []
    by_date_rows: list[dict[str, Any]] = []
    adjustment_rows: list[pd.DataFrame] = []

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
        all_v5, _v5_shortlist, v5_top = apply_player_impact_layer(v2_source)

        baseline_ledger = add_date_to_ledger(evaluate_mode(baseline_top, raw, "BASELINE_OFFICIAL"), match_date)
        v2_ledger = add_date_to_ledger(evaluate_mode(v2_top, raw, "SHADOW_CANDIDATE_V2"), match_date)
        v5_ledger = add_date_to_ledger(evaluate_mode(v5_top, raw, V5_MODE_NAME), match_date)
        baseline_ledgers.append(baseline_ledger)
        v2_ledgers.append(v2_ledger)
        v5_ledgers.append(v5_ledger)

        adjusted = all_v5[all_v5.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper).ne("NOT_APPLIED")].copy()
        if not adjusted.empty:
            adjusted.insert(0, "evaluation_date", match_date)
            adjustment_rows.append(adjusted)

        base_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
        v2_summary = summarize_ledger(v2_ledger, "SHADOW_CANDIDATE_V2")
        v5_summary = summarize_ledger(v5_ledger, V5_MODE_NAME)
        by_date_rows.append(
            {
                "date": match_date,
                "status": "OK",
                "baseline_rows": base_summary["pick_count"],
                "baseline_wins": base_summary["wins"],
                "baseline_losses": base_summary["losses"],
                "baseline_profit": base_summary["profit_units"],
                "candidate_v2_rows": v2_summary["pick_count"],
                "candidate_v2_wins": v2_summary["wins"],
                "candidate_v2_losses": v2_summary["losses"],
                "candidate_v2_profit": v2_summary["profit_units"],
                "candidate_v5_rows": v5_summary["pick_count"],
                "candidate_v5_wins": v5_summary["wins"],
                "candidate_v5_losses": v5_summary["losses"],
                "candidate_v5_profit": v5_summary["profit_units"],
                **action_counts(adjusted),
            }
        )

    all_baseline = concat_nonempty(baseline_ledgers)
    all_v2 = concat_nonempty(v2_ledgers)
    all_v5 = concat_nonempty(v5_ledgers)
    adjustments = concat_nonempty(adjustment_rows)

    summary = pd.DataFrame(
        [
            aggregate_ledger(all_baseline, "BASELINE_OFFICIAL"),
            aggregate_ledger(all_v2, "SHADOW_CANDIDATE_V2"),
            {
                **aggregate_ledger(all_v5, V5_MODE_NAME),
                **action_counts(adjustments),
            },
        ]
    )
    by_date = pd.DataFrame(by_date_rows)

    summary_path = OUTPUT_DIR / SUMMARY_CSV
    by_date_path = OUTPUT_DIR / DATE_LEDGER_CSV
    adjustments_path = OUTPUT_DIR / ADJUSTMENTS_CSV
    report_path = OUTPUT_DIR / REPORT_TXT
    summary.to_csv(summary_path, index=False)
    by_date.to_csv(by_date_path, index=False)
    adjustments.to_csv(adjustments_path, index=False)

    lines = [
        "vSIGMA candidate v5 historical evaluation",
        "",
        f"Historical range: {start_date} through {end_date}",
        "Baseline: frozen historical outputs.",
        "Candidate v2: recent lab historical outputs.",
        "Candidate v5: candidate v2 + conservative player-impact layer.",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Summary",
        summary.to_string(index=False) if not summary.empty else "No summary rows.",
        "",
        "By date",
        by_date.to_string(index=False) if not by_date.empty else "No date rows.",
        "",
        "Player-impact adjustments",
        adjustments[
            [
                c
                for c in [
                    "evaluation_date",
                    "fixture_id",
                    "home_team",
                    "away_team",
                    "market_primary",
                    "player_impact_original_market",
                    "player_impact_adjustment_action",
                    "player_impact_market_translation_hint",
                    "player_impact_adjustment_reason",
                ]
                if c in adjustments.columns
            ]
        ].to_string(index=False)
        if not adjustments.empty
        else "No player-impact adjustments were made.",
        "",
        "Small-sample limitation: player-impact coverage is often missing; missing coverage was treated as neutral uncertainty.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "summary": summary_path,
        "by_date": by_date_path,
        "adjustments": adjustments_path,
        "report": report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate candidate v5 player impact on historical vSIGMA snapshots.")
    parser.add_argument("--start-date", default="2026-04-23")
    parser.add_argument("--end-date", default="2026-05-08")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = evaluate_range(args.start_date, args.end_date)
    print("\n=== CANDIDATE V5 HISTORICAL EVALUATION COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    summary = pd.read_csv(paths["summary"])
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
