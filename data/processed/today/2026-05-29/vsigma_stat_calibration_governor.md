# vSIGMA Stat Calibration Governor - 2026-05-29

## Summary
- rows_reviewed: 6
- severity_counts: MEDIUM=3; LOW=2; HIGH=1
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Recommendations
- total_cards | severity=LOW | status=CALIBRATION_OK | hit_rate=0.800 | bias=UNDER_ESTIMATE | recommendation=Keep current calibration.
- total_corners | severity=MEDIUM | status=MODEL_UNDER_ESTIMATING | hit_rate=0.500 | bias=UNDER_ESTIMATE | recommendation=Increase corner projection only for wide-pressure profiles with real corner sample support.
- total_fouls | severity=HIGH | status=MODEL_OVER_ESTIMATING | hit_rate=0.500 | bias=OVER_ESTIMATE | recommendation=Review metric-specific formula after more post-match samples.
- total_goals | severity=MEDIUM | status=MODEL_OVER_ESTIMATING | hit_rate=0.429 | bias=OVER_ESTIMATE | recommendation=Reduce goal projection pressure: lower goal_nudge and/or reduce projected-goals weight by 5-10% for similar profiles.
- total_shots | severity=LOW | status=CALIBRATION_OK | hit_rate=0.833 | bias=UNDER_ESTIMATE | recommendation=Keep current calibration.
- total_sot | severity=MEDIUM | status=MODEL_UNDER_ESTIMATING | hit_rate=0.500 | bias=UNDER_ESTIMATE | recommendation=Review metric-specific formula after more post-match samples.

## Guardrails
- This governor proposes model changes only; it does not edit forecast formulas automatically.
- Low-sample recommendations must be validated across more days before production tuning.
