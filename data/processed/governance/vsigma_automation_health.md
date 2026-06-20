# vSIGMA Automation Health Monitor - 2026-06-20

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: WARN=2; INFO=5; OK=4
- status_counts: OK=7; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=WARN | action=REVIEW_BOARD | detail=rows=10; decisions=NO_BET=9; LIVE_ONLY=1
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=CANCELLED_NO_BET=9; LIVE_ONLY_WAIT_TRIGGER=1
- live_trigger_validator | status=OK | severity=INFO | action=WAIT_FOR_LIVE_WINDOW | detail=windows=TOO_EARLY=1; triggers=TOO_EARLY=1
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=NS=1
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=0
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=0; statuses=none
- calibration_memory_ledger | status=OK | severity=OK | action=NO | detail=global ledger exists
- daily_workflow_v2 | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_daily_decision_chain_v2.yml active externally
- prelock_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_prelock_live_recheck.yml expected active
- live_trigger_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_live_trigger_validator.yml expected active
- postmatch_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_full_post_match_learning_chain.yml expected active

## Guardrails
- Health monitor does not execute bets or change production behavior.
- WARN means review; BROKEN means a workflow/input needs fixing.
