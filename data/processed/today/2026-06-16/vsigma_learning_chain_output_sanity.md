# vSIGMA Learning Chain Output Sanity Check - 2026-06-16

## Summary
- rows_reviewed: 7
- sanity_status_counts: EMPTY_NO_FALLBACK=7
- severity_counts: WARN=7
- actions: REVIEW_SOURCE_CHAIN=6; REVIEW_LEDGER_BUILD=1
- auto_apply: NO
- production_change: NO

## Component Checks
- post_match_actuals | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_SOURCE_CHAIN | detail=Output has no rows and no same-date fallback rows were found.
- forecast_calibration_summary | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_SOURCE_CHAIN | detail=Output has no rows and no same-date fallback rows were found.
- forecast_backtest | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_SOURCE_CHAIN | detail=Output has no rows and no same-date fallback rows were found.
- stat_calibration_governor | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_SOURCE_CHAIN | detail=Output has no rows and no same-date fallback rows were found.
- calibration_shadow_patch_queue | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_SOURCE_CHAIN | detail=Output has no rows and no same-date fallback rows were found.
- shadow_patch_promotion_readiness | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_SOURCE_CHAIN | detail=Output has no rows and no same-date fallback rows were found.
- stat_calibration_memory_ledger | status=EMPTY_NO_FALLBACK | severity=WARN | rows=0 | fallback_rows=0 | action=REVIEW_LEDGER_BUILD | detail=No same-date ledger rows found.

## Guardrails
- This sanity check is diagnostic only.
- It does not delete, overwrite, or auto-fix model outputs.
- Empty outputs with same-date fallback rows should be regenerated or read through fallback-safe scripts.
