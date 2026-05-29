# vSIGMA Forecast-to-Market Translator - 2026-05-29

## Summary
- rows_translated: 2
- execution_permission_counts: NO_BET_OR_WATCH=1; NO_BET=1
- primary_market_counts: UNDER_3_5_REVIEW=1; NO_CLEAR_STAT_MARKET=1
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET_OR_WATCH | Nice vs Saint Etienne | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-12 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=12; confidence=MEDIUM 66.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; negative translation score after guards
- #2 | NO_BET | Cde Juventud Italiana vs Tecnico Universitario | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
