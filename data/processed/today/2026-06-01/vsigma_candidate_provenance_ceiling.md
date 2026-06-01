# vSIGMA Candidate Provenance Ceiling - 2026-06-01

## Summary
- rows_reviewed: 4
- ceiling_action_counts: NO_CHANGE=4
- candidate_origin_counts: OBJECTIVE_PROXY=4
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Cordoba vs Huesca | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling
- Almeria vs Valladolid | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling
- RB Bragantino vs Internacional | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling after proxy inversion guard
- Vasco DA Gama vs Atletico-MG | origin=OBJECTIVE_PROXY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling after proxy inversion guard

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
