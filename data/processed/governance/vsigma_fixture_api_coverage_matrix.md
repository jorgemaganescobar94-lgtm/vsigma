# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-31

## Summary
- fixtures_reviewed: 4
- api_readiness_gates: EARLY_CANDIDATE_PRELOCK_REQUIRED=2; LOW_COVERAGE_NO_BET=2
- lineup_coverage: NOT_DUE_YET=4
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=4
- recent_stats_coverage: FULL=2; NONE=2
- injuries_coverage: FULL=2; NONE=2
- standings_coverage: FULL=3; NONE=1
- odds_coverage: FULL=4
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Bodo/Glimt vs Lillestrom | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Dundee Utd vs Rangers | gate=LOW_COVERAGE_NO_BET | score=55.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Valerenga vs Ham-Kam | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Lask Linz vs Grazer AK | gate=LOW_COVERAGE_NO_BET | score=40.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
