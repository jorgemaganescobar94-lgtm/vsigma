# vSIGMA Context Adjusted Final Picks - 2026-05-28

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 2
- adjusted_status_counts: SHADOW_RISK_ONLY=1; WAIT_PRELOCK=1
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | SHADOW_RISK_ONLY | Bolívar vs Independ. Rivadavia | market=OVER_2_5 | stake=LOW_OR_SYMBOLIC | reason=shadow risk: low-conversion pattern
- #2 | WAIT_PRELOCK | Palmeiras vs Junior | market=BTTS_YES | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
