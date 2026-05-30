# vSIGMA Shadow Experiments - 2026-05-30

## Executive Shadow Summary
- generated_at: 2026-05-30T17:16:54+01:00
- shadow_experiments: 2
- experiment_type_counts: LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW=1; LOW_CONVERSION_OVER25_SHRINKAGE_SHADOW=1
- shadow_status_counts: ACTIVE_SHADOW_ONLY=2

## Active Shadow Experiments
- ACTIVE_SHADOW_ONLY | LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW | pattern=OVER_1_5::FAILURE_MODE_LOW_CONVERSION | production_impact=NONE | auto_apply=NO
- ACTIVE_SHADOW_ONLY | LOW_CONVERSION_OVER25_SHRINKAGE_SHADOW | pattern=OVER_2_5::FAILURE_MODE_LOW_CONVERSION | production_impact=NONE | auto_apply=NO

## Guardrails
- production logic changed: NO
- official picks changed: NO
- predictive formulas changed: NO
- thresholds changed: NO
- calibration changed: NO
- ranking changed: NO
- market-selection changed: NO
- auto_apply: NO for every experiment

## Promotion Path
- Shadow experiments are evaluated only after enough closed matching samples exist.
- Promotion requires a separate promotion gate and is never applied by this engine.
