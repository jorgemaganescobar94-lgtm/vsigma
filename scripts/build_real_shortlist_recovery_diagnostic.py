from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

SOURCES = [
    ("root_scored_matches", "data/processed/matches_vsigma_scored_v3.csv", "SCORING", True),
    ("dated_scored_matches", "data/processed/today/{day}/matches_vsigma_scored_v3.csv", "SCORING", False),
    ("today_execution_shortlist", "data/processed/today/{day}/vsigma_today_execution_shortlist.csv", "SHORTLIST", True),
    ("today_execution_bets_only", "data/processed/today/{day}/vsigma_today_execution_bets_only.csv", "BETS", True),
    ("context_adjusted_final_picks", "data/processed/today/{day}/vsigma_context_adjusted_final_picks.csv", "ADJUSTED", True),
    ("real_objective_context_gate", "data/processed/today/{day}/vsigma_real_objective_context_gate.csv", "OBJECTIVE_PROXY", False),
    ("objective_context_execution_bridge", "data/processed/today/{day}/vsigma_objective_context_execution_bridge.csv", "OBJECTIVE_PROXY", False),
    ("candidate_provenance_ledger", "data/processed/today/{day}/vsigma_candidate_provenance_ledger.csv", "PROVENANCE", False),
]

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "component",
    "component_type",
    "path",
    "exists",
    "total_rows",
    "same_day_rows",
    "real_rows",
    "proxy_rows",
    "bet_like_rows",
    "blocked_rows",
    "status_counts",
    "diagnostic_status",
    "detail",
    "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "overall_status",
    "root_cause",
    "root_scored_same_day_rows",
    "real_shortlist_rows",
    "real_bet_rows",
    "proxy_rows",
    "next_action",
    "auto_apply",
    "production_change",
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


def row_day(row: dict[str, str]) -> str:
    for field in ("target_date", "date", "fixture_datetime_utc"):
        value = norm(row.get(field))[:10]
        if value:
            return value
    return ""


