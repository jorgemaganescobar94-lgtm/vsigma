# vSIGMA Promotion Gate - 2026-06-18

## Executive Gate Summary
- generated_at: 2026-06-18T00:43:01+01:00
- experiments reviewed: 1
- promotion_decision_counts: NOT_READY_SAMPLE_TOO_SMALL=1
- auto_promote_counts: NO=1

## Gate Decisions
- NOT_READY_SAMPLE_TOO_SMALL | LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW | closed=1 | wins=1 | losses=0 | auto_promote=NO | production_change=NO | next=COLLECT_MORE_CLOSED_SAMPLES

## Guardrails
- auto_promote: NO for every gate decision
- production_change: NO for every gate decision
- official picks changed: NO
- predictive formulas changed: NO
- thresholds changed: NO
- calibration changed: NO
- ranking changed: NO
- market-selection changed: NO

## Policy
- This gate can classify evidence but cannot apply promotion.
- Any promotion requires a separate reviewed PR and sufficient closed matching samples.
