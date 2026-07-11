# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-11

## Summary
- fixtures_reviewed: 13
- api_readiness_gates: LOW_COVERAGE_NO_BET=5; EARLY_CANDIDATE_PRELOCK_REQUIRED=4; WAIT_LINEUPS_OR_LIVE_ONLY=4
- lineup_coverage: NONE=9; NOT_DUE_YET=4
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=13
- recent_stats_coverage: FULL=8; NONE=5
- injuries_coverage: NONE=8; FULL=5
- standings_coverage: FULL=8; NONE=5
- odds_coverage: FULL=8; NONE=5
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Orgryte IS vs BK Hacken | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Aalesund vs Molde | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Tromso vs Valerenga | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Fredrikstad vs Lillestrom | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NONE
- Gwangju FC vs Pohang Steelers | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Ulsan Hyundai FC vs Jeonbuk Motors | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Mjallby AIF vs AIK Stockholm | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Gimcheon Sangmu FC vs Bucheon FC 1995 | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Kauno Žalgiris vs Panevėžys | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Caxias vs Floresta | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Gnistan vs Mariehamn | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Lahti vs HJK Helsinki | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Turku PS vs AC Oulu | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
