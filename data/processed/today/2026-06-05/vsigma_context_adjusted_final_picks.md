# vSIGMA Context Adjusted Final Picks - 2026-06-05

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 1
- adjusted_status_counts: INPUT_ROW_MISSING_REVIEW=1
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | INPUT_ROW_MISSING_REVIEW | Las Palmas vs Malaga | market=OVER_1_5 | stake=NO_STAKE | reason=dated real objective context gate has no matching fixture row

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
