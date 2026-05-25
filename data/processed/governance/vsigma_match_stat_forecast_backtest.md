# vSIGMA Match Statistical Forecast Backtest - 2026-05-25

## Summary
- rows_checked: 6
- forecast_grade_counts: NO_ACTUALS_YET=6
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=6
- total_sot_hit_counts: ACTUAL_UNAVAILABLE=6
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- IF Elfsborg vs BK Hacken | status=NS | goals_actual=NA vs pred=2.35-3.90 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- SC Paderborn 07 vs VfL Wolfsburg | status=NS | goals_actual=NA vs pred=2.65-4.35 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-14 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- IFK Goteborg vs Mjallby AIF | status=NS | goals_actual=NA vs pred=2.40-3.98 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=8-14 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Sandefjord vs Fredrikstad | status=NS | goals_actual=NA vs pred=2.10-3.52 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Botafogo SP vs Athletic Club | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- ST Mirren vs Partick | status=NS | goals_actual=NA vs pred=1.56-3.07 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=4-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
