from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path

import pandas as pd


DEFAULT_PROCESSED_DIR = Path("data/processed")
DEFAULT_INPUT = "vsigma_today_competition_top.csv"
DEFAULT_OUTPUT = "vsigma_today_match_script_forecasts.csv"
DEFAULT_REPORT = "vsigma_today_match_script_forecasts_report.txt"

FORECAST_COLUMNS = [
    "forecast_rank",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "predicted_match_script",
    "predicted_score_main",
    "predicted_score_alt",
    "predicted_home_xg_range",
    "predicted_away_xg_range",
    "predicted_home_shots_range",
    "predicted_away_shots_range",
    "predicted_home_sot_range",
    "predicted_away_sot_range",
    "predicted_total_corners_range",
    "predicted_possession_split",
    "predicted_pick_path",
    "predicted_pick_breaker",
    "predicted_total_goals_range",
    "predicted_first_goal_side",
    "predicted_state_gravity",
    "forecast_confidence_band",
    "forecast_inputs_used",
]


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


def num_or_none(value: object) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def range_text(center: float, spread: float, low: float = 0.0, high: float = 99.0, digits: int = 1) -> str:
    left = clamp(center - spread, low, high)
    right = clamp(center + spread, low, high)
    return f"{left:.{digits}f}-{right:.{digits}f}"


def int_range_text(center: float, spread: float, low: int = 0, high: int = 99) -> str:
    left = int(round(clamp(center - spread, low, high)))
    right = int(round(clamp(center + spread, low, high)))
    if right < left:
        right = left
    return f"{left}-{right}"


def blended_stat(row: pd.Series, side: str, stat: str, fallback: float) -> float:
    other = "away" if side == "home" else "home"
    own = num_or_none(row.get(f"{side}_recent_{stat}_for_pg"))
    against = num_or_none(row.get(f"{other}_recent_{stat}_against_pg"))
    values = [value for value in [own, against] if value is not None]
    if not values:
        return fallback
    return sum(values) / len(values)


def projected_goals(row: pd.Series) -> tuple[float, float]:
    home = num_or_none(row.get("projected_home_goals"))
    away = num_or_none(row.get("projected_away_goals"))
    if home is not None and away is not None:
        return clamp(home, 0.2, 4.2), clamp(away, 0.2, 4.2)

    home_gf = safe_float(row.get("home_goals_for_pg"), 1.25)
    home_ga = safe_float(row.get("home_goals_against_pg"), 1.25)
    away_gf = safe_float(row.get("away_goals_for_pg"), 1.25)
    away_ga = safe_float(row.get("away_goals_against_pg"), 1.25)
    return clamp((home_gf + away_ga) / 2.0, 0.2, 4.2), clamp((away_gf + home_ga) / 2.0, 0.2, 4.2)


def modal_score(row: pd.Series, home_xg: float, away_xg: float) -> tuple[str, str]:
    market = norm_upper(row.get("market_primary"))
    home = int(round(home_xg))
    away = int(round(away_xg))
    total = home + away

    if market == "OVER_2_5" and total < 3:
        if home_xg >= away_xg:
            home = max(home, 2)
            away = max(away, 1)
        else:
            home = max(home, 1)
            away = max(away, 2)
    elif market == "OVER_1_5" and total < 2:
        if home_xg >= away_xg:
            home = max(home, 1)
            away = max(away, 1)
        else:
            home = max(home, 1)
            away = max(away, 1)
    elif market == "UNDER_3_5" and total > 3:
        if home_xg >= away_xg:
            home, away = 2, 1
        else:
            home, away = 1, 2
    elif market in {"HOME_WIN", "HOME_DNB"} and home <= away:
        home = away + 1
    elif market in {"AWAY_WIN", "AWAY_DNB"} and away <= home:
        away = home + 1
    elif market == "BTTS_YES":
        home = max(home, 1)
        away = max(away, 1)
    elif market == "BTTS_NO":
        if home_xg >= away_xg:
            away = 0
        else:
            home = 0

    home = int(clamp(home, 0, 5))
    away = int(clamp(away, 0, 5))
    main = f"{home}-{away}"

    if market in {"OVER_2_5", "BTTS_YES"}:
        alt_home = max(1, min(3, home - 1 if home > away + 1 else home))
        alt_away = max(1, min(3, away - 1 if away > home + 1 else away))
        if alt_home + alt_away < 3 and market == "OVER_2_5":
            if home_xg >= away_xg:
                alt_home += 1
            else:
                alt_away += 1
    elif market == "UNDER_3_5":
        alt_home, alt_away = (1, 1) if home_xg + away_xg >= 2.0 else (1, 0)
    elif market in {"HOME_WIN", "HOME_DNB"}:
        alt_home, alt_away = max(1, home), max(0, home - 1)
    elif market in {"AWAY_WIN", "AWAY_DNB"}:
        alt_home, alt_away = max(0, away - 1), max(1, away)
    else:
        alt_home, alt_away = max(0, home - 1), max(0, away)

    alt = f"{int(clamp(alt_home, 0, 5))}-{int(clamp(alt_away, 0, 5))}"
    if alt == main:
        alt = likely_scoreline_alt(row, main, home_xg, away_xg)
    return main, alt


