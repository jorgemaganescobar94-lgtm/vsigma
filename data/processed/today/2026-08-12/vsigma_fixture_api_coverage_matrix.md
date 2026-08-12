# vSIGMA Fixture API Coverage Matrix v3 - 2026-08-12

## Summary
- fixtures_reviewed: 15
- api_readiness_gates: LOW_COVERAGE_NO_BET=15
- lineup_coverage: NONE=8; NOT_DUE_YET=7
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=15
- recent_stats_coverage: NONE=15
- injuries_coverage: NONE=15
- standings_coverage: NONE=15
- odds_coverage: NONE=8; FULL=7
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- FC Copenhagen vs Debreceni VSC | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Platense vs Coquimbo Unido | gate=LOW_COVERAGE_NO_BET | score=30.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Deportes Tolima vs Independiente del Valle | gate=LOW_COVERAGE_NO_BET | score=25.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE
- Palmeiras vs Cerro Porteno | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- RB Bragantino vs Atletico-MG | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Rapid Vienna vs Paide | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Tigre vs Atletico Torque | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- GKS Katowice vs Hapoel Tel Aviv | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Arkadag vs Goa | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- East Bengal II vs Al Arabi | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Amazulu vs Orlando Pirates | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Durban City vs Golden Arrows | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Kaizer Chiefs vs Sekhukhune United | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Milford FC vs Siwelele | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- La Unión vs Aucas | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
