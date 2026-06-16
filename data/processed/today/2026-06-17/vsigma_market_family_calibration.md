# vSIGMA Market Family Calibration - 2026-06-17

## Summary
- family_rows: 3
- sample_gate_counts: INSUFFICIENT_SAMPLE=3
- calibration_status_counts: HOLD_SAMPLE=3
- confidence_signal_counts: NO_WEIGHT_CHANGE=3
- auto_apply: NO
- production_change: NO

## Family Rows
- NO_MARKET | real=0/3 | green=0 red=0 void=0 | gate=INSUFFICIENT_SAMPLE | status=HOLD_SAMPLE | signal=NO_WEIGHT_CHANGE | action=Collect more market-family samples before changing confidence.
- TOTAL_GOALS | real=0/3 | green=0 red=0 void=0 | gate=INSUFFICIENT_SAMPLE | status=HOLD_SAMPLE | signal=NO_WEIGHT_CHANGE | action=Collect more market-family samples before changing confidence.
- UNKNOWN_FAMILY | real=0/4 | green=0 red=0 void=0 | gate=INSUFFICIENT_SAMPLE | status=HOLD_SAMPLE | signal=NO_WEIGHT_CHANGE | action=Collect more market-family samples before changing confidence.

## Guardrails
- This calibration is family-level and advisory only; it does not change model weights.
- Sample gates block upgrades/downgrades until enough real audited rows exist.
- Diagnostic, pending and no-pick rows do not count as real market-family hit-rate sample.
- Any upgrade/downgrade candidate requires causal review before a future manual patch.