def likely_scoreline_alt(row: pd.Series, main: str, home_xg: float, away_xg: float) -> str:
    raw = norm_text(row.get("likely_scoreline"))
    if raw:
        for part in raw.replace("/", "|").split("|"):
            score = part.strip()
            if score and score != main:
                return score
    if home_xg >= away_xg:
        return "1-1" if main != "1-1" else "2-1"
    return "1-1" if main != "1-1" else "1-2"


def possession_split(row: pd.Series, home_xg: float, away_xg: float) -> str:
    home_pos = num_or_none(row.get("home_recent_possession_pct"))
    away_pos = num_or_none(row.get("away_recent_possession_pct"))
    if home_pos is not None and away_pos is not None and home_pos + away_pos > 0:
        home_share = home_pos / (home_pos + away_pos) * 100.0
    else:
        home_share = 50.0 + clamp((home_xg - away_xg) * 4.0, -8.0, 8.0)
    home_low = int(round(clamp(home_share - 4.0, 35.0, 65.0)))
    home_high = int(round(clamp(home_share + 4.0, 35.0, 65.0)))
    away_high = 100 - home_low
    away_low = 100 - home_high
    return f"home {home_low}-{home_high}% / away {away_low}-{away_high}%"


def first_goal_side(row: pd.Series, home_xg: float, away_xg: float) -> str:
    market = norm_upper(row.get("market_primary"))
    if market in {"HOME_WIN", "HOME_DNB"}:
        return "Home more likely"
    if market in {"AWAY_WIN", "AWAY_DNB"}:
        return "Away more likely"
    if home_xg - away_xg >= 0.35:
        return "Home slight lean"
    if away_xg - home_xg >= 0.35:
        return "Away slight lean"
    return "Either side"


def state_gravity(row: pd.Series, home_xg: float, away_xg: float) -> str:
    market = norm_upper(row.get("market_primary"))
    total = home_xg + away_xg
    if market in {"OVER_2_5", "BTTS_YES"} or total >= 3.1:
        return "open exchange"
    if market == "UNDER_3_5" or total <= 2.4:
        return "controlled low-volatility state"
    if home_xg - away_xg >= 0.45:
        return "home territorial edge"
    if away_xg - home_xg >= 0.45:
        return "away territorial edge"
    return "balanced pressure"


