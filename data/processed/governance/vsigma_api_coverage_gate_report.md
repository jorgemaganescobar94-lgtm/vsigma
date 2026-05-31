# vSIGMA API Coverage Gate Applied to Board v2 - 2026-05-31

## Summary
- rows_reviewed: 24
- gate_actions: NO_BET_CONFIRMED=9; EARLY_WATCH_ONLY=7; EARLY_PRELOCK_REQUIRED=7; DOWNGRADED_TO_NO_BET=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Cordoba vs Huesca | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- RB Bragantino vs Internacional | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Almeria vs Valladolid | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Vasco DA Gama vs Atletico-MG | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Leganes vs Mirandes | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=STAT_WATCH_ONLY->STAT_WATCH_ONLY | permission=STAT_WATCH_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Zaragoza vs Malaga | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=STAT_WATCH_ONLY->STAT_WATCH_ONLY | permission=STAT_WATCH_ONLY->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Vasteras SK FK vs IFK Goteborg | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=STAT_WATCH_ONLY->STAT_WATCH_ONLY | permission=STAT_WATCH_ONLY->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Racing Santander vs Cadiz | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=STAT_WATCH_ONLY->STAT_WATCH_ONLY | permission=STAT_WATCH_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Castellón vs Eibar | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=STAT_WATCH_ONLY->STAT_WATCH_ONLY | permission=STAT_WATCH_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- BK Hacken vs Hammarby FF | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Degerfors IF vs IF Brommapojkarna | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Burgos vs FC Andorra | api_gate=LOW_COVERAGE_NO_BET | action=DOWNGRADED_TO_NO_BET | decision=NO_BET_OR_WATCH->NO_BET | permission=NO_BET_OR_WATCH->NO | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; odds_coverage=NONE
- Gent vs Genk | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Palmeiras vs Chapecoense-sc | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Deportivo La Coruna vs Las Palmas | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=NO_BET->NO_BET | permission=NO_BET->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Ceara vs Operario-PR | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Londrina vs Vila Nova | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- São Bernardo vs Novorizontino | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- AC Oulu vs FF Jaro | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Kauno Žalgiris vs FK Zalgiris Vilnius | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Anápolis vs Maranhão | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Guarani Campinas vs Amazonas | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Inter De Limeira vs Ypiranga-RS | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Santa Cruz vs Ferroviária | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
