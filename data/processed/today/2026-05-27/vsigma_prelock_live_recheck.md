# vSIGMA Prelock/Live Recheck - 2026-05-27

## Summary
- rows_rechecked: 10
- recheck_decision_counts: LIVE_ONLY_WAIT_TRIGGER=4; STAT_WATCH_ONLY=2; NO_BET_OR_WATCH=2; CANCELLED_NO_BET=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Recheck Rows
- #1 | LIVE_ONLY_WAIT_TRIGGER | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=LINEUPS_NOT_CONFIRMED | min=46.25 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #2 | LIVE_ONLY_WAIT_TRIGGER | Libertad Asuncion vs UCV | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=226.25 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #3 | LIVE_ONLY_WAIT_TRIGGER | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=226.22 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #4 | LIVE_ONLY_WAIT_TRIGGER | Independiente del Valle vs Rosario Central | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=226.26 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #5 | STAT_WATCH_ONLY | Racing Club vs Independiente Petrolero | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #6 | STAT_WATCH_ONLY | Caracas FC vs Botafogo | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #7 | NO_BET_OR_WATCH | Vasco DA Gama vs Barracas Central | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #8 | NO_BET_OR_WATCH | Atletico-MG vs Puerto Cabello | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #9 | CANCELLED_NO_BET | Cienciano vs Juventud | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #10 | CANCELLED_NO_BET | Cuniburo vs Orense SC | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence

## Guardrails
- This recheck does not execute automatically.
- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
