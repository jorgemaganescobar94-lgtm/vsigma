# vSIGMA API Coverage Gate Applied to Board v2 - 2026-06-10

## Summary
- rows_reviewed: 2
- gate_actions: EARLY_WATCH_ONLY=1; NO_BET_CONFIRMED=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Malaga vs Las Palmas | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Cape Town City vs Magesi | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
