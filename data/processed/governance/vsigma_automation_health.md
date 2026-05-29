# vSIGMA Automation Health Monitor - 2026-05-29

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: OK=6; WARN=1; INFO=4
- status_counts: OK=7; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=OK | action=NO | detail=rows=2; decisions=NO_BET_OR_WATCH=1; NO_BET=1
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=NO_BET_OR_WATCH=1; CANCELLED_NO_BET=1
- live_trigger_validator | status=OK | severity=OK | action=NO | detail=windows=none; triggers=none
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=FT=7; 2H=10; 1H=1; NS=2
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=7
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=36; statuses=CALIBRATION_OK=2; MODEL_UNDER_ESTIMATING=2; MODEL_OVER_ESTIMATING=2
- calibration_memory_ledger | status=OK | severity=OK | action=NO | detail=global ledger exists
- daily_workflow_v2 | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_daily_decision_chain_v2.yml active externally
- prelock_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_prelock_live_recheck.yml expected active
- live_trigger_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_live_trigger_validator.yml expected active
- postmatch_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_full_post_match_learning_chain.yml expected active

## Guardrails
- Health monitor does not execute bets or change production behavior.
- WARN means review; BROKEN means a workflow/input needs fixing.
