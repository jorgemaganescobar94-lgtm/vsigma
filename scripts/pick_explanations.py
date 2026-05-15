from __future__ import annotations

from pathlib import Path

import pandas as pd


EXPLANATION_COLUMNS = [
    "pick_main_why",
    "pick_supporting_edges",
    "pick_primary_risk",
    "pick_execution_rationale",
    "pick_bucket_rationale",
    "pick_rank_rationale",
    "pick_failure_mode",
    "pick_confirmation_layers",
]

CONTROLLED_EXPLANATION_TAGS = {
    "STRONG_ROLLING_STATS",
    "ROLLING_STATS_AVAILABLE",
    "CLEAN_MARKET_FIT",
    "MARKET_FIT_NOT_REPORTED",
    "CORE_GATE_PASSED",
    "EXTENDED_GATE_PASSED",
    "STANDARD_FILL_EXECUTABLE",
    "PREMIUM_RULE_EVIDENCE",
    "STANDARD_RULE_EVIDENCE",
    "EDGE_ABOVE_THRESHOLD",
    "EDGE_STRONG",
    "MODEL_PROB_STRONG",
    "MODEL_PROB_EXTENDED_STRONG",
    "EXECUTION_SCORE_TOP",
    "SELECTION_SCORE_HIGH",
    "BET_EXECUTABLE",
    "LEAN_PLAY_EXECUTABLE",
    "AVAILABILITY_ADVISORY_ONLY",
    "AVAILABILITY_RISK_REPORTED_ONLY",
    "LINEUP_INACTIVE_NO_EDGE",
    "LINEUP_CONFIRMS_THESIS_ACTIVE",
    "LINEUP_ADVISORY_ONLY",
    "LINEUP_ATTACK_WEAKENED_ACTIVE",
    "LINEUP_DEFENSE_WEAKENED_ACTIVE",
    "COVERAGE_RICH_SUPPORT",
    "COVERAGE_PARTIAL_CAUTION",
    "COVERAGE_THIN_NO_EXTRA_TRUST",
    "COVERAGE_LIMITS_INJURIES",
    "COVERAGE_LIMITS_LINEUPS",
    "COVERAGE_LIMITS_STATS",
    "COVERAGE_LIMITS_ODDS",
    "FAILURE_MODE_DRAW_LIVE",
    "FAILURE_MODE_LOW_CONVERSION",
    "FAILURE_MODE_ONE_SIDED_STATE",
    "FAILURE_MODE_AVALANCHE_RISK",
    "FAILURE_MODE_ATTACK_THIN",
    "FAILURE_MODE_DEFENSE_THIN",
    "FAILURE_MODE_MARKET_TOO_FINE",
    "FAILURE_MODE_ONE_GOAL_SCRIPT",
    "FAILURE_MODE_BTTS_BREAK",
    "FAILURE_MODE_THIN_MARGIN",
}

FAILURE_MODE_BY_FRAGILITY = {
    "AWAY_WIN_DRAW_RISK": "DRAW_LIVE",
    "OVER_2_5_DAMAGE_SYNC_FAIL": "LOW_CONVERSION",
    "UNDER_3_5_AVALANCHE_RISK": "AVALANCHE_RISK",
}


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


def fmt(value: object, digits: int = 3, default: str = "NA") -> str:
    try:
        if pd.isna(value):
            return default
        return f"{float(value):.{digits}f}"
    except Exception:
        return default


def has_usable_odds(row: pd.Series) -> bool:
    return safe_float(row.get("primary_odds_used"), 0.0) > 1.0


def has_stats_support(row: pd.Series) -> bool:
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


def has_form_support(row: pd.Series) -> bool:
    return "home_form_pts" in row.index and "away_form_pts" in row.index and (
        not pd.isna(row.get("home_form_pts")) or not pd.isna(row.get("away_form_pts"))
    )