def script_text(row: pd.Series, home_xg: float, away_xg: float) -> str:
    market = norm_upper(row.get("market_primary"))
    failure = norm_upper(row.get("pick_failure_mode"))
    total = home_xg + away_xg
    side = "home" if home_xg >= away_xg else "away"
    stats_quality = norm_upper(row.get("recent_stats_quality_flag")) or "UNKNOWN"

    if market == "OVER_2_5":
        base = "Open, active match with both penalty boxes reached often"
    elif market == "OVER_1_5":
        base = "Moderately open game where two goals can arrive through sustained chance volume"
    elif market == "UNDER_3_5":
        base = "Controlled script with enough structure to avoid a four-goal game"
    elif market in {"HOME_WIN", "HOME_DNB"}:
        base = "Home control script with territorial edge and pressure tilted toward the away box"
    elif market in {"AWAY_WIN", "AWAY_DNB"}:
        base = "Away control or transition edge with the visitor carrying the cleaner scoring route"
    elif market == "BTTS_YES":
        base = "Two-way scoring script with both teams owning a credible route to at least one goal"
    elif market == "BTTS_NO":
        base = f"One-sided scoring script where the {side} attack is more likely to control the useful chances"
    else:
        base = "Market-specific script supported by model edge, but with moderate uncertainty"

    if failure == "LOW_CONVERSION":
        return f"{base}; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: {total:.1f}; stats={stats_quality}."
    if failure == "DRAW_LIVE":
        return f"{base}; draw/live tension remains plausible if the edge does not convert early. Total-goal lean: {total:.1f}; stats={stats_quality}."
    if failure == "BTTS_BREAK":
        return f"{base}; one side failing to convert its route is the main risk. Total-goal lean: {total:.1f}; stats={stats_quality}."
    if failure == "AVALANCHE_RISK":
        return f"{base}; the breaker is an early goal that opens the match too far. Total-goal lean: {total:.1f}; stats={stats_quality}."
    return f"{base}; expected state is {state_gravity(row, home_xg, away_xg)}. Total-goal lean: {total:.1f}; stats={stats_quality}."


def pick_path(row: pd.Series, home_xg: float, away_xg: float) -> str:
    market = norm_upper(row.get("market_primary"))
    if market == "OVER_2_5":
        return "Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing."
    if market == "OVER_1_5":
        return "Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path."
    if market == "UNDER_3_5":
        return "Pick wins if game state stays structured and neither side turns the match into repeated transition attacks."
    if market == "HOME_WIN":
        return "Pick wins if home pressure converts into a lead and avoids the draw-live state."
    if market == "AWAY_WIN":
        return "Pick wins if the away attacking edge converts and the home side cannot keep the game level."
    if market == "HOME_DNB":
        return "Pick wins with a home win and pushes if the control edge stalls into a draw."
    if market == "AWAY_DNB":
        return "Pick wins with an away win and pushes if the visitor edge stalls into a draw."
    if market == "BTTS_YES":
        return "Pick wins if both attacks reach their scoring route at least once."
    if market == "BTTS_NO":
        stronger = "home" if home_xg >= away_xg else "away"
        return f"Pick wins if the {stronger} side controls scoring and the other attack stays below one goal."
    return "Pick wins if the modeled market edge appears in the match script without a major game-state shock."


def pick_breaker(row: pd.Series) -> str:
    failure = norm_upper(row.get("pick_failure_mode"))
    risk = norm_text(row.get("accuracy_primary_risk")) or norm_text(row.get("pick_primary_risk"))
    if failure == "LOW_CONVERSION":
        return "Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market."
    if failure == "DRAW_LIVE":
        return "The edge stalls into a draw script, especially if the favored side does not score first."
    if failure == "BTTS_BREAK":
        return "One attack has the route but fails to finish, breaking the both-teams scoring path."
    if failure == "AVALANCHE_RISK":
        return "An early goal or transition chain breaks the controlled script and creates too many goals."
    if failure == "THIN_MARGIN":
        return "The model edge is real but thin; one key chance or market-price miss can decide it."
    if risk:
        return f"Primary risk: {risk}."
    return "Unexpected early game-state shock or poor finishing against the modeled chance profile."


def confidence_band(row: pd.Series) -> str:
    score = safe_float(row.get("accuracy_confidence_score"), safe_float(row.get("execution_score"), 0.0))
    prob = safe_float(row.get("competition_calibrated_prob"), safe_float(row.get("primary_model_prob"), 0.0))
    quality = norm_upper(row.get("recent_stats_quality_flag"))
    if score >= 130 and prob >= 0.80 and quality == "FULL":
        return "HIGH_FORECAST_CONFIDENCE"
    if score >= 105 and prob >= 0.74:
        return "MEDIUM_HIGH_FORECAST_CONFIDENCE"
    return "MEDIUM_FORECAST_CONFIDENCE"


