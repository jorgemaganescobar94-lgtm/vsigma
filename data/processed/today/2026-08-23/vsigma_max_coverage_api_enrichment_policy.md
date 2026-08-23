# vSIGMA Max-Coverage API Enrichment Policy - 2026-08-23

## Summary
- policy_status: MAX_COVERAGE_POLICY_READY
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 3
- rows_allowed: 3
- full_scoring_enrichment_rows: 3
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- blocked_rows: 0
- estimated_call_units: 15
- decision_counts: FULL_ENRICHMENT_ALLOWED_FOR_SCORING=3
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=3
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- auto_apply: NO
- production_change: NO

## Policy Rows
- Fenerbahçe vs Lyon | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Dinamo Zagreb vs Viking | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO
- Independ. Rivadavia vs Fluminense | decision=FULL_ENRICHMENT_ALLOWED_FOR_SCORING | downstream=SCORING_ALLOWED_WITH_NORMAL_GATES | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | calls_executed=NO

## Guardrails
- This policy follows the active API subscription guard; it does not assume an Ultra plan.
- It does not execute external calls by itself.
- Low-trust fixtures may be queried for diagnostics, but cannot feed picks or scoring unless a separate reviewed model supports them.
- Enrichment never creates stake permission by itself.
