# vSIGMA Post-Match Stat Actuals - 2026-05-27

## Summary
- rows_final: 6
- verdict_counts: FINAL_ACTUALS_AVAILABLE=6
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- San Lorenzo vs Deportivo Recoleta | status=FT | goals=1 | SoT=11 | corners=11 | cards=7 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Santos vs Deportivo Cuenca | status=FT | goals=3 | SoT=7 | corners=7 | cards=7 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Estudiantes L.P. vs Independiente Medellin | status=FT | goals=1 | SoT=9 | corners=14 | cards=4 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Flamengo vs Cusco | status=FT | goals=3 | SoT=16 | corners=11 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big
- Club Nacional vs Coquimbo Unido | status=FT | goals=1 | SoT=6 | corners=10 | cards=6 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Universitario vs Deportes Tolima | status=FT | goals=0 | SoT=5 | corners=12 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
