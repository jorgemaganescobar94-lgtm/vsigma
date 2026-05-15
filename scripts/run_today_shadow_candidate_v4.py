from __future__ import annotations

import argparse
import math
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import (
        add_accuracy_mode_fields,
        add_competition_probability_calibration,
        build_probability_calibration_table,
        select_competition_top,
        sort_accuracy_candidates,
    )
    from build_match_script_forecasts import build_and_write_forecasts, forecast_row
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import (
        add_accuracy_mode_fields,
        add_competition_probability_calibration,
        build_probability_calibration_table,
        select_competition_top,
        sort_accuracy_candidates,
    )
    from scripts.build_match_script_forecasts import build_and_write_forecasts, forecast_row


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_V2_SHORTLIST_CSV = "vsigma_today_candidate_v2_competition_shortlist.csv"
CANDIDATE_V2_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"
HISTORICAL_SOURCE_INPUT = "vsigma_execution_shortlist_historical.csv"

CANDIDATE_V4_SHORTLIST_CSV = "vsigma_today_candidate_v4_competition_shortlist.csv"
CANDIDATE_V4_TOP_CSV = "vsigma_today_candidate_v4_competition_top.csv"
CANDIDATE_V4_REPORT_TXT = "vsigma_today_candidate_v4_competition_report.txt"
CANDIDATE_V4_FORECASTS_CSV = "vsigma_today_candidate_v4_match_script_forecasts.csv"
CANDIDATE_V4_FORECASTS_REPORT = "vsigma_today_candidate_v4_match_script_forecasts_report.txt"
COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv"
COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_report.txt"
SHADOW_RUN_REPORT = "today_shadow_candidate_v4_report.csv"
PRE_JOURNAL = "daily_pre_shadow_candidate_v4.md"

V4_MODE_NAME = "SHADOW_CANDIDATE_V4_O25_LOW_CONVERSION_FIREWALL"
KEEP = "KEEP_OVER_2_5"
DEGRADE = "DEGRADE_TO_OVER_1_5"
REMOVE = "REMOVE_FROM_COMPETITION_TOP"
SECONDARY = "SECONDARY_ONLY"
NOT_APPLIED = "NOT_APPLIED"

FIREWALL_COLUMNS = [
    "over25_low_conversion_firewall_flag",
    "over25_low_conversion_firewall_decision",
    "over25_low_conversion_firewall_reason",
    "over25_low_conversion_confirmation_score",
    "over25_low_conversion_recommended_market",
    "over25_low_conversion_original_market",
    "over25_low_conversion_action",
]

EMPTY_V4_COLUMNS = [
    "date",
    "league",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "market_alt",
    "accuracy_mode_rank",
    "competition_raw_prob",
    "competition_calibrated_prob",
    "accuracy_confidence_score",
    "accuracy_primary_risk",
    "pick_mode",
    *FIREWALL_COLUMNS,
]

COMPARISON_COLUMNS = [
    "comparison_status",
    "fixture_id",
    "fixture",
    "league",
    "baseline_rank",
    "candidate_v2_rank",
    "candidate_v4_rank",
    "baseline_market",
    "candidate_v2_market",
    "candidate_v4_market",
    "candidate_v4_original_market",
    "candidate_v4_firewall_decision",
    "candidate_v4_firewall_score",
    "candidate_v4_firewall_action",
    "baseline_primary_risk",
    "candidate_v2_primary_risk",
    "candidate_v4_primary_risk",
]

NO_BET_EMPTY_V2_REASON = "candidate v2 shortlist empty"


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def empty_v4_frame(source: pd.DataFrame | None = None) -> pd.DataFrame:
    source_cols = list(source.columns) if source is not None and not source.empty else []
    columns = list(dict.fromkeys([*source_cols, *EMPTY_V4_COLUMNS]))
    return pd.DataFrame(columns=columns)


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def compare_key(df: pd.DataFrame, market_sensitive: bool = True) -> pd.Series:
    fixture = df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()
    if not market_sensitive:
        return fixture
    market = df.get("market_primary", pd.Series("", index=df.index)).astype(str).str.strip().str.upper()
    return fixture + "::" + market


def first_available(row: pd.Series, columns: list[str]) -> object:
    for col in columns:
        if col in row.index and pd.notna(row.get(col)) and norm_text(row.get(col)):
            return row.get(col)
    return pd.NA


def score_total(score: object) -> float | None:
    text = norm_text(score)
    match = re.search(r"(\d+)\s*-\s*(\d+)", text)
    if not match:
        return None
    return float(int(match.group(1)) + int(match.group(2)))