def lineup_tag(row: pd.Series) -> str:
    state = norm_text(row.get("lineup_activation_state"))
    quality = norm_text(row.get("lineup_quality_flag"))
    confirmation = safe_float(row.get("lineup_confirmation_score"), 0.0)
    home_attack = safe_float(row.get("home_lineup_attack_continuity_score"), 0.0)
    away_attack = safe_float(row.get("away_lineup_attack_continuity_score"), 0.0)
    home_defense = safe_float(row.get("home_lineup_defense_continuity_score"), 0.0)
    away_defense = safe_float(row.get("away_lineup_defense_continuity_score"), 0.0)

    if state == "ACTIVE" and min(home_attack, away_attack) <= -0.12:
        return "LINEUP_ATTACK_WEAKENED_ACTIVE"
    if state == "ACTIVE" and min(home_defense, away_defense) <= -0.12:
        return "LINEUP_DEFENSE_WEAKENED_ACTIVE"
    if state == "ACTIVE" and quality == "FULL" and confirmation >= 0.10:
        return "LINEUP_CONFIRMS_THESIS_ACTIVE"
    if state in {"ACTIVE", "ADVISORY_ONLY"} or quality not in {"", "NONE"}:
        return "LINEUP_ADVISORY_ONLY"
    return "LINEUP_INACTIVE_NO_EDGE"


def availability_tags(row: pd.Series) -> list[str]:
    tags = ["AVAILABILITY_ADVISORY_ONLY"]
    quality = norm_text(row.get("injuries_quality_flag"))
    known_risk = safe_float(row.get("availability_known_risk_score"), 0.0)
    home_sev = norm_text(row.get("home_absence_severity_flag"))
    away_sev = norm_text(row.get("away_absence_severity_flag"))
    if quality == "FULL" and (known_risk >= 4.0 or "HIGH" in {home_sev, away_sev}):
        tags.append("AVAILABILITY_RISK_REPORTED_ONLY")
    return tags


def coverage_tags(row: pd.Series) -> list[str]:
    if not norm_text(row.get("league_coverage_source_status")).startswith("OFFICIAL_API"):
        return []
    coverage_class = norm_text(row.get("league_coverage_class"))
    tags: list[str] = []
    if coverage_class in {"COVERAGE_RICH", "COVERAGE_GOOD"}:
        tags.append("COVERAGE_RICH_SUPPORT")
    elif coverage_class == "COVERAGE_PARTIAL":
        tags.append("COVERAGE_PARTIAL_CAUTION")
    elif coverage_class in {"COVERAGE_THIN", "COVERAGE_MINIMAL"}:
        tags.append("COVERAGE_THIN_NO_EXTRA_TRUST")

    if safe_float(row.get("league_has_fixture_stats_coverage"), 1.0) < 1:
        tags.append("COVERAGE_LIMITS_STATS")
    if safe_float(row.get("league_has_injuries_coverage"), 1.0) < 1:
        tags.append("COVERAGE_LIMITS_INJURIES")
    if safe_float(row.get("league_has_lineups_coverage"), 1.0) < 1:
        tags.append("COVERAGE_LIMITS_LINEUPS")
    if safe_float(row.get("league_has_odds_coverage"), 1.0) < 1:
        tags.append("COVERAGE_LIMITS_ODDS")
    return tags


def failure_mode(row: pd.Series) -> str:
    fragility = norm_text(row.get("execution_fragility_reason"))
    if fragility in FAILURE_MODE_BY_FRAGILITY:
        return FAILURE_MODE_BY_FRAGILITY[fragility]

    lineup = lineup_tag(row)
    if lineup == "LINEUP_ATTACK_WEAKENED_ACTIVE":
        return "ATTACK_THIN"
    if lineup == "LINEUP_DEFENSE_WEAKENED_ACTIVE":
        return "DEFENSE_THIN"

    edge = safe_float(row.get("primary_edge"), 0.0)
    if edge > 0 and edge < 0.04:
        return "THIN_MARGIN"

    market = norm_text(row.get("market_primary"))
    if market in {"HOME_WIN", "AWAY_WIN"}:
        return "DRAW_LIVE"
    if market in {"HOME_DNB", "AWAY_DNB"}:
        return "ONE_GOAL_SCRIPT"
    if market == "BTTS_YES":
        return "BTTS_BREAK"
    if market == "BTTS_NO":
        return "ONE_SIDED_STATE"
    if market == "UNDER_3_5":
        return "AVALANCHE_RISK"
    if market in {"OVER_1_5", "OVER_2_5"}:
        return "LOW_CONVERSION"
    return "MARKET_TOO_FINE"


