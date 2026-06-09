# vSIGMA Candidate Provenance Ledger - 2026-06-09

## Summary
- rows_reviewed: 3
- candidate_origin_counts: TRANSLATOR_ONLY=2; REAL_SHORTLIST=1
- max_execution_permission_counts: NO_BET=2; LIVE_ONLY=1
- allowed_downstream_use_counts: NO_BET_ONLY=2; LIVE_CONFIRMATION_REQUIRED=1
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Nautico Recife vs Fortaleza EC | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Ponte Preta vs Cuiaba | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Almeria vs Castellón | origin=REAL_SHORTLIST | market=OVER_1_5_SUPPORTED | direction=OVER_TEMPO | max_permission=LIVE_ONLY | strength=60 | allowed=LIVE_CONFIRMATION_REQUIRED | reason=dated shortlist row marked BET

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
