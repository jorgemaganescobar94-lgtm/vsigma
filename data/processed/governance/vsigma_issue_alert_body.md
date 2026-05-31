# vSIGMA Alert - 2026-05-31

System status: **ATTENTION**
Alert required: **YES**
Notify required: **YES**
Alert hash: `713aa1a0ac570e05f277423c0081cfb18ec95f369ea542f6fc3eeb8a7db3addc`

## Signals
- - #1 | LIVE_ONLY_WAIT_TRIGGER | Cordoba vs Huesca | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup=WAIT_PRELOCK | min=633.49 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - #2 | LIVE_ONLY_WAIT_TRIGGER | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_PRELOCK | lineup=WAIT_PRELOCK | min=333.43 | availability=AVAILABILITY_ELEVATED_BOTH | next=wait for live trigger | note=prematch serious stake blocked
- - #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=333.43 | score=3-1 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- - #3 | LIVE_ONLY_WAIT_TRIGGER | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup=WAIT_PRELOCK | min=483.51 | availability=AVAILABILITY_UNKNOWN_OR_CLEAN | next=wait for live trigger | note=prematch serious stake blocked
- - #3 | window=TOO_LATE | decision=TOO_LATE | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | status=2H | min=56.0 | mtko=483.51 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=live window passed
- - #4 | LIVE_ONLY_WAIT_TRIGGER | Vasco DA Gama vs Atletico-MG | market=BTTS_YES_REVIEW | stake=NO_STAKE_PRELOCK | lineup=WAIT_PRELOCK | min=633.42 | availability=AVAILABILITY_REPORTED_ADVISORY | next=wait for live trigger | note=prematch serious stake blocked
- - READY_LOW_STAKE_REVIEW still requires manual price and live/prelock confirmation.
- - WARN means review; BROKEN means a workflow/input needs fixing.
- - live_trigger_counts: TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- - live_trigger_validator | status=OK | severity=WARN | action=REVIEW_LIVE_WINDOW_MISSED_OR_FINISHED | detail=windows=TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1; triggers=TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- - memory_decision_counts: CALIBRATION_STABLE=4; MIXED_CALIBRATION_REVIEW=1; PATCH_CANDIDATE_REVIEW=1
- - prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=CANCELLED_NO_BET=11; STAT_WATCH_ONLY=5; LIVE_ONLY_WAIT_TRIGGER=4; NO_BET_OR_WATCH=4
- - recheck_decision_counts: CANCELLED_NO_BET=11; STAT_WATCH_ONLY=5; LIVE_ONLY_WAIT_TRIGGER=4; NO_BET_OR_WATCH=4
- - total_goals | days=4 | rows=26 | hit_rate=0.347 | bias=OVER_ESTIMATE | decision=PATCH_CANDIDATE_REVIEW | patch=YES_REVIEW_ONLY | next=Review lowering total_goals projection/range for matching profiles; do not auto-apply.
- - window_counts: TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1

## Health Snapshot
```
# vSIGMA Automation Health Monitor - 2026-05-31

## Summary
- system_status: ATTENTION
- components_checked: 11
- severity_counts: WARN=3; OK=4; INFO=4
- status_counts: OK=7; CONFIG_EXPECTED=4
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_execution_board | status=OK | severity=WARN | action=REVIEW_BOARD | detail=rows=24; decisions=NO_BET=10; STAT_WATCH_ONLY=5; NO_BET_OR_WATCH=5; LIVE_ONLY=4
- prelock_live_recheck | status=OK | severity=WARN | action=REVIEW_PRELOCK_LIVE | detail=decisions=CANCELLED_NO_BET=11; STAT_WATCH_ONLY=5; LIVE_ONLY_WAIT_TRIGGER=4; NO_BET_OR_WATCH=4
- live_trigger_validator | status=OK | severity=WARN | action=REVIEW_LIVE_WINDOW_MISSED_OR_FINISHED | detail=windows=TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1; triggers=TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- postmatch_results_refresh | status=OK | severity=OK | action=NO | detail=NS=4
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
# vSIGMA Live Trigger Validator - 2026-05-31

## Summary
- rows_validated: 4
- window_counts: TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- live_trigger_counts: TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- auto_apply: NO
- production_change: NO

## Rows
- #1 | window=TOO_EARLY | decision=TOO_EARLY | Cordoba vs Huesca | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=633.49 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window
- #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=333.43 | score=3-1 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | window=TOO_LATE | decision=TOO_LATE | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | status=2H | min=56.0 | mtko=483.51 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=live window passed
- #4 | window=TOO_EARLY | decision=TOO_EARLY | Vasco DA Gama vs Atletico-MG | market=BTTS_YES_REVIEW | status=NS | min=0 | mtko=633.42 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.

```

## Guardrails
- This issue is an alert only.
- Manual review is required before any action.
