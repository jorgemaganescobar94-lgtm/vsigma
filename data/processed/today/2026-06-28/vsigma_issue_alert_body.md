# vSIGMA Alert - 2026-06-28

System status: **BROKEN**
Alert required: **YES**
Notify required: **YES**
Alert hash: `8061b9fe7858865634a60a9eaf272169f0423f2e26b4f9810922923d4e2d9150`

## Signals
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- - severity_counts: BROKEN=1; WARN=1; OK=2; INFO=7
- - system_status: BROKEN

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-06-28

## Summary
- system_status: BROKEN
- components_checked: 11
- severity_counts: BROKEN=1; WARN=1; OK=2; INFO=7
- status_counts: MISSING=2; OK=2; WAITING_OR_NOT_RUN=3; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- prelock_live_recheck | status=MISSING | severity=WARN | action=RUN_PRELOCK_RECHECK | detail=prelock/live report missing
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

```

## Live Trigger Snapshot
```
# vSIGMA Live Trigger Validator - 2026-06-28

## Summary
- rows_validated: 0
- window_counts: none
- live_trigger_counts: none
- auto_apply: NO
- production_change: NO

## Rows
- none. No live/prelock candidates found.

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.

```

## Guardrails
- This issue is an alert only.
- Manual review is required before any action.
