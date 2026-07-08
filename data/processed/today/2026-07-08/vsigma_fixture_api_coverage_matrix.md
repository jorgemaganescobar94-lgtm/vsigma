# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-08

## Summary
- fixtures_reviewed: 9
- api_readiness_gates: LOW_COVERAGE_NO_BET=9
- lineup_coverage: NOT_DUE_YET=7; NONE=2
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=9
- recent_stats_coverage: NONE=9
- injuries_coverage: NONE=9
- standings_coverage: NONE=9
- odds_coverage: FULL=7; NONE=2
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Kairat Almaty vs Sutjeska | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Zira vs Torpedo Kutaisi | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- FC Differdange 03 vs Ilves | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- ML Vitebsk vs Universitatea Craiova | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Flora Tallinn vs Saburtalo | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Petrocub vs Egnatia Rrogozhinë | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- GAP Connah S Quay FC vs Ballkani | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Saint-Laurent vs Forge | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Santo Domingo vs Independiente del Valle | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
