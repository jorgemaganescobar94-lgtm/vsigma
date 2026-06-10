# vSIGMA Stat Calibration Governor - 2026-06-10

## Summary
- rows_reviewed: 1
- severity_counts: LOW_SAMPLE=1
- auto_apply_allowed: NO
- source_guard: DATED_INPUT_ONLY
- production_change: NO

## Recommendations
- total_goals | severity=LOW_SAMPLE | status=LOW_SAMPLE_HOLD | hit_rate=1.000 | bias=BALANCED_OR_ON_RANGE | recommendation=Hold. Need at least 3 evaluated rows before tuning.

## Guardrails
- This governor proposes model changes only; it does not edit forecast formulas automatically.
- Low-sample recommendations must be validated across more days before production tuning.
