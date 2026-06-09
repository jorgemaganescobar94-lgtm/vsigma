# vSIGMA Proxy Bridge Calibration Guard - 2026-06-09

## Summary
- rows_reviewed: 3
- guard_action_counts: NO_CHANGE=3
- auto_apply: NO
- production_change: NO

## Guard Rows
- Almeria vs Castellón | action=NO_CHANGE | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | before=OVER_1_5_SUPPORTED -> after=OVER_1_5_SUPPORTED | permission=LIVE_ONLY -> LIVE_ONLY | reason=not a proxy inversion
- Nautico Recife vs Fortaleza EC | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Ponte Preta vs Cuiaba | action=NO_CHANGE | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
