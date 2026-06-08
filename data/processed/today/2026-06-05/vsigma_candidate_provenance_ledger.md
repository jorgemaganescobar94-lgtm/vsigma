# vSIGMA Candidate Provenance Ledger - 2026-06-05

## Summary
- rows_reviewed: 1
- candidate_origin_counts: OBJECTIVE_PROXY=1
- max_execution_permission_counts: NO_BET=1
- allowed_downstream_use_counts: DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION=1
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Las Palmas vs Malaga | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=17 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
