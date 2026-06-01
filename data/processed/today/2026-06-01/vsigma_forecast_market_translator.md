# vSIGMA Forecast-to-Market Translator - 2026-06-01

## Summary
- rows_translated: 0
- execution_permission_counts: none
- primary_market_counts: none
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- none. Need dated match stat forecasts first.

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
