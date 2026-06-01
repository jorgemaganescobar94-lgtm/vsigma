# vSIGMA Proxy Bridge Calibration Guard - 2026-06-01

## Summary
- rows_reviewed: 4
- guard_action_counts: NO_CHANGE=2; BLOCKED_INVERSION=2
- auto_apply: NO
- production_change: NO

## Guard Rows
- Cordoba vs Huesca | action=NO_CHANGE | market_hint=OVER_2_5 | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Almeria vs Valladolid | action=NO_CHANGE | market_hint=OVER_2_5 | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- RB Bragantino vs Internacional | action=BLOCKED_INVERSION | market_hint=OVER_1_5 | before=UNDER_3_5_REVIEW -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET_OR_WATCH -> NO_BET | reason=proxy objective-context tempo/over source cannot be inverted into under/no-goals market
- Vasco DA Gama vs Atletico-MG | action=BLOCKED_INVERSION | market_hint=OVER_1_5 | before=UNDER_3_5_REVIEW -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET_OR_WATCH -> NO_BET | reason=proxy objective-context tempo/over source cannot be inverted into under/no-goals market

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
