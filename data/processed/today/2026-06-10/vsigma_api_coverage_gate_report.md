# vSIGMA API Coverage Gate Applied to Board v2 - 2026-06-10

## Summary
- rows_reviewed: 2
- gate_actions: PREMATCH_BLOCKED_KEEP_WATCH=1; UNKNOWN_COVERAGE_BLOCK=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Malaga vs Las Palmas | api_gate=WAIT_LINEUPS_OR_LIVE_ONLY | action=PREMATCH_BLOCKED_KEEP_WATCH | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->LIVE_ONLY | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Cape Town City vs Magesi | api_gate=UNKNOWN | action=UNKNOWN_COVERAGE_BLOCK | decision=NO_BET->NO_BET | permission=NO->NO | missing=unknown

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
