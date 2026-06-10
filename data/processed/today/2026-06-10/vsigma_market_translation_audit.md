# vSIGMA Market Translation Audit - 2026-06-10

## Summary
- audit_rows: 3
- market_family_counts: UNKNOWN_FAMILY=2; TOTAL_GOALS=1
- translation_audit_status_counts: TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW=3
- translation_quality_label_counts: PENDING=3
- translation_error_family_counts: PENDING=3
- odds_escalation_counts: NO_ESCALATION_PENDING=3
- auto_apply: NO
- production_change: NO

## Translation Rows
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Almeria vs Castellón | family=TOTAL_GOALS | market=OVER_1_5_SUPPORTED | quality=PENDING | safer=SAME_TOTAL_FAMILY_REVIEW_LINE_WIDTH | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Nautico Recife vs Fortaleza EC | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Ponte Preta vs Cuiaba | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.

## Guardrails
- This audit evaluates market translation only; it does not create picks or stake permission.
- Suggested safer families are advisory and require manual/causal review.
- Odds escalation is blocked by default unless sample and price checks later support it.
- Diagnostic rows must not train the model.
