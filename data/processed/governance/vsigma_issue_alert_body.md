# vSIGMA Alert - 2026-06-10

System status: **ATTENTION**
Alert required: **YES**
Notify required: **YES**
Alert hash: `55cc9eff672c75d7d9fc52a31710433cc02c092611fa0a8384e5181ccf7ecb0c`

## Signals
- - READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- - total_goals | days=5 | rows=27 | hit_rate=0.371 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-06-10

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: WARN=2; OK=5; INFO=4
- status_counts: OK=7; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=WARN | action=REVIEW_BOARD | detail=rows=2; decisions=LIVE_ONLY=1; NO_BET=1
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=none
- live_trigger_validator | status=OK | severity=OK | action=NO | detail=windows=none; triggers=none
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=FT=1; NS=1
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=1
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=1; statuses=LOW_SAMPLE_HOLD=1
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
# vSIGMA Live Trigger Validator - 2026-06-10

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
