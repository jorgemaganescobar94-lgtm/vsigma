# vSIGMA Match Stat Forecast Calibration - 2026-05-28

## Summary
- detail_rows: 49
- calibration_status_counts: CALIBRATION_OK=3; MODEL_OVER_ESTIMATING=3
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Metric Summary
- total_cards | rows=6 | hit_rate=0.833 | avg_error=1.50 | bias=OVER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=8 | hit_rate=0.625 | avg_error=2.62 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_fouls | rows=9 | hit_rate=0.667 | avg_error=7.78 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_goals | rows=9 | hit_rate=0.556 | avg_error=0.86 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=9 | hit_rate=0.778 | avg_error=4.56 | bias=OVER_ESTIMATE | status=CALIBRATION_OK
- total_sot | rows=8 | hit_rate=1.000 | avg_error=1.50 | bias=BALANCED_OR_ON_RANGE | status=CALIBRATION_OK

## Guardrails
- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.
- Low sample metrics are held and not used for automatic model changes.
