# vSIGMA Forecast-to-Market Translator - 2026-05-29

## Summary
- rows_translated: 20
- execution_permission_counts: NO_BET_OR_WATCH=10; NO_BET=8; STAT_WATCH_ONLY=1; LIVE_ONLY=1
- primary_market_counts: NO_CLEAR_STAT_MARKET=8; OVER_1_5_SUPPORTED=6; UNDER_3_5_REVIEW=2; CARDS_OVER_3_5_REVIEW=2; CORNERS_OVER_8_5_REVIEW=1; BTTS_YES_REVIEW=1
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | STAT_WATCH_ONLY | Valerenga vs Kristiansund BK | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=48 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=58; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; statistical watch only; no portfolio/context confirmation
- #2 | NO_BET_OR_WATCH | Fredrikstad vs Start | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=23 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=33; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #3 | NO_BET_OR_WATCH | Orgryte IS vs IF Elfsborg | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=18 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=28; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #4 | LIVE_ONLY | Monza vs Catanzaro | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=17 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=33; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #5 | NO_BET_OR_WATCH | Aalesund vs Ham-Kam | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=16 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=34; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #6 | NO_BET_OR_WATCH | Tigre vs Alianza Atletico | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=12; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #7 | NO_BET_OR_WATCH | Rosenborg vs Bodo/Glimt | primary=CORNERS_OVER_8_5_REVIEW | secondary=CORNERS_OVER_9_5_AGGRESSIVE | score=-1 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=17; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #8 | NO_BET_OR_WATCH | Cruzeiro vs Barcelona SC | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #9 | NO_BET | America de Cali vs Macara | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-4 | stake=NO_STAKE | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=0; confidence=MEDIUM 71.6; portfolio=REVIEW_ONLY; no stat market has enough support
- #10 | NO_BET_OR_WATCH | Boca Juniors vs U. Catolica | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-4 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 62.6; portfolio=REVIEW_ONLY; negative translation score after guards
- #11 | NO_BET_OR_WATCH | Nice vs Saint Etienne | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-6 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=12; confidence=MEDIUM 66.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #12 | NO_BET_OR_WATCH | Brann vs Sarpsborg 08 FF | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=-20 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=28; confidence=LOW 57.6; portfolio=NO_PORTFOLIO_CONTEXT; low forecast confidence blocks execution; watch only
- #13 | NO_BET_OR_WATCH | KFUM Oslo vs Tromso | primary=BTTS_YES_REVIEW | secondary=OVER_1_5_REVIEW | score=-32 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=16; confidence=LOW 57.6; portfolio=NO_PORTFOLIO_CONTEXT; low forecast confidence blocks execution; watch only
- #14 | NO_BET | El Mokawloon vs Future FC | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #15 | NO_BET | Ghazl El Mehalla vs Haras El Hodood | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #16 | NO_BET | Masr vs Kahraba Ismailia | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #17 | NO_BET | National Bank of Egypt vs Al Ittihad | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #18 | NO_BET | FK Trakai vs Suduva Marijampole | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #19 | NO_BET | TransINVEST Vilnius vs Hegelmann Litauen | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #20 | NO_BET | Cde Juventud Italiana vs Tecnico Universitario | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
