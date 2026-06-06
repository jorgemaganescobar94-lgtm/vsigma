# vSIGMA Max-Coverage API Enrichment Executor - 2026-06-05

## Summary
- executor_status: EXECUTION_COMPLETE
- policy_rows_reviewed: 34
- rows_selected: 2
- rows_executed: 2
- rows_dry_run: 0
- rows_success_any: 2
- rows_failed_all: 0
- scoring_allowed_rows: 2
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- endpoint_success_counts: fixture_detail=2; predictions=2; odds=2; events=1
- endpoint_failure_counts: statistics=2; lineups=2; events=1
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: YES_LOGGED_EXECUTION
- auto_apply: NO
- production_change: NO

## Executor Rows
- Castellón vs Almeria | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail;predictions;odds | failed=statistics;events;lineups | scoring_after=YES_PENDING_NORMAL_GATES
- HK Kopavogur vs Afturelding | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=EXECUTE_API_CALLS | status=EXECUTED_WITH_DATA | success=fixture_detail;events;predictions;odds | failed=statistics;lineups | scoring_after=YES_PENDING_NORMAL_GATES

## Guardrails
- This executor may collect API data, but it does not create picks, stake permission, or bypass normal gates.
- SCORING_ALLOWED_WITH_NORMAL_GATES rows still require separate scoring and promotion gates before any market can be considered.
- COVERAGE_GATE_ONLY and DIAGNOSTIC_ONLY_NO_SCORING rows cannot feed picks.
- auto_apply=NO and production_change=NO are hardcoded.
