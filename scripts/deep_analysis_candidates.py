from __future__ import annotations

from pathlib import Path
import math
import re
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

SHORTLIST_CSV = ROOT / "data" / "processed" / "vsigma_core_shortlist.csv"
SCORED_CSV = ROOT / "data" / "processed" / "matches_vsigma_scored_v3.csv"
OUTPUT_CSV = ROOT / "data" / "processed" / "vsigma_deep_analysis_candidates.csv"
PROMOTED_RULES_PRODUCTION_CSV = ROOT / "data" / "processed" / "vsigma_promoted_rules_production_report.csv"

PRODUCTION_READY_STATUS = "PROMOTED_PRODUCTION_READY"
ACTIONABLE_RECOMMENDATIONS = {"BET", "LEAN_PLAY"}
CORE_EXECUTION_VERDICTS = {"TOP_CORE", "CORE_SHORTLIST"}
PREMIUM_RULE_TIER = "PREMIUM_EVIDENCE"
STANDARD_RULE_TIER = "STANDARD_EVIDENCE"
GENERIC_RULE_TIER = "GENERIC_BROAD"
NON_GENERIC_RULE_TIERS = {PREMIUM_RULE_TIER, STANDARD_RULE_TIER}
GENERIC_RULE_MATCH_RATE_PCT = 65.0
GENERIC_RULE_ACTIONABLE_COVERAGE_PCT = 65.0
PREMIUM_MIN_VALIDATION_WINDOWS = 2
PREMIUM_MIN_POSITIVE_WINDOW_RATE_PCT = 75.0
PREMIUM_MIN_VALIDATION_GRADED = 14
PREMIUM_MIN_VALIDATION_ROI_PCT = 12.0
PREMIUM_MIN_CURRENT_GRADED = 25
PREMIUM_MIN_CURRENT_ROI_PCT = 5.0
PROMOTED_RULE_REQUIRED_COLUMNS = [
    "rule_type",
    "metric",
    "direction",
    "threshold",
    "rule",
]

MARKET_FIT_SAFE_OK = "SAFE_OK"
MARKET_FIT_DOWNGRADED = "MARKET_FIT_DOWNGRADED"
MARKET_FIT_BLOCKED = "MARKET_FIT_BLOCKED"
FRAGILITY_AWAY_WIN_DRAW_RISK = "AWAY_WIN_DRAW_RISK"
FRAGILITY_OVER_25_SYNC_FAIL = "OVER_2_5_DAMAGE_SYNC_FAIL"
FRAGILITY_UNDER_35_AVALANCHE_RISK = "UNDER_3_5_AVALANCHE_RISK"
AVAILABILITY_SAFE = "AVAILABILITY_SAFE"
AVAILABILITY_UNCERTAIN = "AVAILABILITY_UNCERTAIN"
ABSENCE_RISK_HIGH = "ABSENCE_RISK_HIGH"
COVERAGE_TOO_WEAK_FOR_CONFIDENCE = "COVERAGE_TOO_WEAK_FOR_CONFIDENCE"
LINEUP_CONFIRMS_THESIS = "LINEUP_CONFIRMS_THESIS"
LINEUP_UNCERTAIN = "LINEUP_UNCERTAIN"
LINEUP_ATTACK_WEAKENED = "LINEUP_ATTACK_WEAKENED"
LINEUP_DEFENSE_WEAKENED = "LINEUP_DEFENSE_WEAKENED"
GOALKEEPER_UNKNOWN = "GOALKEEPER_UNKNOWN"
LINEUP_CONFIRMS_THESIS_ACTIVE = "LINEUP_CONFIRMS_THESIS_ACTIVE"
LINEUP_UNCERTAIN_ADVISORY = "LINEUP_UNCERTAIN_ADVISORY"
LINEUP_INACTIVE_NO_TIMING_EDGE = "LINEUP_INACTIVE_NO_TIMING_EDGE"
LINEUP_DEFENSE_WEAKENED_ACTIVE = "LINEUP_DEFENSE_WEAKENED_ACTIVE"
LINEUP_ATTACK_WEAKENED_ACTIVE = "LINEUP_ATTACK_WEAKENED_ACTIVE"
GOALKEEPER_UNKNOWN_ADVISORY = "GOALKEEPER_UNKNOWN_ADVISORY"


ODDS_COLS = [
    "odds_1_home_v3",
    "odds_1_draw_v3",
    "odds_1_away_v3",
    "odds_home_dnb_v3",
    "odds_away_dnb_v3",
    "odds_btts_yes_v3",
    "odds_btts_no_v3",
    "odds_over_1_5_v3",
    "odds_over_2_5_v3",
    "odds_under_3_5_v3",
]

EXTRA_COLS = [
    "tie_state_label",
    "tie_adjustment_note",
    "market_family_hint",
    "vsigma_priority",
]

RECENT_STATS_COLS = [
    "recent_stats_quality_flag",
    "recent_stats_process_score",
    "home_recent_stats_matches_used",
    "away_recent_stats_matches_used",
    "home_recent_stats_coverage_ratio",
    "away_recent_stats_coverage_ratio",
    "home_recent_shots_for_pg",
    "away_recent_shots_for_pg",
    "home_recent_shots_against_pg",
    "away_recent_shots_against_pg",
    "home_recent_sot_for_pg",
    "away_recent_sot_for_pg",
    "home_recent_sot_against_pg",
    "away_recent_sot_against_pg",
    "home_recent_possession_pct",
    "away_recent_possession_pct",
    "home_recent_corners_for_pg",
    "away_recent_corners_for_pg",
    "home_recent_corners_against_pg",
    "away_recent_corners_against_pg",
    "home_recent_fouls_pg",
    "away_recent_fouls_pg",
    "home_recent_yellow_pg",
    "away_recent_yellow_pg",
    "home_recent_offsides_pg",
    "away_recent_offsides_pg",
    "home_recent_blocked_shots_pg",
    "away_recent_blocked_shots_pg",
]

RECENT_LAB_COLS = [
    "home_recent_lab_trust_multiplier",
    "away_recent_lab_trust_multiplier",
    "recent_lab_context_score",
    "home_recent_opponent_strength_avg",
    "away_recent_opponent_strength_avg",
    "home_recent_schedule_difficulty_score",
    "away_recent_schedule_difficulty_score",
    "home_recent_schedule_quality_flag",
    "away_recent_schedule_quality_flag",
    "recent_schedule_balance_delta",
    "home_recent_anomaly_count_last5",
    "away_recent_anomaly_count_last5",
    "home_recent_clean_sample_size",
    "away_recent_clean_sample_size",
    "home_recent_anomaly_penalty",
    "away_recent_anomaly_penalty",
    "home_recent_event_coverage_flag",
    "away_recent_event_coverage_flag",
    "recent_sample_cleanliness_flag",
]

AVAILABILITY_COLS = [
    "home_injuries_count",
    "away_injuries_count",
    "home_injuries_available_flag",
    "away_injuries_available_flag",
    "home_injuries_coverage_flag",
    "away_injuries_coverage_flag",
    "home_absence_risk_score",
    "away_absence_risk_score",
    "home_absence_severity_flag",
    "away_absence_severity_flag",
    "injuries_quality_flag",
    "availability_known_risk_score",
    "availability_uncertainty_penalty",
    "availability_attack_penalty",
    "home_absences",
    "away_absences",
]

LINEUP_COLS = [
    "home_lineup_available_flag",
    "away_lineup_available_flag",
    "home_lineup_quality_flag",
    "away_lineup_quality_flag",
    "lineup_quality_flag",
    "lineup_activation_state",
    "lineup_activation_window_minutes",
    "lineup_minutes_to_kickoff",
    "lineup_timing_eligible_flag",
    "lineup_structural_confidence_flag",
    "home_lineup_known_starters_count",
    "away_lineup_known_starters_count",
    "home_lineup_bench_known_flag",
    "away_lineup_bench_known_flag",
    "home_lineup_attacker_count",
    "away_lineup_attacker_count",
    "home_lineup_defender_count",
    "away_lineup_defender_count",
    "home_lineup_midfielder_count",
    "away_lineup_midfielder_count",
    "home_lineup_goalkeeper_known_flag",
    "away_lineup_goalkeeper_known_flag",
    "home_lineup_attack_continuity_score",
    "away_lineup_attack_continuity_score",
    "home_lineup_defense_continuity_score",
    "away_lineup_defense_continuity_score",
    "lineup_confirmation_score",
    "lineup_uncertainty_penalty",
    "lineup_score_nudge",
]

COVERAGE_COLS = [
    "league_coverage_class",
    "league_data_reliability_score",
    "league_coverage_rich_flag",
    "league_has_odds_coverage",
    "league_has_fixture_stats_coverage",
    "league_has_injuries_coverage",
    "league_has_lineups_coverage",
    "league_has_predictions_coverage",
    "league_stats_reliability_multiplier",
    "league_coverage_uncertainty_penalty",
    "league_coverage_source_status",
    "league_coverage_note",
]

