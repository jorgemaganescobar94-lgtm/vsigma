from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, TODAY_DIR, format_markdown_table, read_csv_lenient
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, TODAY_DIR, format_markdown_table, read_csv_lenient


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "vsigma_experiment_registry.json"
LEDGER_DIR = PROCESSED_DIR / "ledger"
ODDS_DIR = PROCESSED_DIR / "odds_snapshots"
GOVERNANCE_DIR = PROCESSED_DIR / "governance"

LEDGER_CSV = LEDGER_DIR / "vsigma_immutable_daily_pick_ledger.csv"
PERFORMANCE_SUMMARY_CSV = LEDGER_DIR / "vsigma_experiment_performance_summary.csv"
PERFORMANCE_REPORT_MD = LEDGER_DIR / "vsigma_experiment_performance_report.md"
DRIFT_SUMMARY_CSV = PROCESSED_DIR / "vsigma_drift_monitor_summary.csv"
DRIFT_REPORT_TXT = PROCESSED_DIR / "vsigma_drift_monitor_report.txt"
CLV_SUMMARY_CSV = ODDS_DIR / "vsigma_clv_summary.csv"
V7_ADVICE_CSV = ODDS_DIR / "vsigma_candidate_v7_calibration_advice.csv"

PROMOTION_SUMMARY_CSV = GOVERNANCE_DIR / "vsigma_promotion_governance_summary.csv"
PROMOTION_REPORT_MD = GOVERNANCE_DIR / "vsigma_promotion_governance_report.md"
THRESHOLD_SUMMARY_CSV = GOVERNANCE_DIR / "vsigma_threshold_governance_summary.csv"
THRESHOLD_REPORT_MD = GOVERNANCE_DIR / "vsigma_threshold_governance_report.md"
GOVERNANCE_DASHBOARD_MD = GOVERNANCE_DIR / "vsigma_governance_dashboard.md"

OFFICIAL_EXPERIMENT_ID = "OFFICIAL_BASELINE"
PROMOTION_MIN_SETTLED = 30
THRESHOLD_MIN_SETTLED = 10
THRESHOLD_RECALIBRATION_SETTLED = 20


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_upper(value: object) -> str:
    return normalize_text(value).upper()


def numeric_series(series: pd.Series | None) -> pd.Series:
    if series is None:
        return pd.Series(dtype=float)
    return pd.to_numeric(series, errors="coerce")


def as_float(value: object, default: float | None = None) -> float | None:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def boolish(value: object) -> bool:
    text = normalize_upper(value)
    return text in {"1", "TRUE", "YES", "Y"}


def load_registry(registry_path: Path = REGISTRY_PATH) -> list[dict[str, Any]]:
    if not registry_path.exists():
        return []
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    experiments = payload.get("experiments", [])
    return [dict(item) for item in experiments if isinstance(item, dict)]


def stable_read(path: Path) -> pd.DataFrame:
    return read_csv_lenient(path)


