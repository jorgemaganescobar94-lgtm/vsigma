from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
DEFAULT_PLAN_NAME = "API-Football Pro"
DEFAULT_PLAN_REQUESTS_PER_DAY = 7_500
DEFAULT_PRO_POLICY_ROWS_PER_RUN = 250
MAX_HIGH_CAPACITY_POLICY_ROWS_PER_RUN = 5_000

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league", "country",
    "queue_priority", "risk_label", "estimated_call_units", "max_coverage_decision", "enrichment_mode",
    "downstream_use", "external_calls_allowed", "external_calls_executed", "policy_reason", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "policy_status", "api_plan_name", "plan_requests_per_day",
    "rows_reviewed", "rows_allowed", "full_scoring_enrichment_rows", "coverage_probe_rows",
    "diagnostic_only_rows", "blocked_rows", "estimated_call_units", "decision_counts",
    "downstream_use_counts", "external_calls_allowed", "external_calls_executed", "next_action",
    "auto_apply", "production_change",
]

LOW_TRUST_LEAGUE_TOKENS = [
    "U17", "U18", "U19", "U20", "U21", "U23", "WOMEN", "FEMEN", "W LEAGUE", "USL W LEAGUE",
    "RESERVE", "RESERVES", "RESERVE LEAGUE", "ACADEMY", "AKADEMI", "YOUTH", "JUNIOR",
    "1. LIGA CLASSIC", "3. DIVISION", "3. LIGA", "DIVISION 2", "DERDE DIVISIE",
]
LOW_TRUST_TEAM_PATTERNS = [
    r"\bU17\b", r"\bU18\b", r"\bU19\b", r"\bU20\b", r"\bU21\b", r"\bU23\b",
    r"\bII\b", r"\bIII\b", r"\bIV\b", r"\bB\b", r"\bW\b",
    r"\bRES\.?\b", r"\bRESERVE\b", r"\bACADEMY\b", r"\bAKADEMI\b",
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


def load_plan_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_queue_to_enrichment_dry_run_plan.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_queue_to_enrichment_dry_run_plan.csv")
    return rows


def load_subscription_guard(processed: Path, day: str) -> dict[str, str]:
    rows = read_rows(processed / "today" / day / "vsigma_api_subscription_guard.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_subscription_guard.csv")
    return rows[0] if rows else {}


def subscription_policy(processed: Path, day: str) -> dict[str, object]:
    guard = load_subscription_guard(processed, day)
    plan = norm(guard.get("subscription_plan")) or "Pro"
    display_plan = plan if plan.upper().startswith("API-FOOTBALL") else f"API-Football {plan}"
    limit_day = as_int(guard.get("requests_limit_day")) or DEFAULT_PLAN_REQUESTS_PER_DAY
    executor_mode = up(guard.get("executor_mode")) or "PRO_CONTROLLED_EXECUTION"
    recommended_limit = as_int(guard.get("recommended_executor_limit"))
    guard_allowed = up(guard.get("api_calls_allowed")) or "YES"

    if "MAX_COVERAGE_EXECUTION" in executor_mode or limit_day >= 50_000:
        max_rows = MAX_HIGH_CAPACITY_POLICY_ROWS_PER_RUN
    elif recommended_limit > 0:
        max_rows = recommended_limit
    else:
        max_rows = DEFAULT_PRO_POLICY_ROWS_PER_RUN

    external_allowed = "YES_MAX_COVERAGE_POLICY" if guard_allowed == "YES" else "NO_SUBSCRIPTION_GUARD"

    return {
        "api_plan_name": display_plan,
        "plan_requests_per_day": limit_day,
        "max_policy_rows_per_run": max_rows,
        "external_calls_allowed": external_allowed,
    }


def hard_low_trust(row: dict[str, str]) -> bool:
    league = up(row.get("league"))
    teams = f"{up(row.get('home_team'))} {up(row.get('away_team'))}"
    if any(token in league for token in LOW_TRUST_LEAGUE_TOKENS):
        return True
    return any(re.search(pattern, teams) for pattern in LOW_TRUST_TEAM_PATTERNS)


def classify(row: dict[str, str]) -> tuple[str, str, str, str]:
    priority = up(row.get("queue_priority"))
    risk = up(row.get("risk_label"))
    low_trust = hard_low_trust(row)

    if low_trust:
        return (
            "DIAGNOSTIC_COVERAGE_ALLOWED_LOW_TRUST",
            "COVERAGE_PROBE_ONLY",
            "DIAGNOSTIC_ONLY_NO_SCORING",
            "Low-trust youth/reserve/women/B/II/academy/low-tier token detected; API coverage can be collected but cannot feed picks.",
        )
    if "P1_TRUSTED_MISSING_SCORING" in priority and risk == "MEDIUM":
        return (
            "FULL_ENRICHMENT_ALLOWED_FOR_SCORING",
            "FULL_ENRICHMENT_WITH_NORMAL_GATES",
            "SCORING_ALLOWED_WITH_NORMAL_GATES",
            "P1 trusted fixture with medium risk; API enrichment may feed scoring only after all normal gates pass.",
        )
    if "P1_TRUSTED_MISSING_SCORING" in priority:
        return (
            "DIAGNOSTIC_COVERAGE_ALLOWED_CONTEXT_VOLATILITY",
            "COVERAGE_PROBE_ONLY",
            "DIAGNOSTIC_ONLY_NO_SCORING",
            "P1 fixture has context volatility; collect coverage but do not feed scoring without manual review.",
        )
    if "P2_LOW_COVERAGE_SCORING" in priority or "HIGH_LOW_COVERAGE" in risk:
        return (
            "COVERAGE_PROBE_ALLOWED_LOW_COVERAGE",
            "COVERAGE_PROBE_ONLY",
            "COVERAGE_GATE_ONLY",
            "P2 low-coverage fixture; use API to test data availability before any future scoring route.",
        )
    return (
        "DIAGNOSTIC_COVERAGE_ALLOWED_DEFAULT",
        "COVERAGE_PROBE_ONLY",
        "DIAGNOSTIC_ONLY_NO_SCORING",
        "Default max-coverage policy: collect coverage diagnostics only; no scoring permission.",
    )


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    policy = subscription_policy(processed, day)
    max_policy_rows_per_run = int(policy["max_policy_rows_per_run"])
    external_allowed = str(policy["external_calls_allowed"])
    out: list[dict[str, object]] = []
    for idx, row in enumerate(load_plan_rows(processed, day), start=1):
        if idx > max_policy_rows_per_run:
            break
        decision, mode, downstream, reason = classify(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "queue_priority": norm(row.get("queue_priority")),
            "risk_label": norm(row.get("risk_label")),
            "estimated_call_units": as_int(row.get("estimated_call_units")),
            "max_coverage_decision": decision,
            "enrichment_mode": mode,
            "downstream_use": downstream,
            "external_calls_allowed": external_allowed,
            "external_calls_executed": "NO",
            "policy_reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    scoring = [r for r in out if r["downstream_use"] == "SCORING_ALLOWED_WITH_NORMAL_GATES"]
    coverage = [r for r in out if r["downstream_use"] == "COVERAGE_GATE_ONLY"]
    diagnostic = [r for r in out if r["downstream_use"] == "DIAGNOSTIC_ONLY_NO_SCORING"]
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "policy_status": "MAX_COVERAGE_POLICY_READY" if out else "NO_ROWS_TO_COVER",
        "api_plan_name": policy["api_plan_name"],
        "plan_requests_per_day": policy["plan_requests_per_day"],
        "rows_reviewed": len(out),
        "rows_allowed": len(out) if external_allowed.startswith("YES") else 0,
        "full_scoring_enrichment_rows": len(scoring),
        "coverage_probe_rows": len(coverage),
        "diagnostic_only_rows": len(diagnostic),
        "blocked_rows": 0,
        "estimated_call_units": sum(as_int(r.get("estimated_call_units")) for r in out),
        "decision_counts": counts(out, "max_coverage_decision"),
        "downstream_use_counts": counts(out, "downstream_use"),
        "external_calls_allowed": external_allowed if out else "NO",
        "external_calls_executed": "NO",
        "next_action": "Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{k}={v}" for k, v in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Max-Coverage API Enrichment Policy - {day}",
        "",
        "## Summary",
        f"- policy_status: {summary['policy_status']}",
        f"- api_plan_name: {summary['api_plan_name']}",
        f"- plan_requests_per_day: {summary['plan_requests_per_day']}",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- rows_allowed: {summary['rows_allowed']}",
        f"- full_scoring_enrichment_rows: {summary['full_scoring_enrichment_rows']}",
        f"- coverage_probe_rows: {summary['coverage_probe_rows']}",
        f"- diagnostic_only_rows: {summary['diagnostic_only_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- estimated_call_units: {summary['estimated_call_units']}",
        f"- decision_counts: {summary['decision_counts']}",
        f"- downstream_use_counts: {summary['downstream_use_counts']}",
        f"- external_calls_allowed: {summary['external_calls_allowed']}",
        "- external_calls_executed: NO",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Policy Rows",
    ]
    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | decision={row['max_coverage_decision']} | downstream={row['downstream_use']} | mode={row['enrichment_mode']} | calls_executed=NO"
        )
    lines += [
        "",
        "## Guardrails",
        "- This policy follows the active API subscription guard; it does not assume an Ultra plan.",
        "- It does not execute external calls by itself.",
        "- Low-trust fixtures may be queried for diagnostics, but cannot feed picks or scoring unless a separate reviewed model supports them.",
        "- Enrichment never creates stake permission by itself.",
    ]
    return "\n".join(lines) + "\n"


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    section = "## Max-Coverage API Enrichment Policy"
    lines = [
        section,
        f"- policy_status: {summary.get('policy_status', 'UNKNOWN')}",
        f"- api_plan_name: {summary.get('api_plan_name', 'UNKNOWN')}",
        f"- plan_requests_per_day: {summary.get('plan_requests_per_day', 'UNKNOWN')}",
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- rows_allowed: {summary.get('rows_allowed', 'UNKNOWN')}",
        f"- full_scoring_enrichment_rows: {summary.get('full_scoring_enrichment_rows', 'UNKNOWN')}",
        f"- coverage_probe_rows: {summary.get('coverage_probe_rows', 'UNKNOWN')}",
        f"- diagnostic_only_rows: {summary.get('diagnostic_only_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- estimated_call_units: {summary.get('estimated_call_units', 'UNKNOWN')}",
        f"- downstream_use_counts: {summary.get('downstream_use_counts', 'UNKNOWN')}",
        f"- external_calls_allowed: {summary.get('external_calls_allowed', 'UNKNOWN')}",
        f"- external_calls_executed: {summary.get('external_calls_executed', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            if section in text:
                before = text.split(section, 1)[0].rstrip()
                after = text.split(section, 1)[1]
                next_idx = after.find("\n## ")
                tail = after[next_idx:] if next_idx >= 0 else ""
                text = before + block + tail
            else:
                text = text.rstrip() + block
            md_path.write_text(text, encoding="utf-8")


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md_text = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_max_coverage_api_enrichment_policy.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_max_coverage_api_enrichment_policy_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_max_coverage_api_enrichment_policy.md").write_text(md_text, encoding="utf-8")
    append_panel(processed, day, summary[0])
    s = summary[0]
    print("=== VSIGMA MAX-COVERAGE API ENRICHMENT POLICY ===")
    print(f"policy_status={s['policy_status']}")
    print(f"api_plan_name={s['api_plan_name']}")
    print(f"plan_requests_per_day={s['plan_requests_per_day']}")
    print(f"rows_allowed={s['rows_allowed']}")
    print(f"full_scoring_enrichment_rows={s['full_scoring_enrichment_rows']}")
    print(f"coverage_probe_rows={s['coverage_probe_rows']}")
    print(f"diagnostic_only_rows={s['diagnostic_only_rows']}")
    print(f"external_calls_executed={s['external_calls_executed']}")
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