ODDS_STRUCTURE_COLS = [
    "odds_imp_over15",
    "odds_imp_over25",
    "odds_imp_under35",
    "odds_imp_btts_yes",
    "odds_imp_home_win",
    "odds_imp_draw",
    "odds_imp_away_win",
    "odds_imp_home_dnb",
    "odds_imp_away_dnb",
    "odds_market_support_count",
    "odds_bookmaker_support_count",
    "odds_dispersion_score",
    "odds_structure_coherence_flag",
    "odds_total_ladder_shape",
    "odds_goal_expectation_band",
    "odds_side_fragility_flag",
    "odds_btts_support_flag",
    "odds_over25_support_flag",
    "odds_over15_support_flag",
    "odds_under35_support_flag",
    "odds_market_translation_hint",
    "odds_line_aggression_flag",
    "odds_confidence_adjustment_score",
    "odds_structure_depth_status",
]


def n(row, col, default=np.nan):
    val = row[col] if col in row.index else default
    try:
        if pd.isna(val):
            return default
        return float(val)
    except Exception:
        return default


def nz(row, col, default=0.0):
    val = n(row, col, np.nan)
    if pd.isna(val):
        return default
    return float(val)


def clip(x, low, high):
    return max(low, min(high, x))


def implied_prob(odds):
    try:
        if odds is None or pd.isna(odds) or float(odds) <= 1.0:
            return np.nan
        return 1.0 / float(odds)
    except Exception:
        return np.nan


def availability_interpretation(row) -> str:
    if "injuries_quality_flag" not in row.index:
        return AVAILABILITY_SAFE
    quality = str(row.get("injuries_quality_flag", "")).strip().upper()
    home_sev = str(row.get("home_absence_severity_flag", "")).strip().upper()
    away_sev = str(row.get("away_absence_severity_flag", "")).strip().upper()
    risk = nz(row, "availability_known_risk_score")

    if quality in {"", "NONE", "SPARSE"}:
        return COVERAGE_TOO_WEAK_FOR_CONFIDENCE
    if quality == "FULL" and (home_sev == "HIGH" or away_sev == "HIGH" or risk >= 4.0):
        return ABSENCE_RISK_HIGH
    if quality == "PARTIAL":
        return AVAILABILITY_UNCERTAIN
    return AVAILABILITY_SAFE


def lineup_activation_state(row) -> str:
    state = str(row.get("lineup_activation_state", "")).strip().upper()
    if state in {"ACTIVE", "ADVISORY_ONLY", "INACTIVE"}:
        return state
    quality = str(row.get("lineup_quality_flag", "")).strip().upper()
    if quality == "NONE" or quality == "":
        return "INACTIVE"
    return "ADVISORY_ONLY"


def lineup_is_active(row) -> bool:
    return lineup_activation_state(row) == "ACTIVE"


def lineup_interpretation(row) -> str:
    if "lineup_quality_flag" not in row.index:
        return LINEUP_INACTIVE_NO_TIMING_EDGE

    quality = str(row.get("lineup_quality_flag", "")).strip().upper()
    state = lineup_activation_state(row)
    if state == "INACTIVE" or quality == "NONE":
        return LINEUP_INACTIVE_NO_TIMING_EDGE

    home_gk = n(row, "home_lineup_goalkeeper_known_flag")
    away_gk = n(row, "away_lineup_goalkeeper_known_flag")
    if (not pd.isna(home_gk) and float(home_gk) <= 0) or (not pd.isna(away_gk) and float(away_gk) <= 0):
        return GOALKEEPER_UNKNOWN_ADVISORY if state != "ACTIVE" else GOALKEEPER_UNKNOWN

    home_attack = n(row, "home_lineup_attack_continuity_score")
    away_attack = n(row, "away_lineup_attack_continuity_score")
    if (
        (not pd.isna(home_attack) and float(home_attack) <= -0.12)
        or (not pd.isna(away_attack) and float(away_attack) <= -0.12)
    ):
        return LINEUP_ATTACK_WEAKENED_ACTIVE if state == "ACTIVE" else LINEUP_UNCERTAIN_ADVISORY

    home_defense = n(row, "home_lineup_defense_continuity_score")
    away_defense = n(row, "away_lineup_defense_continuity_score")
    if (
        (not pd.isna(home_defense) and float(home_defense) <= -0.12)
        or (not pd.isna(away_defense) and float(away_defense) <= -0.12)
    ):
        return LINEUP_DEFENSE_WEAKENED_ACTIVE if state == "ACTIVE" else LINEUP_UNCERTAIN_ADVISORY

    if state == "ACTIVE" and quality == "FULL" and nz(row, "lineup_confirmation_score") >= 0.10:
        return LINEUP_CONFIRMS_THESIS_ACTIVE
    return LINEUP_UNCERTAIN_ADVISORY


def lineup_goal_adjustment(row, side: str) -> float:
    if not lineup_is_active(row):
        return 0.0
    opponent = "away" if side == "home" else "home"
    attack = nz(row, f"{side}_lineup_attack_continuity_score")
    opponent_defense = nz(row, f"{opponent}_lineup_defense_continuity_score")
    return clip((attack * 0.10) - (opponent_defense * 0.04), -0.05, 0.05)


def lineup_market_fit_adjustment(row, market: str) -> float:
    if not lineup_is_active(row):
        return 0.0

    home_attack = nz(row, "home_lineup_attack_continuity_score")
    away_attack = nz(row, "away_lineup_attack_continuity_score")
    home_defense = nz(row, "home_lineup_defense_continuity_score")
    away_defense = nz(row, "away_lineup_defense_continuity_score")
    attack_avg = (home_attack + away_attack) / 2.0
    defense_avg = (home_defense + away_defense) / 2.0
    adjustment = 0.0

    if market in {"OVER_1_5", "OVER_2_5", "BTTS_YES"}:
        if attack_avg <= -0.12:
            adjustment -= 0.02
        elif attack_avg >= 0.14:
            adjustment += 0.01

    if market in {"UNDER_3_5", "BTTS_NO"}:
        if defense_avg <= -0.12:
            adjustment -= 0.02
        elif defense_avg >= 0.14:
            adjustment += 0.01

    if market in {"HOME_WIN", "HOME_DNB", "HOME_TEAM_OVER_0_5"} and home_attack <= -0.12:
        adjustment -= 0.015
    if market in {"AWAY_WIN", "AWAY_DNB", "AWAY_TEAM_OVER_0_5"} and away_attack <= -0.12:
        adjustment -= 0.015

    return round(float(np.clip(adjustment, -0.025, 0.015)), 4)


def side_coverage_weight(row, side: str) -> float:
    coverage = str(row.get(f"{side}_injuries_coverage_flag", "")).strip().upper()
    return {
        "FULL": 1.0,
        "PARTIAL": 0.45,
        "SPARSE": 0.20,
        "NONE": 0.0,
        "": 0.0,
    }.get(coverage, 0.0)


def side_reliable_high_absence(row, side: str) -> bool:
    quality = str(row.get("injuries_quality_flag", "")).strip().upper()
    severity = str(row.get(f"{side}_absence_severity_flag", "")).strip().upper()
    return bool(quality == "FULL" and (severity == "HIGH" or nz(row, f"{side}_absence_risk_score") >= 3.0))


def side_absence_goal_penalty(row, side: str) -> float:
    return 0.0


def confidence_band(score: float) -> str:
    if score >= 82:
        return "HIGH"
    if score >= 70:
        return "MEDIUM_HIGH"
    if score >= 58:
        return "MEDIUM"
    return "LOW"


def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def poisson_market_probs(home_lambda: float, away_lambda: float, max_goals: int = 7) -> dict:
    matrix = {}
    total_mass = 0.0

    for h in range(max_goals + 1):
        ph = poisson_pmf(h, home_lambda)
        for a in range(max_goals + 1):
            pa = poisson_pmf(a, away_lambda)
            p = ph * pa
            matrix[(h, a)] = p
            total_mass += p

    if total_mass <= 0:
        total_mass = 1.0

    for k in matrix:
        matrix[k] /= total_mass

    home_win = sum(p for (h, a), p in matrix.items() if h > a)
    draw = sum(p for (h, a), p in matrix.items() if h == a)
    away_win = sum(p for (h, a), p in matrix.items() if h < a)

    over_15 = sum(p for (h, a), p in matrix.items() if (h + a) >= 2)
    over_25 = sum(p for (h, a), p in matrix.items() if (h + a) >= 3)
    under_35 = sum(p for (h, a), p in matrix.items() if (h + a) <= 3)

    home_score_yes = sum(p for (h, a), p in matrix.items() if h >= 1)
    away_score_yes = sum(p for (h, a), p in matrix.items() if a >= 1)
    btts_yes = sum(p for (h, a), p in matrix.items() if h >= 1 and a >= 1)
    btts_no = 1.0 - btts_yes

    return {
        "HOME_WIN": round(home_win, 4),
        "DRAW": round(draw, 4),
        "AWAY_WIN": round(away_win, 4),
        "OVER_1_5": round(over_15, 4),
        "OVER_2_5": round(over_25, 4),
        "UNDER_3_5": round(under_35, 4),
        "BTTS_YES": round(btts_yes, 4),
        "BTTS_NO": round(btts_no, 4),
        "HOME_TEAM_OVER_0_5": round(home_score_yes, 4),
        "AWAY_TEAM_OVER_0_5": round(away_score_yes, 4),
        "HOME_DNB": round(home_win, 4),
        "AWAY_DNB": round(away_win, 4),
    }


