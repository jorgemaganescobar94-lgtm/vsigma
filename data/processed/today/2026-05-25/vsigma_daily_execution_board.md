# vSIGMA Daily Execution Board - 2026-05-25

## Summary
- rows_on_board: 6
- final_decision_counts: STAT_WATCH_ONLY=2; PRELOCK_REVIEW_LOW_STAKE=1; LIVE_ONLY=1; NO_BET_OR_WATCH=1; NO_BET=1
- board_bucket_counts: WATCHLIST=2; CANDIDATE_REVIEW=1; LIVE_CANDIDATE=1; WEAK_WATCH=1; BLOCKED=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Board Rows
- #1 | PRELOCK_REVIEW_LOW_STAKE | IF Elfsborg vs BK Hacken | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=LOW_IF_CONFIRMED | score=41 | conf=MEDIUM | bucket=CANDIDATE_REVIEW | stats=goals 2.35-3.90 | shots 20-31 | SoT 6-11 | corners 8-13 | cards 3-7 | prelock=price remains above minimum; market not over-compressed; no new attacking/availability downgrade | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=new availability downgrade
- #2 | LIVE_ONLY | SC Paderborn 07 vs VfL Wolfsburg | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=SYMBOLIC_ONLY | score=26 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 2.65-4.35 | shots 22-34 | SoT 7-14 | corners 9-15 | cards 2-5 | prelock=price remains above minimum; market not over-compressed; lineups confirmed; no new attacking/availability downgrade | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups; new availability downgrade
- #3 | STAT_WATCH_ONLY | IFK Goteborg vs Mjallby AIF | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=37 | conf=MEDIUM | bucket=WATCHLIST | stats=goals 2.40-3.98 | shots 25-38 | SoT 8-14 | corners 8-15 | cards 2-5 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups; new availability downgrade
- #4 | STAT_WATCH_ONLY | Sandefjord vs Fredrikstad | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=32 | conf=MEDIUM | bucket=WATCHLIST | stats=goals 2.10-3.52 | shots 25-37 | SoT 6-12 | corners 10-16 | cards 2-5 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups; new availability downgrade
- #5 | NO_BET_OR_WATCH | ST Mirren vs Partick | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | stake=NO_STAKE_OR_SYMBOLIC | score=-42 | conf=LOW | bucket=WEAK_WATCH | stats=goals 1.56-3.07 | shots 13-23 | SoT 4-10 | corners 7-15 | cards 1-5 | prelock=none | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; low forecast confidence; bad or incomplete lineups
- #6 | NO_BET | Botafogo SP vs Athletic Club | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence

## Guardrails
- This board is a decision dashboard, not an auto-bet executor.
- REVIEW_LOW_STAKE still requires price/prelock/live confirmation.
- STAT_WATCH_ONLY is observation only unless promoted by context/portfolio later.
