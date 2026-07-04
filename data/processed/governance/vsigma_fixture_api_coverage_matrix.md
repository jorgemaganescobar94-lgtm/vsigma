# vSIGMA Fixture API Coverage Matrix v3 - 2026-07-04

## Summary
- fixtures_reviewed: 17
- api_readiness_gates: LOW_COVERAGE_NO_BET=12; WAIT_LINEUPS_OR_LIVE_ONLY=4; EARLY_WATCH_MORE_DATA_REQUIRED=1
- lineup_coverage: NONE=16; PROBABLE_LOW=1
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=16; PROBABLE_XI_CONSENSUS_LOW=1
- recent_stats_coverage: NONE=12; FULL=5
- injuries_coverage: NONE=15; FULL=2
- standings_coverage: NONE=12; FULL=5
- odds_coverage: NONE=12; FULL=5
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Halmstad vs Vasteras SK FK | gate=EARLY_WATCH_MORE_DATA_REQUIRED | score=88.0 | lineups=PROBABLE_LOW | probable=PROBABLE_XI_CONSENSUS_LOW | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=PROBABLE_LOW
- Degerfors IF vs Malmo FF | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NONE
- Jeonbuk Motors vs Gangwon FC | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Daejeon Citizen vs Bucheon FC 1995 | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- FC Anyang vs Pohang Steelers | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Panevėžys vs Hegelmann Litauen | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Criciuma vs Sport Recife | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Londrina vs CRB | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Novorizontino vs Atletico Goianiense | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Confiança vs Barra | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Maranhão vs Inter De Limeira | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Maringá vs Volta Redonda | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Santa Cruz vs Ituano | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- FF Jaro vs Ilves | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Lahti vs Gnistan | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- SJK vs Turku PS | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- VPS vs Mariehamn | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
