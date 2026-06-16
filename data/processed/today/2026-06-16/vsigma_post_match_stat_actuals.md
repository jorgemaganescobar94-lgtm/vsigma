# vSIGMA Post-Match Stat Actuals - 2026-06-16

## Summary
- rows_final: 6
- verdict_counts: FINAL_ACTUALS_AVAILABLE=6
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- Hartford Athletic W vs New England Mutiny W | status=FT | goals=3 | SoT=NA | corners=NA | cards=NA | metrics=goals; xg; big
- Dakota vs Sporting | status=FT | goals=2 | SoT=NA | corners=NA | cards=NA | metrics=goals; xg; big
- Iran vs New Zealand | status=FT | goals=4 | SoT=12 | corners=5 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big
- Rochedale Rovers vs Moreton City Excelsior | status=FT | goals=7 | SoT=NA | corners=NA | cards=NA | metrics=goals; xg; big
- WDSC Wolves vs Eastern Suburbs | status=FT | goals=3 | SoT=NA | corners=NA | cards=NA | metrics=goals; xg; big
- Redlands United vs SC Wanderers | status=FT | goals=6 | SoT=NA | corners=NA | cards=NA | metrics=goals; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
