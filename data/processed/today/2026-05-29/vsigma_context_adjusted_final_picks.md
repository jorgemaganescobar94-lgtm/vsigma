# vSIGMA Context Adjusted Final Picks - 2026-05-29

## Summary
- input_verdict: DATED_UPSTREAM_OK
- missing_inputs: none
- stale_inputs: none
- rows_reviewed: 3
- adjusted_status_counts: SHADOW_RISK_ONLY=2; WAIT_PRELOCK=1
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- #1 | SHADOW_RISK_ONLY | America de Cali vs Macara | market=OVER_1_5 | stake=LOW_OR_SYMBOLIC | reason=shadow risk: low-conversion pattern
- #2 | SHADOW_RISK_ONLY | Boca Juniors vs U. Catolica | market=OVER_1_5 | stake=LOW_OR_SYMBOLIC | reason=shadow risk: low-conversion pattern
- #3 | WAIT_PRELOCK | Monza vs Catanzaro | market=OVER_2_5 | stake=NO_PREMATCH_STAKE | reason=objective/availability gate requires prelock or lineup confirmation

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
