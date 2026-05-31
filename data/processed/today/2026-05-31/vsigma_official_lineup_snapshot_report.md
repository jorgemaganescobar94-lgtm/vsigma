# vSIGMA Official Lineup Snapshot Import - 2026-05-31

## Summary
- rows_processed: 24
- eligible_fixtures: 15
- api_calls_made: 15
- cache_hits: 0
- lineup_rows_written: 16
- full_lineup_rows: 16
- no_lineup_rows: 14
- api_errors: 0
- key_status: API_SPORTS
- api_status_counts: NO_LINEUPS_RETURNED=8; OK=7
- auto_apply: NO
- production_change: NO

## Imported Official Rows
- Nice vs Saint Etienne | side=home | players=11 | formation=3-4-2-1 | status=OK
- Nice vs Saint Etienne | side=away | players=11 | formation=4-3-3 | status=OK
- Vasteras SK FK vs IFK Goteborg | side=home | players=11 | formation=3-4-3 | status=OK
- Vasteras SK FK vs IFK Goteborg | side=away | players=11 | formation=4-2-3-1 | status=OK
- BK Hacken vs Hammarby FF | side=home | players=11 | formation=4-2-3-1 | status=OK
- BK Hacken vs Hammarby FF | side=away | players=11 | formation=4-2-3-1 | status=OK
- RB Bragantino vs Internacional | side=home | players=11 | formation=4-2-3-1 | status=OK
- RB Bragantino vs Internacional | side=away | players=11 | formation=3-4-2-1 | status=OK
- Degerfors IF vs IF Brommapojkarna | side=home | players=11 | formation=4-2-3-1 | status=OK
- Degerfors IF vs IF Brommapojkarna | side=away | players=11 | formation=4-4-2 | status=OK
- Londrina vs Vila Nova | side=home | players=11 | formation=4-2-3-1 | status=OK
- Londrina vs Vila Nova | side=away | players=11 | formation=4-2-3-1 | status=OK
- São Bernardo vs Novorizontino | side=home | players=11 | formation=4-2-3-1 | status=OK
- São Bernardo vs Novorizontino | side=away | players=11 | formation=4-2-3-1 | status=OK
- AC Oulu vs FF Jaro | side=home | players=11 | formation=4-2-3-1 | status=OK
- AC Oulu vs FF Jaro | side=away | players=11 | formation=3-4-2-1 | status=OK

## Guardrails
- Official lineup importer only reads API/player snapshots; it never fabricates players.
- Output feeds the probable XI accuracy ledger only.
- No stake or model-weight change is applied here.
- API failures degrade to report status and do not fail the daily chain.
