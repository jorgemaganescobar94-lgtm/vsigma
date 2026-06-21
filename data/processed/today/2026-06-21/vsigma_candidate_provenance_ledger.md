# vSIGMA Candidate Provenance Ledger - 2026-06-21

## Summary
- rows_reviewed: 11
- candidate_origin_counts: TRANSLATOR_ONLY=11
- max_execution_permission_counts: NO_BET=11
- allowed_downstream_use_counts: NO_BET_ONLY=11
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Avai vs Cuiaba | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- CRB vs Fortaleza EC | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Goias vs Operario-PR | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- São Bernardo vs Juventude | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Džiugas Telšiai vs Suduva Marijampole | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Barra vs Amazonas | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Brusque vs Floresta | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Ferroviária vs Inter De Limeira | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Ituano vs Figueirense | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Maranhão vs Paysandu | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Caxias vs Maringá | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
