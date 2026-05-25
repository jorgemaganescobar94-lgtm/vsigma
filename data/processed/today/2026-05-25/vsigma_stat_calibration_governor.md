# vSIGMA Stat Calibration Governor - 2026-05-25

## Summary
- rows_reviewed: 6
- severity_counts: HIGH=3; LOW=3
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Recommendations
- total_cards | severity=HIGH | status=MODEL_UNDER_ESTIMATING | hit_rate=0.667 | bias=UNDER_ESTIMATE | recommendation=Raise cards baseline: add card-risk bump for high-foul/high-urgency matches and widen upper card range.
- total_corners | severity=HIGH | status=MODEL_OVER_ESTIMATING | hit_rate=0.333 | bias=OVER_ESTIMATE | recommendation=Reduce corner projection: lower shot_corner_nudge cap and reduce corner range high by 1 for high-tempo profiles.
- total_fouls | severity=LOW | status=CALIBRATION_OK | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | recommendation=Keep current calibration.
- total_goals | severity=HIGH | status=MODEL_OVER_ESTIMATING | hit_rate=0.000 | bias=OVER_ESTIMATE | recommendation=Reduce goal projection pressure: lower goal_nudge and/or reduce projected-goals weight by 5-10% for similar profiles.
- total_shots | severity=LOW | status=CALIBRATION_OK | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | recommendation=Keep current calibration.
- total_sot | severity=LOW | status=CALIBRATION_OK | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | recommendation=Keep current calibration.

## Guardrails
- This governor proposes model changes only; it does not edit forecast formulas automatically.
- Low-sample recommendations must be validated across more days before production tuning.
