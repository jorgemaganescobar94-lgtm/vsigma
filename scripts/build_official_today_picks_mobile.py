from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path("data/processed")
STOP_STATUSES = {"STOP", "BROKEN", "SYSTEM_FIX_REQUIRED", "CRITICAL_STOP"}
READY_ACTIONS = {"ENTER", "READY", "READY_LOW_STAKE_REVIEW", "EXECUTABLE", "EXECUTE", "APPROVED"}
BLOCK_ACTIONS = {"NO", "NO_BET", "WAIT", "HOLD", "STOP", "BROKEN", "SYSTEM_FIX_REQUIRED", "BLOCK", "BLOCKED"}

OUT_FIELDS = [
    "target_date", "generated_at", "official_status", "betting_permission",
    "rank", "home_team", "away_team", "primary_market", "secondary_market",
    "official_action", "executable_now", "stake_band", "confidence", "source_file",
    "block_reason", "operator_note", "auto_bet", "production_change",
]


def s(v: object) -> str:
    return "" if v is None else str(v).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def contains_any(text: str, values: set[str]) -> bool:
    upper = text.upper()
    return any(v in upper for v in values)


def mobile_guard(today_dir: Path) -> tuple[str, str, list[str]]:
    rows = read_csv(today_dir / "vsigma_mobile_operator_control_panel.csv")
    if not rows:
        return "MISSING_MOBILE_PANEL", "NO", ["mobile operator control panel missing"]

    notes: list[str] = []
    blocked = False
    permission = "UNKNOWN"
    for row in rows:
        card = s(row.get("card"))
        status = s(row.get("status"))
        detail = s(row.get("detail"))
        notes.append(f"{card}:{status}:{detail}")
        if "betting_permission=YES" in detail:
            permission = "YES"
        if "betting_permission=NO" in detail:
            permission = "NO"
        if status.upper() in STOP_STATUSES or contains_any(detail, STOP_STATUSES):
            blocked = True

    if blocked:
        return "SYSTEM_STOP_NO_PICKS", permission, notes
    if permission != "YES":
        return "NO_BETTING_PERMISSION", permission, notes
    return "MOBILE_GATE_OPEN", permission, notes


def row_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = s(row.get(key))
        if value:
            return value
    return ""


def is_executable(row: dict[str, str]) -> bool:
    action = row_value(row, "official_action", "recheck_decision", "base_decision", "decision", "action")
    executable = row_value(row, "executable_now", "permission", "betting_permission", "is_actionable")
    block = row_value(row, "final_block_reason", "block_reason", "kill_switch", "gate_decision", "availability_status")

    if action.upper() in BLOCK_ACTIONS or contains_any(block, STOP_STATUSES | {"NO_BOARD", "MISSING", "BLOCK", "OUTSIDE_PRELOCK_WINDOW"}):
        return False
    if executable.upper() in {"NO", "FALSE", "0"}:
        return False
    if action.upper() in READY_ACTIONS:
        return True
    if executable.upper() in {"YES", "TRUE", "1"} and action.upper() not in BLOCK_ACTIONS:
        return True
    return False


def collect_candidate_rows(today_dir: Path) -> list[dict[str, object]]:
    sources = [
        today_dir / "vsigma_prelock_live_recheck.csv",
        today_dir / "vsigma_daily_execution_board.csv",
        today_dir / "vsigma_execution_board.csv",
        today_dir / "vsigma_daily_board.csv",
        today_dir / "vsigma_shortlist.csv",
    ]
    out: list[dict[str, object]] = []
    seen = set()

    for source in sources:
        rows = read_csv(source)
        for idx, row in enumerate(rows, start=1):
            if not is_executable(row):
                continue
            home = row_value(row, "home_team", "home")
            away = row_value(row, "away_team", "away")
            primary = row_value(row, "primary_market", "market_primary", "market", "recommended_market")
            key = (home, away, primary, source.name)
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "rank": row_value(row, "rank") or str(len(out) + 1),
                "home_team": home,
                "away_team": away,
                "primary_market": primary,
                "secondary_market": row_value(row, "secondary_market", "market_secondary", "alternative_market"),
                "official_action": row_value(row, "official_action", "recheck_decision", "decision", "action"),
                "executable_now": row_value(row, "executable_now", "permission", "is_actionable"),
                "stake_band": row_value(row, "stake_band", "stake", "stake_quality"),
                "confidence": row_value(row, "forecast_confidence", "confidence", "accuracy_confidence_score"),
                "source_file": source.name,
                "block_reason": row_value(row, "final_block_reason", "block_reason", "kill_switch", "gate_decision"),
                "operator_note": row_value(row, "operator_note", "note", "next_action"),
            })
    return out


