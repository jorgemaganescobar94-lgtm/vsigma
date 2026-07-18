# vSIGMA Objective Availability Gate - 2026-07-18

## Summary
- rows_reviewed: 3
- gate_decision_counts: WAIT_PRELOCK=3
- objective_status_counts: OBJECTIVE_NEUTRAL_OR_UNKNOWN=3
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=3
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | Universitatea Craiova vs ML Vitebsk | market=BTTS_YES | objective=OBJECTIVE_NEUTRAL_OR_UNKNOWN | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #2 | WAIT_PRELOCK | Malisheva vs Vllaznia Shkodër | market=OVER_2_5 | objective=OBJECTIVE_NEUTRAL_OR_UNKNOWN | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #3 | WAIT_PRELOCK | Atert Bissen vs KI Klaksvik | market=OVER_2_5 | objective=OBJECTIVE_NEUTRAL_OR_UNKNOWN | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
