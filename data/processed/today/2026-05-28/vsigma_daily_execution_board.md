# vSIGMA Daily Execution Board - 2026-05-28

## Summary
- rows_on_board: 3
- final_decision_counts: NO_BET_OR_WATCH=2; LIVE_ONLY=1
- board_bucket_counts: WEAK_WATCH=2; LIVE_CANDIDATE=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Board Rows
- #1 | LIVE_ONLY | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | alt=CORNERS_OVER_9_5_AGGRESSIVE | stake=SYMBOLIC_ONLY | score=5 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 1.49-2.76 | shots 22-35 | SoT 5-10 | corners 10-18 | cards 2-6 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #2 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | stake=NO_STAKE_OR_SYMBOLIC | score=2 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.66-2.84 | shots 21-32 | SoT 5-10 | corners 8-13 | cards 2-6 | prelock=none | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #3 | NO_BET_OR_WATCH | Casa Pia vs Torreense | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | stake=NO_STAKE_OR_SYMBOLIC | score=-22 | conf=LOW | bucket=WEAK_WATCH | stats=goals 1.49-2.76 | shots 13-22 | SoT 4-9 | corners 7-13 | cards 4-9 | prelock=none | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; low forecast confidence

## Guardrails
- This board is a decision dashboard, not an auto-bet executor.
- REVIEW_LOW_STAKE still requires price/prelock/live confirmation.
- STAT_WATCH_ONLY is observation only unless promoted by context/portfolio later.
