from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import mean
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
SOURCE_CANDIDATES = [
    "matches_vsigma_scored_v3.csv",
    "vsigma_today_execution_shortlist.csv",
    "vsigma_today_execution_bets_only.csv",
]
FIELDS = [
    "target_date", "generated_at", "forecast_rank", "fixture_id", "country", "league", "home_team", "away_team",
    "source_file", "market_hint", "modal_scoreline", "scenario_map",
    "home_goals_low", "home_goals_mid", "home_goals_high",
    "away_goals_low", "away_goals_mid", "away_goals_high",
    "total_goals_low", "total_goals_mid", "total_goals_high",
    "home_shots_low", "home_shots_mid", "home_shots_high",
    "away_shots_low", "away_shots_mid", "away_shots_high",
    "total_shots_low", "total_shots_mid", "total_shots_high",
    "home_sot_low", "home_sot_mid", "home_sot_high",
    "away_sot_low", "away_sot_mid", "away_sot_high",
    "total_sot_low", "total_sot_mid", "total_sot_high",
    "home_corners_low", "home_corners_mid", "home_corners_high",
    "away_corners_low", "away_corners_mid", "away_corners_high",
    "total_corners_low", "total_corners_mid", "total_corners_high",
    "home_cards_low", "home_cards_mid", "home_cards_high",
    "away_cards_low", "away_cards_mid", "away_cards_high",
    "total_cards_low", "total_cards_mid", "total_cards_high",
    "home_fouls_low", "home_fouls_mid", "home_fouls_high",
    "away_fouls_low", "away_fouls_mid", "away_fouls_high",
    "total_fouls_low", "total_fouls_mid", "total_fouls_high",
    "tempo_projection", "shot_volume_level", "corner_volume_level", "card_risk_level", "both_teams_threat_level",
    "forecast_confidence", "forecast_confidence_score", "forecast_warning",
    "source_guard", "auto_apply", "production_change",
]


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def num(v: object, default: float = 0.0) -> float:
    try:
        text = norm(v)
        if not text or text.lower() == "nan":
            return default
        value = float(text)
        if math.isnan(value):
            return default
        return value
    except (TypeError, ValueError):
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in FIELDS})


def dated_source(processed: Path, target_date: str) -> tuple[Path | None, str]:
    base = processed / "today" / target_date
    for name in SOURCE_CANDIDATES:
        p = base / name
        if p.exists():
            return p, name
    return None, "NONE"


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day_rows(data: list[dict[str, str]], target_date: str) -> list[dict[str, str]]:
    return [r for r in data if row_day(r) in {"", target_date}]


def avg(values: list[float], default: float) -> float:
    clean = [v for v in values if v > 0]
    return mean(clean) if clean else default


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def f2(value: float) -> str:
    return f"{value:.2f}"


def confidence_width(confidence: float) -> float:
    # Wider ranges when confidence is low; tighter ranges only when data quality is genuinely strong.
    if confidence >= 78:
        return 0.86
    if confidence >= 66:
        return 1.00
    if confidence >= 56:
        return 1.12
    return 1.25


def range_float(mid: float, pct: float = 0.22, add: float = 0.10, upper: float = 9.5, width: float = 1.0) -> tuple[str, str, str]:
    pct *= width
    add *= width
    low = clamp(mid * (1 - pct) - add, 0, upper)
    high = clamp(mid * (1 + pct) + add, 0, upper)
    return f2(low), f2(clamp(mid, 0, upper)), f2(max(high, low))


def range_int(mid: float, pct: float = 0.18, add: float = 0.55, upper: int = 80, width: float = 1.0) -> tuple[int, int, int]:
    pct *= width
    add *= width
    low = int(max(0, math.floor(mid * (1 - pct) - add)))
    high = int(min(upper, math.ceil(mid * (1 + pct) + add)))
    mid_i = int(max(0, round(mid)))
    return low, mid_i, max(high, low)


