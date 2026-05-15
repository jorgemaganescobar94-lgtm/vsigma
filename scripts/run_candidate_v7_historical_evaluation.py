from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top
    from run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from run_today_shadow_candidate_v7 import V7_MODE_NAME, build_v7_shortlist, norm_upper
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top
    from scripts.run_today_shadow_candidate_v2_post_results import evaluate_competition_picks, summarize_ledger
    from scripts.run_today_shadow_candidate_v7 import V7_MODE_NAME, build_v7_shortlist, norm_upper


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
BASELINE_HISTORICAL_DIR = PROCESSED_DIR / "historical"
RECENT_LAB_HISTORICAL_DIR = PROCESSED_DIR / "recent_lab_historical" / "historical"
OUTPUT_DIR = PROCESSED_DIR / "candidate_v7_historical"

SUMMARY_CSV = "vsigma_candidate_v7_historical_summary.csv"
DATE_LEDGER_CSV = "vsigma_candidate_v7_historical_by_date.csv"
GUARD_ROWS_CSV = "vsigma_candidate_v7_historical_price_guard_rows.csv"
REPORT_TXT = "vsigma_candidate_v7_historical_report.txt"


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
            "home_team_id",
            "away_team_id",
            "market_alt",
            "alt_model_prob",
            "alt_odds_used",
            "alt_implied_prob",
            "alt_edge",
            "pick_primary_risk",
            "pick_failure_mode",
        ]
        if c in deep.columns
    ]
    if len(merge_cols) <= 1:
        return shortlist.copy()
    out = shortlist.drop(columns=[c for c in merge_cols if c != "fixture_id" and c in shortlist.columns], errors="ignore")
    return out.merge(deep[merge_cols].drop_duplicates("fixture_id"), on="fixture_id", how="left")


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
    probs = pd.to_numeric(ledger.get("competition_calibrated_prob", ledger.get("primary_model_prob", pd.Series(index=ledger.index))), errors="coerce")
    mask = result.isin({"WIN", "LOSS"}) & probs.notna()
    if not mask.any():
        return pd.NA
    y = result[mask].eq("WIN").astype(float)
    return round(float(((probs[mask] - y) ** 2).mean()), 6)


def counts_mix(series: pd.Series) -> str:
    values: list[str] = []
    for raw in series.dropna().astype(str):
        for part in raw.replace("|", ";").split(";"):
            item = part.strip()
            if item and item.upper() not in {"NAN", "NONE"}:
                values.append(item)
    if not values:
        return ""
    counts = pd.Series(values).value_counts()
    return "; ".join(f"{idx}:{int(value)}" for idx, value in counts.items())


def aggregate_ledger(ledger: pd.DataFrame, mode: str) -> dict[str, Any]:
    summary = summarize_ledger(ledger, mode)
    decided = int(summary["wins"]) + int(summary["losses"])
    return {
        "mode": mode,
        "segment": "OVERALL",
        "rows": int(summary["pick_count"]),
        "settled_rows": int(summary["settled_rows"]),
        "wins": int(summary["wins"]),
        "losses": int(summary["losses"]),
        "hit_rate": round(float(summary["wins"]) / decided * 100.0, 6) if decided else pd.NA,
        "profit_units": summary["profit_units"],
        "roi_percent": summary["roi_percent"],
        "brier_score": brier_score(ledger),
        "market_mix": counts_mix(ledger.get("market_primary", pd.Series(dtype=object))) if not ledger.empty else "",
        "failure_mode_mix": counts_mix(ledger.get("accuracy_primary_risk", ledger.get("pick_failure_mode", pd.Series(dtype=object)))) if not ledger.empty else "",
    }


def segment_ledger(ledger: pd.DataFrame, mode: str, segment: str, mask: pd.Series) -> dict[str, Any]:
    row = aggregate_ledger(ledger[mask].copy() if not ledger.empty else pd.DataFrame(), mode)
    row["segment"] = segment
    return row


def guard_counts(rows: pd.DataFrame) -> dict[str, int]:
    decisions = rows.get("price_discipline_decision", pd.Series(dtype=object)).map(norm_upper)
    allowed = pd.to_numeric(rows.get("price_discipline_execution_allowed_flag", pd.Series(dtype=object)), errors="coerce").fillna(0)
    return {
        "price_guard_input_rows": int(len(rows)),
        "price_guard_accepted_rows": int(allowed.eq(1).sum()) if len(rows) else 0,
        "price_guard_rejected_rows": int(allowed.ne(1).sum()) if len(rows) else 0,
        "price_ok_rows": int(decisions.eq("PRICE_OK").sum()) if len(rows) else 0,
        "price_thin_secondary_rows": int(decisions.eq("PRICE_THIN_SECONDARY_ONLY").sum()) if len(rows) else 0,
        "price_prelock_required_rows": int(decisions.eq("PRICE_NEEDS_PRELOCK_CONFIRMATION").sum()) if len(rows) else 0,
        "price_drift_penalized_rows": int(decisions.eq("PRICE_DRIFT_PENALIZED").sum()) if len(rows) else 0,
    }


def pattern_mask(ledger: pd.DataFrame, market_values: set[str], failure_token: str) -> pd.Series:
    if ledger.empty:
        return pd.Series(dtype=bool)
    market = ledger.get("market_primary", pd.Series("", index=ledger.index)).map(norm_upper)
    failure = ledger.get("accuracy_primary_risk", ledger.get("pick_failure_mode", pd.Series("", index=ledger.index))).astype(str).str.upper()
    return market.isin(market_values) & failure.str.contains(failure_token, na=False)


