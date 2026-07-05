# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-05

## Summary
- fixtures_reviewed: 8
- api_readiness_gates: LOW_COVERAGE_NO_BET=8
- lineup_coverage: NONE=7; NOT_DUE_YET=1
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=8
- recent_stats_coverage: NONE=5; FULL=3
- injuries_coverage: NONE=5; FULL=3
- standings_coverage: PARTIAL=6; NONE=2
- odds_coverage: NONE=8
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Gwangju FC vs Ulsan Hyundai FC | gate=LOW_COVERAGE_NO_BET | score=27.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- FC Seoul vs Incheon United | gate=LOW_COVERAGE_NO_BET | score=27.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- IFK Goteborg vs AIK Stockholm | gate=LOW_COVERAGE_NO_BET | score=62.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=NONE | missing=lineup_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- IF Elfsborg vs Hammarby FF | gate=LOW_COVERAGE_NO_BET | score=77.5 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=NONE | missing=lineup_coverage=NOT_DUE_YET; standings_coverage=PARTIAL; odds_coverage=NONE
- Kalmar FF vs Orgryte IS | gate=LOW_COVERAGE_NO_BET | score=62.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=NONE | missing=lineup_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- Gimcheon Sangmu FC vs Jeju United FC | gate=LOW_COVERAGE_NO_BET | score=27.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- Šiauliai vs FK Zalgiris Vilnius | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ypiranga-RS vs Paysandu | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