def inputs_used(row: pd.Series) -> str:
    inputs = ["market", "projected_goals", "competition_probability", "pick_risk"]
    if norm_upper(row.get("recent_stats_quality_flag")) not in {"", "NONE"}:
        inputs.append("recent_stats")
    if "home_recent_schedule_quality_flag" in row.index and norm_text(row.get("home_recent_schedule_quality_flag")):
        inputs.append("schedule_strength")
    if "recent_sample_cleanliness_flag" in row.index and norm_text(row.get("recent_sample_cleanliness_flag")):
        inputs.append("anomaly_cleanliness")
    if norm_upper(row.get("league_coverage_source_status")).startswith("OFFICIAL_API"):
        inputs.append("league_coverage")
    return "+".join(inputs)


def forecast_row(row: pd.Series, rank: int) -> dict[str, object]:
    home_xg, away_xg = projected_goals(row)
    home_shots = blended_stat(row, "home", "shots", fallback=home_xg * 6.2 + 4.0)
    away_shots = blended_stat(row, "away", "shots", fallback=away_xg * 6.2 + 4.0)
    home_sot = blended_stat(row, "home", "sot", fallback=home_xg * 2.4 + 0.8)
    away_sot = blended_stat(row, "away", "sot", fallback=away_xg * 2.4 + 0.8)
    home_corners = blended_stat(row, "home", "corners", fallback=home_shots * 0.35)
    away_corners = blended_stat(row, "away", "corners", fallback=away_shots * 0.35)
    main_score, alt_score = modal_score(row, home_xg, away_xg)

    return {
        "forecast_rank": rank,
        "fixture_id": row.get("fixture_id"),
        "league": row.get("league"),
        "home_team": row.get("home_team"),
        "away_team": row.get("away_team"),
        "market_primary": row.get("market_primary"),
        "predicted_match_script": script_text(row, home_xg, away_xg),
        "predicted_score_main": main_score,
        "predicted_score_alt": alt_score,
        "predicted_home_xg_range": range_text(home_xg, 0.35, 0.1, 4.5),
        "predicted_away_xg_range": range_text(away_xg, 0.35, 0.1, 4.5),
        "predicted_home_shots_range": int_range_text(home_shots, 2.0, 3, 28),
        "predicted_away_shots_range": int_range_text(away_shots, 2.0, 3, 28),
        "predicted_home_sot_range": int_range_text(home_sot, 1.0, 0, 12),
        "predicted_away_sot_range": int_range_text(away_sot, 1.0, 0, 12),
        "predicted_total_corners_range": int_range_text(home_corners + away_corners, 2.0, 3, 18),
        "predicted_possession_split": possession_split(row, home_xg, away_xg),
        "predicted_pick_path": pick_path(row, home_xg, away_xg),
        "predicted_pick_breaker": pick_breaker(row),
        "predicted_total_goals_range": range_text(home_xg + away_xg, 0.55, 0.4, 6.5),
        "predicted_first_goal_side": first_goal_side(row, home_xg, away_xg),
        "predicted_state_gravity": state_gravity(row, home_xg, away_xg),
        "forecast_confidence_band": confidence_band(row),
        "forecast_inputs_used": inputs_used(row),
    }


def sort_picks(picks: pd.DataFrame) -> pd.DataFrame:
    if picks.empty:
        return picks.copy()
    out = picks.copy()
    rank_col = "accuracy_mode_rank" if "accuracy_mode_rank" in out.columns else "execution_rank"
    if rank_col in out.columns:
        out["_rank_sort"] = pd.to_numeric(out[rank_col], errors="coerce")
        out = out.sort_values("_rank_sort", ascending=True, na_position="last").drop(columns=["_rank_sort"])
    return out.reset_index(drop=True)


