# vSIGMA Calibration Shadow Patch Queue - 2026-05-29

## Summary
- rows_reviewed: 6
- queue_decisions: PROMOTE_TO_SHADOW_TEST=4; NO_PATCH_STABLE=2
- shadow_priorities: HIGH=4; NONE=2
- threshold_gates: CRITICAL_SIGNAL=4; STABLE=2
- input_source_guard: DATED_SUMMARY
- input_source_path: data/processed/today/2026-05-29/vsigma_match_stat_forecast_calibration_summary.csv
- auto_apply_allowed: NO
- production_change: NO

## Queue
- total_cards | decision=NO_PATCH_STABLE | priority=NONE | sample=5 | hit_rate=0.800 | err=1.60 | bias=UNDER_ESTIMATE | threshold=STABLE | source=DATED_SUMMARY | patch=NONE
- total_corners | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=6 | hit_rate=0.500 | err=2.83 | bias=UNDER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=DATED_SUMMARY | patch=Shadow raise corner range only for wide-pressure profiles with repeated corner support.
- total_fouls | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=6 | hit_rate=0.500 | err=5.33 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=DATED_SUMMARY | patch=Shadow reduce foul baseline and cap foul inflation from urgency/context until referee data confirms.
- total_goals | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=7 | hit_rate=0.429 | err=1.22 | bias=OVER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=DATED_SUMMARY | patch=Shadow reduce goal-pressure weight 3-5% and tighten upper goal range only for matching high-error profiles.
- total_shots | decision=NO_PATCH_STABLE | priority=NONE | sample=6 | hit_rate=0.833 | err=4.83 | bias=UNDER_ESTIMATE | threshold=STABLE | source=DATED_SUMMARY | patch=NONE
- total_sot | decision=PROMOTE_TO_SHADOW_TEST | priority=HIGH | sample=6 | hit_rate=0.500 | err=2.67 | bias=UNDER_ESTIMATE | threshold=CRITICAL_SIGNAL | source=DATED_SUMMARY | patch=Shadow raise SoT conversion only where shot quality and box entries are strong.

## Guardrails
- Shadow patch queue is advisory only; it does not edit forecast formulas.
- No production change is allowed from this script.
- Ledger fallback is same-date only and exists only to avoid empty-refresh downgrades.
- Promotion requires larger sample, consecutive non-regression, and manual review.
