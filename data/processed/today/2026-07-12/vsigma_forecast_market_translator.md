# vSIGMA Forecast-to-Market Translator - 2026-07-12

## Summary
- rows_translated: 2
- execution_permission_counts: NO_BET=2
- primary_market_counts: NO_CLEAR_STAT_MARKET=2
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET | Gwangju FC vs Pohang Steelers | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=CANDIDATE_PROVENANCE_CEILING | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only; candidate_provenance_ceiling=max_permission=NO_BET; origin=OBJECTIVE_PROXY
- #2 | NO_BET | Ulsan Hyundai FC vs Jeonbuk Motors | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=PROXY_BRIDGE_INVERSION_BLOCK | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
