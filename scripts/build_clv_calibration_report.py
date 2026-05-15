from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from capture_odds_snapshots import ODDS_SNAPSHOT_DIR, PROCESSED_DIR, SNAPSHOT_CSV, TODAY_DIR, norm_text, norm_upper
except ModuleNotFoundError:
    from scripts.capture_odds_snapshots import ODDS_SNAPSHOT_DIR, PROCESSED_DIR, SNAPSHOT_CSV, TODAY_DIR, norm_text, norm_upper


SUMMARY_CSV = "vsigma_clv_summary.csv"
REPORT_MD = "vsigma_clv_report.md"
TRUE_PRE_MISSING_MESSAGE = "CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING"
BACKFILLED_AUDIT_ONLY_MESSAGE = "CLV_BACKFILLED_AUDIT_ONLY"

CLV_COLUMNS = [
    "target_date",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "experiment_id",
    "source_candidate_version",
    "pre_price",
    "prelock_price",
    "close_proxy_price",
    "clv_delta",
    "clv_percent",
    "clv_direction",
    "clv_interpretation",
    "result",
    "profit_units",
    "snapshot_rebuild_mode",
    "true_pre_snapshot_available_flag",
    "clv_usable_for_threshold_calibration_flag",
    "source_snapshot_stage",
    "source_snapshot_note",
]

INSUFFICIENT_PRE_MESSAGE = "CLV_TRACKING_INSUFFICIENT_PRE_SNAPSHOT_MISSING"


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def safe_float(value: object, default: float | None = None) -> float | None:
    try:
        if pd.isna(value) or norm_text(value) == "":
            return default
        return float(value)
    except Exception:
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


def filter_snapshots_for_target_date(snapshots: pd.DataFrame, target_date: str | None) -> tuple[pd.DataFrame, dict[str, object]]:
    if snapshots.empty or not target_date:
        return snapshots.copy(), {"status": "PASS", "excluded_rows": 0, "mismatched_dates": []}
    if "target_date" not in snapshots.columns:
        return snapshots.iloc[0:0].copy(), {
            "status": "CLV_DATE_MISMATCH",
            "excluded_rows": int(len(snapshots)),
            "mismatched_dates": ["MISSING_TARGET_DATE_COLUMN"],
        }
    observed = snapshots["target_date"].map(normalize_date_value)
    matched = snapshots[observed.eq(target_date)].copy()
    mismatched_dates = sorted({value for value in observed.tolist() if value and value != target_date})
    excluded_rows = int(len(snapshots) - len(matched))
    status = "CLV_DATE_MISMATCH" if excluded_rows else "PASS"
    return matched, {"status": status, "excluded_rows": excluded_rows, "mismatched_dates": mismatched_dates}


def latest_stage_row(rows: pd.DataFrame, stage: str) -> pd.Series | None:
    subset = rows[rows["pipeline_stage"].astype(str).str.upper().eq(stage)].copy()
    if subset.empty:
        return None
    if "generated_at" in subset.columns:
        subset = subset.sort_values("generated_at")
    return subset.iloc[-1]


def price_from(row: pd.Series | None) -> float | None:
    if row is None:
        return None
    return safe_float(row.get("selected_price"), None)


def int_flag(value: object, default: int = 0) -> int:
    text = norm_text(value).upper()
    if text in {"1", "1.0", "TRUE", "YES", "Y"}:
        return 1
    if text in {"0", "0.0", "FALSE", "NO", "N"}:
        return 0
    return default


def row_flag(row: pd.Series | None, column: str, default: int) -> int:
    if row is None:
        return 0
    if column not in row.index:
        return default
    return int_flag(row.get(column), default)


def clv_direction(pre_price: float | None, end_price: float | None, true_pre_available: bool) -> tuple[str, object, object, str]:
    if not true_pre_available:
        return "CLV_UNAVAILABLE", pd.NA, pd.NA, TRUE_PRE_MISSING_MESSAGE
    if pre_price is None or pre_price <= 1.0:
        return "CLV_UNAVAILABLE", pd.NA, pd.NA, TRUE_PRE_MISSING_MESSAGE
    if end_price is None or end_price <= 1.0:
        return "CLV_UNAVAILABLE", pd.NA, pd.NA, "CLV unavailable: missing close-proxy price."
    delta = round(end_price - pre_price, 6)
    percent = round(((pre_price - end_price) / pre_price) * 100.0, 6)
    if delta < -0.001:
        return "CLV_POSITIVE", delta, percent, "Price shortened after PRE; vSIGMA beat the close proxy."
    if delta > 0.001:
        return "CLV_NEGATIVE", delta, percent, "Price drifted higher after PRE; market moved against vSIGMA."
    return "CLV_FLAT", delta, percent, "Price movement was flat within tolerance."


