from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "forecast_confidence", "forecast_warning",
    "actual_status", "actual_home_goals", "actual_away_goals", "actual_total_goals",
    "pred_home_goals_low", "pred_home_goals_mid", "pred_home_goals_high", "home_goals_hit", "home_goals_abs_error_mid",
    "pred_away_goals_low", "pred_away_goals_mid", "pred_away_goals_high", "away_goals_hit", "away_goals_abs_error_mid",
    "pred_total_goals_low", "pred_total_goals_mid", "pred_total_goals_high", "total_goals_hit", "total_goals_abs_error_mid",
    "actual_home_sot", "actual_away_sot", "actual_total_sot",
    "pred_total_sot_low", "pred_total_sot_mid", "pred_total_sot_high", "total_sot_hit", "total_sot_abs_error_mid",
    "actual_home_corners", "actual_away_corners", "actual_total_corners", "total_corners_hit", "total_corners_abs_error_mid",
    "actual_home_cards", "actual_away_cards", "actual_total_cards", "total_cards_hit", "total_cards_abs_error_mid",
    "actual_home_fouls", "actual_away_fouls", "actual_total_fouls", "total_fouls_hit", "total_fouls_abs_error_mid",
    "available_actual_metrics", "range_hits", "range_misses", "forecast_grade", "calibration_note",
    "source_guard", "auto_apply", "production_change",
]
FINAL_STATUS = {"FT", "AET", "PEN"}


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def num(v: object, default: float | None = None) -> float | None:
    text = norm(v)
    if not text or text.lower() == "nan":
        return default
    try:
        return float(text)
    except ValueError:
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
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def dated_path(processed: Path, target_date: str, filename: str) -> Path:
    return processed / "today" / target_date / filename


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day_rows(rows: list[dict[str, str]], target_date: str) -> list[dict[str, str]]:
    return [r for r in rows if row_day(r) in {"", target_date}]


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = norm(row.get("fixture_id")).replace(".0", "")
        if fid and fid not in out:
            out[fid] = row
    return out


def first_num(row: dict[str, str], names: list[str]) -> float | None:
    for name in names:
        if name in row:
            value = num(row.get(name), None)
            if value is not None:
                return value
    return None


def hit(actual: float | None, low: object, high: object) -> str:
    if actual is None:
        return "ACTUAL_UNAVAILABLE"
    lo = num(low, None)
    hi = num(high, None)
    if lo is None or hi is None:
        return "PRED_UNAVAILABLE"
    return "HIT" if lo <= actual <= hi else "MISS"


def err(actual: float | None, mid: object) -> str:
    if actual is None:
        return ""
    m = num(mid, None)
    if m is None:
        return ""
    return f"{abs(actual - m):.2f}"


def val(actual: float | None) -> str:
    if actual is None:
        return ""
    if abs(actual - round(actual)) < 1e-9:
        return str(int(round(actual)))
    return f"{actual:.2f}"


def actual_status(match: dict[str, str]) -> str:
    short = up(match.get("fixture_status_short") or match.get("status"))
    long = up(match.get("fixture_status_long"))
    if short:
        return short
    if "MATCH FINISHED" in long:
        return "FT"
    return "UNKNOWN"


def is_final(match: dict[str, str]) -> bool:
    short = actual_status(match)
    long = up(match.get("fixture_status_long"))
    return short in FINAL_STATUS or "MATCH FINISHED" in long


def actual_goals(match: dict[str, str]) -> tuple[float | None, float | None]:
    home = first_num(match, ["goals_home", "score_fulltime_home", "home_goals", "actual_home_goals"])
    away = first_num(match, ["goals_away", "score_fulltime_away", "away_goals", "actual_away_goals"])
    return home, away


def actual_pair(match: dict[str, str], home_names: list[str], away_names: list[str]) -> tuple[float | None, float | None]:
    return first_num(match, home_names), first_num(match, away_names)


