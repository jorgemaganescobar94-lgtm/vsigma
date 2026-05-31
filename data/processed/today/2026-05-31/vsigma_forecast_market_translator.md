# vSIGMA Forecast-to-Market Translator - 2026-05-31

## Summary
- rows_translated: 24
- execution_permission_counts: NO_BET=10; STAT_WATCH_ONLY=5; NO_BET_OR_WATCH=5; LIVE_ONLY=4
- primary_market_counts: OVER_1_5_SUPPORTED=11; NO_CLEAR_STAT_MARKET=10; CORNERS_OVER_8_5_REVIEW=2; BTTS_YES_REVIEW=1
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | STAT_WATCH_ONLY | Leganes vs Mirandes | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=53 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=63; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #2 | STAT_WATCH_ONLY | Zaragoza vs Malaga | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=53 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=63; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #3 | STAT_WATCH_ONLY | Vasteras SK FK vs IFK Goteborg | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=37 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=55; confidence=MEDIUM 66.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #4 | LIVE_ONLY | Cordoba vs Huesca | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=36 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=52; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #5 | STAT_WATCH_ONLY | Racing Santander vs Cadiz | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=32 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=42; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #6 | STAT_WATCH_ONLY | Castellón vs Eibar | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=31 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=41; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #7 | NO_BET_OR_WATCH | BK Hacken vs Hammarby FF | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=21 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=39; confidence=MEDIUM 66.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #8 | NO_BET_OR_WATCH | Degerfors IF vs IF Brommapojkarna | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=18 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=28; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #9 | NO_BET_OR_WATCH | Burgos vs FC Andorra | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=18 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=28; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #10 | LIVE_ONLY | RB Bragantino vs Internacional | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=17 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=41; confidence=MEDIUM 66.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #11 | LIVE_ONLY | Almeria vs Valladolid | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=12 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=28; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #12 | LIVE_ONLY | Vasco DA Gama vs Atletico-MG | primary=BTTS_YES_REVIEW | secondary=OVER_1_5_REVIEW | score=11 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=35; confidence=MEDIUM 66.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #13 | NO_BET_OR_WATCH | Gent vs Genk | primary=CORNERS_OVER_8_5_REVIEW | secondary=CORNERS_OVER_9_5_AGGRESSIVE | score=1 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=11; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #14 | NO_BET | Deportivo La Coruna vs Las Palmas | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-10 | stake=NO_STAKE | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=0; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #15 | NO_BET_OR_WATCH | Palmeiras vs Chapecoense-sc | primary=CORNERS_OVER_8_5_REVIEW | secondary=CORNERS_OVER_9_5_AGGRESSIVE | score=-26 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=22; confidence=LOW 57.6; portfolio=NO_PORTFOLIO_CONTEXT; low forecast confidence blocks execution; watch only
- #16 | NO_BET | Ceara vs Operario-PR | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #17 | NO_BET | Londrina vs Vila Nova | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #18 | NO_BET | São Bernardo vs Novorizontino | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #19 | NO_BET | AC Oulu vs FF Jaro | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #20 | NO_BET | Kauno Žalgiris vs FK Zalgiris Vilnius | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #21 | NO_BET | Anápolis vs Maranhão | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #22 | NO_BET | Guarani Campinas vs Amazonas | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #23 | NO_BET | Inter De Limeira vs Ypiranga-RS | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #24 | NO_BET | Santa Cruz vs Ferroviária | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