def project_goals(row) -> tuple[float, float]:
    home_gf = nz(row, "home_goals_for_pg")
    away_gf = nz(row, "away_goals_for_pg")
    home_ga = nz(row, "home_goals_against_pg")
    away_ga = nz(row, "away_goals_against_pg")

    home_scored = nz(row, "home_scored_rate")
    away_scored = nz(row, "away_scored_rate")
    home_clean = nz(row, "home_clean_sheet_rate")
    away_clean = nz(row, "away_clean_sheet_rate")

    home_form = nz(row, "home_form_pts")
    away_form = nz(row, "away_form_pts")
    home_recent_trust = clip(nz(row, "home_recent_lab_trust_multiplier", 1.0), 0.78, 1.08)
    away_recent_trust = clip(nz(row, "away_recent_lab_trust_multiplier", 1.0), 0.78, 1.08)

    home_rank = n(row, "home_rank")
    away_rank = n(row, "away_rank")

    proj_home = (0.58 * home_gf * home_recent_trust) + 0.42 * away_ga
    proj_away = (0.58 * away_gf * away_recent_trust) + 0.42 * home_ga

    proj_home += 0.35 * ((home_scored - 0.5) * home_recent_trust)
    proj_away += 0.35 * ((away_scored - 0.5) * away_recent_trust)

    proj_home -= 0.20 * max(0.0, away_clean - 0.20)
    proj_away -= 0.20 * max(0.0, home_clean - 0.20)

    proj_home += 0.15 * ((home_form - 1.33) * home_recent_trust)
    proj_away += 0.15 * ((away_form - 1.33) * away_recent_trust)

    if not pd.isna(home_rank) and not pd.isna(away_rank):
        rank_delta = away_rank - home_rank
        proj_home += 0.03 * rank_delta
        proj_away -= 0.03 * rank_delta

    home_stats_cov = nz(row, "home_recent_stats_coverage_ratio")
    away_stats_cov = nz(row, "away_recent_stats_coverage_ratio")
    stats_multiplier = fixture_stats_reliability_multiplier(row)
    if home_stats_cov > 0:
        home_process = (
            nz(row, "home_recent_sot_for_pg") * 0.08
            + nz(row, "away_recent_sot_against_pg") * 0.04
            + nz(row, "home_recent_shots_for_pg") * 0.01
        )
        proj_home += min(0.28, home_process * home_recent_trust * min(home_stats_cov, 1.0) * stats_multiplier)
    if away_stats_cov > 0:
        away_process = (
            nz(row, "away_recent_sot_for_pg") * 0.08
            + nz(row, "home_recent_sot_against_pg") * 0.04
            + nz(row, "away_recent_shots_for_pg") * 0.01
        )
        proj_away += min(0.28, away_process * away_recent_trust * min(away_stats_cov, 1.0) * stats_multiplier)

    proj_home -= side_absence_goal_penalty(row, "home")
    proj_away -= side_absence_goal_penalty(row, "away")
    proj_home += lineup_goal_adjustment(row, "home")
    proj_away += lineup_goal_adjustment(row, "away")

    tie_label = str(row.get("tie_state_label", ""))
    if tie_label in {"HOME_TRAILING", "AWAY_TRAILING"}:
        proj_home += 0.08
        proj_away += 0.08
    elif tie_label == "LEVEL_TIE":
        proj_home += 0.04
        proj_away += 0.04

    proj_home = clip(proj_home, 0.35, 3.20)
    proj_away = clip(proj_away, 0.35, 3.20)

    return round(proj_home, 2), round(proj_away, 2)


def side_bias(row, proj_home: float, proj_away: float) -> float:
    bias = proj_home - proj_away

    team_edge_raw = n(row, "team_edge_raw")
    if not pd.isna(team_edge_raw):
        bias += 0.06 * float(team_edge_raw)

    home_form = nz(row, "home_form_pts")
    away_form = nz(row, "away_form_pts")
    bias += 0.10 * (home_form - away_form)

    home_scored = nz(row, "home_scored_rate")
    away_scored = nz(row, "away_scored_rate")
    bias += 0.10 * (home_scored - away_scored)

    home_sot = n(row, "home_recent_sot_for_pg")
    away_sot = n(row, "away_recent_sot_for_pg")
    if not pd.isna(home_sot) and not pd.isna(away_sot):
        coverage = min(nz(row, "home_recent_stats_coverage_ratio"), nz(row, "away_recent_stats_coverage_ratio"))
        bias += 0.04 * (float(home_sot) - float(away_sot)) * coverage * fixture_stats_reliability_multiplier(row)

    return round(bias, 2)


def likely_scoreline(row) -> str:
    ph, pa = project_goals(row)
    bias = side_bias(row, ph, pa)
    total = ph + pa

    if bias >= 0.55:
        if total <= 2.35:
            return "1-0 / 2-0 / 2-1"
        if total <= 3.00:
            return "2-1 / 1-0 / 2-0"
        return "2-1 / 3-1 / 2-2"

    if bias <= -0.55:
        if total <= 2.35:
            return "0-1 / 0-2 / 1-2"
        if total <= 3.00:
            return "1-2 / 0-1 / 1-1"
        return "1-2 / 1-3 / 2-2"

    if total <= 2.20:
        return "1-1 / 1-0 / 0-1"
    if total <= 3.00:
        return "1-1 / 2-1 / 1-2"
    return "2-2 / 2-1 / 1-2"


def market_to_odds_col(market: str) -> str | None:
    mapping = {
        "HOME_WIN": "odds_1_home_v3",
        "AWAY_WIN": "odds_1_away_v3",
        "HOME_DNB": "odds_home_dnb_v3",
        "AWAY_DNB": "odds_away_dnb_v3",
        "BTTS_YES": "odds_btts_yes_v3",
        "BTTS_NO": "odds_btts_no_v3",
        "OVER_1_5": "odds_over_1_5_v3",
        "OVER_2_5": "odds_over_2_5_v3",
        "UNDER_3_5": "odds_under_3_5_v3",
    }
    return mapping.get(market)


def candidate_markets(row, probs: dict) -> list[str]:
    hint = str(row.get("market_family_hint", ""))
    tie_label = str(row.get("tie_state_label", ""))

    if "HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK" in hint:
        candidates = ["HOME_WIN", "HOME_DNB", "OVER_1_5", "OVER_2_5", "BTTS_YES", "UNDER_3_5"]
    elif "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK" in hint:
        candidates = ["AWAY_WIN", "AWAY_DNB", "OVER_1_5", "OVER_2_5", "BTTS_YES", "UNDER_3_5"]
    elif "OVER_OR_BTTS_CHECK" in hint:
        candidates = ["OVER_1_5", "OVER_2_5", "BTTS_YES", "UNDER_3_5", "HOME_WIN", "AWAY_WIN"]
    elif "UNDER_OR_TEAM_TOTAL_UNDER_CHECK" in hint:
        candidates = ["UNDER_3_5", "OVER_1_5", "BTTS_NO", "HOME_WIN", "AWAY_WIN"]
    else:
        candidates = ["OVER_1_5", "OVER_2_5", "BTTS_YES", "UNDER_3_5", "HOME_WIN", "AWAY_WIN"]

    if tie_label in {"HOME_TRAILING", "AWAY_TRAILING"}:
        candidates = [m for m in candidates if m != "BTTS_NO"]
        if "UNDER_3_5" in candidates and probs.get("OVER_1_5", 0) >= 0.70:
            candidates.remove("UNDER_3_5")
            candidates.append("UNDER_3_5")

    return list(dict.fromkeys(candidates))


def market_fit_bonus(row, market: str, probs: dict) -> float:
    hint = str(row.get("market_family_hint", ""))
    tie_label = str(row.get("tie_state_label", ""))
    bonus = 0.0

    if "OVER_OR_BTTS_CHECK" in hint:
        if market == "OVER_1_5":
            bonus += 0.05
        elif market == "OVER_2_5":
            bonus += 0.03
        elif market == "BTTS_YES":
            bonus += 0.02

    if "HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK" in hint:
        if market == "HOME_DNB":
            bonus += 0.04
        elif market == "HOME_WIN":
            bonus += 0.02

    if "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK" in hint:
        if market == "AWAY_DNB":
            bonus += 0.04
        elif market == "AWAY_WIN":
            bonus += 0.02

    if tie_label in {"HOME_TRAILING", "AWAY_TRAILING"}:
        if market in {"OVER_1_5", "OVER_2_5", "BTTS_YES"}:
            bonus += 0.05
        elif market == "UNDER_3_5":
            bonus -= 0.04

    bonus += lineup_market_fit_adjustment(row, market)
    bonus += odds_structure_market_adjustment(row, market)

    return bonus


