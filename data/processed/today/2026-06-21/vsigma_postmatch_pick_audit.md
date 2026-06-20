# vSIGMA Postmatch Pick Audit - 2026-06-21

## Summary
- audit_rows: 10
- audit_status_counts: PENDING_FINAL_ACTUALS=10
- pick_outcome_counts: PENDING=10
- quality_label_counts: PENDING=10
- learning_signal_counts: WAIT_FOR_FINAL_ACTUALS=10
- auto_apply: NO
- production_change: NO

## Audit Rows
- PENDING_FINAL_ACTUALS | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Ceara vs Botafogo SP | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Londrina vs Athletic Club | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Vila Nova vs Nautico Recife | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Banga vs FK Zalgiris Vilnius | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Panevėžys vs Šiauliai | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | TransINVEST Vilnius vs Kauno Žalgiris | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Anápolis vs AO Itabaiana | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Botafogo PB vs Volta Redonda | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.
- PENDING_FINAL_ACTUALS | Santa Cruz vs Ypiranga-RS | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | quality=PENDING | learning=WAIT_FOR_FINAL_ACTUALS | note=No final actuals found for fixture yet.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- GREEN/RED results are not final learning by themselves; causal review is still required.
- NO_BET rows require separate correctness review when tied to a real fixture.
- Diagnostic rows do not train the model.
