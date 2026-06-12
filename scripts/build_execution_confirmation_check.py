from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path

BASE = Path("data/processed")


def clean(v: object) -> str:
    t = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def yn(v: object, default: str = "PENDING") -> str:
    text = str(v or default).strip().upper()
    aliases = {
        "Y": "YES",
        "YES": "YES",
        "SI": "YES",
        "SÍ": "YES",
        "TRUE": "YES",
        "1": "YES",
        "N": "NO",
        "NO": "NO",
        "FALSE": "NO",
        "0": "NO",
        "P": "PENDING",
        "PENDING": "PENDING",
        "NA": "NA",
        "N/A": "NA",
    }
    return aliases.get(text, default)


def fnum(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).replace("%", "").strip())
    except Exception:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    return rows[0] if rows else {}


def write_csv(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(row.keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def confirmation_verdict(
    final_lock: dict[str, str],
    lineups_confirmed: str,
    tactical_confirmed: str,
    price_live: str,
    portfolio_ok: str,
    monitor_confirmed: str,
) -> tuple[str, str, list[str]]:
    flags: list[str] = []
    lock_verdict = str(final_lock.get("final_execution_verdict", ""))
    monitor_required = str(final_lock.get("monitor_required", "NO"))

    if not final_lock:
        return "NO_EXECUTION_NO_FINAL_LOCK", "Final execution lock is missing.", ["NO_FINAL_LOCK"]

    if lock_verdict.startswith("NO_EXECUTION"):
        return lock_verdict, "Final lock already blocks execution.", ["FINAL_LOCK_BLOCK"]

    if lock_verdict in {"EXECUTION_HOLD_LOW_AGREEMENT", "EXECUTION_HOLD_CONTEXT_WEAK"}:
        return "EXECUTION_HOLD_MANUAL_REVIEW", "Final lock requires manual review before any stake.", [lock_verdict]

    if lineups_confirmed != "YES":
        flags.append("LINEUPS_NOT_CONFIRMED")
    if tactical_confirmed != "YES":
        flags.append("TACTICAL_NOT_CONFIRMED")
    if price_live != "YES":
        flags.append("PRICE_NOT_CONFIRMED_LIVE")
    if portfolio_ok != "YES":
        flags.append("PORTFOLIO_NOT_OK")
    if monitor_required == "YES" and monitor_confirmed != "YES":
        flags.append("MONITOR_NOT_CONFIRMED")

    if flags:
        if "LINEUPS_NOT_CONFIRMED" in flags:
            return "EXECUTION_HOLD_LINEUPS", "Lineups are not confirmed.", flags
        if "TACTICAL_NOT_CONFIRMED" in flags:
            return "EXECUTION_HOLD_TACTICAL", "Tactical read has not confirmed the market path.", flags
        if "PRICE_NOT_CONFIRMED_LIVE" in flags:
            return "EXECUTION_HOLD_PRICE_RECHECK", "Price is not confirmed live.", flags
        if "PORTFOLIO_NOT_OK" in flags:
            return "EXECUTION_HOLD_PORTFOLIO", "Portfolio or exposure check failed or is pending.", flags
        return "EXECUTION_HOLD_MONITOR", "Monitor-required gate has not received extra confirmation.", flags

    if lock_verdict == "EXECUTION_HOLD_MONITOR" or monitor_required == "YES":
        return "EXECUTE_SMALL_STAKE_MONITOR", "All confirmations passed, but monitor flag limits this to small stake only.", []

    if lock_verdict == "EXECUTABLE_SHADOW":
        return "EXECUTE_SMALL_STAKE", "All confirmations passed. Small stake only; no automation.", []

    return "EXECUTION_HOLD_MANUAL_REVIEW", f"Unhandled final lock verdict: {lock_verdict}", ["UNHANDLED_LOCK_VERDICT"]


def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA Execution Confirmation Check - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('fixture')}",
        f"- confirmation_verdict: {row.get('confirmation_verdict')}",
        f"- selected_market: {row.get('selected_market')}",
        f"- selected_odds: {row.get('selected_odds')}",
        f"- selected_expected_roi: {row.get('selected_expected_roi')}",
        f"- stake_cap_pct_bankroll: {row.get('stake_cap_pct_bankroll')}",
        "",
        "## Required confirmations",
        f"- lineups_confirmed: {row.get('lineups_confirmed')}",
        f"- tactical_confirmed: {row.get('tactical_confirmed')}",
        f"- price_live: {row.get('price_live')}",
        f"- portfolio_ok: {row.get('portfolio_ok')}",
        f"- monitor_confirmed: {row.get('monitor_confirmed')}",
        "",
        "## Upstream lock",
        f"- final_execution_verdict: {row.get('final_execution_verdict')}",
        f"- monitor_required: {row.get('monitor_required')}",
        f"- veto_flags: {row.get('veto_flags')}",
        "",
        "## Confirmation note",
        f"- {row.get('confirmation_note')}",
        f"- blocking_flags: {row.get('blocking_flags')}",
        f"- user_notes: {row.get('user_notes')}",
        "",
        "## Hard rules",
        "- auto_bet: NO",
        "- production_change: NO",
        "- This file never sends or places bets.",
        "- EXECUTE_SMALL_STAKE only means all local checks passed and stake remains capped.",
    ]) + "\n"


