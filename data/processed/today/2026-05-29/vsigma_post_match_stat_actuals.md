# vSIGMA Post-Match Stat Actuals - 2026-05-29

## Summary
- rows_final: 2
- verdict_counts: FINAL_ACTUALS_AVAILABLE=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Actual Rows
- America de Cali vs Macara | status=FT | goals=0 | SoT=6 | corners=12 | cards=5 | metrics=goals; sot; shots; corners; cards; fouls; xg; big
- Boca Juniors vs U. Catolica | status=FT | goals=1 | SoT=3 | corners=11 | cards=4 | metrics=goals; sot; shots; corners; cards; fouls; xg; big

## Guardrails
- This normalizer does not infer missing shots/corners/cards/fouls from recent averages.
- It only exposes final fixture actuals that exist in dated source files.
