# vSIGMA Pick Quality Classification - 2026-06-06

## Summary
- classification_rows: 1
- quality_class_counts: DIAGNOSTIC_NO_LEARNING=1
- error_family_counts: NONE=1
- learning_action_counts: NO_MODEL_CHANGE=1
- manual_review_required_counts: NO=1
- auto_apply: NO
- production_change: NO

## Classification Rows
- DIAGNOSTIC_NO_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | market=NO_MARKET | outcome=NO_PICK | error=NONE | action=NO_MODEL_CHANGE | manual=NO | note=Diagnostic row; not a fixture-level pick/no-bet and must not train the model.

## Guardrails
- This classifier labels audit rows; it does not change model weights or picks.
- GREEN/RED labels are candidates until causal review confirms the lesson.
- NO_BET correctness requires real fixture context and manual/causal review.
- Diagnostic rows must not train the model.
