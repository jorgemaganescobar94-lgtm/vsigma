# vSIGMA Post-Match Stat Actuals - 2026-05-29

## Summary
- rows_final: 7
- verdict_counts: FINAL_ACTUALS_AVAILABLE=7
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- America de Cali vs Macara | status=FT | goals=0 | SoT=6 | corners=12 | cards=5 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Tigre vs Alianza Atletico | status=FT | goals=2 | SoT=7 | corners=5 | cards=8 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Boca Juniors vs U. Catolica | status=FT | goals=1 | SoT=3 | corners=11 | cards=4 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Cruzeiro vs Barcelona SC | status=FT | goals=4 | SoT=10 | corners=8 | cards=6 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- TransINVEST Vilnius vs Hegelmann Litauen | status=FT | goals=3 | SoT=NA | corners=NA | cards=NA | metrics=goals; xg; big
- Masr vs Kahraba Ismailia | status=FT | goals=2 | SoT=12 | corners=9 | cards=3 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- El Mokawloon vs Future FC | status=FT | goals=4 | SoT=12 | corners=16 | cards=NA | metrics=goals; sot; shots; corners; fouls; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