def md(day: str, generated_at: str, official_status: str, betting_permission: str, rows: list[dict[str, object]], guard_notes: list[str]) -> str:
    lines = [
        f"# vSIGMA Official Today Picks - {day}",
        "",
        "## Official Gate",
        f"- official_status: {official_status}",
        f"- betting_permission: {betting_permission}",
        f"- generated_at: {generated_at}",
        "- auto_bet: NO",
        "- production_change: NO",
        "",
    ]

    if not rows:
        lines += [
            "## Official Picks",
            "- none.",
            "",
            "## Verdict",
            "- NO OFFICIAL EXECUTABLE PICKS.",
            "- Do not replace this with manual vSIGMA reading.",
            "",
        ]
    else:
        lines += ["## Official Picks"]
        for row in rows:
            lines.append(
                f"- #{row.get('rank')} | {row.get('home_team')} vs {row.get('away_team')} | "
                f"market={row.get('primary_market')} | alt={row.get('secondary_market')} | "
                f"action={row.get('official_action')} | stake={row.get('stake_band')} | source={row.get('source_file')}"
            )
        lines.append("")

    lines += [
        "## Guard Notes",
    ]
    for note in guard_notes[:12]:
        lines.append(f"- {note}")
    lines += [
        "",
        "## Rules",
        "- If official_status is SYSTEM_STOP_NO_PICKS, BROKEN, MISSING_MOBILE_PANEL or NO_BETTING_PERMISSION, there are no official picks.",
        "- This file is the mobile operator surface only; it does not auto-place bets.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, timezone: str, processed_dir: Path) -> None:
    now = datetime.now(ZoneInfo(timezone))
    if not day:
        day = now.date().isoformat()
    generated_at = now.isoformat(timespec="seconds")
    today_dir = processed_dir / "today" / day

    official_status, betting_permission, guard_notes = mobile_guard(today_dir)
    candidates: list[dict[str, object]] = []
    if official_status == "MOBILE_GATE_OPEN":
        candidates = collect_candidate_rows(today_dir)
        official_status = "OFFICIAL_PICKS_AVAILABLE" if candidates else "NO_EXECUTABLE_ROWS"

    output_rows = []
    for row in candidates:
        output_rows.append({
            "target_date": day,
            "generated_at": generated_at,
            "official_status": official_status,
            "betting_permission": betting_permission,
            **row,
            "auto_bet": "NO",
            "production_change": "NO",
        })

    if not output_rows:
        output_rows = [{
            "target_date": day,
            "generated_at": generated_at,
            "official_status": official_status,
            "betting_permission": betting_permission,
            "rank": "",
            "home_team": "",
            "away_team": "",
            "primary_market": "",
            "secondary_market": "",
            "official_action": "NO_PICKS",
            "executable_now": "NO",
            "stake_band": "NO_STAKE",
            "confidence": "",
            "source_file": "vsigma_mobile_operator_control_panel.csv",
            "block_reason": official_status,
            "operator_note": "Official mobile gate did not allow executable picks.",
            "auto_bet": "NO",
            "production_change": "NO",
        }]

    for folder in [today_dir, processed_dir / "governance"]:
        write_csv(folder / f"vsigma_official_today_picks_{day}.csv", output_rows, OUT_FIELDS)
        (folder / f"vsigma_official_today_picks_{day}.md").write_text(
            md(day, generated_at, official_status, betting_permission, candidates, guard_notes),
            encoding="utf-8",
        )

    print(f"official_status={official_status} betting_permission={betting_permission} picks={len(candidates)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="")
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)
