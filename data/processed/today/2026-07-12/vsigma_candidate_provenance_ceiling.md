# vSIGMA Candidate Provenance Ceiling - 2026-07-12

## Summary
- rows_reviewed: 2
- ceiling_action_counts: CAPPED=1; NO_CHANGE=1
- candidate_origin_counts: OBJECTIVE_PROXY=2
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Gwangju FC vs Pohang Steelers | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET_OR_WATCH -> NO_BET | stake=NO_STAKE_OR_SYMBOLIC -> NO_STAKE | action=CAPPED | reason=permission NO_BET_OR_WATCH exceeded provenance ceiling NO_BET from OBJECTIVE_PROXY
- Ulsan Hyundai FC vs Jeonbuk Motors | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
