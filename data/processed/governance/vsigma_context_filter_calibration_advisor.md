# vSIGMA Context Filter Calibration Advisor - 2026-05-23

## Executive Calibration
- calibration_verdict: FILTER_IMPROVED_BUT_TOO_COARSE
- base_profit_units: 0.16
- adjusted_profit_units: 0.38
- net_adjustment_delta_units: 0.22
- avoided_loss_units: 1.0
- missed_win_units: 0.78
- recommended_policy: Keep context filter, but split hard downgrade vs reduced-stake review; do not auto-veto all context downgrades from one day.
- min_samples_before_rule_change: 20
- calibration_label_counts: CONTEXT_FILTER_VALIDATED_CASE=1; SOFTEN_CONTEXT_DOWNGRADE_CANDIDATE=1; SHADOW_KEEP_VALIDATED_CASE=1
- auto_apply: NO
- production_change: NO

## Detail Rows
- #1 | CONTEXT_FILTER_VALIDATED_CASE | Bologna vs Inter | market=AWAY_WIN | audit=AVOIDED_LOSS | note=Context downgrade avoided a losing base BET.
- #2 | SOFTEN_CONTEXT_DOWNGRADE_CANDIDATE | Lazio vs Pisa | market=HOME_WIN | audit=MISSED_WIN | note=Context downgrade missed a winning base BET; single sample is not enough for reversal.
- #3 | SHADOW_KEEP_VALIDATED_CASE | Kalmar FF vs Degerfors IF | market=OVER_1_5 | audit=KEPT_WIN | note=Adjusted portfolio kept a winner despite shadow risk.

## Guardrails
- This advisor does not change production behavior.
- It only recommends how to calibrate context filters after repeated samples.
