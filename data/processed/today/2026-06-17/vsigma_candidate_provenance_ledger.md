# vSIGMA Candidate Provenance Ledger - 2026-06-17

## Summary
- rows_reviewed: 7
- candidate_origin_counts: TRANSLATOR_ONLY=7
- max_execution_permission_counts: NO_BET=7
- allowed_downstream_use_counts: NO_BET_ONLY=7
- auto_apply: NO
- production_change: NO

## Candidate Rows
- HJK Helsinki vs Inter Turku | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Ilves vs FF Jaro | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Turku PS vs KuPS | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Gnistan vs Lahti | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- SJK vs VPS | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Hegelmann Litauen vs Džiugas Telšiai | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin
- Kauno Žalgiris vs Banga | origin=TRANSLATOR_ONLY | market=NO_CLEAR_STAT_MARKET | direction=UNKNOWN | max_permission=NO_BET | strength=8 | allowed=NO_BET_ONLY | reason=translator row exists without identifiable shortlist origin

## Guardrails
- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.
- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.
- Real shortlist rows still require downstream gates, price, lineups and manual review.
