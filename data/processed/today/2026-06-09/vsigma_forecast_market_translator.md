# vSIGMA Forecast-to-Market Translator - 2026-06-09

## Summary
- rows_translated: 3
- execution_permission_counts: NO_BET=2; LIVE_ONLY=1
- primary_market_counts: NO_CLEAR_STAT_MARKET=2; OVER_1_5_SUPPORTED=1
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | LIVE_ONLY | Almeria vs Castellón | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=28 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=44; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #2 | NO_BET | Nautico Recife vs Fortaleza EC | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #3 | NO_BET | Ponte Preta vs Cuiaba | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