def range_bounds(value: object) -> tuple[float | None, float | None]:
    text = norm_text(value)
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)", text)
    if not match:
        return None, None
    return float(match.group(1)), float(match.group(2))


def generated_forecast(row: pd.Series) -> dict[str, object]:
    try:
        return forecast_row(row, 1)
    except Exception:
        total = safe_float(row.get("projected_total_goals"), 0.0)
        likely = norm_text(row.get("likely_scoreline")).split("/")[0].strip()
        return {
            "predicted_score_main": likely,
            "predicted_score_alt": "",
            "predicted_total_goals_range": f"{max(0.4, total - 0.55):.1f}-{min(6.5, total + 0.55):.1f}",
            "predicted_pick_path": norm_text(row.get("pick_execution_rationale")),
            "predicted_state_gravity": "",
        }


def over15_available_clean(row: pd.Series) -> bool:
    if norm_upper(row.get("market_alt")) != "OVER_1_5":
        return False
    alt_prob = safe_float(row.get("alt_model_prob"), 0.0)
    alt_odds = safe_float(row.get("alt_odds_used"), 0.0)
    alt_edge = safe_float(row.get("alt_edge"), -99.0)
    return bool(alt_prob >= 0.80 and alt_odds > 1.0 and alt_edge >= -0.005)


def confirmation_score(row: pd.Series, candidate_v2_top_keys: set[str]) -> tuple[float, list[str]]:
    forecast = generated_forecast(row)
    reasons: list[str] = []
    score = 0.0

    projected_total = safe_float(row.get("projected_total_goals"), 0.0)
    low, high = range_bounds(forecast.get("predicted_total_goals_range"))
    total_floor = low if low is not None else max(0.0, projected_total - 0.55)
    total_ceiling = high if high is not None else projected_total + 0.55
    if projected_total >= 4.2 or total_floor >= 3.7:
        score += 2.0
        reasons.append("FORECAST_TOTAL_XG_HIGH")
    elif projected_total >= 3.6 or total_ceiling >= 4.1:
        score += 1.0
        reasons.append("FORECAST_TOTAL_XG_USABLE")

    main_total = score_total(forecast.get("predicted_score_main"))
    alt_total = score_total(forecast.get("predicted_score_alt"))
    if main_total is not None and main_total >= 3:
        score += 1.0
        reasons.append("MODAL_SCORE_3_PLUS")
    if alt_total is not None and alt_total >= 3:
        score += 1.0
        reasons.append("ALT_SCORE_3_PLUS")
    elif alt_total is not None and math.isclose(alt_total, 2.0):
        score += 0.25
        reasons.append("ALT_SCORE_NARROWLY_SHORT")

    pick_path = norm_upper(forecast.get("predicted_pick_path"))
    if "THREE" in pick_path or "3+" in pick_path or "3 GOAL" in pick_path or "THREE-GOAL" in pick_path:
        score += 1.0
        reasons.append("PICK_PATH_3_GOAL_EXPLICIT")

    calibrated = safe_float(row.get("competition_calibrated_prob"), safe_float(row.get("primary_model_prob"), 0.0))
    if calibrated >= 0.84:
        score += 2.0
        reasons.append("CALIBRATED_PROB_HIGH")
    elif calibrated >= 0.78:
        score += 1.0
        reasons.append("CALIBRATED_PROB_USABLE")

    confidence = safe_float(row.get("accuracy_confidence_score"), 0.0)
    if confidence >= 135.0:
        score += 2.0
        reasons.append("ACCURACY_CONFIDENCE_HIGH")
    elif confidence >= 120.0:
        score += 1.0
        reasons.append("ACCURACY_CONFIDENCE_USABLE")

    source = norm_upper(row.get("execution_shortlist_source"))
    if source == "PREMIUM_CORE":
        score += 1.5
        reasons.append("CORE_PRIORITY")
    elif source in {"PREMIUM_EXTENDED", "STANDARD_FILL"}:
        score -= 1.0
        reasons.append("NOT_CORE_PRIORITY")

    aggression = norm_upper(row.get("odds_line_aggression_flag"))
    if aggression in {"", "NAN", "NONE", "NO_WARNING", "BALANCED", "NORMAL"}:
        score += 0.5
        reasons.append("NO_ODDS_AGGRESSION_WARNING")
    elif aggression:
        score -= 1.5
        reasons.append(f"ODDS_AGGRESSION_{aggression}")

    ladder = norm_upper(row.get("odds_total_ladder_shape"))
    if ladder in {"WIDE_GOALS", "EXPANDED_GOALS", "HIGH_GOALS"}:
        score += 1.5
        reasons.append(f"ODDS_LADDER_{ladder}")
    elif ladder in {"MILD_GOALS", "BALANCED_GOALS"}:
        score += 0.5
        reasons.append(f"ODDS_LADDER_{ladder}")
    elif ladder in {"LOW_GOALS", "COMPRESSED_GOALS"}:
        score -= 1.0
        reasons.append(f"ODDS_LADDER_{ladder}")

    over25_support = norm_upper(row.get("odds_over25_support_flag"))
    if over25_support == "SUPPORTED":
        score += 1.0
        reasons.append("ODDS_OVER25_SUPPORTED")
    elif over25_support in {"WEAK", "UNSUPPORTED"}:
        score -= 1.0
        reasons.append(f"ODDS_OVER25_{over25_support}")

    key = f"{norm_text(row.get('fixture_id'))}::OVER_2_5"
    if key in candidate_v2_top_keys:
        score += 1.0
        reasons.append("CANDIDATE_V2_TOP_AGREES")

    if over15_available_clean(row):
        score -= 1.5
        reasons.append("OVER15_CLEAN_SURVIVAL_AVAILABLE")

    return round(score, 3), reasons


