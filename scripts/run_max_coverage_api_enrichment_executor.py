from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from api_football_client import APIFootballClient, APIFootballError

PROCESSED = Path("data/processed")

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "fixture_id",
    "home_team",
    "away_team",
    "league",
    "country",
    "max_coverage_decision",
    "enrichment_mode",
    "downstream_use",
    "external_calls_allowed",
    "executor_mode",
    "planned_endpoints",
    "executed_endpoints",
    "successful_endpoints",
    "failed_endpoints",
    "fixture_detail_status",
    "statistics_status",
    "events_status",
    "lineups_status",
    "predictions_status",
    "odds_status",
    "executor_status",
    "scoring_eligibility_after_execution",
    "raw_output_dir",
    "error_summary",
    "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "executor_status",
    "policy_rows_reviewed",
    "rows_selected",
    "rows_executed",
    "rows_dry_run",
    "rows_success_any",
    "rows_failed_all",
    "scoring_allowed_rows",
    "coverage_probe_rows",
    "diagnostic_only_rows",
    "endpoint_success_counts",
    "endpoint_failure_counts",
    "external_calls_allowed",
    "external_calls_executed",
    "auto_apply",
    "production_change",
]

ENDPOINTS_FULL = ["fixture_detail", "statistics", "events", "lineups", "predictions", "odds"]
ENDPOINTS_PROBE = ["fixture_detail", "statistics", "events"]
ENDPOINTS_DIAGNOSTIC = ["fixture_detail"]

def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default

def up(value: object) -> str:
    return norm(value).upper()

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

def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

def policy_path(processed: Path, day: str) -> Path:
    today = processed / "today" / day / "vsigma_max_coverage_api_enrichment_policy.csv"
    if today.exists():
        return today
    return processed / "governance" / "vsigma_max_coverage_api_enrichment_policy.csv"

def load_policy(processed: Path, day: str) -> list[dict[str, str]]:
    path = policy_path(processed, day)
    rows = read_csv(path)
    if path.parent.name == "governance" and rows and "target_date" in rows[0]:
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows

def endpoint_plan(row: dict[str, str]) -> list[str]:
    downstream = up(row.get("downstream_use"))
    mode = up(row.get("enrichment_mode"))
    if downstream == "SCORING_ALLOWED_WITH_NORMAL_GATES" or mode == "FULL_ENRICHMENT_WITH_NORMAL_GATES":
        return ENDPOINTS_FULL
    if downstream == "COVERAGE_GATE_ONLY":
        return ENDPOINTS_PROBE
    return ENDPOINTS_DIAGNOSTIC

def call_endpoint(client: APIFootballClient, endpoint: str, fixture_id: str) -> dict:
    if endpoint == "fixture_detail":
        return client.fixtures(id=fixture_id)
    if endpoint == "statistics":
        return client.fixture_statistics(fixture_id)
    if endpoint == "events":
        return client.fixture_events(fixture_id)
    if endpoint == "lineups":
        return client.fixture_lineups(fixture_id)
    if endpoint == "predictions":
        return client.predictions(fixture_id)
    if endpoint == "odds":
        return client.odds(fixture=fixture_id)
    raise ValueError(f"Unknown endpoint: {endpoint}")

def response_has_rows(payload: dict) -> bool:
    response = payload.get("response")
    return isinstance(response, list) and len(response) > 0

def selected_rows(rows: list[dict[str, str]], limit: int | None) -> list[dict[str, str]]:
    allowed = [
        row for row in rows
        if up(row.get("external_calls_allowed")) == "YES_MAX_COVERAGE_POLICY"
        and norm(row.get("fixture_id"))
    ]
    if limit is not None:
        allowed = allowed[:limit]
    return allowed

def endpoint_status(success: dict[str, bool], endpoint: str) -> str:
    if endpoint not in success:
        return "NOT_PLANNED"
    return "OK" if success[endpoint] else "FAILED_OR_EMPTY"

