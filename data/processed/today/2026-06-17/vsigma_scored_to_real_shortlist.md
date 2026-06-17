# vSIGMA Scored-to-Real Shortlist Builder - 2026-06-17

## Summary
- source_rows: 7
- same_day_rows: 7
- real_shortlist_rows: 0
- real_bets_rows: 0
- selector_status_counts: NO_REAL_SHORTLIST=7
- next_action: No real shortlist rows; keep proxy bridge capped at NO_BET.
- auto_apply: NO
- production_change: NO

## Selector Diagnostics
- Hegelmann Litauen vs Džiugas Telšiai | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Kauno Žalgiris vs Banga | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Gnistan vs Lahti | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- HJK Helsinki vs Inter Turku | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Ilves vs FF Jaro | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- SJK vs VPS | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Turku PS vs KuPS | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning

## Real Shortlist Rows
- none. No real scored row passed selector floors.

## Real Bets Rows
- none. No row reached real BET floor.

## Guardrails
- This builder only selects real scored rows; it does not use objective proxy rows.
- NO_DATA_BLOCKED or insufficient-data rows are refused.
- Real shortlist rows still require downstream objective, availability, forecast, translator, board and prelock gates.
