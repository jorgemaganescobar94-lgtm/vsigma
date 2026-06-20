# vSIGMA Official Pick Ledger - 2026-06-20

## Summary
- ledger_rows: 10
- decision_bucket_counts: NO_BET=9; LIVE_ONLY=1
- ledger_status_counts: OFFICIAL_NO_BET=9; LIVE_REVIEW_REQUIRED=1
- official_pick_permission_counts: NO_PICK_NO_STAKE=9; MANUAL_REVIEW_ONLY_NO_STAKE=1
- postmatch_audit_required_counts: YES=10
- auto_apply: NO
- production_change: NO

## Ledger Rows
- 1 | LIVE_REVIEW_REQUIRED | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | decision=LIVE_ONLY | permission=MANUAL_REVIEW_ONLY_NO_STAKE | audit=YES
- 2 | OFFICIAL_NO_BET | Ceara vs Botafogo SP | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 3 | OFFICIAL_NO_BET | Londrina vs Athletic Club | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 4 | OFFICIAL_NO_BET | Vila Nova vs Nautico Recife | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 5 | OFFICIAL_NO_BET | Banga vs FK Zalgiris Vilnius | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 6 | OFFICIAL_NO_BET | Panevėžys vs Šiauliai | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 7 | OFFICIAL_NO_BET | TransINVEST Vilnius vs Kauno Žalgiris | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 8 | OFFICIAL_NO_BET | Anápolis vs AO Itabaiana | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 9 | OFFICIAL_NO_BET | Botafogo PB vs Volta Redonda | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES
- 10 | OFFICIAL_NO_BET | Santa Cruz vs Ypiranga-RS | market=NO_CLEAR_STAT_MARKET | decision=NO_BET | permission=NO_PICK_NO_STAKE | audit=YES

## Guardrails
- This ledger records official daily decisions; it does not create picks.
- NO_BET rows are first-class learning objects, not failures by default.
- No row creates stake permission or betting execution.
- Postmatch quality labels remain PENDING until the postmatch audit chain fills them.
