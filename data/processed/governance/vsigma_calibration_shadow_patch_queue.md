# vSIGMA Calibration Shadow Patch Queue - 2026-05-28

## Summary
- rows_reviewed: 6
- queue_decisions: NO_PATCH_STABLE=3; PROMOTE_TO_SHADOW_TEST=3
- shadow_priorities: NONE=3; HIGH=3
- threshold_gates: STABLE=3; CRITICAL_SIGNAL=3
- input_source_guard: LEDGER_DATED_FALLBACK
- input_source_path: data/processed/ledger/vsigma_stat_calibration_memory.csv
- auto_apply_allowed: NO
- production_change: NO

## Queue
- total_cards | decision=NO_PATCH_STABLE | priority=NONE | sample=6 | hit_rate=0.833 | err=1.50 | bias=OVER_ESTIMATE | threshold=STABLE
- total_corners | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=8 | hit_rate=0.625 | err=2.62 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL
- total_fouls | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=9 | hit_rate=0.667 | err=7.78 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL
- total_goals | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=9 | hit_rate=0.556 | err=0.86 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL
- total_shots | decision=NO_PATCH_STABLE | priority=NONE | sample=9 | hit_rate=0.778 | err=4.56 | bias=OVER_ESTIMATE | threshold=STABLE
- total_sot | decision=NO_PATCH_STABLE | priority=NONE | sample=8 | hit_rate=1.000 | err=1.50 | bias=BALANCED_OR_ON_RANGE | threshold=STABLE

## Guardrails
- Shadow patch queue is advisory only.
- No production change is allowed from this script.
- Ledger fallback is same-date only.
- Promotion requires larger sample, consecutive non-regression, and manual review.
