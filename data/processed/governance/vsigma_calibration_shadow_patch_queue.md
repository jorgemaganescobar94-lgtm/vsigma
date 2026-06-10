# vSIGMA Calibration Shadow Patch Queue - 2026-06-10

## Summary
- rows_reviewed: 1
- queue_decisions: REJECT_LOW_SAMPLE=1
- shadow_priorities: NONE=1
- threshold_gates: MONITOR_SIGNAL=1
- input_source_guard: DATED_SUMMARY
- input_source_path: data/processed/today/2026-06-10/vsigma_match_stat_forecast_calibration_summary.csv
- auto_apply_allowed: NO
- production_change: NO

## Queue
- total_goals | decision=REJECT_LOW_SAMPLE | priority=NONE | sample=1 | hit_rate=1.000 | err=0.35 | bias=BALANCED_OR_ON_RANGE | threshold=MONITOR_SIGNAL | source=DATED_SUMMARY | patch=NONE

## Guardrails
- Shadow patch queue is advisory only; it does not edit forecast formulas.
- No production change is allowed from this script.
- Ledger fallback is same-date only and exists only to avoid empty-refresh downgrades.
- Promotion requires larger sample, consecutive non-regression, and manual review.
