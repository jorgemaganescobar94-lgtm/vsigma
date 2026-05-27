# vSIGMA Forecast-to-Market Translator - 2026-05-27

## Summary
- rows_translated: 10
- execution_permission_counts: LIVE_ONLY=4; STAT_WATCH_ONLY=2; NO_BET_OR_WATCH=2; NO_BET=2
- primary_market_counts: OVER_1_5_SUPPORTED=6; CARDS_OVER_3_5_REVIEW=2; NO_CLEAR_STAT_MARKET=2
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | STAT_WATCH_ONLY | Racing Club vs Independiente Petrolero | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=45 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=55; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #2 | STAT_WATCH_ONLY | Caracas FC vs Botafogo | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=45 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=63; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #3 | LIVE_ONLY | Crystal Palace vs Rayo Vallecano | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=37 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=41; confidence=MEDIUM 71.6; portfolio=REVIEW_ONLY; lineups/context require live or prelock confirmation
- #4 | LIVE_ONLY | Libertad Asuncion vs UCV | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=35 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=47; confidence=MEDIUM 62.6; portfolio=REVIEW_ONLY; lineups/context require live or prelock confirmation
- #5 | LIVE_ONLY | Olimpia vs A. Italiano | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=17 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=41; confidence=MEDIUM 62.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #6 | LIVE_ONLY | Independiente del Valle vs Rosario Central | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=12 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=28; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #7 | NO_BET_OR_WATCH | Vasco DA Gama vs Barracas Central | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #8 | NO_BET_OR_WATCH | Atletico-MG vs Puerto Cabello | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-10 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #9 | NO_BET | Cienciano vs Juventud | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-18 | stake=NO_STAKE | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=0; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #10 | NO_BET | Cuniburo vs Orense SC | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
