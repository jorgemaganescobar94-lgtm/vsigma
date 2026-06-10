# vSIGMA Pick Quality Classification - 2026-06-10

## Summary
- classification_rows: 3
- quality_class_counts: PENDING_FINAL_ACTUALS=3
- error_family_counts: PENDING=3
- learning_action_counts: WAIT_FOR_POSTMATCH_DATA=3
- manual_review_required_counts: NO=3
- auto_apply: NO
- production_change: NO

## Classification Rows
- PENDING_FINAL_ACTUALS | Almeria vs Castellón | market=OVER_1_5_SUPPORTED | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Nautico Recife vs Fortaleza EC | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Ponte Preta vs Cuiaba | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.

## Guardrails
- This classifier labels audit rows; it does not change model weights or picks.
- GREEN/RED labels are candidates until causal review confirms the lesson.
- NO_BET correctness requires real fixture context and manual/causal review.
- Diagnostic rows must not train the model.
