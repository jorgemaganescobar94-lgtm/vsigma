# vSIGMA Stat Calibration Governor - 2026-05-27

## Summary
- rows_reviewed: 6
- severity_counts: HIGH=4; LOW=2
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Recommendations
- total_cards | severity=LOW | status=CALIBRATION_OK | hit_rate=0.750 | bias=UNDER_ESTIMATE | recommendation=Keep current calibration.
- total_corners | severity=LOW | status=MODEL_OVER_ESTIMATING | hit_rate=0.667 | bias=OVER_ESTIMATE | recommendation=Reduce corner projection: lower shot_corner_nudge cap and reduce corner range high by 1 for high-tempo profiles.
- total_fouls | severity=HIGH | status=MODEL_UNDER_ESTIMATING | hit_rate=0.667 | bias=UNDER_ESTIMATE | recommendation=Review metric-specific formula after more post-match samples.
- total_goals | severity=HIGH | status=MODEL_OVER_ESTIMATING | hit_rate=0.167 | bias=OVER_ESTIMATE | recommendation=Reduce goal projection pressure: lower goal_nudge and/or reduce projected-goals weight by 5-10% for similar profiles.
- total_shots | severity=HIGH | status=MODEL_OVER_ESTIMATING | hit_rate=0.500 | bias=OVER_ESTIMATE | recommendation=Review metric-specific formula after more post-match samples.
- total_sot | severity=HIGH | status=MODEL_UNDER_ESTIMATING | hit_rate=0.333 | bias=UNDER_ESTIMATE | recommendation=Review metric-specific formula after more post-match samples.

## Guardrails
- This governor proposes model changes only; it does not edit forecast formulas automatically.
- Low-sample recommendations must be validated across more days before production tuning.
