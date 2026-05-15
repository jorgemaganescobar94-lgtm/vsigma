from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

try:
    from pick_explanations import add_pick_explanations, failure_mode
except ModuleNotFoundError:
    from scripts.pick_explanations import add_pick_explanations, failure_mode


DEFAULT_PROCESSED_DIR = Path("data/processed")

COMPETITION_MODE_NAME = "COMPETITION_ACCURACY_MODE"

TODAY_SHORTLIST_INPUT = "vsigma_today_execution_shortlist.csv"
COMPETITION_SHORTLIST_OUTPUT = "vsigma_today_competition_shortlist.csv"
COMPETITION_TOP_OUTPUT = "vsigma_today_competition_top.csv"
COMPETITION_REPORT_OUTPUT = "vsigma_today_competition_report.txt"

HISTORICAL_SOURCE_INPUT = "vsigma_execution_shortlist_historical.csv"
PROBABILITY_SUMMARY_OUTPUT = "vsigma_probability_evaluation_summary.csv"
PROBABILITY_REPORT_OUTPUT = "vsigma_probability_evaluation_report.txt"
PROBABILITY_CALIBRATION_TABLE_OUTPUT = "vsigma_probability_calibration_table.csv"
PROBABILITY_CALIBRATION_REPORT_OUTPUT = "vsigma_probability_calibration_report.txt"

ACCURACY_COLUMNS = [
    "accuracy_mode_eligible_flag",
    "accuracy_confidence_score",
    "accuracy_mode_reason",
    "accuracy_primary_risk",
    "accuracy_mode_bucket",
    "accuracy_mode_rank",
]

CALIBRATED_PROBABILITY_COLUMNS = [
    "competition_raw_prob",
    "competition_calibrated_prob",
    "competition_prob_calibration_bucket",
    "competition_prob_calibration_reason",
    "competition_prob_shrinkage_applied_flag",
]

ACTIONABLE_RECOMMENDATIONS = {"BET"}
BLOCKED_MARKET_FIT_STATUSES = {"MARKET_FIT_DOWNGRADED", "MARKET_FIT_BLOCKED"}
STABLE_MARKETS = {"OVER_1_5", "UNDER_3_5"}
CONDITIONAL_STABLE_MARKETS = {"OVER_2_5"}
FRAGILE_SIDE_MARKETS = {"HOME_WIN", "AWAY_WIN"}
BTTS_MARKETS = {"BTTS_YES", "BTTS_NO"}

MAX_COMPETITION_TOP_ROWS = 3
MAX_TOP_PER_LEAGUE = 1
MAX_TOP_PER_MARKET = 2
MIN_CORE_SCORE = 86.0
MIN_EXTENDED_SCORE = 96.0
MIN_STANDARD_SCORE = 104.0

GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}
DECIDED_RESULTS = {"WIN", "LOSS"}
MIN_CALIBRATED_PROB = 0.55
MAX_CALIBRATED_PROB = 0.95

CALIBRATION_GROUP_SPECS = [
    {
        "group_type": "MARKET_BUCKET",
        "group_cols": ["market_primary", "accuracy_mode_bucket"],
        "min_sample_size": 3,
        "max_down_adjustment": 0.08,
        "max_up_adjustment": 0.04,
    },
    {
        "group_type": "MARKET",
        "group_cols": ["market_primary"],
        "min_sample_size": 4,
        "max_down_adjustment": 0.08,
        "max_up_adjustment": 0.03,
    },
    {
        "group_type": "BUCKET",
        "group_cols": ["accuracy_mode_bucket"],
        "min_sample_size": 4,
        "max_down_adjustment": 0.06,
        "max_up_adjustment": 0.03,
    },
    {
        "group_type": "GLOBAL",
        "group_cols": [],
        "min_sample_size": 6,
        "max_down_adjustment": 0.05,
        "max_up_adjustment": 0.02,
    },
]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def bool_flag(value: object) -> bool:
    text = norm_text(value)
    if text in {"1", "TRUE", "YES", "Y"}:
        return True
    if text in {"0", "FALSE", "NO", "N", ""}:
        return False
    return bool(safe_float(value, 0.0))


def clamp_prob(value: object) -> float:
    return max(MIN_CALIBRATED_PROB, min(MAX_CALIBRATED_PROB, safe_float(value, 0.0)))


def competition_eligible_mask(df: pd.DataFrame) -> pd.Series:
    if "accuracy_mode_eligible_flag" not in df.columns:
        return pd.Series(False, index=df.index)
    return df["accuracy_mode_eligible_flag"].map(bool_flag)


def has_strong_stats_support(row: pd.Series) -> bool:
    quality = norm_text(row.get("recent_stats_quality_flag"))
    process_score = safe_float(row.get("recent_stats_process_score"), 0.0)
    home_used = safe_float(row.get("home_recent_stats_matches_used"), 0.0)
    away_used = safe_float(row.get("away_recent_stats_matches_used"), 0.0)
    home_cov = safe_float(row.get("home_recent_stats_coverage_ratio"), 0.0)
    away_cov = safe_float(row.get("away_recent_stats_coverage_ratio"), 0.0)
    return bool(
        quality == "FULL"
        or process_score >= 3.0
        or (min(home_used, away_used) >= 4 and min(home_cov, away_cov) >= 0.60)
    )


def has_partial_stats_support(row: pd.Series) -> bool:
    quality = norm_text(row.get("recent_stats_quality_flag"))
    return quality in {"PARTIAL", "SPARSE"} or safe_float(row.get("recent_stats_process_score"), 0.0) > 0.0


