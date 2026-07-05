# vSIGMA API Board Candidate Bridge - 2026-07-05

- board_rows: 2
- lineup_rows: 40
- candidates_written: 0
- skipped_rows: 2
- board_source: data/processed/today/2026-07-05/vsigma_daily_execution_board.csv
- lineup_source: data/processed/today/2026-07-05/vsigma_forced_api_board_fixture_lineups.csv
- auto_bet: NO
- production_change: NO

## Skipped rows

- idx=1 fixture=1494194 Degerfors IF vs Malmo FF reason=UNSUPPORTED_MARKET market=NO_CLEAR_STAT_MARKET
- idx=2 fixture=1506988 Jeonbuk Motors vs Gangwon FC reason=UNSUPPORTED_MARKET market=NO_CLEAR_STAT_MARKET

## Guardrails
- This bridge does not call API directly.
- This bridge does not create picks from unsupported markets.
- Missing odds/probabilities are not invented.
- Batch execution remains auto_bet: NO.
