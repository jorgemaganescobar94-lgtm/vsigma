# vSIGMA Pick Quality Classification - 2026-06-18

## Summary
- classification_rows: 2
- quality_class_counts: PENDING_FINAL_ACTUALS=2
- error_family_counts: PENDING=2
- learning_action_counts: WAIT_FOR_POSTMATCH_DATA=2
- manual_review_required_counts: NO=2
- auto_apply: NO
- production_change: NO

## Classification Rows
- PENDING_FINAL_ACTUALS | Gnistan vs Lahti | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | SJK vs VPS | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.

## Guardrails
- This classifier labels audit rows; it does not change model weights or picks.
- GREEN/RED labels are candidates until causal review confirms the lesson.
- NO_BET correctness requires real fixture context and manual/causal review.
- Diagnostic rows must not train the model.
