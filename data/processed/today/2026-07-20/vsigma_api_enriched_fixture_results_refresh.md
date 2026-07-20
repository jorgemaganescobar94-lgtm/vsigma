# vSIGMA API-Enriched Fixture Results Refresh - 2026-07-20

## Summary
- rows_reviewed: 3
- api_calls_planned: 3
- api_calls_executed: 3
- finished_rows: 3
- pending_rows: 0
- refresh_status_counts: OK=3
- provider_counts: API-SPORTS_DIRECT=3
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
- auto_apply: NO
- production_change: NO

## Result Rows
- Hammarby FF vs Degerfors IF | status=FT | score=4-0 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- Halmstad vs BK Hacken | status=FT | score=0-2 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- FC Anyang vs Gwangju FC | status=FT | score=1-1 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched

## Guardrails
- This refresh only stores fixture results for calibration.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- auto_apply=NO and production_change=NO are hardcoded.
