from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
LEDGER_STAT_CALIBRATION = PROCESSED / "ledger" / "vsigma_stat_calibration_memory.csv"

FIELDS = [
    "target_date",
    "generated_at",
    "component",
    "path",
    "rows_count",
    "fallback_path",
    "fallback_rows",
    "sanity_status",
    "severity",
    "recommended_action",
    "detail",
    "source_guard",
    "auto_apply",
    "production_change",
]


def n(value: object) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def rows_for_date(path: Path, day: str) -> list[dict[str, str]]:
    rows = read_csv(path)
    if not rows:
        return []
    if "target_date" not in rows[0]:
        return rows
    return [row for row in rows if n(row.get("target_date")) == day]


def row_count(path: Path) -> int:
    return len(read_csv(path))


def ledger_rows(day: str) -> int:
    return len(rows_for_date(LEDGER_STAT_CALIBRATION, day))


def add_row(
    rows: list[dict[str, object]],
    day: str,
    generated_at: str,
    component: str,
    path: Path,
    fallback_path: Path | None = None,
    expected_when_fallback: bool = False,
) -> None:
    count = row_count(path)
    fallback_count = len(rows_for_date(fallback_path, day)) if fallback_path else 0

    if count > 0:
        status = "PASS"
        severity = "OK"
        action = "NO_ACTION"
        detail = "Output has data rows."
    elif expected_when_fallback and fallback_count > 0:
        status = "EMPTY_WITH_VALID_FALLBACK"
        severity = "WARN"
        action = "USE_FALLBACK_OR_RERUN_CHAIN"
        detail = "Output is empty, but same-date fallback rows exist."
    elif fallback_count > 0:
        status = "EMPTY_BUT_NONCRITICAL_FALLBACK_EXISTS"
        severity = "INFO"
        action = "MONITOR"
        detail = "Output is empty while fallback rows exist; not marked critical for this component."
    else:
        status = "EMPTY_NO_FALLBACK"
        severity = "WARN"
        action = "REVIEW_SOURCE_CHAIN"
        detail = "Output has no rows and no same-date fallback rows were found."

    rows.append({
        "target_date": day,
        "generated_at": generated_at,
        "component": component,
        "path": str(path),
        "rows_count": count,
        "fallback_path": str(fallback_path) if fallback_path else "",
        "fallback_rows": fallback_count,
        "sanity_status": status,
        "severity": severity,
        "recommended_action": action,
        "detail": detail,
        "source_guard": "SANITY_DIAGNOSTIC_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    })


def build(day: str, tz: str) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows: list[dict[str, object]] = []

    add_row(
        rows,
        day,
        generated_at,
        "post_match_actuals",
        dated(day, "vsigma_post_match_stat_actuals.csv"),
    )
    add_row(
        rows,
        day,
        generated_at,
        "forecast_calibration_summary",
        dated(day, "vsigma_match_stat_forecast_calibration_summary.csv"),
        LEDGER_STAT_CALIBRATION,
        expected_when_fallback=True,
    )
    add_row(
        rows,
        day,
        generated_at,
        "forecast_backtest",
        dated(day, "vsigma_match_stat_forecast_backtest.csv"),
    )
    add_row(
        rows,
        day,
        generated_at,
        "stat_calibration_governor",
        dated(day, "vsigma_stat_calibration_governor.csv"),
        LEDGER_STAT_CALIBRATION,
        expected_when_fallback=True,
    )
    add_row(
        rows,
        day,
        generated_at,
        "calibration_shadow_patch_queue",
        dated(day, "vsigma_calibration_shadow_patch_queue.csv"),
        LEDGER_STAT_CALIBRATION,
        expected_when_fallback=True,
    )
    add_row(
        rows,
        day,
        generated_at,
        "shadow_patch_promotion_readiness",
        dated(day, "vsigma_shadow_patch_promotion_readiness.csv"),
        dated(day, "vsigma_calibration_shadow_patch_queue.csv"),
        expected_when_fallback=True,
    )

    rows.append({
        "target_date": day,
        "generated_at": generated_at,
        "component": "stat_calibration_memory_ledger",
        "path": str(LEDGER_STAT_CALIBRATION),
        "rows_count": ledger_rows(day),
        "fallback_path": "",
        "fallback_rows": 0,
        "sanity_status": "PASS" if ledger_rows(day) > 0 else "EMPTY_NO_FALLBACK",
        "severity": "OK" if ledger_rows(day) > 0 else "WARN",
        "recommended_action": "NO_ACTION" if ledger_rows(day) > 0 else "REVIEW_LEDGER_BUILD",
        "detail": "Same-date ledger rows available." if ledger_rows(day) > 0 else "No same-date ledger rows found.",
        "source_guard": "SANITY_DIAGNOSTIC_ONLY",
        "auto_apply": "NO",
        "production_change": "NO",
    })
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def md(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Learning Chain Output Sanity Check - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- sanity_status_counts: {counts(rows, 'sanity_status')}",
        f"- severity_counts: {counts(rows, 'severity')}",
        f"- actions: {counts(rows, 'recommended_action')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Component Checks",
    ]
    if not rows:
        lines.append("- none")
    for row in rows:
        lines.append(
            "- "
            f"{row['component']} | status={row['sanity_status']} | severity={row['severity']} | "
            f"rows={row['rows_count']} | fallback_rows={row['fallback_rows']} | action={row['recommended_action']} | "
            f"detail={row['detail']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This sanity check is diagnostic only.",
        "- It does not delete, overwrite, or auto-fix model outputs.",
        "- Empty outputs with same-date fallback rows should be regenerated or read through fallback-safe scripts.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_learning_chain_output_sanity.csv", rows)
        (base / "vsigma_learning_chain_output_sanity.md").write_text(md(day, rows), encoding="utf-8")
    print("=== VSIGMA LEARNING CHAIN OUTPUT SANITY ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"sanity_status_counts={counts(rows, 'sanity_status')}")
    print(f"severity_counts={counts(rows, 'severity')}")
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
