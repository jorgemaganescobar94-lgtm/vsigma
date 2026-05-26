# vSIGMA Objective Availability Gate - 2026-05-26

## Summary
- rows_reviewed: 1
- gate_decision_counts: WAIT_PRELOCK=1
- objective_status_counts: OBJECTIVE_PROXY_ONLY=1
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | LDU de Quito vs Always Ready | market=UNDER_3_5 | objective=OBJECTIVE_PROXY_ONLY | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
