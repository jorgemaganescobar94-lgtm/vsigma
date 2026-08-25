# vSIGMA Context Adjusted Final Picks - 2026-08-25

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 3
- adjusted_status_counts: WAIT_PRELOCK=3
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | WAIT_PRELOCK | Independ. Rivadavia vs Fluminense | market=OVER_1_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #2 | WAIT_PRELOCK | Fenerbahçe vs Lyon | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #3 | WAIT_PRELOCK | Dinamo Zagreb vs Viking | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