def bucket_rationale(row: pd.Series) -> str:
    source = norm_text(row.get("execution_shortlist_source"))
    bucket = norm_text(row.get("final_execution_bucket"))
    rec = norm_text(row.get("final_recommendation"))
    market_fit = norm_text(row.get("execution_market_fit_status")) or "MARKET_FIT_NOT_REPORTED"

    if source == "PREMIUM_CORE":
        return (
            "PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; "
            f"{rec or 'UNKNOWN'}; {market_fit}"
        )
    if source == "PREMIUM_EXTENDED":
        status = norm_text(row.get("premium_extended_governance_status")) or "EXTENDED_QUALITY_OK"
        return (
            "PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; "
            f"{status}; edge>={fmt(0.08, 2)}; prob>={fmt(0.82, 2)}"
        )
    if source == "STANDARD_FILL":
        return (
            "STANDARD_FILL: STANDARD_FILL_EXECUTABLE; APPROVED_STANDARD; "
            f"{rec or 'UNKNOWN'}; {market_fit}"
        )
    return f"{source or bucket or 'UNKNOWN'}: EXECUTABLE_AFTER_FINAL_GOVERNANCE"


def supporting_tags(row: pd.Series) -> list[str]:
    tags: list[str] = []
    source = norm_text(row.get("execution_shortlist_source"))
    bucket = norm_text(row.get("final_execution_bucket"))
    recommendation = norm_text(row.get("final_recommendation"))
    market_fit = norm_text(row.get("execution_market_fit_status"))
    edge = safe_float(row.get("primary_edge"), 0.0)
    model_prob = safe_float(row.get("primary_model_prob"), 0.0)
    execution_score = safe_float(row.get("execution_score"), 0.0)
    selection_score = safe_float(row.get("selection_score"), 0.0)
    evidence_tier = norm_text(row.get("production_governance_best_evidence_tier"))

    if has_stats_support(row):
        tags.append("STRONG_ROLLING_STATS")
    elif norm_text(row.get("recent_stats_quality_flag")) not in {"", "NONE"}:
        tags.append("ROLLING_STATS_AVAILABLE")

    if market_fit == "SAFE_OK":
        tags.append("CLEAN_MARKET_FIT")
    elif not market_fit:
        tags.append("MARKET_FIT_NOT_REPORTED")

    if source == "PREMIUM_CORE":
        tags.append("CORE_GATE_PASSED")
    elif source == "PREMIUM_EXTENDED":
        tags.append("EXTENDED_GATE_PASSED")
    elif source == "STANDARD_FILL":
        tags.append("STANDARD_FILL_EXECUTABLE")

    if evidence_tier == "PREMIUM_EVIDENCE" or bucket == "APPROVED_PREMIUM":
        tags.append("PREMIUM_RULE_EVIDENCE")
    elif evidence_tier == "STANDARD_EVIDENCE" or bucket == "APPROVED_STANDARD":
        tags.append("STANDARD_RULE_EVIDENCE")

    if edge > 0:
        tags.append("EDGE_ABOVE_THRESHOLD")
    if edge >= 0.08:
        tags.append("EDGE_STRONG")
    if model_prob >= 0.75:
        tags.append("MODEL_PROB_STRONG")
    if model_prob >= 0.82:
        tags.append("MODEL_PROB_EXTENDED_STRONG")
    if execution_score >= 100.0:
        tags.append("EXECUTION_SCORE_TOP")
    if selection_score >= 80.0:
        tags.append("SELECTION_SCORE_HIGH")

    if recommendation == "BET":
        tags.append("BET_EXECUTABLE")
    elif recommendation == "LEAN_PLAY":
        tags.append("LEAN_PLAY_EXECUTABLE")

    tags.extend(availability_tags(row))
    tags.append(lineup_tag(row))
    tags.extend(coverage_tags(row))

    seen = set()
    return [tag for tag in tags if tag in CONTROLLED_EXPLANATION_TAGS and not (tag in seen or seen.add(tag))]


