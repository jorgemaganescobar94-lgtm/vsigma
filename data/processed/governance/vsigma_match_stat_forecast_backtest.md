# vSIGMA Match Statistical Forecast Backtest - 2026-05-29

## Summary
- rows_checked: 20
- forecast_grade_counts: NO_ACTUALS_YET=13; D_RANGE_WEAK=4; C_RANGE_MIXED=2; B_RANGE_GOOD=1
- total_goals_hit_counts: ACTUAL_UNAVAILABLE=13; MISS=4; HIT=3
- total_sot_hit_counts: ACTUAL_UNAVAILABLE=14; HIT=3; MISS=3
- calibration_note: v45.1 refuses to grade non-final fixtures.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Backtest Rows
- Fredrikstad vs Start | status=2H | goals_actual=NA vs pred=2.35-3.90 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-13 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Monza vs Catanzaro | status=1H | goals_actual=NA vs pred=2.30-3.83 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=8-14 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Valerenga vs Kristiansund BK | status=2H | goals_actual=NA vs pred=2.15-3.60 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-13 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Orgryte IS vs IF Elfsborg | status=2H | goals_actual=NA vs pred=2.10-3.52 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- America de Cali vs Macara | status=FT | goals_actual=0 vs pred=1.95-3.30 (MISS) | SoT_actual=6 vs pred=5-10 (HIT) | grade=C_RANGE_MIXED | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Cruzeiro vs Barcelona SC | status=FT | goals_actual=4 vs pred=1.81-3.07 (MISS) | SoT_actual=10 vs pred=5-11 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Tigre vs Alianza Atletico | status=FT | goals_actual=2 vs pred=1.51-2.62 (HIT) | SoT_actual=7 vs pred=4-9 (HIT) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Nice vs Saint Etienne | status=NS | goals_actual=NA vs pred=1.71-2.92 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-10 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Aalesund vs Ham-Kam | status=2H | goals_actual=NA vs pred=2.30-4.07 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Rosenborg vs Bodo/Glimt | status=2H | goals_actual=NA vs pred=1.92-3.45 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=7-14 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Boca Juniors vs U. Catolica | status=FT | goals_actual=1 vs pred=1.87-3.38 (MISS) | SoT_actual=3 vs pred=5-11 (MISS) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- Brann vs Sarpsborg 08 FF | status=2H | goals_actual=NA vs pred=2.16-3.84 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- KFUM Oslo vs Tromso | status=2H | goals_actual=NA vs pred=2.02-3.61 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=6-12 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- El Mokawloon vs Future FC | status=FT | goals_actual=4 vs pred=1.58-3.12 (MISS) | SoT_actual=12 vs pred=5-11 (MISS) | grade=D_RANGE_WEAK | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_fouls
- Ghazl El Mehalla vs Haras El Hodood | status=2H | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- Masr vs Kahraba Ismailia | status=FT | goals_actual=2 vs pred=1.58-3.12 (HIT) | SoT_actual=12 vs pred=5-11 (MISS) | grade=B_RANGE_GOOD | metrics=home_goals; away_goals; total_goals; total_sot; total_corners; total_cards; total_fouls
- National Bank of Egypt vs Al Ittihad | status=2H | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- FK Trakai vs Suduva Marijampole | status=2H | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none
- TransINVEST Vilnius vs Hegelmann Litauen | status=FT | goals_actual=3 vs pred=1.58-3.12 (HIT) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=C_RANGE_MIXED | metrics=home_goals; away_goals; total_goals
- Cde Juventud Italiana vs Tecnico Universitario | status=NS | goals_actual=NA vs pred=1.58-3.12 (ACTUAL_UNAVAILABLE) | SoT_actual=NA vs pred=5-11 (ACTUAL_UNAVAILABLE) | grade=NO_ACTUALS_YET | metrics=none

## Guardrails
- This report grades only final fixtures: FT/AET/PEN.
- It does not infer missing corners/cards/fouls from recent averages or placeholder zeros.
- Use this to calibrate v44 forecasts before connecting them to market execution.
