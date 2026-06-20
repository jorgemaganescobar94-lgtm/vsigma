# vSIGMA Alert - 2026-06-20

System status: **ATTENTION**
Alert required: **YES**
Notify required: **YES**
Alert hash: `939b6d56d084f969ba6fb83b07ecd0ff5e843b33782fc4dd512e743dd251d3ea`

## Signals
- - #1 | LIVE_ONLY_WAIT_TRIGGER | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup=WAIT_PRELOCK | min=1165.65 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- - prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=CANCELLED_NO_BET=9; LIVE_ONLY_WAIT_TRIGGER=1
- - recheck_decision_counts: CANCELLED_NO_BET=9; LIVE_ONLY_WAIT_TRIGGER=1
- - total_goals | days=5 | rows=27 | hit_rate=0.371 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.

## Health Snapshot
```
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

```

## Live Trigger Snapshot
```
# vSIGMA Live Trigger Validator - 2026-06-20

## Summary
- rows_validated: 1
- window_counts: TOO_EARLY=1
- live_trigger_counts: TOO_EARLY=1
- auto_apply: NO
- production_change: NO

## Rows
- #1 | window=TOO_EARLY | decision=TOO_EARLY | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1165.65 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.

```

## Guardrails
- This issue is an alert only.
- Manual review is required before any action.
