# vSIGMA API Quota-Aware Enrichment Gate - 2026-06-09

## Summary
- quota_gate_status: NO_AUTO_ENRICHMENT_ALLOWED
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 0
- p1_rows: 0
- p2_rows: 0
- p1_estimated_units: 0
- p2_estimated_units: 0
- p2_probe_units: 0
- total_estimated_units: 0
- auto_units_reserved: 0
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: none
- api_calls_allowed: NO
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
- auto_apply: NO
- production_change: NO

## Allowlist / Policy Rows
- none. Dry-run enrichment plan is missing or empty.

## Guardrails
- This gate is policy/allowlist only; it does not call APIs.
- API calls executed remains NO until a separate enrichment executor is explicitly run.
- P1 may be auto-allowlisted within the subscription guard limit; P2 is coverage-probe-only; volatile/manual rows stay blocked.
- Enrichment alone never creates pick or stake permission.
