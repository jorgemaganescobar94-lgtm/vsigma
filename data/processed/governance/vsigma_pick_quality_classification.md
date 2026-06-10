# vSIGMA Pick Quality Classification - 2026-06-10

## Summary
- classification_rows: 2
- quality_class_counts: PENDING_FINAL_ACTUALS=1; NO_BET_CAUSAL_REVIEW_REQUIRED=1
- error_family_counts: PENDING=1; NO_BET_REVIEW=1
- learning_action_counts: WAIT_FOR_POSTMATCH_DATA=1; REVIEW_NO_BET_CORRECTNESS=1
- manual_review_required_counts: NO=1; YES=1
- auto_apply: NO
- production_change: NO

## Classification Rows
- PENDING_FINAL_ACTUALS | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- NO_BET_CAUSAL_REVIEW_REQUIRED | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | outcome=NO_PICK | error=NO_BET_REVIEW | action=REVIEW_NO_BET_CORRECTNESS | manual=YES | note=Real fixture no-bet has final actuals; classify as correct protection or too conservative.

## Guardrails
- This classifier labels audit rows; it does not change model weights or picks.
- GREEN/RED labels are candidates until causal review confirms the lesson.
- NO_BET correctness requires real fixture context and manual/causal review.
- Diagnostic rows must not train the model.
