# vSIGMA Objective Availability Gate - 2026-05-23

## Summary
- rows_reviewed: 3
- gate_decision_counts: WAIT_PRELOCK=2; SHADOW_RISK_REVIEW=1
- objective_status_counts: OBJECTIVE_SUPPORTS_PICK=1; OBJECTIVE_CONFLICT=1; OBJECTIVE_SUPPORTS_TEMPO=1
- availability_status_counts: AVAILABILITY_REPORTED_ADVISORY=2; AVAILABILITY_RISK_ON_PICK_SIDE=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | Bologna vs Inter | market=AWAY_WIN | objective=OBJECTIVE_SUPPORTS_PICK | availability=AVAILABILITY_REPORTED_ADVISORY | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #2 | WAIT_PRELOCK | Lazio vs Pisa | market=HOME_WIN | objective=OBJECTIVE_CONFLICT | availability=AVAILABILITY_RISK_ON_PICK_SIDE | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #3 | SHADOW_RISK_REVIEW | Kalmar FF vs Degerfors IF | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_REPORTED_ADVISORY | lineup=LINEUPS_NOT_CONFIRMED | action=Allow only with stronger live/prelock confirmation

## Guardrails
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
