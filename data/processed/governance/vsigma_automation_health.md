# vSIGMA Automation Health Monitor - 2026-05-27

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: WARN=3; OK=4; INFO=4
- status_counts: OK=7; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=WARN | action=REVIEW_BOARD | detail=rows=16; decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; NO_BET=4; PRELOCK_REVIEW_LOW_STAKE=2; LIVE_ONLY=2
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- live_trigger_validator | status=OK | severity=WARN | action=REVIEW_LIVE_WINDOW_MISSED_OR_FINISHED | detail=windows=MATCH_FINISHED=2; TOO_EARLY=2; triggers=MATCH_FINISHED=2; TOO_EARLY=2
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=FT=6; NS=10
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=6
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=34; statuses=MODEL_OVER_ESTIMATING=3; MODEL_UNDER_ESTIMATING=2; CALIBRATION_OK=1
- calibration_memory_ledger | status=OK | severity=OK | action=NO | detail=global ledger exists
- daily_workflow_v2 | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_daily_decision_chain_v2.yml active externally
- prelock_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_prelock_live_recheck.yml expected active
- live_trigger_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_live_trigger_validator.yml expected active
- postmatch_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_full_post_match_learning_chain.yml expected active

## Guardrails
- Health monitor does not execute bets or change production behavior.
- WARN means review; BROKEN means a workflow/input needs fixing.
