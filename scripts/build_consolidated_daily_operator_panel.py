from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
PANEL_FIELDS = [
    "target_date",
    "generated_at",
    "section",
    "status",
    "detail",
    "next_action",
    "auto_apply",
    "production_change",
]

EXECUTABLE_DECISIONS = {
    "READY_LOW_STAKE_REVIEW",
    "REVIEW_LOW_STAKE",
    "PRELOCK_REVIEW",
    "ACTION_REVIEW_NOW",
    "EXECUTABLE_PREMATCH",
    "PREMATCH_CORE",
    "CORE_PREMATCH",
}
LIVE_DECISIONS = {
    "LIVE_ONLY",
    "LIVE_ONLY_WAIT_TRIGGER",
    "LIVE_RECHECK_ONLY",
}
WATCH_DECISIONS = {
    "STAT_WATCH_ONLY",
    "NO_BET_OR_WATCH",
    "WATCH_ONLY",
    "WEAK_WATCH",
}
NO_BET_DECISIONS = {
    "NO_BET",
    "CANCELLED_NO_BET",
    "BLOCKED",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PANEL_FIELDS)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in PANEL_FIELDS} for row in rows])


def clean(value: object, limit: int = 180) -> str:
    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) > limit:
        return text[: max(0, limit - 1)].rstrip() + "…"
    return text


def nz(*values: object, default: str = "", limit: int = 180) -> str:
    for value in values:
        text = clean(value, limit=limit)
        if text and text.lower() not in {"none", "nan", "unknown"}:
            return text
    return default


def meta(text: str, key: str) -> str:
    match = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return match.group(1).strip() if match else "UNKNOWN"


def fmt_counts(counts: Counter[str]) -> str:
    if not counts:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in counts.items())


def teams(row: dict[str, str]) -> str:
    return f"{nz(row.get('home_team'), default='UNKNOWN_HOME')} vs {nz(row.get('away_team'), default='UNKNOWN_AWAY')}"


def decision_of(row: dict[str, str]) -> str:
    return nz(row.get("final_decision"), row.get("recheck_decision"), row.get("base_decision"), default="UNKNOWN")


def fixture_key(row: dict[str, str]) -> str:
    fid = str(row.get("fixture_id", "")).replace(".0", "").strip()
    if fid:
        return fid
    return "|".join([teams(row), nz(row.get("primary_market"), row.get("market"))])


