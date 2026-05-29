# vSIGMA Objective Availability Gate - 2026-05-29

## Summary
- rows_reviewed: 3
- gate_decision_counts: SHADOW_RISK_REVIEW=2; WAIT_PRELOCK=1
- objective_status_counts: OBJECTIVE_SUPPORTS_TEMPO=3
- availability_status_counts: AVAILABILITY_UNKNOWN_OR_CLEAN=3
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | WAIT_PRELOCK | Monza vs Catanzaro | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution
- #2 | SHADOW_RISK_REVIEW | Boca Juniors vs U. Catolica | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=LINEUPS_NOT_CONFIRMED | action=Allow only with stronger live/prelock confirmation
- #3 | SHADOW_RISK_REVIEW | America de Cali vs Macara | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | lineup=LINEUPS_NOT_CONFIRMED | action=Allow only with stronger live/prelock confirmation

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
