from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

BOARD_FIELDS = [
    "target_date", "generated_at", "board_rank", "fixture_id", "home_team", "away_team",
    "final_decision", "board_bucket", "primary_market", "secondary_market", "stake_band",
    "execution_permission", "portfolio_status", "context_level", "forecast_confidence",
    "forecast_warning", "translation_score", "kill_switch", "stat_profile", "key_stat_forecast",
    "prelock_trigger", "live_trigger", "cancel_trigger", "operator_note", "source_guard",
    "auto_apply", "production_change",
]

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "lineup_bridge_status",
    "lineup_source_status", "starting_xi_rows", "home_starting_xi_rows", "away_starting_xi_rows",
    "home_formation", "away_formation", "original_final_decision", "bridged_final_decision",
    "original_execution_permission", "bridged_execution_permission", "original_forecast_warning",
    "bridged_forecast_warning", "original_operator_note", "bridged_operator_note", "bridge_action",
    "bridge_reason", "canonical_board_permission", "pick_permission", "stake_permission", "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "board_rows_reviewed", "lineup_confirmed_rows", "lineup_missing_rows",
    "board_rows_written", "bridge_status_counts", "bridge_action_counts", "pick_permission_counts",
    "stake_permission_counts", "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def load_board_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_daily_execution_board.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_daily_execution_board.csv")
    return rows


def load_lineup_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_forced_api_board_fixture_lineups.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_forced_api_board_fixture_lineups.csv")
    return rows


def split_tokens(text: str) -> list[str]:
    return [part.strip() for part in norm(text).replace(",", ";").split(";") if part.strip()]


def join_tokens(tokens: list[str]) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for token in tokens:
        key = up(token)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(token)
    return "; ".join(out)


def remove_warning(text: str, warning: str) -> str:
    return join_tokens([token for token in split_tokens(text) if up(token) != up(warning)])


def add_warning(text: str, warning: str) -> str:
    return join_tokens(split_tokens(text) + [warning])


def replace_missing_lineup_note(text: str) -> str:
    replacements = {
        "missing=lineup_coverage=NOT_DUE_YET;": "missing=lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS;",
        "missing=lineup_coverage=NONE;": "missing=lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS;",
        "lineup_coverage=NOT_DUE_YET": "lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS",
        "lineup_coverage=NONE": "lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS",
    }
    out = norm(text)
    for old, new in replacements.items():
        out = out.replace(old, new)
    if "CONFIRMED_BY_FORCED_API_LINEUPS" not in out:
        sep = "; " if out else ""
        out = f"{out}{sep}lineup_coverage=CONFIRMED_BY_FORCED_API_LINEUPS"
    return out


def lineup_profile(lineup_rows: list[dict[str, str]], fixture_id: str) -> dict[str, object]:
    rows = [row for row in lineup_rows if norm(row.get("fixture_id")) == fixture_id]
    starters = [row for row in rows if up(row.get("row_type")) == "START_XI"]
    home = [row for row in starters if up(row.get("team_side")).startswith("HOME")]
    away = [row for row in starters if up(row.get("team_side")).startswith("AWAY")]
    home_formations = [norm(row.get("formation")) for row in home if norm(row.get("formation"))]
    away_formations = [norm(row.get("formation")) for row in away if norm(row.get("formation"))]
    api_statuses = {up(row.get("api_status")) for row in rows if norm(row.get("api_status"))}
    confirmed = len(home) == 11 and len(away) == 11 and (not api_statuses or "OK" in api_statuses)
    return {
        "rows": rows,
        "starters": starters,
        "home_starters": home,
        "away_starters": away,
        "confirmed": confirmed,
        "home_formation": home_formations[0] if home_formations else "",
        "away_formation": away_formations[0] if away_formations else "",
        "api_status": ";".join(sorted(api_statuses)) if api_statuses else "NO_LINEUP_ROWS",
    }


