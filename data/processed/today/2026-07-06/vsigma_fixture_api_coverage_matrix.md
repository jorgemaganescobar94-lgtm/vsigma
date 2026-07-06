# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-06

## Summary
- fixtures_reviewed: 6
- api_readiness_gates: LOW_COVERAGE_NO_BET=4; EARLY_CANDIDATE_PRELOCK_REQUIRED=2
- lineup_coverage: NONE=4; NOT_DUE_YET=2
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=6
- recent_stats_coverage: NONE=4; FULL=2
- injuries_coverage: NONE=4; FULL=2
- standings_coverage: NONE=4; FULL=2
- odds_coverage: NONE=4; FULL=2
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- BK Hacken vs Djurgardens IF | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- IF Brommapojkarna vs Gais | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Suduva Marijampole vs TransINVEST Vilnius | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Botafogo SP vs Avai | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Vila Nova vs São Bernardo | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Brusque vs Figueirense | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