def confirmation_layers(row: pd.Series) -> str:
    layers: list[str] = []
    if has_stats_support(row):
        layers.append("STATS")
    if has_usable_odds(row) and safe_float(row.get("primary_edge"), 0.0) > 0:
        layers.append("ODDS")
    if norm_text(row.get("execution_market_fit_status")) == "SAFE_OK":
        layers.append("MARKET_TRANSLATION")
    if has_form_support(row):
        layers.append("FORM")
    if lineup_tag(row) == "LINEUP_CONFIRMS_THESIS_ACTIVE":
        layers.append("LINEUP_ACTIVE")
    if norm_text(row.get("injuries_quality_flag")) not in {"", "NONE"}:
        layers.append("ADVISORY_AVAILABILITY")
    if norm_text(row.get("league_coverage_class")) in {"COVERAGE_RICH", "COVERAGE_GOOD"}:
        layers.append("LEAGUE_COVERAGE")

    if not layers:
        layers.append("ODDS")
    return "+".join(layers)


def rank_rationale(row: pd.Series, rank_context: str = "EXECUTION_SHORTLIST") -> str:
    context = norm_text(rank_context) or "EXECUTION_SHORTLIST"
    source = norm_text(row.get("execution_shortlist_source"))
    execution_rank = row.get("execution_rank", "")

    if context == "SAFE_TOP5":
        return (
            "SAFE_TOP5_SORT: "
            f"mode_rank={row.get('mode_rank', '')}; source_priority={row.get('mode_source_priority', '')}; "
            f"safe_score={fmt(row.get('safe_score'), 3)}; selection_score={fmt(row.get('selection_score'), 3)}; "
            f"primary_edge={fmt(row.get('primary_edge'), 3)}; primary_model_prob={fmt(row.get('primary_model_prob'), 3)}; "
            f"execution_rank={execution_rank}; caps=league1_market1_fixture1"
        )
    if context == "BALANCED_TOP5":
        return (
            "BALANCED_TOP5_SORT: "
            f"mode_rank={row.get('mode_rank', '')}; balanced_score={fmt(row.get('balanced_score'), 3)}; "
            f"selection_score={fmt(row.get('selection_score'), 3)}; primary_edge={fmt(row.get('primary_edge'), 3)}; "
            f"primary_model_prob={fmt(row.get('primary_model_prob'), 3)}; execution_rank={execution_rank}; "
            "caps=league2_market2_fixture1"
        )
    if context == "AGGRESSIVE_TOP5":
        return (
            "AGGRESSIVE_TOP5_SORT: "
            f"mode_rank={row.get('mode_rank', '')}; aggressive_score={fmt(row.get('aggressive_score'), 3)}; "
            f"primary_edge={fmt(row.get('primary_edge'), 3)}; primary_odds_used={fmt(row.get('primary_odds_used'), 3)}; "
            f"selection_score={fmt(row.get('selection_score'), 3)}; execution_rank={execution_rank}; "
            "caps=league2_market2_fixture1"
        )

    return (
        "EXECUTION_SHORTLIST_SORT: "
        f"execution_rank={execution_rank}; phase={source or 'UNKNOWN'}; "
        f"execution_score={fmt(row.get('execution_score'), 3)}; selection_score={fmt(row.get('selection_score'), 3)}; "
        f"primary_edge={fmt(row.get('primary_edge'), 3)}; primary_model_prob={fmt(row.get('primary_model_prob'), 3)}; "
        f"shortlist_rank={row.get('shortlist_rank', '')}; caps=league2_market2_fixture1"
    )


