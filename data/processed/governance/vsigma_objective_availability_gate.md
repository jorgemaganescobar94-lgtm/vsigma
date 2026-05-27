# vSIGMA Objective Availability Gate - 2026-05-27

## Summary
- rows_reviewed: 4
- gate_decision_counts: WAIT_PRELOCK=3; SHADOW_RISK_REVIEW=1
- objective_status_counts: OBJECTIVE_SUPPORTS_TEMPO=4
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=4
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | SHADOW_RISK_REVIEW | Crystal Palace vs Rayo Vallecano | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=LINEUPS_NOT_CONFIRMED | action=Allow only with stronger live/prelock confirmation
- #2 | WAIT_PRELOCK | Libertad Asuncion vs UCV | market=BTTS_YES | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #3 | WAIT_PRELOCK | Independiente del Valle vs Rosario Central | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #4 | WAIT_PRELOCK | Olimpia vs A. Italiano | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
