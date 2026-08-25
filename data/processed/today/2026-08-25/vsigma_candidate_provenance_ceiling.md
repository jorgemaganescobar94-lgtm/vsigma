# vSIGMA Candidate Provenance Ceiling - 2026-08-25

## Summary
- rows_reviewed: 3
- ceiling_action_counts: NO_CHANGE=3
- candidate_origin_counts: OBJECTIVE_PROXY=3
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Fenerbahçe vs Lyon | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Dinamo Zagreb vs Viking | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Independ. Rivadavia vs Fluminense | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
