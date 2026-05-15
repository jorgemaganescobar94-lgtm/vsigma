from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"

DEFAULT_INPUT = PROCESSED_DIR / "matches_league_filtered.csv"
DEFAULT_OUTPUT = PROCESSED_DIR / "matches_player_impact_enriched.csv"
DEFAULT_REPORT = PROCESSED_DIR / "player_impact_enrichment_report.csv"

PLAYER_IMPACT_NUMERIC_COLUMNS = [
    "home_attacking_core_available_score",
    "away_attacking_core_available_score",
    "home_defensive_core_available_score",
    "away_defensive_core_available_score",
    "player_impact_uncertainty_penalty",
]

PLAYER_IMPACT_TEXT_COLUMNS = [
    "home_goalkeeper_confidence_flag",
    "away_goalkeeper_confidence_flag",
    "home_player_impact_coverage_flag",
    "away_player_impact_coverage_flag",
    "player_impact_quality_flag",
    "player_impact_market_translation_hint",
]

PLAYER_IMPACT_COLUMNS = [*PLAYER_IMPACT_NUMERIC_COLUMNS, *PLAYER_IMPACT_TEXT_COLUMNS]

FULL_QUALITY = {"FULL", "CONFIRMED"}
PARTIAL_QUALITY = {"PARTIAL", "ADVISORY_ONLY"}
SUPPORTED_INJURY_QUALITY = {"FULL", "PARTIAL"}


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


