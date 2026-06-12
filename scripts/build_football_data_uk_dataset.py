from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

import pandas as pd

BASE = Path("data/modeling")
BASE_URL = "https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"

LEAGUES = {
    "E0": {"league_id": 39, "league_name": "Premier League", "country": "England"},
    "SP1": {"league_id": 140, "league_name": "La Liga", "country": "Spain"},
    "I1": {"league_id": 135, "league_name": "Serie A", "country": "Italy"},
    "D1": {"league_id": 78, "league_name": "Bundesliga", "country": "Germany"},
    "F1": {"league_id": 61, "league_name": "Ligue 1", "country": "France"},
}

DEFAULT_LEAGUES = list(LEAGUES.keys())
DEFAULT_SEASONS = ["2021", "2122", "2223", "2324", "2425"]
RESULT_MAP = {"H": "HOME", "D": "DRAW", "A": "AWAY"}


def fnum(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def fint(value: object, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def odds_triplet(row: pd.Series, prefixes: tuple[str, str, str]) -> tuple[float, float, float] | None:
    h, d, a = (fnum(row.get(col), 0.0) for col in prefixes)
    if h > 1.0 and d > 1.0 and a > 1.0:
        ih, idr, ia = 1 / h, 1 / d, 1 / a
        total = ih + idr + ia
        return round(ih / total, 5), round(idr / total, 5), round(ia / total, 5)
    return None


def binary_odds(row: pd.Series, over_col: str, under_col: str) -> tuple[float, float] | None:
    over, under = fnum(row.get(over_col), 0.0), fnum(row.get(under_col), 0.0)
    if over > 1.0 and under > 1.0:
        io, iu = 1 / over, 1 / under
        total = io + iu
        return round(io / total, 5), round(iu / total, 5)
    return None


def result_class(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "HOME"
    if away_goals > home_goals:
        return "AWAY"
    return "DRAW"


def points_for(gf: int, ga: int) -> int:
    if gf > ga:
        return 3
    if gf == ga:
        return 1
    return 0


def avg(values: list[float]) -> float:
    vals = [float(v) for v in values if v is not None]
    return round(sum(vals) / len(vals), 4) if vals else 0.0


def rolling_features(history: deque[dict[str, float]], prefix: str, window: int) -> dict[str, float]:
    recent = list(history)[-window:]
    return {
        f"feat_{prefix}_last{window}_games": float(len(recent)),
        f"feat_{prefix}_last{window}_gf": avg([x["gf"] for x in recent]),
        f"feat_{prefix}_last{window}_ga": avg([x["ga"] for x in recent]),
        f"feat_{prefix}_last{window}_points": avg([x["points"] for x in recent]),
        f"feat_{prefix}_last{window}_shots_for": avg([x["shots_for"] for x in recent]),
        f"feat_{prefix}_last{window}_shots_against": avg([x["shots_against"] for x in recent]),
        f"feat_{prefix}_last{window}_sot_for": avg([x["sot_for"] for x in recent]),
        f"feat_{prefix}_last{window}_sot_against": avg([x["sot_against"] for x in recent]),
        f"feat_{prefix}_last{window}_corners_for": avg([x["corners_for"] for x in recent]),
        f"feat_{prefix}_last{window}_corners_against": avg([x["corners_against"] for x in recent]),
        f"feat_{prefix}_last{window}_cards_for": avg([x["cards_for"] for x in recent]),
        f"feat_{prefix}_last{window}_cards_against": avg([x["cards_against"] for x in recent]),
    }


def update_history(history: dict[tuple[str, str], deque[dict[str, float]]], league_code: str, home: str, away: str, row: pd.Series, window_cap: int) -> None:
    hg, ag = fint(row.get("FTHG")), fint(row.get("FTAG"))
    home_key, away_key = (league_code, home), (league_code, away)
    h_cards = fint(row.get("HY")) + fint(row.get("HR"))
    a_cards = fint(row.get("AY")) + fint(row.get("AR"))
    history[home_key].append({
        "gf": float(hg),
        "ga": float(ag),
        "points": float(points_for(hg, ag)),
        "shots_for": fnum(row.get("HS")),
        "shots_against": fnum(row.get("AS")),
        "sot_for": fnum(row.get("HST")),
        "sot_against": fnum(row.get("AST")),
        "corners_for": fnum(row.get("HC")),
        "corners_against": fnum(row.get("AC")),
        "cards_for": float(h_cards),
        "cards_against": float(a_cards),
    })
    history[away_key].append({
        "gf": float(ag),
        "ga": float(hg),
        "points": float(points_for(ag, hg)),
        "shots_for": fnum(row.get("AS")),
        "shots_against": fnum(row.get("HS")),
        "sot_for": fnum(row.get("AST")),
        "sot_against": fnum(row.get("HST")),
        "corners_for": fnum(row.get("AC")),
        "corners_against": fnum(row.get("HC")),
        "cards_for": float(a_cards),
        "cards_against": float(h_cards),
    })
    while len(history[home_key]) > window_cap:
        history[home_key].popleft()
    while len(history[away_key]) > window_cap:
        history[away_key].popleft()


def parse_date(value: object) -> pd.Timestamp | None:
    parsed = pd.to_datetime(value, dayfirst=True, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed


def season_start_year(season_code: str) -> int:
    if len(season_code) == 4 and season_code.isdigit():
        return 2000 + int(season_code[:2])
    return 0


def build_row(row: pd.Series, league_code: str, season_code: str, match_idx: int, history: dict[tuple[str, str], deque[dict[str, float]]], window: int) -> dict[str, object] | None:
    home, away = str(row.get("HomeTeam") or "").strip(), str(row.get("AwayTeam") or "").strip()
    if not home or not away or pd.isna(row.get("FTHG")) or pd.isna(row.get("FTAG")):
        return None
    date = parse_date(row.get("Date"))
    if date is None:
        return None
    hg, ag = fint(row.get("FTHG")), fint(row.get("FTAG"))
    league_meta = LEAGUES[league_code]
    market = odds_triplet(row, ("AvgCH", "AvgCD", "AvgCA")) or odds_triplet(row, ("AvgH", "AvgD", "AvgA"))
    odds_available = 1.0 if market else 0.0
    if not market:
        market = (0.50, 0.29, 0.21)
    totals_market = binary_odds(row, "AvgC>2.5", "AvgC<2.5") or binary_odds(row, "Avg>2.5", "Avg<2.5") or (0.0, 0.0)
    out: dict[str, object] = {
        "fixture_id": f"FDATA-{league_code}-{season_code}-{match_idx:04d}",
        "fixture_date": date.strftime("%Y-%m-%d"),
        "league_id": league_meta["league_id"],
        "league_name": league_meta["league_name"],
        "country": league_meta["country"],
        "season": season_start_year(season_code),
        "season_code": season_code,
        "home_team": home,
        "away_team": away,
        "target_home_goals": hg,
        "target_away_goals": ag,
        "target_total_goals": hg + ag,
        "target_result_class": RESULT_MAP.get(str(row.get("FTR")), result_class(hg, ag)),
        "target_btts": int(hg > 0 and ag > 0),
        "target_over25": int(hg + ag >= 3),
        "target_under35": int(hg + ag <= 3),
        "target_home_shots": fnum(row.get("HS")),
        "target_away_shots": fnum(row.get("AS")),
        "target_home_sot": fnum(row.get("HST")),
        "target_away_sot": fnum(row.get("AST")),
        "target_home_corners": fnum(row.get("HC")),
        "target_away_corners": fnum(row.get("AC")),
        "target_home_yellows": fnum(row.get("HY")),
        "target_away_yellows": fnum(row.get("AY")),
        "target_home_reds": fnum(row.get("HR")),
        "target_away_reds": fnum(row.get("AR")),
        "feat_home_advantage": 1.0,
        "feat_odds_available": odds_available,
        "feat_market_home_prob": market[0],
        "feat_market_draw_prob": market[1],
        "feat_market_away_prob": market[2],
        "feat_market_over25_prob": totals_market[0],
        "feat_market_under25_prob": totals_market[1],
        "feat_season_start_year": float(season_start_year(season_code)),
    }
    for code in LEAGUES:
        out[f"feat_league_{code}"] = 1.0 if code == league_code else 0.0
    out.update(rolling_features(history[(league_code, home)], "home", window))
    out.update(rolling_features(history[(league_code, away)], "away", window))
    return out


def download_csv(season_code: str, league_code: str) -> pd.DataFrame:
    url = BASE_URL.format(season=season_code, league=league_code)
    return pd.read_csv(url)


def build_dataset(seasons: list[str], leagues: list[str], out_path: Path, summary_path: Path, window: int, strict: bool) -> None:
    rows: list[dict[str, object]] = []
    downloads: list[dict[str, object]] = []
    history: dict[tuple[str, str], deque[dict[str, float]]] = defaultdict(deque)
    match_idx = 0
    for season_code in seasons:
        for league_code in leagues:
            if league_code not in LEAGUES:
                raise RuntimeError(f"Unknown league code: {league_code}. Valid: {sorted(LEAGUES)}")
            try:
                df = download_csv(season_code, league_code)
            except Exception as exc:
                downloads.append({"season": season_code, "league": league_code, "status": "failed", "error": str(exc)})
                if strict:
                    raise
                continue
            df["_parsed_date"] = pd.to_datetime(df.get("Date"), dayfirst=True, errors="coerce")
            df = df.sort_values("_parsed_date")
            before = len(rows)
            for _, row in df.iterrows():
                built = build_row(row, league_code, season_code, match_idx, history, window)
                if built is None:
                    continue
                rows.append(built)
                update_history(history, league_code, str(row.get("HomeTeam")).strip(), str(row.get("AwayTeam")).strip(), row, max(window, 10))
                match_idx += 1
            downloads.append({"season": season_code, "league": league_code, "status": "ok", "source_rows": int(len(df)), "written_rows": len(rows) - before})
    if not rows:
        raise RuntimeError("No rows built from Football-Data CSVs")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_out = pd.DataFrame(rows).sort_values(["fixture_date", "fixture_id"])
    core = ["fixture_id", "fixture_date", "league_id", "season", "home_team", "away_team", "target_home_goals", "target_away_goals", "target_result_class"]
    cols = core + [c for c in df_out.columns if c not in core]
    df_out[cols].to_csv(out_path, index=False, encoding="utf-8")
    summary = {
        "rows": int(len(df_out)),
        "seasons": seasons,
        "leagues": leagues,
        "window": window,
        "downloads": downloads,
        "odds_available_rows": int(df_out.get("feat_odds_available", pd.Series(dtype=float)).sum()),
        "target_result_counts": df_out["target_result_class"].value_counts().to_dict(),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Football-Data dataset rows={len(df_out)} out={out_path}")
    print(f"summary={summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", action="append", default=[], help="Football-Data season code, e.g. 2324")
    parser.add_argument("--league", action="append", default=[], help="Football-Data league code: E0, SP1, I1, D1, F1")
    parser.add_argument("--out", type=Path, default=BASE / "vsigma_football_data_uk_top5.csv")
    parser.add_argument("--summary-out", type=Path, default=BASE / "vsigma_football_data_uk_top5_summary.json")
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    build_dataset(args.season or DEFAULT_SEASONS, args.league or DEFAULT_LEAGUES, args.out, args.summary_out, args.window, args.strict)
