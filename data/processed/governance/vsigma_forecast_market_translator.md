# vSIGMA Forecast-to-Market Translator - 2026-05-28

## Summary
- rows_translated: 3
- execution_permission_counts: NO_BET_OR_WATCH=2; LIVE_ONLY=1
- primary_market_counts: UNDER_3_5_REVIEW=2; CORNERS_OVER_8_5_REVIEW=1
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | LIVE_ONLY | Palmeiras vs Junior | primary=CORNERS_OVER_8_5_REVIEW | secondary=CORNERS_OVER_9_5_AGGRESSIVE | score=5 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=17; confidence=MEDIUM 62.6; portfolio=REVIEW_ONLY; lineups/context require live or prelock confirmation
- #2 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=12; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #3 | NO_BET_OR_WATCH | Casa Pia vs Torreense | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=-22 | stake=NO_STAKE_OR_SYMBOLIC | kill=LOW_FORECAST_CONFIDENCE | reason=stat_score=20; confidence=LOW 59.6; portfolio=NO_PORTFOLIO_CONTEXT; low forecast confidence blocks execution; watch only

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
