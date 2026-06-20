# vSIGMA Forecast-to-Market Translator - 2026-06-20

## Summary
- rows_translated: 10
- execution_permission_counts: NO_BET=9; LIVE_ONLY=1
- primary_market_counts: NO_CLEAR_STAT_MARKET=9; OVER_1_5_SUPPORTED=1
- calibration_note: v68.2 candidate provenance ceiling applied after market translation.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | LIVE_ONLY | Almeria vs Malaga | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=28 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=44; confidence=MEDIUM 71.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #2 | NO_BET | Ceara vs Botafogo SP | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #3 | NO_BET | Londrina vs Athletic Club | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #4 | NO_BET | Vila Nova vs Nautico Recife | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #5 | NO_BET | Banga vs FK Zalgiris Vilnius | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #6 | NO_BET | Panevėžys vs Šiauliai | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #7 | NO_BET | TransINVEST Vilnius vs Kauno Žalgiris | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #8 | NO_BET | Anápolis vs AO Itabaiana | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #9 | NO_BET | Botafogo PB vs Volta Redonda | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support
- #10 | NO_BET | Santa Cruz vs Ypiranga-RS | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 51.1; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- Candidate provenance ceiling can only downgrade or preserve permissions.
- Final execution still requires price/prelock/live confirmation.
