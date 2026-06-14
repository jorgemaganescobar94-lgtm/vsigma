# vSIGMA Market Translation Audit - 2026-06-15

## Summary
- audit_rows: 1
- market_family_counts: TOTAL_GOALS=1
- translation_audit_status_counts: TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW=1
- translation_quality_label_counts: PENDING=1
- translation_error_family_counts: PENDING=1
- odds_escalation_counts: NO_ESCALATION_PENDING=1
- auto_apply: NO
- production_change: NO

## Translation Rows
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Malaga vs Las Palmas | family=TOTAL_GOALS | market=OVER_1_5_SUPPORTED | quality=PENDING | safer=SAME_TOTAL_FAMILY_REVIEW_LINE_WIDTH | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.

## Guardrails
- This audit evaluates market translation only; it does not create picks or stake permission.
- Suggested safer families are advisory and require manual/causal review.
- Odds escalation is blocked by default unless sample and price checks later support it.
- Diagnostic rows must not train the model.
