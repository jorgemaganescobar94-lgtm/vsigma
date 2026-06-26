# vSIGMA Daily Operator Brief - 2026-06-26

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | NONE | First-read operator priority |
| Risk | NONE | Operational risk after sanity + health gate |
| Alert | LOCAL_ONLY / LOW | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=0; no_bet=0 | Candidate distribution |
| Reason | no active/live/watch action; no_bet=0 | Why this action level was selected |
| Final | NO_OPERATOR_ACTION | sanity=PASS; no active/live/watch action; no_bet=0; closed=0 |

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
| Previous | date=2026-06-25; action=UNKNOWN; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | data/processed/governance/vsigma_operator_brief.csv |
| Current | date=2026-06-26; action=NONE; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | current_build |
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
- sanity_check: PASS | no active/live/watch action; no_bet=0; closed=0
- operator_status: REVIEW
- primary_next_action: Open health/board/recheck summaries; no automatic action.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 0
- no_bet: 0
- board_decisions: none
- recheck_decisions: UNKNOWN
- live_triggers: none
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
- SANITY_DETAIL=no active/live/watch action; no_bet=0; closed=0
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-26/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- none

## No Bet
- none

## Live Trigger Status
- no live trigger report or no live candidates

## Learning / Calibration
- no calibration signal

## Key Files
- data/processed/today/2026-06-26/vsigma_daily_execution_board.md
- data/processed/today/2026-06-26/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-26/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-26/vsigma_automation_health.md
- data/processed/today/2026-06-26/vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.
- Historical drift notifies only on material operator changes: action level, final decision, risk, or active candidates.
- Alert routing is diagnostic only; this script writes the route but does not send comments or external notifications.
