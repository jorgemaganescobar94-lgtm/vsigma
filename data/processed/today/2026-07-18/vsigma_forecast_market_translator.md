# vSIGMA Forecast-to-Market Translator - 2026-07-18

## Summary
- rows_translated: 3
- execution_permission_counts: NO_BET=3
- primary_market_counts: NO_CLEAR_STAT_MARKET=3
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET | Malisheva vs Vllaznia Shkodër | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #2 | NO_BET | Atert Bissen vs KI Klaksvik | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #3 | NO_BET | Universitatea Craiova vs ML Vitebsk | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=PROXY_BRIDGE_INVERSION_BLOCK | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
