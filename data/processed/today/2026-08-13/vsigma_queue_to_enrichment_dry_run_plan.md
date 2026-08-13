# vSIGMA Queue-to-Enrichment Dry Run Planner - 2026-08-13

## Summary
- rows_planned: 1
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=1
- risk_label_counts: MEDIUM=1
- priority_counts: P1_TRUSTED_MISSING_SCORING=1
- total_estimated_call_units: 5
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.
- auto_apply: NO
- production_change: NO

## Dry Run Rows
- RB Bragantino vs Atletico-MG | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | units=5 | blocks=recent_stats; standings; odds; injuries_optional; lineups_prelock_optional | decision=DRY_RUN_ONLY_NO_API_CALLS

## Guardrails
- This planner is dry-run only.
- It does not call APIs, touch secrets, increase spend, create picks, create stake permission, or bypass gates.
- Any future enrichment/API stage requires explicit approval and its own safety gate.
