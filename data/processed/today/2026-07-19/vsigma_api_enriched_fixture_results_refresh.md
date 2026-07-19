# vSIGMA API-Enriched Fixture Results Refresh - 2026-07-19

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
- Malisheva vs Vllaznia Shkodër | status=FT | score=5-0 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- Atert Bissen vs KI Klaksvik | status=FT | score=1-2 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched
- Universitatea Craiova vs ML Vitebsk | status=FT | score=1-0 | ready=YES | provider=API-SPORTS_DIRECT | note=fixture fetched

## Guardrails
- This refresh only stores fixture results for calibration.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- auto_apply=NO and production_change=NO are hardcoded.
