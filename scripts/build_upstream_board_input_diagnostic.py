from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")
TODAY = ROOT / "today"
GOVERNANCE = ROOT / "governance"

INPUTS = [
    ("real_objective_context_gate", "vsigma_real_objective_context_gate.csv", True),
    ("objective_availability_gate", "vsigma_objective_availability_gate.csv", True),
    ("context_adjusted_final_picks", "vsigma_context_adjusted_final_picks.csv", True),
    ("context_matrix", "vsigma_context_matrix.csv", True),
    ("context_matrix_portfolio", "vsigma_context_matrix_portfolio.csv", True),
    ("match_stat_forecasts", "vsigma_match_stat_forecasts.csv", True),
    ("forecast_market_translator", "vsigma_forecast_market_translator.csv", True),
    ("daily_execution_board", "vsigma_daily_execution_board.csv", True),
    ("fixture_api_coverage_matrix", "vsigma_fixture_api_coverage_matrix_v3.csv", False),
    ("probable_lineup_consensus", "vsigma_probable_lineup_consensus.csv", False),
]

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "component",
    "path",
    "exists",
    "row_count",
    "date_status",
    "decision_counts",
    "quality_counts",
    "status",
    "detail",
    "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "overall_status",
    "first_empty_required_component",
    "missing_required_count",
    "empty_required_count",
    "date_issue_count",
    "board_rows",
    "translator_rows",
    "forecast_rows",
    "next_action",
    "auto_apply",
    "production_change",
]

DATE_FIELDS = ["target_date", "date", "match_date"]
DECISION_FIELDS = [
    "final_decision",
    "board_bucket",
    "base_decision",
    "recheck_decision",
    "market_decision",
    "portfolio_status",
    "execution_permission",
]
QUALITY_FIELDS = [
    "forecast_confidence",
    "context_level",
    "source_guard",
    "gate_decision",
    "kill_switch",
    "forecast_warning",
    "quality_status",
    "status",
]


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def count_field(rows: list[dict[str, str]], fields: list[str]) -> str:
    counts: list[str] = []
    if not rows:
        return "none"
    available = set(rows[0].keys())
    for field in fields:
        if field not in available:
            continue
        counter = Counter(clean(row.get(field)) or "BLANK" for row in rows)
        counts.append(f"{field}:" + ";".join(f"{k}={v}" for k, v in counter.most_common(8)))
    return " | ".join(counts) if counts else "none"


def detect_date_status(rows: list[dict[str, str]], day: str) -> str:
    if not rows:
        return "NO_ROWS"
    available = set(rows[0].keys())
    date_fields = [field for field in DATE_FIELDS if field in available]
    if not date_fields:
        return "NO_DATE_FIELD"
    values = set()
    for field in date_fields:
        for row in rows:
            value = clean(row.get(field))
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                values.add(value)
    if not values:
        return "DATE_UNKNOWN"
    if values == {day}:
        return "OK"
    return "DATE_MISMATCH:" + ";".join(sorted(values))


def component_status(name: str, required: bool, exists: bool, row_count: int, date_status: str) -> tuple[str, str]:
    if not exists:
        if required:
            return "MISSING_REQUIRED", "required upstream file is missing"
        return "MISSING_OPTIONAL", "optional upstream file is missing"
    if row_count == 0:
        if required:
            return "EMPTY_REQUIRED", "required upstream file exists but has zero rows"
        return "EMPTY_OPTIONAL", "optional upstream file has zero rows"
    if date_status.startswith("DATE_MISMATCH"):
        return "DATE_MISMATCH", date_status
    if date_status in {"DATE_UNKNOWN"}:
        return "DATE_UNKNOWN", "file has rows but no parseable target date"
    if date_status == "NO_DATE_FIELD":
        return "DATE_NOT_DECLARED", "file has rows but no explicit date field"
    return "OK", "file has rows and passed basic diagnostic checks"


