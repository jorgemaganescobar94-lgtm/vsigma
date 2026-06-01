# vSIGMA Forecast-to-Market Translator - 2026-06-01

## Summary
- rows_translated: 4
- execution_permission_counts: NO_BET_OR_WATCH=2; NO_BET=2
- primary_market_counts: UNDER_3_5_REVIEW=2; NO_CLEAR_STAT_MARKET=2
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET_OR_WATCH | RB Bragantino vs Internacional | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-22 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only
- #2 | NO_BET_OR_WATCH | Vasco DA Gama vs Atletico-MG | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-22 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=12; confidence=LOW 56.7; portfolio=REVIEW_ONLY; low forecast confidence blocks execution; watch only
- #3 | NO_BET | Cordoba vs Huesca | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support
- #4 | NO_BET | Almeria vs Valladolid | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-34 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 56.7; portfolio=REVIEW_ONLY; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
