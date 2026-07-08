# vSIGMA Proxy Bridge Calibration Guard - 2026-07-08

## Summary
- rows_reviewed: 2
- guard_action_counts: NO_CHANGE=2
- auto_apply: NO
- production_change: NO

## Guard Rows
- Vikingur Reykjavik vs Gyori ETO FC | action=NO_CHANGE | market_hint=OVER_2_5 | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion
- Lincoln Red Imps FC vs Inter Club d'Escaldes | action=NO_CHANGE | market_hint=OVER_2_5 | before=NO_CLEAR_STAT_MARKET -> after=NO_CLEAR_STAT_MARKET | permission=NO_BET -> NO_BET | reason=not a proxy inversion

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
