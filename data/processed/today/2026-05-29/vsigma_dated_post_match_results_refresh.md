# vSIGMA Dated Post-Match Results Refresh - 2026-05-29

## Summary
- rows_reported: 3
- status_counts: FT=2; NS=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Rows
- America de Cali vs Macara | status=FT | goals=0-0 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Boca Juniors vs U. Catolica | status=FT | goals=0-1 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Monza vs Catanzaro | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at

## Guardrails
- If API credentials are missing, this step writes a diagnostic report and exits successfully.
- This refresh only writes dated outputs and does not infer missing stats.
