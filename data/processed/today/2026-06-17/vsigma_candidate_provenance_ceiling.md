# vSIGMA Candidate Provenance Ceiling - 2026-06-17

## Summary
- rows_reviewed: 7
- ceiling_action_counts: NO_CHANGE=7
- candidate_origin_counts: TRANSLATOR_ONLY=7
- auto_apply: NO
- production_change: NO

## Ceiling Rows
- Gnistan vs Lahti | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- HJK Helsinki vs Inter Turku | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Ilves vs FF Jaro | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- SJK vs VPS | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Turku PS vs KuPS | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Hegelmann Litauen vs Džiugas Telšiai | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing
- Kauno Žalgiris vs Banga | origin=TRANSLATOR_ONLY | max=NO_BET | permission=NO_BET -> NO_BET | stake=NO_STAKE -> NO_STAKE | action=NO_CHANGE | reason=permission already within provenance ceiling or ledger missing

## Guardrails
- Ceiling enforcement is diagnostic/safety governance only.
- It can never upgrade a candidate beyond its provenance ceiling.
- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.
