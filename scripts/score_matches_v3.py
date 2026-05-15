from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = ROOT / "data" / "processed" / "matches_league_filtered.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_SCORED = OUTPUT_DIR / "matches_vsigma_scored_v3.csv"
OUTPUT_TOP = OUTPUT_DIR / "vsigma_top_candidates_v3.csv"
OUTPUT_REPORT = OUTPUT_DIR / "vsigma_score_report_v3.csv"


LEAGUE_BASE_SCORE = {
    "TIER_1": 30,
    "TIER_2": 23,
    "TIER_3": 13,
    "TIER_4": 4,
}

RECENT_STATS_NUMERIC_COLS = [
    "home_recent_stats_matches_used", "away_recent_stats_matches_used",
    "home_recent_stats_coverage_ratio", "away_recent_stats_coverage_ratio",
    "home_recent_stats_available_flag", "away_recent_stats_available_flag",
    "home_recent_shots_for_pg", "away_recent_shots_for_pg",
    "home_recent_shots_against_pg", "away_recent_shots_against_pg",
    "home_recent_sot_for_pg", "away_recent_sot_for_pg",
    "home_recent_sot_against_pg", "away_recent_sot_against_pg",
    "home_recent_possession_pct", "away_recent_possession_pct",
    "home_recent_corners_for_pg", "away_recent_corners_for_pg",
    "home_recent_corners_against_pg", "away_recent_corners_against_pg",
    "home_recent_fouls_pg", "away_recent_fouls_pg",
    "home_recent_yellow_pg", "away_recent_yellow_pg",
    "home_recent_offsides_pg", "away_recent_offsides_pg",
    "home_recent_blocked_shots_pg", "away_recent_blocked_shots_pg",
]

INJURIES_NUMERIC_COLS = [
    "home_injuries_count", "away_injuries_count",
    "home_injuries_available_flag", "away_injuries_available_flag",
    "home_absence_risk_score", "away_absence_risk_score",
]

LINEUP_NUMERIC_COLS = [
    "home_lineup_available_flag", "away_lineup_available_flag",
    "home_lineup_known_starters_count", "away_lineup_known_starters_count",
    "home_lineup_bench_known_flag", "away_lineup_bench_known_flag",
    "home_lineup_attacker_count", "away_lineup_attacker_count",
    "home_lineup_defender_count", "away_lineup_defender_count",
    "home_lineup_midfielder_count", "away_lineup_midfielder_count",
    "home_lineup_goalkeeper_known_flag", "away_lineup_goalkeeper_known_flag",
    "home_lineup_attack_continuity_score", "away_lineup_attack_continuity_score",
    "home_lineup_defense_continuity_score", "away_lineup_defense_continuity_score",
    "lineup_confirmation_score", "lineup_uncertainty_penalty",
    "lineup_activation_window_minutes", "lineup_minutes_to_kickoff",
    "lineup_timing_eligible_flag", "lineup_structural_confidence_flag",
]

COVERAGE_NUMERIC_COLS = [
    "league_has_odds_coverage",
    "league_has_fixture_stats_coverage",
    "league_has_injuries_coverage",
    "league_has_lineups_coverage",
    "league_has_predictions_coverage",
    "league_coverage_rich_flag",
    "league_data_reliability_score",
]

RECENT_LAB_NUMERIC_COLS = [
    "home_recent_opponent_strength_avg", "away_recent_opponent_strength_avg",
    "home_recent_schedule_difficulty_score", "away_recent_schedule_difficulty_score",
    "recent_schedule_balance_delta",
    "home_recent_schedule_matches_used", "away_recent_schedule_matches_used",
    "home_recent_anomaly_count_last5", "away_recent_anomaly_count_last5",
    "home_recent_clean_sample_size", "away_recent_clean_sample_size",
    "home_recent_anomaly_penalty", "away_recent_anomaly_penalty",
    "home_recent_events_checked_last5", "away_recent_events_checked_last5",
]

RECENT_LAB_TEXT_COLS = [
    "home_recent_schedule_quality_flag", "away_recent_schedule_quality_flag",
    "recent_sample_cleanliness_flag",
    "home_recent_event_coverage_flag", "away_recent_event_coverage_flag",
]

ODDS_STRUCTURE_NUMERIC_COLS = [
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
    "odds_confidence_adjustment_score",
]

ODDS_STRUCTURE_TEXT_COLS = [
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
    "odds_structure_depth_status",
]

