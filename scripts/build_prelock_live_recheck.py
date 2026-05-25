from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team",
    "base_decision", "recheck_decision", "primary_market", "secondary_market", "stake_band",
    "lineup_status", "minutes_to_kickoff", "availability_status", "gate_decision",
    "forecast_confidence", "translation_score", "kill_switch", "next_check", "operator_note",
    "source_guard", "auto_apply", "production_change",
]


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def num(v: object, default: float | None = None) -> float | None:
    try:
        t = norm(v)
        if not t or t.lower() == "nan":
            return default
        return float(t)
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
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def dated(base: Path, day: str, name: str) -> Path:
    return base / "today" / day / name


def row_day(row: dict[str, str]) -> str:
    for k in ("target_date", "date"):
        v = norm(row.get(k))[:10]
        if v:
            return v
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [r for r in rows if row_day(r) in {"", day}]


def ix(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for r in rows:
        fid = norm(r.get("fixture_id")).replace(".0", "")
        if fid and fid not in out:
            out[fid] = r
    return out


def rank_order(decision: str) -> int:
    return {
        "READY_LOW_STAKE_REVIEW": 1,
        "WAIT_PRELOCK": 2,
        "WAIT_LINEUPS": 3,
        "LIVE_RECHECK_ONLY": 4,
        "LIVE_ONLY_WAIT_TRIGGER": 5,
        "STAT_WATCH_ONLY": 6,
        "NO_BET_OR_WATCH": 7,
        "CANCELLED_NO_BET": 8,
    }.get(up(decision), 99)


def timing(minutes: float | None) -> str:
    if minutes is None:
        return "UNKNOWN"
    if minutes <= 0:
        return "LIVE"
    if minutes <= 30:
        return "F30"
    if minutes <= 60:
        return "F60"
    if minutes <= 90:
        return "F90"
    return "EARLY"


def decide(board: dict[str, str], gate: dict[str, str] | None, tr: dict[str, str] | None) -> tuple[str, str, str]:
    base = up(board.get("final_decision"))
    conf = up(board.get("forecast_confidence"))
    score = num(board.get("translation_score"), num((tr or {}).get("translation_score"), 0.0)) or 0.0
    kill = up((tr or {}).get("kill_switch"))
    lineup = up((gate or {}).get("lineup_status"))
    gd = up((gate or {}).get("gate_decision"))
    av = up((gate or {}).get("availability_status"))
    mins = num((gate or {}).get("lineup_minutes_to_kickoff"), None)
    t = timing(mins)

    if base == "NO_BET" or kill == "LOW_FORECAST_CONFIDENCE" or conf == "LOW":
        return "CANCELLED_NO_BET" if base == "NO_BET" else "NO_BET_OR_WATCH", "none", "blocked by board or low confidence"
    if av in {"AVAILABILITY_CONFLICT", "AVAILABILITY_RISK_ON_PICK_SIDE"}:
        return "CANCELLED_NO_BET", "rerun after availability update", "availability conflict"
    if base == "NO_BET_OR_WATCH":
        return "NO_BET_OR_WATCH", "watch only", "weak watch state"
    if base == "STAT_WATCH_ONLY":
        return "STAT_WATCH_ONLY", "rerun full chain if promoted", "stat signal lacks portfolio context"
    if base == "LIVE_ONLY":
        if t == "LIVE":
            return "LIVE_RECHECK_ONLY", "live sample required", "prematch window closed"
        return "LIVE_ONLY_WAIT_TRIGGER", "wait for live trigger", "prematch serious stake blocked"
    if base in {"PRELOCK_REVIEW_LOW_STAKE", "REVIEW_ONLY"}:
        if gd == "WAIT_PRELOCK" or lineup == "WAIT_PRELOCK" or t == "EARLY":
            return "WAIT_PRELOCK", "rerun F90/F60/F30", "outside prelock or gate requests prelock"
        if t == "LIVE":
            return "LIVE_RECHECK_ONLY", "live sample required", "prelock window passed"
        if score >= 30 and conf != "LOW" and lineup in {"LINEUPS_CONFIRMED", "LINEUPS_NOT_CONFIRMED", "LINEUP_PROXY_ONLY"}:
            return "READY_LOW_STAKE_REVIEW", "price/prelock/live confirmation", "low-stake review allowed, not automatic"
        return "WAIT_LINEUPS", "rerun at next checkpoint", "lineup or score not strong enough"
    return "NO_BET_OR_WATCH", "watch only", "unclassified state"


def build_row(board: dict[str, str], gate: dict[str, str] | None, tr: dict[str, str] | None, day: str, gen: str, rank: int) -> dict[str, object]:
    recheck, next_check, note = decide(board, gate, tr)
    return {
        "target_date": day,
        "generated_at": gen,
        "rank": rank,
        "fixture_id": norm(board.get("fixture_id")),
        "home_team": norm(board.get("home_team")),
        "away_team": norm(board.get("away_team")),
        "base_decision": up(board.get("final_decision")),
        "recheck_decision": recheck,
        "primary_market": up(board.get("primary_market")),
        "secondary_market": up(board.get("secondary_market")),
        "stake_band": up(board.get("stake_band")),
        "lineup_status": up((gate or {}).get("lineup_status")),
        "minutes_to_kickoff": norm((gate or {}).get("lineup_minutes_to_kickoff")),
        "availability_status": up((gate or {}).get("availability_status")),
        "gate_decision": up((gate or {}).get("gate_decision")),
        "forecast_confidence": up(board.get("forecast_confidence")),
        "translation_score": norm(board.get("translation_score")),
        "kill_switch": up((tr or {}).get("kill_switch")),
        "next_check": next_check,
        "operator_note": note,
        "source_guard": "DATED_INPUT_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, base: Path) -> list[dict[str, object]]:
    gen = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    board = same_day(read_rows(dated(base, day, "vsigma_daily_execution_board.csv")), day)
    gates = ix(same_day(read_rows(dated(base, day, "vsigma_objective_availability_gate.csv")), day))
    trans = ix(same_day(read_rows(dated(base, day, "vsigma_forecast_market_translator.csv")), day))
    rows: list[dict[str, object]] = []
    for i, b in enumerate(board, start=1):
        fid = norm(b.get("fixture_id")).replace(".0", "")
        rows.append(build_row(b, gates.get(fid), trans.get(fid), day, gen, i))
    rows.sort(key=lambda r: (rank_order(str(r["recheck_decision"])), int(r["rank"])))
    for i, r in enumerate(rows, start=1):
        r["rank"] = i
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Prelock/Live Recheck - {day}", "", "## Summary",
        f"- rows_rechecked: {len(rows)}",
        f"- recheck_decision_counts: {counts(rows, 'recheck_decision')}",
        "- source_guard: DATED_INPUT_ONLY", "- auto_apply: NO", "- production_change: NO", "", "## Recheck Rows",
    ]
    if not rows:
        lines.append("- none. Run daily execution board first.")
    for r in rows:
        lines.append(
            f"- #{r['rank']} | {r['recheck_decision']} | {r['home_team']} vs {r['away_team']} | "
            f"market={r['primary_market']} | stake={r['stake_band']} | lineup={r['lineup_status']} | "
            f"min={r['minutes_to_kickoff'] or 'NA'} | availability={r['availability_status']} | "
            f"next={r['next_check']} | note={r['operator_note']}"
        )
    lines += ["", "## Guardrails", "- This recheck does not execute automatically.", "- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write_rows(out_base / "vsigma_prelock_live_recheck.csv", rows)
        (out_base / "vsigma_prelock_live_recheck.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA PRELOCK LIVE RECHECK ===")
    print(f"rows_rechecked={len(rows)}")
    print(f"recheck_decision_counts={counts(rows, 'recheck_decision')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
