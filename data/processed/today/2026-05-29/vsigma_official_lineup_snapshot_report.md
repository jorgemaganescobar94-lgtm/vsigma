# vSIGMA Official Lineup Snapshot Import - 2026-05-29

## Summary
- rows_processed: 2
- eligible_fixtures: 2
- api_calls_made: 1
- cache_hits: 1
- lineup_rows_written: 2
- full_lineup_rows: 2
- no_lineup_rows: 2
- api_errors: 0
- key_status: API_SPORTS
- api_status_counts: NO_LINEUPS_RETURNED=1
- auto_apply: NO
- production_change: NO

## Imported Official Rows
- Nice vs Saint Etienne | side=home | players=11 | formation=3-4-2-1 | status=OK
- Nice vs Saint Etienne | side=away | players=11 | formation=4-3-3 | status=OK

## Guardrails
- Official lineup importer only reads API/player snapshots; it never fabricates players.
- Output feeds the probable XI accuracy ledger only.
- No stake or model-weight change is applied here.
- API failures degrade to report status and do not fail the daily chain.
