# vSIGMA Proxy Bridge Calibration Guard - 2026-07-12

## Summary
- rows_reviewed: 2
- guard_action_counts: BLOCKED_INVERSION=1; NO_CHANGE=1
- auto_apply: NO
- production_change: NO

## Guard Rows
- Ulsan Hyundai FC vs Jeonbuk Motors | action=BLOCKED_INVERSION | market_hint=OVER_1_5 | before=UNDER_3_5_REVIEW -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET_OR_WATCH -> NO_BET | reason=proxy objective-context tempo/over source cannot be inverted into under/no-goals market
- Gwangju FC vs Pohang Steelers | action=NO_CHANGE | market_hint=AWAY_WIN | before=UNDER_3_5_REVIEW -> after=UNDER_3_5_REVIEW | permission=NO_BET_OR_WATCH -> NO_BET_OR_WATCH | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
