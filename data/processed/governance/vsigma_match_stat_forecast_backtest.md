# vSIGMA Match Statistical Forecast Backtest - 2026-05-25

## Summary
- rows_checked: 6
- forecast_grade_counts: NO_ACTUALS_YET=3; D_RANGE_WEAK=2; B_RANGE_GOOD=1
- total_goals_hit_counts: MISS=3; ACTUAL_UNAVAILABLE=3
- total_sot_hit_counts: HIT=3; ACTUAL_UNAVAILABLE=3
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- IF Elfsborg vs BK Hacken | status=FT | goals_actual=2 vs pred=2.35-3.90 (MISS) | SoT_actual=9 vs pred=6-11 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- SC Paderborn 07 vs VfL Wolfsburg | status=ET | goals_actual=NA vs pred=2.65-4.35 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-14 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- IFK Goteborg vs Mjallby AIF | status=FT | goals_actual=2 vs pred=2.40-3.98 (MISS) | SoT_actual=13 vs pred=8-14 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Sandefjord vs Fredrikstad | status=FT | goals_actual=2 vs pred=2.10-3.52 (MISS) | SoT_actual=9 vs pred=6-12 (HIT) | grade=B_RANGE_GOOD | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Botafogo SP vs Athletic Club | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- ST Mirren vs Partick | status=2H | goals_actual=NA vs pred=1.56-3.07 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=4-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
