from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from capture_odds_snapshots import ODDS_SNAPSHOT_DIR, PROCESSED_DIR, TODAY_DIR, norm_text, norm_upper
    from update_immutable_daily_ledger import LEDGER_CSV
except ModuleNotFoundError:
    from scripts.capture_odds_snapshots import ODDS_SNAPSHOT_DIR, PROCESSED_DIR, TODAY_DIR, norm_text, norm_upper
    from scripts.update_immutable_daily_ledger import LEDGER_CSV


ADVICE_CSV = "vsigma_candidate_v7_calibration_advice.csv"
ADVICE_MD = "vsigma_candidate_v7_calibration_advice.md"
CLV_SUMMARY_CSV = "vsigma_clv_summary.csv"
INSUFFICIENT_PRE_MESSAGE = "CLV_TRACKING_INSUFFICIENT_PRE_SNAPSHOT_MISSING"
TRUE_PRE_MISSING_MESSAGE = "CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING"
BACKFILLED_AUDIT_ONLY_MESSAGE = "CLV_BACKFILLED_AUDIT_ONLY"

ADVICE_COLUMNS = [
    "market_family",
    "failure_mode",
    "drift_status",
    "clv_direction",
    "league",
    "n",
    "wins",
    "losses",
    "profit_units",
    "roi_percent",
    "avg_clv_delta",
    "recommendation",
    "recommendation_reason",
]


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or norm_text(value) == "":
            return default
        return float(value)
    except Exception:
        return default


def int_flag(value: object, default: int = 0) -> int:
    text = norm_text(value).upper()
    if text in {"1", "1.0", "TRUE", "YES", "Y"}:
        return 1
    if text in {"0", "0.0", "FALSE", "NO", "N"}:
        return 0
    return default


def normalize_date_value(value: object) -> str:
    if pd.isna(value):
        return ""
    text = norm_text(value)
    if not text:
        return ""
    try:
        return pd.Timestamp(text).date().isoformat()
    except Exception:
        return text[:10]


def filter_for_target_date(df: pd.DataFrame, target_date: str | None, label: str) -> tuple[pd.DataFrame, dict[str, object]]:
    if df.empty or not target_date:
        return df.copy(), {"label": label, "status": "PASS", "excluded_rows": 0, "mismatched_dates": []}
    date_column = "target_date" if "target_date" in df.columns else ("date" if "date" in df.columns else "")
    if not date_column:
        return df.iloc[0:0].copy(), {
            "label": label,
            "status": "CLV_DATE_MISMATCH",
            "excluded_rows": int(len(df)),
            "mismatched_dates": ["MISSING_TARGET_DATE_COLUMN"],
        }
    observed = df[date_column].map(normalize_date_value)
    matched = df[observed.eq(target_date)].copy()
    mismatched_dates = sorted({value for value in observed.tolist() if value and value != target_date})
    excluded_rows = int(len(df) - len(matched))
    return matched, {
        "label": label,
        "status": "CLV_DATE_MISMATCH" if excluded_rows else "PASS",
        "excluded_rows": excluded_rows,
        "mismatched_dates": mismatched_dates,
    }


def market_family(value: object) -> str:
    market = norm_upper(value)
    if market in {"HOME_WIN", "AWAY_WIN"}:
        return "WIN"
    return market or "UNKNOWN"


def failure_mode(value: object) -> str:
    text = norm_upper(value)
    if "LOW_CONVERSION" in text:
        return "LOW_CONVERSION"
    if "BTTS_BREAK" in text:
        return "BTTS_BREAK"
    if "DRAW_LIVE" in text:
        return "DRAW_LIVE"
    return "ANY"


def pattern_name(market: str, failure: str) -> str:
    if market == "WIN" and failure == "DRAW_LIVE":
        return "HOME/AWAY_WIN + FAILURE_MODE_DRAW_LIVE"
    if failure == "ANY":
        return f"{market} + ANY"
    return f"{market} + FAILURE_MODE_{failure}"


def drift_lookup(drift: pd.DataFrame) -> dict[str, str]:
    if drift.empty or "pattern" not in drift.columns or "drift_status" not in drift.columns:
        return {}
    return {norm_text(row["pattern"]): norm_upper(row["drift_status"]) for _, row in drift.iterrows()}


