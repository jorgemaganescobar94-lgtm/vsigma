# vSIGMA Context Adjusted Final Picks - 2026-05-27

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 4
- adjusted_status_counts: WAIT_PRELOCK=2; BET_KEEP=1; SHADOW_RISK_ONLY=1
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | BET_KEEP | Flamengo vs Cusco | market=BTTS_YES | stake=NORMAL_IF_PRELOCK_OK | reason=strong base edge and execution score with no context downgrade
- #2 | SHADOW_RISK_ONLY | Club Nacional vs Coquimbo Unido | market=OVER_1_5 | stake=LOW_OR_SYMBOLIC | reason=shadow risk: low-conversion pattern
- #3 | WAIT_PRELOCK | Olimpia vs A. Italiano | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #4 | WAIT_PRELOCK | Crystal Palace vs Rayo Vallecano | market=OVER_1_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