NUMERIC_COLS = [
    "home_xg_for", "home_xg_against", "away_xg_for", "away_xg_against",
    "home_sot_for", "away_sot_for", "home_big_for", "away_big_for",
    "home_form_pts", "away_form_pts",
    "home_goals_for_pg", "away_goals_for_pg",
    "home_goals_against_pg", "away_goals_against_pg",
    "home_scored_rate", "away_scored_rate",
    "home_clean_sheet_rate", "away_clean_sheet_rate",
    "home_btts_rate", "away_btts_rate",
    "home_over15_rate", "away_over15_rate",
    "home_over25_rate", "away_over25_rate",
    "home_rank", "away_rank",
    "home_points", "away_points",
    "home_goals_diff", "away_goals_diff",
    "home_urgency_score", "away_urgency_score",
    "league_team_count",
    "home_recent_matches", "away_recent_matches",
    *RECENT_STATS_NUMERIC_COLS,
    *INJURIES_NUMERIC_COLS,
    *LINEUP_NUMERIC_COLS,
    *COVERAGE_NUMERIC_COLS,
    *RECENT_LAB_NUMERIC_COLS,
    *ODDS_STRUCTURE_NUMERIC_COLS,
]

TEXT_COLS = [
    "home_motivation", "away_motivation",
    "home_absences", "away_absences",
    "data_enrichment_level",
    "recent_stats_quality_flag",
    "home_injuries_coverage_flag", "away_injuries_coverage_flag",
    "home_absence_severity_flag", "away_absence_severity_flag",
    "injuries_quality_flag",
    "home_lineup_quality_flag", "away_lineup_quality_flag", "lineup_quality_flag",
    "lineup_activation_state",
    "league_coverage_class",
    "league_coverage_source_status",
    "league_coverage_note",
    *RECENT_LAB_TEXT_COLS,
    *ODDS_STRUCTURE_TEXT_COLS,
]


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    missing = {
        **{col: np.nan for col in NUMERIC_COLS if col not in df.columns},
        **{col: "" for col in TEXT_COLS if col not in df.columns},
    }
    if missing:
        df = pd.concat([df, pd.DataFrame(missing, index=df.index)], axis=1)
    return df