def clv_lookup(clv: pd.DataFrame) -> dict[tuple[str, str, str], dict[str, object]]:
    lookup: dict[tuple[str, str, str], dict[str, object]] = {}
    if clv.empty:
        return lookup
    for _, row in clv.iterrows():
        key = (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")), norm_text(row.get("experiment_id")))
        usable = int_flag(row.get("clv_usable_for_threshold_calibration_flag"), 1 if "clv_usable_for_threshold_calibration_flag" not in clv.columns else 0)
        direction = norm_upper(row.get("clv_direction")) or "CLV_UNAVAILABLE"
        interpretation = row.get("clv_interpretation", "")
        if not usable:
            direction = "CLV_UNAVAILABLE"
            interpretation = BACKFILLED_AUDIT_ONLY_MESSAGE if "BACKFILLED_FROM_AVAILABLE_OUTPUTS" in norm_upper(row.get("snapshot_rebuild_mode")) else TRUE_PRE_MISSING_MESSAGE
        lookup[key] = {
            "clv_direction": direction,
            "clv_delta": row.get("clv_delta", "") if usable else "",
            "clv_interpretation": interpretation,
            "clv_usable_for_threshold_calibration_flag": usable,
        }
    return lookup


def enrich_ledger_for_advice(ledger: pd.DataFrame, drift: pd.DataFrame, clv: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(columns=[*ADVICE_COLUMNS, "result"])
    out = ledger.copy()
    out = out[~out.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")].copy()
    if out.empty:
        return out
    out["market_family"] = out.get("market_primary", pd.Series("", index=out.index)).map(market_family)
    risk_source = out.get("risk_tags", out.get("accuracy_primary_risk", pd.Series("", index=out.index)))
    out["failure_mode"] = risk_source.map(failure_mode)
    drift_by_pattern = drift_lookup(drift)
    out["drift_status"] = [drift_by_pattern.get(pattern_name(row["market_family"], row["failure_mode"]), "UNKNOWN") for _, row in out.iterrows()]
    clv_by_key = clv_lookup(clv)
    clv_rows = [
        clv_by_key.get(
            (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")), norm_text(row.get("experiment_id"))),
            {"clv_direction": "CLV_UNAVAILABLE", "clv_delta": "", "clv_interpretation": TRUE_PRE_MISSING_MESSAGE, "clv_usable_for_threshold_calibration_flag": 0},
        )
        for _, row in out.iterrows()
    ]
    out["clv_direction"] = [row["clv_direction"] for row in clv_rows]
    out["clv_delta"] = [row["clv_delta"] for row in clv_rows]
    out["clv_interpretation"] = [row.get("clv_interpretation", "") for row in clv_rows]
    return out


def recommendation(n: int, roi: float | None, clv_direction: str, drift_status: str) -> tuple[str, str]:
    if n < 10:
        return "SAMPLE_TOO_SMALL", "Fewer than 10 settled rows; collect more snapshots before changing thresholds."
    if clv_direction in {"", "CLV_UNAVAILABLE"}:
        return "INSUFFICIENT_CLV_DATA", f"{TRUE_PRE_MISSING_MESSAGE}; do not change thresholds."
    roi_value = roi if roi is not None else 0.0
    if drift_status in {"ACTIVE_DRIFT", "NEEDS_RECALIBRATION"}:
        return "SECONDARY_ONLY", f"{drift_status} requires execution restraint until recalibrated."
    if roi_value < 0 and clv_direction == "CLV_NEGATIVE":
        return "RAISE_MIN_EDGE", "ROI is negative and CLV is negative; suggest stricter v7 edge requirement."
    if roi_value < 0:
        return "REQUIRE_PRELOCK_CONFIRMATION", "ROI is negative; require pre-lock confirmation before loosening price rules."
    if roi_value > 0 and clv_direction == "CLV_POSITIVE":
        return "KEEP_THRESHOLD", "ROI and CLV are both constructive; keep threshold and continue sampling."
    if roi_value > 15 and clv_direction in {"CLV_POSITIVE", "CLV_FLAT"}:
        return "LOWER_MIN_EDGE", "Strong ROI with non-negative CLV may justify a small future loosen, not an automatic change."
    return "KEEP_THRESHOLD", "No strong evidence for a threshold change."


def summarize_group(group: pd.DataFrame, keys: tuple[Any, ...]) -> dict[str, object]:
    market, failure, drift_status, clv_dir, league = keys
    result = group.get("result", pd.Series(dtype=object)).astype(str).str.upper()
    profit = pd.to_numeric(group.get("profit_units", pd.Series(dtype=object)), errors="coerce").fillna(0.0)
    clv_delta = pd.to_numeric(group.get("clv_delta", pd.Series(dtype=object)), errors="coerce")
    n = int(len(group))
    wins = int(result.eq("WIN").sum())
    losses = int(result.eq("LOSS").sum())
    profit_units = round(float(profit.sum()), 6)
    roi = round(profit_units / n * 100.0, 6) if n else None
    rec, reason = recommendation(n, roi, norm_upper(clv_dir), norm_upper(drift_status))
    return {
        "market_family": market,
        "failure_mode": failure,
        "drift_status": drift_status,
        "clv_direction": clv_dir,
        "league": league,
        "n": n,
        "wins": wins,
        "losses": losses,
        "profit_units": profit_units,
        "roi_percent": roi if roi is not None else pd.NA,
        "avg_clv_delta": round(float(clv_delta.mean()), 6) if clv_delta.notna().any() else pd.NA,
        "recommendation": rec,
        "recommendation_reason": reason,
    }


def build_advice_rows(enriched: pd.DataFrame) -> pd.DataFrame:
    if enriched.empty:
        return pd.DataFrame(columns=ADVICE_COLUMNS)
    work = enriched.copy()
    if "league" not in work.columns:
        work["league"] = "ALL"
    work["league_group"] = "ALL"
    rows: list[dict[str, object]] = []
    group_cols = ["market_family", "failure_mode", "drift_status", "clv_direction", "league_group"]
    for keys, group in work.groupby(group_cols, dropna=False):
        rows.append(summarize_group(group, keys))
    league_counts = work.groupby("league", dropna=False).size()
    eligible_leagues = set(league_counts[league_counts >= 10].index.astype(str).tolist())
    if eligible_leagues:
        league_work = work[work["league"].astype(str).isin(eligible_leagues)].copy()
        league_work["league_group"] = league_work["league"]
        for keys, group in league_work.groupby(group_cols, dropna=False):
            rows.append(summarize_group(group, keys))
    return pd.DataFrame(rows, columns=ADVICE_COLUMNS)


def markdown_table(df: pd.DataFrame, max_rows: int = 40) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).fillna("")
    lines = [
        "| " + " | ".join(str(c) for c in view.columns) + " |",
        "| " + " | ".join("---" for _ in view.columns) + " |",
    ]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[c]).replace("|", "/") for c in view.columns) + " |")
    return "\n".join(lines)


