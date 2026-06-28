# vSIGMA API Board Candidate Bridge - 2026-06-28

- board_rows: 1
- lineup_rows: 1
- candidates_written: 0
- skipped_rows: 1
- board_source: data/processed/today/2026-06-28/vsigma_daily_execution_board.csv
- lineup_source: data/processed/today/2026-06-28/vsigma_forced_api_board_fixture_lineups.csv
- auto_bet: NO
- production_change: NO

## Skipped rows

- idx=1 fixture=DIAGNOSTIC_EMPTY_BY_PROMOTION_GATE NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS reason=UNSUPPORTED_MARKET market=NO_MARKET

## Guardrails
- This bridge does not call API directly.
- This bridge does not create picks from unsupported markets.
- Missing odds/probabilities are not invented.
- Batch execution remains auto_bet: NO.
