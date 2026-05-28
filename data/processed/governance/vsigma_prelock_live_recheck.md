# vSIGMA Prelock/Live Recheck - 2026-05-28

## Summary
- rows_rechecked: 3
- recheck_decision_counts: NO_BET_OR_WATCH=2; LIVE_ONLY_WAIT_TRIGGER=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Recheck Rows
- #1 | LIVE_ONLY_WAIT_TRIGGER | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=196.53 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- #2 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | market=UNDER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #3 | NO_BET_OR_WATCH | Casa Pia vs Torreense | market=UNDER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=none | note=blocked by board or low confidence

## Guardrails
- This recheck does not execute automatically.
- READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
