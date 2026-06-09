# vSIGMA Market Translation Audit - 2026-06-09

## Summary
- audit_rows: 1
- market_family_counts: NO_MARKET=1
- translation_audit_status_counts: TRANSLATION_NOT_REQUIRED_DIAGNOSTIC=1
- translation_quality_label_counts: DIAGNOSTIC_NO_MARKET_LEARNING=1
- translation_error_family_counts: NONE=1
- odds_escalation_counts: NOT_APPLICABLE=1
- auto_apply: NO
- production_change: NO

## Translation Rows
- TRANSLATION_NOT_REQUIRED_DIAGNOSTIC | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | family=NO_MARKET | market=NO_MARKET | quality=DIAGNOSTIC_NO_MARKET_LEARNING | safer=NO_MARKET | odds=NOT_APPLICABLE | note=Diagnostic/non-fixture row; market translation must not train the model.

## Guardrails
- This audit evaluates market translation only; it does not create picks or stake permission.
- Suggested safer families are advisory and require manual/causal review.
- Odds escalation is blocked by default unless sample and price checks later support it.
- Diagnostic rows must not train the model.
