# vSIGMA Official Pick Ledger - 2026-06-17

## Summary
- ledger_rows: 7
- decision_bucket_counts: NO_BET=7
- ledger_status_counts: OFFICIAL_NO_BET=7
- official_pick_permission_counts: NO_PICK_NO_STAKE=7
- postmatch_audit_required_counts: YES=7
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | OFFICIAL_NO_BET | Gnistan vs Lahti | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 2 | OFFICIAL_NO_BET | HJK Helsinki vs Inter Turku | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 3 | OFFICIAL_NO_BET | Ilves vs FF Jaro | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 4 | OFFICIAL_NO_BET | SJK vs VPS | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 5 | OFFICIAL_NO_BET | Turku PS vs KuPS | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 6 | OFFICIAL_NO_BET | Hegelmann Litauen vs Džiugas Telšiai | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 7 | OFFICIAL_NO_BET | Kauno Žalgiris vs Banga | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