def execute(day: str, tz: str, processed: Path, dry_run: bool, limit: int | None, force_refresh: bool) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    policy_rows = load_policy(processed, day)
    rows = selected_rows(policy_rows, limit)

    client = None if dry_run else APIFootballClient()

    out_rows: list[dict[str, object]] = []
    endpoint_success_counter: Counter[str] = Counter()
    endpoint_failure_counter: Counter[str] = Counter()

    for row in rows:
        fixture_id = norm(row.get("fixture_id"))
        endpoints = endpoint_plan(row)
        base_dir = processed / "today" / day / "api_enrichment" / fixture_id
        success: dict[str, bool] = {}
        errors: list[str] = []

        if dry_run:
            executor_status = "DRY_RUN_NO_CALLS"
            executed = []
        else:
            executed = []
            for endpoint in endpoints:
                try:
                    payload = call_endpoint(client, endpoint, fixture_id)  # type: ignore[arg-type]
                    write_json(base_dir / f"{endpoint}.json", payload)
                    ok = response_has_rows(payload)
                    success[endpoint] = ok
                    executed.append(endpoint)
                    if ok:
                        endpoint_success_counter[endpoint] += 1
                    else:
                        endpoint_failure_counter[endpoint] += 1
                        errors.append(f"{endpoint}:EMPTY_RESPONSE")
                except APIFootballError as exc:
                    success[endpoint] = False
                    executed.append(endpoint)
                    endpoint_failure_counter[endpoint] += 1
                    errors.append(f"{endpoint}:{exc}")
                    write_json(base_dir / f"{endpoint}.error.json", {
                        "endpoint": endpoint,
                        "fixture_id": fixture_id,
                        "error": str(exc),
                        "status_code": exc.status_code,
                        "api_errors": exc.api_errors,
                        "is_plan_limit": exc.is_plan_limit,
                    })
                except Exception as exc:
                    success[endpoint] = False
                    executed.append(endpoint)
                    endpoint_failure_counter[endpoint] += 1
                    errors.append(f"{endpoint}:{type(exc).__name__}:{exc}")
                    write_json(base_dir / f"{endpoint}.error.json", {
                        "endpoint": endpoint,
                        "fixture_id": fixture_id,
                        "error": f"{type(exc).__name__}: {exc}",
                    })

            executor_status = "EXECUTED_WITH_DATA" if any(success.values()) else "EXECUTED_NO_DATA_OR_ERRORS"

        downstream = norm(row.get("downstream_use"))
        scoring_after = "NO"
        if downstream == "SCORING_ALLOWED_WITH_NORMAL_GATES":
            has_fixture_detail = success.get("fixture_detail", False)
            has_market_signal = success.get("predictions", False) or success.get("odds", False)
            scoring_after = (
                "YES_PENDING_NORMAL_GATES"
                if has_fixture_detail and has_market_signal
                else "NO_MISSING_REQUIRED_API_DATA"
            )
        elif downstream == "COVERAGE_GATE_ONLY":
            scoring_after = "NO_COVERAGE_GATE_ONLY"
        else:
            scoring_after = "NO_DIAGNOSTIC_ONLY"

        out_rows.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": fixture_id,
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "max_coverage_decision": norm(row.get("max_coverage_decision")),
            "enrichment_mode": norm(row.get("enrichment_mode")),
            "downstream_use": downstream,
            "external_calls_allowed": norm(row.get("external_calls_allowed")),
            "executor_mode": "DRY_RUN" if dry_run else "EXECUTE_API_CALLS",
            "planned_endpoints": ";".join(endpoints),
            "executed_endpoints": ";".join(executed),
            "successful_endpoints": ";".join([ep for ep, ok in success.items() if ok]),
            "failed_endpoints": ";".join([ep for ep, ok in success.items() if not ok]),
            "fixture_detail_status": endpoint_status(success, "fixture_detail"),
            "statistics_status": endpoint_status(success, "statistics"),
            "events_status": endpoint_status(success, "events"),
            "lineups_status": endpoint_status(success, "lineups"),
            "predictions_status": endpoint_status(success, "predictions"),
            "odds_status": endpoint_status(success, "odds"),
            "executor_status": executor_status,
            "scoring_eligibility_after_execution": scoring_after,
            "raw_output_dir": base_dir.as_posix(),
            "error_summary": " | ".join(errors),
            "auto_apply": "NO",
            "production_change": "NO",
        })

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "executor_status": "DRY_RUN_READY" if dry_run else "EXECUTION_COMPLETE",
        "policy_rows_reviewed": len(policy_rows),
        "rows_selected": len(rows),
        "rows_executed": 0 if dry_run else len(rows),
        "rows_dry_run": len(rows) if dry_run else 0,
        "rows_success_any": sum(1 for row in out_rows if norm(row.get("successful_endpoints"))),
        "rows_failed_all": sum(1 for row in out_rows if not norm(row.get("successful_endpoints")) and not dry_run),
        "scoring_allowed_rows": sum(1 for row in out_rows if row.get("downstream_use") == "SCORING_ALLOWED_WITH_NORMAL_GATES"),
        "coverage_probe_rows": sum(1 for row in out_rows if row.get("downstream_use") == "COVERAGE_GATE_ONLY"),
        "diagnostic_only_rows": sum(1 for row in out_rows if row.get("downstream_use") == "DIAGNOSTIC_ONLY_NO_SCORING"),
        "endpoint_success_counts": "; ".join(f"{k}={v}" for k, v in endpoint_success_counter.most_common()) or "none",
        "endpoint_failure_counts": "; ".join(f"{k}={v}" for k, v in endpoint_failure_counter.most_common()) or "none",
        "external_calls_allowed": "YES_MAX_COVERAGE_POLICY" if rows else "NO_ROWS",
        "external_calls_executed": "NO_DRY_RUN" if dry_run else "YES_LOGGED_EXECUTION",
        "auto_apply": "NO",
        "production_change": "NO",
    }]

    return out_rows, summary, markdown(day, out_rows, summary[0], dry_run)

