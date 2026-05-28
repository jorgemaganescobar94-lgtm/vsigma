# vSIGMA Post-Match Stat Actuals - 2026-05-28

## Summary
- rows_final: 9
- verdict_counts: FINAL_ACTUALS_AVAILABLE=9
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- RB Bragantino vs Carabobo FC | status=FT | goals=2 | SoT=11 | corners=9 | cards=5 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- River Plate vs Blooming | status=FT | goals=3 | SoT=10 | corners=8 | cards=2 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Bolívar vs Independ. Rivadavia | status=FT | goals=4 | SoT=13 | corners=10 | cards=6 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Corinthians vs Platense | status=FT | goals=2 | SoT=10 | corners=9 | cards=4 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Fluminense vs Deportivo La Guaira | status=FT | goals=4 | SoT=6 | corners=3 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big
- Penarol vs Santa Fe | status=FT | goals=1 | SoT=7 | corners=11 | cards=4 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Petrojet vs El Gouna FC | status=FT | goals=3 | SoT=9 | corners=9 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big
- El Geish vs Wadi Degla | status=FT | goals=2 | SoT=NA | corners=NA | cards=NA | metrics=goals; shots; fouls; xg; big
- Ismaily SC vs Pharco | status=FT | goals=3 | SoT=10 | corners=3 | cards=5 | metrics=goals; sot; shots; corners; cards; fouls; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
