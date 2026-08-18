# vSIGMA Post-Match Stat Actuals - 2026-08-18

## Summary
- rows_final: 2
- verdict_counts: FINAL_ACTUALS_AVAILABLE=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- Dinamo Zagreb vs Viking | status=FT | goals=4 | SoT=7 | corners=12 | cards=2 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Fenerbahçe vs Lyon | status=FT | goals=2 | SoT=10 | corners=3 | cards=3 | metrics=goals; sot; shots; corners; cards; fouls; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
