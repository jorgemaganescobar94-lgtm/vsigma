# vSIGMA Match Stat Forecast Calibration - 2026-06-10

## Summary
- detail_rows: 1
- calibration_status_counts: LOW_SAMPLE_HOLD=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Metric Summary
- total_goals | rows=1 | hit_rate=1.000 | avg_error=0.35 | bias=BALANCED_OR_ON_RANGE | status=LOW_SAMPLE_HOLD

## Guardrails
- Calibration only uses actual metrics present in vsigma_post_match_stat_actuals.
- Low sample metrics are held and not used for automatic model changes.
