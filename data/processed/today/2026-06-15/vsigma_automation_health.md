# vSIGMA Automation Health Monitor - 2026-06-15

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: OK=6; WARN=1; INFO=4
- status_counts: OK=6; MISSING=1; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=OK | action=NO | detail=rows=1; decisions=NO_BET=1
- prelock_live_recheck | status=MISSING | severity=WARN | action=RUN_PRELOCK_RECHECK | detail=prelock/live report missing
- live_trigger_validator | status=OK | severity=OK | action=NO | detail=windows=none; triggers=none
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=FT=12; NS=52; PST=5; 1H=1; HT=1; SUSP=1
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=12
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=0; statuses=none
- calibration_memory_ledger | status=OK | severity=OK | action=NO | detail=global ledger exists
- daily_workflow_v2 | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_daily_decision_chain_v2.yml active externally
- prelock_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_prelock_live_recheck.yml expected active
- live_trigger_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_live_trigger_validator.yml expected active
- postmatch_workflow | status=CONFIG_EXPECTED | severity=INFO | action=CHECK_GH_WORKFLOW_LIST_IF_NEEDED | detail=vsigma_full_post_match_learning_chain.yml expected active

## Guardrails
- Health monitor does not execute bets or change production behavior.
- WARN means review; BROKEN means a workflow/input needs fixing.
