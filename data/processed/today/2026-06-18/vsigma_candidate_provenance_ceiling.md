# vSIGMA Candidate Provenance Ceiling - 2026-06-18

## Summary
- rows_reviewed: 1
- ceiling_action_counts: NO_CHANGE=1
- candidate_origin_counts: TRANSLATOR_ONLY=1
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- AC Oulu vs Mariehamn | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