def same_day(rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    return [row for row in rows if row_day(row) in {"", day}]


def is_proxy(row: dict[str, str]) -> bool:
    marker = " ".join(
        [
            up(row.get("bridge_source")),
            up(row.get("guardrail_status")),
            up(row.get("candidate_origin")),
            up(row.get("allowed_downstream_use")),
        ]
    )
    return "OBJECTIVE_PROXY" in marker or "BASE_PROXY_FROM_OBJECTIVE_GATE" in marker or "DIAGNOSTIC_ONLY" in marker


def is_bet_like(row: dict[str, str]) -> bool:
    fields = [
        "final_recommendation",
        "base_final_recommendation",
        "adjusted_final_status",
        "execution_permission",
        "final_decision",
        "recommended_action",
    ]
    joined = " ".join(up(row.get(field)) for field in fields)
    if "NO_BET" in joined or "NO_STAKE" in joined or "BLOCK" in joined:
        return False
    return any(token in joined for token in ["BET", "REVIEW", "LIVE_ONLY", "STAT_WATCH"])


def is_blocked(row: dict[str, str]) -> bool:
    joined = " ".join(up(v) for v in row.values())
    return any(token in joined for token in ["NO_BET", "NO_STAKE", "BLOCKED", "MAX_BLOCK", "HARD_DOWN"])


def status_counts(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "none"
    fields = [
        "final_recommendation",
        "execution_verdict",
        "adjusted_final_status",
        "execution_permission",
        "final_decision",
        "candidate_origin",
        "max_execution_permission",
        "guardrail_status",
    ]
    parts: list[str] = []
    available = set(rows[0].keys())
    for field in fields:
        if field not in available:
            continue
        counter = Counter(up(row.get(field)) or "BLANK" for row in rows)
        parts.append(field + ":" + ";".join(f"{key}={value}" for key, value in counter.most_common(8)))
    return " | ".join(parts) if parts else "none"


def component_status(exists: bool, rows: list[dict[str, str]], same: list[dict[str, str]], real_rows: int, proxy_rows: int, component_type: str) -> tuple[str, str]:
    if not exists:
        return "MISSING", "file is not present"
    if not rows:
        return "EMPTY", "file exists but has no data rows"
    if not same:
        return "NO_SAME_DAY_ROWS", "file has rows but none for target date"
    if component_type in {"SHORTLIST", "BETS", "ADJUSTED"} and real_rows == 0 and proxy_rows > 0:
        return "PROXY_ONLY", "same-day rows exist but are proxy/diagnostic only"
    if component_type in {"SHORTLIST", "BETS", "ADJUSTED"} and real_rows == 0:
        return "NO_REAL_ROWS", "same-day rows exist but no real executable/source rows"
    return "HAS_REAL_ROWS" if real_rows else "HAS_ROWS", "file has same-day rows"


def analyse(day: str, tz: str) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows_out: list[dict[str, object]] = []
    metrics = {
        "root_scored_same_day_rows": 0,
        "real_shortlist_rows": 0,
        "real_bet_rows": 0,
        "proxy_rows": 0,
    }

    for component, template, component_type, real_source_candidate in SOURCES:
        path = Path(template.format(day=day))
        exists = path.exists()
        rows = read_rows(path)
        same = same_day(rows, day)
        proxy_count = sum(1 for row in same if is_proxy(row))
        real_count = len(same) - proxy_count if real_source_candidate else 0
        bet_like = sum(1 for row in same if is_bet_like(row))
        blocked = sum(1 for row in same if is_blocked(row))
        status, detail = component_status(exists, rows, same, real_count, proxy_count, component_type)

        if component == "root_scored_matches":
            metrics["root_scored_same_day_rows"] = len(same)
        if component in {"today_execution_shortlist", "context_adjusted_final_picks"}:
            metrics["real_shortlist_rows"] += real_count
        if component == "today_execution_bets_only":
            metrics["real_bet_rows"] += real_count
        metrics["proxy_rows"] += proxy_count

        rows_out.append(
            {
                "target_date": day,
                "generated_at": generated_at,
                "component": component,
                "component_type": component_type,
                "path": str(path),
                "exists": str(exists).lower(),
                "total_rows": len(rows),
                "same_day_rows": len(same),
                "real_rows": real_count,
                "proxy_rows": proxy_count,
                "bet_like_rows": bet_like,
                "blocked_rows": blocked,
                "status_counts": status_counts(same),
                "diagnostic_status": status,
                "detail": detail,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )

    overall, root_cause, next_action = decide(metrics, rows_out)
    summary = [
        {
            "target_date": day,
            "generated_at": generated_at,
            "overall_status": overall,
            "root_cause": root_cause,
            "root_scored_same_day_rows": metrics["root_scored_same_day_rows"],
            "real_shortlist_rows": metrics["real_shortlist_rows"],
            "real_bet_rows": metrics["real_bet_rows"],
            "proxy_rows": metrics["proxy_rows"],
            "next_action": next_action,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    ]
    return rows_out, summary, md(day, rows_out, summary[0])


def decide(metrics: dict[str, int], components: list[dict[str, object]]) -> tuple[str, str, str]:
    root_status = next((str(row["diagnostic_status"]) for row in components if row["component"] == "root_scored_matches"), "MISSING")
    shortlist_status = next((str(row["diagnostic_status"]) for row in components if row["component"] == "today_execution_shortlist"), "MISSING")
    bets_status = next((str(row["diagnostic_status"]) for row in components if row["component"] == "today_execution_bets_only"), "MISSING")

    if metrics["real_shortlist_rows"] > 0 or metrics["real_bet_rows"] > 0:
        return "REAL_CANDIDATES_AVAILABLE", "real shortlist or bets rows exist", "Use normal gates; do not rely on proxy bridge unless real rows fail downstream."
    if root_status == "MISSING":
        return "SCORING_SOURCE_MISSING", "matches_vsigma_scored_v3.csv missing", "Run scoring/enrichment chain before candidate selection."
    if metrics["root_scored_same_day_rows"] == 0:
        return "SCORING_SOURCE_EMPTY_FOR_DATE", "scored source exists but has no rows for target date", "Refresh/fix scoring source date coverage."
    if shortlist_status in {"EMPTY", "MISSING"} and bets_status in {"EMPTY", "MISSING"}:
        return "FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN", "scoring has same-day rows but real shortlist/bets outputs are absent or empty", "Run/repair real selection step from scored matches into shortlist/bets-only outputs."
    if metrics["proxy_rows"] > 0 and metrics["real_shortlist_rows"] == 0:
        return "SHORTLIST_PROXY_ONLY", "only proxy rows are available downstream", "Recover real shortlist source; keep proxy rows capped at NO_BET."
    return "NO_REAL_CANDIDATES", "no real candidate rows survived current filters", "Inspect selection thresholds and source coverage before any market discussion."


def md(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Real Shortlist Recovery Diagnostic - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- root_cause: {summary['root_cause']}",
        f"- root_scored_same_day_rows: {summary['root_scored_same_day_rows']}",
        f"- real_shortlist_rows: {summary['real_shortlist_rows']}",
        f"- real_bet_rows: {summary['real_bet_rows']}",
        f"- proxy_rows: {summary['proxy_rows']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Component Rows",
    ]
    for row in rows:
        lines.append(
            f"- {row['component']} | status={row['diagnostic_status']} | same_day={row['same_day_rows']} | real={row['real_rows']} | proxy={row['proxy_rows']} | bet_like={row['bet_like_rows']} | path={row['path']} | detail={row['detail']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This diagnostic never creates picks or stake permission.",
        "- Real candidate recovery must come from scored/selection outputs, not from proxy bridge rows.",
        "- Proxy-only availability remains NO_BET through provenance ceiling.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = analyse(day, tz)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_real_shortlist_recovery_diagnostic.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_real_shortlist_recovery_diagnostic_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_real_shortlist_recovery_diagnostic.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA REAL SHORTLIST RECOVERY DIAGNOSTIC ===")
    print(f"overall_status={summary[0]['overall_status']}")
    print(f"root_cause={summary[0]['root_cause']}")
    print(f"real_shortlist_rows={summary[0]['real_shortlist_rows']}")
    print(f"real_bet_rows={summary[0]['real_bet_rows']}")
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
