# vSIGMA Fixture API Coverage Matrix v3 - 2026-06-09

## Summary
- fixtures_reviewed: 3
- api_readiness_gates: LOW_COVERAGE_NO_BET=2; EARLY_WATCH_MORE_DATA_REQUIRED=1
- lineup_coverage: NONE=2; NOT_DUE_YET=1
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=3
- recent_stats_coverage: NONE=2; FULL=1
- injuries_coverage: NONE=3
- standings_coverage: NONE=2; FULL=1
- odds_coverage: NONE=2; FULL=1
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Almeria vs Castellón | gate=EARLY_WATCH_MORE_DATA_REQUIRED | score=80.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Nautico Recife vs Fortaleza EC | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ponte Preta vs Cuiaba | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
