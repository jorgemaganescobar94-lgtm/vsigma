# vSIGMA No Bet Audit - 2026-06-18

## Summary
audit_rows: 2
- no_bet_audit_status_counts: NO_BET_AUDIT_PENDING_FINAL_ACTUALS=2
- no_bet_quality_label_counts: PENDING=2
- evidence_profile_counts: NO_POSTMATCH_PRESSURE_METRICS=2
- missed_opportunity_risk_counts: PENDING=2
- protection_value_signal_counts: PENDING=2
- auto_apply: NO
- production_change: NO

## Audit Rows
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | Gnistan vs Lahti | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.
- NO_BET_AUDIT_PENDING_FINAL_ACTUALS | SJK vs VPS | quality=PENDING | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=PENDING | protection=PENDING | manual=NO | note=Real No Bet row but final actuals are not available yet.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- NO_BET_PROTECTION_CANDIDATE and NO_BET_TOO_CONSERVATIVE_CANDIDATE are review labels, not final truth.
- A No Bet can only become a learning signal after causal review and sufficient sample size.
- Diagnostic rows must not train the model.
