# vSIGMA Market Translation Audit - 2026-06-21

## Summary
- audit_rows: 10
- market_family_counts: UNKNOWN_FAMILY=9; TOTAL_GOALS=1
- translation_audit_status_counts: TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW=10
- translation_quality_label_counts: PENDING=10
- translation_error_family_counts: PENDING=10
- odds_escalation_counts: NO_ESCALATION_PENDING=10
- auto_apply: NO
- production_change: NO

## Translation Rows
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Almeria vs Malaga | family=TOTAL_GOALS | market=OVER_1_5_SUPPORTED | quality=PENDING | safer=SAME_TOTAL_FAMILY_REVIEW_LINE_WIDTH | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Ceara vs Botafogo SP | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Londrina vs Athletic Club | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Vila Nova vs Nautico Recife | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Banga vs FK Zalgiris Vilnius | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Panevėžys vs Šiauliai | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | TransINVEST Vilnius vs Kauno Žalgiris | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Anápolis vs AO Itabaiana | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Botafogo PB vs Volta Redonda | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.
- TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW | Santa Cruz vs Ypiranga-RS | family=UNKNOWN_FAMILY | market=NO_CLEAR_STAT_MARKET | quality=PENDING | safer=MANUAL_FAMILY_REVIEW | odds=NO_ESCALATION_PENDING | note=Waiting for final actuals or causal review before judging market translation.

## Guardrails
- This audit evaluates market translation only; it does not create picks or stake permission.
- Suggested safer families are advisory and require manual/causal review.
- Odds escalation is blocked by default unless sample and price checks later support it.
- Diagnostic rows must not train the model.
