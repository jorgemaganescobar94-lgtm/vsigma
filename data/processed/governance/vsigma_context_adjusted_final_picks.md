# vSIGMA Context Adjusted Final Picks - 2026-05-27

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 4
- adjusted_status_counts: WAIT_PRELOCK=3; SHADOW_RISK_ONLY=1
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | SHADOW_RISK_ONLY | Crystal Palace vs Rayo Vallecano | market=OVER_1_5 | stake=LOW_OR_SYMBOLIC | reason=shadow risk: low-conversion pattern
- #2 | WAIT_PRELOCK | Independiente del Valle vs Rosario Central | market=OVER_1_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #3 | WAIT_PRELOCK | Libertad Asuncion vs UCV | market=BTTS_YES | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #4 | WAIT_PRELOCK | Olimpia vs A. Italiano | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