def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object], dry_run: bool) -> str:
    lines = [
        f"# vSIGMA Max-Coverage API Enrichment Executor - {day}",
        "",
        "## Summary",
        f"- executor_status: {summary['executor_status']}",
        f"- policy_rows_reviewed: {summary['policy_rows_reviewed']}",
        f"- rows_selected: {summary['rows_selected']}",
        f"- rows_executed: {summary['rows_executed']}",
        f"- rows_dry_run: {summary['rows_dry_run']}",
        f"- rows_success_any: {summary['rows_success_any']}",
        f"- rows_failed_all: {summary['rows_failed_all']}",
        f"- scoring_allowed_rows: {summary['scoring_allowed_rows']}",
        f"- coverage_probe_rows: {summary['coverage_probe_rows']}",
        f"- diagnostic_only_rows: {summary['diagnostic_only_rows']}",
        f"- endpoint_success_counts: {summary['endpoint_success_counts']}",
        f"- endpoint_failure_counts: {summary['endpoint_failure_counts']}",
        f"- external_calls_allowed: {summary['external_calls_allowed']}",
        f"- external_calls_executed: {summary['external_calls_executed']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Executor Rows",
    ]
    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | downstream={row['downstream_use']} | "
            f"mode={row['executor_mode']} | status={row['executor_status']} | "
            f"success={row['successful_endpoints'] or 'none'} | failed={row['failed_endpoints'] or 'none'} | "
            f"scoring_after={row['scoring_eligibility_after_execution']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This executor may collect API data, but it does not create picks, stake permission, or bypass normal gates.",
        "- SCORING_ALLOWED_WITH_NORMAL_GATES rows still require separate scoring and promotion gates before any market can be considered.",
        "- COVERAGE_GATE_ONLY and DIAGNOSTIC_ONLY_NO_SCORING rows cannot feed picks.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]], summary: list[dict[str, object]], md: str) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_max_coverage_api_enrichment_executor.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_max_coverage_api_enrichment_executor_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_max_coverage_api_enrichment_executor.md").write_text(md, encoding="utf-8")

def run(day: str, tz: str, processed: Path, dry_run: bool, limit: int | None, force_refresh: bool) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = execute(day, tz, processed, dry_run=dry_run, limit=limit, force_refresh=force_refresh)
    write_outputs(processed, day, rows, summary, md)
    s = summary[0]
    print("=== VSIGMA MAX-COVERAGE API ENRICHMENT EXECUTOR ===")
    print(f"executor_status={s['executor_status']}")
    print(f"rows_selected={s['rows_selected']}")
    print(f"rows_executed={s['rows_executed']}")
    print(f"external_calls_executed={s['external_calls_executed']}")
    print("auto_apply=NO")
    print("production_change=NO")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    parser.add_argument("--execute", action="store_true", help="Execute real API calls. Default is dry-run.")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force-refresh", action="store_true")
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir, dry_run=not args.execute, limit=args.limit, force_refresh=args.force_refresh)

if __name__ == "__main__":
    main()
