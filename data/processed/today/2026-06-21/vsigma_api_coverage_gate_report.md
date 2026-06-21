# vSIGMA API Coverage Gate Applied to Board v2 - 2026-06-21

## Summary
- rows_reviewed: 11
- gate_actions: NO_BET_CONFIRMED=11
- auto_apply: NO
- production_change: NO

## Gate Rows
- Avai vs Cuiaba | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- CRB vs Fortaleza EC | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Goias vs Operario-PR | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- São Bernardo vs Juventude | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Džiugas Telšiai vs Suduva Marijampole | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Barra vs Amazonas | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Brusque vs Floresta | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Caxias vs Maringá | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ferroviária vs Inter De Limeira | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ituano vs Figueirense | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Maranhão vs Paysandu | api_gate=LOW_COVERAGE_NO_BET | action=NO_BET_CONFIRMED | decision=NO_BET->NO_BET | permission=NO_BET->NO | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Probable XI can support early planning, never final lock by itself.
- Official lineup remains primary truth.
- It does not create new picks or execute bets.
- It does not fabricate unavailable data.