def run(
    day: str,
    home: str,
    away: str,
    processed_dir: Path,
    lineups_confirmed: str,
    tactical_confirmed: str,
    price_live: str,
    portfolio_ok: str,
    monitor_confirmed: str,
    stake_cap_pct_bankroll: float,
    user_notes: str,
) -> None:
    slug = clean(f"{home}_vs_{away}")
    today = processed_dir / "today" / day
    final_lock = read_one(today / f"vsigma_final_execution_lock_{slug}.csv")

    lineups = yn(lineups_confirmed)
    tactical = yn(tactical_confirmed)
    price = yn(price_live)
    portfolio = yn(portfolio_ok)
    monitor = yn(monitor_confirmed, "PENDING")

    confirmation, note, flags = confirmation_verdict(final_lock, lineups, tactical, price, portfolio, monitor)

    row = {
        "target_date": day,
        "fixture": slug.replace("_", " "),
        "home_team": home,
        "away_team": away,
        "confirmation_verdict": confirmation,
        "selected_market": final_lock.get("selected_market", ""),
        "selected_odds": final_lock.get("selected_odds", ""),
        "selected_expected_roi": final_lock.get("selected_expected_roi", ""),
        "selected_edge_prob": final_lock.get("selected_edge_prob", ""),
        "stake_cap_pct_bankroll": stake_cap_pct_bankroll,
        "lineups_confirmed": lineups,
        "tactical_confirmed": tactical,
        "price_live": price,
        "portfolio_ok": portfolio,
        "monitor_confirmed": monitor,
        "final_execution_verdict": final_lock.get("final_execution_verdict", "MISSING"),
        "monitor_required": final_lock.get("monitor_required", "NO"),
        "veto_flags": final_lock.get("veto_flags", ""),
        "confirmation_note": note,
        "blocking_flags": ";".join(flags),
        "user_notes": user_notes,
        "auto_bet": "NO",
        "production_change": "NO",
    }

    for folder in [today, processed_dir / "governance"]:
        write_csv(folder / f"vsigma_execution_confirmation_check_{slug}.csv", row)
        (folder / f"vsigma_execution_confirmation_check_{slug}.md").write_text(md(row), encoding="utf-8")

    print(f"Execution confirmation: {confirmation} market={row['selected_market']} stake_cap={stake_cap_pct_bankroll}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    parser.add_argument("--lineups-confirmed", default="PENDING")
    parser.add_argument("--tactical-confirmed", default="PENDING")
    parser.add_argument("--price-live", default="PENDING")
    parser.add_argument("--portfolio-ok", default="PENDING")
    parser.add_argument("--monitor-confirmed", default="PENDING")
    parser.add_argument("--stake-cap-pct-bankroll", type=float, default=0.25)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    run(
        args.date,
        args.home,
        args.away,
        args.processed_dir,
        args.lineups_confirmed,
        args.tactical_confirmed,
        args.price_live,
        args.portfolio_ok,
        args.monitor_confirmed,
        args.stake_cap_pct_bankroll,
        args.notes,
    )
