# vSIGMA Candidate Provenance Ceiling - 2026-06-20

## Summary
- rows_reviewed: 10
- ceiling_action_counts: NO_CHANGE=10
- candidate_origin_counts: TRANSLATOR_ONLY=9; REAL_SHORTLIST=1
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Almeria vs Malaga | origin=REAL_SHORTLIST | max=LIVE_ONLY | permission=LIVE_ONLY -> LIVE_ONLY | stake=SYMBOLIC_ONLY -> SYMBOLIC_ONLY | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Ceara vs Botafogo SP | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Londrina vs Athletic Club | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Vila Nova vs Nautico Recife | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Banga vs FK Zalgiris Vilnius | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Panevėžys vs Šiauliai | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- TransINVEST Vilnius vs Kauno Žalgiris | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Anápolis vs AO Itabaiana | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Botafogo PB vs Volta Redonda | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Santa Cruz vs Ypiranga-RS | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
