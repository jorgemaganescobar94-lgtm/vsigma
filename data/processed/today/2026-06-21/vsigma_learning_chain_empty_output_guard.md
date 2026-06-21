# vSIGMA Learning Chain Empty Output Hard Guard - 2026-06-21

## Summary
- guard_status: WARN
- commit_allowed: YES
- rows_reviewed: 7
- guard_decisions: WARN_ONLY=6; PASS=1
- auto_apply: NO
- production_change: NO

## Component Guards
- post_match_actuals | decision=PASS | commit_allowed=YES | status=PASS | rows=71 | fallback_rows=0 | reason=No blocking empty-output condition.
- forecast_calibration_summary | decision=WARN_ONLY | commit_allowed=YES | status=EMPTY_NO_FALLBACK | rows=0 | fallback_rows=0 | reason=Non-blocking empty-output warning; keep workflow visible.
- forecast_backtest | decision=WARN_ONLY | commit_allowed=YES | status=EMPTY_NO_FALLBACK | rows=0 | fallback_rows=0 | reason=Non-blocking empty-output warning; keep workflow visible.
- stat_calibration_governor | decision=WARN_ONLY | commit_allowed=YES | status=EMPTY_NO_FALLBACK | rows=0 | fallback_rows=0 | reason=Non-blocking empty-output warning; keep workflow visible.
- calibration_shadow_patch_queue | decision=WARN_ONLY | commit_allowed=YES | status=EMPTY_NO_FALLBACK | rows=0 | fallback_rows=0 | reason=Non-blocking empty-output warning; keep workflow visible.
- shadow_patch_promotion_readiness | decision=WARN_ONLY | commit_allowed=YES | status=EMPTY_NO_FALLBACK | rows=0 | fallback_rows=0 | reason=Non-blocking empty-output warning; keep workflow visible.
- stat_calibration_memory_ledger | decision=WARN_ONLY | commit_allowed=YES | status=EMPTY_NO_FALLBACK | rows=0 | fallback_rows=0 | reason=Non-blocking empty-output warning; keep workflow visible.

## Guardrails
- This guard does not modify model formulas or picks.
- When --fail-on-block is used, BLOCK_COMMIT returns a non-zero exit code before the workflow commit step.
- Blocks only critical empty outputs with valid same-date fallback or critical sanity severity.