def explanation_for_row(row: pd.Series, rank_context: str = "EXECUTION_SHORTLIST") -> dict[str, str]:
    tags = supporting_tags(row)
    failure = failure_mode(row)
    market_fit = norm_text(row.get("execution_market_fit_status")) or "MARKET_FIT_NOT_REPORTED"
    recommendation = norm_text(row.get("final_recommendation")) or "UNKNOWN"
    governance = norm_text(row.get("production_governance_status")) or norm_text(row.get("final_execution_bucket"))
    main_tags = [
        tag
        for tag in tags
        if tag
        in {
            "CORE_GATE_PASSED",
            "EXTENDED_GATE_PASSED",
            "STANDARD_FILL_EXECUTABLE",
            "STRONG_ROLLING_STATS",
            "CLEAN_MARKET_FIT",
            "COVERAGE_RICH_SUPPORT",
            "COVERAGE_PARTIAL_CAUTION",
            "COVERAGE_THIN_NO_EXTRA_TRUST",
            "EDGE_ABOVE_THRESHOLD",
            "MODEL_PROB_STRONG",
            "BET_EXECUTABLE",
            "LEAN_PLAY_EXECUTABLE",
        }
    ]
    if not main_tags:
        main_tags = tags[:4]

    return {
        "pick_main_why": ";".join(main_tags[:6]),
        "pick_supporting_edges": ";".join(tags),
        "pick_primary_risk": (
            f"FAILURE_MODE_{failure}; market={norm_text(row.get('market_primary')) or 'UNKNOWN'}; "
            f"edge={fmt(row.get('primary_edge'), 3)}; market_fit={market_fit}"
        ),
        "pick_execution_rationale": (
            f"{recommendation}; edge={fmt(row.get('primary_edge'), 3)}; "
            f"prob={fmt(row.get('primary_model_prob'), 3)}; odds={fmt(row.get('primary_odds_used'), 2)}; "
            f"{market_fit}; {governance or 'GOVERNANCE_NOT_REPORTED'}"
        ),
        "pick_bucket_rationale": bucket_rationale(row),
        "pick_rank_rationale": rank_rationale(row, rank_context),
        "pick_failure_mode": failure,
        "pick_confirmation_layers": confirmation_layers(row),
    }


def add_pick_explanations(df: pd.DataFrame, rank_context: str = "EXECUTION_SHORTLIST") -> pd.DataFrame:
    out = df.copy()
    if out.empty:
        for col in EXPLANATION_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=object)
        return out

    explanations = [explanation_for_row(row, rank_context) for _, row in out.iterrows()]
    explanation_df = pd.DataFrame(explanations, index=out.index)
    for col in EXPLANATION_COLUMNS:
        out[col] = explanation_df[col]
    return out


def write_pick_explanation_outputs(shortlist: pd.DataFrame, processed_dir: Path) -> tuple[Path, Path]:
    processed_dir.mkdir(parents=True, exist_ok=True)
    csv_path = processed_dir / "vsigma_today_pick_explanations.csv"
    report_path = processed_dir / "vsigma_today_pick_explanations_report.txt"

    id_cols = [
        "execution_rank",
        "date",
        "league",
        "fixture_id",
        "home_team",
        "away_team",
        "market_primary",
        "final_recommendation",
        "execution_shortlist_source",
        "execution_score",
        "selection_score",
        "primary_edge",
        "primary_model_prob",
    ]
    output_cols = [col for col in id_cols + EXPLANATION_COLUMNS if col in shortlist.columns]
    shortlist[output_cols].to_csv(csv_path, index=False)

    lines = ["vSIGMA today pick explanations", ""]
    if shortlist.empty:
        lines.append("No executable picks in today's shortlist.")
    else:
        ordered = shortlist.sort_values("execution_rank") if "execution_rank" in shortlist.columns else shortlist
        for _, row in ordered.iterrows():
            lines.extend(
                [
                    (
                        f"#{row.get('execution_rank', '')} {row.get('home_team', '')} vs {row.get('away_team', '')} "
                        f"| {row.get('league', '')} | {row.get('market_primary', '')} | {row.get('final_recommendation', '')}"
                    ),
                    f"Por que sobrevive: {row.get('pick_main_why', '')}",
                    f"Bucket: {row.get('pick_bucket_rationale', '')}",
                    f"Soporte: {row.get('pick_supporting_edges', '')}",
                    f"Riesgo principal: {row.get('pick_primary_risk', '')}",
                    f"Ranking: {row.get('pick_rank_rationale', '')}",
                    f"Capas: {row.get('pick_confirmation_layers', '')}",
                    "",
                ]
            )

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return csv_path, report_path