def market_accuracy_bonus(market: str) -> float:
    if market == "OVER_1_5":
        return 12.0
    if market == "UNDER_3_5":
        return 10.0
    if market == "OVER_2_5":
        return 4.0
    if market in {"HOME_DNB", "AWAY_DNB"}:
        return 1.0
    if market in FRAGILE_SIDE_MARKETS:
        return -10.0
    if market in BTTS_MARKETS:
        return -8.0
    return -6.0


def derive_failure_mode(row: pd.Series) -> str:
    existing = norm_text(row.get("pick_failure_mode"))
    if existing:
        return existing
    try:
        return norm_text(failure_mode(row))
    except Exception:
        return "UNKNOWN"


def failure_mode_penalty(row: pd.Series, market: str, mode: str) -> float:
    if mode == "DRAW_LIVE":
        return 16.0 if market in FRAGILE_SIDE_MARKETS else 8.0
    if mode == "BTTS_BREAK":
        return 14.0
    if mode == "LOW_CONVERSION":
        return 6.0 if market == "OVER_2_5" else 2.0
    if mode == "AVALANCHE_RISK":
        return 4.0 if market == "UNDER_3_5" else 9.0
    if mode == "THIN_MARGIN":
        return 10.0
    if mode in {"MARKET_TOO_FINE", "ATTACK_THIN", "DEFENSE_THIN"}:
        return 8.0
    return 0.0


def accuracy_source_bucket(row: pd.Series) -> str:
    source = norm_text(row.get("execution_shortlist_source"))
    bucket = norm_text(row.get("final_execution_bucket"))
    if source == "PREMIUM_CORE" or (
        bucket == "APPROVED_PREMIUM" and norm_text(row.get("base_execution_verdict")) in {"TOP_CORE", "CORE_SHORTLIST"}
    ):
        return "PREMIUM_CORE"
    if source == "PREMIUM_EXTENDED":
        return "PREMIUM_EXTENDED"
    if source == "STANDARD_FILL" or bucket == "APPROVED_STANDARD":
        return "STANDARD_FILL"
    return source or bucket or "UNKNOWN"


