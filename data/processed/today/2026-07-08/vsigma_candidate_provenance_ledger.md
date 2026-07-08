# vSIGMA Candidate Provenance Ledger - 2026-07-08

## Summary
- rows_reviewed: 2
- candidate_origin_counts: OBJECTIVE_PROXY=2
- max_execution_permission_counts: NO_BET=2
- allowed_downstream_use_counts: DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Lincoln Red Imps FC vs Inter Club d'Escaldes | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=21 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row
- Vikingur Reykjavik vs Gyori ETO FC | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=21 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
