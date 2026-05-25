# vSIGMA Match Stat Forecast Calibration - 2026-05-25

## Summary
- detail_rows: 20
- calibration_status_counts: CALIBRATION_OK=4; MODEL_OVER_ESTIMATING=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Metric Summary
- total_cards | rows=4 | hit_rate=0.750 | avg_error=3.00 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=3 | hit_rate=0.333 | avg_error=4.33 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_fouls | rows=3 | hit_rate=1.000 | avg_error=3.00 | bias=BALANCED_OR_ON_RANGE | status=CALIBRATION_OK
- total_goals | rows=4 | hit_rate=0.000 | avg_error=1.11 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=3 | hit_rate=1.000 | avg_error=2.67 | bias=BALANCED_OR_ON_RANGE | status=CALIBRATION_OK
- total_sot | rows=3 | hit_rate=1.000 | avg_error=1.00 | bias=BALANCED_OR_ON_RANGE | status=CALIBRATION_OK

## Guardrails
- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.
- Low sample metrics are held and not used for automatic model changes.
