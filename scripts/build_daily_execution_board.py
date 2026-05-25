from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "board_rank", "fixture_id", "home_team", "away_team",
    "final_decision", "board_bucket", "primary_market", "secondary_market", "stake_band",
    "execution_permission", "portfolio_status", "context_level", "forecast_confidence", "forecast_warning",
    "translation_score", "kill_switch", "stat_profile", "key_stat_forecast",
    "prelock_trigger", "live_trigger", "cancel_trigger", "operator_note",
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


def dated(base: Path, day: str, name: str) -> Path:
    return base / "today" / day / name


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [r for r in rows if row_day(r) in {"", day}]


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = norm(row.get("fixture_id")).replace(".0", "")
        if fid and fid not in out:
            out[fid] = row
    return out


def execution_order(permission: str) -> int:
    return {
        "REVIEW_LOW_STAKE": 1,
        "REVIEW_ONLY": 2,
        "LIVE_ONLY": 3,
        "STAT_WATCH_ONLY": 4,
        "NO_BET_OR_WATCH": 5,
        "NO_BET": 6,
    }.get(up(permission), 9)


def decision(permission: str, portfolio_status: str, confidence: str, kill: str) -> tuple[str, str, str]:
    p = up(permission)
    port = up(portfolio_status)
    conf = up(confidence)
    k = up(kill)
    if p == "REVIEW_LOW_STAKE":
        return "PRELOCK_REVIEW_LOW_STAKE", "CANDIDATE_REVIEW", "Low stake only if price, lineups and live/prelock signal confirm."
    if p == "REVIEW_ONLY":
        return "REVIEW_ONLY", "CANDIDATE_REVIEW", "Review only; no automatic execution."
    if p == "LIVE_ONLY":
        return "LIVE_ONLY", "LIVE_CANDIDATE", "No prematch serious stake; require live tempo and chance confirmation."
    if p == "STAT_WATCH_ONLY":
        return "STAT_WATCH_ONLY", "WATCHLIST", "Statistical signal only; blocked from execution without portfolio/context confirmation."
    if p == "NO_BET_OR_WATCH":
        return "NO_BET_OR_WATCH", "WEAK_WATCH", "No stake; watch only if live data dramatically changes context."
    if p == "NO_BET":
        return "NO_BET", "BLOCKED", "No execution permission."
    if conf == "LOW" or k:
        return "NO_BET_OR_WATCH", "WEAK_WATCH", "Unclassified permission with low confidence or kill switch."
    if port in {"REVIEW_ONLY", "LIVE_ONLY_OR_SYMBOLIC"}:
        return "REVIEW_ONLY", "CANDIDATE_REVIEW", "Portfolio allows only review/live handling."
    return "NO_BET_OR_WATCH", "WEAK_WATCH", "No clear final permission."


def key_stats(forecast: dict[str, str] | None) -> str:
    if not forecast:
        return "stats unavailable"
    return (
        f"goals {forecast.get('total_goals_low','')}-{forecast.get('total_goals_high','')} | "
        f"shots {forecast.get('total_shots_low','')}-{forecast.get('total_shots_high','')} | "
        f"SoT {forecast.get('total_sot_low','')}-{forecast.get('total_sot_high','')} | "
        f"corners {forecast.get('total_corners_low','')}-{forecast.get('total_corners_high','')} | "
        f"cards {forecast.get('total_cards_low','')}-{forecast.get('total_cards_high','')}"
    )


def prelock_trigger(permission: str, warning: str, primary: str) -> str:
    p = up(permission)
    w = up(warning)
    if p in {"NO_BET", "NO_BET_OR_WATCH", "STAT_WATCH_ONLY"}:
        return "none"
    triggers = ["price remains above minimum", "market not over-compressed"]
    if "LINEUPS_INACTIVE" in w:
        triggers.append("lineups confirmed")
    if "AVAILABILITY_RISK" in w:
        triggers.append("no new attacking/availability downgrade")
    if "OVER_2_5" in up(primary):
        triggers.append("conversion risk acceptable")
    return "; ".join(triggers)


def live_trigger(permission: str, primary: str) -> str:
    p = up(permission)
    if p in {"NO_BET"}:
        return "none"
    if "OVER" in up(primary) or "BTTS" in up(primary):
        return "live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm"
    if "CORNERS" in up(primary):
        return "live wide pressure: crosses, blocked shots and corner pace"
    if "CARDS" in up(primary):
        return "live tension: fouls, transitions, referee/card profile"
    if "UNDER" in up(primary):
        return "live control: low SoT, low big chances, stable defensive structure"
    return "live confirmation required"


