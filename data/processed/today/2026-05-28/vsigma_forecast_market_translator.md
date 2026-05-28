# vSIGMA Forecast-to-Market Translator - 2026-05-28

## Summary
- rows_translated: 12
- execution_permission_counts: NO_BET_OR_WATCH=7; NO_BET=4; LIVE_ONLY=1
- primary_market_counts: NO_CLEAR_STAT_MARKET=4; OVER_1_5_SUPPORTED=2; BTTS_YES_REVIEW=2; UNDER_3_5_REVIEW=2; CORNERS_OVER_8_5_REVIEW=1; CARDS_OVER_3_5_REVIEW=1
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | NO_BET_OR_WATCH | River Plate vs Blooming | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=26 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=36; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #2 | NO_BET_OR_WATCH | RB Bragantino vs Carabobo FC | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=23 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=41; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #3 | NO_BET_OR_WATCH | Corinthians vs Platense | primary=BTTS_YES_REVIEW | secondary=OVER_1_5_REVIEW | score=6 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=16; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #4 | LIVE_ONLY | Palmeiras vs Junior | primary=CORNERS_OVER_8_5_REVIEW | secondary=CORNERS_OVER_9_5_AGGRESSIVE | score=5 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=17; confidence=MEDIUM 62.6; portfolio=REVIEW_ONLY; lineups/context require live or prelock confirmation
- #5 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=12; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #6 | NO_BET_OR_WATCH | Fluminense vs Deportivo La Guaira | primary=BTTS_YES_REVIEW | secondary=OVER_1_5_REVIEW | score=-2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=16; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #7 | NO_BET_OR_WATCH | Penarol vs Santa Fe | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-10 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #8 | NO_BET | Bolívar vs Independ. Rivadavia | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-24 | stake=NO_STAKE | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=0; confidence=MEDIUM 62.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; no stat market has enough support
- #9 | NO_BET_OR_WATCH | Casa Pia vs Torreense | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-34 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=20; confidence=LOW 49.6; portfolio=NO_PORTFOLIO_CONTEXT; low forecast confidence blocks execution; watch only
- #10 | NO_BET | El Geish vs Wadi Degla | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #11 | NO_BET | Ismaily SC vs Pharco | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #12 | NO_BET | Petrojet vs El Gouna FC | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
