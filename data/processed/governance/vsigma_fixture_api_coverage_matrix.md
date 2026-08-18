# vSIGMA Fixture API Coverage Matrix v3 - 2026-08-18

## Summary
- fixtures_reviewed: 14
- api_readiness_gates: LOW_COVERAGE_NO_BET=11; EARLY_WATCH_MORE_DATA_REQUIRED=3
- lineup_coverage: NONE=9; NOT_DUE_YET=5
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=14
- recent_stats_coverage: NONE=10; FULL=4
- injuries_coverage: NONE=12; FULL=2
- standings_coverage: NONE=12; FULL=1; PARTIAL=1
- odds_coverage: NONE=10; FULL=4
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Independ. Rivadavia vs Fluminense | gate=EARLY_WATCH_MORE_DATA_REQUIRED | score=80.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=FULL | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE
- Fenerbahçe vs Lyon | gate=EARLY_WATCH_MORE_DATA_REQUIRED | score=80.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET; standings_coverage=NONE
- Dinamo Zagreb vs Viking | gate=EARLY_WATCH_MORE_DATA_REQUIRED | score=80.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NOT_DUE_YET; standings_coverage=NONE
- Deportivo Recoleta vs Boca Juniors | gate=LOW_COVERAGE_NO_BET | score=62.5 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=NONE | missing=lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE
- Levski Sofia vs AEK Athens FC | gate=LOW_COVERAGE_NO_BET | score=45.0 | lineups=NOT_DUE_YET | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=FULL | missing=recent_stats_coverage=NONE; lineup_coverage=NOT_DUE_YET; injuries_coverage=NONE; standings_coverage=NONE
- Hapoel Acre vs Maccabi Kiryat Gat | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Hapoel Afula vs Ashdod | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Hapoel Kfar Shalem vs Kafr Qasim | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Hapoel Ra'anana vs Maccabi Ahi Nazareth | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Hapoel Rishon LeZion vs Hapoel Kfar Saba | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ironi Modi'in vs Maccabi Herzliya | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Maccabi Bnei Raina vs Bnei Yehuda | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Maccabi Kabilio Jaffa vs Kiryat Yam SC | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Londrina vs Atletico Goianiense | gate=LOW_COVERAGE_NO_BET | score=20.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