def firewall_decision(row: pd.Series, candidate_v2_top_keys: set[str]) -> dict[str, object]:
    market = norm_upper(row.get("market_primary"))
    risk_blob = " ".join(
        norm_upper(row.get(col))
        for col in ["accuracy_primary_risk", "pick_primary_risk", "pick_failure_mode", "predicted_pick_breaker"]
    )
    original_market = market or pd.NA
    applies = market == "OVER_2_5" and "LOW_CONVERSION" in risk_blob
    if not applies:
        return {
            "over25_low_conversion_firewall_flag": 0,
            "over25_low_conversion_firewall_decision": NOT_APPLIED,
            "over25_low_conversion_firewall_reason": "Firewall applies only to OVER_2_5 with LOW_CONVERSION primary risk.",
            "over25_low_conversion_confirmation_score": 0.0,
            "over25_low_conversion_recommended_market": market or pd.NA,
            "over25_low_conversion_original_market": original_market,
            "over25_low_conversion_action": "NO_ACTION",
        }

    score, reasons = confirmation_score(row, candidate_v2_top_keys)
    clean_o15 = over15_available_clean(row)
    exceptional_threshold = 12.5

    if score >= exceptional_threshold:
        decision = KEEP
        recommended = "OVER_2_5"
        action = "KEEP_PRIMARY_MARKET"
        reason = "Exceptional confirmation cleared the O2.5 low-conversion firewall."
    elif clean_o15:
        decision = DEGRADE
        recommended = "OVER_1_5"
        action = "MARKET_DOWNGRADED_TO_OVER_1_5"
        reason = "Clean O1.5 survival route exists and O2.5 confirmation was below exceptional threshold."
    elif score >= 9.0:
        decision = SECONDARY
        recommended = "OVER_2_5"
        action = "SECONDARY_ONLY"
        reason = "O2.5 confirmation was useful but not strong enough for competition top under LOW_CONVERSION."
    else:
        decision = REMOVE
        recommended = "NO_COMPETITION_PICK"
        action = "REMOVE_FROM_TOP"
        reason = "O2.5 LOW_CONVERSION confirmation was too thin and no clean O1.5 downgrade was available."

    return {
        "over25_low_conversion_firewall_flag": 1,
        "over25_low_conversion_firewall_decision": decision,
        "over25_low_conversion_firewall_reason": reason + " Evidence: " + ";".join(reasons),
        "over25_low_conversion_confirmation_score": score,
        "over25_low_conversion_recommended_market": recommended,
        "over25_low_conversion_original_market": original_market,
        "over25_low_conversion_action": action,
    }


