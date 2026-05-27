# vSIGMA Prelock/Live Recheck - 2026-05-27

## Summary
- rows_rechecked: 16
- recheck_decision_counts: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Recheck Rows
- #1 | READY_LOW_STAKE_REVIEW | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=10.52 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- #2 | READY_LOW_STAKE_REVIEW | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=10.53 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- #3 | LIVE_ONLY_WAIT_TRIGGER | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1120.49 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #4 | LIVE_ONLY_WAIT_TRIGGER | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1300.47 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #5 | STAT_WATCH_ONLY | Universitario vs Deportes Tolima | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #6 | STAT_WATCH_ONLY | Racing Club vs Independiente Petrolero | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #7 | STAT_WATCH_ONLY | Caracas FC vs Botafogo | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #8 | STAT_WATCH_ONLY | Libertad Asuncion vs UCV | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #9 | NO_BET_OR_WATCH | Estudiantes L.P. vs Independiente Medellin | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #10 | NO_BET_OR_WATCH | Independiente del Valle vs Rosario Central | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #11 | NO_BET_OR_WATCH | Vasco DA Gama vs Barracas Central | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #12 | NO_BET_OR_WATCH | Atletico-MG vs Puerto Cabello | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #13 | CANCELLED_NO_BET | Santos vs Deportivo Cuenca | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #14 | CANCELLED_NO_BET | San Lorenzo vs Deportivo Recoleta | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #15 | CANCELLED_NO_BET | Cienciano vs Juventud | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #16 | CANCELLED_NO_BET | Cuniburo vs Orense SC | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence

## Guardrails
- This recheck does not execute automatically.
- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
