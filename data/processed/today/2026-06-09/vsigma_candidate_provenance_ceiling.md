# vSIGMA Candidate Provenance Ceiling - 2026-06-09

## Summary
- rows_reviewed: 3
- ceiling_action_counts: NO_CHANGE=3
- candidate_origin_counts: TRANSLATOR_ONLY=2; REAL_SHORTLIST=1
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Almeria vs Castellón | origin=REAL_SHORTLIST | max=LIVE_ONLY | permission=LIVE_ONLY -> LIVE_ONLY | stake=SYMBOLIC_ONLY -> SYMBOLIC_ONLY | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Nautico Recife vs Fortaleza EC | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Ponte Preta vs Cuiaba | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
