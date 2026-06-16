# vSIGMA Official Pick Ledger - 2026-06-16

## Summary
- ledger_rows: 3
- decision_bucket_counts: NO_BET=3
- ledger_status_counts: OFFICIAL_NO_BET=3
- official_pick_permission_counts: NO_PICK_NO_STAKE=3
- postmatch_audit_required_counts: YES=3
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | OFFICIAL_NO_BET | FK Zalgiris Vilnius vs Panevėžys | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 2 | OFFICIAL_NO_BET | Suduva Marijampole vs Šiauliai | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 3 | OFFICIAL_NO_BET | TransINVEST Vilnius vs FK Trakai | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
