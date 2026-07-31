# vSIGMA Objective Availability Gate - 2026-07-31

## Summary
- rows_reviewed: 4
- gate_decision_counts: WAIT_PRELOCK=4
- objective_status_counts: OBJECTIVE_SUPPORTS_TEMPO=3; OBJECTIVE_NEUTRAL_OR_UNKNOWN=1
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=4
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | Aalesund vs Viking | market=AWAY_WIN | objective=OBJECTIVE_NEUTRAL_OR_UNKNOWN | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #2 | WAIT_PRELOCK | KFUM Oslo vs Molde | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #3 | WAIT_PRELOCK | IF Brommapojkarna vs Hammarby FF | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #4 | WAIT_PRELOCK | Remo vs Vitoria | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
