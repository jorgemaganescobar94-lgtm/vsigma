# vSIGMA Objective Availability Gate - 2026-05-25

## Summary
- rows_reviewed: 2
- gate_decision_counts: SHADOW_RISK_REVIEW=1; WAIT_PRELOCK=1
- objective_status_counts: OBJECTIVE_SUPPORTS_TEMPO=2
- availability_status_counts: AVAILABILITY_REPORTED_ADVISORY=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Gate Rows
- #1 | SHADOW_RISK_REVIEW | IF Elfsborg vs BK Hacken | market=OVER_2_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_REPORTED_ADVISORY | lineup=LINEUPS_CONFIRMED | action=Allow only with stronger live/prelock confirmation
- #2 | WAIT_PRELOCK | SC Paderborn 07 vs VfL Wolfsburg | market=OVER_1_5 | objective=OBJECTIVE_SUPPORTS_TEMPO | availability=AVAILABILITY_REPORTED_ADVISORY | lineup=WAIT_PRELOCK | action=Wait for lineups/prelock before execution

## Guardrails
- This gate refuses root-level execution fallback.
- This gate does not change production picks automatically.
- Objective and availability conflicts require prelock/manual review before premium execution.
