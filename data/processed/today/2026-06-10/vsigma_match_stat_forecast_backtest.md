# vSIGMA Match Statistical Forecast Backtest - 2026-06-10

## Summary
- rows_checked: 2
- forecast_grade_counts: NO_ACTUALS_YET=1; A_RANGE_STRONG=1
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=1; HIT=1
- total_sot_hit_counts: ACTUAL_UNAVAILABLE=2
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- Malaga vs Las Palmas | status=NS | goals_actual=NA vs pred=2.30-3.83 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Cape Town City vs Magesi | status=FT | goals_actual=2 vs pred=1.58-3.12 (HIT) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=A_RANGE_STRONG | metrics=home_goals; away_goals; total_goals

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
