# vSIGMA API Coverage Gate Applied to Board v2 - 2026-05-29

## Summary
- rows_reviewed: 20
- gate_actions: EARLY_PRELOCK_REQUIRED=8; NO_BET_CONFIRMED=7; PREMATCH_BLOCKED_KEEP_WATCH=4; EARLY_WATCH_ONLY=1
- auto_apply: NO
- production_change: NO

## Gate Rows
- Monza vs Catanzaro | api_gate=EARLY_WATCH_MORE_DATA_REQUIRED | action=EARLY_WATCH_ONLY | decision=LIVE_ONLY->LIVE_ONLY | permission=LIVE_ONLY->NO_PREMATCH | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Valerenga vs Kristiansund BK | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=STAT_WATCH_ONLY->STAT_WATCH_ONLY | permission=STAT_WATCH_ONLY->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Fredrikstad vs Start | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Orgryte IS vs IF Elfsborg | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Aalesund vs Ham-Kam | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Tigre vs Alianza Atletico | api_gate=WAIT_LINEUPS_OR_LIVE_ONLY | action=PREMATCH_BLOCKED_KEEP_WATCH | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->NO_PREMATCH | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Rosenborg vs Bodo/Glimt | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- Cruzeiro vs Barcelona SC | api_gate=WAIT_LINEUPS_OR_LIVE_ONLY | action=PREMATCH_BLOCKED_KEEP_WATCH | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->NO_PREMATCH | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Boca Juniors vs U. Catolica | api_gate=WAIT_LINEUPS_OR_LIVE_ONLY | action=PREMATCH_BLOCKED_KEEP_WATCH | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->NO_PREMATCH | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Nice vs Saint Etienne | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET; standings_coverage=PARTIAL
- Brann vs Sarpsborg 08 FF | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- KFUM Oslo vs Tromso | api_gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | action=EARLY_PRELOCK_REQUIRED | decision=NO_BET_OR_WATCH->NO_BET_OR_WATCH | permission=NO_BET_OR_WATCH->PRELOCK_REQUIRED | missing=lineup_coverage=NOT_DUE_YET
- America de Cali vs Macara | api_gate=WAIT_LINEUPS_OR_LIVE_ONLY | action=PREMATCH_BLOCKED_KEEP_WATCH | decision=NO_BET->NO_BET | permission=NO_BET->NO_PREMATCH | missing=lineup_coverage=NONE; injuries_coverage=NONE
- El Mokawloon vs Future FC | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ghazl El Mehalla vs Haras El Hodood | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Masr vs Kahraba Ismailia | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- National Bank of Egypt vs Al Ittihad | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- FK Trakai vs Suduva Marijampole | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- TransINVEST Vilnius vs Hegelmann Litauen | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Cde Juventud Italiana vs Tecnico Universitario | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