def goal_bucket(mid: float) -> int:
    if mid < 0.55:
        return 0
    if mid < 1.45:
        return 1
    if mid < 2.35:
        return 2
    if mid < 3.25:
        return 3
    return 4


def level(value: float, low: float, high: float, low_label: str, mid_label: str, high_label: str) -> str:
    if value >= high:
        return high_label
    if value <= low:
        return low_label
    return mid_label


def league_profiles(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    buckets: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        league = norm(r.get("league")) or "UNKNOWN"
        home_goals = num(r.get("projected_home_goals"), 0) or avg([
            num(r.get("home_goals_for_pg"), 0), num(r.get("away_goals_against_pg"), 0)
        ], 1.25)
        away_goals = num(r.get("projected_away_goals"), 0) or avg([
            num(r.get("away_goals_for_pg"), 0), num(r.get("home_goals_against_pg"), 0)
        ], 1.10)
        buckets[league]["home_goals"].append(home_goals)
        buckets[league]["away_goals"].append(away_goals)
        buckets[league]["total_shots"].append(avg([
            num(r.get("home_recent_shots_for_pg"), 0) + num(r.get("away_recent_shots_for_pg"), 0),
            num(r.get("home_recent_shots_against_pg"), 0) + num(r.get("away_recent_shots_against_pg"), 0),
        ], 23.0))
        corners_total = num(r.get("home_recent_corners_for_pg"), 0) + num(r.get("away_recent_corners_for_pg"), 0)
        if corners_total > 0:
            buckets[league]["total_corners"].append(corners_total)
        cards_total = num(r.get("home_recent_yellow_pg"), 0) + num(r.get("away_recent_yellow_pg"), 0)
        if cards_total > 0:
            buckets[league]["total_cards"].append(cards_total)
    profiles: dict[str, dict[str, float]] = {}
    for league, vals in buckets.items():
        profiles[league] = {
            "home_goals": avg(vals["home_goals"], 1.25),
            "away_goals": avg(vals["away_goals"], 1.10),
            "total_shots": avg(vals["total_shots"], 23.0),
            "total_corners": avg(vals["total_corners"], 9.2),
            "total_cards": avg(vals["total_cards"], 3.8),
        }
    return profiles


def market_hint(row: dict[str, str]) -> str:
    for field in ("market_primary", "odds_market_translation_hint", "market_family_hint", "vsigma_priority"):
        value = up(row.get(field))
        if value:
            return value
    return "UNKNOWN"


def has_real_pair(row: dict[str, str], a: str, b: str) -> bool:
    return num(row.get(a), 0) > 0 and num(row.get(b), 0) > 0


def forecast_row(row: dict[str, str], target_date: str, generated_at: str, rank: int, source_name: str, profiles: dict[str, dict[str, float]]) -> dict[str, object]:
    league = norm(row.get("league")) or "UNKNOWN"
    prof = profiles.get(league, {})

    form_home_goals = avg([num(row.get("home_goals_for_pg"), 0), num(row.get("away_goals_against_pg"), 0)], prof.get("home_goals", 1.25))
    form_away_goals = avg([num(row.get("away_goals_for_pg"), 0), num(row.get("home_goals_against_pg"), 0)], prof.get("away_goals", 1.10))
    proj_home = num(row.get("projected_home_goals"), 0)
    proj_away = num(row.get("projected_away_goals"), 0)
    home_goals_mid = 0.58 * proj_home + 0.42 * form_home_goals if proj_home > 0 else form_home_goals
    away_goals_mid = 0.58 * proj_away + 0.42 * form_away_goals if proj_away > 0 else form_away_goals

    over25 = num(row.get("odds_imp_over25"), 0)
    over15 = num(row.get("odds_imp_over15"), 0)
    under35 = num(row.get("odds_imp_under35"), 0)
    goal_nudge = 0.0
    if over25 >= 0.58:
        goal_nudge += 0.12
    elif over25 >= 0.52:
        goal_nudge += 0.05
    elif 0 < over25 <= 0.42:
        goal_nudge -= 0.10
    if over15 >= 0.82:
        goal_nudge += 0.03
    if under35 >= 0.72:
        goal_nudge -= 0.06

    total_before = max(home_goals_mid + away_goals_mid, 0.1)
    home_share = home_goals_mid / total_before
    home_goals_mid = clamp(home_goals_mid + goal_nudge * home_share, 0.05, 4.5)
    away_goals_mid = clamp(away_goals_mid + goal_nudge * (1 - home_share), 0.05, 4.5)
    total_goals_mid = home_goals_mid + away_goals_mid

    home_shots_mid = avg([
        num(row.get("home_recent_shots_for_pg"), 0),
        num(row.get("away_recent_shots_against_pg"), 0),
    ], prof.get("total_shots", 23.0) * 0.52)
    away_shots_mid = avg([
        num(row.get("away_recent_shots_for_pg"), 0),
        num(row.get("home_recent_shots_against_pg"), 0),
    ], prof.get("total_shots", 23.0) * 0.48)
    home_shots_mid *= clamp(0.90 + home_goals_mid / 11.0, 0.86, 1.14)
    away_shots_mid *= clamp(0.90 + away_goals_mid / 11.0, 0.86, 1.14)

    home_sot_mid = avg([
        num(row.get("home_recent_sot_for_pg"), 0),
        num(row.get("away_recent_sot_against_pg"), 0),
    ], home_shots_mid * 0.33)
    away_sot_mid = avg([
        num(row.get("away_recent_sot_for_pg"), 0),
        num(row.get("home_recent_sot_against_pg"), 0),
    ], away_shots_mid * 0.33)
    home_sot_mid = clamp(home_sot_mid, home_shots_mid * 0.18, home_shots_mid * 0.55)
    away_sot_mid = clamp(away_sot_mid, away_shots_mid * 0.18, away_shots_mid * 0.55)

    home_corners_mid = avg([
        num(row.get("home_recent_corners_for_pg"), 0),
        num(row.get("away_recent_corners_against_pg"), 0),
    ], prof.get("total_corners", 9.2) * 0.52)
    away_corners_mid = avg([
        num(row.get("away_recent_corners_for_pg"), 0),
        num(row.get("home_recent_corners_against_pg"), 0),
    ], prof.get("total_corners", 9.2) * 0.48)
    shot_corner_nudge = clamp(((home_shots_mid + away_shots_mid) - 23.0) / 42.0, -0.10, 0.14)
    home_corners_mid *= 1 + shot_corner_nudge
    away_corners_mid *= 1 + shot_corner_nudge

    home_fouls_mid = avg([num(row.get("home_recent_fouls_pg"), 0)], 12.0)
    away_fouls_mid = avg([num(row.get("away_recent_fouls_pg"), 0)], 12.0)
    home_cards_mid = avg([num(row.get("home_recent_yellow_pg"), 0)], prof.get("total_cards", 3.8) * 0.50)
    away_cards_mid = avg([num(row.get("away_recent_yellow_pg"), 0)], prof.get("total_cards", 3.8) * 0.50)
    urgency_total = num(row.get("home_urgency_score"), 0) + num(row.get("away_urgency_score"), 0)
    if urgency_total >= 4:
        home_cards_mid += 0.10
        away_cards_mid += 0.10
    if home_fouls_mid + away_fouls_mid >= 28:
        home_cards_mid += 0.08
        away_cards_mid += 0.08

    total_shots_mid = home_shots_mid + away_shots_mid
    total_sot_mid = home_sot_mid + away_sot_mid
    total_corners_mid = home_corners_mid + away_corners_mid
    total_cards_mid = home_cards_mid + away_cards_mid
    total_fouls_mid = home_fouls_mid + away_fouls_mid

    modal_home = goal_bucket(home_goals_mid)
    modal_away = goal_bucket(away_goals_mid)
    modal = f"{modal_home}-{modal_away} / {max(0, modal_home - 1)}-{modal_away} / {modal_home}-{modal_away + 1}"

    tempo = level(total_shots_mid + total_corners_mid * 1.0 + total_goals_mid * 2.8, 34, 48, "LOW_TEMPO", "MEDIUM_TEMPO", "HIGH_TEMPO")
    shot_level = level(total_shots_mid, 21, 29, "LOW_SHOT_VOLUME", "MEDIUM_SHOT_VOLUME", "HIGH_SHOT_VOLUME")
    corner_level = level(total_corners_mid, 8.0, 11.0, "LOW_CORNER_VOLUME", "MEDIUM_CORNER_VOLUME", "HIGH_CORNER_VOLUME")
    card_level = level(total_cards_mid, 3.0, 5.0, "LOW_CARD_RISK", "MEDIUM_CARD_RISK", "HIGH_CARD_RISK")
    btts_threat = level(min(home_sot_mid, away_sot_mid), 2.7, 4.1, "ONE_SIDE_THREAT", "BALANCED_THREAT", "BOTH_TEAMS_THREAT")

    warnings: list[str] = []
    if "LOW_CONVERSION" in up(row.get("pick_failure_mode")):
        warnings.append("LOW_CONVERSION")
    if up(row.get("lineup_activation_state")) == "INACTIVE":
        warnings.append("LINEUPS_INACTIVE")
    if num(row.get("availability_known_risk_score"), 0) >= 15 or num(row.get("home_absence_risk_score"), 0) >= 10 or num(row.get("away_absence_risk_score"), 0) >= 10:
        warnings.append("AVAILABILITY_RISK")
    if num(row.get("league_data_reliability_score"), 0.6) < 0.70:
        warnings.append("LOW_LEAGUE_RELIABILITY")
    if up(row.get("recent_stats_quality_flag")) not in {"FULL", ""}:
        warnings.append("PARTIAL_RECENT_STATS")
    if not has_real_pair(row, "home_recent_shots_for_pg", "away_recent_shots_for_pg"):
        warnings.append("SHOT_SAMPLE_WEAK")
    if not has_real_pair(row, "home_recent_corners_for_pg", "away_recent_corners_for_pg"):
        warnings.append("CORNER_SAMPLE_WEAK")
    if not has_real_pair(row, "home_recent_yellow_pg", "away_recent_yellow_pg"):
        warnings.append("CARD_SAMPLE_WEAK")

    confidence = 49.0
    confidence += 18.0 * clamp(num(row.get("league_data_reliability_score"), 0.6), 0.0, 1.0)
    confidence += 5.0 if up(row.get("recent_stats_quality_flag")) == "FULL" else 0.0
    confidence += 4.0 if num(row.get("odds_bookmaker_support_count"), 0) >= 4 else 0.0
    confidence += 4.0 if up(row.get("lineup_quality_flag")) in {"FULL", "LINEUPS_CONFIRMED"} else 0.0
    confidence += 3.0 if has_real_pair(row, "home_recent_shots_for_pg", "away_recent_shots_for_pg") else -3.0
    confidence += 2.0 if has_real_pair(row, "home_recent_corners_for_pg", "away_recent_corners_for_pg") else -2.0
    confidence += 1.5 if has_real_pair(row, "home_recent_yellow_pg", "away_recent_yellow_pg") else -1.5
    confidence -= 6.0 if "LINEUPS_INACTIVE" in warnings else 0.0
    confidence -= 5.0 if "AVAILABILITY_RISK" in warnings else 0.0
    confidence -= 4.0 if "PARTIAL_RECENT_STATS" in warnings else 0.0
    confidence = clamp(confidence, 30.0, 92.0)
    confidence_label = "HIGH" if confidence >= 77 else "MEDIUM" if confidence >= 61 else "LOW"
    width = confidence_width(confidence)

    hg_l, hg_m, hg_h = range_float(home_goals_mid, pct=0.26, add=0.09, upper=5.0, width=width)
    ag_l, ag_m, ag_h = range_float(away_goals_mid, pct=0.26, add=0.09, upper=5.0, width=width)
    tg_l, tg_m, tg_h = range_float(total_goals_mid, pct=0.21, add=0.12, upper=8.0, width=width)
    hs_l, hs_m, hs_h = range_int(home_shots_mid, pct=0.20, add=0.5, upper=45, width=width)
    a_sh_l, a_sh_m, a_sh_h = range_int(away_shots_mid, pct=0.20, add=0.5, upper=45, width=width)
    ts_l, ts_m, ts_h = range_int(total_shots_mid, pct=0.16, add=0.8, upper=80, width=width)
    hso_l, hso_m, hso_h = range_int(home_sot_mid, pct=0.24, add=0.35, upper=20, width=width)
    aso_l, aso_m, aso_h = range_int(away_sot_mid, pct=0.24, add=0.35, upper=20, width=width)
    tso_l, tso_m, tso_h = range_int(total_sot_mid, pct=0.20, add=0.5, upper=35, width=width)
    hc_l, hc_m, hc_h = range_int(home_corners_mid, pct=0.22, add=0.35, upper=20, width=width)
    ac_l, ac_m, ac_h = range_int(away_corners_mid, pct=0.22, add=0.35, upper=20, width=width)
    tc_l, tc_m, tc_h = range_int(total_corners_mid, pct=0.18, add=0.55, upper=32, width=width)
    hca_l, hca_m, hca_h = range_int(home_cards_mid, pct=0.28, add=0.28, upper=10, width=width)
    aca_l, aca_m, aca_h = range_int(away_cards_mid, pct=0.28, add=0.28, upper=10, width=width)
    tca_l, tca_m, tca_h = range_int(total_cards_mid, pct=0.23, add=0.45, upper=14, width=width)
    hf_l, hf_m, hf_h = range_int(home_fouls_mid, pct=0.17, add=0.8, upper=35, width=width)
    af_l, af_m, af_h = range_int(away_fouls_mid, pct=0.17, add=0.8, upper=35, width=width)
    tf_l, tf_m, tf_h = range_int(total_fouls_mid, pct=0.14, add=1.2, upper=70, width=width)

    scenarios = []
    if tempo == "HIGH_TEMPO":
        scenarios.append("open tempo")
    if btts_threat == "BOTH_TEAMS_THREAT":
        scenarios.append("both teams carry threat")
    if corner_level == "HIGH_CORNER_VOLUME":
        scenarios.append("wide/corner pressure")
    if card_level == "HIGH_CARD_RISK":
        scenarios.append("discipline risk")
    if not scenarios:
        scenarios.append("standard state")

    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "forecast_rank": rank,
        "fixture_id": norm(row.get("fixture_id")),
        "country": norm(row.get("country")),
        "league": league,
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "source_file": source_name,
        "market_hint": market_hint(row),
        "modal_scoreline": modal,
        "scenario_map": "; ".join(scenarios),
        "home_goals_low": hg_l, "home_goals_mid": hg_m, "home_goals_high": hg_h,
        "away_goals_low": ag_l, "away_goals_mid": ag_m, "away_goals_high": ag_h,
        "total_goals_low": tg_l, "total_goals_mid": tg_m, "total_goals_high": tg_h,
        "home_shots_low": hs_l, "home_shots_mid": hs_m, "home_shots_high": hs_h,
        "away_shots_low": a_sh_l, "away_shots_mid": a_sh_m, "away_shots_high": a_sh_h,
        "total_shots_low": ts_l, "total_shots_mid": ts_m, "total_shots_high": ts_h,
        "home_sot_low": hso_l, "home_sot_mid": hso_m, "home_sot_high": hso_h,
        "away_sot_low": aso_l, "away_sot_mid": aso_m, "away_sot_high": aso_h,
        "total_sot_low": tso_l, "total_sot_mid": tso_m, "total_sot_high": tso_h,
        "home_corners_low": hc_l, "home_corners_mid": hc_m, "home_corners_high": hc_h,
        "away_corners_low": ac_l, "away_corners_mid": ac_m, "away_corners_high": ac_h,
        "total_corners_low": tc_l, "total_corners_mid": tc_m, "total_corners_high": tc_h,
        "home_cards_low": hca_l, "home_cards_mid": hca_m, "home_cards_high": hca_h,
        "away_cards_low": aca_l, "away_cards_mid": aca_m, "away_cards_high": aca_h,
        "total_cards_low": tca_l, "total_cards_mid": tca_m, "total_cards_high": tca_h,
        "home_fouls_low": hf_l, "home_fouls_mid": hf_m, "home_fouls_high": hf_h,
        "away_fouls_low": af_l, "away_fouls_mid": af_m, "away_fouls_high": af_h,
        "total_fouls_low": tf_l, "total_fouls_mid": tf_m, "total_fouls_high": tf_h,
        "tempo_projection": tempo,
        "shot_volume_level": shot_level,
        "corner_volume_level": corner_level,
        "card_risk_level": card_level,
        "both_teams_threat_level": btts_threat,
        "forecast_confidence": confidence_label,
        "forecast_confidence_score": f"{confidence:.1f}",
        "forecast_warning": "; ".join(warnings) if warnings else "none",
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(target_date: str, timezone: str, processed: Path) -> tuple[list[dict[str, object]], str]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    source, source_name = dated_source(processed, target_date)
    if source is None:
        return [], "NONE"
    raw = same_day_rows(read_rows(source), target_date)
    profiles = league_profiles(raw)
    rows = [forecast_row(r, target_date, generated_at, i, source_name, profiles) for i, r in enumerate(raw, start=1)]
    rows.sort(key=lambda r: (-float(r["forecast_confidence_score"]), -float(r["total_goals_mid"]), int(r["forecast_rank"])))
    for i, r in enumerate(rows, start=1):
        r["forecast_rank"] = i
    return rows, source_name


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]], source_name: str) -> str:
    lines = [
        f"# vSIGMA Match Statistical Forecasts - {target_date}",
        "",
        "## Summary",
        f"- rows_forecasted: {len(rows)}",
        f"- source_file: {source_name}",
        "- source_guard: DATED_INPUT_ONLY",
        f"- confidence_counts: {counts(rows, 'forecast_confidence')}",
        f"- tempo_counts: {counts(rows, 'tempo_projection')}",
        "- calibration_note: v44.1 tightened range width and confidence penalties; no auto-execution.",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Forecast Rows",
    ]
    if not rows:
        lines.append("- none. Missing dated scored/shortlist source; root fallback refused.")
    for r in rows:
        lines.append(
            f"- #{r['forecast_rank']} | {r['home_team']} vs {r['away_team']} | score={r['modal_scoreline']} | "
            f"goals={r['total_goals_low']}-{r['total_goals_high']} | shots={r['total_shots_low']}-{r['total_shots_high']} | "
            f"SoT={r['total_sot_low']}-{r['total_sot_high']} | corners={r['total_corners_low']}-{r['total_corners_high']} | "
            f"cards={r['total_cards_low']}-{r['total_cards_high']} | tempo={r['tempo_projection']} | conf={r['forecast_confidence']}({r['forecast_confidence_score']}) | warning={r['forecast_warning']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Forecasts are ranges, not exact-stat promises.",
        "- This report refuses root-level or governance fallback sources.",
        "- Use these forecasts as an input to market selection, not as automatic execution permission.",
    ]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows, source_name = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_match_stat_forecasts.csv", rows)
        (base / "vsigma_match_stat_forecasts.md").write_text(md(target_date, rows, source_name), encoding="utf-8")
    print("=== VSIGMA MATCH STATISTICAL FORECASTS ===")
    print(f"rows_forecasted={len(rows)}")
    print(f"source_file={source_name}")
    print(f"confidence_counts={counts(rows, 'forecast_confidence')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
