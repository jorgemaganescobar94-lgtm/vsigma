# vSIGMA No Bet Audit - 2026-06-10

## Summary
audit_rows: 2
- no_bet_audit_status_counts: NO_BET_AUDIT_NOT_APPLICABLE=1; NO_BET_CAUSAL_REVIEW_READY=1
- no_bet_quality_label_counts: NOT_A_NO_BET_ROW=1; NO_BET_TOO_CONSERVATIVE_CANDIDATE=1
- evidence_profile_counts: NO_POSTMATCH_PRESSURE_METRICS=1; LOW_EVENT_MATCH=1
- missed_opportunity_risk_counts: NOT_APPLICABLE=1; MEDIUM_TO_HIGH_PENDING_MARKET_REVIEW=1
- protection_value_signal_counts: NOT_APPLICABLE=1; LOW=1
- auto_apply: NO
- production_change: NO

## Audit Rows
- NO_BET_AUDIT_NOT_APPLICABLE | Malaga vs Las Palmas | quality=NOT_A_NO_BET_ROW | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=NOT_APPLICABLE | protection=NOT_APPLICABLE | manual=NO | note=Row is not a No Bet decision; handled by pick quality/market translation audits.
- NO_BET_CAUSAL_REVIEW_READY | Cape Town City vs Magesi | quality=NO_BET_TOO_CONSERVATIVE_CANDIDATE | evidence=LOW_EVENT_MATCH | missed=MEDIUM_TO_HIGH_PENDING_MARKET_REVIEW | protection=LOW | manual=YES | note=Final match looked low-event; review if a safe market was missed or if pre-match data correctly blocked it.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- NO_BET_PROTECTION_CANDIDATE and NO_BET_TOO_CONSERVATIVE_CANDIDATE are review labels, not final truth.
- A No Bet can only become a learning signal after causal review and sufficient sample size.
- Diagnostic rows must not train the model.