def result_lookup(processed_dir: Path, target_date: str | None = None) -> dict[tuple[str, str, str], dict[str, object]]:
    sources = [
        ("OFFICIAL_BASELINE", "vsigma_execution_shortlist_results_ledger.csv"),
        ("CANDIDATE_V2_SCHEDULE_ANOMALY", "vsigma_today_candidate_v2_results_ledger.csv"),
        ("CANDIDATE_V7_PRICE_DISCIPLINE", "vsigma_today_candidate_v7_results_ledger.csv"),
    ]
    lookup: dict[tuple[str, str, str], dict[str, object]] = {}
    for experiment_id, filename in sources:
        df = read_csv_optional(processed_dir / filename)
        if df.empty:
            continue
        if target_date:
            date_column = "target_date" if "target_date" in df.columns else ("date" if "date" in df.columns else "")
            if date_column:
                df = df[df[date_column].map(normalize_date_value).eq(target_date)].copy()
                if df.empty:
                    continue
        for _, row in df.iterrows():
            key = (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")), experiment_id)
            lookup[key] = {
                "result": row.get("actionable_result", row.get("primary_result", "")),
                "profit_units": row.get("actionable_profit_units", row.get("primary_profit_units", "")),
            }
    return lookup


def build_clv_rows(snapshots: pd.DataFrame, processed_dir: Path, target_date: str | None = None) -> pd.DataFrame:
    if snapshots.empty:
        return pd.DataFrame(columns=CLV_COLUMNS)
    required = ["target_date", "fixture_id", "market_primary", "experiment_id", "pipeline_stage"]
    for column in required:
        if column not in snapshots.columns:
            snapshots[column] = ""
    results = result_lookup(processed_dir, target_date)
    rows: list[dict[str, object]] = []
    group_cols = ["target_date", "fixture_id", "market_primary", "experiment_id"]
    for key, group in snapshots.groupby(group_cols, dropna=False):
        target_date, fixture_id, market, experiment_id = key
        pre = latest_stage_row(group, "PRE")
        prelock = latest_stage_row(group, "PRELOCK")
        close = latest_stage_row(group, "CLOSE_PROXY")
        post = latest_stage_row(group, "POST")
        close_source = close if close is not None else (post if post is not None else prelock)
        pre_price = price_from(pre)
        prelock_price = price_from(prelock)
        close_price = price_from(close_source)
        true_pre_available = bool(row_flag(pre, "true_pre_snapshot_available_flag", 1))
        pre_usable = bool(row_flag(pre, "clv_usable_for_threshold_calibration_flag", 1))
        close_usable = bool(row_flag(close_source, "clv_usable_for_threshold_calibration_flag", 1))
        direction, delta, percent, interpretation = clv_direction(pre_price, close_price, true_pre_available)
        calibration_usable = int(direction != "CLV_UNAVAILABLE" and true_pre_available and pre_usable and close_usable)
        rebuild_modes = sorted({norm_text(value) for value in group.get("snapshot_rebuild_mode", pd.Series(dtype=object)).dropna().tolist() if norm_text(value)})
        source_stages = sorted({norm_upper(value) for value in group.get("source_snapshot_stage", group.get("pipeline_stage", pd.Series(dtype=object))).dropna().tolist() if norm_text(value)})
        source_notes = sorted({norm_text(value) for value in group.get("source_snapshot_note", pd.Series(dtype=object)).dropna().tolist() if norm_text(value)})
        if any(mode == "BACKFILLED_FROM_AVAILABLE_OUTPUTS" for mode in rebuild_modes) and not calibration_usable:
            interpretation = BACKFILLED_AUDIT_ONLY_MESSAGE if true_pre_available else TRUE_PRE_MISSING_MESSAGE
        elif not true_pre_available:
            interpretation = TRUE_PRE_MISSING_MESSAGE
        source = pre if pre is not None else (prelock if prelock is not None else close_source)
        result = results.get((norm_text(fixture_id), norm_upper(market), norm_text(experiment_id)), {})
        rows.append(
            {
                "target_date": target_date,
                "fixture_id": fixture_id,
                "league": source.get("league", "") if source is not None else "",
                "home_team": source.get("home_team", "") if source is not None else "",
                "away_team": source.get("away_team", "") if source is not None else "",
                "market_primary": norm_upper(market),
                "experiment_id": experiment_id,
                "source_candidate_version": ";".join(sorted({norm_text(value) for value in group.get("source_candidate_version", pd.Series(dtype=object)).dropna().tolist() if norm_text(value)})),
                "pre_price": pre_price if pre_price is not None else pd.NA,
                "prelock_price": prelock_price if prelock_price is not None else pd.NA,
                "close_proxy_price": close_price if close_price is not None else pd.NA,
                "clv_delta": delta,
                "clv_percent": percent,
                "clv_direction": direction,
                "clv_interpretation": interpretation,
                "result": result.get("result", ""),
                "profit_units": result.get("profit_units", ""),
                "snapshot_rebuild_mode": ";".join(rebuild_modes),
                "true_pre_snapshot_available_flag": int(true_pre_available),
                "clv_usable_for_threshold_calibration_flag": calibration_usable,
                "source_snapshot_stage": ";".join(source_stages),
                "source_snapshot_note": ";".join(source_notes),
            }
        )
    return pd.DataFrame(rows, columns=CLV_COLUMNS)


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
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


def write_report(path: Path, summary: pd.DataFrame, target_date: str | None, validation: dict[str, object] | None = None) -> None:
    scoped = summary.copy()
    counts = scoped.get("clv_direction", pd.Series(dtype=object)).value_counts().reset_index()
    if not counts.empty:
        counts.columns = ["clv_direction", "rows"]
    validation = validation or {"status": "PASS", "excluded_rows": 0, "mismatched_dates": []}
    missing_pre_rows = int(
        scoped.get("clv_interpretation", pd.Series(dtype=object)).astype(str).isin([INSUFFICIENT_PRE_MESSAGE, TRUE_PRE_MISSING_MESSAGE]).sum()
    )
    true_pre_rows = int(scoped.get("true_pre_snapshot_available_flag", pd.Series(dtype=object)).map(lambda value: int_flag(value, 0)).sum())
    calibration_usable_rows = int(scoped.get("clv_usable_for_threshold_calibration_flag", pd.Series(dtype=object)).map(lambda value: int_flag(value, 0)).sum())
    backfilled_rows = int(scoped.get("snapshot_rebuild_mode", pd.Series(dtype=object)).astype(str).str.contains("BACKFILLED_FROM_AVAILABLE_OUTPUTS", na=False).sum())
    audit_only_rows = int(len(scoped) - calibration_usable_rows)
    provenance = pd.DataFrame(
        [
            {"metric": "true_pre_rows", "rows": true_pre_rows},
            {"metric": "backfilled_rows", "rows": backfilled_rows},
            {"metric": "calibration_usable_rows", "rows": calibration_usable_rows},
            {"metric": "audit_only_rows", "rows": audit_only_rows},
        ]
    )
    tracking_status = "CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED"
    if missing_pre_rows:
        tracking_status = TRUE_PRE_MISSING_MESSAGE
    elif backfilled_rows:
        tracking_status = BACKFILLED_AUDIT_ONLY_MESSAGE
    lines = [
        "# vSIGMA CLV Calibration Report",
        "",
        f"- Target date: {target_date or 'ALL'}",
        f"- Rows: {len(scoped)}",
        f"- Date validation status: {validation.get('status', 'PASS')}",
        f"- Date-mismatched rows excluded: {validation.get('excluded_rows', 0)}",
        f"- Mismatched target dates observed: {', '.join(validation.get('mismatched_dates', []) or []) or 'None'}",
        f"- Missing PRE snapshot rows: {missing_pre_rows}",
        f"- CLV tracking status: {tracking_status}",
        "",
        "## Snapshot Provenance",
        markdown_table(provenance),
        "",
        "## CLV Direction Mix",
        markdown_table(counts),
        "",
        "## CLV Rows",
        markdown_table(scoped[[c for c in CLV_COLUMNS if c in scoped.columns]], max_rows=40),
        "",
        "Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_clv_calibration_report(
    processed_dir: Path = PROCESSED_DIR,
    odds_dir: Path = ODDS_SNAPSHOT_DIR,
    target_date: str | None = None,
) -> dict[str, Path]:
    odds_dir.mkdir(parents=True, exist_ok=True)
    snapshots = read_csv_optional(odds_dir / SNAPSHOT_CSV.name)
    scoped_snapshots, validation = filter_snapshots_for_target_date(snapshots, target_date)
    summary = build_clv_rows(scoped_snapshots, processed_dir, target_date)
    summary_path = odds_dir / SUMMARY_CSV
    report_path = odds_dir / REPORT_MD
    summary.to_csv(summary_path, index=False)
    write_report(report_path, summary, target_date, validation)
    if target_date:
        snapshot_dir = TODAY_DIR / target_date / "odds_snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        for path in [summary_path, report_path]:
            if path.exists():
                (snapshot_dir / path.name).write_bytes(path.read_bytes())
    return {"summary": summary_path, "report": report_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA CLV/proxy movement summary from odds snapshots.")
    parser.add_argument("--date", default=None)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--odds-dir", type=Path, default=ODDS_SNAPSHOT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat() if args.date else None
    paths = build_clv_calibration_report(args.processed_dir, args.odds_dir, target_date)
    print("\n=== CLV CALIBRATION REPORT BUILT ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