def clip(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def team_coverage(row: pd.Series, side: str) -> str:
    lineup_quality = norm_upper(row.get(f"{side}_lineup_quality_flag"))
    lineup_available = safe_float(row.get(f"{side}_lineup_available_flag"), 0.0) >= 1.0
    starters = safe_float(row.get(f"{side}_lineup_known_starters_count"), 0.0)
    injury_quality = norm_upper(row.get("injuries_quality_flag"))
    injury_coverage = norm_upper(row.get(f"{side}_injuries_coverage_flag"))

    lineup_full = lineup_available and lineup_quality in FULL_QUALITY and starters >= 10
    lineup_partial = lineup_available and (lineup_quality in PARTIAL_QUALITY or starters >= 7)
    injury_supported = injury_quality in SUPPORTED_INJURY_QUALITY and injury_coverage in {"FULL", "PARTIAL"}

    if lineup_full and injury_supported:
        return "FULL"
    if lineup_full or (lineup_partial and injury_supported):
        return "PARTIAL"
    return "NONE"


def goalkeeper_flag(row: pd.Series, side: str, coverage: str) -> str:
    if coverage == "NONE":
        return "UNKNOWN_COVERAGE"
    gk_known = safe_float(row.get(f"{side}_lineup_goalkeeper_known_flag"), np.nan)
    if not pd.isna(gk_known) and gk_known >= 1.0:
        return "CONFIRMED"
    if norm_upper(row.get(f"{side}_lineup_quality_flag")) in FULL_QUALITY:
        return "UNCERTAIN"
    return "UNKNOWN_COVERAGE"


def attacking_core_score(row: pd.Series, side: str, coverage: str) -> float:
    if coverage == "NONE":
        return 0.0

    lineup_attack = safe_float(row.get(f"{side}_lineup_attack_continuity_score"), 0.0)
    attackers = safe_float(row.get(f"{side}_lineup_attacker_count"), np.nan)
    midfielders = safe_float(row.get(f"{side}_lineup_midfielder_count"), np.nan)
    absence_risk = safe_float(row.get(f"{side}_absence_risk_score"), 0.0)
    absence_severity = norm_upper(row.get(f"{side}_absence_severity_flag"))

    score = lineup_attack * 0.55
    if not pd.isna(attackers):
        if attackers <= 1:
            score -= 0.10
        elif attackers >= 3:
            score += 0.05
    if not pd.isna(midfielders) and midfielders <= 2:
        score -= 0.04
    if absence_severity == "HIGH" or absence_risk >= 3.0:
        score -= 0.12
    elif absence_severity == "MEDIUM" or absence_risk >= 1.5:
        score -= 0.05
    if coverage == "PARTIAL":
        score *= 0.55
    return round(clip(score, -0.25, 0.20), 3)


def defensive_core_score(row: pd.Series, side: str, coverage: str, gk_flag: str) -> float:
    if coverage == "NONE":
        return 0.0

    lineup_defense = safe_float(row.get(f"{side}_lineup_defense_continuity_score"), 0.0)
    defenders = safe_float(row.get(f"{side}_lineup_defender_count"), np.nan)
    absence_risk = safe_float(row.get(f"{side}_absence_risk_score"), 0.0)
    absence_severity = norm_upper(row.get(f"{side}_absence_severity_flag"))

    score = lineup_defense * 0.55
    if not pd.isna(defenders):
        if defenders <= 2:
            score -= 0.10
        elif defenders >= 4:
            score += 0.04
    if gk_flag == "UNCERTAIN":
        score -= 0.10
    if absence_severity == "HIGH" or absence_risk >= 3.0:
        score -= 0.10
    elif absence_severity == "MEDIUM" or absence_risk >= 1.5:
        score -= 0.04
    if coverage == "PARTIAL":
        score *= 0.55
    return round(clip(score, -0.25, 0.20), 3)


def quality_flag(home_coverage: str, away_coverage: str) -> str:
    if home_coverage == "FULL" and away_coverage == "FULL":
        return "FULL"
    if home_coverage != "NONE" or away_coverage != "NONE":
        return "PARTIAL"
    return "NONE"


def market_translation_hint(features: dict[str, Any]) -> str:
    quality = features["player_impact_quality_flag"]
    if quality == "NONE":
        return "PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE"

    home_attack = float(features["home_attacking_core_available_score"])
    away_attack = float(features["away_attacking_core_available_score"])
    home_defense = float(features["home_defensive_core_available_score"])
    away_defense = float(features["away_defensive_core_available_score"])
    gk_uncertain = (
        features["home_goalkeeper_confidence_flag"] == "UNCERTAIN"
        or features["away_goalkeeper_confidence_flag"] == "UNCERTAIN"
    )

    weak_attack_sides = sum(score <= -0.10 for score in [home_attack, away_attack])
    weak_defense_sides = sum(score <= -0.10 for score in [home_defense, away_defense])

    if weak_attack_sides >= 2:
        return "BOTH_ATTACKING_CORES_WEAKENED_DOWNGRADE_GOALS"
    if weak_attack_sides == 1:
        return "ONE_ATTACKING_CORE_WEAKENED_BTTS_O25_CAUTION"
    if weak_defense_sides >= 1 or gk_uncertain:
        return "DEFENSIVE_OR_GK_WEAKNESS_SUPPORTS_GOALS_SIDE_RISK"
    if home_attack >= 0.08 and away_attack >= 0.08:
        return "LINEUPS_CONFIRM_ATTACKING_THESIS"
    return "PLAYER_IMPACT_NEUTRAL"


def build_player_impact_features(row: pd.Series) -> dict[str, Any]:
    home_coverage = team_coverage(row, "home")
    away_coverage = team_coverage(row, "away")
    home_gk = goalkeeper_flag(row, "home", home_coverage)
    away_gk = goalkeeper_flag(row, "away", away_coverage)

    features: dict[str, Any] = {
        "home_player_impact_coverage_flag": home_coverage,
        "away_player_impact_coverage_flag": away_coverage,
        "player_impact_quality_flag": quality_flag(home_coverage, away_coverage),
        "home_goalkeeper_confidence_flag": home_gk,
        "away_goalkeeper_confidence_flag": away_gk,
    }
    features["home_attacking_core_available_score"] = attacking_core_score(row, "home", home_coverage)
    features["away_attacking_core_available_score"] = attacking_core_score(row, "away", away_coverage)
    features["home_defensive_core_available_score"] = defensive_core_score(row, "home", home_coverage, home_gk)
    features["away_defensive_core_available_score"] = defensive_core_score(row, "away", away_coverage, away_gk)

    quality = features["player_impact_quality_flag"]
    features["player_impact_uncertainty_penalty"] = {
        "FULL": 0.0,
        "PARTIAL": 0.02,
        "NONE": 0.0,
    }[quality]
    features["player_impact_market_translation_hint"] = market_translation_hint(features)
    return features


def add_player_impact_fields(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if out.empty:
        for col in PLAYER_IMPACT_NUMERIC_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=float)
        for col in PLAYER_IMPACT_TEXT_COLUMNS:
            if col not in out.columns:
                out[col] = pd.Series(dtype=object)
        return out

    features = pd.DataFrame([build_player_impact_features(row) for _, row in out.iterrows()], index=out.index)
    out = out.drop(columns=[col for col in PLAYER_IMPACT_COLUMNS if col in out.columns], errors="ignore")
    return pd.concat([out, features], axis=1)


def build_report(source: pd.DataFrame, enriched: pd.DataFrame) -> pd.DataFrame:
    quality = enriched.get("player_impact_quality_flag", pd.Series(dtype=object)).map(norm_upper)
    hints = enriched.get("player_impact_market_translation_hint", pd.Series(dtype=object)).map(norm_upper)
    return pd.DataFrame(
        [
            {
                "rows_processed": int(len(enriched)),
                "full_rows": int(quality.eq("FULL").sum()),
                "partial_rows": int(quality.eq("PARTIAL").sum()),
                "none_rows": int(quality.eq("NONE").sum()),
                "attack_weakened_rows": int(hints.str.contains("ATTACKING_CORE", na=False).sum()),
                "defense_or_gk_risk_rows": int(hints.str.contains("DEFENSIVE_OR_GK", na=False).sum()),
                "input_columns": int(len(source.columns)),
                "output_columns": int(len(enriched.columns)),
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        ]
    )


def enrich_file(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT, report_path: Path = DEFAULT_REPORT) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Missing player impact input: {input_path}")
    source = pd.read_csv(input_path)
    enriched = add_player_impact_fields(source)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(output_path, index=False)
    build_report(source, enriched).to_csv(report_path, index=False)
    return enriched


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add conservative player-impact fields from lineup/injury coverage.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    enriched = enrich_file(Path(args.input), Path(args.output), Path(args.report))
    print("\n=== PLAYER IMPACT ENRICHMENT COMPLETADO ===")
    print(f"Rows processed: {len(enriched)}")
    print(f"Output: {Path(args.output)}")
    print(f"Report: {Path(args.report)}")


if __name__ == "__main__":
    main()
