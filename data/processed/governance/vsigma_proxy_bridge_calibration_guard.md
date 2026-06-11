# vSIGMA Proxy Bridge Calibration Guard - 2026-06-10

## Summary
- rows_reviewed: 1
- guard_action_counts: NO_CHANGE=1
- auto_apply: NO
- production_change: NO

## Guard Rows
- Malaga vs Las Palmas | action=NO_CHANGE | market_hint=OVER_OR_BTTS_CHECK | before=OVER_1_5_SUPPORTED -> after=OVER_1_5_SUPPORTED | permission=LIVE_ONLY -> LIVE_ONLY | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