def cancel_trigger(permission: str, warning: str, kill: str) -> str:
    p = up(permission)
    w = up(warning)
    k = up(kill)
    cancels = []
    if p in {"NO_BET", "NO_BET_OR_WATCH"}:
        cancels.append("default no bet")
    if "LOW_FORECAST_CONFIDENCE" in k:
        cancels.append("low forecast confidence")
    if "NO_PORTFOLIO_CONTEXT" in k:
        cancels.append("no portfolio/context confirmation")
    if "LINEUPS_INACTIVE" in w:
        cancels.append("bad or incomplete lineups")
    if "AVAILABILITY_RISK" in w:
        cancels.append("new availability downgrade")
    if not cancels:
        cancels.append("price below minimum or live sample contradicts thesis")
    return "; ".join(cancels)


def build_row(trans: dict[str, str], forecast: dict[str, str] | None, day: str, generated_at: str, rank: int) -> dict[str, object]:
    perm = up(trans.get("execution_permission"))
    primary = up(trans.get("primary_stat_market"))
    secondary = up(trans.get("secondary_stat_market"))
    final, bucket, note = decision(perm, trans.get("portfolio_status", ""), trans.get("forecast_confidence", ""), trans.get("kill_switch", ""))
    return {
        "target_date": day,
        "generated_at": generated_at,
        "board_rank": rank,
        "fixture_id": norm(trans.get("fixture_id")),
        "home_team": norm(trans.get("home_team")),
        "away_team": norm(trans.get("away_team")),
        "final_decision": final,
        "board_bucket": bucket,
        "primary_market": primary,
        "secondary_market": secondary,
        "stake_band": up(trans.get("stake_band")),
        "execution_permission": perm,
        "portfolio_status": up(trans.get("portfolio_status")),
        "context_level": up(trans.get("context_level")),
        "forecast_confidence": up(trans.get("forecast_confidence")),
        "forecast_warning": norm(trans.get("forecast_warning")),
        "translation_score": norm(trans.get("translation_score")),
        "kill_switch": up(trans.get("kill_switch")),
        "stat_profile": norm(trans.get("stat_profile")),
        "key_stat_forecast": key_stats(forecast),
        "prelock_trigger": prelock_trigger(perm, trans.get("forecast_warning", ""), primary),
        "live_trigger": live_trigger(perm, primary),
        "cancel_trigger": cancel_trigger(perm, trans.get("forecast_warning", ""), trans.get("kill_switch", "")),
        "operator_note": note,
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, base: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    trans = same_day(read_rows(dated(base, day, "vsigma_forecast_market_translator.csv")), day)
    forecasts = index_by_fixture(same_day(read_rows(dated(base, day, "vsigma_match_stat_forecasts.csv")), day))
    rows: list[dict[str, object]] = []
    ordered = sorted(trans, key=lambda r: (execution_order(r.get("execution_permission", "")), -int(num(r.get("translation_score"), 0))))
    for i, row in enumerate(ordered, start=1):
        fid = norm(row.get("fixture_id")).replace(".0", "")
        rows.append(build_row(row, forecasts.get(fid), day, generated_at, i))
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Daily Execution Board - {day}",
        "",
        "## Summary",
        f"- rows_on_board: {len(rows)}",
        f"- final_decision_counts: {counts(rows, 'final_decision')}",
        f"- board_bucket_counts: {counts(rows, 'board_bucket')}",
        "- source_guard: DATED_INPUT_ONLY",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Board Rows",
    ]
    if not rows:
        lines.append("- none. Run match stat forecasts and forecast market translator first.")
    for r in rows:
        lines.append(
            f"- #{r['board_rank']} | {r['final_decision']} | {r['home_team']} vs {r['away_team']} | "
            f"market={r['primary_market']} | alt={r['secondary_market']} | stake={r['stake_band']} | "
            f"score={r['translation_score']} | conf={r['forecast_confidence']} | bucket={r['board_bucket']} | "
            f"stats={r['key_stat_forecast']} | prelock={r['prelock_trigger']} | live={r['live_trigger']} | cancel={r['cancel_trigger']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This board is a decision dashboard, not an auto-bet executor.",
        "- REVIEW_LOW_STAKE still requires price/prelock/live confirmation.",
        "- STAT_WATCH_ONLY is observation only unless promoted by context/portfolio later.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write_rows(out_base / "vsigma_daily_execution_board.csv", rows)
        (out_base / "vsigma_daily_execution_board.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA DAILY EXECUTION BOARD ===")
    print(f"rows_on_board={len(rows)}")
    print(f"final_decision_counts={counts(rows, 'final_decision')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
