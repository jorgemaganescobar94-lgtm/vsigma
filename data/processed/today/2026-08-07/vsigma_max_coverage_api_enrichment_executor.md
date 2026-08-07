# vSIGMA Max-Coverage API Enrichment Executor - 2026-08-07

## Summary
- executor_status: EXECUTION_COMPLETE
- policy_rows_reviewed: 1
- rows_selected: 1
- rows_executed: 1
- rows_dry_run: 0
- rows_success_any: 1
- rows_failed_all: 0
- scoring_allowed_rows: 1
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- endpoint_success_counts: fixture_detail=1; statistics=1; events=1; lineups=1; predictions=1; odds=1
- endpoint_failure_counts: none
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: YES_LOGGED_EXECUTION
- auto_apply: NO
- production_change: NO

## Executor Rows
- Dundee Utd vs Rangers | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail;statistics;events;lineups;predictions;odds | failed=none | scoring_after=YES_PENDING_NORMAL_GATES

## Guardrails
- This executor may collect API data, but it does not create picks, stake permission, or bypass normal gates.
- SCORING_ALLOWED_WITH_NORMAL_GATES rows still require separate scoring and promotion gates before any market can be considered.
- COVERAGE_GATE_ONLY and DIAGNOSTIC_ONLY_NO_SCORING rows cannot feed picks.
- auto_apply=NO and production_change=NO are hardcoded.
