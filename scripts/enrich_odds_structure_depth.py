from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
from typing import Any

import numpy as np
import pandas as pd

try:
    from api_football_client import APIFootballClient, APIFootballError
except ModuleNotFoundError:
    from scripts.api_football_client import APIFootballClient, APIFootballError


ROOT = Path(__file__).resolve().parents[1]

RAW_MATCHES = ROOT / "data" / "raw" / "matches.csv"
FILTERED_MATCHES = ROOT / "data" / "processed" / "matches_league_filtered.csv"
BACKUP_MATCHES = ROOT / "data" / "raw" / "matches_before_odds_structure_depth_backup.csv"
SUMMARY_PATH = ROOT / "data" / "processed" / "vsigma_odds_structure_depth_summary.csv"
REPORT_PATH = ROOT / "data" / "processed" / "vsigma_odds_structure_depth_report.txt"

MAX_TIER_RANK_TO_ENRICH = 2

BET_MATCH_WINNER = 1
BET_GOALS_OU = 5
BET_BTTS = 8
BET_HOME_NO_BET = 206
BET_AWAY_NO_BET = 207

ODDS_DEPTH_NUMERIC_FIELDS = [
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

ODDS_DEPTH_TEXT_FIELDS = [
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
    "odds_structure_depth_error",
    "odds_structure_depth_updated_at",
]

ODDS_DEPTH_FIELDS = [*ODDS_DEPTH_NUMERIC_FIELDS, *ODDS_DEPTH_TEXT_FIELDS]


ODDS_COLUMN_FALLBACKS = {
    "OVER_1_5": "odds_over_1_5_v3",
    "OVER_2_5": "odds_over_2_5_v3",
    "UNDER_3_5": "odds_under_3_5_v3",
    "BTTS_YES": "odds_btts_yes_v3",
    "HOME_WIN": "odds_1_home_v3",
    "DRAW": "odds_1_draw_v3",
    "AWAY_WIN": "odds_1_away_v3",
    "HOME_DNB": "odds_home_dnb_v3",
    "AWAY_DNB": "odds_away_dnb_v3",
}

OUTPUT_FIELD_BY_MARKET = {
    "OVER_1_5": "odds_imp_over15",
    "OVER_2_5": "odds_imp_over25",
    "UNDER_3_5": "odds_imp_under35",
    "BTTS_YES": "odds_imp_btts_yes",
    "HOME_WIN": "odds_imp_home_win",
    "DRAW": "odds_imp_draw",
    "AWAY_WIN": "odds_imp_away_win",
    "HOME_DNB": "odds_imp_home_dnb",
    "AWAY_DNB": "odds_imp_away_dnb",
}


@dataclass
class ParsedOdds:
    values: dict[str, list[float]]
    bookmaker_ids: set[str]


def safe_float(value: object) -> float:
    try:
        if pd.isna(value):
            return np.nan
        number = float(str(value).strip().replace(",", "."))
        return number if number > 1.0 else np.nan
    except Exception:
        return np.nan


def implied_prob(odd: object) -> float:
    odd_float = safe_float(odd)
    if pd.isna(odd_float):
        return np.nan
    return 1.0 / odd_float


def norm_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def print_console(value: object = "") -> None:
    text = str(value)
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def empty_market_values() -> dict[str, list[float]]:
    return {key: [] for key in OUTPUT_FIELD_BY_MARKET}


def append_odd(values: dict[str, list[float]], market_key: str, odd: object) -> None:
    odd_float = safe_float(odd)
    if not pd.isna(odd_float):
        values.setdefault(market_key, []).append(float(odd_float))


def parse_odds_payload(payload: dict[str, Any]) -> ParsedOdds:
    values = empty_market_values()
    bookmaker_ids: set[str] = set()

    for item in payload.get("response", []) or []:
        for bookmaker in item.get("bookmakers", []) or []:
            bookmaker_id = bookmaker.get("id") or bookmaker.get("name") or f"bookmaker_{len(bookmaker_ids) + 1}"
            bookmaker_ids.add(str(bookmaker_id))
            for bet in bookmaker.get("bets", []) or []:
                bet_id = bet.get("id")
                for value in bet.get("values", []) or []:
                    label = norm_text(value.get("value"))
                    odd = value.get("odd")

                    if bet_id == BET_MATCH_WINNER:
                        if label == "home":
                            append_odd(values, "HOME_WIN", odd)
                        elif label == "draw":
                            append_odd(values, "DRAW", odd)
                        elif label == "away":
                            append_odd(values, "AWAY_WIN", odd)
                    elif bet_id == BET_BTTS:
                        if label == "yes":
                            append_odd(values, "BTTS_YES", odd)
                    elif bet_id == BET_GOALS_OU:
                        if label == "over 1.5":
                            append_odd(values, "OVER_1_5", odd)
                        elif label == "over 2.5":
                            append_odd(values, "OVER_2_5", odd)
                        elif label == "under 3.5":
                            append_odd(values, "UNDER_3_5", odd)
                    elif bet_id == BET_HOME_NO_BET:
                        append_odd(values, "HOME_DNB", odd)
                    elif bet_id == BET_AWAY_NO_BET:
                        append_odd(values, "AWAY_DNB", odd)

    return ParsedOdds(values=values, bookmaker_ids=bookmaker_ids)


def odds_from_existing_row(row: pd.Series) -> ParsedOdds:
    values = empty_market_values()
    for market_key, column in ODDS_COLUMN_FALLBACKS.items():
        if column in row.index:
            append_odd(values, market_key, row.get(column))

    bookmaker_count = pd.to_numeric(
        pd.Series([row.get("odds_bookmakers_count_v3", np.nan)]),
        errors="coerce",
    ).iloc[0]
    if pd.isna(bookmaker_count) or bookmaker_count <= 0:
        bookmaker_ids: set[str] = set()
    else:
        bookmaker_ids = {f"fallback_{idx}" for idx in range(int(bookmaker_count))}
    return ParsedOdds(values=values, bookmaker_ids=bookmaker_ids)


def mean_implied(odds: list[float]) -> float:
    probs = [implied_prob(odd) for odd in odds]
    probs = [float(prob) for prob in probs if not pd.isna(prob)]
    if not probs:
        return np.nan
    return round(float(np.mean(probs)), 6)


def market_dispersion(odds: list[float]) -> float:
    probs = np.array([implied_prob(odd) for odd in odds], dtype=float)
    probs = probs[~np.isnan(probs)]
    if len(probs) < 2:
        return np.nan
    mean = float(np.mean(probs))
    if mean <= 0:
        return np.nan
    return float((np.max(probs) - np.min(probs)) / mean)


def clipped_adjustment(value: float) -> float:
    return round(float(np.clip(value, -0.04, 0.035)), 4)


def support_flag(prob: float, support_count: int, strong_threshold: float, weak_threshold: float) -> str:
    if support_count <= 0 or pd.isna(prob):
        return "UNKNOWN"
    if prob >= strong_threshold:
        return "SUPPORTED"
    if prob >= weak_threshold:
        return "MIXED"
    return "WEAK"


def derive_depth_fields(parsed: ParsedOdds) -> dict[str, object]:
    values = parsed.values
    support_count = sum(1 for odds in values.values() if odds)
    bookmaker_count = len(parsed.bookmaker_ids)

    output: dict[str, object] = {}
    for market_key, field_name in OUTPUT_FIELD_BY_MARKET.items():
        output[field_name] = mean_implied(values.get(market_key, []))

    dispersions = [
        market_dispersion(values.get(market_key, []))
        for market_key in ["OVER_1_5", "OVER_2_5", "UNDER_3_5", "BTTS_YES", "HOME_WIN", "DRAW", "AWAY_WIN"]
    ]
    dispersions = [value for value in dispersions if not pd.isna(value)]
    raw_dispersion = float(np.mean(dispersions)) if dispersions else np.nan
    dispersion_score = 0.0 if pd.isna(raw_dispersion) else round(float(np.clip(raw_dispersion / 0.28, 0.0, 1.0)), 4)

    over15 = output["odds_imp_over15"]
    over25 = output["odds_imp_over25"]
    under35 = output["odds_imp_under35"]
    btts = output["odds_imp_btts_yes"]
    home = output["odds_imp_home_win"]
    draw = output["odds_imp_draw"]
    away = output["odds_imp_away_win"]

    if support_count == 0:
        coherence = "NO_ODDS_UNCERTAIN"
    elif bookmaker_count < 2 or support_count < 4:
        coherence = "THIN_UNCERTAIN"
    elif dispersion_score <= 0.35:
        coherence = "RICH_COHERENT"
    elif dispersion_score <= 0.65:
        coherence = "RICH_MIXED"
    else:
        coherence = "RICH_NOISY"

    if pd.isna(over15) or pd.isna(over25) or pd.isna(under35):
        ladder_shape = "UNKNOWN"
        goal_band = "UNKNOWN"
        line_aggression = "UNKNOWN"
    elif over25 >= 0.56 and over15 >= 0.74:
        ladder_shape = "WIDE_GOALS" if under35 <= 0.60 else "BROAD_GOALS"
        goal_band = "HIGH"
        line_aggression = "OVER_2_5_SUPPORTED"
    elif over15 >= 0.72 and over25 < 0.52 and under35 >= 0.66:
        ladder_shape = "MILD_GOALS"
        goal_band = "MEDIUM"
        line_aggression = "PREFER_OVER_1_5"
    elif over15 < 0.68 and over25 < 0.46 and under35 >= 0.72:
        ladder_shape = "LOW_GOALS"
        goal_band = "LOW"
        line_aggression = "AVOID_AGGRESSIVE_OVERS"
    else:
        ladder_shape = "BALANCED"
        goal_band = "MEDIUM"
        line_aggression = "NEUTRAL"

    btts_flag = support_flag(btts, len(values.get("BTTS_YES", [])), 0.54, 0.50)
    over25_flag = support_flag(over25, len(values.get("OVER_2_5", [])), 0.55, 0.50)
    over15_flag = support_flag(over15, len(values.get("OVER_1_5", [])), 0.72, 0.66)
    under35_flag = support_flag(under35, len(values.get("UNDER_3_5", [])), 0.68, 0.60)

    side_fragility = "UNKNOWN"
    if not any(pd.isna(value) for value in [home, draw, away]):
        favorite = max(float(home), float(away))
        if float(draw) >= 0.27 and favorite <= 0.54:
            side_fragility = "DRAW_LIVE_FRAGILITY"
        elif abs(float(home) - float(away)) <= 0.07:
            side_fragility = "BALANCED_SIDE_PRICE"
        else:
            side_fragility = "SIDE_PRICE_CLEANER"

    if coherence in {"NO_ODDS_UNCERTAIN", "THIN_UNCERTAIN"}:
        translation_hint = "ODDS_DEPTH_UNCERTAIN"
        adjustment = 0.0
    elif line_aggression in {"PREFER_OVER_1_5", "AVOID_AGGRESSIVE_OVERS"}:
        translation_hint = "PREFER_MILDER_TOTAL"
        adjustment = -0.015
    elif ladder_shape in {"BROAD_GOALS", "WIDE_GOALS"} and over25_flag == "SUPPORTED":
        translation_hint = "ALLOW_AGGRESSIVE_TOTAL"
        adjustment = 0.025
    elif side_fragility == "DRAW_LIVE_FRAGILITY":
        translation_hint = "CAUTION_FRAGILE_SIDE"
        adjustment = -0.015
    elif btts_flag == "WEAK":
        translation_hint = "CAUTION_BTTS"
        adjustment = -0.01
    else:
        translation_hint = "NEUTRAL"
        adjustment = 0.0

    if coherence == "RICH_NOISY":
        adjustment -= 0.01
    elif coherence == "RICH_COHERENT" and adjustment > 0:
        adjustment += 0.005

    output.update(
        {
            "odds_market_support_count": int(support_count),
            "odds_bookmaker_support_count": int(bookmaker_count),
            "odds_dispersion_score": dispersion_score,
            "odds_structure_coherence_flag": coherence,
            "odds_total_ladder_shape": ladder_shape,
            "odds_goal_expectation_band": goal_band,
            "odds_side_fragility_flag": side_fragility,
            "odds_btts_support_flag": btts_flag,
            "odds_over25_support_flag": over25_flag,
            "odds_over15_support_flag": over15_flag,
            "odds_under35_support_flag": under35_flag,
            "odds_market_translation_hint": translation_hint,
            "odds_line_aggression_flag": line_aggression,
            "odds_confidence_adjustment_score": clipped_adjustment(adjustment),
        }
    )
    return output


def ensure_depth_columns(raw: pd.DataFrame) -> pd.DataFrame:
    missing = {}
    for col in ODDS_DEPTH_NUMERIC_FIELDS:
        if col not in raw.columns:
            missing[col] = np.nan
    for col in ODDS_DEPTH_TEXT_FIELDS:
        if col not in raw.columns:
            missing[col] = ""
        else:
            raw[col] = raw[col].astype("object")
    if missing:
        raw = pd.concat([raw, pd.DataFrame(missing, index=raw.index)], axis=1)
    return raw


def summarize_depth(raw: pd.DataFrame, target_fixture_ids: set[object]) -> pd.DataFrame:
    target = raw[raw["fixture_id"].isin(target_fixture_ids)].copy() if "fixture_id" in raw.columns else raw.iloc[0:0].copy()
    rows = [
        {
            "summary_scope": "overall",
            "metric": "target_fixtures",
            "rows_total": int(len(target)),
        }
    ]
    for col in [
        "odds_structure_depth_status",
        "odds_structure_coherence_flag",
        "odds_total_ladder_shape",
        "odds_market_translation_hint",
        "odds_line_aggression_flag",
    ]:
        if col in target.columns:
            for value, count in target[col].fillna("").astype(str).value_counts(dropna=False).items():
                rows.append(
                    {
                        "summary_scope": col,
                        "metric": value or "BLANK",
                        "rows_total": int(count),
                    }
                )
    return pd.DataFrame(rows)


def write_report(path: Path, summary: pd.DataFrame, preview: pd.DataFrame) -> None:
    display_cols = [
        "fixture_id",
        "league",
        "home_team",
        "away_team",
        "odds_structure_coherence_flag",
        "odds_total_ladder_shape",
        "odds_market_translation_hint",
        "odds_line_aggression_flag",
        "odds_dispersion_score",
        "odds_confidence_adjustment_score",
    ]
    existing = [col for col in display_cols if col in preview.columns]
    lines = [
        "vSIGMA ODDS STRUCTURE DEPTH",
        "",
        "Purpose: lab-only market translation governance from paid odds ladder depth.",
        "Missing or thin odds are treated as uncertainty, not as a negative football signal.",
        "",
        "Summary",
        summary.to_string(index=False) if not summary.empty else "No summary rows.",
        "",
        "Fixture preview",
        preview[existing].to_string(index=False) if not preview.empty and existing else "No fixture rows.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def enrich_odds_structure_depth(
    raw: pd.DataFrame,
    filtered: pd.DataFrame,
    client: APIFootballClient | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = ensure_depth_columns(raw.copy())
    filtered = filtered.copy()
    tier = pd.to_numeric(filtered.get("league_tier_rank"), errors="coerce")
    targets = filtered[tier.le(MAX_TIER_RANK_TO_ENRICH)].copy()

    rows = []
    for _, match in targets.iterrows():
        fixture_id = match.get("fixture_id")
        raw_idx_list = raw.index[raw["fixture_id"].eq(fixture_id)].tolist()
        if not raw_idx_list:
            continue
        raw_idx = raw_idx_list[0]
        status = "OK"
        error = ""

        parsed: ParsedOdds
        try:
            if client is not None:
                payload = client.odds(fixture=fixture_id)
                parsed = parse_odds_payload(payload)
                if sum(1 for odds in parsed.values.values() if odds) == 0:
                    parsed = odds_from_existing_row(raw.loc[raw_idx])
                    status = "FALLBACK_EXISTING_ODDS" if sum(1 for odds in parsed.values.values() if odds) else "NO_ODDS_FOUND"
            else:
                parsed = odds_from_existing_row(raw.loc[raw_idx])
                status = "FALLBACK_EXISTING_ODDS" if sum(1 for odds in parsed.values.values() if odds) else "NO_ODDS_FOUND"
        except APIFootballError as exc:
            parsed = odds_from_existing_row(raw.loc[raw_idx])
            status = "API_ERROR_FALLBACK" if sum(1 for odds in parsed.values.values() if odds) else "API_ERROR_NO_ODDS"
            error = str(exc)
        except Exception as exc:
            parsed = odds_from_existing_row(raw.loc[raw_idx])
            status = "ERROR_FALLBACK" if sum(1 for odds in parsed.values.values() if odds) else "ERROR_NO_ODDS"
            error = str(exc)

        fields = derive_depth_fields(parsed)
        fields["odds_structure_depth_status"] = status
        fields["odds_structure_depth_error"] = error
        fields["odds_structure_depth_updated_at"] = datetime.now(timezone.utc).isoformat()

        for col, value in fields.items():
            raw.loc[raw_idx, col] = value

        rows.append(
            {
                "fixture_id": fixture_id,
                "league": match.get("league"),
                "home_team": match.get("home_team"),
                "away_team": match.get("away_team"),
                **fields,
            }
        )

    return raw, pd.DataFrame(rows)


def main() -> None:
    if not RAW_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {RAW_MATCHES}")
    if not FILTERED_MATCHES.exists():
        raise FileNotFoundError(f"No existe: {FILTERED_MATCHES}")

    raw = pd.read_csv(RAW_MATCHES)
    filtered = pd.read_csv(FILTERED_MATCHES)

    if not BACKUP_MATCHES.exists():
        shutil.copy2(RAW_MATCHES, BACKUP_MATCHES)

    client = APIFootballClient()
    enriched, preview = enrich_odds_structure_depth(raw, filtered, client)
    enriched.to_csv(RAW_MATCHES, index=False)

    target_ids = set(preview["fixture_id"].tolist()) if not preview.empty else set()
    summary = summarize_depth(enriched, target_ids)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_PATH, index=False)
    write_report(REPORT_PATH, summary, preview)

    print("\n=== ODDS STRUCTURE DEPTH COMPLETADO ===")
    print(f"Target fixtures: {len(preview)}")
    print(f"Raw CSV updated: {RAW_MATCHES}")
    print(f"Summary: {SUMMARY_PATH}")
    print(f"Report: {REPORT_PATH}")
    if not preview.empty:
        display_cols = [
            "fixture_id",
            "home_team",
            "away_team",
            "odds_structure_coherence_flag",
            "odds_total_ladder_shape",
            "odds_market_translation_hint",
            "odds_line_aggression_flag",
            "odds_confidence_adjustment_score",
        ]
        print_console(preview[[c for c in display_cols if c in preview.columns]].to_string(index=False))


if __name__ == "__main__":
    main()
