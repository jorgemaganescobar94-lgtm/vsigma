# vSIGMA Forecast-to-Market Translator - 2026-05-25

## Summary
- rows_translated: 6
- execution_permission_counts: LIVE_ONLY=4; REVIEW_LOW_STAKE=1; NO_BET=1
- primary_market_counts: OVER_1_5_SUPPORTED=4; UNDER_3_5_REVIEW=1; NO_CLEAR_STAT_MARKET=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | REVIEW_LOW_STAKE | IF Elfsborg vs BK Hacken | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=41 | stake=LOW_IF_CONFIRMED | kill=NONE | reason=stat_score=41; confidence=MEDIUM 76.6; portfolio=REVIEW_ONLY; stat forecast supports market but no automatic execution
- #2 | LIVE_ONLY | IFK Goteborg vs Mjallby AIF | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=37 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=55; confidence=MEDIUM 66.6; portfolio=NO_PORTFOLIO_CONTEXT; lineups/context require live or prelock confirmation
- #3 | LIVE_ONLY | Sandefjord vs Fredrikstad | primary=OVER_1_5_SUPPORTED | secondary=BTTS_OR_OVER_1_5_REVIEW | score=32 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=50; confidence=MEDIUM 66.6; portfolio=NO_PORTFOLIO_CONTEXT; lineups/context require live or prelock confirmation
- #4 | LIVE_ONLY | SC Paderborn 07 vs VfL Wolfsburg | primary=OVER_1_5_SUPPORTED | secondary=OVER_2_5_REVIEW | score=26 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=50; confidence=MEDIUM 66.6; portfolio=LIVE_ONLY_OR_SYMBOLIC; lineups/context require live or prelock confirmation
- #5 | LIVE_ONLY | ST Mirren vs Partick | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-42 | stake=SYMBOLIC_ONLY | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=12; confidence=LOW 49.6; portfolio=NO_PORTFOLIO_CONTEXT; lineups/context require live or prelock confirmation
- #6 | NO_BET | Botafogo SP vs Athletic Club | primary=NO_CLEAR_STAT_MARKET | secondary=NONE | score=-42 | stake=NO_STAKE | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=0; confidence=LOW 55.6; portfolio=NO_PORTFOLIO_CONTEXT; no stat market has enough support

## Guardrails
- This translator does not execute bets.
- It downgrades for low confidence, lineups inactive, availability risk, low conversion and context matrix status.
- Final execution still requires price/prelock/live confirmation.