def to_numeric(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def normalize_rate(s: pd.Series) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    if s.dropna().empty:
        return s
    if s.dropna().max() > 1.5:
        return s / 100.0
    return s


def clip(s: pd.Series | float, low: float, high: float):
    if isinstance(s, pd.Series):
        return s.clip(lower=low, upper=high)
    return max(low, min(high, s))


def motivation_to_num(value) -> float:
    if pd.isna(value):
        return 0.0

    txt = str(value).strip().lower()

    if txt in {"", "nan", "none", "-", "null"}:
        return 0.0

    try:
        num = float(txt)
        if -1.0 <= num <= 1.0:
            return num
        return 0.0
    except ValueError:
        pass

    high_words = [
        "high", "alta", "must win", "title", "champion", "promotion",
        "relegation", "survival", "europe", "playoff", "play-off",
        "final", "derby", "objective", "urgent", "necesita",
    ]
    medium_words = [
        "medium", "media", "normal", "moderate", "competitive",
        "compite", "important",
    ]
    low_words = [
        "low", "baja", "nothing", "nada", "safe", "rotation", "rotacion", "friendly",
    ]

    if any(w in txt for w in high_words):
        return 1.0
    if any(w in txt for w in medium_words):
        return 0.5
    if any(w in txt for w in low_words):
        return -0.5

    return 0.0


def absences_to_num(value) -> float:
    if pd.isna(value):
        return 0.0

    txt = str(value).strip().lower()

    if txt in {"", "nan", "none", "no", "0", "-", "sin bajas"}:
        return 0.0

    try:
        return min(float(txt), 6.0)
    except ValueError:
        pass

    parts = [p.strip() for p in txt.replace("|", ",").replace("/", ",").replace(";", ",").split(",") if p.strip()]
    return min(float(len(parts)), 6.0)


def coverage_uncertainty_penalty(flag: str) -> float:
    # Advisory mode: weak/unknown injury coverage is reported, not scored.
    # Unknown remains unknown in the source fields; it just stops acting like
    # a negative execution signal.
    return 0.0


def team_coverage_weight(flag: pd.Series) -> pd.Series:
    return flag.astype(str).str.upper().map(
        {
            "FULL": 1.0,
            "PARTIAL": 0.45,
            "SPARSE": 0.20,
            "NONE": 0.0,
        }
    ).fillna(0.0)


def reliable_high_absence_risk(df: pd.DataFrame) -> pd.Series:
    quality = df["injuries_quality_flag"].astype(str).str.upper()
    home_severity = df["home_absence_severity_flag"].astype(str).str.upper()
    away_severity = df["away_absence_severity_flag"].astype(str).str.upper()
    known_risk = pd.to_numeric(df["availability_known_risk_score"], errors="coerce").fillna(0.0)
    return quality.eq("FULL") & ((known_risk >= 4.0) | home_severity.eq("HIGH") | away_severity.eq("HIGH"))


def side_reliable_high_absence_risk(df: pd.DataFrame, side: str) -> pd.Series:
    quality = df["injuries_quality_flag"].astype(str).str.upper()
    severity = df[f"{side}_absence_severity_flag"].astype(str).str.upper()
    risk = pd.to_numeric(df[f"{side}_absence_risk_score"], errors="coerce").fillna(0.0)
    return quality.eq("FULL") & (severity.eq("HIGH") | risk.ge(3.0))


def official_coverage_loaded(df: pd.DataFrame) -> pd.Series:
    return df["league_coverage_source_status"].astype(str).str.upper().str.startswith("OFFICIAL_API")


def coverage_bool(df: pd.DataFrame, col: str, default: float = 1.0) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce").fillna(default).clip(lower=0, upper=1)


def stats_coverage_multiplier(df: pd.DataFrame) -> pd.Series:
    loaded = official_coverage_loaded(df)
    has_stats = coverage_bool(df, "league_has_fixture_stats_coverage")
    reliability = pd.to_numeric(df["league_data_reliability_score"], errors="coerce").fillna(1.0).clip(0.4, 1.0)
    return pd.Series(np.where(loaded, has_stats * reliability, 1.0), index=df.index)


def coverage_uncertainty_penalty_series(df: pd.DataFrame) -> pd.Series:
    loaded = official_coverage_loaded(df)
    coverage_class = df["league_coverage_class"].astype(str).str.upper()
    penalty = coverage_class.map(
        {
            "COVERAGE_RICH": 0.0,
            "COVERAGE_GOOD": 0.0,
            "COVERAGE_PARTIAL": 0.35,
            "COVERAGE_THIN": 0.85,
            "COVERAGE_MINIMAL": 1.25,
        }
    ).fillna(0.0)
    return pd.Series(np.where(loaded, penalty, 0.0), index=df.index)


def compute_rank_strength(rank: pd.Series, team_count: pd.Series) -> pd.Series:
    rank = pd.to_numeric(rank, errors="coerce")
    team_count = pd.to_numeric(team_count, errors="coerce")

    out = pd.Series(np.nan, index=rank.index, dtype=float)

    valid = rank.notna() & team_count.notna() & (team_count > 1)
    out.loc[valid] = 1 - ((rank.loc[valid] - 1) / (team_count.loc[valid] - 1))

    return out


def recent_lab_trust_multiplier(df: pd.DataFrame, side: str) -> pd.Series:
    schedule_quality = df[f"{side}_recent_schedule_quality_flag"].astype(str).str.upper()
    event_coverage = df[f"{side}_recent_event_coverage_flag"].astype(str).str.upper()
    schedule_difficulty = pd.to_numeric(
        df[f"{side}_recent_schedule_difficulty_score"],
        errors="coerce",
    ).fillna(0.0)
    anomaly_penalty = pd.to_numeric(
        df[f"{side}_recent_anomaly_penalty"],
        errors="coerce",
    ).fillna(0.0)

    schedule_active = schedule_quality.isin(["FULL", "PARTIAL"]).astype(float)
    event_active = event_coverage.isin(["SUPPORTED", "PARTIAL"]).astype(float)

    # Conservative lab-only trust adjustment. Hard recent schedules can add
    # modest trust; easy or anomaly-heavy samples reduce trust. Missing event
    # coverage stays neutral because it is uncertainty, not evidence of noise.
    multiplier = (
        1.0
        + schedule_difficulty.clip(-1.0, 1.0) * 0.08 * schedule_active
        - anomaly_penalty.clip(0.0, 1.20) * 0.10 * event_active
    )
    return multiplier.clip(lower=0.78, upper=1.08)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo filtrado: {INPUT_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df = ensure_columns(df).copy()

    for col in NUMERIC_COLS:
        df[col] = to_numeric(df, col)

    df["league_coverage_class"] = df["league_coverage_class"].replace("", "COVERAGE_UNKNOWN")
    df["league_coverage_source_status"] = df["league_coverage_source_status"].replace("", "COVERAGE_NOT_LOADED")
    df["league_data_reliability_score"] = df["league_data_reliability_score"].fillna(1.0)
    df["league_coverage_uncertainty_penalty"] = coverage_uncertainty_penalty_series(df).round(2)
    df["league_stats_reliability_multiplier"] = stats_coverage_multiplier(df).round(3)

    rate_cols = [
        "home_scored_rate", "away_scored_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_btts_rate", "away_btts_rate",
        "home_over15_rate", "away_over15_rate",
        "home_over25_rate", "away_over25_rate",
    ]
    for col in rate_cols:
        df[col] = normalize_rate(df[col])

    # 1) League quality
    df["league_quality_score"] = df["league_tier"].map(LEAGUE_BASE_SCORE).fillna(0)

    # 2) Data quality
    old_core = [
        "home_xg_for", "home_xg_against", "away_xg_for", "away_xg_against",
        "home_sot_for", "away_sot_for", "home_big_for", "away_big_for",
    ]

    prior_core = [
        "home_form_pts", "away_form_pts",
        "home_goals_for_pg", "away_goals_for_pg",
        "home_goals_against_pg", "away_goals_against_pg",
        "home_scored_rate", "away_scored_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_btts_rate", "away_btts_rate",
        "home_over15_rate", "away_over15_rate",
        "home_over25_rate", "away_over25_rate",
    ]

    standings_core = [
        "home_rank", "away_rank",
        "home_points", "away_points",
        "home_goals_diff", "away_goals_diff",
        "home_urgency_score", "away_urgency_score",
        "league_team_count",
    ]

    recent_stats_core = [
        "home_recent_shots_for_pg", "away_recent_shots_for_pg",
        "home_recent_sot_for_pg", "away_recent_sot_for_pg",
        "home_recent_shots_against_pg", "away_recent_shots_against_pg",
        "home_recent_sot_against_pg", "away_recent_sot_against_pg",
        "home_recent_corners_for_pg", "away_recent_corners_for_pg",
        "home_recent_corners_against_pg", "away_recent_corners_against_pg",
        "home_recent_possession_pct", "away_recent_possession_pct",
        "home_recent_stats_coverage_ratio", "away_recent_stats_coverage_ratio",
    ]

    df["old_data_count"] = df[old_core].notna().sum(axis=1)
    df["prior_data_count"] = df[prior_core].notna().sum(axis=1)
    df["standings_data_count"] = df[standings_core].notna().sum(axis=1)
    df["recent_stats_data_count"] = df[recent_stats_core].notna().sum(axis=1)
    injuries_core = [
        "home_injuries_count", "away_injuries_count",
        "home_absence_risk_score", "away_absence_risk_score",
    ]
    df["injuries_data_count"] = df[injuries_core].notna().sum(axis=1)

    df["data_quality_score"] = (
        (df["old_data_count"] / len(old_core)) * 8
        + (df["prior_data_count"] / len(prior_core)) * 10
        + (df["standings_data_count"] / len(standings_core)) * 6
        + (df["recent_stats_data_count"] / len(recent_stats_core)) * 4
    ).round(2)

    df["data_warning"] = "NO_DATA"
    df.loc[df["prior_data_count"] >= 8, "data_warning"] = "OK_PRIOR"
    df.loc[df["standings_data_count"] >= 6, "data_warning"] = "OK_STANDINGS"
    df.loc[(df["prior_data_count"] >= 8) & (df["standings_data_count"] >= 6), "data_warning"] = "OK_PRIOR_STANDINGS"
    df.loc[df["old_data_count"] >= 4, "data_warning"] = "OK_FULL"
    df.loc[
        df["data_warning"].isin(["OK_PRIOR", "OK_STANDINGS", "OK_PRIOR_STANDINGS", "OK_FULL"])
        & (df["recent_stats_data_count"] >= 8),
        "data_warning",
    ] = df.loc[
        df["data_warning"].isin(["OK_PRIOR", "OK_STANDINGS", "OK_PRIOR_STANDINGS", "OK_FULL"])
        & (df["recent_stats_data_count"] >= 8),
        "data_warning",
    ].astype(str) + "_STATS"

    # 2b) Availability semantics. Unknown coverage is not clean zero.
    home_coverage_weight = team_coverage_weight(df["home_injuries_coverage_flag"])
    away_coverage_weight = team_coverage_weight(df["away_injuries_coverage_flag"])
    df["home_absences_num"] = (df["home_absence_risk_score"] * home_coverage_weight).where(
        home_coverage_weight > 0,
        np.nan,
    )
    df["away_absences_num"] = (df["away_absence_risk_score"] * away_coverage_weight).where(
        away_coverage_weight > 0,
        np.nan,
    )
    df["home_availability_unknown_penalty"] = df["home_injuries_coverage_flag"].apply(coverage_uncertainty_penalty)
    df["away_availability_unknown_penalty"] = df["away_injuries_coverage_flag"].apply(coverage_uncertainty_penalty)
    df["availability_uncertainty_penalty"] = (
        df["home_availability_unknown_penalty"] + df["away_availability_unknown_penalty"]
    ).round(2)
    df["availability_known_risk_score"] = (
        df["home_absences_num"].fillna(0) + df["away_absences_num"].fillna(0)
    ).round(2)
    high_absence_advisory_penalty = reliable_high_absence_risk(df).astype(float) * 0.10
    home_high_absence_advisory = side_reliable_high_absence_risk(df, "home").astype(float)
    away_high_absence_advisory = side_reliable_high_absence_risk(df, "away").astype(float)
    df["availability_attack_penalty"] = high_absence_advisory_penalty.round(2)

    # 2c) Lineups are a late confirmation layer. They only move the score when
    # FULL lineups are structurally confident and inside the activation window.
    lineup_active = df["lineup_activation_state"].astype(str).str.upper().eq("ACTIVE").astype(float)
    lineup_confirmation = pd.to_numeric(df["lineup_confirmation_score"], errors="coerce").fillna(0.0)
    df["lineup_score_nudge"] = clip(
        lineup_confirmation * 0.55 * lineup_active,
        -0.35,
        0.35,
    ).round(2)
    df["home_recent_lab_trust_multiplier"] = recent_lab_trust_multiplier(df, "home").round(3)
    df["away_recent_lab_trust_multiplier"] = recent_lab_trust_multiplier(df, "away").round(3)
    df["recent_lab_context_score"] = clip(
        ((df["home_recent_lab_trust_multiplier"] + df["away_recent_lab_trust_multiplier"]) / 2.0 - 1.0) * 8.0,
        -1.20,
        0.80,
    ).round(2)

    # 3) Prior / recent attack environment
    home_attack_prior = (
        df["home_goals_for_pg"].fillna(0) * 4.2
        + df["home_scored_rate"].fillna(0) * 5.5
        + df["home_over15_rate"].fillna(0) * 2.2
        + df["home_over25_rate"].fillna(0) * 1.8
        + df["home_btts_rate"].fillna(0) * 1.4
    )

    away_attack_prior = (
        df["away_goals_for_pg"].fillna(0) * 4.2
        + df["away_scored_rate"].fillna(0) * 5.5
        + df["away_over15_rate"].fillna(0) * 2.2
        + df["away_over25_rate"].fillna(0) * 1.8
        + df["away_btts_rate"].fillna(0) * 1.4
    )
    home_attack_prior = home_attack_prior * df["home_recent_lab_trust_multiplier"]
    away_attack_prior = away_attack_prior * df["away_recent_lab_trust_multiplier"]

    home_process_attack = (
        df["home_recent_sot_for_pg"].fillna(0) * 1.15
        + df["home_recent_shots_for_pg"].fillna(0) * 0.22
        + df["home_recent_corners_for_pg"].fillna(0) * 0.18
        - df["away_recent_sot_against_pg"].fillna(0) * 0.10
    ) * df["home_recent_lab_trust_multiplier"]
    away_process_attack = (
        df["away_recent_sot_for_pg"].fillna(0) * 1.15
        + df["away_recent_shots_for_pg"].fillna(0) * 0.22
        + df["away_recent_corners_for_pg"].fillna(0) * 0.18
        - df["home_recent_sot_against_pg"].fillna(0) * 0.10
    ) * df["away_recent_lab_trust_multiplier"]
    process_coverage = (
        df["home_recent_stats_coverage_ratio"].fillna(0)
        + df["away_recent_stats_coverage_ratio"].fillna(0)
    ) / 2.0
    process_environment = (
        (home_process_attack + away_process_attack) / 3.8
    ).clip(lower=0, upper=4) * process_coverage * df["league_stats_reliability_multiplier"]

    df["attack_environment_score"] = clip(
        (
            home_attack_prior
            + away_attack_prior
            + (df["home_goals_against_pg"].fillna(0) * 1.8)
            + (df["away_goals_against_pg"].fillna(0) * 1.8)
        ) / 2.4,
        0,
        18,
    ).round(2)
    df["recent_stats_process_score"] = process_environment.round(2)
    df["attack_environment_score"] = clip(
        df["attack_environment_score"]
        + df["recent_stats_process_score"]
        + df["recent_lab_context_score"]
        - df["availability_attack_penalty"]
        - df["league_coverage_uncertainty_penalty"],
        0,
        20,
    ).round(2)

    # 4) Goal paths
    df["home_goal_path_score"] = clip(
        df["home_goals_for_pg"].fillna(0) * 3.5
        + df["home_scored_rate"].fillna(0) * 5.0
        + df["away_goals_against_pg"].fillna(0) * 2.8
        - df["away_clean_sheet_rate"].fillna(0) * 2.5,
        0,
        18,
    ).round(2)
    df["home_goal_path_score"] = clip(
        df["home_goal_path_score"]
        + (
            df["home_recent_sot_for_pg"].fillna(0) * 0.45
            + df["away_recent_sot_against_pg"].fillna(0) * 0.25
            + df["home_recent_shots_for_pg"].fillna(0) * 0.06
        )
        * df["home_recent_lab_trust_multiplier"]
        * df["home_recent_stats_coverage_ratio"].fillna(0)
        * df["league_stats_reliability_multiplier"],
        0,
        20,
    ).round(2)
    df["home_goal_path_score"] = clip(
        df["home_goal_path_score"]
        - home_high_absence_advisory * 0.03,
        0,
        20,
    ).round(2)

    df["away_goal_path_score"] = clip(
        df["away_goals_for_pg"].fillna(0) * 3.5
        + df["away_scored_rate"].fillna(0) * 5.0
        + df["home_goals_against_pg"].fillna(0) * 2.8
        - df["home_clean_sheet_rate"].fillna(0) * 2.5,
        0,
        18,
    ).round(2)
    df["away_goal_path_score"] = clip(
        df["away_goal_path_score"]
        + (
            df["away_recent_sot_for_pg"].fillna(0) * 0.45
            + df["home_recent_sot_against_pg"].fillna(0) * 0.25
            + df["away_recent_shots_for_pg"].fillna(0) * 0.06
        )
        * df["away_recent_lab_trust_multiplier"]
        * df["away_recent_stats_coverage_ratio"].fillna(0)
        * df["league_stats_reliability_multiplier"],
        0,
        20,
    ).round(2)
    df["away_goal_path_score"] = clip(
        df["away_goal_path_score"]
        - away_high_absence_advisory * 0.03,
        0,
        20,
    ).round(2)

    # 5) Standings strength
    df["home_rank_strength"] = compute_rank_strength(df["home_rank"], df["league_team_count"]).fillna(0)
    df["away_rank_strength"] = compute_rank_strength(df["away_rank"], df["league_team_count"]).fillna(0)

    continental_world_mask = (
        df["country"].astype(str).eq("World")
        & df["league"].astype(str).str.contains(
            "Champions League|Europa League|Conference League|Libertadores|Sudamericana",
            case=False,
            na=False,
        )
    )

    standings_edge = (
        (df["home_rank_strength"] - df["away_rank_strength"]) * 6.0
        + ((df["home_points"].fillna(0) - df["away_points"].fillna(0)) * 0.12)
        + ((df["home_goals_diff"].fillna(0) - df["away_goals_diff"].fillna(0)) * 0.08)
    )

    standings_edge = standings_edge.where(~continental_world_mask, standings_edge * 0.45)

    # 6) Team edge
    home_strength = (
        df["home_form_pts"].fillna(0) * 3.5
        + df["home_goals_for_pg"].fillna(0) * 4.0
        - df["home_goals_against_pg"].fillna(0) * 2.8
        + df["home_scored_rate"].fillna(0) * 3.0
        + df["home_clean_sheet_rate"].fillna(0) * 1.5
        + df["home_rank_strength"].fillna(0) * 4.0
        + df["home_urgency_score"].fillna(0) * 1.5
        - home_high_absence_advisory * 0.05
    )

    away_strength = (
        df["away_form_pts"].fillna(0) * 3.5
        + df["away_goals_for_pg"].fillna(0) * 4.0
        - df["away_goals_against_pg"].fillna(0) * 2.8
        + df["away_scored_rate"].fillna(0) * 3.0
        + df["away_clean_sheet_rate"].fillna(0) * 1.5
        + df["away_rank_strength"].fillna(0) * 4.0
        + df["away_urgency_score"].fillna(0) * 1.5
        - away_high_absence_advisory * 0.05
    )

    lab_side_edge = (df["home_recent_lab_trust_multiplier"] - df["away_recent_lab_trust_multiplier"]) * 3.0
    df["team_edge_raw"] = (home_strength - away_strength + standings_edge + lab_side_edge).round(2)
    df["team_edge_score"] = clip(df["team_edge_raw"].abs() * 1.1, 0, 16).round(2)

    # 7) Motivation and coverage-aware absences
    df["home_motivation_num"] = df["home_motivation"].apply(motivation_to_num)
    df["away_motivation_num"] = df["away_motivation"].apply(motivation_to_num)

    df["motivation_total_score"] = clip(
        (df["home_motivation_num"].abs() + df["away_motivation_num"].abs()) * 3.0,
        0,
        6,
    ).round(2)

    df["absences_noise_penalty"] = clip(
        high_absence_advisory_penalty,
        0,
        0.15,
    ).round(2)

    # 8) Standings context bonus
    df["standings_context_score"] = clip(
        (
            df["home_urgency_score"].fillna(0)
            + df["away_urgency_score"].fillna(0)
            + df["home_rank_strength"].fillna(0)
            + df["away_rank_strength"].fillna(0)
        ) * 1.6,
        0,
        8,
    )

    df.loc[continental_world_mask, "standings_context_score"] = (
        df.loc[continental_world_mask, "standings_context_score"] * 0.55
    )

    df["standings_context_score"] = df["standings_context_score"].round(2)

    # 9) Final score
    df["vsigma_pre_score"] = (
        df["league_quality_score"]
        + df["data_quality_score"]
        + df["attack_environment_score"]
        + df["team_edge_score"]
        + df["motivation_total_score"]
        + df["standings_context_score"]
        + df["lineup_score_nudge"]
        - df["absences_noise_penalty"]
    ).round(2)

    df.loc[df["league_tier"] == "TIER_4", "vsigma_pre_score"] = (
        df.loc[df["league_tier"] == "TIER_4", "vsigma_pre_score"] - 12
    ).round(2)

    df.loc[df["data_warning"] == "NO_DATA", "vsigma_pre_score"] = (
        df.loc[df["data_warning"] == "NO_DATA", "vsigma_pre_score"] - 18
    ).round(2)

    # 10) Priority
    has_real_data = df["data_warning"].isin([
        "OK_FULL",
        "OK_PRIOR",
        "OK_STANDINGS",
        "OK_PRIOR_STANDINGS",
        "OK_FULL_STATS",
        "OK_PRIOR_STATS",
        "OK_STANDINGS_STATS",
        "OK_PRIOR_STANDINGS_STATS",
    ])

    conditions = [
        has_real_data & (df["vsigma_pre_score"] >= 66),
        has_real_data & (df["vsigma_pre_score"] >= 55),
        has_real_data & (df["vsigma_pre_score"] >= 44),
        has_real_data & (df["vsigma_pre_score"] >= 35),
    ]

    choices = [
        "A_ANALIZAR_PRIMERO",
        "B_ANALIZAR",
        "C_SOLO_SI_BLOQUE_SECO",
        "D_CONTEXT_ONLY",
    ]

    df["vsigma_priority"] = np.select(conditions, choices, default="NO_DATA_BLOCKED")

    # 11) Market hint
    df["market_family_hint"] = "NO_DATA_ENRICHMENT_REQUIRED"

    df.loc[
        has_real_data
        & (df["home_goal_path_score"] >= 7.2)
        & (df["away_goal_path_score"] >= 7.2)
        & (
            (df["home_btts_rate"].fillna(0) + df["away_btts_rate"].fillna(0) >= 0.95)
            | (df["attack_environment_score"] >= 8.8)
            | (
                (df["home_goals_for_pg"].fillna(0) + df["away_goals_for_pg"].fillna(0) >= 3.2)
                & (df["home_goals_against_pg"].fillna(0) + df["away_goals_against_pg"].fillna(0) >= 2.0)
            )
        ),
        "market_family_hint",
    ] = "OVER_OR_BTTS_CHECK"

    df.loc[
        has_real_data
        & (df["team_edge_raw"] >= 2.5)
        & (df["home_goal_path_score"] >= 6.8),
        "market_family_hint",
    ] = "HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK"

    df.loc[
        has_real_data
        & (df["team_edge_raw"] <= -2.5)
        & (df["away_goal_path_score"] >= 6.8),
        "market_family_hint",
    ] = "AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK"

    df.loc[
        has_real_data
        & (df["home_goal_path_score"] <= 5.8)
        & (df["away_goal_path_score"] <= 5.8)
        & (df["attack_environment_score"] <= 7.0)
        & (
            (df["home_over25_rate"].fillna(0) + df["away_over25_rate"].fillna(0) <= 0.85)
            | (df["home_goals_for_pg"].fillna(0) + df["away_goals_for_pg"].fillna(0) <= 2.2)
        ),
        "market_family_hint",
    ] = "UNDER_OR_TEAM_TOTAL_UNDER_CHECK"

    # 12) Order
    df = df.sort_values(
        by=["vsigma_pre_score", "league_tier_rank", "data_quality_score", "team_edge_score"],
        ascending=[False, True, False, False],
    )

    output_cols = [
        "date", "country", "league", "league_tier", "fixture_id", "home_team", "away_team", "status",
        "vsigma_pre_score", "vsigma_priority", "market_family_hint", "data_warning",
        "league_quality_score", "data_quality_score", "standings_context_score",
        "attack_environment_score", "recent_stats_process_score", "recent_lab_context_score",
        "team_edge_score", "team_edge_raw",
        "league_coverage_class", "league_data_reliability_score", "league_coverage_rich_flag",
        "league_has_odds_coverage", "league_has_fixture_stats_coverage", "league_has_injuries_coverage",
        "league_has_lineups_coverage", "league_has_predictions_coverage",
        "league_stats_reliability_multiplier", "league_coverage_uncertainty_penalty",
        "league_coverage_source_status", "league_coverage_note",
        "home_goal_path_score", "away_goal_path_score",
        "home_recent_lab_trust_multiplier", "away_recent_lab_trust_multiplier",
        "home_recent_opponent_strength_avg", "away_recent_opponent_strength_avg",
        "home_recent_schedule_difficulty_score", "away_recent_schedule_difficulty_score",
        "home_recent_schedule_quality_flag", "away_recent_schedule_quality_flag",
        "recent_schedule_balance_delta",
        "home_recent_anomaly_count_last5", "away_recent_anomaly_count_last5",
        "home_recent_clean_sample_size", "away_recent_clean_sample_size",
        "home_recent_anomaly_penalty", "away_recent_anomaly_penalty",
        "home_recent_event_coverage_flag", "away_recent_event_coverage_flag",
        "recent_sample_cleanliness_flag",
        "odds_imp_over15", "odds_imp_over25", "odds_imp_under35", "odds_imp_btts_yes",
        "odds_imp_home_win", "odds_imp_draw", "odds_imp_away_win",
        "odds_imp_home_dnb", "odds_imp_away_dnb",
        "odds_market_support_count", "odds_bookmaker_support_count", "odds_dispersion_score",
        "odds_structure_coherence_flag", "odds_total_ladder_shape", "odds_goal_expectation_band",
        "odds_side_fragility_flag", "odds_btts_support_flag", "odds_over25_support_flag",
        "odds_over15_support_flag", "odds_under35_support_flag",
        "odds_market_translation_hint", "odds_line_aggression_flag",
        "odds_confidence_adjustment_score", "odds_structure_depth_status",
        "home_injuries_count", "away_injuries_count",
        "home_injuries_available_flag", "away_injuries_available_flag",
        "home_injuries_coverage_flag", "away_injuries_coverage_flag",
        "home_absence_risk_score", "away_absence_risk_score",
        "home_absence_severity_flag", "away_absence_severity_flag",
        "injuries_quality_flag", "availability_known_risk_score",
        "availability_uncertainty_penalty", "availability_attack_penalty",
        "home_absences", "away_absences",
        "home_lineup_available_flag", "away_lineup_available_flag",
        "home_lineup_quality_flag", "away_lineup_quality_flag", "lineup_quality_flag",
        "lineup_activation_state", "lineup_activation_window_minutes",
        "lineup_minutes_to_kickoff", "lineup_timing_eligible_flag", "lineup_structural_confidence_flag",
        "home_lineup_known_starters_count", "away_lineup_known_starters_count",
        "home_lineup_bench_known_flag", "away_lineup_bench_known_flag",
        "home_lineup_attacker_count", "away_lineup_attacker_count",
        "home_lineup_defender_count", "away_lineup_defender_count",
        "home_lineup_midfielder_count", "away_lineup_midfielder_count",
        "home_lineup_goalkeeper_known_flag", "away_lineup_goalkeeper_known_flag",
        "home_lineup_attack_continuity_score", "away_lineup_attack_continuity_score",
        "home_lineup_defense_continuity_score", "away_lineup_defense_continuity_score",
        "lineup_confirmation_score", "lineup_uncertainty_penalty", "lineup_score_nudge",
        "home_rank", "away_rank", "home_points", "away_points",
        "home_goals_diff", "away_goals_diff",
        "home_urgency_score", "away_urgency_score",
        "home_form_pts", "away_form_pts",
        "home_goals_for_pg", "away_goals_for_pg",
        "home_goals_against_pg", "away_goals_against_pg",
        "home_scored_rate", "away_scored_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_btts_rate", "away_btts_rate",
        "home_over15_rate", "away_over15_rate",
        "home_over25_rate", "away_over25_rate",
        "home_recent_matches", "away_recent_matches",
        "home_recent_stats_matches_used", "away_recent_stats_matches_used",
        "home_recent_stats_coverage_ratio", "away_recent_stats_coverage_ratio",
        "home_recent_shots_for_pg", "away_recent_shots_for_pg",
        "home_recent_shots_against_pg", "away_recent_shots_against_pg",
        "home_recent_sot_for_pg", "away_recent_sot_for_pg",
        "home_recent_sot_against_pg", "away_recent_sot_against_pg",
        "home_recent_possession_pct", "away_recent_possession_pct",
        "home_recent_corners_for_pg", "away_recent_corners_for_pg",
        "home_recent_corners_against_pg", "away_recent_corners_against_pg",
        "home_recent_fouls_pg", "away_recent_fouls_pg",
        "home_recent_yellow_pg", "away_recent_yellow_pg",
        "home_recent_offsides_pg", "away_recent_offsides_pg",
        "home_recent_blocked_shots_pg", "away_recent_blocked_shots_pg",
        "recent_stats_quality_flag",
        "data_enrichment_level",
    ]

    existing_output_cols = [c for c in output_cols if c in df.columns]

    df.to_csv(OUTPUT_SCORED, index=False)
    df[existing_output_cols].head(30).to_csv(OUTPUT_TOP, index=False)

    report = (
        df.groupby(["league_tier", "vsigma_priority", "market_family_hint"])
        .size()
        .reset_index(name="matches")
        .sort_values(["league_tier", "vsigma_priority", "matches"], ascending=[True, True, False])
    )
    report.to_csv(OUTPUT_REPORT, index=False)

    print("\n=== SCORE INICIAL vSIGMA v3 COMPLETADO ===")
    print(f"Partidos recibidos del filtro: {len(df)}")
    print(f"Archivo score completo: {OUTPUT_SCORED}")
    print(f"Archivo top candidatos: {OUTPUT_TOP}")
    print(f"Archivo reporte: {OUTPUT_REPORT}")

    print("\nDistribución por prioridad:")
    print(df["vsigma_priority"].value_counts().to_string())

    print("\nDistribución por pista de mercado:")
    print(df["market_family_hint"].value_counts().to_string())

    print("\nTOP 25 candidatos iniciales:")
    print(df[existing_output_cols].head(25).to_string(index=False))


if __name__ == "__main__":
    main()
