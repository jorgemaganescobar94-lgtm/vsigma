# vSIGMA Official Pick Ledger - 2026-06-17

## Summary
- ledger_rows: 2
- decision_bucket_counts: NO_BET=2
- ledger_status_counts: OFFICIAL_NO_BET=2
- official_pick_permission_counts: NO_PICK_NO_STAKE=2
- postmatch_audit_required_counts: YES=2
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | OFFICIAL_NO_BET | Gnistan vs Lahti | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 2 | OFFICIAL_NO_BET | SJK vs VPS | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
