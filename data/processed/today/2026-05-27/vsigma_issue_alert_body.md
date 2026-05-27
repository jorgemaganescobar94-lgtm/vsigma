# vSIGMA Alert - 2026-05-27

Generated: 2026-05-27T19:54:46+01:00
System status: **ATTENTION**
Alert required: **YES**

## Signals
- - prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- - live_trigger_validator | status=OK | severity=WARN | action=REVIEW_LIVE_WINDOW_MISSED_OR_FINISHED | detail=windows=MATCH_FINISHED=2; TOO_EARLY=2; triggers=MATCH_FINISHED=2; TOO_EARLY=2
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - recheck_decision_counts: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- - #1 | READY_LOW_STAKE_REVIEW | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=10.52 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- - #2 | READY_LOW_STAKE_REVIEW | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | stake=LOW_IF_CONFIRMED | lineup=LINEUPS_CONFIRMED | min=10.53 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=price/prelock/live confirmation | note=low-stake review allowed, not automatic
- - #3 | LIVE_ONLY_WAIT_TRIGGER | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1120.49 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - #4 | LIVE_ONLY_WAIT_TRIGGER | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | stake=SYMBOLIC_ONLY | lineup=WAIT_PRELOCK | min=1300.47 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
- - window_counts: MATCH_FINISHED=2; TOO_EARLY=2
- - live_trigger_counts: MATCH_FINISHED=2; TOO_EARLY=2
- - #1 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.52 | score=3-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- - #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.53 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- - memory_decision_counts: ACCUMULATE_MORE_SAMPLE=5; PATCH_CANDIDATE_REVIEW=1
- - total_goals | days=2 | rows=10 | hit_rate=0.100 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-05-27

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: WARN=3; OK=4; INFO=4
- status_counts: OK=7; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=WARN | action=REVIEW_BOARD | detail=rows=16; decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; NO_BET=4; PRELOCK_REVIEW_LOW_STAKE=2; LIVE_ONLY=2
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- live_trigger_validator | status=OK | severity=WARN | action=REVIEW_LIVE_WINDOW_MISSED_OR_FINISHED | detail=windows=MATCH_FINISHED=2; TOO_EARLY=2; triggers=MATCH_FINISHED=2; TOO_EARLY=2
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=FT=6; NS=10
- postmatch_stat_actuals | status=OK | severity=OK | action=NO | detail=rows_final=6
- forecast_calibration | status=OK | severity=OK | action=NO | detail=detail_rows=34; statuses=MODEL_OVER_ESTIMATING=3; MODEL_UNDER_ESTIMATING=2; CALIBRATION_OK=1
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
# vSIGMA Live Trigger Validator - 2026-05-27

## Summary
- rows_validated: 4
- window_counts: MATCH_FINISHED=2; TOO_EARLY=2
- live_trigger_counts: MATCH_FINISHED=2; TOO_EARLY=2
- auto_apply: NO
- production_change: NO

## Rows
- #1 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.52 | score=3-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.53 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | window=TOO_EARLY | decision=TOO_EARLY | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1120.49 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window
- #4 | window=TOO_EARLY | decision=TOO_EARLY | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1300.47 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.

```

## Guardrails
- This issue is an alert only.
- Manual review is required before any action.
