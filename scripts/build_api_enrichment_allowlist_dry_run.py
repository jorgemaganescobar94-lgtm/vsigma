from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league",
    "quota_policy_decision", "planned_mode", "allowlist_status", "allowlist_mode",
    "quota_units_reserved", "external_calls_executed", "allowlist_reason", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "allowlist_status", "rows_reviewed", "allowlisted_rows",
    "full_enrichment_dry_rows", "coverage_probe_dry_rows", "blocked_rows", "quota_units_reserved",
    "allowlist_status_counts", "external_calls_executed", "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0


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


def load_quota_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_quota_aware_enrichment_gate.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_quota_aware_enrichment_gate.csv")
    return rows


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    decision = up(row.get("quota_policy_decision"))
    allowed = up(row.get("api_calls_allowed"))
    if decision == "AUTO_ENRICHMENT_ALLOWED_P1" and allowed.startswith("YES"):
        return "ALLOWLISTED_DRY_RUN", "P1_FULL_ENRICHMENT_PLAN", "P1 is quota-allowed; this plan remains dry-run only."
    if decision == "COVERAGE_PROBE_ALLOWED_P2" and allowed.startswith("YES"):
        return "ALLOWLISTED_DRY_RUN", "P2_COVERAGE_PROBE_PLAN", "P2 is quota-allowed for coverage probe only; this plan remains dry-run only."
    return "BLOCKED_BY_POLICY", "NO_ACTION", "Row is not allowlisted by quota/risk policy."


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    out = []
    for row in load_quota_rows(processed, day):
        status, mode, reason = classify(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "quota_policy_decision": norm(row.get("quota_policy_decision")),
            "planned_mode": norm(row.get("planned_mode")),
            "allowlist_status": status,
            "allowlist_mode": mode,
            "quota_units_reserved": as_int(row.get("quota_units_reserved")),
            "external_calls_executed": "NO",
            "allowlist_reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    allowlisted = [r for r in out if r["allowlist_status"] == "ALLOWLISTED_DRY_RUN"]
    full = [r for r in out if r["allowlist_mode"] == "P1_FULL_ENRICHMENT_PLAN"]
    probe = [r for r in out if r["allowlist_mode"] == "P2_COVERAGE_PROBE_PLAN"]
    blocked = [r for r in out if r["allowlist_status"] == "BLOCKED_BY_POLICY"]
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "allowlist_status": "ALLOWLIST_DRY_RUN_READY" if out else "NO_QUOTA_GATE_ROWS",
        "rows_reviewed": len(out),
        "allowlisted_rows": len(allowlisted),
        "full_enrichment_dry_rows": len(full),
        "coverage_probe_dry_rows": len(probe),
        "blocked_rows": len(blocked),
        "quota_units_reserved": sum(as_int(r.get("quota_units_reserved")) for r in allowlisted),
        "allowlist_status_counts": counts(out, "allowlist_mode"),
        "external_calls_executed": "NO",
        "next_action": "Review allowlist. A separate approved enrichment step is required before external calls.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{k}={v}" for k, v in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API Enrichment Allowlist Dry Run - {day}",
        "",
        "## Summary",
        f"- allowlist_status: {summary['allowlist_status']}",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- allowlisted_rows: {summary['allowlisted_rows']}",
        f"- full_enrichment_dry_rows: {summary['full_enrichment_dry_rows']}",
        f"- coverage_probe_dry_rows: {summary['coverage_probe_dry_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- quota_units_reserved: {summary['quota_units_reserved']}",
        f"- allowlist_status_counts: {summary['allowlist_status_counts']}",
        "- external_calls_executed: NO",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Rows",
    ]
    for row in rows[:120]:
        lines.append(f"- {row['home_team']} vs {row['away_team']} | {row['allowlist_mode']} | status={row['allowlist_status']} | calls=NO")
    lines += ["", "## Guardrails", "- Dry-run only.", "- No external calls are made.", "- No pick or stake permission is created."]
    return "\n".join(lines) + "\n"


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    lines = [
        "## API Enrichment Allowlist Dry Run",
        f"- allowlist_status: {summary.get('allowlist_status', 'UNKNOWN')}",
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- allowlisted_rows: {summary.get('allowlisted_rows', 'UNKNOWN')}",
        f"- full_enrichment_dry_rows: {summary.get('full_enrichment_dry_rows', 'UNKNOWN')}",
        f"- coverage_probe_dry_rows: {summary.get('coverage_probe_dry_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- quota_units_reserved: {summary.get('quota_units_reserved', 'UNKNOWN')}",
        f"- external_calls_executed: {summary.get('external_calls_executed', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            section = "## API Enrichment Allowlist Dry Run"
            block = "\n" + "\n".join(lines) + "\n"
            if section not in text:
                md_path.write_text(text.rstrip() + block, encoding="utf-8")


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_enrichment_allowlist_dry_run.csv", rows, FIELDS)
        write_csv(base / "vsigma_api_enrichment_allowlist_dry_run_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_enrichment_allowlist_dry_run.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API ENRICHMENT ALLOWLIST DRY RUN ===")
    print(f"allowlist_status={summary[0]['allowlist_status']}")
    print(f"allowlisted_rows={summary[0]['allowlisted_rows']}")
    print(f"external_calls_executed={summary[0]['external_calls_executed']}")
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
