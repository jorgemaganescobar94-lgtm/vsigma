# vSIGMA Match Statistical Forecast Backtest - 2026-05-25

## Summary
- rows_graded: 6
- forecast_grade_counts: D_RANGE_WEAK=6
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=6
- total_sot_hit_counts: MISS=6
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- IF Elfsborg vs BK Hacken | status=NS | goals_actual= vs pred=2.35-3.90 (ACTUAL_UNAVAILABLE) | SoT_actual=0 vs pred=6-11 (MISS) | grade=D_RANGE_WEAK | metrics=total_sot
- SC Paderborn 07 vs VfL Wolfsburg | status=NS | goals_actual= vs pred=2.65-4.35 (ACTUAL_UNAVAILABLE) | SoT_actual=0 vs pred=7-14 (MISS) | grade=D_RANGE_WEAK | metrics=total_sot
- IFK Goteborg vs Mjallby AIF | status=NS | goals_actual= vs pred=2.40-3.98 (ACTUAL_UNAVAILABLE) | SoT_actual=0 vs pred=8-14 (MISS) | grade=D_RANGE_WEAK | metrics=total_sot
- Sandefjord vs Fredrikstad | status=NS | goals_actual= vs pred=2.10-3.52 (ACTUAL_UNAVAILABLE) | SoT_actual=0 vs pred=6-12 (MISS) | grade=D_RANGE_WEAK | metrics=total_sot
- Botafogo SP vs Athletic Club | status=NS | goals_actual= vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=0 vs pred=5-11 (MISS) | grade=D_RANGE_WEAK | metrics=total_sot
- ST Mirren vs Partick | status=NS | goals_actual= vs pred=1.56-3.07 (ACTUAL_UNAVAILABLE) | SoT_actual=0 vs pred=4-10 (MISS) | grade=D_RANGE_WEAK | metrics=total_sot

## Guardrails
- This report grades only actual metrics present in dated post-match files.
- It does not infer missing corners/cards/fouls from recent averages.
- Use this to calibrate v44 forecasts before connecting them to market execution.