def evaluate_range(start_date: str, end_date: str) -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline_ledgers: list[pd.DataFrame] = []
    v2_ledgers: list[pd.DataFrame] = []
    v7_ledgers: list[pd.DataFrame] = []
    guard_frames: list[pd.DataFrame] = []
    by_date_rows: list[dict[str, Any]] = []

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
        all_v7, _v7_shortlist, v7_top = build_v7_shortlist(v2_source)
        if not all_v7.empty:
            guard = all_v7.copy()
            guard.insert(0, "evaluation_date", match_date)
            guard_frames.append(guard)
        baseline_ledger = add_date_to_ledger(evaluate_mode(baseline_top, raw, "BASELINE_OFFICIAL"), match_date)
        v2_ledger = add_date_to_ledger(evaluate_mode(v2_top, raw, "SHADOW_CANDIDATE_V2"), match_date)
        v7_ledger = add_date_to_ledger(evaluate_mode(v7_top, raw, V7_MODE_NAME), match_date)
        baseline_ledgers.append(baseline_ledger)
        v2_ledgers.append(v2_ledger)
        v7_ledgers.append(v7_ledger)
        base_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
        v2_summary = summarize_ledger(v2_ledger, "SHADOW_CANDIDATE_V2")
        v7_summary = summarize_ledger(v7_ledger, V7_MODE_NAME)
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
                "candidate_v7_rows": v7_summary["pick_count"],
                "candidate_v7_wins": v7_summary["wins"],
                "candidate_v7_losses": v7_summary["losses"],
                "candidate_v7_profit": v7_summary["profit_units"],
                **guard_counts(all_v7),
            }
        )

    all_baseline = concat_nonempty(baseline_ledgers)
    all_v2 = concat_nonempty(v2_ledgers)
    all_v7 = concat_nonempty(v7_ledgers)
    all_guard = concat_nonempty(guard_frames)
    summary_rows = [
        aggregate_ledger(all_baseline, "BASELINE_OFFICIAL"),
        aggregate_ledger(all_v2, "SHADOW_CANDIDATE_V2"),
        {**aggregate_ledger(all_v7, V7_MODE_NAME), **guard_counts(all_guard)},
    ]
    segments = [
        ("OVER_1_5_LOW_CONVERSION", {"OVER_1_5"}, "LOW_CONVERSION"),
        ("OVER_2_5_LOW_CONVERSION", {"OVER_2_5"}, "LOW_CONVERSION"),
        ("BTTS_YES_BTTS_BREAK", {"BTTS_YES"}, "BTTS_BREAK"),
        ("WIN_DRAW_LIVE", {"HOME_WIN", "AWAY_WIN"}, "DRAW_LIVE"),
    ]
    for mode, ledger in [("BASELINE_OFFICIAL", all_baseline), ("SHADOW_CANDIDATE_V2", all_v2), (V7_MODE_NAME, all_v7)]:
        for segment, markets, token in segments:
            summary_rows.append(segment_ledger(ledger, mode, segment, pattern_mask(ledger, markets, token)))
    summary = pd.DataFrame(summary_rows)
    by_date = pd.DataFrame(by_date_rows)
    summary_path = OUTPUT_DIR / SUMMARY_CSV
    by_date_path = OUTPUT_DIR / DATE_LEDGER_CSV
    guard_path = OUTPUT_DIR / GUARD_ROWS_CSV
    report_path = OUTPUT_DIR / REPORT_TXT
    summary.to_csv(summary_path, index=False)
    by_date.to_csv(by_date_path, index=False)
    all_guard.to_csv(guard_path, index=False)
    usable_dates = by_date[by_date.get("status", pd.Series(dtype=object)).eq("OK")]["date"].tolist() if not by_date.empty else []
    lines = [
        "vSIGMA candidate v7 historical evaluation",
        "",
        f"Requested historical range: {start_date} through {end_date}",
        f"Usable dates: {', '.join(usable_dates) if usable_dates else 'none'}",
        "Baseline: frozen historical outputs.",
        "Candidate v2: recent lab historical outputs.",
        "Candidate v7: candidate v2 + Price Discipline / CLV / Drift Execution Guard.",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Summary",
        summary.to_string(index=False) if not summary.empty else "No summary rows.",
        "",
        "By date",
        by_date.to_string(index=False) if not by_date.empty else "No date rows.",
        "",
        "Price guard rows",
        all_guard[
            [
                c
                for c in [
                    "evaluation_date",
                    "fixture_id",
                    "home_team",
                    "away_team",
                    "market_primary",
                    "accuracy_primary_risk",
                    "price_discipline_decision",
                    "price_discipline_min_edge_required",
                    "price_discipline_actual_edge",
                    "price_discipline_drift_status",
                    "clv_direction",
                ]
                if c in all_guard.columns
            ]
        ].to_string(index=False)
        if not all_guard.empty
        else "No guard rows.",
        "",
        "Small-sample limitation: v7 is shadow-only and applies execution governance; it does not create predictive picks.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {"summary": summary_path, "by_date": by_date_path, "guard_rows": guard_path, "report": report_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate candidate v7 price discipline guard on historical snapshots.")
    parser.add_argument("--start-date", default="2026-04-23")
    parser.add_argument("--end-date", default="2026-05-08")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = evaluate_range(args.start_date, args.end_date)
    print("\n=== CANDIDATE V7 HISTORICAL EVALUATION COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    summary = pd.read_csv(paths["summary"])
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
