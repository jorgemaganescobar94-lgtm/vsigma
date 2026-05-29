# vSIGMA Objective Availability Gate - 2026-05-29

## Summary
- rows_reviewed: 1
- gate_decision_counts: SHADOW_RISK_REVIEW=1
- objective_status_counts: OBJECTIVE_SUPPORTS_TEMPO=1
- availability_status_counts: AVAILABILITY_ELEVATED_BOTH=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | SHADOW_RISK_REVIEW | Nice vs Saint Etienne | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_ELEVATED_BOTH | lineup=LINEUPS_NOT_CONFIRMED | action=Allow only with stronger live/prelock confirmation

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