def accuracy_reason_and_score(row: pd.Series) -> tuple[bool, float, str, str, str]:
    market = norm_text(row.get("market_primary"))
    source_bucket = accuracy_source_bucket(row)
    recommendation = norm_text(row.get("final_recommendation"))
    market_fit = norm_text(row.get("execution_market_fit_status"))
    failure = derive_failure_mode(row)
    edge = safe_float(row.get("primary_edge"), 0.0)
    model_prob = safe_float(row.get("primary_model_prob"), 0.0)
    odds = safe_float(row.get("primary_odds_used"), 0.0)
    selection_score = safe_float(row.get("selection_score"), 0.0)
    execution_score = safe_float(row.get("execution_score"), 0.0)
    base_verdict = norm_text(row.get("base_execution_verdict"))
    final_bucket = norm_text(row.get("final_execution_bucket"))

    strong_stats = has_strong_stats_support(row)
    partial_stats = has_partial_stats_support(row)

    score = 50.0
    if source_bucket == "PREMIUM_CORE":
        score += 18.0
    elif source_bucket == "PREMIUM_EXTENDED":
        score += 4.0
    elif source_bucket == "STANDARD_FILL":
        score -= 8.0

    if final_bucket == "APPROVED_PREMIUM":
        score += 10.0
    elif final_bucket == "APPROVED_STANDARD":
        score += 1.0

    if base_verdict == "TOP_CORE":
        score += 8.0
    elif base_verdict == "CORE_SHORTLIST":
        score += 5.0
    elif base_verdict == "WATCH":
        score -= 8.0

    score += market_accuracy_bonus(market)

    if market_fit == "SAFE_OK":
        score += 8.0
    elif market_fit in BLOCKED_MARKET_FIT_STATUSES:
        score -= 99.0
    elif not market_fit:
        score -= 2.0

    if strong_stats:
        score += 10.0
    elif partial_stats:
        score += 3.0
    else:
        score -= 8.0

    coverage_class = norm_text(row.get("league_coverage_class"))
    if coverage_class in {"COVERAGE_RICH", "COVERAGE_GOOD"}:
        score += 4.0
    elif coverage_class == "COVERAGE_PARTIAL":
        score -= 3.0
    elif coverage_class in {"COVERAGE_THIN", "COVERAGE_MINIMAL"}:
        score -= 8.0

    score += max(-10.0, min(18.0, (model_prob - 0.70) * 80.0))
    score += max(0.0, min(10.0, edge * 45.0))
    score += max(0.0, min(8.0, (selection_score - 75.0) / 2.0))
    score += max(0.0, min(10.0, (execution_score - 95.0) / 4.0))
    score -= failure_mode_penalty(row, market, failure)

    lineup_state = norm_text(row.get("lineup_activation_state"))
    lineup_quality = norm_text(row.get("lineup_quality_flag"))
    if lineup_state == "ACTIVE" and lineup_quality not in {"FULL", "CONFIRMED"}:
        score -= 3.0
    elif lineup_state not in {"ACTIVE", "ADVISORY_ONLY", ""} and market in FRAGILE_SIDE_MARKETS:
        score -= 2.0

    tags: list[str] = []
    risk = f"FAILURE_MODE_{failure or 'UNKNOWN'}"
    eligible = True
    reject_reason = ""

    if source_bucket == "PREMIUM_CORE":
        tags.append("ACCURACY_CORE_PRIORITY")
    elif source_bucket == "PREMIUM_EXTENDED":
        tags.append("ACCURACY_EXTENDED_REVIEW")

    if market in STABLE_MARKETS:
        tags.append("ACCURACY_MARKET_STABLE")
    if market in {"OVER_1_5", "OVER_2_5"} and strong_stats:
        tags.append("ACCURACY_OVER_CONFIRMED")
    if model_prob >= 0.82:
        tags.append("ACCURACY_MODEL_PROB_HIGH")
    if failure not in {"DRAW_LIVE", "BTTS_BREAK", "THIN_MARGIN", "MARKET_TOO_FINE"}:
        tags.append("ACCURACY_FAILURE_MODE_ACCEPTABLE")

    if recommendation not in ACTIONABLE_RECOMMENDATIONS:
        eligible = False
        reject_reason = "ACCURACY_NO_BET_PREFERRED"
    elif edge <= 0 or odds <= 1.0:
        eligible = False
        reject_reason = "ACCURACY_NO_BET_PREFERRED"
    elif market_fit in BLOCKED_MARKET_FIT_STATUSES:
        eligible = False
        reject_reason = "ACCURACY_MARKET_FIT_BLOCKED"
    elif market in FRAGILE_SIDE_MARKETS and not (
        source_bucket == "PREMIUM_CORE"
        and strong_stats
        and model_prob >= 0.86
        and edge >= 0.16
        and score >= 105.0
    ):
        eligible = False
        reject_reason = "ACCURACY_SIDE_TOO_FRAGILE"
    elif market in BTTS_MARKETS and not (
        source_bucket == "PREMIUM_CORE"
        and strong_stats
        and model_prob >= 0.86
        and edge >= 0.14
        and score >= 105.0
    ):
        eligible = False
        reject_reason = "ACCURACY_BTTS_SUPPORT_INSUFFICIENT"
    elif market == "OVER_2_5" and not (
        strong_stats
        and source_bucket == "PREMIUM_CORE"
        and model_prob >= 0.78
        and edge >= 0.10
        and score >= MIN_CORE_SCORE
    ):
        eligible = False
        reject_reason = "ACCURACY_OVER_SUPPORT_INSUFFICIENT"
    elif market not in STABLE_MARKETS and market not in CONDITIONAL_STABLE_MARKETS and market not in FRAGILE_SIDE_MARKETS and market not in BTTS_MARKETS:
        eligible = False
        reject_reason = "ACCURACY_MARKET_TOO_FINE"
    elif source_bucket == "PREMIUM_EXTENDED" and not (
        market in STABLE_MARKETS
        and strong_stats
        and model_prob >= 0.84
        and edge >= 0.10
        and score >= MIN_EXTENDED_SCORE
    ):
        eligible = False
        reject_reason = "ACCURACY_EXTENDED_REJECTED"
    elif source_bucket == "STANDARD_FILL" and not (
        market in STABLE_MARKETS
        and strong_stats
        and model_prob >= 0.86
        and edge >= 0.12
        and score >= MIN_STANDARD_SCORE
    ):
        eligible = False
        reject_reason = "ACCURACY_STANDARD_REJECTED"
    elif source_bucket == "PREMIUM_CORE" and score < MIN_CORE_SCORE:
        eligible = False
        reject_reason = "ACCURACY_CORE_SUPPORT_TOO_THIN"

    if not strong_stats and eligible:
        eligible = False
        reject_reason = "ACCURACY_STATS_SUPPORT_TOO_THIN"

    if not eligible:
        tags.append(reject_reason or "ACCURACY_NO_BET_PREFERRED")

    if eligible and not tags:
        tags.append("ACCURACY_FAILURE_MODE_ACCEPTABLE")

    if eligible and source_bucket == "PREMIUM_CORE":
        bucket = "ACCURACY_CORE"
    elif eligible and source_bucket == "PREMIUM_EXTENDED":
        bucket = "ACCURACY_EXTENDED_STRONG"
    elif eligible:
        bucket = "ACCURACY_EXCEPTIONAL"
    else:
        bucket = "ACCURACY_REJECTED"

    return eligible, round(score, 3), ";".join(dict.fromkeys(tags)), risk, bucket


def add_accuracy_mode_fields(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if out.empty:
        for col in ACCURACY_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=object)
        for col in CALIBRATED_PROBABILITY_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=object)
        return out

    if "execution_score" not in out.columns:
        out["execution_score"] = pd.to_numeric(out.get("selection_score", 0.0), errors="coerce").fillna(0.0)

    if "pick_failure_mode" not in out.columns:
        out = add_pick_explanations(out)

    rows = [accuracy_reason_and_score(row) for _, row in out.iterrows()]
    out["accuracy_mode_eligible_flag"] = [int(value[0]) for value in rows]
    out["accuracy_confidence_score"] = [value[1] for value in rows]
    out["accuracy_mode_reason"] = [value[2] for value in rows]
    out["accuracy_primary_risk"] = [value[3] for value in rows]
    out["accuracy_mode_bucket"] = [value[4] for value in rows]
    out["accuracy_mode_rank"] = pd.NA

    eligible_index = out["accuracy_mode_eligible_flag"].eq(1)
    if eligible_index.any():
        ordered_index = out[eligible_index].sort_values(
            [
                "accuracy_confidence_score",
                "primary_model_prob",
                "primary_edge",
                "execution_score",
            ],
            ascending=[False, False, False, False],
            na_position="last",
            kind="mergesort",
        ).index
        out.loc[ordered_index, "accuracy_mode_rank"] = range(1, len(ordered_index) + 1)

    return out


