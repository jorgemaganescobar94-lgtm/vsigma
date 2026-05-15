from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, format_markdown_table
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, format_markdown_table


EXTENDED_DIR = PROCESSED_DIR / "extended_historical"
LEDGER_INPUT = EXTENDED_DIR / "vsigma_extended_all_ledgers.csv"
SUMMARY_CSV = "vsigma_drift_monitor_summary.csv"
REPORT_TXT = "vsigma_drift_monitor_report.txt"

GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def norm_upper(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def parse_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_ledgers(processed_dir: Path = PROCESSED_DIR) -> pd.DataFrame:
    extended = read_csv_optional(processed_dir / "extended_historical" / "vsigma_extended_all_ledgers.csv")
    if not extended.empty:
        return extended
    frames: list[pd.DataFrame] = []
    for mode, filename in [
        ("BASELINE_OFFICIAL", "vsigma_execution_shortlist_results_ledger.csv"),
        ("SHADOW_CANDIDATE_V2", "vsigma_today_candidate_v2_results_ledger.csv"),
        ("SHADOW_CANDIDATE_V4_O25_LOW_CONVERSION_FIREWALL", "vsigma_today_candidate_v4_results_ledger.csv"),
        ("SHADOW_CANDIDATE_V5_PLAYER_IMPACT", "vsigma_today_candidate_v5_results_ledger.csv"),
        ("SHADOW_CANDIDATE_V6_API_PREDICTIONS_BENCHMARK", "vsigma_today_candidate_v6_results_ledger.csv"),
    ]:
        df = read_csv_optional(processed_dir / filename)
        if not df.empty:
            if "comparison_mode" not in df.columns:
                df["comparison_mode"] = mode
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def settled_subset(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    status = df.get("ledger_result_status", pd.Series("", index=df.index)).map(norm_upper)
    result = df.get("actionable_result", pd.Series("", index=df.index)).map(norm_upper)
    return df[status.eq("RESULT_AVAILABLE") & result.isin(GRADED_RESULTS)].copy()


def drift_status(settled_rows: int, losses: int, profit: float, min_sample: int) -> str:
    if settled_rows < min_sample:
        return "SAMPLE_TOO_SMALL"
    loss_rate = losses / settled_rows if settled_rows else 0.0
    if settled_rows >= max(min_sample * 2, 8) and loss_rate >= 0.7 and profit < 0:
        return "NEEDS_RECALIBRATION"
    if loss_rate >= 0.65 and profit < 0:
        return "ACTIVE_DRIFT"
    if loss_rate >= 0.5 or profit < 0:
        return "WATCH_PATTERN"
    return "NO_DRIFT"


def summarize_pattern(name: str, df: pd.DataFrame, mask: pd.Series, min_sample: int) -> dict[str, Any]:
    subset = settled_subset(df[mask].copy()) if not df.empty else pd.DataFrame()
    result = subset.get("actionable_result", pd.Series("", index=subset.index)).map(norm_upper)
    profit = pd.to_numeric(subset.get("actionable_profit_units", pd.Series(index=subset.index)), errors="coerce").sum(skipna=True) if not subset.empty else 0.0
    rows = int(len(subset))
    wins = int(result.eq("WIN").sum()) if rows else 0
    losses = int(result.eq("LOSS").sum()) if rows else 0
    return {
        "pattern": name,
        "settled_rows": rows,
        "wins": wins,
        "losses": losses,
        "profit_units": round(float(profit), 6),
        "roi_percent": round(float(profit) / rows * 100.0, 6) if rows else pd.NA,
        "drift_status": drift_status(rows, losses, float(profit), min_sample),
    }


def build_drift_summary(ledger: pd.DataFrame, min_sample: int = 5) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(
            [{"pattern": "OVERALL", "settled_rows": 0, "wins": 0, "losses": 0, "profit_units": 0.0, "roi_percent": pd.NA, "drift_status": "SAMPLE_TOO_SMALL"}]
        )
    market = ledger.get("market_primary", pd.Series("", index=ledger.index)).map(norm_upper)
    failure = (
        ledger.get("accuracy_primary_risk", ledger.get("pick_failure_mode", pd.Series("", index=ledger.index)))
        .astype(str)
        .str.upper()
    )
    mode = ledger.get("comparison_mode", pd.Series("", index=ledger.index)).astype(str)
    rows = [
        summarize_pattern("OVER_2_5 + FAILURE_MODE_LOW_CONVERSION", ledger, market.eq("OVER_2_5") & failure.str.contains("LOW_CONVERSION", na=False), min_sample),
        summarize_pattern("OVER_1_5 + FAILURE_MODE_LOW_CONVERSION", ledger, market.eq("OVER_1_5") & failure.str.contains("LOW_CONVERSION", na=False), min_sample),
        summarize_pattern("BTTS_YES + FAILURE_MODE_BTTS_BREAK", ledger, market.eq("BTTS_YES") & failure.str.contains("BTTS_BREAK", na=False), min_sample),
        summarize_pattern("HOME/AWAY_WIN + FAILURE_MODE_DRAW_LIVE", ledger, market.isin(["HOME_WIN", "AWAY_WIN"]) & failure.str.contains("DRAW_LIVE", na=False), min_sample),
        summarize_pattern("candidate v2 vs baseline daily winner", ledger, mode.str.contains("CANDIDATE_V2", na=False), min_sample),
        summarize_pattern("candidate v4 firewall performance", ledger, mode.str.contains("CANDIDATE_V4", na=False), min_sample),
        summarize_pattern(
            "candidate v5 player-impact adjusted subset",
            ledger,
            mode.str.contains("CANDIDATE_V5", na=False)
            & ledger.get("player_impact_action", pd.Series("", index=ledger.index)).astype(str).str.upper().ne("NOT_APPLIED"),
            min_sample,
        ),
        summarize_pattern(
            "candidate v6 API-prediction aligned subset",
            ledger,
            mode.str.contains("CANDIDATE_V6", na=False)
            & ledger.get("api_prediction_alignment_flag", pd.Series("", index=ledger.index)).astype(str).str.upper().eq("ALIGNED"),
            min_sample,
        ),
        summarize_pattern(
            "candidate v6 API-prediction disagreement subset",
            ledger,
            mode.str.contains("CANDIDATE_V6", na=False)
            & ledger.get("api_prediction_alignment_flag", pd.Series("", index=ledger.index)).astype(str).str.upper().eq("DISAGREEMENT"),
            min_sample,
        ),
    ]
    return pd.DataFrame(rows)


def build_drift_monitor(processed_dir: Path = PROCESSED_DIR, min_sample: int = 5) -> dict[str, Path]:
    ledger = load_ledgers(processed_dir)
    summary = build_drift_summary(ledger, min_sample)
    summary_path = processed_dir / SUMMARY_CSV
    report_path = processed_dir / REPORT_TXT
    summary.to_csv(summary_path, index=False)
    counts = summary["drift_status"].value_counts().to_dict() if not summary.empty else {}
    lines = [
        "# vSIGMA Drift Monitor",
        "",
        f"- Generated for: {date.today().isoformat()}",
        f"- Source ledger rows: {len(ledger)}",
        f"- NO_DRIFT: {counts.get('NO_DRIFT', 0)}",
        f"- WATCH_PATTERN: {counts.get('WATCH_PATTERN', 0)}",
        f"- ACTIVE_DRIFT: {counts.get('ACTIVE_DRIFT', 0)}",
        f"- NEEDS_RECALIBRATION: {counts.get('NEEDS_RECALIBRATION', 0)}",
        f"- SAMPLE_TOO_SMALL: {counts.get('SAMPLE_TOO_SMALL', 0)}",
        "",
        format_markdown_table(summary, max_rows=50),
        "",
        "Drift monitor is advisory only. It does not change official baseline selection logic.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {"summary": summary_path, "report": report_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA drift monitor from recent settled ledgers.")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--min-sample", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = build_drift_monitor(args.processed_dir, args.min_sample)
    print("\n=== VSIGMA DRIFT MONITOR COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
