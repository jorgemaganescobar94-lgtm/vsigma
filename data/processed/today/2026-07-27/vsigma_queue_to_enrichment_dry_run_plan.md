# vSIGMA Queue-to-Enrichment Dry Run Planner - 2026-07-27

## Summary
- rows_planned: 4
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=4
- risk_label_counts: MEDIUM=4
- priority_counts: P1_TRUSTED_MISSING_SCORING=4
- total_estimated_call_units: 20
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.
- auto_apply: NO
- production_change: NO

## Dry Run Rows
- IF Brommapojkarna vs Hammarby FF | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | units=5 | blocks=recent_stats; standings; odds; injuries_optional; lineups_prelock_optional | decision=DRY_RUN_ONLY_NO_API_CALLS
- KFUM Oslo vs Molde | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | units=5 | blocks=recent_stats; standings; odds; injuries_optional; lineups_prelock_optional | decision=DRY_RUN_ONLY_NO_API_CALLS
- Remo vs Vitoria | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | units=5 | blocks=recent_stats; standings; odds; injuries_optional; lineups_prelock_optional | decision=DRY_RUN_ONLY_NO_API_CALLS
- Aalesund vs Viking | priority=P1_TRUSTED_MISSING_SCORING | risk=MEDIUM | units=5 | blocks=recent_stats; standings; odds; injuries_optional; lineups_prelock_optional | decision=DRY_RUN_ONLY_NO_API_CALLS

## Guardrails
- This planner is dry-run only.
- It does not call APIs, touch secrets, increase spend, create picks, create stake permission, or bypass gates.
- Any future enrichment/API stage requires explicit approval and its own safety gate.