def odds_depth_active(row) -> bool:
    coherence = str(row.get("odds_structure_coherence_flag", "")).strip().upper()
    return coherence in {"RICH_COHERENT", "RICH_MIXED", "RICH_NOISY"}


def odds_structure_market_adjustment(row, market: str) -> float:
    if not odds_depth_active(row):
        return 0.0

    market = str(market).strip().upper()
    coherence = str(row.get("odds_structure_coherence_flag", "")).strip().upper()
    ladder = str(row.get("odds_total_ladder_shape", "")).strip().upper()
    hint = str(row.get("odds_market_translation_hint", "")).strip().upper()
    line = str(row.get("odds_line_aggression_flag", "")).strip().upper()
    side_fragility = str(row.get("odds_side_fragility_flag", "")).strip().upper()
    btts_flag = str(row.get("odds_btts_support_flag", "")).strip().upper()
    over25_flag = str(row.get("odds_over25_support_flag", "")).strip().upper()
    over15_flag = str(row.get("odds_over15_support_flag", "")).strip().upper()
    under35_flag = str(row.get("odds_under35_support_flag", "")).strip().upper()

    adjustment = 0.0

    if market == "OVER_2_5":
        if line in {"PREFER_OVER_1_5", "AVOID_AGGRESSIVE_OVERS"} or hint == "PREFER_MILDER_TOTAL":
            adjustment -= 0.060
        elif over25_flag == "SUPPORTED" and ladder in {"BROAD_GOALS", "WIDE_GOALS"}:
            adjustment += 0.025
    elif market == "OVER_1_5":
        if line in {"PREFER_OVER_1_5", "AVOID_AGGRESSIVE_OVERS"} or hint == "PREFER_MILDER_TOTAL":
            adjustment += 0.035
        elif over15_flag == "WEAK" and ladder == "LOW_GOALS":
            adjustment -= 0.015
    elif market == "UNDER_3_5":
        if under35_flag == "SUPPORTED" and ladder in {"LOW_GOALS", "MILD_GOALS"}:
            adjustment += 0.020
        elif ladder == "WIDE_GOALS":
            adjustment -= 0.035
    elif market in {"BTTS_YES", "BTTS_NO"}:
        if btts_flag == "SUPPORTED" and market == "BTTS_YES":
            adjustment += 0.015
        elif btts_flag in {"WEAK", "UNKNOWN"} and market == "BTTS_YES":
            adjustment -= 0.035
        elif btts_flag == "SUPPORTED" and market == "BTTS_NO":
            adjustment -= 0.025
    elif market in {"HOME_WIN", "AWAY_WIN"}:
        if side_fragility in {"DRAW_LIVE_FRAGILITY", "BALANCED_SIDE_PRICE"}:
            adjustment -= 0.035
        elif side_fragility == "SIDE_PRICE_CLEANER":
            adjustment += 0.010
    elif market in {"HOME_DNB", "AWAY_DNB"}:
        if side_fragility == "DRAW_LIVE_FRAGILITY":
            adjustment += 0.010

    if coherence == "RICH_NOISY":
        adjustment -= 0.010

    return round(float(np.clip(adjustment, -0.060, 0.035)), 4)


def choose_primary_alt(row) -> tuple[str, str, dict]:
    ph, pa = project_goals(row)
    probs = poisson_market_probs(ph, pa)

    width_bonus_map = {
        "OVER_1_5": 0.12,
        "UNDER_3_5": 0.10,
        "HOME_DNB": 0.08,
        "AWAY_DNB": 0.08,
        "HOME_TEAM_OVER_0_5": 0.07,
        "AWAY_TEAM_OVER_0_5": 0.07,
        "OVER_2_5": 0.03,
        "BTTS_YES": 0.02,
        "HOME_WIN": -0.02,
        "AWAY_WIN": -0.02,
        "BTTS_NO": -0.03,
    }

    scored_candidates = []

    for market in candidate_markets(row, probs):
        prob = probs.get(market, np.nan)
        odds_col = market_to_odds_col(market)
        odds_val = n(row, odds_col) if odds_col else np.nan
        imp = implied_prob(odds_val)

        fit_bonus = market_fit_bonus(row, market, probs)
        width_bonus = width_bonus_map.get(market, 0.0)

        price_quality = 0.0
        if not pd.isna(odds_val):
            ov = float(odds_val)
            if 1.40 <= ov <= 3.50:
                price_quality += 0.04
            elif ov < 1.30:
                price_quality -= 0.08
            elif ov > 4.50:
                price_quality -= 0.04
            if official_coverage_loaded_row(row) and coverage_flag(row, "league_has_odds_coverage") < 1:
                price_quality -= 0.02

        missing_odds_penalty = -0.12 if pd.isna(imp) else 0.0

        if pd.isna(imp):
            edge = np.nan
            score = (
                prob * 42
                + fit_bonus * 100
                + width_bonus * 100
                + price_quality * 100
                + missing_odds_penalty * 100
            )
        else:
            edge = prob - imp
            score = (
                edge * 75
                + prob * 28
                + fit_bonus * 100
                + width_bonus * 100
                + price_quality * 100
            )

        scored_candidates.append(
            {
                "market": market,
                "prob": prob,
                "odds": odds_val,
                "implied": imp,
                "edge": edge,
                "score": score,
            }
        )

    scored_candidates = sorted(scored_candidates, key=lambda x: x["score"], reverse=True)

    priced_non_negative = [
        x for x in scored_candidates
        if not pd.isna(x["implied"]) and not pd.isna(x["edge"]) and x["edge"] >= -0.01
    ]
    if priced_non_negative:
        best_priced_non_negative = sorted(priced_non_negative, key=lambda x: x["score"], reverse=True)[0]
        if not pd.isna(scored_candidates[0]["edge"]) and scored_candidates[0]["edge"] < -0.01:
            scored_candidates = [best_priced_non_negative] + [
                x for x in scored_candidates if x["market"] != best_priced_non_negative["market"]
            ]

    if len(scored_candidates) >= 2:
        a = scored_candidates[0]
        b = scored_candidates[1]
        if pd.isna(a["implied"]) and (not pd.isna(b["implied"])) and (pd.isna(b["edge"]) is False) and b["edge"] >= -0.01:
            scored_candidates = [b, a] + scored_candidates[2:]

    primary = scored_candidates[0]
    alt = scored_candidates[1] if len(scored_candidates) > 1 else scored_candidates[0]

    meta = {
        "primary_prob": round(primary["prob"], 4),
        "primary_odds": primary["odds"],
        "primary_implied": primary["implied"],
        "primary_edge": primary["edge"],
        "alt_prob": round(alt["prob"], 4),
        "alt_odds": alt["odds"],
        "alt_implied": alt["implied"],
        "alt_edge": alt["edge"],
    }

    return primary["market"], alt["market"], meta


def reasons(row, meta: dict) -> tuple[str, str, str]:
    ph, pa = project_goals(row)
    bias = side_bias(row, ph, pa)

    r1 = f"Proj goles: local {ph:.2f} | visitante {pa:.2f}"
    r2 = (
        f"Market edge primario: prob {meta['primary_prob']:.3f}"
        + (
            f" | impl {meta['primary_implied']:.3f} | edge {meta['primary_edge']:+.3f}"
            if not pd.isna(meta["primary_implied"])
            else " | sin cuota útil, fallback modelo"
        )
    )
    stats_note = (
        f"stats={row.get('recent_stats_quality_flag', 'NA')}"
        f" hSOT={n(row, 'home_recent_sot_for_pg'):.2f}"
        f" aSOT={n(row, 'away_recent_sot_for_pg'):.2f}"
        if str(row.get("recent_stats_quality_flag", "")) not in {"", "nan"}
        else "stats=NA"
    )
    lab_note = (
        f"lab_sched={row.get('home_recent_schedule_quality_flag', 'NA')}/{row.get('away_recent_schedule_quality_flag', 'NA')}"
        f" trust={n(row, 'home_recent_lab_trust_multiplier', 1.0):.2f}/{n(row, 'away_recent_lab_trust_multiplier', 1.0):.2f}"
        f" clean={row.get('recent_sample_cleanliness_flag', 'NA')}"
        if "home_recent_lab_trust_multiplier" in row.index
        else "lab_recent=NA"
    )
    availability = availability_interpretation(row)
    availability_note = (
        f"availability={availability}"
        f" inj={row.get('injuries_quality_flag', 'NA')}"
        f" hRisk={n(row, 'home_absence_risk_score'):.2f}"
        f" aRisk={n(row, 'away_absence_risk_score'):.2f}"
    )
    lineup = lineup_interpretation(row)
    lineup_note = (
        f"lineup={lineup}"
        f" state={lineup_activation_state(row)}"
        f" q={row.get('lineup_quality_flag', 'NA')}"
        f" hXI={n(row, 'home_lineup_known_starters_count'):.0f}"
        f" aXI={n(row, 'away_lineup_known_starters_count'):.0f}"
        f" conf={n(row, 'lineup_confirmation_score'):.2f}"
    )
    coverage_note = (
        f"coverage={row.get('league_coverage_class', 'COVERAGE_UNKNOWN')}"
        f" rel={n(row, 'league_data_reliability_score', 1.0):.2f}"
        f" stats={row.get('league_has_fixture_stats_coverage', 'NA')}"
        f" odds={row.get('league_has_odds_coverage', 'NA')}"
        f" inj={row.get('league_has_injuries_coverage', 'NA')}"
        f" lineups={row.get('league_has_lineups_coverage', 'NA')}"
    )
    odds_depth_note = (
        f"odds_depth={row.get('odds_structure_coherence_flag', 'NA')}"
        f" ladder={row.get('odds_total_ladder_shape', 'NA')}"
        f" hint={row.get('odds_market_translation_hint', 'NA')}"
        f" line={row.get('odds_line_aggression_flag', 'NA')}"
        if "odds_structure_coherence_flag" in row.index
        else "odds_depth=NA"
    )
    r3 = (
        f"Bias lado: {bias:+.2f} | tie={row.get('tie_state_label', 'NA')} | "
        f"hint={row.get('market_family_hint', '')} | {coverage_note} | {stats_note} | {lab_note} | "
        f"{odds_depth_note} | {availability_note} | {lineup_note}"
    )
    return r1, r2, r3


