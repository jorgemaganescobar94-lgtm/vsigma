# vSIGMA Post-Match Stat Actuals - 2026-05-25

## Summary
- rows_final: 4
- verdict_counts: FINAL_ACTUALS_AVAILABLE=4
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- IF Elfsborg vs BK Hacken | status=FT | goals=2 | SoT=9 | corners=7 | cards=4 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- IFK Goteborg vs Mjallby AIF | status=FT | goals=2 | SoT=13 | corners=5 | cards=10 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Sandefjord vs Fredrikstad | status=FT | goals=2 | SoT=9 | corners=11 | cards=5 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- ST Mirren vs Partick | status=FT | goals=1 | SoT=NA | corners=NA | cards=5 | metrics=goals; cards; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
