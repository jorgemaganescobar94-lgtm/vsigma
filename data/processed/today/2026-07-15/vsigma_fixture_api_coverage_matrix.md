# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-15

## Summary
- fixtures_reviewed: 6
- api_readiness_gates: LOW_COVERAGE_NO_BET=6
- lineup_coverage: NOT_DUE_YET=6
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=6
- recent_stats_coverage: NONE=6
- injuries_coverage: NONE=6
- standings_coverage: NONE=6
- odds_coverage: FULL=6
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Sutjeska vs Kairat Almaty | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Atert Bissen vs KI Klaksvik | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Universitatea Craiova vs ML Vitebsk | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Egnatia Rrogozhinë vs Petrocub | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Malisheva vs Vllaznia Shkodër | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Dečić vs FK Liepaja | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