def analysis_label(bucket: str) -> str:
    if bucket == "TOP_CORE":
        return "TOP_CORE"
    if bucket == "CORE_SHORTLIST":
        return "CORE"
    return "WATCH"


def edge_floor_band(edge) -> str:
    if pd.isna(edge):
        return "NO_ODDS"
    edge = float(edge)
    if edge < 0.00:
        return "NEGATIVE"
    if edge < 0.02:
        return "THIN"
    if edge < 0.05:
        return "PLAYABLE"
    return "STRONG"


def execution_verdict(row) -> tuple[str, str]:
    edge = row.get("primary_edge", np.nan)
    shortlist_bucket = str(row.get("shortlist_bucket", ""))
    confidence = str(row.get("confidence_band", ""))

    band = edge_floor_band(edge)

    if band == "NEGATIVE":
        return "NO_BET", "NO_BET"
    if band == "THIN":
        return "WATCH", "WATCH"
    if band == "PLAYABLE":
        if shortlist_bucket == "TOP_CORE":
            return "CORE_SHORTLIST", "LEAN_PLAY"
        return "WATCH", "LEAN_PLAY"
    if band == "STRONG":
        if shortlist_bucket == "TOP_CORE":
            return "TOP_CORE", "BET"
        if shortlist_bucket == "CORE_SHORTLIST":
            return "CORE_SHORTLIST", "BET"
        return "WATCH", "BET"

    if confidence in {"HIGH", "MEDIUM_HIGH"} and shortlist_bucket in {"TOP_CORE", "CORE_SHORTLIST"}:
        return shortlist_bucket, "MODEL_ONLY"
    return "WATCH", "MODEL_ONLY"


