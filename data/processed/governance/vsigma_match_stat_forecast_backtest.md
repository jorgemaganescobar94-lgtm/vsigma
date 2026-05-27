# vSIGMA Match Statistical Forecast Backtest - 2026-05-27

## Summary
- rows_checked: 16
- forecast_grade_counts: NO_ACTUALS_YET=10; D_RANGE_WEAK=4; C_RANGE_MIXED=2
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=10; MISS=5; HIT=1
- total_sot_hit_counts: ACTUAL_UNAVAILABLE=10; MISS=4; HIT=2
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- Flamengo vs Cusco | status=FT | goals_actual=3 vs pred=2.41-3.72 (HIT) | SoT_actual=16 vs pred=8-13 (MISS) | grade=C_RANGE_MIXED | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_fouls
- Universitario vs Deportes Tolima | status=FT | goals_actual=0 vs pred=2.15-3.35 (MISS) | SoT_actual=5 vs pred=7-12 (MISS) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_fouls
- Santos vs Deportivo Cuenca | status=FT | goals_actual=3 vs pred=1.84-2.91 (MISS) | SoT_actual=7 vs pred=6-11 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Estudiantes L.P. vs Independiente Medellin | status=FT | goals_actual=1 vs pred=1.69-2.69 (MISS) | SoT_actual=9 vs pred=6-10 (HIT) | grade=C_RANGE_MIXED | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- San Lorenzo vs Deportivo Recoleta | status=FT | goals_actual=1 vs pred=1.43-2.32 (MISS) | SoT_actual=11 vs pred=6-10 (MISS) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Club Nacional vs Coquimbo Unido | status=FT | goals_actual=1 vs pred=2.69-4.43 (MISS) | SoT_actual=6 vs pred=8-14 (MISS) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Racing Club vs Independiente Petrolero | status=NS | goals_actual=NA vs pred=2.20-3.67 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-14 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Crystal Palace vs Rayo Vallecano | status=NS | goals_actual=NA vs pred=2.05-3.45 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Independiente del Valle vs Rosario Central | status=NS | goals_actual=NA vs pred=2.05-3.45 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Vasco DA Gama vs Barracas Central | status=NS | goals_actual=NA vs pred=1.56-2.69 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-13 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Libertad Asuncion vs UCV | status=NS | goals_actual=NA vs pred=2.35-4.15 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-13 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Olimpia vs A. Italiano | status=NS | goals_actual=NA vs pred=2.16-3.84 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Caracas FC vs Botafogo | status=NS | goals_actual=NA vs pred=2.16-3.84 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-13 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Atletico-MG vs Puerto Cabello | status=NS | goals_actual=NA vs pred=2.02-3.61 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Cienciano vs Juventud | status=NS | goals_actual=NA vs pred=1.78-3.22 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Cuniburo vs Orense SC | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
