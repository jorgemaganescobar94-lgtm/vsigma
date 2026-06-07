# vSIGMA Alert - 2026-06-07

System status: **BROKEN**
Alert required: **YES**
Notify required: **YES**
Alert hash: `666f987e886617de8e2e06fa09918d39c09d38e4f64f28548b23d9cd2fe656b5`

## Signals
- - READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- - memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- - severity_counts: BROKEN=1; WARN=1; OK=5; INFO=4
- - system_status: BROKEN
- - total_goals | days=4 | rows=26 | hit_rate=0.347 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-06-07

## Summary
- system_status: BROKEN
- components_checked: 11
- severity_counts: BROKEN=1; WARN=1; OK=5; INFO=4
- status_counts: MISSING=1; OK=6; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=MISSING | severity=BROKEN | action=RUN_DAILY_DECISION_CHAIN_V2 | detail=vsigma_daily_execution_board.md/csv missing
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=none
- live_trigger_validator | status=OK | severity=OK | action=NO | detail=windows=none; triggers=none
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

```

## Live Trigger Snapshot
```
# vSIGMA Live Trigger Validator - 2026-06-07

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