def build(day: str, tz: str) -> tuple[list[dict[str, str]], list[dict[str, str]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = TODAY / day
    rows: list[dict[str, str]] = []

    metrics = {
        "missing_required_count": 0,
        "empty_required_count": 0,
        "date_issue_count": 0,
        "board_rows": 0,
        "translator_rows": 0,
        "forecast_rows": 0,
    }
    first_empty_required = "none"

    for component, filename, required in INPUTS:
        path = folder / filename
        file_exists = path.exists()
        data = read_csv(path)
        row_count = len(data)
        date_status = detect_date_status(data, day) if file_exists else "MISSING"
        status, detail = component_status(component, required, file_exists, row_count, date_status)
        if required and status == "MISSING_REQUIRED":
            metrics["missing_required_count"] += 1
            if first_empty_required == "none":
                first_empty_required = component
        if required and status == "EMPTY_REQUIRED":
            metrics["empty_required_count"] += 1
            if first_empty_required == "none":
                first_empty_required = component
        if status in {"DATE_MISMATCH", "DATE_UNKNOWN"}:
            metrics["date_issue_count"] += 1
        if component == "daily_execution_board":
            metrics["board_rows"] = row_count
        if component == "forecast_market_translator":
            metrics["translator_rows"] = row_count
        if component == "match_stat_forecasts":
            metrics["forecast_rows"] = row_count

        rows.append(
            {
                "target_date": day,
                "generated_at": generated,
                "component": component,
                "path": str(path),
                "exists": str(file_exists).lower(),
                "row_count": str(row_count),
                "date_status": date_status,
                "decision_counts": count_field(data, DECISION_FIELDS),
                "quality_counts": count_field(data, QUALITY_FIELDS),
                "status": status,
                "detail": detail,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )

    overall, next_action = overall_status(metrics, first_empty_required)
    summary = [
        {
            "target_date": day,
            "generated_at": generated,
            "overall_status": overall,
            "first_empty_required_component": first_empty_required,
            "missing_required_count": str(metrics["missing_required_count"]),
            "empty_required_count": str(metrics["empty_required_count"]),
            "date_issue_count": str(metrics["date_issue_count"]),
            "board_rows": str(metrics["board_rows"]),
            "translator_rows": str(metrics["translator_rows"]),
            "forecast_rows": str(metrics["forecast_rows"]),
            "next_action": next_action,
            "auto_apply": "NO",
            "production_change": "NO",
        }
    ]
    return rows, summary, md(day, rows, summary[0])


def overall_status(metrics: dict[str, int], first_empty_required: str) -> tuple[str, str]:
    if metrics["date_issue_count"]:
        return "UPSTREAM_DATE_REVIEW", "Fix upstream date issues before interpreting board output."
    if metrics["missing_required_count"]:
        return "UPSTREAM_MISSING", f"Build missing required upstream component first: {first_empty_required}."
    if metrics["empty_required_count"]:
        if first_empty_required == "match_stat_forecasts":
            return "FORECAST_EMPTY", "Investigate fixture/stat forecast source; translator and board cannot populate without forecasts."
        if first_empty_required == "forecast_market_translator":
            return "TRANSLATOR_EMPTY", "Forecasts exist but translator is empty; inspect market translation inputs/gates."
        if first_empty_required == "daily_execution_board":
            if metrics["translator_rows"] > 0:
                return "BOARD_EMPTY_BUT_TRANSLATOR_HAS_ROWS", "Board is empty despite translator rows; inspect board thresholds/gates."
            return "BOARD_EMPTY_EXPECTED_NO_CANDIDATES", "Board is empty and translator has no rows; no candidates reached board."
        return "UPSTREAM_EMPTY", f"Required upstream component is empty: {first_empty_required}."
    if metrics["board_rows"] == 0:
        if metrics["translator_rows"] > 0:
            return "BOARD_EMPTY_BUT_TRANSLATOR_HAS_ROWS", "Board is empty despite translator rows; inspect board thresholds/gates."
        return "BOARD_EMPTY_EXPECTED_NO_CANDIDATES", "No translated candidates reached board; No Bet remains valid."
    return "OK", "Upstream inputs and board contain rows; use panel/operator gates."


def md(day: str, rows: list[dict[str, str]], summary: dict[str, str]) -> str:
    lines = [
        f"# vSIGMA Upstream Board Input Diagnostic - {day}",
        "",
        "## Summary",
        f"- overall_status: {summary['overall_status']}",
        f"- first_empty_required_component: {summary['first_empty_required_component']}",
        f"- missing_required_count: {summary['missing_required_count']}",
        f"- empty_required_count: {summary['empty_required_count']}",
        f"- date_issue_count: {summary['date_issue_count']}",
        f"- forecast_rows: {summary['forecast_rows']}",
        f"- translator_rows: {summary['translator_rows']}",
        f"- board_rows: {summary['board_rows']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Component Rows",
    ]
    for row in rows:
        lines.append(
            f"- {row['component']} | status={row['status']} | rows={row['row_count']} | date={row['date_status']} | path={row['path']} | detail={row['detail']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Diagnostic only; this does not execute bets or alter stake permission.",
        "- Empty board is not a pick signal; it is a No Bet / upstream diagnostic state.",
        "- Use this file to locate where the daily chain loses candidates before the board.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, markdown = build(day, tz)
    for base in [TODAY / day, GOVERNANCE]:
        write_csv(base / "vsigma_upstream_board_input_diagnostic.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_upstream_board_input_diagnostic_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_upstream_board_input_diagnostic.md").write_text(markdown, encoding="utf-8")
    print("=== VSIGMA UPSTREAM BOARD INPUT DIAGNOSTIC ===")
    print(f"overall_status={summary[0]['overall_status']}")
    print(f"first_empty_required_component={summary[0]['first_empty_required_component']}")
    print(f"forecast_rows={summary[0]['forecast_rows']}")
    print(f"translator_rows={summary[0]['translator_rows']}")
    print(f"board_rows={summary[0]['board_rows']}")
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
