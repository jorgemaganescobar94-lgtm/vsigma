# vSIGMA Proxy Bridge Calibration Guard - 2026-06-08

## Summary
- rows_reviewed: 0
- guard_action_counts: none
- auto_apply: NO
- production_change: NO

## Guard Rows
- none. No translator rows reviewed.

## Guardrails
- Diagnostic/post-processing only; no stake permission is added.
- The guard can only downgrade or preserve rows, never upgrade them.
- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.
