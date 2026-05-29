# vSIGMA API Coverage Gate Applied to Board v2 - 2026-05-29

## Summary
- rows_reviewed: 2
- gate_actions: EARLY_WATCH_ONLY=1; NO_BET_CONFIRMED=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Nice vs Saint Etienne | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->NO_PREMATCH | missing=lineup_coverage=PROBABLE_LOW; standings_coverage=PARTIAL
- Cde Juventud Italiana vs Tecnico Universitario | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
