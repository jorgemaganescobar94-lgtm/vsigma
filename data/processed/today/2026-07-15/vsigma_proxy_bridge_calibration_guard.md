# vSIGMA Proxy Bridge Calibration Guard - 2026-07-15

## Summary
- rows_reviewed: 1
- guard_action_counts: NO_CHANGE=1
- auto_apply: NO
- production_change: NO

## Guard Rows
- The New Saints vs Sabah FA | action=NO_CHANGE | market_hint=HOME_WIN | before=UNDER_3_5_REVIEW -> after=UNDER_3_5_REVIEW | permission=NO_BET_OR_WATCH -> NO_BET_OR_WATCH | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
