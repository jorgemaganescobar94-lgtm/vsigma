# vSIGMA API-Enriched Fixture Results Refresh - 2026-07-28

## Summary
- rows_reviewed: 4
- api_calls_planned: 4
- api_calls_executed: 4
- finished_rows: 4
- pending_rows: 0
- refresh_status_counts: OK=4
- provider_counts: API-SPORTS_DIRECT=4
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
- auto_apply: NO
- production_change: NO

## Result Rows
- IF Brommapojkarna vs Hammarby FF | status=FT | score=1-1 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- KFUM Oslo vs Molde | status=FT | score=2-4 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- Remo vs Vitoria | status=FT | score=2-0 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- Aalesund vs Viking | status=FT | score=1-1 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched

## Guardrails
- This refresh only stores fixture results for calibration.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- auto_apply=NO and production_change=NO are hardcoded.
