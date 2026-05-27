# vSIGMA Forecast-to-Market Translator - 2026-05-27

## Summary
- rows_translated: 16
- execution_permission_counts: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; NO_BET=4; REVIEW_LOW_STAKE=2; LIVE_ONLY=2
- primary_market_counts: OVER_1_5_SUPPORTED=9; NO_CLEAR_STAT_MARKET=4; CARDS_OVER_3_5_REVIEW=3
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | STAT_WATCH_ONLY | Universitario vs Deportes Tolima | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=51 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=41; confidence=HIGH 81.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #2 | REVIEW_LOW_STAKE | Flamengo vs Cusco | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=45 | stake=LOW_IF_CONFIRMED | kill=NONE | reason=stat_score=33; confidence=HIGH 81.6; portfolio=EDGE_ONLY_REVIEW; stat forecast supports market but no automatic execution
- #3 | STAT_WATCH_ONLY | Racing Club vs Independiente Petrolero | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=45 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=55; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #4 | STAT_WATCH_ONLY | Caracas FC vs Botafogo | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=45 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=63; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #5 | REVIEW_LOW_STAKE | Club Nacional vs Coquimbo Unido | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=37 | stake=LOW_IF_CONFIRMED | kill=NONE | reason=stat_score=41; confidence=MEDIUM 72.6; portfolio=EDGE_ONLY_REVIEW; stat forecast supports market but no automatic execution
- #6 | STAT_WATCH_ONLY | Libertad Asuncion vs UCV | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=29 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=47; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #7 | LIVE_ONLY | Crystal Palace vs Rayo Vallecano | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=25 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=41; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #8 | NO_BET_OR_WATCH | Estudiantes L.P. vs Independiente Medellin | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=18 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=8; confidence=HIGH 81.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #9 | NO_BET_OR_WATCH | Independiente del Valle vs Rosario Central | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=18 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=28; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #10 | LIVE_ONLY | Olimpia vs A. Italiano | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=17 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=41; confidence=MEDIUM 62.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #11 | NO_BET | Santos vs Deportivo Cuenca | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=10 | stake=NO_STAKE | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=0; confidence=HIGH 81.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #12 | NO_BET | San Lorenzo vs Deportivo Recoleta | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=10 | stake=NO_STAKE | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=0; confidence=HIGH 81.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #13 | NO_BET_OR_WATCH | Vasco DA Gama vs Barracas Central | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #14 | NO_BET_OR_WATCH | Atletico-MG vs Puerto Cabello | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-10 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #15 | NO_BET | Cienciano vs Juventud | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-18 | stake=NO_STAKE | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=0; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #16 | NO_BET | Cuniburo vs Orense SC | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