def apply_over25_low_conversion_firewall(
    candidate_v2_shortlist: pd.DataFrame,
    candidate_v2_top: pd.DataFrame | None = None,
    calibration_table: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source = candidate_v2_shortlist.copy()
    if source.empty:
        for col in FIREWALL_COLUMNS:
            source[col] = pd.Series(dtype=object)
        return source, source.copy(), source.copy()

    top = candidate_v2_top if candidate_v2_top is not None else pd.DataFrame()
    top_keys = set(compare_key(top).tolist()) if not top.empty else set()
    decisions = [firewall_decision(row, top_keys) for _, row in source.iterrows()]
    decision_df = pd.DataFrame(decisions, index=source.index)
    out = pd.concat([source, decision_df], axis=1)

    downgrade_mask = out["over25_low_conversion_firewall_decision"].eq(DEGRADE)
    for idx in out[downgrade_mask].index:
        out.loc[idx, "market_primary"] = "OVER_1_5"
        old_alt = out.loc[idx, "market_alt"] if "market_alt" in out.columns else pd.NA
        out.loc[idx, "market_alt"] = out.loc[idx, "over25_low_conversion_original_market"]
        if norm_upper(old_alt) == "OVER_1_5":
            swaps = [
                ("primary_model_prob", "alt_model_prob"),
                ("primary_odds_used", "alt_odds_used"),
                ("primary_implied_prob", "alt_implied_prob"),
                ("primary_edge", "alt_edge"),
            ]
            for primary_col, alt_col in swaps:
                if primary_col in out.columns and alt_col in out.columns:
                    old_primary = out.loc[idx, primary_col]
                    out.loc[idx, primary_col] = out.loc[idx, alt_col]
                    out.loc[idx, alt_col] = old_primary
        for col in ["accuracy_mode_reason", "pick_confirmation_layers"]:
            if col in out.columns:
                prefix = norm_text(out.loc[idx, col])
                out.loc[idx, col] = (prefix + ";O25_LOW_CONVERSION_FIREWALL_DOWNGRADED_TO_O15").strip(";")

    can_recalculate_accuracy = (
        "recent_stats_quality_flag" in out.columns
        and "execution_shortlist_source" in out.columns
        and "final_recommendation" in out.columns
    )
    if can_recalculate_accuracy:
        out = add_accuracy_mode_fields(out)
        out = add_competition_probability_calibration(out, calibration_table if calibration_table is not None else pd.DataFrame())
    else:
        if "accuracy_mode_eligible_flag" not in out.columns:
            out["accuracy_mode_eligible_flag"] = 1
        if "competition_raw_prob" not in out.columns:
            out["competition_raw_prob"] = pd.to_numeric(out.get("primary_model_prob", pd.Series(index=out.index)), errors="coerce")
        if "competition_calibrated_prob" not in out.columns:
            out["competition_calibrated_prob"] = out["competition_raw_prob"]
        if "accuracy_confidence_score" not in out.columns:
            out["accuracy_confidence_score"] = pd.to_numeric(out.get("selection_score", pd.Series(index=out.index)), errors="coerce").fillna(0.0)
        if "accuracy_mode_reason" not in out.columns:
            out["accuracy_mode_reason"] = ""
        if "accuracy_primary_risk" not in out.columns:
            out["accuracy_primary_risk"] = ""
        if "accuracy_mode_bucket" not in out.columns:
            out["accuracy_mode_bucket"] = "ACCURACY_CORE"
        if "execution_shortlist_source" not in out.columns:
            out["execution_shortlist_source"] = "PREMIUM_CORE"
        if "execution_rank" not in out.columns:
            out["execution_rank"] = range(1, len(out) + 1)
    out["pick_mode"] = V4_MODE_NAME

    blocked_mask = out["over25_low_conversion_firewall_decision"].isin({REMOVE, SECONDARY})
    out.loc[blocked_mask, "accuracy_mode_eligible_flag"] = 0
    out.loc[blocked_mask, "accuracy_mode_bucket"] = "ACCURACY_REJECTED"
    out.loc[blocked_mask, "accuracy_mode_reason"] = (
        out.loc[blocked_mask, "accuracy_mode_reason"].map(norm_text)
        + ";O25_LOW_CONVERSION_FIREWALL_NOT_TOP"
    ).str.strip(";")
    out.loc[blocked_mask, "final_recommendation"] = "WATCH"

    shortlist = sort_accuracy_candidates(out[out["accuracy_mode_eligible_flag"].eq(1)].copy())
    if not shortlist.empty:
        shortlist["accuracy_mode_rank"] = range(1, len(shortlist) + 1)
        shortlist["pick_mode"] = V4_MODE_NAME
    top_v4 = select_competition_top(shortlist)
    if not top_v4.empty:
        top_v4["pick_mode"] = V4_MODE_NAME
    return out.reset_index(drop=True), shortlist.reset_index(drop=True), top_v4.reset_index(drop=True)


def build_three_way_comparison(
    baseline: pd.DataFrame,
    candidate_v2: pd.DataFrame,
    candidate_v4: pd.DataFrame,
) -> pd.DataFrame:
    frames = {
        "baseline": baseline.copy(),
        "candidate_v2": candidate_v2.copy(),
        "candidate_v4": candidate_v4.copy(),
    }
    by_fixture: dict[str, dict[str, pd.Series]] = {}
    for label, df in frames.items():
        if df.empty:
            continue
        df["_fixture_key"] = compare_key(df, market_sensitive=False)
        for key, row in df.drop_duplicates("_fixture_key").set_index("_fixture_key").iterrows():
            by_fixture.setdefault(key, {})[label] = row

    rows: list[dict[str, object]] = []
    for key in sorted(by_fixture):
        item = by_fixture[key]
        b = item.get("baseline", pd.Series(dtype=object))
        v2 = item.get("candidate_v2", pd.Series(dtype=object))
        v4 = item.get("candidate_v4", pd.Series(dtype=object))
        source = b if not b.empty else (v2 if not v2.empty else v4)
        status_parts = [
            name.upper()
            for name, row in [("baseline", b), ("candidate_v2", v2), ("candidate_v4", v4)]
            if not row.empty
        ]
        rows.append(
            {
                "comparison_status": "+".join(status_parts),
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["accuracy_mode_rank", "execution_rank"]) if not b.empty else pd.NA,
                "candidate_v2_rank": first_available(v2, ["accuracy_mode_rank", "execution_rank"]) if not v2.empty else pd.NA,
                "candidate_v4_rank": first_available(v4, ["accuracy_mode_rank", "execution_rank"]) if not v4.empty else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if not b.empty else pd.NA,
                "candidate_v2_market": first_available(v2, ["market_primary"]) if not v2.empty else pd.NA,
                "candidate_v4_market": first_available(v4, ["market_primary"]) if not v4.empty else pd.NA,
                "candidate_v4_original_market": first_available(v4, ["over25_low_conversion_original_market"]) if not v4.empty else pd.NA,
                "candidate_v4_firewall_decision": first_available(v4, ["over25_low_conversion_firewall_decision"]) if not v4.empty else pd.NA,
                "candidate_v4_firewall_score": first_available(v4, ["over25_low_conversion_confirmation_score"]) if not v4.empty else pd.NA,
                "candidate_v4_firewall_action": first_available(v4, ["over25_low_conversion_action"]) if not v4.empty else pd.NA,
                "baseline_primary_risk": first_available(b, ["accuracy_primary_risk", "pick_primary_risk"]) if not b.empty else pd.NA,
                "candidate_v2_primary_risk": first_available(v2, ["accuracy_primary_risk", "pick_primary_risk"]) if not v2.empty else pd.NA,
                "candidate_v4_primary_risk": first_available(v4, ["accuracy_primary_risk", "pick_primary_risk"]) if not v4.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows, columns=COMPARISON_COLUMNS)


def write_no_bet_v4_report(path: Path, reason: str, baseline: pd.DataFrame, candidate_v2: pd.DataFrame) -> None:
    lines = [
        "vSIGMA SHADOW CANDIDATE V4",
        "",
        "CANDIDATE_V4_NO_BET",
        f"reason: {reason}",
        "",
        "Layer: candidate v2 signals + O2.5 Low Conversion Firewall.",
        "Status: experimental shadow; official baseline and candidate v2 outputs are not replaced.",
        "",
        f"Baseline official picks: {len(baseline)}",
        f"Candidate v2 shadow picks: {len(candidate_v2)}",
        "Candidate v4 competition shortlist rows: 0",
        "Candidate v4 competition top rows: 0",
        "",
        "## O2.5 Low Conversion Firewall",
        "",
        "No OVER_2_5 + LOW_CONVERSION rows were checked because candidate v2 produced no competition shortlist.",
        "",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_v4_report(path: Path, all_rows: pd.DataFrame, shortlist: pd.DataFrame, top: pd.DataFrame) -> None:
    checked = all_rows[all_rows.get("over25_low_conversion_firewall_flag", 0).eq(1)].copy()
    lines = [
        "vSIGMA SHADOW CANDIDATE V4",
        "",
        "Layer: candidate v2 signals + O2.5 Low Conversion Firewall.",
        "Status: experimental shadow; official baseline and candidate v2 outputs are not replaced.",
        "",
        f"Candidate v2 input rows: {len(all_rows)}",
        f"Candidate v4 competition shortlist rows: {len(shortlist)}",
        f"Candidate v4 competition top rows: {len(top)}",
        "",
        "## O2.5 Low Conversion Firewall",
        "",
    ]
    if checked.empty:
        lines.append("No OVER_2_5 + LOW_CONVERSION rows were checked.")
    else:
        cols = [
            "fixture_id",
            "home_team",
            "away_team",
            "over25_low_conversion_original_market",
            "over25_low_conversion_recommended_market",
            "over25_low_conversion_firewall_decision",
            "over25_low_conversion_confirmation_score",
            "over25_low_conversion_action",
            "over25_low_conversion_firewall_reason",
        ]
        lines.append(checked[[c for c in cols if c in checked.columns]].to_string(index=False))
    lines.extend(["", "## Candidate v4 Top", ""])
    if top.empty:
        lines.append("No v4 competition top picks survived.")
    else:
        cols = [
            "accuracy_mode_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "competition_calibrated_prob",
            "accuracy_confidence_score",
            "over25_low_conversion_firewall_decision",
            "over25_low_conversion_confirmation_score",
        ]
        lines.append(top[[c for c in cols if c in top.columns]].to_string(index=False))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_comparison_report(path: Path, baseline: pd.DataFrame, v2: pd.DataFrame, v4: pd.DataFrame, comparison: pd.DataFrame) -> None:
    overlap_all = int(comparison["comparison_status"].eq("BASELINE+CANDIDATE_V2+CANDIDATE_V4").sum()) if not comparison.empty else 0
    adjusted = int(
        v4.get("over25_low_conversion_firewall_decision", pd.Series(dtype=object)).isin([DEGRADE, REMOVE, SECONDARY]).sum()
    ) if not v4.empty else 0
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 VS CANDIDATE V4",
        "",
        "Baseline: official frozen Competition Accuracy Mode + Probability Calibration.",
        "Candidate v2: shadow schedule-strength + anomaly-cleaning layer.",
        "Candidate v4: candidate v2 + O2.5 Low Conversion Firewall.",
        "",
        f"Baseline official picks: {len(baseline)}",
        f"Candidate v2 shadow picks: {len(v2)}",
        f"Candidate v4 shadow picks: {len(v4)}",
        f"Three-way fixture overlap: {overlap_all}",
        f"Candidate v4 adjusted/blocked O2.5 rows in top: {adjusted}",
        "",
        "Side-by-side picks",
        comparison.to_string(index=False) if not comparison.empty else "No compared rows.",
        "",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_firewall_section(all_rows: pd.DataFrame) -> list[str]:
    checked = all_rows[all_rows.get("over25_low_conversion_firewall_flag", 0).eq(1)].copy()
    lines = ["## O2.5 Low Conversion Firewall", ""]
    if checked.empty:
        lines.extend(["- Checked: 0", ""])
        return lines
    for decision in [KEEP, DEGRADE, SECONDARY, REMOVE]:
        subset = checked[checked["over25_low_conversion_firewall_decision"].eq(decision)]
        lines.append(f"- {decision}: {len(subset)}")
        for _, row in subset.iterrows():
            lines.append(
                f"  - {row.get('home_team')} vs {row.get('away_team')}: "
                f"{row.get('over25_low_conversion_original_market')} -> "
                f"{row.get('over25_low_conversion_recommended_market')} "
                f"(score {row.get('over25_low_conversion_confirmation_score')})"
            )
    lines.append("")
    return lines


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(norm_text(row.get(col)).replace("|", "\\|") for col in cols) + " |")
    return "\n".join(lines)


def write_pre_journal(path: Path, match_date: str, timezone_name: str, top: pd.DataFrame, comparison: pd.DataFrame, all_rows: pd.DataFrame) -> None:
    lines = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v4 Pre",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_name}",
        "- Mode: SHADOW / experimental / non-official",
        "- Layer: candidate v2 + O2.5 Low Conversion Firewall",
        "",
    ]
    lines.extend(markdown_firewall_section(all_rows))
    lines.extend(["## Candidate v4 Shadow Top", ""])
    if top.empty:
        lines.append("_No top picks survived._")
    else:
        cols = [
            "accuracy_mode_rank",
            "home_team",
            "away_team",
            "market_primary",
            "over25_low_conversion_firewall_decision",
            "over25_low_conversion_confirmation_score",
        ]
        lines.append(markdown_table(top[[c for c in cols if c in top.columns]]))
    lines.extend(["", "## Baseline vs Candidate v2 vs Candidate v4", ""])
    lines.append(markdown_table(comparison) if not comparison.empty else "_No comparison rows._")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_no_bet_pre_journal(
    path: Path,
    match_date: str,
    timezone_name: str,
    reason: str,
    comparison: pd.DataFrame,
) -> None:
    lines = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v4 Pre",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_name}",
        "- Mode: SHADOW / experimental / non-official",
        "- Layer: candidate v2 + O2.5 Low Conversion Firewall",
        "",
        "## Candidate v4 Decision",
        "",
        "- CANDIDATE_V4_NO_BET",
        f"- reason: {reason}",
        "",
        "## O2.5 Low Conversion Firewall",
        "",
        "- Checked: 0",
        "",
        "## Candidate v4 Shadow Top",
        "",
        "_No top picks survived._",
        "",
        "## Baseline vs Candidate v2 vs Candidate v4",
        "",
        markdown_table(comparison) if not comparison.empty else "_No comparison rows._",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_shadow_run_report(
    path: Path,
    match_date: str,
    timezone_name: str,
    baseline_top: pd.DataFrame,
    candidate_v2_top: pd.DataFrame,
    candidate_v4_top: pd.DataFrame,
    checked: pd.DataFrame,
    status: str = "OK",
    reason: str = "",
) -> None:
    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "mode": V4_MODE_NAME,
                "status": status,
                "reason": reason,
                "baseline_competition_rows": int(len(baseline_top)),
                "candidate_v2_competition_rows": int(len(candidate_v2_top)),
                "candidate_v4_competition_rows": int(len(candidate_v4_top)),
                "firewall_checked_rows": int(len(checked)),
                "firewall_kept_rows": int(checked["over25_low_conversion_firewall_decision"].eq(KEEP).sum()) if not checked.empty else 0,
                "firewall_downgraded_rows": int(checked["over25_low_conversion_firewall_decision"].eq(DEGRADE).sum()) if not checked.empty else 0,
                "firewall_secondary_rows": int(checked["over25_low_conversion_firewall_decision"].eq(SECONDARY).sum()) if not checked.empty else 0,
                "firewall_removed_rows": int(checked["over25_low_conversion_firewall_decision"].eq(REMOVE).sum()) if not checked.empty else 0,
                "official_baseline_preserved": 1,
                "candidate_v2_preserved": 1,
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(path, index=False)


