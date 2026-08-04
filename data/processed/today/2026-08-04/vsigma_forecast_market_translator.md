# vSIGMA Forecast-to-Market Translator - 2026-08-04

## Summary
- rows_translated: 1
- execution_permission_counts: NO_BET=1
- primary_market_counts: NO_CLEAR_STAT_MARKET=1
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET | Dundee Utd vs Rangers | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=CANDIDATE_PROVENANCE_CEILING | reason=stat_score=12; confidence=LOW 56.7; portfolio=LIVE_ONLY_OR_SYMBOLIC; low forecast confidence blocks execution; watch only; candidate_provenance_ceiling=max_permission=NO_BET; origin=OBJECTIVE_PROXY

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
