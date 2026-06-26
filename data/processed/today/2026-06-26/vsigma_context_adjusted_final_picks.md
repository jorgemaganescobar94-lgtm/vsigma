# vSIGMA Context Adjusted Final Picks - 2026-06-26

## Summary
- input_verdict: INPUT_MISSING_DATED_UPSTREAM
- missing_inputs: vsigma_today_execution_bets_only.csv or vsigma_today_execution_shortlist.csv
- stale_inputs: none
- rows_reviewed: 0
- adjusted_status_counts: none
- auto_apply: NO
- production_change: NO

## Final Adjusted Picks
- none. Missing or stale dated upstream input; refused governance/root fallback.

## Guardrails
- This report refuses governance and root-level fallbacks.
- Required upstream files must exist under data/processed/today/<date>/.
- Real objective context and objective availability gates override base ranking when present.
