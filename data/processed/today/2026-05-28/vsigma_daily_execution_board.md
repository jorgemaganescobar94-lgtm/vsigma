# vSIGMA Daily Execution Board - 2026-05-28

## Summary
- rows_on_board: 12
- final_decision_counts: NO_BET_OR_WATCH=7; NO_BET=4; LIVE_ONLY=1
- board_bucket_counts: WEAK_WATCH=7; BLOCKED=4; LIVE_CANDIDATE=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Board Rows
- #1 | LIVE_ONLY | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | alt=CORNERS_OVER_9_5_AGGRESSIVE | stake=SYMBOLIC_ONLY | score=5 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 1.49-2.76 | shots 22-35 | SoT 5-10 | corners 10-18 | cards 2-6 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #2 | NO_BET_OR_WATCH | River Plate vs Blooming | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=26 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 2.05-3.45 | shots 23-34 | SoT 7-14 | corners 8-13 | cards 5-10 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #3 | NO_BET_OR_WATCH | RB Bragantino vs Carabobo FC | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=23 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 2.35-4.15 | shots 22-35 | SoT 7-14 | corners 7-14 | cards 3-8 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #4 | NO_BET_OR_WATCH | Corinthians vs Platense | market=BTTS_YES_REVIEW | alt=OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=6 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.41-2.46 | shots 19-29 | SoT 7-13 | corners 6-11 | cards 2-5 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #5 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | stake=NO_STAKE_OR_SYMBOLIC | score=2 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.66-2.84 | shots 21-32 | SoT 5-10 | corners 8-13 | cards 2-6 | prelock=none | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #6 | NO_BET_OR_WATCH | Fluminense vs Deportivo La Guaira | market=BTTS_YES_REVIEW | alt=OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=-2 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.63-2.99 | shots 18-29 | SoT 6-12 | corners 5-10 | cards 2-7 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #7 | NO_BET_OR_WATCH | Penarol vs Santa Fe | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | stake=NO_STAKE_OR_SYMBOLIC | score=-10 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.83-3.30 | shots 18-29 | SoT 6-12 | corners 4-8 | cards 3-8 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #8 | NO_BET_OR_WATCH | Casa Pia vs Torreense | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | stake=NO_STAKE_OR_SYMBOLIC | score=-34 | conf=LOW | bucket=WEAK_WATCH | stats=goals 1.42-2.83 | shots 13-23 | SoT 4-9 | corners 6-13 | cards 3-9 | prelock=none | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; low forecast confidence; bad or incomplete lineups
- #9 | NO_BET | Bolívar vs Independ. Rivadavia | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-24 | conf=MEDIUM | bucket=BLOCKED | stats=goals 1.97-3.53 | shots 21-34 | SoT 7-13 | corners 6-12 | cards 2-7 | prelock=none | live=none | cancel=default no bet; bad or incomplete lineups
- #10 | NO_BET | El Geish vs Wadi Degla | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence
- #11 | NO_BET | Ismaily SC vs Pharco | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence
- #12 | NO_BET | Petrojet vs El Gouna FC | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence

## Guardrails
- This board is a decision dashboard, not an auto-bet executor.
- REVIEW_LOW_STAKE still requires price/prelock/live confirmation.
- STAT_WATCH_ONLY is observation only unless promoted by context/portfolio later.