def combine(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return a + b


def forecast_grade(hits: int, misses: int, available: int) -> str:
    if available == 0:
        return "NO_ACTUALS_YET"
    if misses == 0 and hits >= 3:
        return "A_RANGE_STRONG"
    if hits >= misses + 2:
        return "B_RANGE_GOOD"
    if hits >= misses:
        return "C_RANGE_MIXED"
    return "D_RANGE_WEAK"


def unavailable_row(forecast: dict[str, str], match: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "fixture_id": norm(forecast.get("fixture_id")),
        "home_team": norm(forecast.get("home_team")),
        "away_team": norm(forecast.get("away_team")),
        "forecast_confidence": norm(forecast.get("forecast_confidence")),
        "forecast_warning": norm(forecast.get("forecast_warning")),
        "actual_status": actual_status(match),
        "actual_home_goals": "",
        "actual_away_goals": "",
        "actual_total_goals": "",
        "pred_home_goals_low": forecast.get("home_goals_low", ""),
        "pred_home_goals_mid": forecast.get("home_goals_mid", ""),
        "pred_home_goals_high": forecast.get("home_goals_high", ""),
        "home_goals_hit": "ACTUAL_UNAVAILABLE",
        "home_goals_abs_error_mid": "",
        "pred_away_goals_low": forecast.get("away_goals_low", ""),
        "pred_away_goals_mid": forecast.get("away_goals_mid", ""),
        "pred_away_goals_high": forecast.get("away_goals_high", ""),
        "away_goals_hit": "ACTUAL_UNAVAILABLE",
        "away_goals_abs_error_mid": "",
        "pred_total_goals_low": forecast.get("total_goals_low", ""),
        "pred_total_goals_mid": forecast.get("total_goals_mid", ""),
        "pred_total_goals_high": forecast.get("total_goals_high", ""),
        "total_goals_hit": "ACTUAL_UNAVAILABLE",
        "total_goals_abs_error_mid": "",
        "actual_home_sot": "",
        "actual_away_sot": "",
        "actual_total_sot": "",
        "pred_total_sot_low": forecast.get("total_sot_low", ""),
        "pred_total_sot_mid": forecast.get("total_sot_mid", ""),
        "pred_total_sot_high": forecast.get("total_sot_high", ""),
        "total_sot_hit": "ACTUAL_UNAVAILABLE",
        "total_sot_abs_error_mid": "",
        "actual_home_corners": "",
        "actual_away_corners": "",
        "actual_total_corners": "",
        "total_corners_hit": "ACTUAL_UNAVAILABLE",
        "total_corners_abs_error_mid": "",
        "actual_home_cards": "",
        "actual_away_cards": "",
        "actual_total_cards": "",
        "total_cards_hit": "ACTUAL_UNAVAILABLE",
        "total_cards_abs_error_mid": "",
        "actual_home_fouls": "",
        "actual_away_fouls": "",
        "actual_total_fouls": "",
        "total_fouls_hit": "ACTUAL_UNAVAILABLE",
        "total_fouls_abs_error_mid": "",
        "available_actual_metrics": "none",
        "range_hits": 0,
        "range_misses": 0,
        "forecast_grade": "NO_ACTUALS_YET",
        "calibration_note": "v45.1 refuses to grade non-final fixtures; wait for FT/AET/PEN and post-match stat enrichment.",
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build_row(forecast: dict[str, str], match: dict[str, str], target_date: str, generated_at: str) -> dict[str, object]:
    if not is_final(match):
        return unavailable_row(forecast, match, target_date, generated_at)

    hg, ag = actual_goals(match)
    tg = combine(hg, ag)

    h_sot, a_sot = actual_pair(match, ["actual_home_sot", "home_sot", "home_sot_for"], ["actual_away_sot", "away_sot", "away_sot_for"])
    h_cor, a_cor = actual_pair(match, ["actual_home_corners", "home_corners", "home_corners_for"], ["actual_away_corners", "away_corners", "away_corners_for"])
    h_cards, a_cards = actual_pair(match, ["actual_home_cards", "home_cards", "home_yellow_cards"], ["actual_away_cards", "away_cards", "away_yellow_cards"])
    h_fouls, a_fouls = actual_pair(match, ["actual_home_fouls", "home_fouls"], ["actual_away_fouls", "away_fouls"])

    t_sot = combine(h_sot, a_sot)
    t_cor = combine(h_cor, a_cor)
    t_cards = combine(h_cards, a_cards)
    t_fouls = combine(h_fouls, a_fouls)

    # API-Football snapshots can contain placeholder 0.0 statistic fields before real post-match stats are loaded.
    # For final matches with goals but 0-0 SoT, treat SoT as unavailable rather than as a certain zero sample.
    if t_sot == 0 and (tg or 0) > 0:
        h_sot, a_sot, t_sot = None, None, None

    checks = {
        "home_goals": hit(hg, forecast.get("home_goals_low"), forecast.get("home_goals_high")),
        "away_goals": hit(ag, forecast.get("away_goals_low"), forecast.get("away_goals_high")),
        "total_goals": hit(tg, forecast.get("total_goals_low"), forecast.get("total_goals_high")),
        "total_sot": hit(t_sot, forecast.get("total_sot_low"), forecast.get("total_sot_high")),
        "total_corners": hit(t_cor, forecast.get("total_corners_low"), forecast.get("total_corners_high")),
        "total_cards": hit(t_cards, forecast.get("total_cards_low"), forecast.get("total_cards_high")),
        "total_fouls": hit(t_fouls, forecast.get("total_fouls_low"), forecast.get("total_fouls_high")),
    }
    available = [k for k, v in checks.items() if v in {"HIT", "MISS"}]
    hits = sum(1 for v in checks.values() if v == "HIT")
    misses = sum(1 for v in checks.values() if v == "MISS")

    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "fixture_id": norm(forecast.get("fixture_id")),
        "home_team": norm(forecast.get("home_team")),
        "away_team": norm(forecast.get("away_team")),
        "forecast_confidence": norm(forecast.get("forecast_confidence")),
        "forecast_warning": norm(forecast.get("forecast_warning")),
        "actual_status": actual_status(match),
        "actual_home_goals": val(hg),
        "actual_away_goals": val(ag),
        "actual_total_goals": val(tg),
        "pred_home_goals_low": forecast.get("home_goals_low", ""),
        "pred_home_goals_mid": forecast.get("home_goals_mid", ""),
        "pred_home_goals_high": forecast.get("home_goals_high", ""),
        "home_goals_hit": checks["home_goals"],
        "home_goals_abs_error_mid": err(hg, forecast.get("home_goals_mid")),
        "pred_away_goals_low": forecast.get("away_goals_low", ""),
        "pred_away_goals_mid": forecast.get("away_goals_mid", ""),
        "pred_away_goals_high": forecast.get("away_goals_high", ""),
        "away_goals_hit": checks["away_goals"],
        "away_goals_abs_error_mid": err(ag, forecast.get("away_goals_mid")),
        "pred_total_goals_low": forecast.get("total_goals_low", ""),
        "pred_total_goals_mid": forecast.get("total_goals_mid", ""),
        "pred_total_goals_high": forecast.get("total_goals_high", ""),
        "total_goals_hit": checks["total_goals"],
        "total_goals_abs_error_mid": err(tg, forecast.get("total_goals_mid")),
        "actual_home_sot": val(h_sot),
        "actual_away_sot": val(a_sot),
        "actual_total_sot": val(t_sot),
        "pred_total_sot_low": forecast.get("total_sot_low", ""),
        "pred_total_sot_mid": forecast.get("total_sot_mid", ""),
        "pred_total_sot_high": forecast.get("total_sot_high", ""),
        "total_sot_hit": checks["total_sot"],
        "total_sot_abs_error_mid": err(t_sot, forecast.get("total_sot_mid")),
        "actual_home_corners": val(h_cor),
        "actual_away_corners": val(a_cor),
        "actual_total_corners": val(t_cor),
        "total_corners_hit": checks["total_corners"],
        "total_corners_abs_error_mid": err(t_cor, forecast.get("total_corners_mid")),
        "actual_home_cards": val(h_cards),
        "actual_away_cards": val(a_cards),
        "actual_total_cards": val(t_cards),
        "total_cards_hit": checks["total_cards"],
        "total_cards_abs_error_mid": err(t_cards, forecast.get("total_cards_mid")),
        "actual_home_fouls": val(h_fouls),
        "actual_away_fouls": val(a_fouls),
        "actual_total_fouls": val(t_fouls),
        "total_fouls_hit": checks["total_fouls"],
        "total_fouls_abs_error_mid": err(t_fouls, forecast.get("total_fouls_mid")),
        "available_actual_metrics": "; ".join(available) if available else "none",
        "range_hits": hits,
        "range_misses": misses,
        "forecast_grade": forecast_grade(hits, misses, len(available)),
        "calibration_note": "v45.1 grades only final fixtures and only metrics with actual data available; corners/cards/fouls require post-match stat enrichment.",
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    forecasts_path = dated_path(processed, target_date, "vsigma_match_stat_forecasts.csv")
    matches_path = dated_path(processed, target_date, "matches.csv")
    forecasts = same_day_rows(read_rows(forecasts_path), target_date)
    matches = index_by_fixture(same_day_rows(read_rows(matches_path), target_date))
    out: list[dict[str, object]] = []
    for f in forecasts:
        fid = norm(f.get("fixture_id")).replace(".0", "")
        match = matches.get(fid)
        if not match:
            continue
        out.append(build_row(f, match, target_date, generated_at))
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Match Statistical Forecast Backtest - {target_date}",
        "",
        "## Summary",
        f"- rows_checked: {len(rows)}",
        f"- forecast_grade_counts: {counts(rows, 'forecast_grade')}",
        f"- total_goals_hit_counts: {counts(rows, 'total_goals_hit')}",
        f"- total_sot_hit_counts: {counts(rows, 'total_sot_hit')}",
        "- calibration_note: v45.1 refuses to grade non-final fixtures.",
        "- source_guard: DATED_INPUT_ONLY",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Backtest Rows",
    ]
    if not rows:
        lines.append("- none. Need dated forecasts and dated post-match results first.")
    for r in rows:
        lines.append(
            f"- {r['home_team']} vs {r['away_team']} | status={r['actual_status']} | "
            f"goals_actual={r['actual_total_goals'] or 'NA'} vs pred={r['pred_total_goals_low']}-{r['pred_total_goals_high']} ({r['total_goals_hit']}) | "
            f"SoT_actual={r['actual_total_sot'] or 'NA'} vs pred={r['pred_total_sot_low']}-{r['pred_total_sot_high']} ({r['total_sot_hit']}) | "
            f"grade={r['forecast_grade']} | metrics={r['available_actual_metrics']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This report grades only final fixtures: FT/AET/PEN.",
        "- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.",
        "- Use this to calibrate v44 forecasts before connecting them to market execution.",
    ]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_match_stat_forecast_backtest.csv", rows)
        (base / "vsigma_match_stat_forecast_backtest.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA MATCH STAT FORECAST BACKTEST ===")
    print(f"rows_checked={len(rows)}")
    print(f"forecast_grade_counts={counts(rows, 'forecast_grade')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
