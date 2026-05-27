# vSIGMA Alert - 2026-05-27

Generated: 2026-05-27T16:06:16+01:00
System status: **ATTENTION**
Alert required: **YES**

## Signals
- - prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - recheck_decision_counts: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- - #1 | READY_LOW_STAKE_REVIEW | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=10.52 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- - #2 | READY_LOW_STAKE_REVIEW | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=10.53 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- - #3 | LIVE_ONLY_WAIT_TRIGGER | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1120.49 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - #4 | LIVE_ONLY_WAIT_TRIGGER | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1300.47 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-05-27

## Summary
- system_status: ATTENTION
- components_checked: 9
- severity_counts: WARN=2; OK=4; INFO=3
- status_counts: OK=6; CONFIG_EXPECTED=3
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=WARN | action=REVIEW_BOARD | detail=rows=16; decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; NO_BET=4; PRELOCK_REVIEW_LOW_STAKE=2; LIVE_ONLY=2
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=FT=2; NS=2
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=2
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=0; statuses=none
- calibration_memory_ledger | status=OK | severity=OK | action=NO | detail=global ledger exists
- daily_workflow_v2 | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_daily_decision_chain_v2.yml active externally
- prelock_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_prelock_live_recheck.yml expected active
- postmatch_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_full_post_match_learning_chain.yml expected active

## Guardrails
- Health monitor does not execute bets or change production behavior.
- WARN means review; BROKEN means a workflow/input needs fixing.

```

## Guardrails
- This issue is an alert only.
- Manual review is required before any action.