def write_advice_report(path: Path, advice: pd.DataFrame, target_date: str | None) -> None:
    counts = advice.get("recommendation", pd.Series(dtype=object)).value_counts().reset_index()
    if not counts.empty:
        counts.columns = ["recommendation", "rows"]
    unavailable_rows = int(advice.get("clv_direction", pd.Series(dtype=object)).astype(str).str.upper().eq("CLV_UNAVAILABLE").sum())
    lines = [
        "# vSIGMA Candidate v7 Calibration Advisor",
        "",
        f"- Target date context: {target_date or 'ALL'}",
        "- Advisory only: this report never edits config/vsigma_price_discipline_config.json.",
        f"- CLV tracking status: {TRUE_PRE_MISSING_MESSAGE if unavailable_rows else 'CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED'}",
        "",
        "## Recommendation Mix",
        markdown_table(counts),
        "",
        "## Advice",
        markdown_table(advice),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_candidate_v7_calibration_advisor(
    processed_dir: Path = PROCESSED_DIR,
    odds_dir: Path = ODDS_SNAPSHOT_DIR,
    ledger_path: Path | None = None,
    target_date: str | None = None,
) -> dict[str, Path]:
    odds_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = ledger_path or LEDGER_CSV
    ledger = read_csv_optional(ledger_path)
    drift = read_csv_optional(processed_dir / "vsigma_drift_monitor_summary.csv")
    clv = read_csv_optional(odds_dir / CLV_SUMMARY_CSV)
    ledger, ledger_validation = filter_for_target_date(ledger, target_date, "LEDGER")
    clv, clv_validation = filter_for_target_date(clv, target_date, "CLV")
    read_csv_optional(processed_dir / "vsigma_today_candidate_v7_competition_shortlist.csv")
    read_csv_optional(processed_dir / "ledger" / "vsigma_experiment_performance_summary.csv")
    enriched = enrich_ledger_for_advice(ledger, drift, clv)
    advice = build_advice_rows(enriched)
    advice_path = odds_dir / ADVICE_CSV
    report_path = odds_dir / ADVICE_MD
    advice.to_csv(advice_path, index=False)
    write_advice_report(report_path, advice, target_date)
    if ledger_validation["status"] == "CLV_DATE_MISMATCH" or clv_validation["status"] == "CLV_DATE_MISMATCH":
        with report_path.open("a", encoding="utf-8") as handle:
            handle.write("\n## Date Validation\n")
            for validation in [ledger_validation, clv_validation]:
                handle.write(
                    f"\n- {validation['label']}: {validation['status']}; "
                    f"excluded_rows={validation['excluded_rows']}; "
                    f"mismatched_dates={', '.join(validation['mismatched_dates'] or []) or 'None'}"
                )
            handle.write("\n")
    if target_date:
        snapshot_dir = TODAY_DIR / target_date / "odds_snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        for path in [advice_path, report_path]:
            if path.exists():
                (snapshot_dir / path.name).write_bytes(path.read_bytes())
    return {"advice": advice_path, "report": report_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build advisory-only candidate v7 CLV/ROI threshold calibration suggestions.")
    parser.add_argument("--date", default=None)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--odds-dir", type=Path, default=ODDS_SNAPSHOT_DIR)
    parser.add_argument("--ledger-path", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat() if args.date else None
    paths = build_candidate_v7_calibration_advisor(args.processed_dir, args.odds_dir, args.ledger_path, target_date)
    print("\n=== CANDIDATE V7 CALIBRATION ADVISOR BUILT ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