def decided_competition_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    if "accuracy_mode_eligible_flag" not in df.columns:
        df = add_accuracy_mode_fields(df)
    result_status = df.get("result_status", pd.Series("", index=df.index)).map(norm_text)
    result = df.get("actionable_result", pd.Series("", index=df.index)).map(norm_text)
    raw_prob = pd.to_numeric(df.get("primary_model_prob", pd.Series(index=df.index, dtype=float)), errors="coerce")
    return df[
        competition_eligible_mask(df)
        & result_status.eq("RESULT_AVAILABLE")
        & result.isin(DECIDED_RESULTS)
        & raw_prob.notna()
    ].copy()


def calibration_group_key(row: pd.Series, group_type: str) -> str:
    market = norm_text(row.get("market_primary")) or "UNKNOWN"
    bucket = norm_text(row.get("accuracy_mode_bucket")) or "UNKNOWN"
    if group_type == "MARKET_BUCKET":
        return f"{market}|{bucket}"
    if group_type == "MARKET":
        return market
    if group_type == "BUCKET":
        return bucket
    return "COMPETITION_GLOBAL"


def capped_adjustment(empirical_hit_rate: float, raw_avg_prob: float, max_down: float, max_up: float) -> float:
    return max(-max_down, min(max_up, empirical_hit_rate - raw_avg_prob))


def build_probability_calibration_table(historical: pd.DataFrame) -> pd.DataFrame:
    rows = decided_competition_rows(historical)
    output_rows: list[dict[str, object]] = []

    for spec in CALIBRATION_GROUP_SPECS:
        group_type = spec["group_type"]
        group_cols = spec["group_cols"]
        if rows.empty:
            groups = []
        elif group_cols:
            working = rows.copy()
            for col in group_cols:
                working[col] = working[col].map(norm_text)
            groups = list(working.groupby(group_cols, dropna=False, sort=True))
        else:
            groups = [("COMPETITION_GLOBAL", rows)]

        for keys, subset in groups:
            if not isinstance(keys, tuple):
                keys = (keys,)
            result = subset["actionable_result"].map(norm_text)
            wins = int(result.eq("WIN").sum())
            losses = int(result.eq("LOSS").sum())
            sample_size = wins + losses
            raw_avg = float(pd.to_numeric(subset["primary_model_prob"], errors="coerce").mean())
            empirical = wins / sample_size if sample_size else 0.0
            eligible = sample_size >= int(spec["min_sample_size"])
            adjustment = (
                capped_adjustment(
                    empirical,
                    raw_avg,
                    float(spec["max_down_adjustment"]),
                    float(spec["max_up_adjustment"]),
                )
                if eligible
                else 0.0
            )
            row = {
                "group_type": group_type,
                "group_key": "|".join(str(key) for key in keys) if group_cols else "COMPETITION_GLOBAL",
                "market_primary": "",
                "accuracy_mode_bucket": "",
                "sample_size": sample_size,
                "wins": wins,
                "losses": losses,
                "raw_avg_predicted_probability": round(raw_avg, 6) if sample_size else pd.NA,
                "empirical_hit_rate": round(empirical, 6) if sample_size else pd.NA,
                "calibration_adjustment": round(adjustment, 6) if sample_size else 0.0,
                "calibrated_avg_probability": round(
                    max(MIN_CALIBRATED_PROB, min(MAX_CALIBRATED_PROB, raw_avg + adjustment)),
                    6,
                )
                if sample_size
                else pd.NA,
                "min_sample_size": int(spec["min_sample_size"]),
                "usable_for_lookup": int(eligible),
                "calibration_note": "USABLE" if eligible else "THIN_SAMPLE_NOT_USED",
            }
            if group_type == "MARKET_BUCKET":
                row["market_primary"] = keys[0]
                row["accuracy_mode_bucket"] = keys[1]
            elif group_type == "MARKET":
                row["market_primary"] = keys[0]
            elif group_type == "BUCKET":
                row["accuracy_mode_bucket"] = keys[0]
            output_rows.append(row)

    columns = [
        "group_type",
        "group_key",
        "market_primary",
        "accuracy_mode_bucket",
        "sample_size",
        "wins",
        "losses",
        "raw_avg_predicted_probability",
        "empirical_hit_rate",
        "calibration_adjustment",
        "calibrated_avg_probability",
        "min_sample_size",
        "usable_for_lookup",
        "calibration_note",
    ]
    return pd.DataFrame(output_rows, columns=columns)


def lookup_calibration_rule(row: pd.Series, calibration_table: pd.DataFrame) -> pd.Series | None:
    if calibration_table.empty:
        return None
    usable = calibration_table[
        pd.to_numeric(calibration_table.get("usable_for_lookup", 0), errors="coerce").fillna(0).eq(1)
    ].copy()
    if usable.empty:
        return None

    market = norm_text(row.get("market_primary"))
    bucket = norm_text(row.get("accuracy_mode_bucket"))
    lookups = [
        ("MARKET_BUCKET", market, bucket),
        ("MARKET", market, ""),
        ("BUCKET", "", bucket),
        ("GLOBAL", "", ""),
    ]
    for group_type, market_key, bucket_key in lookups:
        subset = usable[usable["group_type"].map(norm_text).eq(group_type)]
        if market_key:
            subset = subset[subset["market_primary"].map(norm_text).eq(market_key)]
        if bucket_key:
            subset = subset[subset["accuracy_mode_bucket"].map(norm_text).eq(bucket_key)]
        if not subset.empty:
            return subset.iloc[0]
    return None


