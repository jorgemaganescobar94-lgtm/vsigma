# vSIGMA Objective Availability Gate - 2026-05-31

## Summary
- rows_reviewed: 4
- gate_decision_counts: WAIT_PRELOCK=4
- objective_status_counts: OBJECTIVE_SUPPORTS_TEMPO=4
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=2; AVAILABILITY_ELEVATED_BOTH=1; AVAILABILITY_REPORTED_ADVISORY=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | Cordoba vs Huesca | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #2 | WAIT_PRELOCK | Almeria vs Valladolid | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #3 | WAIT_PRELOCK | RB Bragantino vs Internacional | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_ELEVATED_BOTH | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #4 | WAIT_PRELOCK | Vasco DA Gama vs Atletico-MG | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_REPORTED_ADVISORY | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
