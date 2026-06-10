# vSIGMA Forecast-to-Market Translator - 2026-06-10

## Summary
- rows_translated: 2
- execution_permission_counts: LIVE_ONLY=1; NO_BET=1
- primary_market_counts: OVER_1_5_SUPPORTED=1; NO_CLEAR_STAT_MARKET=1
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | LIVE_ONLY | Malaga vs Las Palmas | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=17 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=33; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #2 | NO_BET | Cape Town City vs Magesi | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
