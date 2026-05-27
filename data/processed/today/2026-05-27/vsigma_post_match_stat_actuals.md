# vSIGMA Post-Match Stat Actuals - 2026-05-27

## Summary
- rows_final: 2
- verdict_counts: FINAL_ACTUALS_AVAILABLE=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- Flamengo vs Cusco | status=FT | goals=3 | SoT=16 | corners=11 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big
- Club Nacional vs Coquimbo Unido | status=FT | goals=1 | SoT=6 | corners=10 | cards=6 | metrics=goals; sot; shots; corners; cards; fouls; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
