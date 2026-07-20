# vSIGMA Proxy Bridge Calibration Guard - 2026-07-20

## Summary
- rows_reviewed: 3
- guard_action_counts: NO_CHANGE=2; BLOCKED_INVERSION=1
- auto_apply: NO
- production_change: NO

## Guard Rows
- Hammarby FF vs Degerfors IF | action=BLOCKED_INVERSION | market_hint=BTTS_YES | before=UNDER_3_5_REVIEW -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET_OR_WATCH -> NO_BET | reason=proxy objective-context tempo/over source cannot be inverted into under/no-goals market
- Halmstad vs BK Hacken | action=NO_CHANGE | market_hint=AWAY_WIN | before=UNDER_3_5_REVIEW -> after=UNDER_3_5_REVIEW | permission=NO_BET_OR_WATCH -> NO_BET_OR_WATCH | reason=not a proxy inversion
- FC Anyang vs Gwangju FC | action=NO_CHANGE | market_hint=HOME_WIN | before=UNDER_3_5_REVIEW -> after=UNDER_3_5_REVIEW | permission=NO_BET_OR_WATCH -> NO_BET_OR_WATCH | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
