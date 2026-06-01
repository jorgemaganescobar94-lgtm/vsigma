# vSIGMA Candidate Provenance Ledger - 2026-06-01

## Summary
- rows_reviewed: 4
- candidate_origin_counts: OBJECTIVE_PROXY=4
- max_execution_permission_counts: NO_BET=4
- allowed_downstream_use_counts: DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION=4
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Cordoba vs Huesca | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=18 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row
- Almeria vs Valladolid | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=18 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row
- RB Bragantino vs Internacional | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=18 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row
- Vasco DA Gama vs Atletico-MG | origin=OBJECTIVE_PROXY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=18 | allowed=DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION | reason=objective context bridge created diagnostic shortlist row

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
