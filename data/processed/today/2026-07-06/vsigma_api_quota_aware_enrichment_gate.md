# vSIGMA API Quota-Aware Enrichment Gate - 2026-07-06

## Summary
- quota_gate_status: AUTO_ENRICHMENT_ALLOWED_LIMITED
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 2
- p1_rows: 2
- p2_rows: 0
- p1_estimated_units: 10
- p2_estimated_units: 0
- p2_probe_units: 0
- total_estimated_units: 10
- auto_units_reserved: 10
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=2
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
- auto_apply: NO
- production_change: NO

## Allowlist / Policy Rows
- Degerfors IF vs Malmo FF | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO
- Jeonbuk Motors vs Gangwon FC | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | decision=AUTO_ENRICHMENT_ALLOWED_P1 | mode=FULL_ENRICHMENT_WITH_NORMAL_GATES | reserved=5 | api_allowed=YES_LIMITED | executed=NO

## Guardrails
- This gate is policy/allowlist only; it does not call APIs.
- API calls executed remains NO until a separate enrichment executor is explicitly run.
- P1 may be auto-allowlisted within the subscription guard limit; P2 is coverage-probe-only; volatile/manual rows stay blocked.
- Enrichment alone never creates pick or stake permission.
