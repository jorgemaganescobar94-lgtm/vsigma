# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-14

## Summary
- fixtures_reviewed: 11
- api_readiness_gates: LOW_COVERAGE_NO_BET=11
- lineup_coverage: NOT_DUE_YET=11
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=11
- recent_stats_coverage: NONE=11
- injuries_coverage: NONE=11
- standings_coverage: NONE=11
- odds_coverage: FULL=11
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Gyori ETO FC vs Vikingur Reykjavik | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Inter Club d'Escaldes vs Lincoln Red Imps FC | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Riga vs Ararat-Armenia | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- The New Saints vs Sabah FA | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- KuPS vs Vardar Skopje | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Saburtalo vs Flora Tallinn | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Levski Sofia vs Borac Banja Luka | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Drita vs Kauno Žalgiris | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Shamrock Rovers vs Floriana | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- La Fiorita vs UNA Strassen | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Larne vs Tre Fiori | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
