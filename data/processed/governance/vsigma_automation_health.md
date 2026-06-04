# vSIGMA Automation Health Monitor - 2026-06-04

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: OK=3; WARN=1; INFO=7
- status_counts: OK=4; WAITING_OR_NOT_RUN=3; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=OK | action=NO | detail=rows=0; decisions=NO_BET=0
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=none
- live_trigger_validator | status=OK | severity=OK | action=NO | detail=windows=none; triggers=none
- postmatch_results_refresh | status=WAITING_OR_NOT_RUN | severity=INFO | action=NO_IF_MATCHES_NOT_FINISHED | detail=postmatch refresh not present yet
- postmatch_stat_actuals | status=WAITING_OR_NOT_RUN | severity=INFO | action=NO_IF_MATCHES_NOT_FINISHED | detail=actuals report not present yet
- forecast_calibration | status=WAITING_OR_NOT_RUN | severity=INFO | action=NO_IF_MATCHES_NOT_FINISHED | detail=calibration report not present yet
- calibration_memory_ledger | status=OK | severity=OK | action=NO | detail=global ledger exists
- daily_workflow_v2 | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_daily_decision_chain_v2.yml active externally
- prelock_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_prelock_live_recheck.yml expected active
- live_trigger_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_live_trigger_validator.yml expected active
- postmatch_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_full_post_match_learning_chain.yml expected active

## Guardrails
- Health monitor does not execute bets or change production behavior.
- WARN means review; BROKEN means a workflow/input needs fixing.
