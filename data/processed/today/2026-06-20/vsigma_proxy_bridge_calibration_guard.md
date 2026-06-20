# vSIGMA Proxy Bridge Calibration Guard - 2026-06-20

## Summary
- rows_reviewed: 10
- guard_action_counts: NO_CHANGE=10
- auto_apply: NO
- production_change: NO

## Guard Rows
- Almeria vs Malaga | action=NO_CHANGE | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | before=OVER_1_5_SUPPORTED -> after=OVER_1_5_SUPPORTED | permission=LIVE_ONLY -> LIVE_ONLY | reason=not a proxy inversion
- Ceara vs Botafogo SP | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Londrina vs Athletic Club | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Vila Nova vs Nautico Recife | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Banga vs FK Zalgiris Vilnius | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Panevėžys vs Šiauliai | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- TransINVEST Vilnius vs Kauno Žalgiris | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Anápolis vs AO Itabaiana | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Botafogo PB vs Volta Redonda | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Santa Cruz vs Ypiranga-RS | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
