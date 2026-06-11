# vSIGMA API Coverage Gate Applied to Board v2 - 2026-06-10

## Summary
- rows_reviewed: 2
- gate_actions: DOWNGRADED_TO_NO_BET=1; UNKNOWN_COVERAGE_BLOCK=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Malaga vs Las Palmas | api_gate=LOW_COVERAGE_NO_BET | action=DOWNGRADED_TO_NO_BET | decision=LIVE_ONLY->NO_BET | permission=LIVE_ONLY->NO | missing=lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- Cape Town City vs Magesi | api_gate=UNKNOWN | action=UNKNOWN_COVERAGE_BLOCK | decision=NO_BET->NO_BET | permission=NO->NO | missing=unknown

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
