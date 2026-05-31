# vSIGMA Official Lineup Snapshot Import - 2026-05-31

## Summary
- rows_processed: 24
- eligible_fixtures: 23
- api_calls_made: 16
- cache_hits: 7
- lineup_rows_written: 30
- full_lineup_rows: 30
- no_lineup_rows: 16
- api_errors: 0
- key_status: API_SPORTS
- api_status_counts: OK=7; NO_LINEUPS_RETURNED=9
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
- Racing Santander vs Cadiz | side=home | players=11 | formation=4-2-3-1 | status=OK
- Racing Santander vs Cadiz | side=away | players=11 | formation=4-3-3 | status=OK
- Almeria vs Valladolid | side=home | players=11 | formation=4-2-3-1 | status=OK
- Almeria vs Valladolid | side=away | players=11 | formation=4-4-2 | status=OK
- Zaragoza vs Malaga | side=home | players=11 | formation=4-4-2 | status=OK
- Zaragoza vs Malaga | side=away | players=11 | formation=4-4-2 | status=OK
- Deportivo La Coruna vs Las Palmas | side=home | players=11 | formation=4-4-2 | status=OK
- Deportivo La Coruna vs Las Palmas | side=away | players=11 | formation=4-2-3-1 | status=OK
- Castellón vs Eibar | side=home | players=11 | formation=4-4-2 | status=OK
- Castellón vs Eibar | side=away | players=11 | formation=5-4-1 | status=OK
- Gent vs Genk | side=home | players=11 | formation=4-4-2 | status=OK
- Gent vs Genk | side=away | players=11 | formation=4-2-3-1 | status=OK
- Burgos vs FC Andorra | side=home | players=11 | formation=4-4-2 | status=OK
- Burgos vs FC Andorra | side=away | players=11 | formation=3-4-3 | status=OK

## Guardrails
- Official lineup importer only reads API/player snapshots; it never fabricates players.
- Output feeds the probable XI accuracy ledger only.
- No stake or model-weight change is applied here.
- API failures degrade to report status and do not fail the daily chain.
