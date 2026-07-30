# vSIGMA Forecast-to-Market Translator - 2026-07-30

## Summary
- rows_translated: 4
- execution_permission_counts: NO_BET=4
- primary_market_counts: NO_CLEAR_STAT_MARKET=4
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET | IF Brommapojkarna vs Hammarby FF | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #2 | NO_BET | KFUM Oslo vs Molde | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #3 | NO_BET | Remo vs Vitoria | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=PROXY_BRIDGE_INVERSION_BLOCK | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market
- #4 | NO_BET | Aalesund vs Viking | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=CANDIDATE_PROVENANCE_CEILING | reason=stat_score=12; confidence=LOW 56.7; portfolio=LIVE_ONLY_OR_SYMBOLIC; low forecast confidence blocks execution; watch only; candidate_provenance_ceiling=max_permission=NO_BET; origin=OBJECTIVE_PROXY

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
