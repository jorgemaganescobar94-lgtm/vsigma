# vSIGMA Daily Operator Brief - 2026-06-04

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | REVIEW_NOW | First-read operator priority |
| Risk | HIGH | Operational risk after sanity + health gate |
| Alert | GITHUB_ISSUE_COMMENT / HIGH | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=0; no_bet=1 | Candidate distribution |
| Reason | 0 active manual-review candidate(s); no automatic execution | Why this action level was selected |
| Final | MANUAL_REVIEW_REQUIRED | sanity=PASS; active_review=0; manual review required; no auto execution |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | GITHUB_ISSUE_COMMENT | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | HIGH | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | manual review required now; no automatic execution | Why this route was selected |
| Drift | MATERIAL_CHANGE | Historical drift status |
| DriftNotify | true | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-06-04; action=BROKEN; risk=HIGH; final=SYSTEM_FIX_REQUIRED; active=0 | data\processed\today\2026-06-04\vsigma_operator_brief.csv |
| Current | date=2026-06-04; action=REVIEW_NOW; risk=HIGH; final=MANUAL_REVIEW_REQUIRED; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: BROKEN -> REVIEW_NOW; final_decision: SYSTEM_FIX_REQUIRED -> MANUAL_REVIEW_REQUIRED |
| Changed | action_level,final_decision | Tracked fields: action/final/risk/active |
| Notify | true | true only on material operator drift |

## Executive Summary
- action_level: REVIEW_NOW
- compact_final_decision: MANUAL_REVIEW_REQUIRED
- risk_label: HIGH
- alert_route: GITHUB_ISSUE_COMMENT
- alert_materiality: HIGH
- alert_reason: manual review required now; no automatic execution
- drift_status: MATERIAL_CHANGE
- drift_notify_required: true
- drift_changed_fields: action_level,final_decision
- sanity_check: PASS | active_review=0; manual review required; no auto execution
- operator_status: REVIEW
- primary_next_action: Open health/board/recheck summaries; no automatic action.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 0
- no_bet: 1
- board_decisions: NO_BET=0
- recheck_decisions: none
- live_triggers: none
- alert_notify_required: true
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=REVIEW_NOW
- RISK_LABEL=HIGH
- FINAL_DECISION=MANUAL_REVIEW_REQUIRED
- ALERT_ROUTE=GITHUB_ISSUE_COMMENT
- ALERT_MATERIALITY=HIGH
- ALERT_REASON=manual review required now; no automatic execution
- DRIFT_STATUS=MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=true
- SANITY_CHECK=PASS
- SANITY_DETAIL=active_review=0; manual review required; no auto execution
- WINDOWS_READ=UTF8 | Get-Content data\processed\today\2026-06-04\vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- none

## No Bet
- #0 | NO_BET | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | market=NO_MARKET | bucket=EMPTY_BY_PROMOTION_GATE | score=0 | cancel=default no bet; no promoted raw candidates

## Live Trigger Status
- no live trigger report or no live candidates

## Learning / Calibration
- no calibration signal

## Key Files
- data\processed\today\2026-06-04\vsigma_daily_execution_board.md
- data\processed\today\2026-06-04\vsigma_prelock_live_recheck.md
- data\processed\today\2026-06-04\vsigma_live_trigger_validator.md
- data\processed\today\2026-06-04\vsigma_automation_health.md
- data\processed\today\2026-06-04\vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.
- Historical drift notifies only on material operator changes: action level, final decision, risk, or active candidates.
- Alert routing is diagnostic only; this script writes the route but does not send comments or external notifications.