def bridge_board_row(row: dict[str, str], profile: dict[str, object], day: str, generated: str) -> tuple[dict[str, object], dict[str, object]]:
    fixture_id = norm(row.get("fixture_id"))
    original_warning = norm(row.get("forecast_warning"))
    original_note = norm(row.get("operator_note"))
    original_final = norm(row.get("final_decision"))
    original_perm = norm(row.get("execution_permission"))

    confirmed = bool(profile.get("confirmed"))
    bridged_row: dict[str, object] = dict(row)
    bridge_action = "NO_CHANGE"
    bridge_status = "LINEUPS_NOT_CONFIRMED_BY_API"
    bridge_reason = "Forced API lineup snapshot did not produce 11 home starters and 11 away starters."

    if confirmed:
        bridge_status = "LINEUPS_CONFIRMED_BY_FORCED_API"
        bridge_action = "CLEAR_LINEUPS_INACTIVE_WARNING_KEEP_EXECUTION_LOCK"
        bridge_reason = "Forced API /fixtures/lineups returned 11 home starters and 11 away starters for board fixture_id. Execution remains locked unless a separate prelock resolver promotes it."
        new_warning = remove_warning(original_warning, "LINEUPS_INACTIVE")
        new_warning = add_warning(new_warning, "LINEUPS_CONFIRMED_BY_FORCED_API")
        bridged_row["forecast_warning"] = new_warning
        bridged_row["operator_note"] = replace_missing_lineup_note(original_note)
        bridged_row["prelock_trigger"] = add_warning(norm(row.get("prelock_trigger")), "lineups confirmed by forced API fixture-id refresh")
        # Do not promote to executable pick here. This bridge only removes stale lineup uncertainty.
        bridged_row["final_decision"] = original_final
        bridged_row["execution_permission"] = original_perm
        bridged_row["stake_band"] = norm(row.get("stake_band")) or "NO_STAKE_OR_SYMBOLIC"
        bridged_row["source_guard"] = add_warning(norm(row.get("source_guard")), "FORCED_API_LINEUP_BRIDGE")
    else:
        bridged_row["source_guard"] = add_warning(norm(row.get("source_guard")), "FORCED_API_LINEUP_BRIDGE_NO_CONFIRMATION")

    detail = {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": fixture_id,
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "lineup_bridge_status": bridge_status,
        "lineup_source_status": profile.get("api_status", "UNKNOWN"),
        "starting_xi_rows": len(profile.get("starters", [])),
        "home_starting_xi_rows": len(profile.get("home_starters", [])),
        "away_starting_xi_rows": len(profile.get("away_starters", [])),
        "home_formation": profile.get("home_formation", ""),
        "away_formation": profile.get("away_formation", ""),
        "original_final_decision": original_final,
        "bridged_final_decision": bridged_row.get("final_decision", ""),
        "original_execution_permission": original_perm,
        "bridged_execution_permission": bridged_row.get("execution_permission", ""),
        "original_forecast_warning": original_warning,
        "bridged_forecast_warning": bridged_row.get("forecast_warning", ""),
        "original_operator_note": original_note,
        "bridged_operator_note": bridged_row.get("operator_note", ""),
        "bridge_action": bridge_action,
        "bridge_reason": bridge_reason,
        "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
        "pick_permission": "NO_PICK_PERMISSION",
        "stake_permission": "NO_STAKE_PERMISSION",
        "auto_apply": "NO",
        "production_change": "NO",
    }
    return bridged_row, detail


def make_board_markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Daily Execution Board - {day} (Forced API Lineup Bridged Copy)",
        "",
        "## Summary",
        f"- rows_on_board: {len(rows)}",
        f"- bridge_status_counts: {summary.get('bridge_status_counts', 'none')}",
        f"- bridge_action_counts: {summary.get('bridge_action_counts', 'none')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Board Rows",
    ]
    if not rows:
        lines.append("- none")
    for row in rows:
        lines.append(
            f"- #{row.get('board_rank')} | {row.get('final_decision')} | {row.get('home_team')} vs {row.get('away_team')} | "
            f"market={row.get('primary_market')} | alt={row.get('secondary_market')} | stake={row.get('stake_band')} | "
            f"permission={row.get('execution_permission')} | conf={row.get('forecast_confidence')} | warnings={row.get('forecast_warning')} | "
            f"prelock={row.get('prelock_trigger')} | note={row.get('operator_note')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This is a bridged copy, not automatic execution permission.",
        "- Forced API lineups can clear stale lineup warnings but cannot create picks or stake.",
        "- Any future promotion must be handled by a separate prelock resolver with explicit governance.",
    ]
    return "\n".join(lines) + "\n"


