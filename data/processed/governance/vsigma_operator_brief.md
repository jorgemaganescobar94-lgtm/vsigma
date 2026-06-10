# vSIGMA Daily Operator Brief - 2026-06-10

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | NONE | First-read operator priority |
| Risk | NONE | Operational risk after sanity + health gate |
| Alert | LOCAL_ONLY / LOW | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=1; watch=0; no_bet=1 | Candidate distribution |
| Reason | no active/live/watch action; no_bet=1 | Why this action level was selected |
| Final | NO_OPERATOR_ACTION | sanity=PASS; no active/live/watch action; no_bet=1; closed=1 |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | LOCAL_ONLY | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | LOW | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | non-action state changed but no operator action is required | Why this route was selected |
| Drift | MATERIAL_CHANGE | Historical drift status |
| DriftNotify | true | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-06-10; action=UNKNOWN; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | data/processed/today/2026-06-10/vsigma_operator_brief.csv |
| Current | date=2026-06-10; action=NONE; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: UNKNOWN -> NONE |
| Changed | action_level | Tracked fields: action/final/risk/active |
| Notify | true | true only on material operator drift |

## Executive Summary
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- alert_route: LOCAL_ONLY
- alert_materiality: LOW
- alert_reason: non-action state changed but no operator action is required
- drift_status: MATERIAL_CHANGE
- drift_notify_required: true
- drift_changed_fields: action_level
- sanity_check: PASS | no active/live/watch action; no_bet=1; closed=1
- operator_status: CLOSED_OR_WINDOW_MISSED
- primary_next_action: No active candidate; previous signals are finished or outside useful window.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 1
- watch_only: 0
- no_bet: 1
- board_decisions: LIVE_ONLY=1; NO_BET=1
- recheck_decisions: LIVE_ONLY_WAIT_TRIGGER=1; CANCELLED_NO_BET=1
- live_triggers: MATCH_FINISHED=1
- alert_notify_required: true
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=NONE
- RISK_LABEL=NONE
- FINAL_DECISION=NO_OPERATOR_ACTION
- ALERT_ROUTE=LOCAL_ONLY
- ALERT_MATERIALITY=LOW
- ALERT_REASON=non-action state changed but no operator action is required
- DRIFT_STATUS=MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=true
- SANITY_CHECK=PASS
- SANITY_DETAIL=no active/live/watch action; no_bet=1; closed=1
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-10/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- #1 | LIVE_ONLY_WAIT_TRIGGER | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | window=MATCH_FINISHED | live=MATCH_FINISHED | match=FT | elapsed=90.0 | score=1-1 | reason=match already final

## Watch Only
- none

## No Bet
- #2 | NO_BET | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- window_counts: MATCH_FINISHED=1
- live_trigger_counts: MATCH_FINISHED=1
- #1 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=474.21 | score=1-1 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final

## Learning / Calibration
- no calibration signal

## Key Files
- data/processed/today/2026-06-10/vsigma_daily_execution_board.md
- data/processed/today/2026-06-10/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-10/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-10/vsigma_automation_health.md
- data/processed/today/2026-06-10/vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.
- Historical drift notifies only on material operator changes: action level, final decision, risk, or active candidates.
- Alert routing is diagnostic only; this script writes the route but does not send comments or external notifications.