def calibration_reason(group_type: str, adjustment: float) -> str:
    if adjustment < -0.0005:
        if group_type == "MARKET_BUCKET":
            return "CALIBRATED_MARKET_BUCKET_OVERCONFIDENCE"
        if group_type == "MARKET":
            return "CALIBRATED_MARKET_OVERCONFIDENCE"
        if group_type == "BUCKET":
            return "CALIBRATED_BUCKET_SHRINKAGE"
        return "CALIBRATED_GLOBAL_FALLBACK"
    if adjustment > 0.0005:
        if group_type == "MARKET_BUCKET":
            return "CALIBRATED_MARKET_BUCKET_RELIABILITY_UPLIFT"
        if group_type == "MARKET":
            return "CALIBRATED_MARKET_RELIABILITY_UPLIFT"
        if group_type == "BUCKET":
            return "CALIBRATED_BUCKET_RELIABILITY_UPLIFT"
        return "CALIBRATED_GLOBAL_FALLBACK"
    return "CALIBRATED_NO_MATERIAL_ADJUSTMENT"


def add_competition_probability_calibration(
    df: pd.DataFrame,
    calibration_table: pd.DataFrame | None = None,
) -> pd.DataFrame:
    out = df.copy()
    if out.empty:
        for col in CALIBRATED_PROBABILITY_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=object)
        return out

    if "accuracy_mode_eligible_flag" not in out.columns:
        out = add_accuracy_mode_fields(out)

    table = calibration_table if calibration_table is not None else pd.DataFrame()
    raw = pd.to_numeric(out.get("primary_model_prob", pd.Series(index=out.index, dtype=float)), errors="coerce")
    out["competition_raw_prob"] = raw.round(6)
    out["competition_calibrated_prob"] = raw.round(6)
    out["competition_prob_calibration_bucket"] = "CALIBRATION_NOT_APPLIED"
    out["competition_prob_calibration_reason"] = "CALIBRATION_NOT_APPLIED_NON_COMPETITION"
    out["competition_prob_shrinkage_applied_flag"] = 0

    for idx, row in out.iterrows():
        if not bool_flag(row.get("accuracy_mode_eligible_flag")):
            continue
        raw_prob = raw.loc[idx]
        if pd.isna(raw_prob):
            out.loc[idx, "competition_prob_calibration_reason"] = "CALIBRATION_RAW_PROB_MISSING"
            continue

        rule = lookup_calibration_rule(row, table)
        if rule is None:
            adjustment = -0.015 if raw_prob >= 0.85 else 0.0
            group_type = "THIN_FALLBACK"
            bucket = "THIN_FALLBACK:MINIMAL"
            reason = "CALIBRATION_SAMPLE_THIN_MINIMAL_SHRINK"
        else:
            adjustment = safe_float(rule.get("calibration_adjustment"), 0.0)
            group_type = norm_text(rule.get("group_type"))
            bucket = f"{group_type}:{rule.get('group_key')}"
            reason = calibration_reason(group_type, adjustment)

        calibrated = max(MIN_CALIBRATED_PROB, min(MAX_CALIBRATED_PROB, raw_prob + adjustment))
        out.loc[idx, "competition_calibrated_prob"] = round(calibrated, 6)
        out.loc[idx, "competition_prob_calibration_bucket"] = bucket
        out.loc[idx, "competition_prob_calibration_reason"] = reason
        out.loc[idx, "competition_prob_shrinkage_applied_flag"] = int(abs(calibrated - raw_prob) > 0.0005)

    return out


