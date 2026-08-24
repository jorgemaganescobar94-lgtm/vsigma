# vSIGMA API-Enriched Fixture Results Refresh - 2026-08-24

## Summary
- rows_reviewed: 2
- api_calls_planned: 2
- api_calls_executed: 2
- finished_rows: 2
- pending_rows: 0
- refresh_status_counts: OK=2
- provider_counts: API-SPORTS_DIRECT=2
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
- auto_apply: NO
- production_change: NO

## Result Rows
- Fenerbahçe vs Lyon | status=FT | score=1-1 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- Independ. Rivadavia vs Fluminense | status=PEN | score=1-1 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched

## Guardrails
- This refresh only stores fixture results for calibration.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- auto_apply=NO and production_change=NO are hardcoded.
