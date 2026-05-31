# vSIGMA Prelock/Live Recheck - 2026-05-31

## Summary
- rows_rechecked: 24
- recheck_decision_counts: CANCELLED_NO_BET=11; STAT_WATCH_ONLY=5; LIVE_ONLY_WAIT_TRIGGER=4; NO_BET_OR_WATCH=4
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Recheck Rows
- #1 | LIVE_ONLY_WAIT_TRIGGER | Cordoba vs Huesca | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup=WAIT_PRELOCK | min=633.49 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #2 | LIVE_ONLY_WAIT_TRIGGER | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_PRELOCK | lineup=WAIT_PRELOCK | min=333.43 | availability=AVAILABILITY_ELEVATED_BOTH | next=wait for live trigger | note=prematch serious stake blocked
- #3 | LIVE_ONLY_WAIT_TRIGGER | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup=WAIT_PRELOCK | min=483.51 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #4 | LIVE_ONLY_WAIT_TRIGGER | Vasco DA Gama vs Atletico-MG | market=BTTS_YES_REVIEW | stake=NO_STAKE_PRELOCK | lineup=WAIT_PRELOCK | min=633.42 | availability=AVAILABILITY_REPORTED_ADVISORY | next=wait for live trigger | note=prematch serious stake blocked
- #5 | STAT_WATCH_ONLY | Leganes vs Mirandes | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #6 | STAT_WATCH_ONLY | Zaragoza vs Malaga | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_PRELOCK | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #7 | STAT_WATCH_ONLY | Vasteras SK FK vs IFK Goteborg | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_PRELOCK | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #8 | STAT_WATCH_ONLY | Racing Santander vs Cadiz | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #9 | STAT_WATCH_ONLY | Castellón vs Eibar | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #10 | NO_BET_OR_WATCH | BK Hacken vs Hammarby FF | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_PRELOCK | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #11 | NO_BET_OR_WATCH | Degerfors IF vs IF Brommapojkarna | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_PRELOCK | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #12 | NO_BET_OR_WATCH | Gent vs Genk | market=CORNERS_OVER_8_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #13 | NO_BET_OR_WATCH | Palmeiras vs Chapecoense-sc | market=CORNERS_OVER_8_5_REVIEW | stake=NO_STAKE_PRELOCK | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #14 | CANCELLED_NO_BET | Burgos vs FC Andorra | market=OVER_1_5_SUPPORTED | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #15 | CANCELLED_NO_BET | Deportivo La Coruna vs Las Palmas | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #16 | CANCELLED_NO_BET | Ceara vs Operario-PR | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #17 | CANCELLED_NO_BET | Londrina vs Vila Nova | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #18 | CANCELLED_NO_BET | São Bernardo vs Novorizontino | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #19 | CANCELLED_NO_BET | AC Oulu vs FF Jaro | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #20 | CANCELLED_NO_BET | Kauno Žalgiris vs FK Zalgiris Vilnius | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #21 | CANCELLED_NO_BET | Anápolis vs Maranhão | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #22 | CANCELLED_NO_BET | Guarani Campinas vs Amazonas | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #23 | CANCELLED_NO_BET | Inter De Limeira vs Ypiranga-RS | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #24 | CANCELLED_NO_BET | Santa Cruz vs Ferroviária | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence

## Guardrails
- This recheck does not execute automatically.
- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
