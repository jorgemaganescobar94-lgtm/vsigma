from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import build_max_coverage_api_enrichment_policy as max_coverage

PROCESSED = Path("data/processed")
TODAY = PROCESSED / "today"
GOVERNANCE = PROCESSED / "governance"

SUMMARY_FIELDS = [
    "target_date", "generated_at", "active_api_policy", "policy_source", "api_plan_name",
    "plan_requests_per_day", "external_calls_allowed", "external_calls_executed",
    "scoring_allowed_rows", "coverage_probe_rows", "diagnostic_only_rows", "blocked_rows",
    "legacy_cost_gate_status", "legacy_quota_gate_status", "legacy_allowlist_status",
    "operator_note", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
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


def load_summary(processed: Path, day: str, name: str) -> dict[str, str]:
    rows = read_csv(processed / "today" / day / name) or read_csv(processed / "governance" / name)
    return rows[0] if rows else {}


def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    max_rows = load_summary(processed, day, "vsigma_max_coverage_api_enrichment_policy_summary.csv")
    cost_rows = load_summary(processed, day, "vsigma_enrichment_cost_approval_gate_summary.csv")
    quota_rows = load_summary(processed, day, "vsigma_api_quota_aware_enrichment_gate_summary.csv")
    allow_rows = load_summary(processed, day, "vsigma_api_enrichment_allowlist_dry_run_summary.csv")

    active = "MAX_COVERAGE" if max_rows.get("policy_status") == "MAX_COVERAGE_POLICY_READY" else "NO_ACTIVE_MAX_COVERAGE_POLICY"
    summary = {
        "target_date": day,
        "generated_at": generated,
        "active_api_policy": active,
        "policy_source": "vsigma_max_coverage_api_enrichment_policy",
        "api_plan_name": max_rows.get("api_plan_name", "UNKNOWN"),
        "plan_requests_per_day": max_rows.get("plan_requests_per_day", "UNKNOWN"),
        "external_calls_allowed": max_rows.get("external_calls_allowed", "NO"),
        "external_calls_executed": max_rows.get("external_calls_executed", "NO"),
        "scoring_allowed_rows": max_rows.get("full_scoring_enrichment_rows", "0"),
        "coverage_probe_rows": max_rows.get("coverage_probe_rows", "0"),
        "diagnostic_only_rows": max_rows.get("diagnostic_only_rows", "0"),
        "blocked_rows": max_rows.get("blocked_rows", "0"),
        "legacy_cost_gate_status": f"LEGACY_INFORMATIONAL_ONLY:{cost_rows.get('approval_gate_status', 'UNKNOWN')}",
        "legacy_quota_gate_status": f"LEGACY_SECONDARY_ONLY:{quota_rows.get('quota_gate_status', 'UNKNOWN')}",
        "legacy_allowlist_status": f"LEGACY_SECONDARY_ONLY:{allow_rows.get('allowlist_status', 'UNKNOWN')}",
        "operator_note": "MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.",
        "auto_apply": "NO",
        "production_change": "NO",
    }
    return [summary], markdown(day, summary)


def markdown(day: str, summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Active Max-Coverage API Policy - {day}",
        "",
        "## Summary",
        f"- active_api_policy: {summary['active_api_policy']}",
        f"- policy_source: {summary['policy_source']}",
        f"- api_plan_name: {summary['api_plan_name']}",
        f"- plan_requests_per_day: {summary['plan_requests_per_day']}",
        f"- external_calls_allowed: {summary['external_calls_allowed']}",
        f"- external_calls_executed: {summary['external_calls_executed']}",
        f"- scoring_allowed_rows: {summary['scoring_allowed_rows']}",
        f"- coverage_probe_rows: {summary['coverage_probe_rows']}",
        f"- diagnostic_only_rows: {summary['diagnostic_only_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- legacy_cost_gate_status: {summary['legacy_cost_gate_status']}",
        f"- legacy_quota_gate_status: {summary['legacy_quota_gate_status']}",
        f"- legacy_allowlist_status: {summary['legacy_allowlist_status']}",
        f"- operator_note: {summary['operator_note']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Guardrails",
        "- This integration only declares which API policy is active.",
        "- It does not execute API calls, create picks, create stake permission, or bypass scoring gates.",
        "- MAX_COVERAGE permits broad API collection, but scoring/picks remain restricted by downstream_use and normal gates.",
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


def update_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    section = "## Active API Policy"
    lines = [
        section,
        f"- active_api_policy: {summary.get('active_api_policy', 'UNKNOWN')}",
        f"- policy_source: {summary.get('policy_source', 'UNKNOWN')}",
        f"- external_calls_allowed: {summary.get('external_calls_allowed', 'UNKNOWN')}",
        f"- external_calls_executed: {summary.get('external_calls_executed', 'UNKNOWN')}",
        f"- scoring_allowed_rows: {summary.get('scoring_allowed_rows', 'UNKNOWN')}",
        f"- coverage_probe_rows: {summary.get('coverage_probe_rows', 'UNKNOWN')}",
        f"- diagnostic_only_rows: {summary.get('diagnostic_only_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- legacy_cost_gate_status: {summary.get('legacy_cost_gate_status', 'UNKNOWN')}",
        f"- legacy_quota_gate_status: {summary.get('legacy_quota_gate_status', 'UNKNOWN')}",
        f"- legacy_allowlist_status: {summary.get('legacy_allowlist_status', 'UNKNOWN')}",
        f"- operator_note: {summary.get('operator_note', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            text = replace_or_append_section(text, section, block)
            md_path.write_text(text, encoding="utf-8")
        csv_path = base / "vsigma_consolidated_daily_operator_panel.csv"
        rows = read_csv(csv_path)
        if rows:
            fields = list(rows[0].keys())
            rows = [row for row in rows if row.get("section") != "active_api_policy"]
            rows.append({
                "target_date": day,
                "generated_at": str(summary.get("generated_at", "")),
                "section": "active_api_policy",
                "status": str(summary.get("active_api_policy", "UNKNOWN")),
                "detail": (
                    f"allowed={summary.get('external_calls_allowed', 'UNKNOWN')}; "
                    f"scoring={summary.get('scoring_allowed_rows', 'UNKNOWN')}; "
                    f"coverage={summary.get('coverage_probe_rows', 'UNKNOWN')}; "
                    f"diagnostic={summary.get('diagnostic_only_rows', 'UNKNOWN')}"
                ),
                "next_action": str(summary.get("operator_note", "UNKNOWN")),
                "auto_apply": "NO",
                "production_change": "NO",
            })
            write_csv(csv_path, rows, fields)


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    max_coverage.run(day, tz, processed)
    rows, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_active_max_coverage_api_policy_summary.csv", rows, SUMMARY_FIELDS)
        (base / "vsigma_active_max_coverage_api_policy.md").write_text(md, encoding="utf-8")
    update_panel(processed, day, rows[0])
    s = rows[0]
    print("=== VSIGMA ACTIVE MAX-COVERAGE API POLICY ===")
    print(f"active_api_policy={s['active_api_policy']}")
    print(f"external_calls_allowed={s['external_calls_allowed']}")
    print(f"external_calls_executed={s['external_calls_executed']}")
    print(f"scoring_allowed_rows={s['scoring_allowed_rows']}")
    print(f"coverage_probe_rows={s['coverage_probe_rows']}")
    print(f"diagnostic_only_rows={s['diagnostic_only_rows']}")
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
