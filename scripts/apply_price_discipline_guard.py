from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from daily_hardening import split_fresh_stale_rows
except ModuleNotFoundError:
    from scripts.daily_hardening import split_fresh_stale_rows


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "vsigma_price_discipline_config.json"
DRIFT_SUMMARY_PATH = ROOT / "data" / "processed" / "vsigma_drift_monitor_summary.csv"
PRELOCK_COMPARISON_PATH = ROOT / "data" / "processed" / "vsigma_today_prelock_comparison.csv"

PRICE_OK = "PRICE_OK"
PRICE_THIN_SECONDARY_ONLY = "PRICE_THIN_SECONDARY_ONLY"
PRICE_REJECTED = "PRICE_REJECTED"
PRICE_NEEDS_PRELOCK_CONFIRMATION = "PRICE_NEEDS_PRELOCK_CONFIRMATION"
PRICE_DRIFT_PENALIZED = "PRICE_DRIFT_PENALIZED"
PRICE_NO_ODDS_UNCERTAIN = "PRICE_NO_ODDS_UNCERTAIN"

V7_WAITING_FOR_PRELOCK = "V7_WAITING_FOR_PRELOCK"
V7_PRELOCK_CONFIRMED = "V7_PRELOCK_CONFIRMED"
V7_PRELOCK_REJECTED = "V7_PRELOCK_REJECTED"
V7_PRELOCK_UNAVAILABLE = "V7_PRELOCK_UNAVAILABLE"
V7_PRICE_REJECTED = "V7_PRICE_REJECTED"
V7_SECONDARY_ONLY = "V7_SECONDARY_ONLY"

CLV_POSITIVE = "CLV_POSITIVE"
CLV_NEGATIVE = "CLV_NEGATIVE"
CLV_FLAT = "CLV_FLAT"
CLV_UNAVAILABLE = "CLV_UNAVAILABLE"

PRICE_DISCIPLINE_COLUMNS = [
    "price_discipline_flag",
    "price_discipline_decision",
    "price_discipline_reason",
    "price_discipline_min_edge_required",
    "price_discipline_actual_edge",
    "price_discipline_edge_surplus",
    "price_discipline_market_family",
    "price_discipline_failure_mode_penalty",
    "price_discipline_drift_penalty",
    "price_discipline_final_adjustment",
    "price_discipline_execution_allowed_flag",
    "price_discipline_drift_status",
    "odds_pre_price",
    "odds_prelock_price",
    "odds_close_proxy_price",
    "clv_available_flag",
    "clv_direction",
    "clv_delta",
    "clv_interpretation",
    "candidate_v7_prelock_status",
    "candidate_v7_execution_status",
    "candidate_v7_execution_allowed_flag",
]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def safe_float(value: object, default: float | None = None) -> float | None:
    try:
        if pd.isna(value) or norm_text(value) == "":
            return default
        return float(value)
    except Exception:
        return default


def load_price_discipline_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def market_family(value: object) -> str:
    market = norm_upper(value)
    if market in {"HOME_WIN", "AWAY_WIN"}:
        return "WIN"
    return market or "UNKNOWN"


def failure_mode(row: pd.Series) -> str:
    blob = " ".join(
        norm_upper(row.get(col))
        for col in ["accuracy_primary_risk", "pick_primary_risk", "pick_failure_mode", "predicted_pick_breaker"]
    )
    if "LOW_CONVERSION" in blob:
        return "LOW_CONVERSION"
    if "BTTS_BREAK" in blob:
        return "BTTS_BREAK"
    if "DRAW_LIVE" in blob:
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


def select_rule(config: dict[str, Any], market: str, failure: str) -> dict[str, Any]:
    default = dict(config.get("default_rule", {}))
    for rule in config.get("rules", []):
        if norm_upper(rule.get("market_family")) == market and norm_upper(rule.get("failure_mode")) == failure:
            merged = dict(default)
            merged.update(rule)
            return merged
    for rule in config.get("rules", []):
        if norm_upper(rule.get("market_family")) == market and norm_upper(rule.get("failure_mode")) == "ANY":
            merged = dict(default)
            merged.update(rule)
            return merged
    return default


