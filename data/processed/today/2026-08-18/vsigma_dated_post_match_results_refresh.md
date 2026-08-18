# vSIGMA Dated Post-Match Results Refresh - 2026-08-18

## Summary
- rows_reported: 3
- status_counts: FT=2; HT=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Rows
- Dinamo Zagreb vs Viking | status=FT | goals=2-2 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Fenerbahçe vs Lyon | status=FT | goals=1-1 | stats=STATS_FETCHED | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;score_fulltime_home;score_fulltime_away;results_last_refresh_at;actual_home_sot;actual_away_sot;actual_total_sot;actual_home_shots;actual_away_shots;actual_total_shots;actual_home_corners;actual_away_corners;actual_total_corners;actual_home_cards;actual_away_cards;actual_total_cards;actual_home_fouls;actual_away_fouls;actual_total_fouls
- Independ. Rivadavia vs Fluminense | status=HT | goals=0-0 | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;fixture_status_elapsed;goals_home;goals_away;results_last_refresh_at

## Guardrails
- If API credentials are missing, this step writes a diagnostic report and exits successfully.
- This refresh only writes dated outputs and does not infer missing stats.