def build_match_script_forecasts(picks: pd.DataFrame) -> pd.DataFrame:
    ordered = sort_picks(picks)
    if ordered.empty:
        return pd.DataFrame(columns=FORECAST_COLUMNS)
    rows = [forecast_row(row, idx + 1) for idx, (_, row) in enumerate(ordered.iterrows())]
    return pd.DataFrame(rows, columns=FORECAST_COLUMNS)


def write_forecast_report(path: Path, forecasts: pd.DataFrame, source_label: str) -> None:
    lines = [
        "vSIGMA MATCH SCRIPT + STATS FORECASTS",
        "",
        f"Source: {source_label}",
        "Role: explanation layer only; this file does not select, remove, or promote picks.",
        "Forecast style: deterministic bands and modal scripts, not exact-stat certainty.",
        "",
        f"Forecast rows: {len(forecasts)}",
        "",
    ]
    if forecasts.empty:
        lines.append("No competition picks available for forecast.")
    else:
        for _, row in forecasts.iterrows():
            lines.extend(
                [
                    f"#{row['forecast_rank']} {row['home_team']} vs {row['away_team']} | {row['league']} | {row['market_primary']}",
                    f"Script: {row['predicted_match_script']}",
                    f"Scores: main {row['predicted_score_main']} | alt {row['predicted_score_alt']}",
                    f"xG: home {row['predicted_home_xg_range']} | away {row['predicted_away_xg_range']} | total {row['predicted_total_goals_range']}",
                    f"Stats: shots {row['predicted_home_shots_range']} vs {row['predicted_away_shots_range']}; SOT {row['predicted_home_sot_range']} vs {row['predicted_away_sot_range']}; corners {row['predicted_total_corners_range']}; possession {row['predicted_possession_split']}",
                    f"Path: {row['predicted_pick_path']}",
                    f"Breaker: {row['predicted_pick_breaker']}",
                    "",
                ]
            )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def build_and_write_forecasts(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    input_filename: str = DEFAULT_INPUT,
    output_filename: str = DEFAULT_OUTPUT,
    report_filename: str = DEFAULT_REPORT,
    source_label: str = "official competition top",
    snapshot_date: str | None = None,
) -> tuple[dict[str, Path], pd.DataFrame]:
    processed_dir = Path(processed_dir)
    input_path = processed_dir / input_filename
    if not input_path.exists():
        raise FileNotFoundError(f"Missing forecast input: {input_path}")

    picks = pd.read_csv(input_path)
    forecasts = build_match_script_forecasts(picks)
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_path = processed_dir / output_filename
    report_path = processed_dir / report_filename
    forecasts.to_csv(output_path, index=False)
    write_forecast_report(report_path, forecasts, source_label)

    if snapshot_date:
        snapshot_dir = processed_dir / "today" / snapshot_date
        copy_if_exists(output_path, snapshot_dir)
        copy_if_exists(report_path, snapshot_dir)

    return {"forecast_csv": output_path, "forecast_report": report_path}, forecasts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build match-script and stats forecasts for competition picks.")
    parser.add_argument("--processed-dir", default=str(DEFAULT_PROCESSED_DIR))
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument("--source-label", default="official competition top")
    parser.add_argument("--snapshot-date", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths, forecasts = build_and_write_forecasts(
        processed_dir=Path(args.processed_dir),
        input_filename=args.input,
        output_filename=args.output,
        report_filename=args.report,
        source_label=args.source_label,
        snapshot_date=args.snapshot_date,
    )

    print("\n=== MATCH SCRIPT FORECASTS COMPLETADO ===")
    for key, path in paths.items():
        print(f"{key}: {path}")
    print(f"Forecast rows: {len(forecasts)}")
    if not forecasts.empty:
        display_cols = [
            "forecast_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "predicted_score_main",
            "predicted_score_alt",
            "predicted_total_goals_range",
            "predicted_state_gravity",
        ]
        print(forecasts[display_cols].to_string(index=False))


if __name__ == "__main__":
    main()
