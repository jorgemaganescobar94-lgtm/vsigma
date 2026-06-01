# vSIGMA Forecast-to-Market Translator - 2026-06-01

## Summary
- rows_translated: 4
- execution_permission_counts: NO_BET=4
- primary_market_counts: NO_CLEAR_STAT_MARKET=4
- calibration_note: v68.1 blocks proxy-bridge inversion from tempo/over source into under/no-goals market.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET | Cordoba vs Huesca | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #2 | NO_BET | Almeria vs Valladolid | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #3 | NO_BET | RB Bragantino vs Internacional | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=PROXY_BRIDGE_INVERSION_BLOCK | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market
- #4 | NO_BET | Vasco DA Gama vs Atletico-MG | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=PROXY_BRIDGE_INVERSION_BLOCK | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market

## Guardrails
- This translator does not execute bets.
- Proxy bridge rows can support diagnostics only; they cannot invert tempo/over thesis into under/no-goals markets.
- Final execution still requires price/prelock/live confirmation.
