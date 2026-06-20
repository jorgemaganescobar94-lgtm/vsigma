# vSIGMA Scored-to-Real Shortlist Builder - 2026-06-20

## Summary
- source_rows: 10
- same_day_rows: 10
- real_shortlist_rows: 0
- real_bets_rows: 0
- selector_status_counts: NO_REAL_SHORTLIST=10
- next_action: No real shortlist rows; keep proxy bridge capped at NO_BET.
- auto_apply: NO
- production_change: NO

## Selector Diagnostics
- Almeria vs Malaga | status=NO_REAL_SHORTLIST | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | reason=data quality score below selector floor
- Banga vs FK Zalgiris Vilnius | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Panevėžys vs Šiauliai | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- TransINVEST Vilnius vs Kauno Žalgiris | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Ceara vs Botafogo SP | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Londrina vs Athletic Club | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Vila Nova vs Nautico Recife | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Anápolis vs AO Itabaiana | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Botafogo PB vs Volta Redonda | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning
- Santa Cruz vs Ypiranga-RS | status=NO_REAL_SHORTLIST | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | reason=blocked by scoring/data warning

## Real Shortlist Rows
- none. No real scored row passed selector floors.

## Real Bets Rows
- none. No row reached real BET floor.

## Guardrails
- This builder only selects real scored rows; it does not use objective proxy rows.
- NO_DATA_BLOCKED or insufficient-data rows are refused.
- Real shortlist rows still require downstream objective, availability, forecast, translator, board and prelock gates.
