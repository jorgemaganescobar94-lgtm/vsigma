# vSIGMA Prelock/Live Recheck - 2026-05-28

## Summary
- rows_rechecked: 12
- recheck_decision_counts: NO_BET_OR_WATCH=7; CANCELLED_NO_BET=4; LIVE_ONLY_WAIT_TRIGGER=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Recheck Rows
- #1 | LIVE_ONLY_WAIT_TRIGGER | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1337.37 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #2 | NO_BET_OR_WATCH | River Plate vs Blooming | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #3 | NO_BET_OR_WATCH | RB Bragantino vs Carabobo FC | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #4 | NO_BET_OR_WATCH | Corinthians vs Platense | market=BTTS_YES_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #5 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | market=UNDER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #6 | NO_BET_OR_WATCH | Fluminense vs Deportivo La Guaira | market=BTTS_YES_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #7 | NO_BET_OR_WATCH | Penarol vs Santa Fe | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #8 | NO_BET_OR_WATCH | Casa Pia vs Torreense | market=UNDER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #9 | CANCELLED_NO_BET | Bolívar vs Independ. Rivadavia | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup=LINEUPS_NOT_CONFIRMED | min=47.39 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=none | note=blocked by board or low confidence
- #10 | CANCELLED_NO_BET | El Geish vs Wadi Degla | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #11 | CANCELLED_NO_BET | Ismaily SC vs Pharco | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #12 | CANCELLED_NO_BET | Petrojet vs El Gouna FC | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence

## Guardrails
- This recheck does not execute automatically.
- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
