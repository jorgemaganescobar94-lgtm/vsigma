# vSIGMA Forecast-to-Market Translator - 2026-05-26

## Summary
- rows_translated: 6
- execution_permission_counts: NO_BET_OR_WATCH=5; LIVE_ONLY=1
- primary_market_counts: UNDER_3_5_REVIEW=3; BTTS_YES_REVIEW=1; CARDS_OVER_3_5_REVIEW=1; CORNERS_OVER_8_5_REVIEW=1
- calibration_note: v46.2 separates statistical watchlist from live execution when portfolio context is missing.
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Translated Rows
- #1 | LIVE_ONLY | LDU de Quito vs Always Ready | primary=BTTS_YES_REVIEW | secondary=OVER_1_5_REVIEW | score=23 | stake=SYMBOLIC_ONLY | kill=NONE | reason=stat_score=35; confidence=MEDIUM 62.6; portfolio=REVIEW_ONLY; lineups/context require live or prelock confirmation
- #2 | NO_BET_OR_WATCH | Sao Paulo vs Boston River | primary=UNDER_3_5_REVIEW | secondary=CORNERS_OVER_8_5_REVIEW | score=11 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=29; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #3 | NO_BET_OR_WATCH | Gremio vs Atletico Torque | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=20; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #4 | NO_BET_OR_WATCH | Palestino vs Deportivo Riestra | primary=UNDER_3_5_REVIEW | secondary=NO_GOALS_AGGRESSION | score=2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NO_PORTFOLIO_CONTEXT | reason=stat_score=20; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; no portfolio/context confirmation and score not strong enough
- #5 | NO_BET_OR_WATCH | Lanus vs Mirassol | primary=CARDS_OVER_3_5_REVIEW | secondary=CARDS_OVER_4_5_AGGRESSIVE | score=-2 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=8; confidence=MEDIUM 71.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards
- #6 | NO_BET_OR_WATCH | Millonarios vs O'Higgins | primary=CORNERS_OVER_8_5_REVIEW | secondary=CORNERS_OVER_9_5_AGGRESSIVE | score=-7 | stake=NO_STAKE_OR_SYMBOLIC | kill=NEGATIVE_TRANSLATION_SCORE | reason=stat_score=11; confidence=MEDIUM 62.6; portfolio=NO_PORTFOLIO_CONTEXT; negative translation score after guards

## Guardrails
- This translator does not execute bets.
- No portfolio/context confirmation means STAT_WATCH_ONLY at most, not live execution.
- Final execution still requires price/prelock/live confirmation.
