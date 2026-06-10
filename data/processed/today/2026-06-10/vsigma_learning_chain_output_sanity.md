# vSIGMA Learning Chain Output Sanity Check - 2026-06-10

## Summary
- rows_reviewed: 7
- sanity_status_counts: PASS=7
- severity_counts: OK=7
- actions: NO_ACTION=7
- auto_apply: NO
- production_change: NO

## Component Checks
- post_match_actuals | status=PASS | severity=OK | rows=1 | fallback_rows=0 | action=NO_ACTION | detail=Output has data rows.
- forecast_calibration_summary | status=PASS | severity=OK | rows=1 | fallback_rows=1 | action=NO_ACTION | detail=Output has data rows.
- forecast_backtest | status=PASS | severity=OK | rows=2 | fallback_rows=0 | action=NO_ACTION | detail=Output has data rows.
- stat_calibration_governor | status=PASS | severity=OK | rows=1 | fallback_rows=1 | action=NO_ACTION | detail=Output has data rows.
- calibration_shadow_patch_queue | status=PASS | severity=OK | rows=1 | fallback_rows=1 | action=NO_ACTION | detail=Output has data rows.
- shadow_patch_promotion_readiness | status=PASS | severity=OK | rows=1 | fallback_rows=1 | action=NO_ACTION | detail=Output has data rows.
- stat_calibration_memory_ledger | status=PASS | severity=OK | rows=1 | fallback_rows=0 | action=NO_ACTION | detail=Same-date ledger rows available.

## Guardrails
- This sanity check is diagnostic only.
- It does not delete, overwrite, or auto-fix model outputs.
- Empty outputs with same-date fallback rows should be regenerated or read through fallback-safe scripts.
