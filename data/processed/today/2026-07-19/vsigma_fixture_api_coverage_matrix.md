# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-19

## Summary
- fixtures_reviewed: 8
- api_readiness_gates: EARLY_CANDIDATE_PRELOCK_REQUIRED=3; LOW_COVERAGE_NO_BET=3; WAIT_LINEUPS_OR_LIVE_ONLY=2
- lineup_coverage: NONE=5; NOT_DUE_YET=3
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=8
- recent_stats_coverage: FULL=5; NONE=3
- injuries_coverage: NONE=5; FULL=3
- standings_coverage: FULL=5; NONE=3
- odds_coverage: FULL=5; NONE=3
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Hammarby FF vs Degerfors IF | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Halmstad vs BK Hacken | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- IF Elfsborg vs Sirius | gate=EARLY_CANDIDATE_PRELOCK_REQUIRED | score=95.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET
- Bucheon FC 1995 vs FC Seoul | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- FC Anyang vs Gwangju FC | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Džiugas Telšiai vs Banga | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- FK Zalgiris Vilnius vs TransINVEST Vilnius | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- FF Jaro vs Inter Turku | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
