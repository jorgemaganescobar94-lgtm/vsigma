# vSIGMA Postmatch Pick Audit - 2026-06-10

## Summary
- audit_rows: 2
- audit_status_counts: PENDING_FINAL_ACTUALS=1; NO_BET_AUDIT_READY=1
- pick_outcome_counts: PENDING=1; NO_PICK=1
- quality_label_counts: PENDING=1; NO_BET_PENDING_CAUSAL_REVIEW=1
- learning_signal_counts: WAIT_FOR_FINAL_ACTUALS=1; NO_BET_REVIEW_REQUIRED=1
- auto_apply: NO
- production_change: NO

## Audit Rows
- PENDING_FINAL_ACTUALS | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- NO_BET_AUDIT_READY | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | outcome=NO_PICK | quality=NO_BET_PENDING_CAUSAL_REVIEW | learning=NO_BET_REVIEW_REQUIRED | note=Final actuals found; review whether No Bet avoided risk or was too conservative.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- GREEN/RED results are not final learning by themselves; causal review is still required.
- NO_BET rows require separate correctness review when tied to a real fixture.
- Diagnostic rows do not train the model.
