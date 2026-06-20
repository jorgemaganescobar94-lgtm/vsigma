# vSIGMA No Bet Audit - 2026-06-21

## Summary
audit_rows: 10
- no_bet_audit_status_counts: NO_BET_AUDIT_PENDING_FINAL_ACTUALS=9; NO_BET_AUDIT_NOT_APPLICABLE=1
- no_bet_quality_label_counts: PENDING=9; NOT_A_NO_BET_ROW=1
- evidence_profile_counts: NO_POSTMATCH_PRESSURE_METRICS=10
- missed_opportunity_risk_counts: PENDING=9; NOT_APPLICABLE=1
- protection_value_signal_counts: PENDING=9; NOT_APPLICABLE=1
- auto_apply: NO
- production_change: NO

## Audit Rows
- NO_BET_AUDIT_NOT_APPLICABLE | Almeria vs Malaga | quality=NOT_A_NO_BET_ROW | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=NOT_APPLICABLE | protection=NOT_APPLICABLE | manual=NO | note=Row is not a No Bet decision; handled by pick quality/market translation audits.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Ceara vs Botafogo SP | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Londrina vs Athletic Club | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Vila Nova vs Nautico Recife | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Banga vs FK Zalgiris Vilnius | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Panevėžys vs Šiauliai | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | TransINVEST Vilnius vs Kauno Žalgiris | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Anápolis vs AO Itabaiana | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Botafogo PB vs Volta Redonda | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Santa Cruz vs Ypiranga-RS | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- NO_BET_PROTECTION_CANDIDATE and NO_BET_TOO_CONSERVATIVE_CANDIDATE are review labels, not final truth.
- A No Bet can only become a learning signal after causal review and sufficient sample size.
- Diagnostic rows must not train the model.
