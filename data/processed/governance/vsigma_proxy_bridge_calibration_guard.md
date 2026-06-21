# vSIGMA Proxy Bridge Calibration Guard - 2026-06-21

## Summary
- rows_reviewed: 6
- guard_action_counts: NO_CHANGE=6
- auto_apply: NO
- production_change: NO

## Guard Rows
- CRB vs Fortaleza EC | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Goias vs Operario-PR | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- São Bernardo vs Juventude | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Barra vs Amazonas | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Brusque vs Floresta | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Ferroviária vs Inter De Limeira | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
