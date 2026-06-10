# vSIGMA Official Pick Ledger - 2026-06-10

## Summary
- ledger_rows: 2
- decision_bucket_counts: LIVE_ONLY=1; NO_BET=1
- ledger_status_counts: LIVE_REVIEW_REQUIRED=1; OFFICIAL_NO_BET=1
- official_pick_permission_counts: MANUAL_REVIEW_ONLY_NO_STAKE=1; NO_PICK_NO_STAKE=1
- postmatch_audit_required_counts: YES=2
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | LIVE_REVIEW_REQUIRED | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | decision=LIVE_ONLY | permission=MANUAL_REVIEW_ONLY_NO_STAKE | audit=YES
- 2 | OFFICIAL_NO_BET | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
