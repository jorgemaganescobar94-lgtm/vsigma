# vSIGMA Postmatch Pick Audit - 2026-06-10

## Summary
- audit_rows: 3
- audit_status_counts: PENDING_FINAL_ACTUALS=3
- pick_outcome_counts: PENDING=3
- quality_label_counts: PENDING=3
- learning_signal_counts: WAIT_FOR_FINAL_ACTUALS=3
- auto_apply: NO
- production_change: NO

## Audit Rows
- PENDING_FINAL_ACTUALS | Almeria vs Castellón | market=OVER_1_5_SUPPORTED | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Nautico Recife vs Fortaleza EC | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Ponte Preta vs Cuiaba | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- GREEN/RED results are not final learning by themselves; causal review is still required.
- NO_BET rows require separate correctness review when tied to a real fixture.
- Diagnostic rows do not train the model.
