# vSIGMA Automation Health Monitor - 2026-05-27

## Summary
- system_status: BROKEN
- components_checked: 9
- severity_counts: BROKEN=1; WARN=1; OK=4; INFO=3
- status_counts: MISSING=1; OK=5; CONFIG_EXPECTED=3
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=none
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
