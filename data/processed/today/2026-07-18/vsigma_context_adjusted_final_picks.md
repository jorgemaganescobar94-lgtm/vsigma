# vSIGMA Context Adjusted Final Picks - 2026-07-18

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 3
- adjusted_status_counts: WAIT_PRELOCK=3
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | WAIT_PRELOCK | Universitatea Craiova vs ML Vitebsk | market=BTTS_YES | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #2 | WAIT_PRELOCK | Malisheva vs Vllaznia Shkodër | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #3 | WAIT_PRELOCK | Atert Bissen vs KI Klaksvik | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
