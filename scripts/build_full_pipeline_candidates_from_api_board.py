from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("data/processed")
SUPPORTED_MARKETS = {
    "HOME", "DRAW", "AWAY", "UNDER_3_5", "HOME_TT_OVER_0_5", "AWAY_TT_OVER_0_5",
    "HOME_TT_UNDER_1_5", "AWAY_TT_UNDER_1_5",
}
ODDS_COLUMNS = [
    "odds", "decimal_odds", "current_odds", "market_odds", "best_odds", "primary_odds",
    "price", "live_odds", "closing_odds",
]
PROB_COLUMNS = {
    "home_prob": ["home_prob", "prob_home", "home_probability", "p_home", "model_home_prob"],
    "draw_prob": ["draw_prob", "prob_draw", "draw_probability", "p_draw", "model_draw_prob"],
    "away_prob": ["away_prob", "prob_away", "away_probability", "p_away", "model_away_prob"],
}


def clean(v: object) -> str:
    text = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def fnum(v: object, default: float = 0.0) -> float:
    try:
        text = str(v or "").strip().replace("%", "")
        if not text:
            return default
        return float(text)
    except Exception:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = []
        for row in rows:
            for key in row.keys():
                if key not in fields:
                    fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def pick_first(row: dict[str, str], columns: list[str]) -> str:
    for col in columns:
        val = str(row.get(col, "")).strip()
        if val:
            return val
    return ""


def load_board(processed: Path, day: str) -> tuple[list[dict[str, str]], Path | None]:
    paths = [
        processed / "today" / day / "vsigma_daily_execution_board.csv",
        processed / "governance" / "vsigma_daily_execution_board.csv",
        processed / "today" / day / "vsigma_today_competition_top.csv",
        processed / "vsigma_today_competition_top.csv",
    ]
    for path in paths:
        rows = read_rows(path)
        if rows:
            return rows, path
    return [], None


def load_lineups(processed: Path, day: str) -> tuple[list[dict[str, str]], Path | None]:
    paths = [
        processed / "today" / day / "vsigma_forced_api_board_fixture_lineups.csv",
        processed / "governance" / "vsigma_forced_api_board_fixture_lineups.csv",
        processed / "today" / day / "fixture_lineups_enrichment.csv",
        processed / "fixture_lineups_enrichment.csv",
    ]
    for path in paths:
        rows = read_rows(path)
        if rows:
            return rows, path
    return [], None


