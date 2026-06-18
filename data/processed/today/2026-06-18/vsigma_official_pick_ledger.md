# vSIGMA Official Pick Ledger - 2026-06-18

## Summary
- ledger_rows: 1
- decision_bucket_counts: NO_BET=1
- ledger_status_counts: OFFICIAL_NO_BET=1
- official_pick_permission_counts: NO_PICK_NO_STAKE=1
- postmatch_audit_required_counts: YES=1
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | OFFICIAL_NO_BET | AC Oulu vs Mariehamn | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
