# vSIGMA Match Stat Forecast Calibration - 2026-05-29

## Summary
- detail_rows: 36
- calibration_status_counts: CALIBRATION_OK=2; MODEL_UNDER_ESTIMATING=2; MODEL_OVER_ESTIMATING=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Metric Summary
- total_cards | rows=5 | hit_rate=0.800 | avg_error=1.60 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=6 | hit_rate=0.500 | avg_error=2.83 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING
- total_fouls | rows=6 | hit_rate=0.500 | avg_error=5.33 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_goals | rows=7 | hit_rate=0.429 | avg_error=1.22 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=6 | hit_rate=0.833 | avg_error=4.83 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_sot | rows=6 | hit_rate=0.500 | avg_error=2.67 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING

## Guardrails
- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.
- Low sample metrics are held and not used for automatic model changes.
