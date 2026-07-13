# vSIGMA Context Adjusted Final Picks - 2026-07-13

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 2
- adjusted_status_counts: WAIT_PRELOCK=2
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | WAIT_PRELOCK | Gwangju FC vs Pohang Steelers | market=AWAY_WIN | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #2 | WAIT_PRELOCK | Ulsan Hyundai FC vs Jeonbuk Motors | market=OVER_1_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