def write_empty_candidate_v4_outputs(
    processed_dir: Path,
    snapshot_dir: Path,
    match_date: str,
    timezone_name: str,
    baseline_top: pd.DataFrame,
    candidate_v2_top: pd.DataFrame,
    reason: str,
) -> dict[str, Path]:
    shortlist = empty_v4_frame(candidate_v2_top)
    top = empty_v4_frame(candidate_v2_top)
    all_rows = empty_v4_frame(candidate_v2_top)

    shortlist_path = processed_dir / CANDIDATE_V4_SHORTLIST_CSV
    top_path = processed_dir / CANDIDATE_V4_TOP_CSV
    report_path = processed_dir / CANDIDATE_V4_REPORT_TXT
    comparison_path = processed_dir / COMPARISON_CSV
    comparison_report_path = processed_dir / COMPARISON_REPORT
    shadow_report_path = processed_dir / SHADOW_RUN_REPORT

    shortlist.to_csv(shortlist_path, index=False)
    top.to_csv(top_path, index=False)
    write_no_bet_v4_report(report_path, reason, baseline_top, candidate_v2_top)

    build_and_write_forecasts(
        processed_dir=processed_dir,
        input_filename=CANDIDATE_V4_TOP_CSV,
        output_filename=CANDIDATE_V4_FORECASTS_CSV,
        report_filename=CANDIDATE_V4_FORECASTS_REPORT,
        source_label="shadow candidate v4 competition top",
        snapshot_date=match_date,
    )

    comparison = build_three_way_comparison(baseline_top, candidate_v2_top, top)
    comparison.to_csv(comparison_path, index=False)
    write_comparison_report(comparison_report_path, baseline_top, candidate_v2_top, top, comparison)
    write_shadow_run_report(
        shadow_report_path,
        match_date,
        timezone_name,
        baseline_top,
        candidate_v2_top,
        top,
        pd.DataFrame(),
        status="CANDIDATE_V4_NO_BET",
        reason=reason,
    )

    for path in [shortlist_path, top_path, report_path, comparison_path, comparison_report_path, shadow_report_path]:
        copy_if_exists(path, snapshot_dir)
    copy_if_exists(processed_dir / CANDIDATE_V4_FORECASTS_CSV, snapshot_dir)
    copy_if_exists(processed_dir / CANDIDATE_V4_FORECASTS_REPORT, snapshot_dir)

    pre_journal_path = snapshot_dir / PRE_JOURNAL
    write_no_bet_pre_journal(pre_journal_path, match_date, timezone_name, reason, comparison)

    return {
        "candidate_v4_shortlist": shortlist_path,
        "candidate_v4_top": top_path,
        "candidate_v4_report": report_path,
        "candidate_v4_forecasts": processed_dir / CANDIDATE_V4_FORECASTS_CSV,
        "candidate_v4_forecasts_report": processed_dir / CANDIDATE_V4_FORECASTS_REPORT,
        "comparison_csv": comparison_path,
        "comparison_report": comparison_report_path,
        "shadow_run_report": shadow_report_path,
        "shadow_pre_journal": pre_journal_path,
    }


