# vSIGMA Match Statistical Forecast Backtest - 2026-05-28

## Summary
- rows_checked: 3
- forecast_grade_counts: NO_ACTUALS_YET=3
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=3
- total_sot_hit_counts: ACTUAL_UNAVAILABLE=3
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- Cerro Porteno vs Sporting Cristal | status=NS | goals_actual=NA vs pred=1.66-2.84 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Palmeiras vs Junior | status=NS | goals_actual=NA vs pred=1.49-2.76 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Casa Pia vs Torreense | status=NS | goals_actual=NA vs pred=1.42-2.83 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=4-9 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
