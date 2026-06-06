# vSIGMA No Bet Audit - 2026-06-06

## Summary
audit_rows: 1
- no_bet_audit_status_counts: NO_BET_AUDIT_NOT_REQUIRED_DIAGNOSTIC=1
- no_bet_quality_label_counts: DIAGNOSTIC_NOT_REAL_FIXTURE_NO_BET=1
- evidence_profile_counts: NO_POSTMATCH_PRESSURE_METRICS=1
- missed_opportunity_risk_counts: NOT_APPLICABLE=1
- protection_value_signal_counts: NOT_APPLICABLE=1
- auto_apply: NO
- production_change: NO

## Audit Rows
- NO_BET_AUDIT_NOT_REQUIRED_DIAGNOSTIC | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | quality=DIAGNOSTIC_NOT_REAL_FIXTURE_NO_BET | evidence=NO_POSTMATCH_PRESSURE_METRICS | missed=NOT_APPLICABLE | protection=NOT_APPLICABLE | manual=NO | note=Diagnostic row; no fixture-level No Bet correctness can be evaluated.

## Guardrails
- This audit does not create picks, stake permission, or automatic model changes.
- NO_BET_PROTECTION_CANDIDATE and NO_BET_TOO_CONSERVATIVE_CANDIDATE are review labels, not final truth.
- A No Bet can only become a learning signal after causal review and sufficient sample size.
- Diagnostic rows must not train the model.