def markdown(day: str, details: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Forced API Lineup Bridge to Board - {day}",
        "",
        "## Summary",
        f"- board_rows_reviewed: {summary['board_rows_reviewed']}",
        f"- lineup_confirmed_rows: {summary['lineup_confirmed_rows']}",
        f"- lineup_missing_rows: {summary['lineup_missing_rows']}",
        f"- board_rows_written: {summary['board_rows_written']}",
        f"- bridge_status_counts: {summary['bridge_status_counts']}",
        f"- bridge_action_counts: {summary['bridge_action_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Bridge Rows",
    ]
    if not details:
        lines.append("- none.")
    for row in details:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | status={row['lineup_bridge_status']} | "
            f"starters={row['starting_xi_rows']} ({row['home_starting_xi_rows']}-{row['away_starting_xi_rows']}) | "
            f"formations={row['home_formation']} / {row['away_formation']} | "
            f"decision={row['original_final_decision']}->{row['bridged_final_decision']} | "
            f"permission={row['original_execution_permission']}->{row['bridged_execution_permission']} | action={row['bridge_action']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This bridge only converts confirmed API lineup snapshots into a coverage signal.",
        "- It does not create picks, stake, canonical board permission, whitelist permission, or automatic execution.",
        "- The canonical board remains locked unless a later governed prelock resolver explicitly promotes it.",
    ]
    return "\n".join(lines) + "\n"


def replace_or_append_section(text: str, section: str, block: str) -> str:
    if section not in text:
        return text.rstrip() + block
    before = text.split(section, 1)[0].rstrip()
    after = text.split(section, 1)[1]
    next_idx = after.find("\n## ")
    tail = after[next_idx:] if next_idx >= 0 else ""
    return before + block + tail


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    section = "## Forced API Lineup Bridge to Board"
    lines = [
        section,
        f"- board_rows_reviewed: {summary.get('board_rows_reviewed', 'UNKNOWN')}",
        f"- lineup_confirmed_rows: {summary.get('lineup_confirmed_rows', 'UNKNOWN')}",
        f"- lineup_missing_rows: {summary.get('lineup_missing_rows', 'UNKNOWN')}",
        f"- board_rows_written: {summary.get('board_rows_written', 'UNKNOWN')}",
        f"- bridge_status_counts: {summary.get('bridge_status_counts', 'UNKNOWN')}",
        f"- bridge_action_counts: {summary.get('bridge_action_counts', 'UNKNOWN')}",
        "- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION",
        "- pick_permission: NO_PICK_PERMISSION",
        "- stake_permission: NO_STAKE_PERMISSION",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            md_path.write_text(replace_or_append_section(text, section, block), encoding="utf-8")


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    board = load_board_rows(processed, day)
    lineups = load_lineup_rows(processed, day)
    bridged_board: list[dict[str, object]] = []
    details: list[dict[str, object]] = []
    for row in board:
        fixture_id = norm(row.get("fixture_id"))
        profile = lineup_profile(lineups, fixture_id)
        bridged, detail = bridge_board_row(row, profile, day, generated)
        bridged_board.append(bridged)
        details.append(detail)
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "board_rows_reviewed": len(board),
        "lineup_confirmed_rows": sum(1 for row in details if row.get("lineup_bridge_status") == "LINEUPS_CONFIRMED_BY_FORCED_API"),
        "lineup_missing_rows": sum(1 for row in details if row.get("lineup_bridge_status") != "LINEUPS_CONFIRMED_BY_FORCED_API"),
        "board_rows_written": len(bridged_board),
        "bridge_status_counts": counts(details, "lineup_bridge_status"),
        "bridge_action_counts": counts(details, "bridge_action"),
        "pick_permission_counts": counts(details, "pick_permission"),
        "stake_permission_counts": counts(details, "stake_permission"),
        "next_action": "Use bridged copy for prelock review/repricing. Do not create picks or stake without separate governed promotion.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return bridged_board, details, summary, markdown(day, details, summary[0]), make_board_markdown(day, bridged_board, summary[0])


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    bridged_board, details, summary, md, board_md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_forced_api_lineup_bridge_to_board.csv", details, ROW_FIELDS)
        write_csv(base / "vsigma_forced_api_lineup_bridge_to_board_summary.csv", summary, SUMMARY_FIELDS)
        write_csv(base / "vsigma_daily_execution_board_lineup_bridged.csv", bridged_board, BOARD_FIELDS)
        (base / "vsigma_forced_api_lineup_bridge_to_board.md").write_text(md, encoding="utf-8")
        (base / "vsigma_daily_execution_board_lineup_bridged.md").write_text(board_md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA FORCED API LINEUP BRIDGE TO BOARD ===")
    print(f"board_rows_reviewed={summary[0]['board_rows_reviewed']}")
    print(f"lineup_confirmed_rows={summary[0]['lineup_confirmed_rows']}")
    print(f"lineup_missing_rows={summary[0]['lineup_missing_rows']}")
    print(f"pick_permission=NO_PICK_PERMISSION")
    print(f"stake_permission=NO_STAKE_PERMISSION")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
