# vSIGMA Candidate Provenance Ceiling - 2026-08-01

## Summary
- rows_reviewed: 1
- ceiling_action_counts: CAPPED=1
- candidate_origin_counts: OBJECTIVE_PROXY=1
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Dundee Utd vs Rangers | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET_OR_WATCH -> NO_BET | stake=NO_STAKE_OR_SYMBOLIC -> NO_STAKE | action=CAPPED | reason=permission NO_BET_OR_WATCH exceeded provenance ceiling NO_BET from OBJECTIVE_PROXY

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
