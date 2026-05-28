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
- total_cards | decision=NO_PATCH_STABLE | priority=NONE | sample=6 | hit_rate=0.833 | err=1.50 | bias=OVER_ESTIMATE | threshold=STABLE | source=LEDGER_DATED_FALLBACK | patch=NONE
- total_corners | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=8 | hit_rate=0.625 | err=2.62 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=LEDGER_DATED_FALLBACK | patch=Shadow reduce corner high-range cap by 1 and lower shot-to-corner conversion for high-tempo profiles.
- total_fouls | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=9 | hit_rate=0.667 | err=7.78 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=LEDGER_DATED_FALLBACK | patch=Shadow reduce foul baseline and cap foul inflation from urgency/context until referee data confirms.
- total_goals | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=9 | hit_rate=0.556 | err=0.86 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=LEDGER_DATED_FALLBACK | patch=Shadow reduce goal-pressure weight 3-5% and tighten upper goal range only for matching high-error profiles.
- total_shots | decision=NO_PATCH_STABLE | priority=NONE | sample=9 | hit_rate=0.778 | err=4.56 | bias=OVER_ESTIMATE | threshold=STABLE | source=LEDGER_DATED_FALLBACK | patch=NONE
- total_sot | decision=NO_PATCH_STABLE | priority=NONE | sample=8 | hit_rate=1.000 | err=1.50 | bias=BALANCED_OR_ON_RANGE | threshold=STABLE | source=LEDGER_DATED_FALLBACK | patch=NONE

## Guardrails
- Shadow patch queue is advisory only; it does not edit forecast formulas.
- No production change is allowed from this script.
- Ledger fallback is same-date only and exists only to avoid empty-refresh downgrades.
- Promotion requires larger sample, consecutive non-regression, and manual review.
