# vSIGMA Official Pick Ledger - 2026-06-21

## Summary
- ledger_rows: 6
- decision_bucket_counts: NO_BET=6
- ledger_status_counts: OFFICIAL_NO_BET=6
- official_pick_permission_counts: NO_PICK_NO_STAKE=6
- postmatch_audit_required_counts: YES=6
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | OFFICIAL_NO_BET | CRB vs Fortaleza EC | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 2 | OFFICIAL_NO_BET | Goias vs Operario-PR | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 3 | OFFICIAL_NO_BET | São Bernardo vs Juventude | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 4 | OFFICIAL_NO_BET | Barra vs Amazonas | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 5 | OFFICIAL_NO_BET | Brusque vs Floresta | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 6 | OFFICIAL_NO_BET | Ferroviária vs Inter De Limeira | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