def build_candidate_v4_outputs(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    match_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
) -> dict[str, Path]:
    match_date = match_date or date.today().isoformat()
    snapshot_dir = today_dir / match_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    baseline_top = read_csv_optional(processed_dir / BASELINE_TOP_CSV)
    candidate_v2_shortlist = read_csv_optional(processed_dir / CANDIDATE_V2_SHORTLIST_CSV)
    candidate_v2_top = read_csv_optional(processed_dir / CANDIDATE_V2_TOP_CSV)
    if candidate_v2_shortlist.empty:
        return write_empty_candidate_v4_outputs(
            processed_dir,
            snapshot_dir,
            match_date,
            timezone_name,
            baseline_top,
            candidate_v2_top,
            NO_BET_EMPTY_V2_REASON,
        )

    historical_path = processed_dir / HISTORICAL_SOURCE_INPUT
    calibration_table = (
        build_probability_calibration_table(pd.read_csv(historical_path))
        if historical_path.exists()
        else pd.DataFrame()
    )
    all_rows, shortlist, top = apply_over25_low_conversion_firewall(
        candidate_v2_shortlist,
        candidate_v2_top,
        calibration_table,
    )

    shortlist_path = processed_dir / CANDIDATE_V4_SHORTLIST_CSV
    top_path = processed_dir / CANDIDATE_V4_TOP_CSV
    report_path = processed_dir / CANDIDATE_V4_REPORT_TXT
    comparison_path = processed_dir / COMPARISON_CSV
    comparison_report_path = processed_dir / COMPARISON_REPORT
    shadow_report_path = processed_dir / SHADOW_RUN_REPORT

    shortlist.to_csv(shortlist_path, index=False)
    top.to_csv(top_path, index=False)
    write_v4_report(report_path, all_rows, shortlist, top)
    build_and_write_forecasts(
        processed_dir=processed_dir,
        input_filename=CANDIDATE_V4_TOP_CSV,
        output_filename=CANDIDATE_V4_FORECASTS_CSV,
        report_filename=CANDIDATE_V4_FORECASTS_REPORT,
        source_label="shadow candidate v4 competition top",
        snapshot_date=match_date,
    )

    comparison = build_three_way_comparison(baseline_top, candidate_v2_top, top)
    comparison.to_csv(comparison_path, index=False)
    write_comparison_report(comparison_report_path, baseline_top, candidate_v2_top, top, comparison)

    checked = all_rows[all_rows.get("over25_low_conversion_firewall_flag", 0).eq(1)].copy()
    write_shadow_run_report(
        shadow_report_path,
        match_date,
        timezone_name,
        baseline_top,
        candidate_v2_top,
        top,
        checked,
    )

    for path in [shortlist_path, top_path, report_path, comparison_path, comparison_report_path, shadow_report_path]:
        copy_if_exists(path, snapshot_dir)
    copy_if_exists(processed_dir / CANDIDATE_V4_FORECASTS_CSV, snapshot_dir)
    copy_if_exists(processed_dir / CANDIDATE_V4_FORECASTS_REPORT, snapshot_dir)

    pre_journal_path = snapshot_dir / PRE_JOURNAL
    write_pre_journal(pre_journal_path, match_date, timezone_name, top, comparison, all_rows)

    return {
        "candidate_v4_shortlist": shortlist_path,
        "candidate_v4_top": top_path,
        "candidate_v4_report": report_path,
        "candidate_v4_forecasts": processed_dir / CANDIDATE_V4_FORECASTS_CSV,
        "candidate_v4_forecasts_report": processed_dir / CANDIDATE_V4_FORECASTS_REPORT,
        "comparison_csv": comparison_path,
        "comparison_report": comparison_report_path,
        "shadow_run_report": shadow_report_path,
        "shadow_pre_journal": pre_journal_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build candidate v4 shadow outputs from candidate v2 plus the O2.5 low-conversion firewall."
    )
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = build_candidate_v4_outputs(PROCESSED_DIR, TODAY_DIR, match_date, args.timezone)
    print("\n=== TODAY SHADOW CANDIDATE V4 COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    print("Official baseline and candidate v2 files preserved; v4 wrote separate outputs only.")


if __name__ == "__main__":
    main()
