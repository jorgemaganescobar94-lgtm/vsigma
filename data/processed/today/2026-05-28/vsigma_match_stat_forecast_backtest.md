# vSIGMA Match Statistical Forecast Backtest - 2026-05-28

## Summary
- rows_checked: 12
- forecast_grade_counts: NO_ACTUALS_YET=6; D_RANGE_WEAK=3; B_RANGE_GOOD=3
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=6; MISS=4; HIT=2
- total_sot_hit_counts: HIT=6; ACTUAL_UNAVAILABLE=6
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- River Plate vs Blooming | status=FT | goals_actual=3 vs pred=2.05-3.45 (HIT) | SoT_actual=10 vs pred=7-14 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Cerro Porteno vs Sporting Cristal | status=NS | goals_actual=NA vs pred=1.66-2.84 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Corinthians vs Platense | status=FT | goals_actual=2 vs pred=1.41-2.46 (HIT) | SoT_actual=10 vs pred=7-13 (HIT) | grade=B_RANGE_GOOD | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- RB Bragantino vs Carabobo FC | status=FT | goals_actual=2 vs pred=2.35-4.15 (MISS) | SoT_actual=11 vs pred=7-14 (HIT) | grade=B_RANGE_GOOD | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Bolívar vs Independ. Rivadavia | status=FT | goals_actual=4 vs pred=1.97-3.53 (MISS) | SoT_actual=13 vs pred=7-13 (HIT) | grade=B_RANGE_GOOD | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Penarol vs Santa Fe | status=FT | goals_actual=1 vs pred=1.83-3.30 (MISS) | SoT_actual=7 vs pred=6-12 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Fluminense vs Deportivo La Guaira | status=FT | goals_actual=4 vs pred=1.63-2.99 (MISS) | SoT_actual=6 vs pred=6-12 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_fouls
- Palmeiras vs Junior | status=NS | goals_actual=NA vs pred=1.49-2.76 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- El Geish vs Wadi Degla | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Ismaily SC vs Pharco | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Petrojet vs El Gouna FC | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Casa Pia vs Torreense | status=NS | goals_actual=NA vs pred=1.42-2.83 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=4-9 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
