# vSIGMA Stat Calibration Governor - 2026-05-28

## Summary
- rows_reviewed: 6
- severity_counts: LOW=4; HIGH=1; MEDIUM=1
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Recommendations
- total_cards | severity=LOW | status=CALIBRATION_OK | hit_rate=0.833 | bias=OVER_ESTIMATE | recommendation=Keep current calibration.
- total_corners | severity=LOW | status=MODEL_OVER_ESTIMATING | hit_rate=0.625 | bias=OVER_ESTIMATE | recommendation=Reduce corner projection: lower shot_corner_nudge cap and reduce corner range high by 1 for high-tempo profiles.
- total_fouls | severity=HIGH | status=MODEL_OVER_ESTIMATING | hit_rate=0.667 | bias=OVER_ESTIMATE | recommendation=Review metric-specific formula after more post-match samples.
- total_goals | severity=MEDIUM | status=MODEL_OVER_ESTIMATING | hit_rate=0.556 | bias=OVER_ESTIMATE | recommendation=Reduce goal projection pressure: lower goal_nudge and/or reduce projected-goals weight by 5-10% for similar profiles.
- total_shots | severity=LOW | status=CALIBRATION_OK | hit_rate=0.778 | bias=OVER_ESTIMATE | recommendation=Keep current calibration.
- total_sot | severity=LOW | status=CALIBRATION_OK | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | recommendation=Keep current calibration.

## Guardrails
- This governor proposes model changes only; it does not edit forecast formulas automatically.
- Low-sample recommendations must be validated across more days before production tuning.
