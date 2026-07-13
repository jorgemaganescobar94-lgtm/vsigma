# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-13

## Summary
- fixtures_reviewed: 3
- api_readiness_gates: LOW_COVERAGE_NO_BET=2; EARLY_CANDIDATE_PRELOCK_REQUIRED=1
- lineup_coverage: NONE=2; NOT_DUE_YET=1
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=3
- recent_stats_coverage: NONE=2; FULL=1
- injuries_coverage: NONE=2; FULL=1
- standings_coverage: NONE=2; FULL=1
- odds_coverage: NONE=2; FULL=1
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Djurgardens IF vs Halmstad | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- America Mineiro vs Londrina | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- AO Itabaiana vs Brusque | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
