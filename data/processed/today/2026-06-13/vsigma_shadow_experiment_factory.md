# vSIGMA Shadow Experiment Factory - 2026-06-13

## Summary
- shadow_experiments: 2
- shadow_status_counts: CREATE_SHADOW_ONLY=1; CONTINUE_SHADOW_ONLY=1
- auto_apply: NO
- production_change: NO

## Experiments
- shadow_waiting_prelock_over_1_5_failure_mode_low_conversion_wait_for_post_results | CREATE_SHADOW_ONLY | pattern=WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS | sample=3 | closed=0 | rule=Shadow downgrade OVER_1_5 when failure_mode_low_conversion is present until stronger conversion evidence appears.
- shadow_over_1_5_failure_mode_low_conversion | CONTINUE_SHADOW_ONLY | pattern=OVER_1_5::FAILURE_MODE_LOW_CONVERSION | sample=5 | closed=1 | rule=Shadow downgrade OVER_1_5 when failure_mode_low_conversion is present until stronger conversion evidence appears.

## Guardrails
- Shadow experiments do not change production picks.
- Promotion still requires clean data, closed sample threshold, and separate review.
