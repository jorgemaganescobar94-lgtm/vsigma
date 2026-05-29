# vSIGMA Shadow Forecast A/B Simulator - 2026-05-29

## Summary
- source_guard: CALIBRATION_DETAILS
- detail_rows: 25
- summary_rows: 4
- shadow_verdicts: SHADOW_BETTER_ON_SAMPLE=3; NO_CLEAR_AB_EDGE=1
- auto_apply: NO
- production_change: NO

## Metric Results
- total_goals | verdict=SHADOW_BETTER_ON_SAMPLE | rows=7 | baseline_err=1.216 | shadow_err=1.210 | delta=0.006
- total_sot | verdict=NO_CLEAR_AB_EDGE | rows=6 | baseline_err=2.667 | shadow_err=2.667 | delta=0.000
- total_corners | verdict=SHADOW_BETTER_ON_SAMPLE | rows=6 | baseline_err=2.833 | shadow_err=2.500 | delta=0.333
- total_fouls | verdict=SHADOW_BETTER_ON_SAMPLE | rows=6 | baseline_err=5.333 | shadow_err=4.900 | delta=0.433

## Guardrails
- Shadow-only advisory.
- No forecast formula edits.
- No official pick changes.
- No production change.
