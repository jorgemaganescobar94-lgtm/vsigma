# vSIGMA Scored-to-Real Shortlist Builder - 2026-06-04

## Summary
- source_rows: 0
- same_day_rows: 0
- real_shortlist_rows: 0
- real_bets_rows: 0
- selector_status_counts: none
- next_action: No real shortlist rows; keep proxy bridge capped at NO_BET.
- auto_apply: NO
- production_change: NO

## Selector Diagnostics
- none. No same-day scored rows found.

## Real Shortlist Rows
- none. No real scored row passed selector floors.

## Real Bets Rows
- none. No row reached real BET floor.

## Guardrails
- This builder only selects real scored rows; it does not use objective proxy rows.
- NO_DATA_BLOCKED or insufficient-data rows are refused.
- Real shortlist rows still require downstream objective, availability, forecast, translator, board and prelock gates.
