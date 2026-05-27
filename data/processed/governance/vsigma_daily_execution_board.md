# vSIGMA Daily Execution Board - 2026-05-27

## Summary
- rows_on_board: 10
- final_decision_counts: LIVE_ONLY=4; STAT_WATCH_ONLY=2; NO_BET_OR_WATCH=2; NO_BET=2
- board_bucket_counts: LIVE_CANDIDATE=4; WATCHLIST=2; WEAK_WATCH=2; BLOCKED=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Board Rows
- #1 | LIVE_ONLY | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=SYMBOLIC_ONLY | score=37 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 2.05-3.45 | shots 22-33 | SoT 7-12 | corners 7-13 | cards 4-9 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #2 | LIVE_ONLY | Libertad Asuncion vs UCV | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=SYMBOLIC_ONLY | score=35 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 2.35-4.15 | shots 22-35 | SoT 7-13 | corners 8-14 | cards 3-9 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #3 | LIVE_ONLY | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=SYMBOLIC_ONLY | score=17 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 2.16-3.84 | shots 20-33 | SoT 6-12 | corners 6-12 | cards 3-9 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #4 | LIVE_ONLY | Independiente del Valle vs Rosario Central | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=SYMBOLIC_ONLY | score=12 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 2.05-3.45 | shots 22-33 | SoT 6-11 | corners 8-14 | cards 3-7 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #5 | STAT_WATCH_ONLY | Racing Club vs Independiente Petrolero | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=45 | conf=MEDIUM | bucket=WATCHLIST | stats=goals 2.20-3.67 | shots 24-37 | SoT 7-14 | corners 8-14 | cards 2-6 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #6 | STAT_WATCH_ONLY | Caracas FC vs Botafogo | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=45 | conf=MEDIUM | bucket=WATCHLIST | stats=goals 2.16-3.84 | shots 24-38 | SoT 7-13 | corners 8-14 | cards 3-8 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #7 | NO_BET_OR_WATCH | Vasco DA Gama vs Barracas Central | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | stake=NO_STAKE_OR_SYMBOLIC | score=-2 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.56-2.69 | shots 22-33 | SoT 7-13 | corners 8-14 | cards 3-7 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #8 | NO_BET_OR_WATCH | Atletico-MG vs Puerto Cabello | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | stake=NO_STAKE_OR_SYMBOLIC | score=-10 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 2.02-3.61 | shots 21-33 | SoT 5-11 | corners 6-12 | cards 3-8 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #9 | NO_BET | Cienciano vs Juventud | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-18 | conf=MEDIUM | bucket=BLOCKED | stats=goals 1.78-3.22 | shots 20-32 | SoT 6-12 | corners 7-14 | cards 1-4 | prelock=none | live=none | cancel=default no bet; bad or incomplete lineups
- #10 | NO_BET | Cuniburo vs Orense SC | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence

## Guardrails
- This board is a decision dashboard, not an auto-bet executor.
- REVIEW_LOW_STAKE still requires price/prelock/live confirmation.
- STAT_WATCH_ONLY is observation only unless promoted by context/portfolio later.
