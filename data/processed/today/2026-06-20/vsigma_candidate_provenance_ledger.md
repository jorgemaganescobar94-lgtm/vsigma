# vSIGMA Candidate Provenance Ledger - 2026-06-20

## Summary
- rows_reviewed: 10
- candidate_origin_counts: TRANSLATOR_ONLY=9; REAL_SHORTLIST=1
- max_execution_permission_counts: NO_BET=9; LIVE_ONLY=1
- allowed_downstream_use_counts: NO_BET_ONLY=9; LIVE_CONFIRMATION_REQUIRED=1
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Ceara vs Botafogo SP | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Londrina vs Athletic Club | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Vila Nova vs Nautico Recife | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Panevėžys vs Šiauliai | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- TransINVEST Vilnius vs Kauno Žalgiris | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Banga vs FK Zalgiris Vilnius | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Anápolis vs AO Itabaiana | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Botafogo PB vs Volta Redonda | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Santa Cruz vs Ypiranga-RS | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Almeria vs Malaga | origin=REAL_SHORTLIST | market=OVER_1_5_SUPPORTED | direction=OVER_TEMPO | max_permission=LIVE_ONLY | strength=60 | allowed=LIVE_CONFIRMATION_REQUIRED | reason=dated shortlist row marked BET

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