def norm_rule_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def safe_float(value, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def official_coverage_loaded_row(row: pd.Series) -> bool:
    return norm_rule_text(row.get("league_coverage_source_status")).startswith("OFFICIAL_API")


def coverage_flag(row: pd.Series, col: str, default: float = 1.0) -> float:
    value = safe_float(row.get(col), np.nan)
    if pd.isna(value):
        return default
    return float(np.clip(value, 0.0, 1.0))


def fixture_stats_reliability_multiplier(row: pd.Series) -> float:
    if not official_coverage_loaded_row(row):
        return 1.0
    reliability = safe_float(row.get("league_data_reliability_score"), 1.0)
    return float(np.clip(reliability, 0.4, 1.0)) * coverage_flag(row, "league_has_fixture_stats_coverage")


def coverage_confidence_penalty(row: pd.Series) -> float:
    if not official_coverage_loaded_row(row):
        return 0.0
    coverage_class = norm_rule_text(row.get("league_coverage_class"))
    return {
        "COVERAGE_RICH": 0.0,
        "COVERAGE_GOOD": 0.0,
        "COVERAGE_PARTIAL": 0.75,
        "COVERAGE_THIN": 2.0,
        "COVERAGE_MINIMAL": 3.0,
    }.get(coverage_class, 0.0)


def thin_coverage_governance_caution(row: pd.Series) -> bool:
    if not official_coverage_loaded_row(row):
        return False
    if norm_rule_text(row.get("league_coverage_class")) not in {"COVERAGE_THIN", "COVERAGE_MINIMAL"}:
        return False
    strong_edge = safe_float(row.get("primary_edge"), 0.0) >= 0.12
    strong_prob = safe_float(row.get("primary_model_prob"), 0.0) >= 0.76
    core = norm_rule_text(row.get("base_execution_verdict")) in CORE_EXECUTION_VERDICTS
    return not (strong_edge and strong_prob and core)


def read_optional_float(row: pd.Series, columns: list[str], default: float = np.nan) -> float:
    for col in columns:
        if col in row.index:
            value = n(row, col, np.nan)
            if not pd.isna(value):
                return float(value)
    return default


PROJECTED_GOALS_RE = re.compile(
    r"Proj\s+goles:\s*local\s+([0-9]+(?:[.,][0-9]+)?)\s*\|\s*visitante\s+([0-9]+(?:[.,][0-9]+)?)",
    re.IGNORECASE,
)


def parse_projected_goals_from_reason(value: object) -> tuple[float, float]:
    if pd.isna(value):
        return np.nan, np.nan
    match = PROJECTED_GOALS_RE.search(str(value))
    if not match:
        return np.nan, np.nan
    try:
        return float(match.group(1).replace(",", ".")), float(match.group(2).replace(",", "."))
    except ValueError:
        return np.nan, np.nan


def execution_projected_goals(row: pd.Series) -> tuple[float, float]:
    home = read_optional_float(
        row,
        [
            "projected_home_goals",
            "execution_projected_home_goals",
            "proj_home_goals",
            "home_projected_goals",
        ],
    )
    away = read_optional_float(
        row,
        [
            "projected_away_goals",
            "execution_projected_away_goals",
            "proj_away_goals",
            "away_projected_goals",
        ],
    )
    if not pd.isna(home) and not pd.isna(away):
        return round(home, 2), round(away, 2)

    parsed_home, parsed_away = parse_projected_goals_from_reason(row.get("reason_1", ""))
    if not pd.isna(parsed_home) and not pd.isna(parsed_away):
        return round(parsed_home, 2), round(parsed_away, 2)

    required = [
        "home_goals_for_pg",
        "away_goals_for_pg",
        "home_goals_against_pg",
        "away_goals_against_pg",
    ]
    if all(col in row.index for col in required):
        return project_goals(row)

    return np.nan, np.nan


def has_usable_odds(value: object) -> bool:
    odds = safe_float(value, np.nan)
    return bool(not pd.isna(odds) and odds > 1.0)


def is_currently_actionable(row: pd.Series) -> bool:
    return norm_rule_text(row.get("final_recommendation")) in ACTIONABLE_RECOMMENDATIONS


def is_premium_governed_actionable(row: pd.Series) -> bool:
    return (
        norm_rule_text(row.get("production_governance_status")) == "APPROVED_BY_PREMIUM_PROMOTED_RULE"
        and norm_rule_text(row.get("final_recommendation")) == "BET"
    )


def likely_scoreline_has_avalanche_mode(value: object) -> bool:
    if pd.isna(value):
        return False
    for home_text, away_text in re.findall(r"(\d+)\s*-\s*(\d+)", str(value)):
        home = int(home_text)
        away = int(away_text)
        if max(home, away) >= 3 and abs(home - away) >= 2:
            return True
    return False


def safer_market_hint(row: pd.Series, fallback: str = "") -> str:
    market_alt = norm_rule_text(row.get("market_alt"))
    if market_alt in {"OVER_1_5", "HOME_DNB", "AWAY_DNB"}:
        return market_alt
    return fallback


def away_win_passes_hard_gate(row: pd.Series, projected_home: float, projected_away: float) -> bool:
    projected_strength_ok = True
    if not pd.isna(projected_home) and not pd.isna(projected_away):
        projected_strength_ok = projected_away >= 1.80 and (projected_away - projected_home) >= 0.35

    return bool(
        is_premium_governed_actionable(row)
        and norm_rule_text(row.get("base_execution_verdict")) in CORE_EXECUTION_VERDICTS
        and safe_float(row.get("primary_edge"), np.nan) > 0
        and has_usable_odds(row.get("primary_odds_used"))
        and safe_float(row.get("primary_model_prob"), np.nan) >= 0.79
        and safe_float(row.get("primary_edge"), np.nan) >= 0.16
        and projected_strength_ok
    )


def over_25_passes_sync_gate(projected_home: float, projected_away: float) -> bool:
    if pd.isna(projected_home) or pd.isna(projected_away):
        return False
    total = projected_home + projected_away
    return bool(
        total >= 3.30
        or (max(projected_home, projected_away) >= 2.00 and min(projected_home, projected_away) >= 0.80)
    )


def row_has_over_25_process_support(row: pd.Series) -> bool:
    coverage = min(nz(row, "home_recent_stats_coverage_ratio"), nz(row, "away_recent_stats_coverage_ratio"))
    if coverage < 0.4:
        return False
    sot_total = nz(row, "home_recent_sot_for_pg") + nz(row, "away_recent_sot_for_pg")
    shots_total = nz(row, "home_recent_shots_for_pg") + nz(row, "away_recent_shots_for_pg")
    return bool(sot_total >= 8.0 or shots_total >= 24.0)


def under_35_has_avalanche_risk(row: pd.Series, projected_home: float, projected_away: float) -> bool:
    if not pd.isna(projected_home) and not pd.isna(projected_away):
        total = projected_home + projected_away
        if total >= 3.20 or max(projected_home, projected_away) >= 2.40:
            return True
    coverage = min(nz(row, "home_recent_stats_coverage_ratio"), nz(row, "away_recent_stats_coverage_ratio"))
    if coverage >= 0.4:
        sot_total = nz(row, "home_recent_sot_for_pg") + nz(row, "away_recent_sot_for_pg")
        if sot_total >= 9.0:
            return True
    return likely_scoreline_has_avalanche_mode(row.get("likely_scoreline"))


def availability_requires_execution_downgrade(row: pd.Series, market: str) -> tuple[bool, str]:
    # Advisory mode: availability remains in reasoning, but never hard-downgrades
    # an otherwise actionable execution market.
    return False, ""


def apply_execution_market_fit_hardening(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in [
        "execution_fragility_reason",
        "execution_market_fit_status",
        "execution_market_fit_note",
        "execution_preferred_safer_market",
    ]:
        if col not in out.columns:
            out[col] = ""

    statuses: list[str] = []
    reasons: list[str] = []
    notes: list[str] = []
    safer_markets: list[str] = []
    projected_home_values: list[float] = []
    projected_away_values: list[float] = []

    for _, row in out.iterrows():
        projected_home, projected_away = execution_projected_goals(row)
        projected_home_values.append(projected_home)
        projected_away_values.append(projected_away)

        status = MARKET_FIT_SAFE_OK
        reason = ""
        note = "Execution market translation passed hardening gates."
        preferred = ""

        market = norm_rule_text(row.get("market_primary"))
        actionable = is_currently_actionable(row)
        availability_downgrade, availability_reason = availability_requires_execution_downgrade(row, market)

        if actionable and availability_downgrade:
            status = MARKET_FIT_DOWNGRADED
            reason = availability_reason
            note = "Availability coverage/risk is too weak for this role-sensitive execution market."
            preferred = safer_market_hint(row, "OVER_1_5" if market in {"OVER_2_5", "BTTS_YES"} else "")
        elif actionable and market == "AWAY_WIN" and not away_win_passes_hard_gate(row, projected_home, projected_away):
            status = MARKET_FIT_DOWNGRADED
            reason = FRAGILITY_AWAY_WIN_DRAW_RISK
            note = (
                "AWAY_WIN requires premium governance, core base verdict, usable odds, "
                "and strict model probability/edge strength."
            )
            preferred = safer_market_hint(row, "AWAY_DNB" if norm_rule_text(row.get("market_alt")) == "AWAY_DNB" else "")
        elif (
            actionable
            and market == "OVER_2_5"
            and not (
                over_25_passes_sync_gate(projected_home, projected_away)
                or row_has_over_25_process_support(row)
            )
        ):
            status = MARKET_FIT_DOWNGRADED
            reason = FRAGILITY_OVER_25_SYNC_FAIL
            note = "OVER_2_5 failed the synchronized 3+ goal path gate."
            preferred = safer_market_hint(row, "OVER_1_5")
        elif actionable and market == "UNDER_3_5" and under_35_has_avalanche_risk(row, projected_home, projected_away):
            status = MARKET_FIT_BLOCKED
            reason = FRAGILITY_UNDER_35_AVALANCHE_RISK
            note = "UNDER_3_5 blocked because projected favorite/total profile creates avalanche risk."
            preferred = safer_market_hint(row, "")

        statuses.append(status)
        reasons.append(reason)
        notes.append(note)
        safer_markets.append(preferred)

    out["projected_home_goals"] = projected_home_values
    out["projected_away_goals"] = projected_away_values
    out["projected_total_goals"] = [
        round(home + away, 2) if not pd.isna(home) and not pd.isna(away) else np.nan
        for home, away in zip(projected_home_values, projected_away_values)
    ]
    out["execution_fragility_reason"] = reasons
    out["execution_market_fit_status"] = statuses
    out["execution_market_fit_note"] = notes
    out["execution_preferred_safer_market"] = safer_markets

    downgrade_mask = out["execution_market_fit_status"].isin({MARKET_FIT_DOWNGRADED, MARKET_FIT_BLOCKED})
    out.loc[downgrade_mask, "execution_verdict"] = "WATCH"
    out.loc[downgrade_mask, "final_recommendation"] = "WATCH"

    return out


def infer_promoted_rule_tier(rule_row: pd.Series) -> str:
    explicit_tier = norm_rule_text(rule_row.get("production_rule_tier"))
    if explicit_tier:
        return explicit_tier

    current_match_rate = safe_float(rule_row.get("current_match_rate_pct"), np.nan)
    actionable_coverage = safe_float(rule_row.get("current_actionable_coverage_pct"), np.nan)
    if (
        not pd.isna(current_match_rate)
        and current_match_rate >= GENERIC_RULE_MATCH_RATE_PCT
    ) or (
        not pd.isna(actionable_coverage)
        and actionable_coverage >= GENERIC_RULE_ACTIONABLE_COVERAGE_PCT
    ):
        return GENERIC_RULE_TIER

    validation_windows = safe_float(rule_row.get("validation_windows"))
    positive_window_rate = safe_float(rule_row.get("validation_positive_window_rate_pct"))
    validation_graded = safe_float(rule_row.get("validation_graded_bets"))
    validation_roi = safe_float(rule_row.get("validation_roi_pct"))
    current_graded = safe_float(rule_row.get("current_graded_bets"))
    current_roi = safe_float(rule_row.get("current_roi_pct"))

    premium = (
        validation_windows >= PREMIUM_MIN_VALIDATION_WINDOWS
        and positive_window_rate >= PREMIUM_MIN_POSITIVE_WINDOW_RATE_PCT
        and validation_graded >= PREMIUM_MIN_VALIDATION_GRADED
        and validation_roi >= PREMIUM_MIN_VALIDATION_ROI_PCT
        and current_graded >= PREMIUM_MIN_CURRENT_GRADED
        and current_roi >= PREMIUM_MIN_CURRENT_ROI_PCT
    )
    if premium:
        return PREMIUM_RULE_TIER

    has_evidence = (
        validation_windows > 0
        or validation_graded > 0
        or current_graded > 0
        or validation_roi > 0
        or current_roi > 0
    )
    if has_evidence:
        return STANDARD_RULE_TIER

    return STANDARD_RULE_TIER


def load_promoted_production_rules(path: Path = PROMOTED_RULES_PRODUCTION_CSV) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=PROMOTED_RULE_REQUIRED_COLUMNS + ["production_status"])

    rules = pd.read_csv(path)
    missing = [col for col in PROMOTED_RULE_REQUIRED_COLUMNS if col not in rules.columns]
    if missing:
        raise ValueError(
            f"Promoted production rules file is missing required columns: {missing}"
        )

    if "production_status" not in rules.columns:
        raise ValueError("Promoted production rules file is missing required column: production_status")

    ready = rules[rules["production_status"].astype(str).str.strip() == PRODUCTION_READY_STATUS].copy()
    return ready.reset_index(drop=True)


def add_live_governance_metric_aliases(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "model_edge_abs_num" not in out.columns and "primary_edge" in out.columns:
        out["model_edge_abs_num"] = pd.to_numeric(out["primary_edge"], errors="coerce")

    if "model_edge_pct_num" not in out.columns and "primary_edge" in out.columns:
        out["model_edge_pct_num"] = pd.to_numeric(out["primary_edge"], errors="coerce") * 100.0

    if "odds_num" not in out.columns and "primary_odds_used" in out.columns:
        out["odds_num"] = pd.to_numeric(out["primary_odds_used"], errors="coerce")

    numeric_cols = {
        "model_edge_abs_num",
        "model_edge_pct_num",
        "selection_score",
        "vsigma_pre_score",
        "primary_model_prob",
        "primary_edge",
        "odds_num",
    }
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    return out


def row_matches_promoted_rule(row: pd.Series, rule_row: pd.Series) -> bool:
    metric = str(rule_row["metric"])
    rule_type = str(rule_row["rule_type"])
    direction = str(rule_row["direction"])
    threshold = rule_row["threshold"]

    if metric not in row.index:
        return False

    value = row.get(metric)

    if rule_type == "NUMERIC_THRESHOLD":
        value_num = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
        threshold_num = pd.to_numeric(pd.Series([threshold]), errors="coerce").iloc[0]
        if pd.isna(value_num) or pd.isna(threshold_num):
            return False
        if direction == ">=":
            return bool(value_num >= threshold_num)
        if direction == "<=":
            return bool(value_num <= threshold_num)
        raise ValueError(f"Unsupported numeric promoted-rule direction: {direction}")

    if rule_type == "CATEGORY_BUCKET":
        value_text = "UNKNOWN" if pd.isna(value) or str(value).strip() == "" else str(value).strip()
        return value_text == str(threshold)

    raise ValueError(f"Unsupported promoted-rule type: {rule_type}")


def apply_promoted_rules_governance(
    df: pd.DataFrame,
    promoted_rules: pd.DataFrame,
) -> pd.DataFrame:
    out = add_live_governance_metric_aliases(df)

    out["base_execution_verdict"] = out["execution_verdict"]
    out["base_final_recommendation"] = out["final_recommendation"]

    if promoted_rules.empty:
        out["production_governance_status"] = "NO_PROMOTED_RULES_AVAILABLE"
        out["production_governance_rule_count"] = 0
        out["production_governance_premium_rule_count"] = 0
        out["production_governance_standard_rule_count"] = 0
        out["production_governance_generic_rule_count"] = 0
        out["production_governance_best_evidence_tier"] = ""
        out["production_governance_top_rule"] = ""
        out["production_governance_matched_rules"] = ""
        out["production_governance_note"] = "No production-ready promoted rules were loaded."
        return out

    rule_counts: list[int] = []
    premium_rule_counts: list[int] = []
    standard_rule_counts: list[int] = []
    generic_rule_counts: list[int] = []
    best_evidence_tiers: list[str] = []
    top_rules: list[str] = []
    matched_rule_texts: list[str] = []
    statuses: list[str] = []
    notes: list[str] = []

    for _, row in out.iterrows():
        matches = [
            {
                "rule": str(rule_row["rule"]),
                "tier": infer_promoted_rule_tier(rule_row),
            }
            for _, rule_row in promoted_rules.iterrows()
            if row_matches_promoted_rule(row, rule_row)
        ]
        premium_matches = [match for match in matches if match["tier"] == PREMIUM_RULE_TIER]
        standard_matches = [match for match in matches if match["tier"] == STANDARD_RULE_TIER]
        generic_matches = [match for match in matches if match["tier"] == GENERIC_RULE_TIER]
        non_generic_matches = premium_matches + standard_matches
        base_rec = norm_rule_text(row.get("base_final_recommendation"))
        actionable = base_rec in ACTIONABLE_RECOMMENDATIONS

        if premium_matches and actionable:
            if thin_coverage_governance_caution(row):
                status = "DOWNGRADED_THIN_COVERAGE_PREMIUM_EVIDENCE"
                note = (
                    "Premium promoted-rule evidence was downgraded because official league coverage is thin "
                    "and edge/probability/core support was not strong enough for extra trust."
                )
            else:
                status = "APPROVED_BY_PREMIUM_PROMOTED_RULE"
                note = "Actionable recommendation matched premium promoted-rule evidence."
        elif actionable and standard_matches:
            status = "APPROVED_BY_PROMOTED_RULE"
            note = "Actionable recommendation matched standard promoted-rule evidence."
        elif actionable and generic_matches:
            status = "DOWNGRADED_GENERIC_PROMOTED_RULE_ONLY"
            note = (
                "Base actionable recommendation matched only broad generic promoted rules; "
                "approval requires at least one selective evidence rule."
            )
        elif actionable:
            status = "DOWNGRADED_NO_PROMOTED_RULE_MATCH"
            note = "Base actionable recommendation did not match any production-ready promoted rule."
        elif matches:
            status = "ANNOTATED_NON_ACTIONABLE_RULE_MATCH"
            note = "Non-actionable recommendation matched promoted rule context; no upgrade applied."
        else:
            status = "NON_ACTIONABLE_NO_PROMOTED_RULE_MATCH"
            note = "Non-actionable recommendation did not match production-ready promoted rules."

        rule_counts.append(len(matches))
        premium_rule_counts.append(len(premium_matches))
        standard_rule_counts.append(len(standard_matches))
        generic_rule_counts.append(len(generic_matches))
        if premium_matches:
            best_evidence_tiers.append(PREMIUM_RULE_TIER)
            top_rules.append(premium_matches[0]["rule"])
        elif standard_matches:
            best_evidence_tiers.append(STANDARD_RULE_TIER)
            top_rules.append(standard_matches[0]["rule"])
        elif generic_matches:
            best_evidence_tiers.append(GENERIC_RULE_TIER)
            top_rules.append(generic_matches[0]["rule"])
        else:
            best_evidence_tiers.append("")
            top_rules.append("")
        matched_rule_texts.append(" | ".join(match["rule"] for match in matches))
        statuses.append(status)
        notes.append(note)

    out["production_governance_status"] = statuses
    out["production_governance_rule_count"] = rule_counts
    out["production_governance_premium_rule_count"] = premium_rule_counts
    out["production_governance_standard_rule_count"] = standard_rule_counts
    out["production_governance_generic_rule_count"] = generic_rule_counts
    out["production_governance_best_evidence_tier"] = best_evidence_tiers
    out["production_governance_top_rule"] = top_rules
    out["production_governance_matched_rules"] = matched_rule_texts
    out["production_governance_note"] = notes

    downgrade_mask = out["production_governance_status"].isin(
        {
            "DOWNGRADED_NO_PROMOTED_RULE_MATCH",
            "DOWNGRADED_GENERIC_PROMOTED_RULE_ONLY",
            "DOWNGRADED_THIN_COVERAGE_PREMIUM_EVIDENCE",
        }
    )
    out.loc[downgrade_mask, "execution_verdict"] = "WATCH"
    out.loc[downgrade_mask, "final_recommendation"] = "WATCH"

    return out


DEEP_ANALYSIS_OUTPUT_COLUMNS = [
    "shortlist_rank",
    "shortlist_bucket",
    "analysis_label",
    "date",
    "country",
    "league",
    "fixture_id",
    "home_team",
    "away_team",
    "selection_score",
    "vsigma_pre_score",
    "confidence_band",
    "likely_scoreline",
    "market_primary",
    "market_alt",
    "edge_floor_band",
    "base_execution_verdict",
    "base_final_recommendation",
    "execution_verdict",
    "final_recommendation",
    "production_governance_status",
    "production_governance_rule_count",
    "production_governance_premium_rule_count",
    "production_governance_standard_rule_count",
    "production_governance_generic_rule_count",
    "production_governance_best_evidence_tier",
    "production_governance_top_rule",
    "production_governance_matched_rules",
    "production_governance_note",
    "execution_fragility_reason",
    "execution_market_fit_status",
    "execution_market_fit_note",
    "execution_preferred_safer_market",
    "primary_model_prob",
    "primary_odds_used",
    "primary_implied_prob",
    "primary_edge",
    "alt_model_prob",
    "alt_odds_used",
    "alt_implied_prob",
    "alt_edge",
    "projected_home_goals",
    "projected_away_goals",
    "projected_total_goals",
    "league_coverage_class",
    "league_data_reliability_score",
    "league_coverage_rich_flag",
    "league_has_odds_coverage",
    "league_has_fixture_stats_coverage",
    "league_has_injuries_coverage",
    "league_has_lineups_coverage",
    "league_has_predictions_coverage",
    "league_stats_reliability_multiplier",
    "league_coverage_uncertainty_penalty",
    "league_coverage_source_status",
    "league_coverage_note",
    "recent_stats_quality_flag",
    "recent_stats_process_score",
    "recent_lab_context_score",
    "home_recent_lab_trust_multiplier",
    "away_recent_lab_trust_multiplier",
    "home_recent_opponent_strength_avg",
    "away_recent_opponent_strength_avg",
    "home_recent_schedule_difficulty_score",
    "away_recent_schedule_difficulty_score",
    "home_recent_schedule_quality_flag",
    "away_recent_schedule_quality_flag",
    "recent_schedule_balance_delta",
    "home_recent_anomaly_count_last5",
    "away_recent_anomaly_count_last5",
    "home_recent_clean_sample_size",
    "away_recent_clean_sample_size",
    "home_recent_anomaly_penalty",
    "away_recent_anomaly_penalty",
    "home_recent_event_coverage_flag",
    "away_recent_event_coverage_flag",
    "recent_sample_cleanliness_flag",
    "odds_imp_over15",
    "odds_imp_over25",
    "odds_imp_under35",
    "odds_imp_btts_yes",
    "odds_imp_home_win",
    "odds_imp_draw",
    "odds_imp_away_win",
    "odds_imp_home_dnb",
    "odds_imp_away_dnb",
    "odds_market_support_count",
    "odds_bookmaker_support_count",
    "odds_dispersion_score",
    "odds_structure_coherence_flag",
    "odds_total_ladder_shape",
    "odds_goal_expectation_band",
    "odds_side_fragility_flag",
    "odds_btts_support_flag",
    "odds_over25_support_flag",
    "odds_over15_support_flag",
    "odds_under35_support_flag",
    "odds_market_translation_hint",
    "odds_line_aggression_flag",
    "odds_confidence_adjustment_score",
    "odds_structure_depth_status",
    "home_recent_stats_matches_used",
    "away_recent_stats_matches_used",
    "home_recent_stats_coverage_ratio",
    "away_recent_stats_coverage_ratio",
    "home_injuries_count",
    "away_injuries_count",
    "home_injuries_coverage_flag",
    "away_injuries_coverage_flag",
    "home_absence_risk_score",
    "away_absence_risk_score",
    "home_absence_severity_flag",
    "away_absence_severity_flag",
    "injuries_quality_flag",
    "availability_known_risk_score",
    "availability_uncertainty_penalty",
    "availability_attack_penalty",
    "home_lineup_available_flag",
    "away_lineup_available_flag",
    "home_lineup_quality_flag",
    "away_lineup_quality_flag",
    "lineup_quality_flag",
    "lineup_activation_state",
    "lineup_activation_window_minutes",
    "lineup_minutes_to_kickoff",
    "lineup_timing_eligible_flag",
    "lineup_structural_confidence_flag",
    "home_lineup_known_starters_count",
    "away_lineup_known_starters_count",
    "home_lineup_bench_known_flag",
    "away_lineup_bench_known_flag",
    "home_lineup_attacker_count",
    "away_lineup_attacker_count",
    "home_lineup_defender_count",
    "away_lineup_defender_count",
    "home_lineup_midfielder_count",
    "away_lineup_midfielder_count",
    "home_lineup_goalkeeper_known_flag",
    "away_lineup_goalkeeper_known_flag",
    "home_lineup_attack_continuity_score",
    "away_lineup_attack_continuity_score",
    "home_lineup_defense_continuity_score",
    "away_lineup_defense_continuity_score",
    "lineup_confirmation_score",
    "lineup_uncertainty_penalty",
    "lineup_score_nudge",
    "vsigma_priority",
    "market_family_hint",
    "tie_state_label",
    "tie_adjustment_note",
    "reason_1",
    "reason_2",
    "reason_3",
    "home_rank",
    "away_rank",
    "home_urgency_score",
    "away_urgency_score",
    "home_form_pts",
    "away_form_pts",
    "home_goals_for_pg",
    "away_goals_for_pg",
    "home_goals_against_pg",
    "away_goals_against_pg",
    "home_scored_rate",
    "away_scored_rate",
    "home_clean_sheet_rate",
    "away_clean_sheet_rate",
    "home_btts_rate",
    "away_btts_rate",
    "home_over15_rate",
    "away_over15_rate",
    "home_over25_rate",
    "away_over25_rate",
    "home_recent_shots_for_pg",
    "away_recent_shots_for_pg",
    "home_recent_shots_against_pg",
    "away_recent_shots_against_pg",
    "home_recent_sot_for_pg",
    "away_recent_sot_for_pg",
    "home_recent_sot_against_pg",
    "away_recent_sot_against_pg",
    "home_recent_possession_pct",
    "away_recent_possession_pct",
    "home_recent_corners_for_pg",
    "away_recent_corners_for_pg",
    "home_recent_corners_against_pg",
    "away_recent_corners_against_pg",
    "home_recent_fouls_pg",
    "away_recent_fouls_pg",
    "home_recent_yellow_pg",
    "away_recent_yellow_pg",
    "home_recent_offsides_pg",
    "away_recent_offsides_pg",
    "home_recent_blocked_shots_pg",
    "away_recent_blocked_shots_pg",
]


def write_empty_deep_analysis_output() -> None:
    """NO_BET legítimo con cero candidatos en shortlist: aun así se escribe el
    CSV de salida con SOLO la cabecera (0 filas) usando el esquema canónico,
    para que todos los consumidores aguas abajo tengan un archivo válido."""
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    empty = pd.DataFrame(columns=DEEP_ANALYSIS_OUTPUT_COLUMNS)
    empty.to_csv(OUTPUT_CSV, index=False)
    print(f"Archivo NO_BET (0 candidatos) generado con cabecera: {OUTPUT_CSV}")


def main() -> None:
    if not SHORTLIST_CSV.exists():
        print("No hay shortlist para analizar.")
        write_empty_deep_analysis_output()
        return
    if not SCORED_CSV.exists():
        print("No existe el score v3 para mergear cuotas/contexto.")
        return

    shortlist = pd.read_csv(SHORTLIST_CSV)
    if shortlist.empty:
        print("No hay shortlist para analizar.")
        write_empty_deep_analysis_output()
        return

    scored = pd.read_csv(SCORED_CSV)

    merge_cols = [
        "fixture_id",
    ] + [
        c
        for c in (
            ODDS_COLS
            + EXTRA_COLS
            + RECENT_STATS_COLS
            + RECENT_LAB_COLS
            + ODDS_STRUCTURE_COLS
            + AVAILABILITY_COLS
            + LINEUP_COLS
            + COVERAGE_COLS
        )
        if c in scored.columns
    ]
    shortlist = shortlist.drop(
        columns=[c for c in merge_cols if c != "fixture_id" and c in shortlist.columns],
        errors="ignore",
    )
    df = shortlist.merge(scored[merge_cols], on="fixture_id", how="left")

    confidence_list = []
    scoreline_list = []
    market_primary_list = []
    market_alt_list = []
    reason1_list = []
    reason2_list = []
    reason3_list = []
    analysis_label_list = []

    primary_prob_list = []
    primary_odds_list = []
    primary_impl_list = []
    primary_edge_list = []

    alt_prob_list = []
    alt_odds_list = []
    alt_impl_list = []
    alt_edge_list = []
    projected_home_list = []
    projected_away_list = []

    for _, row in df.iterrows():
        ph, pa = project_goals(row)
        projected_home_list.append(ph)
        projected_away_list.append(pa)

        confidence_list.append(confidence_band(float(row["selection_score"]) - coverage_confidence_penalty(row)))
        scoreline_list.append(likely_scoreline(row))

        mp, ma, meta = choose_primary_alt(row)
        market_primary_list.append(mp)
        market_alt_list.append(ma)

        rs = reasons(row, meta)
        reason1_list.append(rs[0])
        reason2_list.append(rs[1])
        reason3_list.append(rs[2])

        analysis_label_list.append(analysis_label(str(row["shortlist_bucket"])))

        primary_prob_list.append(meta["primary_prob"])
        primary_odds_list.append(meta["primary_odds"])
        primary_impl_list.append(meta["primary_implied"])
        primary_edge_list.append(meta["primary_edge"])

        alt_prob_list.append(meta["alt_prob"])
        alt_odds_list.append(meta["alt_odds"])
        alt_impl_list.append(meta["alt_implied"])
        alt_edge_list.append(meta["alt_edge"])

    df = df.copy().assign(
        confidence_band=confidence_list,
        likely_scoreline=scoreline_list,
        market_primary=market_primary_list,
        market_alt=market_alt_list,
        reason_1=reason1_list,
        reason_2=reason2_list,
        reason_3=reason3_list,
        analysis_label=analysis_label_list,
        primary_model_prob=primary_prob_list,
        primary_odds_used=primary_odds_list,
        primary_implied_prob=primary_impl_list,
        primary_edge=primary_edge_list,
        alt_model_prob=alt_prob_list,
        alt_odds_used=alt_odds_list,
        alt_implied_prob=alt_impl_list,
        alt_edge=alt_edge_list,
        projected_home_goals=projected_home_list,
        projected_away_goals=projected_away_list,
        projected_total_goals=[round(h + a, 2) for h, a in zip(projected_home_list, projected_away_list)],
    )

    verdicts = df.apply(execution_verdict, axis=1)
    df["edge_floor_band"] = df["primary_edge"].apply(edge_floor_band)
    df["execution_verdict"] = [x[0] for x in verdicts]
    df["final_recommendation"] = [x[1] for x in verdicts]
    df = apply_promoted_rules_governance(df, load_promoted_production_rules())
    df = apply_execution_market_fit_hardening(df)

    existing_cols = [c for c in DEEP_ANALYSIS_OUTPUT_COLUMNS if c in df.columns]
    out = df[existing_cols].copy()
    out.to_csv(OUTPUT_CSV, index=False)

    print("\n=== DEEP ANALYSIS CANDIDATES COMPLETADO ===")
    print(f"Archivo generado: {OUTPUT_CSV}")
    print("\nAnálisis resumido:")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