def pick_rows(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty:
        return ledger.copy()
    status = ledger.get("record_status", pd.Series("", index=ledger.index)).astype(str)
    return ledger[~status.eq("NO_BET_RECORD")].copy()


def settled_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    result = df.get("result", pd.Series("", index=df.index)).astype(str).str.upper()
    status = df.get("record_status", pd.Series("", index=df.index)).astype(str).str.upper()
    mask = result.isin(["WIN", "LOSS", "PUSH", "VOID"]) | status.isin(["SETTLED", "VOID"])
    return df[mask].copy()


def win_loss_counts(df: pd.DataFrame) -> tuple[int, int]:
    result = df.get("result", pd.Series(dtype=object)).astype(str).str.upper() if not df.empty else pd.Series(dtype=object)
    return int(result.eq("WIN").sum()), int(result.eq("LOSS").sum())


def hit_rate_percent(wins: int, losses: int) -> float | str:
    decided = wins + losses
    if decided == 0:
        return ""
    return round((wins / decided) * 100.0, 6)


def roi_percent(profit_units: float, settled_count: int) -> float | str:
    if settled_count == 0:
        return ""
    return round((profit_units / settled_count) * 100.0, 6)


def brier_score(df: pd.DataFrame) -> float | str:
    if df.empty:
        return ""
    prob = numeric_series(df.get("calibrated_probability"))
    result = df.get("result", pd.Series("", index=df.index)).astype(str).str.upper()
    mask = prob.notna() & result.isin(["WIN", "LOSS"])
    if not mask.any():
        return ""
    outcome = result[mask].map({"WIN": 1.0, "LOSS": 0.0})
    return round(float(((prob.loc[mask] - outcome) ** 2).mean()), 6)


def max_drawdown(df: pd.DataFrame) -> float:
    if df.empty or "target_date" not in df.columns:
        return 0.0
    work = df.copy()
    work["profit_num"] = numeric_series(work.get("profit_units")).fillna(0.0)
    daily = work.groupby("target_date", dropna=False)["profit_num"].sum().reset_index()
    daily = daily.sort_values("target_date")
    cumulative = daily["profit_num"].cumsum()
    drawdown = cumulative - cumulative.cummax()
    return round(float(drawdown.min()), 6) if not drawdown.empty else 0.0


def counts_mix(series: pd.Series | None) -> str:
    if series is None:
        return ""
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


def extract_failure_modes(value: object) -> list[str]:
    text = normalize_upper(value)
    if not text:
        return ["UNSPECIFIED"]
    modes: list[str] = []
    for token in re.split(r"[;|,]", text):
        token = token.strip()
        if not token or token in {"NAN", "NONE"}:
            continue
        match = re.search(r"FAILURE_MODE_([A-Z0-9_]+)", token)
        if match:
            modes.append(match.group(1))
        elif token in {"LOW_CONVERSION", "BTTS_BREAK", "DRAW_LIVE"}:
            modes.append(token)
    return sorted(set(modes)) or ["UNSPECIFIED"]


def market_family(value: object) -> str:
    text = normalize_upper(value)
    if text.startswith("OVER_"):
        return text
    if text.startswith("BTTS"):
        return "BTTS"
    if "DRAW" in text:
        return "DRAW"
    if text in {"HOME_WIN", "AWAY_WIN"}:
        return "SIDE"
    return text or "UNKNOWN"


def summarize_from_ledger(experiment: dict[str, Any], ledger: pd.DataFrame) -> dict[str, object]:
    exp_id = normalize_text(experiment.get("experiment_id"))
    rows = ledger[ledger.get("experiment_id", pd.Series(dtype=object)).astype(str).eq(exp_id)].copy() if not ledger.empty else pd.DataFrame()
    picks = pick_rows(rows)
    no_bets = rows[rows.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")].copy() if not rows.empty else rows
    settled = settled_rows(picks)
    wins, losses = win_loss_counts(settled)
    profit = round(float(numeric_series(settled.get("profit_units")).fillna(0.0).sum()), 6) if not settled.empty else 0.0
    avg_prob = numeric_series(picks.get("calibrated_probability")).mean() if not picks.empty else pd.NA
    return {
        "experiment_id": exp_id,
        "display_name": experiment.get("display_name", exp_id),
        "current_status": experiment.get("status", ""),
        "allowed_to_select_officially": bool(experiment.get("allowed_to_select_officially", False)),
        "selection_role": experiment.get("selection_role", ""),
        "total_days_observed": int(rows["target_date"].nunique()) if not rows.empty and "target_date" in rows.columns else 0,
        "pick_days": int(picks["target_date"].nunique()) if not picks.empty and "target_date" in picks.columns else 0,
        "no_bet_days": int(no_bets["target_date"].nunique()) if not no_bets.empty and "target_date" in no_bets.columns else 0,
        "picks_total": int(len(picks)),
        "settled_picks": int(len(settled)),
        "wins": wins,
        "losses": losses,
        "hit_rate": hit_rate_percent(wins, losses),
        "profit_units": profit,
        "roi_percent": roi_percent(profit, len(settled)),
        "brier_score": brier_score(settled),
        "max_drawdown": max_drawdown(settled),
        "average_calibrated_probability": round(float(avg_prob), 6) if not pd.isna(avg_prob) else "",
        "market_mix": counts_mix(picks.get("market_primary")) if not picks.empty else "",
        "failure_mode_mix": counts_mix(picks.get("risk_tags")) if not picks.empty else "",
    }


def registry_performance_rows(
    registry: list[dict[str, Any]],
    ledger: pd.DataFrame,
    performance: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    by_id = {}
    if not performance.empty and "experiment_id" in performance.columns:
        by_id = {str(row["experiment_id"]): row.to_dict() for _, row in performance.iterrows()}
    for experiment in registry:
        exp_id = normalize_text(experiment.get("experiment_id"))
        row = summarize_from_ledger(experiment, ledger)
        perf = by_id.get(exp_id, {})
        for key in [
            "total_days_observed",
            "pick_days",
            "no_bet_days",
            "picks_total",
            "settled_picks",
            "wins",
            "losses",
            "hit_rate",
            "profit_units",
            "roi_percent",
            "brier_score",
            "max_drawdown",
            "average_calibrated_probability",
            "market_mix",
            "failure_mode_mix",
        ]:
            if key in perf and not pd.isna(perf[key]):
                row[key] = perf[key]
        if "status" in perf and normalize_text(perf.get("status")):
            row["current_status"] = perf["status"]
        rows.append(row)
    return pd.DataFrame(rows)


def comparison_vs_official(row: pd.Series, official: pd.Series | None) -> str:
    if official is None or row.get("experiment_id") == OFFICIAL_EXPERIMENT_ID:
        return "official reference"
    pieces: list[str] = []
    metrics = [
        ("hit_rate", "hit"),
        ("roi_percent", "roi"),
        ("profit_units", "profit"),
        ("brier_score", "brier"),
        ("max_drawdown", "drawdown"),
    ]
    for metric, label in metrics:
        candidate_value = as_float(row.get(metric))
        official_value = as_float(official.get(metric))
        if candidate_value is None or official_value is None:
            pieces.append(f"{label}:insufficient")
            continue
        if metric == "brier_score":
            verdict = "better" if candidate_value < official_value else "worse" if candidate_value > official_value else "tie"
        elif metric == "max_drawdown":
            verdict = "better" if candidate_value > official_value else "worse" if candidate_value < official_value else "tie"
        else:
            verdict = "better" if candidate_value > official_value else "worse" if candidate_value < official_value else "tie"
        pieces.append(f"{label}:{verdict}")
    return "; ".join(pieces)


def promotion_recommendation(row: pd.Series, official: pd.Series | None) -> tuple[str, str, str]:
    exp_id = normalize_text(row.get("experiment_id"))
    status = normalize_upper(row.get("current_status"))
    role = normalize_upper(row.get("selection_role"))
    settled = int(as_float(row.get("settled_picks"), 0) or 0)
    picks_total = int(as_float(row.get("picks_total"), 0) or 0)
    allowed = boolish(row.get("allowed_to_select_officially"))

    if exp_id == OFFICIAL_EXPERIMENT_ID:
        return (
            "KEEP_OFFICIAL_BASELINE",
            "Official baseline remains frozen; governance does not alter selection logic.",
            "Continue accumulating official settled outcomes and compare challengers against it.",
        )
    if "AUDIT" in status or "AUDIT" in role:
        return (
            "AUDIT_ONLY",
            "Registry marks this experiment as audit-only, so it is not promotion eligible.",
            "Keep as an audit comparator unless registry governance explicitly changes its role.",
        )
    if allowed:
        return (
            "DO_NOT_PROMOTE",
            "Non-official experiment is already allowed to select officially; registry state requires audit before any promotion recommendation.",
            "Audit registry permissions and confirm no accidental official-selection path exists.",
        )
    if settled < PROMOTION_MIN_SETTLED:
        if picks_total == 0:
            return (
                "SAMPLE_TOO_SMALL",
                f"No settled pick evidence; minimum promotion sample is {PROMOTION_MIN_SETTLED}.",
                "Collect live shadow pick days before making a promotion decision.",
            )
        return (
            "SAMPLE_TOO_SMALL",
            f"Only {settled} settled picks; candidate cannot be promoted before {PROMOTION_MIN_SETTLED} settled picks.",
            "Continue shadow tracking with immutable ledger outcomes.",
        )
    if official is None:
        return (
            "NEEDS_MORE_LIVE_DAYS",
            "Official reference metrics are unavailable, so candidate cannot be compared.",
            "Regenerate experiment performance after official settled results exist.",
        )

    candidate_hit = as_float(row.get("hit_rate"))
    official_hit = as_float(official.get("hit_rate"))
    candidate_brier = as_float(row.get("brier_score"))
    official_brier = as_float(official.get("brier_score"))
    if (
        candidate_hit is not None
        and official_hit is not None
        and candidate_brier is not None
        and official_brier is not None
        and candidate_hit <= official_hit - 5.0
        and candidate_brier >= official_brier + 0.03
    ):
        return (
            "DO_NOT_PROMOTE",
            "Candidate materially worsens hit rate and Brier quality versus official baseline.",
            "Diagnose calibration/failure-mode source before further promotion review.",
        )

    better = 0
    comparable = 0
    checks = [
        ("hit_rate", True, 0.0),
        ("roi_percent", True, 0.0),
        ("profit_units", True, 0.0),
        ("brier_score", False, 0.0),
        ("max_drawdown", True, 0.0),
    ]
    for metric, higher_is_better, tolerance in checks:
        candidate_value = as_float(row.get(metric))
        official_value = as_float(official.get(metric))
        if candidate_value is None or official_value is None:
            continue
        comparable += 1
        if higher_is_better and candidate_value > official_value + tolerance:
            better += 1
        if not higher_is_better and candidate_value < official_value - tolerance:
            better += 1

    candidate_picks = int(as_float(row.get("picks_total"), 0) or 0)
    official_picks = int(as_float(official.get("picks_total"), 0) or 0)
    volume_ok = official_picks == 0 or candidate_picks >= max(10, int(official_picks * 0.6))
    if comparable >= 4 and better >= 4 and volume_ok:
        return (
            "PROMOTE_CANDIDATE",
            "Candidate beats official baseline on most promotion metrics with sufficient settled sample and acceptable volume.",
            "Open a formal human promotion review; do not auto-change official selection.",
        )
    if comparable >= 3 and better >= 2:
        return (
            "SHADOW_CONTINUE",
            "Candidate has useful evidence but has not cleared enough metrics for a formal promotion recommendation.",
            "Continue shadow competition and monitor calibration/volume stability.",
        )
    return (
        "DO_NOT_PROMOTE",
        "Candidate does not beat official baseline on enough evidence-backed metrics.",
        "Keep official baseline frozen and investigate weak comparison metrics.",
    )


def build_promotion_summary(registry: list[dict[str, Any]], ledger: pd.DataFrame, performance: pd.DataFrame) -> pd.DataFrame:
    summary = registry_performance_rows(registry, ledger, performance)
    if summary.empty:
        return pd.DataFrame()
    official_rows = summary[summary["experiment_id"].astype(str).eq(OFFICIAL_EXPERIMENT_ID)]
    official = official_rows.iloc[0] if not official_rows.empty else None
    comparisons: list[str] = []
    recommendations: list[str] = []
    reasons: list[str] = []
    evidence: list[str] = []
    for _, row in summary.iterrows():
        comparisons.append(comparison_vs_official(row, official))
        rec, reason, required = promotion_recommendation(row, official)
        recommendations.append(rec)
        reasons.append(reason)
        evidence.append(required)
    summary = summary.assign(
        comparison_vs_official=comparisons,
        promotion_recommendation=recommendations,
        promotion_reason=reasons,
        required_next_evidence=evidence,
    )
    columns = [
        "experiment_id",
        "display_name",
        "current_status",
        "allowed_to_select_officially",
        "total_days_observed",
        "pick_days",
        "no_bet_days",
        "picks_total",
        "settled_picks",
        "wins",
        "losses",
        "hit_rate",
        "profit_units",
        "roi_percent",
        "brier_score",
        "max_drawdown",
        "average_calibrated_probability",
        "market_mix",
        "failure_mode_mix",
        "comparison_vs_official",
        "promotion_recommendation",
        "promotion_reason",
        "required_next_evidence",
    ]
    return summary[[column for column in columns if column in summary.columns]]


def merge_clv(ledger: pd.DataFrame, clv: pd.DataFrame) -> pd.DataFrame:
    picks = pick_rows(ledger)
    if picks.empty:
        return picks
    if clv.empty or "fixture_id" not in clv.columns:
        picks["clv_direction_merged"] = ""
        picks["clv_delta_merged"] = pd.NA
        picks["clv_usable"] = 0
        return picks
    key_cols = [column for column in ["target_date", "fixture_id", "experiment_id", "market_primary"] if column in picks.columns and column in clv.columns]
    if "fixture_id" not in key_cols:
        key_cols = ["fixture_id"]
    clv_small = clv.copy()
    clv_small["fixture_id"] = clv_small["fixture_id"].astype(str)
    picks = picks.copy()
    picks["fixture_id"] = picks["fixture_id"].astype(str)
    clv_cols = [*key_cols]
    for column in ["clv_direction", "clv_delta", "clv_usable_for_threshold_calibration_flag"]:
        if column in clv_small.columns:
            clv_cols.append(column)
    clv_small = clv_small[clv_cols].drop_duplicates(key_cols)
    merged = picks.merge(clv_small, on=key_cols, how="left", suffixes=("", "_clv"))
    direction_source = merged.get("clv_direction_clv", merged.get("clv_direction", pd.Series("", index=merged.index)))
    delta_source = merged.get("clv_delta_clv", merged.get("clv_delta", pd.Series(dtype=object)))
    merged["clv_direction_merged"] = direction_source.fillna("")
    merged["clv_delta_merged"] = numeric_series(delta_source)
    merged["clv_usable"] = numeric_series(merged.get("clv_usable_for_threshold_calibration_flag")).fillna(0).astype(int) if "clv_usable_for_threshold_calibration_flag" in merged.columns else 0
    return merged


def drift_lookup(drift: pd.DataFrame) -> dict[tuple[str, str], str]:
    lookup: dict[tuple[str, str], str] = {}
    if drift.empty or "pattern" not in drift.columns:
        return lookup
    for _, row in drift.iterrows():
        pattern = normalize_upper(row.get("pattern"))
        status = normalize_text(row.get("drift_status")) or "UNKNOWN"
        parts = [part.strip() for part in pattern.split("+")]
        market = market_family(parts[0]) if parts else "UNKNOWN"
        modes = extract_failure_modes(parts[1] if len(parts) > 1 else "")
        for mode in modes:
            lookup[(market, mode)] = status
    return lookup


def group_sample_status(settled_count: int) -> str:
    if settled_count < THRESHOLD_MIN_SETTLED:
        return "SAMPLE_TOO_SMALL"
    if settled_count < THRESHOLD_RECALIBRATION_SETTLED:
        return "WATCH_SAMPLE"
    return "SUFFICIENT_SAMPLE"


def threshold_recommendation(row: pd.Series) -> tuple[str, str]:
    settled = int(as_float(row.get("settled_rows"), 0) or 0)
    roi = as_float(row.get("roi_percent"))
    hit = as_float(row.get("hit_rate"))
    clv_direction = normalize_upper(row.get("clv_direction"))
    drift_status = normalize_upper(row.get("drift_status"))
    avg_clv = as_float(row.get("avg_clv_delta"))

    if settled < THRESHOLD_MIN_SETTLED:
        return "SAMPLE_TOO_SMALL", f"Only {settled} settled rows; minimum threshold-review sample is {THRESHOLD_MIN_SETTLED}."
    if clv_direction in {"CLV_UNAVAILABLE", "NO_CLV", ""} and int(as_float(row.get("clv_rows"), 0) or 0) > 0:
        return "INSUFFICIENT_CLV_DATA", "CLV is unavailable or unusable; do not change thresholds from price evidence."
    if drift_status in {"ACTION_REQUIRED", "ACTIVE_DRIFT_REVIEW"}:
        return "ACTIVE_DRIFT_REVIEW", "Drift monitor has escalated this pattern."
    if roi is not None and roi < 0 and clv_direction == "CLV_NEGATIVE":
        return "RAISE_MIN_EDGE", "ROI and CLV are both negative, indicating price discipline should tighten."
    if roi is not None and roi < -15 and settled >= THRESHOLD_RECALIBRATION_SETTLED:
        if hit is not None and hit < 50:
            return "NEEDS_RECALIBRATION", "Sufficient sample shows materially negative ROI and weak hit rate."
        return "ACTIVE_DRIFT_REVIEW", "Sufficient sample shows materially negative ROI; review drift and threshold fit."
    if roi is not None and roi < 0 and hit is not None and hit >= 55:
        return "RAISE_MIN_EDGE", "Hit rate is acceptable but ROI is negative, pointing to price/edge discipline."
    if roi is not None and roi < 0 and hit is not None and hit < 50:
        return "SECONDARY_ONLY", "Hit rate and ROI are both weak; downgrade this market/failure-mode pattern."
    if roi is not None and roi < 0:
        return "WATCH_PATTERN", "ROI is negative with enough sample; monitor and consider raising edge if trend persists."
    if roi is not None and roi > 0 and clv_direction == "CLV_POSITIVE":
        return "KEEP_THRESHOLD", "ROI and CLV are positive; current threshold is supported."
    if "WATCH" in drift_status:
        return "WATCH_PATTERN", "Drift monitor flags this pattern for observation."
    return "KEEP_THRESHOLD", "No evidence-backed threshold change is warranted."


def build_threshold_summary(ledger: pd.DataFrame, drift: pd.DataFrame, clv: pd.DataFrame, v7_advice: pd.DataFrame) -> pd.DataFrame:
    merged = merge_clv(ledger, clv)
    if merged.empty:
        return pd.DataFrame(
            columns=[
                "market_family",
                "failure_mode",
                "experiment_id",
                "drift_status",
                "clv_direction",
                "league",
                "bucket",
                "rows",
                "settled_rows",
                "wins",
                "losses",
                "hit_rate",
                "profit_units",
                "roi_percent",
                "avg_edge",
                "avg_calibrated_probability",
                "avg_clv_delta",
                "sample_status",
                "threshold_recommendation",
                "threshold_reason",
            ]
        )
    drift_map = drift_lookup(drift)
    expanded: list[dict[str, object]] = []
    for _, row in merged.iterrows():
        modes = extract_failure_modes(row.get("risk_tags"))
        family = market_family(row.get("market_primary"))
        for mode in modes:
            out = row.to_dict()
            out["market_family"] = family
            out["failure_mode"] = mode
            out["drift_status"] = drift_map.get((family, mode), normalize_text(row.get("price_discipline_drift_status")) or "UNKNOWN")
            expanded.append(out)
    work = pd.DataFrame(expanded)
    if work.empty:
        return pd.DataFrame()
    work["is_settled"] = work.get("result", pd.Series("", index=work.index)).astype(str).str.upper().isin(["WIN", "LOSS", "PUSH", "VOID"])
    work["is_win"] = work.get("result", pd.Series("", index=work.index)).astype(str).str.upper().eq("WIN")
    work["is_loss"] = work.get("result", pd.Series("", index=work.index)).astype(str).str.upper().eq("LOSS")
    work["profit_num"] = numeric_series(work.get("profit_units")).fillna(0.0)
    work["edge_num"] = numeric_series(work.get("edge"))
    work["prob_num"] = numeric_series(work.get("calibrated_probability"))
    work["clv_num"] = numeric_series(work.get("clv_delta_merged"))
    work["clv_direction_norm"] = work.get("clv_direction_merged", pd.Series("", index=work.index)).fillna("").astype(str).str.upper()
    work["league_group"] = work.get("league", pd.Series("ALL", index=work.index)).fillna("ALL")
    if "shortlist_bucket" in work.columns:
        work["bucket_group"] = work["shortlist_bucket"].fillna("ALL")
    elif "analysis_label" in work.columns:
        work["bucket_group"] = work["analysis_label"].fillna("ALL")
    else:
        work["bucket_group"] = "ALL"
    aggregate_work = work.copy()
    aggregate_work["league_group"] = "ALL"
    league_group_cols = ["market_family", "failure_mode", "experiment_id", "drift_status", "league_group", "bucket_group"]
    league_sizes = work.groupby(league_group_cols, dropna=False).size().reset_index(name="group_rows")
    league_sizes = league_sizes[league_sizes["group_rows"] >= THRESHOLD_MIN_SETTLED]
    if not league_sizes.empty:
        league_work = work.merge(league_sizes[league_group_cols], on=league_group_cols, how="inner")
        work = pd.concat([aggregate_work, league_work], ignore_index=True)
    else:
        work = aggregate_work

    rows: list[dict[str, object]] = []
    group_cols = ["market_family", "failure_mode", "experiment_id", "drift_status", "league_group", "bucket_group"]
    for keys, group in work.groupby(group_cols, dropna=False):
        settled = group[group["is_settled"]].copy()
        wins = int(settled["is_win"].sum())
        losses = int(settled["is_loss"].sum())
        profit = round(float(settled["profit_num"].sum()), 6) if not settled.empty else 0.0
        clv_counts = group["clv_direction_norm"].replace("", pd.NA).dropna().value_counts()
        clv_direction = str(clv_counts.index[0]) if not clv_counts.empty else ""
        clv_rows = int(group["clv_direction_norm"].replace("", pd.NA).dropna().shape[0])
        row = {
            "market_family": keys[0],
            "failure_mode": keys[1],
            "experiment_id": keys[2],
            "drift_status": keys[3],
            "clv_direction": clv_direction,
            "league": keys[4],
            "bucket": keys[5],
            "rows": int(len(group)),
            "settled_rows": int(len(settled)),
            "wins": wins,
            "losses": losses,
            "hit_rate": hit_rate_percent(wins, losses),
            "profit_units": profit,
            "roi_percent": roi_percent(profit, len(settled)),
            "avg_edge": round(float(group["edge_num"].mean()), 6) if group["edge_num"].notna().any() else "",
            "avg_calibrated_probability": round(float(group["prob_num"].mean()), 6) if group["prob_num"].notna().any() else "",
            "avg_clv_delta": round(float(group["clv_num"].mean()), 6) if group["clv_num"].notna().any() else "",
            "clv_rows": clv_rows,
            "sample_status": group_sample_status(int(len(settled))),
        }
        rec, reason = threshold_recommendation(pd.Series(row))
        row["threshold_recommendation"] = rec
        row["threshold_reason"] = reason
        rows.append(row)

    summary = pd.DataFrame(rows)
    if not v7_advice.empty:
        advice_rows: list[dict[str, object]] = []
        for _, advice in v7_advice.iterrows():
            n = int(as_float(advice.get("n"), 0) or 0)
            row = {
                "market_family": normalize_text(advice.get("market_family")) or "UNKNOWN",
                "failure_mode": normalize_text(advice.get("failure_mode")) or "UNSPECIFIED",
                "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
                "drift_status": normalize_text(advice.get("drift_status")) or "UNKNOWN",
                "clv_direction": normalize_text(advice.get("clv_direction")),
                "league": normalize_text(advice.get("league")) or "ALL",
                "bucket": "V7_ADVISOR",
                "rows": n,
                "settled_rows": n,
                "wins": int(as_float(advice.get("wins"), 0) or 0),
                "losses": int(as_float(advice.get("losses"), 0) or 0),
                "hit_rate": hit_rate_percent(int(as_float(advice.get("wins"), 0) or 0), int(as_float(advice.get("losses"), 0) or 0)),
                "profit_units": as_float(advice.get("profit_units"), 0.0) or 0.0,
                "roi_percent": as_float(advice.get("roi_percent"), ""),
                "avg_edge": "",
                "avg_calibrated_probability": "",
                "avg_clv_delta": as_float(advice.get("avg_clv_delta"), ""),
                "clv_rows": n,
                "sample_status": group_sample_status(n),
                "threshold_recommendation": normalize_text(advice.get("recommendation")) or "DO_NOT_CHANGE",
                "threshold_reason": normalize_text(advice.get("recommendation_reason")) or "Imported from candidate v7 calibration advisor.",
            }
            advice_rows.append(row)
        summary = pd.concat([summary, pd.DataFrame(advice_rows)], ignore_index=True)

    columns = [
        "market_family",
        "failure_mode",
        "experiment_id",
        "drift_status",
        "clv_direction",
        "league",
        "bucket",
        "rows",
        "settled_rows",
        "wins",
        "losses",
        "hit_rate",
        "profit_units",
        "roi_percent",
        "avg_edge",
        "avg_calibrated_probability",
        "avg_clv_delta",
        "sample_status",
        "threshold_recommendation",
        "threshold_reason",
        "clv_rows",
    ]
    return summary[[column for column in columns if column in summary.columns]].sort_values(
        ["threshold_recommendation", "settled_rows", "profit_units"],
        ascending=[True, False, True],
    )


def clv_sufficiency(clv: pd.DataFrame) -> str:
    if clv.empty:
        return "INSUFFICIENT_CLV_DATA: no CLV summary available."
    usable = 0
    if "clv_usable_for_threshold_calibration_flag" in clv.columns:
        usable = int(numeric_series(clv["clv_usable_for_threshold_calibration_flag"]).fillna(0).eq(1).sum())
    direction = clv.get("clv_direction", pd.Series(dtype=object)).astype(str).str.upper()
    available = int((~direction.isin(["", "CLV_UNAVAILABLE", "NAN"])).sum())
    if usable < THRESHOLD_MIN_SETTLED and available < THRESHOLD_MIN_SETTLED:
        return f"INSUFFICIENT_CLV_DATA: usable={usable}, available_direction_rows={available}; do not change thresholds from CLV yet."
    return f"CLV_DATA_SUFFICIENT_FOR_REVIEW: usable={usable}, available_direction_rows={available}; advice remains reporting-only."


def drift_alerts(drift: pd.DataFrame, threshold: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    if not drift.empty:
        for _, row in drift.iterrows():
            settled = int(as_float(row.get("settled_rows"), 0) or 0)
            status = normalize_upper(row.get("drift_status"))
            roi = as_float(row.get("roi_percent"))
            if settled < THRESHOLD_MIN_SETTLED:
                level = "SAMPLE_TOO_SMALL"
            elif status in {"ACTION_REQUIRED", "ACTIVE_DRIFT_REVIEW", "NEEDS_RECALIBRATION"}:
                level = "ACTION_REQUIRED"
            elif roi is not None and roi < -15:
                level = "WARNING"
            elif "WATCH" in status:
                level = "WATCH"
            else:
                level = "INFO"
            rows.append(
                {
                    "alert_level": level,
                    "pattern": row.get("pattern", ""),
                    "settled_rows": settled,
                    "profit_units": row.get("profit_units", ""),
                    "roi_percent": row.get("roi_percent", ""),
                    "drift_status": row.get("drift_status", ""),
                    "governance_action": "Review threshold summary before any config change.",
                }
            )
    if threshold.empty:
        return pd.DataFrame(rows)
    recs = threshold[threshold["threshold_recommendation"].astype(str).isin(["ACTIVE_DRIFT_REVIEW", "NEEDS_RECALIBRATION", "RAISE_MIN_EDGE", "SECONDARY_ONLY"])]
    for _, row in recs.iterrows():
        rows.append(
            {
                "alert_level": "ACTION_REQUIRED" if row["threshold_recommendation"] in {"ACTIVE_DRIFT_REVIEW", "NEEDS_RECALIBRATION"} else "WARNING",
                "pattern": f"{row.get('market_family')} + {row.get('failure_mode')} + {row.get('experiment_id')}",
                "settled_rows": row.get("settled_rows", ""),
                "profit_units": row.get("profit_units", ""),
                "roi_percent": row.get("roi_percent", ""),
                "drift_status": row.get("drift_status", ""),
                "governance_action": row.get("threshold_recommendation", ""),
            }
        )
    return pd.DataFrame(rows).drop_duplicates()


def daily_winner_summary(ledger: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty or "target_date" not in ledger.columns:
        return pd.DataFrame(columns=["target_date", "daily_winner", "winner_reason"])
    rows: list[dict[str, object]] = []
    for target_date, day in ledger.groupby("target_date", dropna=False):
        picks = pick_rows(day)
        if picks.empty:
            rows.append({"target_date": target_date, "daily_winner": "NO_BET_DAY", "winner_reason": "No model registered a pick."})
            continue
        settled = settled_rows(picks)
        if settled.empty:
            rows.append({"target_date": target_date, "daily_winner": "NO_SETTLED_RESULTS", "winner_reason": "Picks exist but no settled results are available."})
            continue
        comp_rows: list[dict[str, object]] = []
        for exp_id, group in settled.groupby("experiment_id", dropna=False):
            wins, losses = win_loss_counts(group)
            profit = round(float(numeric_series(group.get("profit_units")).fillna(0.0).sum()), 6)
            comp_rows.append(
                {
                    "experiment_id": exp_id,
                    "profit": profit,
                    "hit_rate": as_float(hit_rate_percent(wins, losses), 0.0) or 0.0,
                    "settled": len(group),
                }
            )
        if not comp_rows:
            winner = "NO_SETTLED_RESULTS"
            reason = "No comparable settled rows."
        else:
            comp = pd.DataFrame(comp_rows).sort_values(["profit", "hit_rate", "settled"], ascending=[False, False, False])
            top = comp.iloc[0]
            tied = comp[(comp["profit"] == top["profit"]) & (comp["hit_rate"] == top["hit_rate"])]
            if len(tied) > 1:
                winner = "TIE"
                reason = "Top experiments tied on profit and hit rate."
            else:
                exp_id = normalize_text(top["experiment_id"])
                if exp_id == OFFICIAL_EXPERIMENT_ID:
                    winner = "OFFICIAL_BASELINE"
                elif exp_id == "CANDIDATE_V2_SCHEDULE_ANOMALY":
                    winner = "CANDIDATE_V2"
                elif exp_id == "CANDIDATE_V7_PRICE_DISCIPLINE":
                    winner = "CANDIDATE_V7"
                else:
                    winner = "OTHER_CANDIDATE"
                reason = f"{exp_id} led on profit={top['profit']}, hit_rate={top['hit_rate']}, settled={top['settled']}."
        rows.append({"target_date": target_date, "daily_winner": winner, "winner_reason": reason})
    return pd.DataFrame(rows).sort_values("target_date")


def version_leaders(promotion: pd.DataFrame) -> dict[str, object]:
    if promotion.empty:
        return {
            "official_version": OFFICIAL_EXPERIMENT_ID,
            "current_best_official": OFFICIAL_EXPERIMENT_ID,
            "main_challenger": "INSUFFICIENT_EVIDENCE",
        }
    candidates = promotion[~promotion["experiment_id"].astype(str).eq(OFFICIAL_EXPERIMENT_ID)].copy()
    eligible = candidates[~candidates["promotion_recommendation"].astype(str).isin(["AUDIT_ONLY", "SAMPLE_TOO_SMALL"])]
    promotion_ready = candidates[candidates["promotion_recommendation"].astype(str).eq("PROMOTE_CANDIDATE")]
    current_best = promotion_ready.iloc[0]["experiment_id"] if not promotion_ready.empty else OFFICIAL_EXPERIMENT_ID
    challenger_pool = candidates[candidates["experiment_id"].astype(str).isin(["CANDIDATE_V2_SCHEDULE_ANOMALY", "CANDIDATE_V7_PRICE_DISCIPLINE"])].copy()
    if challenger_pool.empty:
        main_challenger = "INSUFFICIENT_EVIDENCE"
    else:
        challenger_pool["roi_num"] = numeric_series(challenger_pool.get("roi_percent")).fillna(-9999)
        challenger_pool["settled_num"] = numeric_series(challenger_pool.get("settled_picks")).fillna(0)
        main_challenger = challenger_pool.sort_values(["settled_num", "roi_num"], ascending=[False, False]).iloc[0]["experiment_id"]

    def best(metric: str, higher: bool = True) -> str:
        source = candidates.copy()
        source[metric + "_num"] = numeric_series(source.get(metric))
        source = source[source[metric + "_num"].notna()]
        if source.empty:
            return "INSUFFICIENT_EVIDENCE"
        return str(source.sort_values(metric + "_num", ascending=not higher).iloc[0]["experiment_id"])

    stable_source = eligible.copy()
    if stable_source.empty:
        most_stable = "INSUFFICIENT_EVIDENCE"
    else:
        stable_source["drawdown_num"] = numeric_series(stable_source.get("max_drawdown")).fillna(-9999)
        stable_source["pick_days_num"] = numeric_series(stable_source.get("pick_days")).fillna(0)
        most_stable = str(stable_source.sort_values(["drawdown_num", "pick_days_num"], ascending=[False, False]).iloc[0]["experiment_id"])

    return {
        "official_version": OFFICIAL_EXPERIMENT_ID,
        "current_best_official": current_best,
        "main_challenger": main_challenger,
        "best_roi_candidate": best("roi_percent", True),
        "best_hit_rate_candidate": best("hit_rate", True),
        "best_brier_candidate": best("brier_score", False),
        "most_stable_candidate": most_stable,
        "small_sample_candidates": ", ".join(candidates[candidates["promotion_recommendation"].astype(str).eq("SAMPLE_TOO_SMALL")]["experiment_id"].astype(str).tolist()) or "none",
        "audit_only_candidates": ", ".join(candidates[candidates["promotion_recommendation"].astype(str).eq("AUDIT_ONLY")]["experiment_id"].astype(str).tolist()) or "none",
    }


def write_markdown_reports(
    promotion: pd.DataFrame,
    threshold: pd.DataFrame,
    daily_winners: pd.DataFrame,
    alerts: pd.DataFrame,
    leaders: dict[str, object],
    clv_status: str,
    evidence_status: list[str],
    target_date: str | None,
    governance_dir: Path,
    today_dir: Path,
) -> dict[str, Path]:
    governance_dir.mkdir(parents=True, exist_ok=True)
    promotion_lines = [
        "# vSIGMA Promotion Governance Report",
        "",
        "This report is advisory only. It does not promote candidates and does not alter official selection logic.",
        "",
        "## Promotion Recommendations",
        format_markdown_table(
            promotion,
            [
                "experiment_id",
                "current_status",
                "settled_picks",
                "hit_rate",
                "profit_units",
                "roi_percent",
                "brier_score",
                "promotion_recommendation",
                "promotion_reason",
            ],
            max_rows=30,
        ),
        "",
    ]
    promotion_report_path = governance_dir / PROMOTION_REPORT_MD.name
    threshold_report_path = governance_dir / THRESHOLD_REPORT_MD.name
    dashboard_path = governance_dir / GOVERNANCE_DASHBOARD_MD.name

    promotion_report_path.write_text("\n".join(promotion_lines), encoding="utf-8")

    threshold_lines = [
        "# vSIGMA Threshold Governance Report",
        "",
        "This report recommends review actions only. It never edits threshold configuration.",
        "",
        f"- CLV sufficiency: {clv_status}",
        "",
        "## Threshold Recommendations",
        format_markdown_table(
            threshold,
            [
                "market_family",
                "failure_mode",
                "experiment_id",
                "drift_status",
                "clv_direction",
                "settled_rows",
                "hit_rate",
                "profit_units",
                "roi_percent",
                "threshold_recommendation",
                "threshold_reason",
            ],
            max_rows=50,
        ),
        "",
    ]
    threshold_report_path.write_text("\n".join(threshold_lines), encoding="utf-8")

    leaders_df = pd.DataFrame([leaders])
    dashboard_lines = [
        f"# vSIGMA Governance Dashboard{f' - {target_date}' if target_date else ''}",
        "",
        "## Version Leader",
        format_markdown_table(leaders_df),
        "",
        "## Promotion Status",
        format_markdown_table(
            promotion,
            ["experiment_id", "settled_picks", "roi_percent", "brier_score", "promotion_recommendation", "required_next_evidence"],
            max_rows=30,
        ),
        "",
        "## Threshold Alerts",
        format_markdown_table(
            threshold,
            ["market_family", "failure_mode", "experiment_id", "settled_rows", "roi_percent", "clv_direction", "threshold_recommendation"],
            max_rows=30,
        ),
        "",
        "## Drift Alerts",
        format_markdown_table(alerts, max_rows=30),
        "",
        "## Daily Winners",
        format_markdown_table(daily_winners.tail(15), max_rows=15),
        "",
        "## CLV Data Sufficiency",
        clv_status,
        "",
        "## Evidence Status",
        "\n".join(f"- {item}" for item in evidence_status) if evidence_status else "- All primary governance inputs available.",
        "",
        "Official baseline remains unchanged: yes.",
        "",
    ]
    dashboard_path.write_text("\n".join(dashboard_lines), encoding="utf-8")

    paths = {
        "promotion_report": promotion_report_path,
        "threshold_report": threshold_report_path,
        "dashboard": dashboard_path,
    }
    if target_date:
        snapshot_dir = today_dir / target_date
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        snapshot_path = snapshot_dir / dashboard_path.name
        shutil.copy2(dashboard_path, snapshot_path)
        paths["dashboard_snapshot"] = snapshot_path
    return paths


def evidence_status(paths: dict[str, Path]) -> list[str]:
    rows: list[str] = []
    for label, path in paths.items():
        if not path.exists():
            rows.append(f"{label}: missing ({path})")
    return rows


def build_governance(
    processed_dir: Path = PROCESSED_DIR,
    registry_path: Path = REGISTRY_PATH,
    ledger_path: Path | None = None,
    target_date: str | None = None,
    today_dir: Path = TODAY_DIR,
) -> dict[str, Path]:
    ledger_dir = processed_dir / "ledger"
    odds_dir = processed_dir / "odds_snapshots"
    governance_dir = processed_dir / "governance"
    ledger_path = ledger_path or ledger_dir / "vsigma_immutable_daily_pick_ledger.csv"

    inputs = {
        "registry": registry_path,
        "immutable_ledger": ledger_path,
        "performance_summary": ledger_dir / "vsigma_experiment_performance_summary.csv",
        "performance_report": ledger_dir / "vsigma_experiment_performance_report.md",
        "drift_summary": processed_dir / "vsigma_drift_monitor_summary.csv",
        "drift_report": processed_dir / "vsigma_drift_monitor_report.txt",
        "clv_summary": odds_dir / "vsigma_clv_summary.csv",
        "v7_advice": odds_dir / "vsigma_candidate_v7_calibration_advice.csv",
    }
    missing = evidence_status(inputs)

    registry = load_registry(registry_path)
    ledger = stable_read(ledger_path)
    performance = stable_read(inputs["performance_summary"])
    drift = stable_read(inputs["drift_summary"])
    clv = stable_read(inputs["clv_summary"])
    v7_advice = stable_read(inputs["v7_advice"])

    promotion = build_promotion_summary(registry, ledger, performance)
    threshold = build_threshold_summary(ledger, drift, clv, v7_advice)
    daily_winners = daily_winner_summary(ledger)
    alerts = drift_alerts(drift, threshold)
    leaders = version_leaders(promotion)
    clv_status = clv_sufficiency(clv)

    governance_dir.mkdir(parents=True, exist_ok=True)
    promotion.to_csv(governance_dir / PROMOTION_SUMMARY_CSV.name, index=False)
    threshold.to_csv(governance_dir / THRESHOLD_SUMMARY_CSV.name, index=False)

    paths = {
        "promotion_summary": governance_dir / PROMOTION_SUMMARY_CSV.name,
        "threshold_summary": governance_dir / THRESHOLD_SUMMARY_CSV.name,
    }
    paths.update(write_markdown_reports(promotion, threshold, daily_winners, alerts, leaders, clv_status, missing, target_date, governance_dir, today_dir))
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA promotion and threshold governance reports.")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--registry-path", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--ledger-path", type=Path, default=None)
    parser.add_argument("--date", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat() if args.date else None
    paths = build_governance(args.processed_dir, args.registry_path, args.ledger_path, target_date)
    print("\n=== PROMOTION & THRESHOLD GOVERNANCE COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    print(f"official_version: {OFFICIAL_EXPERIMENT_ID}")
    print("official_baseline_unchanged: yes")


if __name__ == "__main__":
    main()
