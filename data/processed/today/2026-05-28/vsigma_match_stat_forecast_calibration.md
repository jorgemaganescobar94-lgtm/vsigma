# vSIGMA Match Stat Forecast Calibration - 2026-05-28

## Summary
- detail_rows: 35
- calibration_status_counts: CALIBRATION_OK=3; MODEL_UNDER_ESTIMATING=2; MODEL_OVER_ESTIMATING=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Metric Summary
- total_cards | rows=5 | hit_rate=0.800 | avg_error=1.60 | bias=OVER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=6 | hit_rate=0.667 | avg_error=2.50 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING
- total_fouls | rows=6 | hit_rate=0.667 | avg_error=6.33 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING
- total_goals | rows=6 | hit_rate=0.333 | avg_error=1.01 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=6 | hit_rate=0.833 | avg_error=2.67 | bias=OVER_ESTIMATE | status=CALIBRATION_OK
- total_sot | rows=6 | hit_rate=1.000 | avg_error=1.50 | bias=BALANCED_OR_ON_RANGE | status=CALIBRATION_OK

## Guardrails
- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.
- Low sample metrics are held and not used for automatic model changes.