def unique(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        key = fixture_key(row)
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def top_rows(rows: list[dict[str, str]], decisions: set[str], limit: int = 8) -> list[dict[str, str]]:
    selected = [row for row in unique(rows) if decision_of(row) in decisions]
    return selected[:limit]


def row_line(row: dict[str, str], include_status: bool = True) -> str:
    rank = nz(row.get("board_rank"), row.get("rank"))
    prefix = f"#{rank} | " if rank else ""
    decision = decision_of(row)
    market = nz(row.get("primary_market"), row.get("market"))
    alt = nz(row.get("secondary_market"))
    stake = nz(row.get("stake_band"))
    permission = nz(row.get("execution_permission"))
    confidence = nz(row.get("forecast_confidence"))
    score = nz(row.get("translation_score"))
    status = nz(row.get("match_status"))
    minute = nz(row.get("elapsed"))
    window = nz(row.get("window_status"))
    live_decision = nz(row.get("live_trigger_decision"))
    parts = [
        f"{prefix}{decision}" if include_status else prefix.rstrip(" |"),
        teams(row),
        f"market={market}" if market else "",
        f"alt={alt}" if alt else "",
        f"stake={stake}" if stake else "",
        f"permission={permission}" if permission else "",
        f"conf={confidence}" if confidence else "",
        f"score={score}" if score else "",
        f"window={window}" if window else "",
        f"live={live_decision}" if live_decision else "",
        f"match={status}" if status else "",
        f"min={minute}" if minute else "",
    ]
    return " | ".join(part for part in parts if part)


def merge_live_rows(board_rows: list[dict[str, str]], prelock_rows: list[dict[str, str]], live_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    board_by_key = {fixture_key(row): row for row in unique(board_rows)}
    prelock_by_key = {fixture_key(row): row for row in unique(prelock_rows)}
    live_by_key = {fixture_key(row): row for row in unique(live_rows)}
    out: list[dict[str, str]] = []
    out_keys: set[str] = set()

    for row in unique(board_rows):
        if decision_of(row) in LIVE_DECISIONS:
            key = fixture_key(row)
            merged = dict(row)
            if key in prelock_by_key:
                merged.update(prelock_by_key[key])
            if key in live_by_key:
                merged.update(live_by_key[key])
            out.append(merged)
            out_keys.add(key)

    for row in unique(prelock_rows):
        if decision_of(row) in LIVE_DECISIONS:
            key = fixture_key(row)
            if key in out_keys:
                continue
            base = dict(board_by_key.get(key, row))
            base.update(row)
            if key in live_by_key:
                base.update(live_by_key[key])
            out.append(base)
            out_keys.add(key)

    return out


def extract_coverage(rows: list[dict[str, str]]) -> tuple[str, list[str]]:
    if not rows:
        return "NO_BOARD_ROWS", ["- no daily board rows available"]

    guard_counts = Counter(nz(row.get("source_guard"), default="UNKNOWN") for row in rows)
    permission_counts = Counter(nz(row.get("execution_permission"), default="UNKNOWN") for row in rows)
    warnings = Counter()
    coverage_scores: list[float] = []
    missing_parts: Counter[str] = Counter()

    for row in rows:
        for token in nz(row.get("forecast_warning"), default="").split(";"):
            token = token.strip()
            if token:
                warnings[token] += 1
        note = nz(row.get("operator_note"), default="", limit=500)
        score_match = re.search(r"coverage_score=([0-9.]+)", note)
        if score_match:
            try:
                coverage_scores.append(float(score_match.group(1)))
            except ValueError:
                pass
        missing_match = re.search(r"missing=([^,]+)", note)
        if missing_match:
            for item in missing_match.group(1).split(";"):
                item = item.strip()
                if item:
                    missing_parts[item] += 1

    avg_coverage = f"{sum(coverage_scores) / len(coverage_scores):.1f}" if coverage_scores else "UNKNOWN"
    detail = (
        f"rows={len(rows)}; source_guard={fmt_counts(guard_counts)}; "
        f"permission={fmt_counts(permission_counts)}; avg_coverage={avg_coverage}; "
        f"warnings={fmt_counts(warnings)}"
    )
    lines = [
        f"- board_rows={len(rows)}",
        f"- source_guard_counts: {fmt_counts(guard_counts)}",
        f"- execution_permission_counts: {fmt_counts(permission_counts)}",
        f"- avg_coverage_score: {avg_coverage}",
        f"- forecast_warning_counts: {fmt_counts(warnings)}",
        f"- missing_data_counts: {fmt_counts(missing_parts)}",
    ]
    return detail, lines


def source_reliability_summary(governor_rows: list[dict[str, str]], governor_text: str) -> tuple[str, list[str]]:
    if governor_rows:
        verdict_counts = Counter(nz(row.get("reliability_verdict"), default="UNKNOWN") for row in governor_rows)
        gate_counts = Counter(nz(row.get("sample_gate"), default="UNKNOWN") for row in governor_rows)
        action_counts = Counter(nz(row.get("recommended_registry_action"), default="UNKNOWN") for row in governor_rows)
        detail = (
            f"sources={len(governor_rows)}; verdicts={fmt_counts(verdict_counts)}; "
            f"sample_gates={fmt_counts(gate_counts)}; actions={fmt_counts(action_counts)}"
        )
        lines = [
            f"- sources_reviewed: {len(governor_rows)}",
            f"- verdict_counts: {fmt_counts(verdict_counts)}",
            f"- sample_gate_counts: {fmt_counts(gate_counts)}",
            f"- recommended_action_counts: {fmt_counts(action_counts)}",
        ]
        return detail, lines

    if governor_text:
        detail = (
            f"sources={meta(governor_text, 'sources_reviewed')}; "
            f"verdicts={meta(governor_text, 'verdict_counts')}; "
            f"sample_gates={meta(governor_text, 'sample_gate_counts')}; "
            f"actions={meta(governor_text, 'recommended_action_counts')}"
        )
        lines = [
            f"- sources_reviewed: {meta(governor_text, 'sources_reviewed')}",
            f"- verdict_counts: {meta(governor_text, 'verdict_counts')}",
            f"- sample_gate_counts: {meta(governor_text, 'sample_gate_counts')}",
            f"- recommended_action_counts: {meta(governor_text, 'recommended_action_counts')}",
        ]
        return detail, lines

    return "UNAVAILABLE", ["- source reliability governor unavailable for this date"]


def lineup_summary(folder: Path, governance: Path) -> tuple[str, list[str]]:
    candidates = [
        folder / "official_lineup_sources.csv",
        folder / "probable_lineup_sources_autonomous.csv",
        folder / "vsigma_probable_lineup_consensus.csv",
        folder / "vsigma_probable_lineup_accuracy_ledger.csv",
        folder / "vsigma_probable_lineup_extraction_quality_ledger.csv",
        governance / "official_lineup_sources.csv",
        governance / "probable_lineup_sources_autonomous.csv",
        governance / "vsigma_probable_lineup_accuracy_ledger.csv",
        governance / "vsigma_probable_lineup_extraction_quality_ledger.csv",
    ]
    lines: list[str] = []
    total_rows = 0
    status_counts: Counter[str] = Counter()
    file_count = 0

    for path in candidates:
        rows = read_csv(path)
        if not rows:
            continue
        file_count += 1
        total_rows += len(rows)
        status_field = next((field for field in ["probable_status", "lineup_status", "import_status", "quality_status", "evaluation_status"] if field in rows[0]), "")
        if status_field:
            counts = Counter(nz(row.get(status_field), default="UNKNOWN") for row in rows)
            status_counts.update(counts)
            lines.append(f"- {path}: rows={len(rows)}; {status_field}={fmt_counts(counts)}")
        else:
            lines.append(f"- {path}: rows={len(rows)}")

    if not lines:
        return "NO_LINEUP_FILES", ["- no official/probable lineup files found for panel inputs"]

    detail = f"files={file_count}; rows={total_rows}; statuses={fmt_counts(status_counts)}"
    return detail, lines[:12]


def next_triggers_summary() -> tuple[str, list[str]]:
    trigger_dir = Path(".vsigma/triggers")
    rows = []
    if trigger_dir.exists():
        for path in sorted(trigger_dir.glob("*.trigger")):
            text = read_text(path)
            reason = "UNKNOWN"
            triggered_at = "UNKNOWN"
            day = "UNKNOWN"
            for line in text.splitlines():
                if line.startswith("reason="):
                    reason = line.split("=", 1)[1].strip()
                elif line.startswith("triggered_at="):
                    triggered_at = line.split("=", 1)[1].strip()
                elif line.startswith("date="):
                    day = line.split("=", 1)[1].strip()
            rows.append(f"- {path}: date={day}; reason={reason}; triggered_at={triggered_at}")

    if not rows:
        rows = [
            "- scheduled workflows expected: daily operator brief, prelock official lineup recheck, live trigger validator, post-match learning chain",
            "- no local trigger bridge files found by panel",
        ]
    return f"triggers={len(rows)}", rows[:12]


def operator_summary(operator_text: str, health_text: str, board_rows: list[dict[str, str]], prelock_rows: list[dict[str, str]], live_rows: list[dict[str, str]]) -> tuple[str, str, list[str]]:
    action = meta(operator_text, "action_level") if operator_text else "UNAVAILABLE"
    final = meta(operator_text, "compact_final_decision") if operator_text else "UNAVAILABLE"
    risk = meta(operator_text, "risk_label") if operator_text else "UNAVAILABLE"
    health = meta(health_text, "system_status") if health_text else "UNKNOWN"

    if action == "UNAVAILABLE":
        if not board_rows and not prelock_rows and not live_rows:
            status = "WAIT_DAILY_CHAIN"
            next_action = "Run daily decision chain before using any market signal."
        elif not board_rows:
            status = "PARTIAL_OUTPUTS"
            next_action = "Daily board is missing; do not use prelock/live outputs as picks."
        else:
            status = "PANEL_ONLY"
            next_action = "Operator brief missing; panel summarizes available files only."
    elif action == "BROKEN" or final == "SYSTEM_FIX_REQUIRED" or health == "BROKEN":
        status = "BROKEN"
        next_action = "Fix workflow/input before market discussion."
    else:
        status = action
        next_action = "Follow operator brief and panel categories; no automatic execution."

    detail = f"action={action}; final={final}; risk={risk}; health={health}"
    lines = [
        f"- action_level: {action}",
        f"- compact_final_decision: {final}",
        f"- risk_label: {risk}",
        f"- health_status: {health}",
        f"- panel_status: {status}",
        f"- next_action: {next_action}",
    ]
    return status, detail, lines


def add_panel_row(rows: list[dict[str, str]], day: str, generated: str, section: str, status: str, detail: str, next_action: str) -> None:
    rows.append(
        {
            "target_date": day,
            "generated_at": generated,
            "section": section,
            "status": status,
            "detail": detail,
            "next_action": next_action,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    )


def md_section(title: str, lines: list[str]) -> list[str]:
    out = ["", f"## {title}"]
    out.extend(lines if lines else ["- none"])
    return out


def build(day: str, tz: str) -> tuple[list[dict[str, str]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = ROOT / "today" / day
    governance = ROOT / "governance"

    board_rows = read_csv(folder / "vsigma_daily_execution_board.csv")
    prelock_rows = read_csv(folder / "vsigma_prelock_live_recheck.csv")
    live_rows = read_csv(folder / "vsigma_live_trigger_validator.csv")
    governor_rows = read_csv(folder / "vsigma_probable_lineup_source_reliability_governor.csv") or read_csv(governance / "vsigma_probable_lineup_source_reliability_governor.csv")

    health_text = read_text(folder / "vsigma_automation_health.md")
    operator_text = read_text(folder / "vsigma_operator_brief.md")
    governor_text = read_text(folder / "vsigma_probable_lineup_source_reliability_governor.md") or read_text(governance / "vsigma_probable_lineup_source_reliability_governor.md")

    operator_status, operator_detail, operator_lines = operator_summary(operator_text, health_text, board_rows, prelock_rows, live_rows)

    executable = top_rows(board_rows, EXECUTABLE_DECISIONS, limit=8)
    live_only = merge_live_rows(board_rows, prelock_rows, live_rows)[:8]
    watchlist = top_rows(board_rows, WATCH_DECISIONS, limit=10)
    no_bet = top_rows(board_rows, NO_BET_DECISIONS, limit=12)

    if not executable and not board_rows:
        executable_status = "NO_BOARD"
        executable_detail = "daily execution board missing"
    elif not executable:
        executable_status = "NONE"
        executable_detail = "no prematch executable rows"
    else:
        executable_status = f"ROWS={len(executable)}"
        executable_detail = "; ".join(row_line(row, include_status=True) for row in executable[:3])

    if not live_only:
        live_status = "NONE"
        live_detail = "no live-only rows"
    else:
        live_status = f"ROWS={len(live_only)}"
        live_detail = "; ".join(row_line(row, include_status=True) for row in live_only[:4])

    if not watchlist:
        watch_status = "NONE"
        watch_detail = "no watchlist rows"
    else:
        watch_status = f"ROWS={len(watchlist)}"
        watch_detail = f"top={'; '.join(row_line(row, include_status=True) for row in watchlist[:3])}"

    if not no_bet:
        no_bet_status = "NONE"
        no_bet_detail = "no no-bet rows"
    else:
        no_bet_status = f"ROWS={len(no_bet)}"
        no_bet_detail = f"count={len(no_bet)}; top={'; '.join(row_line(row, include_status=True) for row in no_bet[:3])}"

    coverage_detail, coverage_lines = extract_coverage(board_rows)
    reliability_detail, reliability_lines = source_reliability_summary(governor_rows, governor_text)
    lineup_detail, lineup_lines = lineup_summary(folder, governance)
    trigger_detail, trigger_lines = next_triggers_summary()

    health_status = meta(health_text, "system_status") if health_text else ("MISSING" if operator_status not in {"WAIT_DAILY_CHAIN"} else "WAIT_DAILY_CHAIN")
    health_detail = (
        f"system_status={health_status}; components={meta(health_text, 'components_checked')}; "
        f"severity={meta(health_text, 'severity_counts')}; status_counts={meta(health_text, 'status_counts')}"
        if health_text
        else "automation health report unavailable"
    )

    rows: list[dict[str, str]] = []
    add_panel_row(rows, day, generated, "operator_gate", operator_status, operator_detail, "Use this as the first read; never override BROKEN/NO_BET gates.")
    add_panel_row(rows, day, generated, "executable_prematch", executable_status, executable_detail, "Only rows here can be discussed as prematch executable, still manual-only.")
    add_panel_row(rows, day, generated, "live_only", live_status, live_detail, "Wait for live trigger confirmation; no chase outside window.")
    add_panel_row(rows, day, generated, "watchlist", watch_status, watch_detail, "Observation only unless promoted by later gates.")
    add_panel_row(rows, day, generated, "no_bet", no_bet_status, no_bet_detail, "Do not fill ranking from blocked rows.")
    add_panel_row(rows, day, generated, "api_coverage", "OK" if board_rows else "MISSING_BOARD", coverage_detail, "Coverage gaps block promotion; do not infer missing data.")
    add_panel_row(rows, day, generated, "official_probable_lineups", "OK" if "NO_LINEUP_FILES" not in lineup_detail else "MISSING_OR_NOT_DUE", lineup_detail, "Probables do not become official; quarantine/learning-only stays non-execution.")
    add_panel_row(rows, day, generated, "source_reliability_governor", "ADVISORY_ONLY" if reliability_detail != "UNAVAILABLE" else "UNAVAILABLE", reliability_detail, "Advisory only; no automatic source weight changes.")
    add_panel_row(rows, day, generated, "automation_health", health_status, health_detail, "If BROKEN, fix workflow/input before talking picks.")
    add_panel_row(rows, day, generated, "next_triggers_rechecks", "DIAGNOSTIC", trigger_detail, "Use scheduled workflows or trigger bridge; no betting execution.")

    md = [f"# vSIGMA Consolidated Daily Operator Panel - {day}", ""]
    md += [
        "## First Read",
        f"- panel_status: {operator_status}",
        f"- operator_detail: {operator_detail}",
        f"- executable_prematch: {executable_status}",
        f"- live_only: {live_status}",
        f"- watchlist: {watch_status}",
        f"- no_bet: {no_bet_status}",
        f"- health_status: {health_status}",
        "- auto_apply: NO",
        "- production_change: NO",
    ]

    md += md_section("Operator Gate", operator_lines)
    md += md_section("Executable Prematch", [f"- {row_line(row)}" for row in executable] if executable else ["- none"])
    md += md_section("Live Only", [f"- {row_line(row)}" for row in live_only] if live_only else ["- none"])
    md += md_section("Watchlist", [f"- {row_line(row)}" for row in watchlist] if watchlist else ["- none"])
    md += md_section("No Bet", [f"- {row_line(row)}" for row in no_bet] if no_bet else ["- none"])
    md += md_section("API Coverage", coverage_lines)
    md += md_section("Official / Probable Lineups", lineup_lines)
    md += md_section("Quarantine / Learning-Only / Import Status", lineup_lines)
    md += md_section("Source Reliability Governor", reliability_lines)
    md += md_section("Automation Health", [
        f"- system_status: {health_status}",
        f"- components_checked: {meta(health_text, 'components_checked') if health_text else 'UNKNOWN'}",
        f"- severity_counts: {meta(health_text, 'severity_counts') if health_text else 'UNKNOWN'}",
        f"- status_counts: {meta(health_text, 'status_counts') if health_text else 'UNKNOWN'}",
    ])
    md += md_section("Next Triggers / Rechecks", trigger_lines)
    md += md_section("Key Files", [
        f"- {folder / 'vsigma_consolidated_daily_operator_panel.md'}",
        f"- {folder / 'vsigma_operator_brief.md'}",
        f"- {folder / 'vsigma_daily_execution_board.md'}",
        f"- {folder / 'vsigma_prelock_live_recheck.md'}",
        f"- {folder / 'vsigma_live_trigger_validator.md'}",
        f"- {folder / 'vsigma_automation_health.md'}",
        f"- {folder / 'vsigma_probable_lineup_source_reliability_governor.md'}",
    ])
    md += md_section("Guardrails", [
        "- Panel is diagnostic only; it does not execute bets.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
        "- No Bet, Watch, Live Only, Learning Only and Quarantine are valid successful outcomes.",
        "- Source Reliability Governor remains advisory-only and cannot change weights by itself.",
        "- If the daily board is missing, prelock/live files cannot be used as pick permission.",
    ])

    return rows, "\n".join(md) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, panel = build(day, tz)
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write_csv(base / "vsigma_consolidated_daily_operator_panel.csv", rows)
        write_text(base / "vsigma_consolidated_daily_operator_panel.md", panel)

    status = next((row["status"] for row in rows if row.get("section") == "operator_gate"), "UNKNOWN")
    live = next((row["status"] for row in rows if row.get("section") == "live_only"), "UNKNOWN")
    executable = next((row["status"] for row in rows if row.get("section") == "executable_prematch"), "UNKNOWN")
    health = next((row["status"] for row in rows if row.get("section") == "automation_health"), "UNKNOWN")
    print("=== VSIGMA CONSOLIDATED DAILY OPERATOR PANEL ===")
    print(f"operator_gate={status}")
    print(f"executable_prematch={executable}")
    print(f"live_only={live}")
    print(f"automation_health={health}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
