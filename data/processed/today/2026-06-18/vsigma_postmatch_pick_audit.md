# vSIGMA Postmatch Pick Audit - 2026-06-18

## Summary
- audit_rows: 2
- audit_status_counts: PENDING_FINAL_ACTUALS=2
- pick_outcome_counts: PENDING=2
- quality_label_counts: PENDING=2
- learning_signal_counts: WAIT_FOR_FINAL_ACTUALS=2
- auto_apply: NO
- production_change: NO

## Audit Rows
- PENDING_FINAL_ACTUALS | Gnistan vs Lahti | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | SJK vs VPS | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- GREEN/RED results are not final learning by themselves; causal review is still required.
- NO_BET rows require separate correctness review when tied to a real fixture.
- Diagnostic rows do not train the model.
