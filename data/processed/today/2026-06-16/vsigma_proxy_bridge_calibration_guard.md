# vSIGMA Proxy Bridge Calibration Guard - 2026-06-16

## Summary
- rows_reviewed: 3
- guard_action_counts: NO_CHANGE=3
- auto_apply: NO
- production_change: NO

## Guard Rows
- FK Zalgiris Vilnius vs Panevėžys | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Suduva Marijampole vs Šiauliai | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- TransINVEST Vilnius vs FK Trakai | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
