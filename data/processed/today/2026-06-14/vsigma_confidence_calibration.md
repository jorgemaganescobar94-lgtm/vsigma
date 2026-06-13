# vSIGMA Confidence Calibration - 2026-06-14

## Summary
- confidence_bucket_rows: 1
- sample_gate_counts: INSUFFICIENT_SAMPLE=1
- calibration_status_counts: HOLD_SAMPLE=1
- confidence_bias_signal_counts: NO_CONFIDENCE_SIGNAL=1
- auto_apply: NO
- production_change: NO

## Confidence Rows
- NO_CONFIDENCE | expected=NA | real=0/1 | green=0 red=0 void=0 | observed=NA | gap=NA | gate=INSUFFICIENT_SAMPLE | status=HOLD_SAMPLE | signal=NO_CONFIDENCE_SIGNAL

## Guardrails
- This calibration is advisory only and does not change confidence weights.
- Diagnostic, pending and no-pick rows do not count as real hit-rate sample.
- Confidence upgrades/downgrades require sufficient sample and causal review.
- auto_apply=NO and production_change=NO are hardcoded.
