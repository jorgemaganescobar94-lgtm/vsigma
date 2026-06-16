# vSIGMA Scored-to-Real Shortlist Builder - 2026-06-16

## Summary
- source_rows: 3
- same_day_rows: 3
- real_shortlist_rows: 0
- real_bets_rows: 0
- selector_status_counts: NO_REAL_SHORTLIST=3
- next_action: No real shortlist rows; keep proxy bridge capped at NO_BET.
- auto_apply: NO
- production_change: NO

## Selector Diagnostics
- FK Zalgiris Vilnius vs Panevėžys | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Suduva Marijampole vs Šiauliai | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- TransINVEST Vilnius vs FK Trakai | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning

## Real Shortlist Rows
- none. No real scored row passed selector floors.

## Real Bets Rows
- none. No row reached real BET floor.

## Guardrails
- This builder only selects real scored rows; it does not use objective proxy rows.
- NO_DATA_BLOCKED or insufficient-data rows are refused.
- Real shortlist rows still require downstream objective, availability, forecast, translator, board and prelock gates.
