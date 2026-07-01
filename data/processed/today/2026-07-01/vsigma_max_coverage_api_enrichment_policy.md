# vSIGMA Max-Coverage API Enrichment Policy - 2026-07-01

## Summary
- policy_status: NO_ROWS_TO_COVER
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 0
- rows_allowed: 0
- full_scoring_enrichment_rows: 0
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- blocked_rows: 0
- estimated_call_units: 0
- decision_counts: none
- downstream_use_counts: none
- external_calls_allowed: NO
- external_calls_executed: NO
- auto_apply: NO
- production_change: NO

## Policy Rows

## Guardrails
- This policy follows the active API subscription guard; it does not assume an Ultra plan.
- It does not execute external calls by itself.
- Low-trust fixtures may be queried for diagnostics, but cannot feed picks or scoring unless a separate reviewed model supports them.
- Enrichment never creates stake permission by itself.
