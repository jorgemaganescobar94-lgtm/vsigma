# vSIGMA Objective Availability Gate - 2026-07-20

## Summary
- rows_reviewed: 3
- gate_decision_counts: WAIT_PRELOCK=3
- objective_status_counts: OBJECTIVE_CONFLICT=2; OBJECTIVE_SUPPORTS_TEMPO=1
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=3
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | Halmstad vs BK Hacken | market=AWAY_WIN | objective=OBJECTIVE_CONFLICT | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #2 | WAIT_PRELOCK | Hammarby FF vs Degerfors IF | market=BTTS_YES | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #3 | WAIT_PRELOCK | FC Anyang vs Gwangju FC | market=HOME_WIN | objective=OBJECTIVE_CONFLICT | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
