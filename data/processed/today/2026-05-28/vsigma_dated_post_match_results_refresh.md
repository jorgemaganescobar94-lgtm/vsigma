# vSIGMA Dated Post-Match Results Refresh - 2026-05-28

## Summary
- rows_reported: 12
- status_counts: FT=9; NS=3
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Rows
- RB Bragantino vs Carabobo FC | status=FT | goals=2-0 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- River Plate vs Blooming | status=FT | goals=3-0 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Bolívar vs Independ. Rivadavia | status=FT | goals=1-3 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Corinthians vs Platense | status=FT | goals=0-2 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Fluminense vs Deportivo La Guaira | status=FT | goals=3-1 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Penarol vs Santa Fe | status=FT | goals=0-1 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Petrojet vs El Gouna FC | status=FT | goals=1-2 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_fouls;actual_away_fouls;actual_total_fouls
- El Geish vs Wadi Degla | status=FT | goals=0-2 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Ismaily SC vs Pharco | status=FT | goals=1-2 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Casa Pia vs Torreense | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Cerro Porteno vs Sporting Cristal | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Palmeiras vs Junior | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at

## Guardrails
- If API credentials are missing, this step writes a diagnostic report and exits successfully.
- This refresh only writes dated outputs and does not infer missing stats.
