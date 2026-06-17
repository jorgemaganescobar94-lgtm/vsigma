# vSIGMA Market Translation Audit - 2026-06-18

## Summary
- audit_rows: 2
- market_family_counts: UNKNOWN_FAMILY=2
- translation_audit_status_counts: TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW=2
- translation_quality_label_counts: PENDING=2
- translation_error_family_counts: PENDING=2
- odds_escalation_counts: NO_ESCALATION_PENDING=2
- auto_apply: NO
- production_change: NO

## Translation Rows
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Gnistan vs Lahti | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | SJK vs VPS | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.

## Guardrails
- This audit evaluates market translation only; it does not create picks or stake permission.
- Suggested safer families are advisory and require manual/causal review.
- Odds escalation is blocked by default unless sample and price checks later support it.
- Diagnostic rows must not train the model.
