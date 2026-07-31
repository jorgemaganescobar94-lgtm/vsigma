# vSIGMA Proxy Bridge Calibration Guard - 2026-07-31

## Summary
- rows_reviewed: 4
- guard_action_counts: NO_CHANGE=3; BLOCKED_INVERSION=1
- auto_apply: NO
- production_change: NO

## Guard Rows
- IF Brommapojkarna vs Hammarby FF | action=NO_CHANGE | market_hint=OVER_2_5 | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- KFUM Oslo vs Molde | action=NO_CHANGE | market_hint=OVER_2_5 | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Remo vs Vitoria | action=BLOCKED_INVERSION | market_hint=OVER_1_5 | before=UNDER_3_5_REVIEW -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET_OR_WATCH -> NO_BET | reason=proxy objective-context tempo/over source cannot be inverted into under/no-goals market
- Aalesund vs Viking | action=NO_CHANGE | market_hint=AWAY_WIN | before=UNDER_3_5_REVIEW -> after=UNDER_3_5_REVIEW | permission=NO_BET_OR_WATCH -> NO_BET_OR_WATCH | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