def lineup_status(lineups: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in lineups:
        fid = str(row.get("fixture_id", "")).strip()
        if fid:
            grouped[fid].append(row)
    out: dict[str, dict[str, object]] = {}
    for fid, rows in grouped.items():
        start_rows = [r for r in rows if str(r.get("row_type", "")).upper() in {"START_XI", "STARTING_XI", "STARTER"}]
        sides = Counter(str(r.get("team_side", "")).lower() for r in start_rows)
        api_ok = any(str(r.get("api_status", "")).upper() == "OK" for r in rows)
        total_start = len(start_rows)
        # National-team and lower-coverage feeds sometimes label aliases; require enough total starters plus API OK.
        confirmed = "YES" if api_ok and total_start >= 18 else "PENDING"
        out[fid] = {
            "lineups_confirmed": confirmed,
            "starting_xi_rows": total_start,
            "team_side_counts": ";".join(f"{k}={v}" for k, v in sides.items()) if sides else "none",
            "api_lineup_status": "OK" if api_ok else "MISSING_OR_NOT_OK",
        }
    return out


def normalize_market(value: str) -> str:
    raw = str(value or "").strip().upper()
    compact = clean(raw).upper()
    compact = compact.replace("__", "_")
    aliases = {
        "1": "HOME",
        "HOME_WIN": "HOME",
        "LOCAL": "HOME",
        "HOME": "HOME",
        "2": "AWAY",
        "AWAY_WIN": "AWAY",
        "VISITOR": "AWAY",
        "AWAY": "AWAY",
        "X": "DRAW",
        "DRAW": "DRAW",
        "UNDER35": "UNDER_3_5",
        "UNDER_3_5": "UNDER_3_5",
        "U35": "UNDER_3_5",
        "HOME_TT_OVER_0_5": "HOME_TT_OVER_0_5",
        "AWAY_TT_OVER_0_5": "AWAY_TT_OVER_0_5",
        "HOME_TT_UNDER_1_5": "HOME_TT_UNDER_1_5",
        "AWAY_TT_UNDER_1_5": "AWAY_TT_UNDER_1_5",
    }
    if compact in aliases:
        return aliases[compact]
    if "UNDER_3_5" in compact or "U3_5" in compact:
        return "UNDER_3_5"
    if "HOME" in compact and "WIN" in compact:
        return "HOME"
    if "AWAY" in compact and "WIN" in compact:
        return "AWAY"
    return compact


def market_from_board(row: dict[str, str]) -> tuple[str, str]:
    raw = pick_first(row, ["market_family", "primary_market", "market", "selection", "official_market"])
    market = normalize_market(raw)
    if market not in SUPPORTED_MARKETS:
        return "", raw or "NO_MARKET"
    return market, raw


def odds_from_board(row: dict[str, str]) -> tuple[str, str]:
    for col in ODDS_COLUMNS:
        val = str(row.get(col, "")).strip()
        if val and fnum(val, 0.0) > 1.0:
            return val, col
    return "", "MISSING_ODDS"


def probabilities_from_board(row: dict[str, str]) -> dict[str, str]:
    out = {}
    for target, cols in PROB_COLUMNS.items():
        out[target] = pick_first(row, cols)
    return out


def can_write_forecast(row: dict[str, str], market: str) -> tuple[bool, str]:
    probs = probabilities_from_board(row)
    if all(probs.values()):
        return True, "BOARD_PROBABILITIES"
    # Team-total and U35 gates can still run with fallback probabilities only for non-1X2 markets.
    if market not in {"HOME", "DRAW", "AWAY"}:
        return True, "NO_1X2_PROB_REQUIRED_FOR_GATE_MARKET"
    return False, "MISSING_1X2_PROBABILITIES"


def write_forecast_and_style(processed: Path, day: str, row: dict[str, str], market: str) -> None:
    home = pick_first(row, ["home_team", "home"])
    away = pick_first(row, ["away_team", "away"])
    slug = clean(f"{home}_vs_{away}")
    today = processed / "today" / day
    probs = probabilities_from_board(row)
    home_prob = probs.get("home_prob") or "0.34"
    draw_prob = probs.get("draw_prob") or "0.32"
    away_prob = probs.get("away_prob") or "0.34"
    forecast = [{
        "home_team": home,
        "away_team": away,
        "league_id": row.get("league_id", row.get("competition_id", "")),
        "league_name": row.get("league_name", row.get("competition", row.get("country", ""))),
        "home_prob": home_prob,
        "draw_prob": draw_prob,
        "away_prob": away_prob,
        "home_xg": row.get("home_xg", ""),
        "away_xg": row.get("away_xg", ""),
        "ft_score_primary": row.get("ft_score_primary", ""),
        "source_guard": "API_BOARD_BRIDGE_NO_NEW_API_CALL",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    style = [
        {
            "team_side": "home",
            "matches_sample": row.get("home_recent_matches", ""),
            "avg_goals_for": row.get("home_gf_avg", ""),
            "avg_goals_against": row.get("home_ga_avg", ""),
            "avg_shots": row.get("home_shots_for_avg", ""),
            "avg_sot": row.get("home_sot_for_avg", ""),
            "avg_corners": row.get("home_corners_for_avg", ""),
        },
        {
            "team_side": "away",
            "matches_sample": row.get("away_recent_matches", ""),
            "avg_goals_for": row.get("away_gf_avg", ""),
            "avg_goals_against": row.get("away_ga_avg", ""),
            "avg_shots": row.get("away_shots_for_avg", ""),
            "avg_sot": row.get("away_sot_for_avg", ""),
            "avg_corners": row.get("away_corners_for_avg", ""),
        },
    ]
    write_csv(today / f"vsigma_adhoc_match_stat_forecast_{slug}.csv", forecast)
    write_csv(today / f"vsigma_adhoc_team_style_{slug}.csv", style)


def build_candidates(processed: Path, day: str, default_confirmations: dict[str, str], stake_cap: str) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    board_rows, board_path = load_board(processed, day)
    lineup_rows, lineup_path = load_lineups(processed, day)
    lineup_by_fixture = lineup_status(lineup_rows)
    candidates: list[dict[str, object]] = []
    skipped: list[dict[str, object]] = []
    seen: set[str] = set()

    for idx, row in enumerate(board_rows, start=1):
        fixture_id = str(row.get("fixture_id", "")).strip()
        home = pick_first(row, ["home_team", "home"])
        away = pick_first(row, ["away_team", "away"])
        if not home or not away:
            skipped.append({"input_index": idx, "fixture_id": fixture_id, "skip_reason": "MISSING_TEAMS", "raw_market": ""})
            continue
        market, raw_market = market_from_board(row)
        if not market:
            skipped.append({"input_index": idx, "fixture_id": fixture_id, "home": home, "away": away, "skip_reason": "UNSUPPORTED_MARKET", "raw_market": raw_market})
            continue
        odds, odds_source = odds_from_board(row)
        if not odds:
            skipped.append({"input_index": idx, "fixture_id": fixture_id, "home": home, "away": away, "skip_reason": "MISSING_ODDS", "raw_market": raw_market})
            continue
        ok_forecast, forecast_reason = can_write_forecast(row, market)
        if not ok_forecast:
            skipped.append({"input_index": idx, "fixture_id": fixture_id, "home": home, "away": away, "skip_reason": forecast_reason, "raw_market": raw_market})
            continue
        key = f"{day}|{home}|{away}|{market}|{odds}"
        if key in seen:
            skipped.append({"input_index": idx, "fixture_id": fixture_id, "home": home, "away": away, "skip_reason": "DUPLICATE_CANDIDATE", "raw_market": raw_market})
            continue
        seen.add(key)
        write_forecast_and_style(processed, day, row, market)
        lineup_ctx = lineup_by_fixture.get(fixture_id, {})
        lineups_confirmed = str(lineup_ctx.get("lineups_confirmed") or default_confirmations["lineups_confirmed"])
        note = (
            f"API-board bridge. board_path={board_path}; lineup_path={lineup_path}; "
            f"fixture_id={fixture_id}; raw_market={raw_market}; odds_source={odds_source}; "
            f"forecast_reason={forecast_reason}; lineup_status={lineup_ctx.get('api_lineup_status', 'MISSING')}"
        )
        candidates.append({
            "date": day,
            "home": home,
            "away": away,
            "market_family": market,
            "odds": odds,
            "market_under25_prob": pick_first(row, ["market_under25_prob", "under25_prob", "under_25_prob"]),
            "market_over25_prob": pick_first(row, ["market_over25_prob", "over25_prob", "over_25_prob"]),
            "lineups_confirmed": lineups_confirmed,
            "tactical_confirmed": default_confirmations["tactical_confirmed"],
            "price_live": default_confirmations["price_live"],
            "portfolio_ok": default_confirmations["portfolio_ok"],
            "monitor_confirmed": default_confirmations["monitor_confirmed"],
            "stake_cap_pct_bankroll": stake_cap,
            "notes": note,
        })

    summary = {
        "target_date": day,
        "board_rows": len(board_rows),
        "lineup_rows": len(lineup_rows),
        "candidates_written": len(candidates),
        "skipped_rows": len(skipped),
        "board_source": str(board_path or "MISSING"),
        "lineup_source": str(lineup_path or "MISSING"),
        "auto_bet": "NO",
        "production_change": "NO",
    }
    return candidates, skipped, summary


def md(summary: dict[str, object], skipped: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA API Board Candidate Bridge - {summary.get('target_date')}",
        "",
        f"- board_rows: {summary.get('board_rows')}",
        f"- lineup_rows: {summary.get('lineup_rows')}",
        f"- candidates_written: {summary.get('candidates_written')}",
        f"- skipped_rows: {summary.get('skipped_rows')}",
        f"- board_source: {summary.get('board_source')}",
        f"- lineup_source: {summary.get('lineup_source')}",
        "- auto_bet: NO",
        "- production_change: NO",
        "",
        "## Skipped rows",
        "",
    ]
    if not skipped:
        lines.append("- None")
    else:
        for row in skipped[:50]:
            lines.append(
                f"- idx={row.get('input_index')} fixture={row.get('fixture_id')} "
                f"{row.get('home','')} vs {row.get('away','')} reason={row.get('skip_reason')} market={row.get('raw_market')}"
            )
    lines += [
        "",
        "## Guardrails",
        "- This bridge does not call API directly.",
        "- This bridge does not create picks from unsupported markets.",
        "- Missing odds/probabilities are not invented.",
        "- Batch execution remains auto_bet: NO.",
    ]
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> None:
    processed = Path(args.processed_dir)
    today = processed / "today" / args.date
    batch_dir = processed / "batch_inputs"
    out_csv = Path(args.out_csv) if args.out_csv else batch_dir / f"vsigma_api_board_candidates_{args.date}.csv"
    report_csv = processed / "governance" / f"vsigma_api_board_candidate_bridge_{args.date}.csv"
    report_md = processed / "governance" / f"vsigma_api_board_candidate_bridge_{args.date}.md"
    skipped_csv = processed / "governance" / f"vsigma_api_board_candidate_bridge_skipped_{args.date}.csv"

    default_confirmations = {
        "lineups_confirmed": args.lineups_confirmed,
        "tactical_confirmed": args.tactical_confirmed,
        "price_live": args.price_live,
        "portfolio_ok": args.portfolio_ok,
        "monitor_confirmed": args.monitor_confirmed,
    }
    candidates, skipped, summary = build_candidates(processed, args.date, default_confirmations, str(args.stake_cap_pct_bankroll))
    write_csv(out_csv, candidates)
    write_csv(report_csv, [summary])
    write_csv(skipped_csv, skipped)
    report_md.write_text(md(summary, skipped), encoding="utf-8")

    print(f"API board bridge candidates={len(candidates)} skipped={len(skipped)} out={out_csv}")
    print(f"report={report_md}")

    if args.run_batch and candidates:
        batch_name = args.batch_name or f"api_board_{args.date}"
        cmd = [
            sys.executable,
            "scripts/run_vsigma_batch_shadow_pipeline.py",
            "--input-csv", str(out_csv),
            "--batch-name", batch_name,
        ]
        print("Running batch:", " ".join(cmd))
        subprocess.run(cmd, check=True)
    elif args.run_batch:
        print("Batch skipped: no bridge candidates were written.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    parser.add_argument("--out-csv", default="")
    parser.add_argument("--lineups-confirmed", default="PENDING")
    parser.add_argument("--tactical-confirmed", default="PENDING")
    parser.add_argument("--price-live", default="PENDING")
    parser.add_argument("--portfolio-ok", default="PENDING")
    parser.add_argument("--monitor-confirmed", default="PENDING")
    parser.add_argument("--stake-cap-pct-bankroll", type=float, default=0.25)
    parser.add_argument("--run-batch", action="store_true")
    parser.add_argument("--batch-name", default="")
    run(parser.parse_args())