def prelock_lookup(prelock: pd.DataFrame, target_date: str | None = None) -> dict[tuple[str, str], pd.Series]:
    lookup: dict[tuple[str, str], pd.Series] = {}
    if prelock.empty:
        return lookup
    if target_date:
        prelock, _stale = split_fresh_stale_rows(prelock, target_date, include_target_date=True)
        if prelock.empty:
            return lookup
    for _, row in prelock.iterrows():
        key = (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")))
        lookup[key] = row
    return lookup


def clv_fields(row: pd.Series, prelock_row: pd.Series | None) -> dict[str, object]:
    pre = safe_float(row.get("primary_odds_used"), None)
    prelock = safe_float(prelock_row.get("primary_odds_used"), None) if prelock_row is not None else None
    if pre is None or pre <= 1.0 or prelock is None or prelock <= 1.0:
        return {
            "odds_pre_price": pre if pre is not None else pd.NA,
            "odds_prelock_price": prelock if prelock is not None else pd.NA,
            "odds_close_proxy_price": prelock if prelock is not None else pd.NA,
            "clv_available_flag": 0,
            "clv_direction": CLV_UNAVAILABLE,
            "clv_delta": pd.NA,
            "clv_interpretation": "CLV_UNAVAILABLE: no true closing odds; pre-lock close proxy unavailable.",
        }
    delta = round(prelock - pre, 6)
    if delta < -0.001:
        direction = CLV_POSITIVE
    elif delta > 0.001:
        direction = CLV_NEGATIVE
    else:
        direction = CLV_FLAT
    return {
        "odds_pre_price": pre,
        "odds_prelock_price": prelock,
        "odds_close_proxy_price": prelock,
        "clv_available_flag": 1,
        "clv_direction": direction,
        "clv_delta": delta,
        "clv_interpretation": f"{direction}: pre-lock price used as close proxy, not true close.",
    }


def actual_edge(row: pd.Series) -> float | None:
    edge = safe_float(row.get("primary_edge"), None)
    if edge is not None:
        return edge
    prob = safe_float(row.get("primary_model_prob"), None)
    implied = safe_float(row.get("primary_implied_prob"), None)
    if prob is not None and implied is not None:
        return prob - implied
    odds = safe_float(row.get("primary_odds_used"), None)
    if prob is not None and odds is not None and odds > 1.0:
        return prob - (1.0 / odds)
    return None


def prelock_confirmed(prelock_row: pd.Series | None) -> bool:
    if prelock_row is None:
        return False
    decision = norm_upper(prelock_row.get("prelock_decision"))
    return decision in {"PRELOCK_CONFIRMED", "PRELOCK_NO_CHANGE"}


def prelock_rejected(prelock_row: pd.Series | None) -> bool:
    if prelock_row is None:
        return False
    decision = norm_upper(prelock_row.get("prelock_decision"))
    return decision in {"PRELOCK_REMOVED", "PRELOCK_DOWNGRADED"}


def prelock_unavailable(prelock_row: pd.Series | None) -> bool:
    if prelock_row is None:
        return False
    decision = norm_upper(prelock_row.get("prelock_decision"))
    status = norm_upper(prelock_row.get("prelock_status"))
    return decision == "PRELOCK_NOT_AVAILABLE" or status == "OUTSIDE_PRELOCK_WINDOW"


def v7_state_from_price_decision(decision: str, allowed: int, prelock_row: pd.Series | None, requires_prelock: bool) -> tuple[str, str, int]:
    decision = norm_upper(decision)
    if requires_prelock:
        if prelock_confirmed(prelock_row):
            return V7_PRELOCK_CONFIRMED, V7_PRELOCK_CONFIRMED, allowed
        if prelock_rejected(prelock_row):
            return V7_PRELOCK_REJECTED, V7_PRELOCK_REJECTED, 0
        if prelock_unavailable(prelock_row):
            return V7_PRELOCK_UNAVAILABLE, V7_PRELOCK_UNAVAILABLE, 0
        return V7_WAITING_FOR_PRELOCK, V7_WAITING_FOR_PRELOCK, 0
    if decision in {PRICE_REJECTED, PRICE_DRIFT_PENALIZED, PRICE_NO_ODDS_UNCERTAIN}:
        return "", V7_PRICE_REJECTED, 0
    if decision == PRICE_THIN_SECONDARY_ONLY:
        return "", V7_SECONDARY_ONLY, 0
    return "", decision, allowed


def classify_price_row(row: pd.Series, config: dict[str, Any], drift_by_pattern: dict[str, str], prelock_by_key: dict[tuple[str, str], pd.Series]) -> dict[str, object]:
    market = market_family(row.get("market_primary"))
    failure = failure_mode(row)
    rule = select_rule(config, market, failure)
    edge = actual_edge(row)
    prelock_row = prelock_by_key.get((norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary"))))
    clv = clv_fields(row, prelock_row)
    drift_status = drift_by_pattern.get(pattern_name(market, failure), "UNKNOWN")
    penalties = rule.get("drift_status_penalty", {}) or {}
    default_penalties = config.get("default_rule", {}).get("drift_status_penalty", {}) or {}
    drift_penalty = safe_float(penalties.get(drift_status, default_penalties.get(drift_status, 0.0)), 0.0) or 0.0
    base_min_edge = safe_float(rule.get("min_edge"), 0.055) or 0.055
    min_prob = safe_float(rule.get("min_calibrated_probability"), 0.0) or 0.0
    actual_prob = safe_float(row.get("competition_calibrated_prob"), safe_float(row.get("primary_model_prob"), 0.0)) or 0.0
    failure_penalty = max(0.0, base_min_edge - (safe_float(config.get("default_rule", {}).get("min_edge"), 0.055) or 0.055))
    final_adjustment = drift_penalty
    min_required = round(base_min_edge + drift_penalty, 6)
    requires_prelock = drift_status == "WATCH_PATTERN" and bool(rule.get("require_prelock_if_watch_pattern", False))

    if edge is None:
        decision = PRICE_NO_ODDS_UNCERTAIN
        allowed = 0
        reason = "No usable odds/edge available; missing price is execution uncertainty."
        surplus = pd.NA
    else:
        surplus_value = edge - min_required
        surplus = round(surplus_value, 6)
        exceptional = surplus_value >= 0.04 and actual_prob >= min_prob + 0.02
        if drift_status == "NEEDS_RECALIBRATION" and not exceptional:
            decision = PRICE_REJECTED
            allowed = 0
            reason = "Drift status needs recalibration and edge is not exceptional."
        elif drift_status == "ACTIVE_DRIFT" and not exceptional:
            decision = PRICE_DRIFT_PENALIZED
            allowed = 0
            reason = "Active drift requires secondary-only handling unless edge is exceptional."
        elif actual_prob < min_prob:
            decision = PRICE_REJECTED
            allowed = 0
            reason = f"Calibrated probability {actual_prob:.3f} below required {min_prob:.3f}."
        elif surplus_value < 0:
            decision = PRICE_THIN_SECONDARY_ONLY if bool(rule.get("allow_secondary_only", True)) else PRICE_REJECTED
            allowed = 0
            reason = f"Actual edge {edge:.3f} below required edge {min_required:.3f}."
        elif requires_prelock and prelock_rejected(prelock_row):
            decision = PRICE_REJECTED
            allowed = 0
            reason = "Fresh pre-lock review found a contradiction; v7 execution rejected."
        elif requires_prelock and prelock_unavailable(prelock_row):
            decision = PRICE_NEEDS_PRELOCK_CONFIRMATION
            allowed = 0
            reason = "Fresh pre-lock review is unavailable; v7 cannot confirm execution."
        elif requires_prelock and not prelock_confirmed(prelock_row):
            decision = PRICE_NEEDS_PRELOCK_CONFIRMATION
            allowed = 0
            reason = "Watch-pattern drift requires explicit pre-lock confirmation before execution."
        elif drift_status in {"WATCH_PATTERN", "ACTIVE_DRIFT"} and drift_penalty > 0:
            decision = PRICE_DRIFT_PENALIZED
            allowed = 1
            reason = f"Price cleared drift-adjusted edge with {drift_status} penalty."
        else:
            decision = PRICE_OK
            allowed = 1
            reason = "Price cleared configured minimum edge and probability requirements."

    v7_prelock_status, v7_execution_status, v7_allowed = v7_state_from_price_decision(decision, allowed, prelock_row, requires_prelock)
    return {
        "price_discipline_flag": 1,
        "price_discipline_decision": decision,
        "price_discipline_reason": reason,
        "price_discipline_min_edge_required": min_required,
        "price_discipline_actual_edge": round(edge, 6) if edge is not None else pd.NA,
        "price_discipline_edge_surplus": surplus,
        "price_discipline_market_family": market,
        "price_discipline_failure_mode_penalty": round(failure_penalty, 6),
        "price_discipline_drift_penalty": round(drift_penalty, 6),
        "price_discipline_final_adjustment": round(final_adjustment, 6),
        "price_discipline_execution_allowed_flag": allowed,
        "price_discipline_drift_status": drift_status,
        "candidate_v7_prelock_status": v7_prelock_status,
        "candidate_v7_execution_status": v7_execution_status,
        "candidate_v7_execution_allowed_flag": v7_allowed,
        **clv,
    }


def empty_price_frame(source: pd.DataFrame | None = None) -> pd.DataFrame:
    source_cols = list(source.columns) if source is not None and not source.empty else []
    return pd.DataFrame(columns=list(dict.fromkeys([*source_cols, *PRICE_DISCIPLINE_COLUMNS])))


def apply_price_discipline_guard(
    candidate_v2_rows: pd.DataFrame,
    *,
    config_path: Path = CONFIG_PATH,
    drift_path: Path = DRIFT_SUMMARY_PATH,
    prelock_path: Path = PRELOCK_COMPARISON_PATH,
    target_date: str | None = None,
) -> pd.DataFrame:
    source = candidate_v2_rows.copy()
    if source.empty:
        return empty_price_frame(source)
    config = load_price_discipline_config(config_path)
    drift_by_pattern = drift_lookup(read_csv_optional(drift_path))
    prelock_by_key = prelock_lookup(read_csv_optional(prelock_path), target_date=target_date)
    decisions = [classify_price_row(row, config, drift_by_pattern, prelock_by_key) for _, row in source.iterrows()]
    decision_df = pd.DataFrame(decisions, index=source.index)
    out = pd.concat([source, decision_df], axis=1)
    out["pick_mode"] = "SHADOW_CANDIDATE_V7_PRICE_DISCIPLINE_CLV_DRIFT_GUARD"
    return out.reset_index(drop=True)
