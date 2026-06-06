# vSIGMA Postmatch Pick Audit - 2026-06-06

## Summary
- audit_rows: 1
- audit_status_counts: AUDIT_NOT_REQUIRED_DIAGNOSTIC=1
- pick_outcome_counts: NO_PICK=1
- quality_label_counts: DIAGNOSTIC_NO_PICK=1
- learning_signal_counts: NO_LEARNING_DIAGNOSTIC_ONLY=1
- auto_apply: NO
- production_change: NO

## Audit Rows
- AUDIT_NOT_REQUIRED_DIAGNOSTIC | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | market=NO_MARKET | outcome=NO_PICK | quality=DIAGNOSTIC_NO_PICK | learning=NO_LEARNING_DIAGNOSTIC_ONLY | note=Diagnostic row from empty/no-promotion board; not a fixture-level decision.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- GREEN/RED results are not final learning by themselves; causal review is still required.
- NO_BET rows require separate correctness review when tied to a real fixture.
- Diagnostic rows do not train the model.
