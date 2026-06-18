# vSIGMA Alert - 2026-06-18

System status: **BROKEN**
Alert required: **YES**
Notify required: **YES**
Alert hash: `c48be77071319b9d6b53ceafcbe316d6455e592b71e8351cee40a9a330f8e63f`

## Signals
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- - memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- - severity_counts: BROKEN=1; WARN=1; OK=5; INFO=4
- - system_status: BROKEN
- - total_goals | days=5 | rows=27 | hit_rate=0.371 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-06-18

## Summary
- system_status: BROKEN
- components_checked: 11
- severity_counts: BROKEN=1; WARN=1; OK=5; INFO=4
- status_counts: MISSING=2; OK=5; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- prelock_live_recheck | status=MISSING | severity=WARN | action=RUN_PRELOCK_RECHECK | detail=prelock/live report missing
- live_trigger_validator | status=OK | severity=OK | action=NO | detail=windows=none; triggers=none
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=PST=2; FT=32; NS=91; HT=4
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=32
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=0; statuses=none
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
# vSIGMA Live Trigger Validator - 2026-06-18

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
