# vSIGMA Prelock/Live Recheck - 2026-05-25

## Summary
- rows_rechecked: 6
- recheck_decision_counts: STAT_WATCH_ONLY=2; READY_LOW_STAKE_REVIEW=1; LIVE_ONLY_WAIT_TRIGGER=1; NO_BET_OR_WATCH=1; CANCELLED_NO_BET=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Recheck Rows
- #1 | READY_LOW_STAKE_REVIEW | IF Elfsborg vs BK Hacken | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=24.33 | availability=AVAILABILITY_REPORTED_ADVISORY | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- #2 | LIVE_ONLY_WAIT_TRIGGER | SC Paderborn 07 vs VfL Wolfsburg | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=114.34 | availability=AVAILABILITY_REPORTED_ADVISORY | next=wait for live trigger | note=prematch serious stake blocked
- #3 | STAT_WATCH_ONLY | IFK Goteborg vs Mjallby AIF | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #4 | STAT_WATCH_ONLY | Sandefjord vs Fredrikstad | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=rerun full chain if promoted | note=stat signal lacks portfolio context
- #5 | NO_BET_OR_WATCH | ST Mirren vs Partick | market=UNDER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence
- #6 | CANCELLED_NO_BET | Botafogo SP vs Athletic Club | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence

## Guardrails
- This recheck does not execute automatically.
- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