def sort_accuracy_candidates(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df.copy()
    source_priority = out["execution_shortlist_source"].map(norm_text).map(
        {"PREMIUM_CORE": 1, "PREMIUM_EXTENDED": 2, "STANDARD_FILL": 3}
    ).fillna(9)
    out["_accuracy_source_priority"] = source_priority
    out = out.sort_values(
        [
            "accuracy_confidence_score",
            "_accuracy_source_priority",
            "primary_model_prob",
            "primary_edge",
            "execution_rank",
        ],
        ascending=[False, True, False, False, True],
        na_position="last",
        kind="mergesort",
    )
    return out.drop(columns=["_accuracy_source_priority"], errors="ignore").reset_index(drop=True)


def select_competition_top(shortlist: pd.DataFrame) -> pd.DataFrame:
    eligible = sort_accuracy_candidates(shortlist[shortlist["accuracy_mode_eligible_flag"].eq(1)].copy())
    selected: list[pd.Series] = []
    league_counts: dict[object, int] = {}
    market_counts: dict[object, int] = {}
    fixture_ids: set[object] = set()

    for _, row in eligible.iterrows():
        if len(selected) >= MAX_COMPETITION_TOP_ROWS:
            break
        league = row.get("league") if not pd.isna(row.get("league")) else "__MISSING__"
        market = row.get("market_primary") if not pd.isna(row.get("market_primary")) else "__MISSING__"
        fixture_id = row.get("fixture_id") if not pd.isna(row.get("fixture_id")) else "__MISSING__"

        if league_counts.get(league, 0) >= MAX_TOP_PER_LEAGUE:
            continue
        if market_counts.get(market, 0) >= MAX_TOP_PER_MARKET:
            continue
        if fixture_id in fixture_ids:
            continue

        selected_row = row.copy()
        selected.append(selected_row)
        league_counts[league] = league_counts.get(league, 0) + 1
        market_counts[market] = market_counts.get(market, 0) + 1
        fixture_ids.add(fixture_id)

    if not selected:
        return pd.DataFrame(columns=eligible.columns)

    out = pd.DataFrame(selected).reset_index(drop=True)
    out["accuracy_mode_rank"] = range(1, len(out) + 1)
    out["pick_mode"] = COMPETITION_MODE_NAME
    return out


def write_competition_report(path: Path, source: pd.DataFrame, shortlist: pd.DataFrame, top: pd.DataFrame) -> None:
    lines = [
        "VSIGMA COMPETITION ACCURACY MODE",
        "",
        f"Mode: {COMPETITION_MODE_NAME}",
        f"Normal execution shortlist rows: {len(source)}",
        f"Competition shortlist rows: {len(shortlist)}",
        f"Competition top rows: {len(top)}",
        "",
        "Principle: prefer no pick over weak pick; prioritize stable markets, premium core evidence, strong rolling stats, clean market-fit, and high model probability.",
        "",
    ]

    if shortlist.empty:
        lines.extend(["Competition shortlist", "ACCURACY_NO_BET_PREFERRED", ""])
    else:
        lines.append("Competition shortlist")
        display_cols = [
            "accuracy_mode_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "execution_shortlist_source",
            "competition_raw_prob",
            "competition_calibrated_prob",
            "accuracy_confidence_score",
            "accuracy_mode_bucket",
            "accuracy_mode_reason",
            "accuracy_primary_risk",
            "competition_prob_calibration_reason",
        ]
        lines.append(shortlist[[c for c in display_cols if c in shortlist.columns]].to_string(index=False))
        lines.append("")

    if top.empty:
        lines.extend(["Competition top", "No top picks survived the stricter accuracy gate.", ""])
    else:
        lines.append("Competition top")
        display_cols = [
            "accuracy_mode_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "competition_raw_prob",
            "competition_calibrated_prob",
            "primary_edge",
            "accuracy_confidence_score",
            "accuracy_mode_reason",
            "accuracy_primary_risk",
            "competition_prob_calibration_reason",
        ]
        lines.append(top[[c for c in display_cols if c in top.columns]].to_string(index=False))
        lines.append("")

    rejected = source[source.get("accuracy_mode_eligible_flag", 0).eq(0)] if "accuracy_mode_eligible_flag" in source.columns else pd.DataFrame()
    if not rejected.empty and "accuracy_mode_reason" in rejected.columns:
        lines.append("Most common rejection tags")
        lines.append(rejected["accuracy_mode_reason"].value_counts().head(12).to_string())
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def build_today_competition_outputs(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
) -> tuple[dict[str, Path], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    input_path = processed_dir / TODAY_SHORTLIST_INPUT
    if not input_path.exists():
        raise FileNotFoundError(f"Missing competition input: {input_path}")

    source = pd.read_csv(input_path)
    scored = add_accuracy_mode_fields(source)
    historical_path = processed_dir / HISTORICAL_SOURCE_INPUT
    calibration_table = (
        build_probability_calibration_table(pd.read_csv(historical_path))
        if historical_path.exists()
        else pd.DataFrame()
    )
    scored = add_competition_probability_calibration(scored, calibration_table)
    shortlist = sort_accuracy_candidates(scored[scored["accuracy_mode_eligible_flag"].eq(1)].copy())
    if not shortlist.empty:
        shortlist["accuracy_mode_rank"] = range(1, len(shortlist) + 1)
        shortlist["pick_mode"] = COMPETITION_MODE_NAME
    top = select_competition_top(shortlist)

    processed_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "COMPETITION_SHORTLIST": processed_dir / COMPETITION_SHORTLIST_OUTPUT,
        "COMPETITION_TOP": processed_dir / COMPETITION_TOP_OUTPUT,
        "COMPETITION_REPORT": processed_dir / COMPETITION_REPORT_OUTPUT,
    }
    shortlist.to_csv(paths["COMPETITION_SHORTLIST"], index=False)
    top.to_csv(paths["COMPETITION_TOP"], index=False)
    write_competition_report(paths["COMPETITION_REPORT"], scored, shortlist, top)
    return paths, scored, shortlist, top


def graded_decision_mask(df: pd.DataFrame) -> pd.Series:
    return df["result_status"].map(norm_text).eq("RESULT_AVAILABLE") & df["actionable_result"].map(norm_text).isin({"WIN", "LOSS"})


def probability_eval_subset(df: pd.DataFrame, segment: str, subset: pd.DataFrame) -> dict[str, object]:
    graded = subset[graded_decision_mask(subset)].copy() if not subset.empty else subset.copy()
    results = graded["actionable_result"].map(norm_text) if not graded.empty else pd.Series(dtype=object)
    raw_probs = pd.to_numeric(
        graded.get("competition_raw_prob", graded.get("primary_model_prob", pd.Series(dtype=float))),
        errors="coerce",
    )
    calibrated_probs = pd.to_numeric(
        graded.get("competition_calibrated_prob", raw_probs),
        errors="coerce",
    )
    y = results.eq("WIN").astype(float) if not graded.empty else pd.Series(dtype=float)
    valid_raw_brier = raw_probs.notna() & y.notna()
    valid_calibrated_brier = calibrated_probs.notna() & y.notna()
    profit = pd.to_numeric(graded.get("profit_units", pd.Series(dtype=float)), errors="coerce").sum()
    wins = int(results.eq("WIN").sum()) if not graded.empty else 0
    losses = int(results.eq("LOSS").sum()) if not graded.empty else 0
    decided = wins + losses
    subset_raw_prob = pd.to_numeric(
        subset.get("competition_raw_prob", subset.get("primary_model_prob", pd.Series(dtype=float))),
        errors="coerce",
    )
    subset_calibrated_prob = pd.to_numeric(
        subset.get("competition_calibrated_prob", subset_raw_prob),
        errors="coerce",
    )
    brier_raw = (
        round(float(((raw_probs[valid_raw_brier] - y[valid_raw_brier]) ** 2).mean()), 6)
        if valid_raw_brier.any()
        else pd.NA
    )
    brier_calibrated = (
        round(
            float(((calibrated_probs[valid_calibrated_brier] - y[valid_calibrated_brier]) ** 2).mean()),
            6,
        )
        if valid_calibrated_brier.any()
        else pd.NA
    )
    return {
        "segment": segment,
        "rows_total": int(len(subset)),
        "graded_rows": int(len(graded)),
        "wins": wins,
        "losses": losses,
        "hit_rate": round(wins / decided * 100.0, 6) if decided else pd.NA,
        "brier_score": brier_calibrated,
        "brier_score_raw": brier_raw,
        "brier_score_calibrated": brier_calibrated,
        "avg_probability": round(float(subset_calibrated_prob.mean()), 6) if len(subset) else pd.NA,
        "avg_probability_raw": round(float(subset_raw_prob.mean()), 6) if len(subset) else pd.NA,
        "avg_probability_calibrated": round(float(subset_calibrated_prob.mean()), 6) if len(subset) else pd.NA,
        "avg_edge": round(float(pd.to_numeric(subset.get("primary_edge", pd.Series(dtype=float)), errors="coerce").mean()), 6) if len(subset) else pd.NA,
        "profit_units_total": round(float(profit), 6) if len(graded) else 0.0,
        "roi_percent": round(float(profit) / len(graded) * 100.0, 6) if len(graded) else pd.NA,
    }


def build_probability_evaluation(
    source_csv: Path = DEFAULT_PROCESSED_DIR / HISTORICAL_SOURCE_INPUT,
    output_dir: Path = DEFAULT_PROCESSED_DIR,
) -> tuple[dict[str, Path], pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not source_csv.exists():
        empty = pd.DataFrame(
            columns=[
                "summary_scope",
                "segment",
                "rows_total",
                "graded_rows",
                "wins",
                "losses",
                "hit_rate",
                "brier_score",
                "avg_probability",
                "avg_edge",
                "profit_units_total",
                "roi_percent",
            ]
        )
        paths = {
            "summary": output_dir / PROBABILITY_SUMMARY_OUTPUT,
            "report": output_dir / PROBABILITY_REPORT_OUTPUT,
            "calibration_table": output_dir / PROBABILITY_CALIBRATION_TABLE_OUTPUT,
            "calibration_report": output_dir / PROBABILITY_CALIBRATION_REPORT_OUTPUT,
        }
        empty.to_csv(paths["summary"], index=False)
        pd.DataFrame().to_csv(paths["calibration_table"], index=False)
        paths["report"].write_text(
            "VSIGMA PROBABILITY EVALUATION\n\nHistorical execution source not available.\n",
            encoding="utf-8",
        )
        paths["calibration_report"].write_text(
            "VSIGMA PROBABILITY CALIBRATION\n\nHistorical execution source not available.\n",
            encoding="utf-8",
        )
        return paths, empty

    source = pd.read_csv(source_csv)
    if "accuracy_mode_eligible_flag" not in source.columns:
        source = add_accuracy_mode_fields(source)
    calibration_table = build_probability_calibration_table(source)
    source = add_competition_probability_calibration(source, calibration_table)

    rows: list[dict[str, object]] = []

    def add(scope: str, segment: str, subset: pd.DataFrame) -> None:
        row = probability_eval_subset(source, segment, subset)
        row["summary_scope"] = scope
        rows.append(row)

    add("overall", "FULL_SHORTLIST", source)
    add("mode", COMPETITION_MODE_NAME, source[source["accuracy_mode_eligible_flag"].map(bool_flag)].copy())

    for source_name, subset in source.groupby("execution_shortlist_source", dropna=False, sort=True):
        add("bucket", norm_text(source_name) or "UNKNOWN", subset)

    if "market_primary" in source.columns:
        for market, subset in source.groupby("market_primary", dropna=False, sort=True):
            add("market_family", norm_text(market) or "UNKNOWN", subset)

    prob = pd.to_numeric(source.get("primary_model_prob", pd.Series(index=source.index, dtype=float)), errors="coerce")
    bucketed = source.copy()
    bucketed["probability_bucket"] = pd.cut(
        prob,
        bins=[0.0, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 1.01],
        labels=["0.00-0.60", "0.60-0.70", "0.70-0.75", "0.75-0.80", "0.80-0.85", "0.85-0.90", "0.90-1.00"],
        include_lowest=True,
        right=False,
    )
    for bucket, subset in bucketed.groupby("probability_bucket", dropna=False, sort=True, observed=False):
        add("calibration_bucket", str(bucket), subset)

    summary = pd.DataFrame(rows)
    output_cols = [
        "summary_scope",
        "segment",
        "rows_total",
        "graded_rows",
        "wins",
        "losses",
        "hit_rate",
        "brier_score",
        "brier_score_raw",
        "brier_score_calibrated",
        "avg_probability",
        "avg_probability_raw",
        "avg_probability_calibrated",
        "avg_edge",
        "profit_units_total",
        "roi_percent",
    ]
    summary = summary[output_cols]

    paths = {
        "summary": output_dir / PROBABILITY_SUMMARY_OUTPUT,
        "report": output_dir / PROBABILITY_REPORT_OUTPUT,
        "calibration_table": output_dir / PROBABILITY_CALIBRATION_TABLE_OUTPUT,
        "calibration_report": output_dir / PROBABILITY_CALIBRATION_REPORT_OUTPUT,
    }
    summary.to_csv(paths["summary"], index=False)
    calibration_table.to_csv(paths["calibration_table"], index=False)
    write_probability_report(paths["report"], summary)
    write_probability_calibration_report(paths["calibration_report"], calibration_table, summary)
    return paths, summary


def write_probability_report(path: Path, summary: pd.DataFrame) -> None:
    mode_rows = summary[summary["summary_scope"].isin(["overall", "mode"])].copy()
    calibration = summary[summary["summary_scope"].eq("calibration_bucket")].copy()
    market = summary[summary["summary_scope"].eq("market_family")].copy()
    bucket = summary[summary["summary_scope"].eq("bucket")].copy()

    lines = [
        "VSIGMA PROBABILITY EVALUATION",
        "",
        "Hit rate by mode",
        mode_rows.to_string(index=False) if not mode_rows.empty else "No rows",
        "",
        "Calibration buckets",
        calibration.to_string(index=False) if not calibration.empty else "No rows",
        "",
        "Accuracy by market family",
        market.to_string(index=False) if not market.empty else "No rows",
        "",
        "Accuracy by execution bucket",
        bucket.to_string(index=False) if not bucket.empty else "No rows",
        "",
    ]

    full = mode_rows[mode_rows["segment"].eq("FULL_SHORTLIST")]
    competition = mode_rows[mode_rows["segment"].eq(COMPETITION_MODE_NAME)]
    if not full.empty and not competition.empty:
        full_hit = full.iloc[0]["hit_rate"]
        competition_hit = competition.iloc[0]["hit_rate"]
        full_rows = int(full.iloc[0]["rows_total"])
        competition_rows = int(competition.iloc[0]["rows_total"])
        raw_brier = competition.iloc[0].get("brier_score_raw", pd.NA)
        calibrated_brier = competition.iloc[0].get("brier_score_calibrated", pd.NA)
        lines.extend(
            [
                "Selector behavior",
                (
                    f"Competition mode rows={competition_rows} vs full shortlist rows={full_rows}. "
                    f"Hit rate={competition_hit} vs full shortlist hit rate={full_hit}. "
                    "The mode is narrower by design when competition rows are below full shortlist rows. "
                    f"Competition raw Brier={raw_brier}; calibrated Brier={calibrated_brier}."
                ),
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_probability_calibration_report(
    path: Path,
    calibration_table: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    mode_rows = summary[summary["summary_scope"].isin(["overall", "mode"])].copy()
    competition = mode_rows[mode_rows["segment"].eq(COMPETITION_MODE_NAME)]
    usable = calibration_table[
        pd.to_numeric(calibration_table.get("usable_for_lookup", 0), errors="coerce").fillna(0).eq(1)
    ].copy()
    if not usable.empty:
        usable["_abs_adjustment"] = pd.to_numeric(
            usable["calibration_adjustment"],
            errors="coerce",
        ).abs()
        strongest = usable.sort_values("_abs_adjustment", ascending=False).drop(columns=["_abs_adjustment"])
        usable = usable.drop(columns=["_abs_adjustment"])
    else:
        strongest = usable

    lines = [
        "VSIGMA PROBABILITY CALIBRATION",
        "",
        "Method",
        (
            "Competition probabilities copy primary_model_prob into competition_raw_prob, then apply a capped "
            "deterministic reliability adjustment. Lookup order is market+competition bucket, market, bucket, "
            "then global competition fallback. Thin samples are reported but not used unless they meet the "
            "minimum sample size for that lookup tier."
        ),
        "",
        "Mode comparison",
        mode_rows.to_string(index=False) if not mode_rows.empty else "No rows",
        "",
        "Usable calibration groups",
        usable.to_string(index=False) if not usable.empty else "No usable groups",
        "",
        "Largest absolute adjustments",
        strongest.head(10).to_string(index=False) if not strongest.empty else "No usable groups",
        "",
    ]

    if not competition.empty:
        row = competition.iloc[0]
        lines.extend(
            [
                "Competition calibration verdict",
                (
                    f"Rows={int(row['rows_total'])}; hit_rate={row['hit_rate']}; ROI={row['roi_percent']}; "
                    f"raw_avg_prob={row.get('avg_probability_raw', pd.NA)}; "
                    f"calibrated_avg_prob={row.get('avg_probability_calibrated', pd.NA)}; "
                    f"raw_Brier={row.get('brier_score_raw', pd.NA)}; "
                    f"calibrated_Brier={row.get('brier_score_calibrated', pd.NA)}."
                ),
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build vSIGMA competition accuracy mode outputs.")
    parser.add_argument("--processed-dir", default=str(DEFAULT_PROCESSED_DIR))
    parser.add_argument(
        "--skip-probability-evaluation",
        action="store_true",
        help="Only build today's competition shortlist/top/report.",
    )
    args = parser.parse_args()

    processed_dir = Path(args.processed_dir)
    paths, _source, shortlist, top = build_today_competition_outputs(processed_dir)
    probability_paths: dict[str, Path] = {}
    probability_summary = pd.DataFrame()
    if not args.skip_probability_evaluation:
        probability_paths, probability_summary = build_probability_evaluation(
            processed_dir / HISTORICAL_SOURCE_INPUT,
            processed_dir,
        )

    print("\n=== COMPETITION ACCURACY MODE COMPLETADO ===")
    for key, path in {**paths, **probability_paths}.items():
        print(f"{key}: {path}")
    print(f"Competition shortlist rows: {len(shortlist)}")
    print(f"Competition top rows: {len(top)}")
    if not top.empty:
        display_cols = [
            "accuracy_mode_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "competition_raw_prob",
            "competition_calibrated_prob",
            "accuracy_confidence_score",
            "accuracy_mode_reason",
            "accuracy_primary_risk",
            "competition_prob_calibration_reason",
        ]
        print("\nCompetition top picks:")
        print(top[[c for c in display_cols if c in top.columns]].to_string(index=False))
    if not probability_summary.empty:
        print("\nProbability evaluation by mode:")
        print(
            probability_summary[probability_summary["summary_scope"].isin(["overall", "mode"])].to_string(
                index=False
            )
        )


if __name__ == "__main__":
    main()
