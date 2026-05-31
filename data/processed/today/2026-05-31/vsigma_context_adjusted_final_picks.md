# vSIGMA Context Adjusted Final Picks - 2026-05-31

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 4
- adjusted_status_counts: WAIT_PRELOCK=4
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | WAIT_PRELOCK | Cordoba vs Huesca | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #2 | WAIT_PRELOCK | RB Bragantino vs Internacional | market=OVER_1_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #3 | WAIT_PRELOCK | Almeria vs Valladolid | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation
- #4 | WAIT_PRELOCK | Vasco DA Gama vs Atletico-MG | market=OVER_1_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
