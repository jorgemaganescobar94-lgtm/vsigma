# vSIGMA Market Translation Audit - 2026-06-10

## Summary
- audit_rows: 2
- market_family_counts: TOTAL_GOALS=1; UNKNOWN_FAMILY=1
- translation_audit_status_counts: TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW=1; NO_BET_TRANSLATION_REVIEW_REQUIRED=1
- translation_quality_label_counts: PENDING=1; NO_BET_MARKET_OPPORTUNITY_REVIEW=1
- translation_error_family_counts: PENDING=1; NO_BET_CORRECTNESS_PENDING=1
- odds_escalation_counts: NO_ESCALATION_PENDING=1; NOT_APPLICABLE=1
- auto_apply: NO
- production_change: NO

## Translation Rows
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Malaga vs Las Palmas | family=TOTAL_GOALS | market=OVER_1_5_SUPPORTED | quality=PENDING | safer=SAME_TOTAL_FAMILY_REVIEW_LINE_WIDTH | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- NO_BET_TRANSLATION_REVIEW_REQUIRED | Cape Town City vs Magesi | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=NO_BET_MARKET_OPPORTUNITY_REVIEW | safer=REVIEW_IF_ANY_MARKET_SHOULD_HAVE_EXISTED | odds=NOT_APPLICABLE | note=Real fixture no-bet must be reviewed for correct protection vs excessive conservatism.

## Guardrails
- This audit evaluates market translation only; it does not create picks or stake permission.
- Suggested safer families are advisory and require manual/causal review.
- Odds escalation is blocked by default unless sample and price checks later support it.
- Diagnostic rows must not train the model.
