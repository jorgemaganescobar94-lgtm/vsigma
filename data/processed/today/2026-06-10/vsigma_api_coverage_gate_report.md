# vSIGMA API Coverage Gate Applied to Board v2 - 2026-06-10

## Summary
- rows_reviewed: 1
- gate_actions: NO_BET_CONFIRMED=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Malaga vs Las Palmas | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO->NO | missing=lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
