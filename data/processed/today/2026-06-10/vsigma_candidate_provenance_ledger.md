# vSIGMA Candidate Provenance Ledger - 2026-06-10

## Summary
- rows_reviewed: 1
- candidate_origin_counts: REAL_SHORTLIST=1
- max_execution_permission_counts: LIVE_ONLY=1
- allowed_downstream_use_counts: LIVE_CONFIRMATION_REQUIRED=1
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Malaga vs Las Palmas | origin=REAL_SHORTLIST | market=OVER_1_5_SUPPORTED | direction=OVER_TEMPO | max_permission=LIVE_ONLY | strength=60 | allowed=LIVE_CONFIRMATION_REQUIRED | reason=dated shortlist row marked BET

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
