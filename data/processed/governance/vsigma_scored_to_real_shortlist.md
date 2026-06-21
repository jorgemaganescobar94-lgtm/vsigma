# vSIGMA Scored-to-Real Shortlist Builder - 2026-06-21

## Summary
- source_rows: 6
- same_day_rows: 6
- real_shortlist_rows: 0
- real_bets_rows: 0
- selector_status_counts: NO_REAL_SHORTLIST=6
- next_action: No real shortlist rows; keep proxy bridge capped at NO_BET.
- auto_apply: NO
- production_change: NO

## Selector Diagnostics
- CRB vs Fortaleza EC | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Goias vs Operario-PR | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- São Bernardo vs Juventude | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Barra vs Amazonas | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Brusque vs Floresta | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Ferroviária vs Inter De Limeira | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning

## Real Shortlist Rows
- none. No real scored row passed selector floors.

## Real Bets Rows
- none. No row reached real BET floor.

## Guardrails
- This builder only selects real scored rows; it does not use objective proxy rows.
- NO_DATA_BLOCKED or insufficient-data rows are refused.
- Real shortlist rows still require downstream objective, availability, forecast, translator, board and prelock gates.
