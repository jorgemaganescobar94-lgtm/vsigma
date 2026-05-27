# vSIGMA Match Stat Forecast Calibration - 2026-05-27

## Summary
- detail_rows: 34
- calibration_status_counts: MODEL_OVER_ESTIMATING=3; MODEL_UNDER_ESTIMATING=2; CALIBRATION_OK=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Metric Summary
- total_cards | rows=4 | hit_rate=0.750 | avg_error=1.75 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=6 | hit_rate=0.667 | avg_error=2.50 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_fouls | rows=6 | hit_rate=0.667 | avg_error=4.17 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING
- total_goals | rows=6 | hit_rate=0.167 | avg_error=1.34 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=6 | hit_rate=0.500 | avg_error=7.33 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_sot | rows=6 | hit_rate=0.333 | avg_error=3.50 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING

## Guardrails
- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.
- Low sample metrics are held and not used for automatic model changes.
