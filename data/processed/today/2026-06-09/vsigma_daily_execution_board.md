# vSIGMA Daily Execution Board - 2026-06-09

## Summary
- rows_on_board: 3
- final_decision_counts: NO_BET=2; LIVE_ONLY=1
- board_bucket_counts: BLOCKED=2; LIVE_CANDIDATE=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Board Rows
- #1 | LIVE_ONLY | Almeria vs Castellón | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=SYMBOLIC_ONLY | score=28 | conf=MEDIUM | bucket=LIVE_CANDIDATE | stats=goals 3.09-5.04 | shots 24-36 | SoT 9-16 | corners 8-14 | cards 3-7 | prelock=price remains above minimum; market not over-compressed; lineups confirmed | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #2 | NO_BET | Nautico Recife vs Fortaleza EC | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence
- #3 | NO_BET | Ponte Preta vs Cuiaba | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence

## Guardrails
- This board is a decision dashboard, not an auto-bet executor.
- REVIEW_LOW_STAKE still requires price/prelock/live confirmation.
- STAT_WATCH_ONLY is observation only unless promoted by context/portfolio later.
