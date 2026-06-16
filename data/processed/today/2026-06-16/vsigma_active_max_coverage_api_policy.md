# vSIGMA Active Max-Coverage API Policy - 2026-06-16

## Summary
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 40
- coverage_probe_rows: 0
- diagnostic_only_rows: 4
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
- auto_apply: NO
- production_change: NO

## Guardrails
- This integration only declares which API policy is active.
- It does not execute API calls, create picks, create stake permission, or bypass scoring gates.
- MAX_COVERAGE permits broad API collection, but scoring/picks remain restricted by downstream_use and normal gates.
