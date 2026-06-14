# vSIGMA Daily Operator Brief - 2026-06-14

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | BROKEN | First-read operator priority |
| Risk | HIGH | Operational risk after sanity + health gate |
| Alert | CRITICAL_STOP / CRITICAL | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=0; no_bet=0 | Candidate distribution |
| Reason | system fault blocks market usage | Why this action level was selected |
| Final | SYSTEM_FIX_REQUIRED | sanity=PASS; broken-state routing is explicit |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | CRITICAL_STOP | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | CRITICAL | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | sanity failure or broken system state blocks operator usage | Why this route was selected |
| Drift | MATERIAL_CHANGE | Historical drift status |
| DriftNotify | true | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-06-10; action=UNKNOWN; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | data/processed/governance/vsigma_operator_brief.csv |
| Current | date=2026-06-14; action=BROKEN; risk=HIGH; final=SYSTEM_FIX_REQUIRED; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: UNKNOWN -> BROKEN; final_decision: NO_OPERATOR_ACTION -> SYSTEM_FIX_REQUIRED; risk_label: NONE -> HIGH |
| Changed | action_level,final_decision,risk_label | Tracked fields: action/final/risk/active |
| Notify | true | true only on material operator drift |

## Executive Summary
- action_level: BROKEN
- compact_final_decision: SYSTEM_FIX_REQUIRED
- risk_label: HIGH
- alert_route: CRITICAL_STOP
- alert_materiality: CRITICAL
- alert_reason: sanity failure or broken system state blocks operator usage
- drift_status: MATERIAL_CHANGE
- drift_notify_required: true
- drift_changed_fields: action_level,final_decision,risk_label
- sanity_check: PASS | broken-state routing is explicit
- operator_status: BROKEN
- primary_next_action: Fix missing/broken workflow input before using any market signal.
- health_status: BROKEN
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 0
- no_bet: 0
- board_decisions: UNKNOWN
- recheck_decisions: UNKNOWN
- live_triggers: none
- alert_notify_required: true
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=BROKEN
- RISK_LABEL=HIGH
- FINAL_DECISION=SYSTEM_FIX_REQUIRED
- ALERT_ROUTE=CRITICAL_STOP
- ALERT_MATERIALITY=CRITICAL
- ALERT_REASON=sanity failure or broken system state blocks operator usage
- DRIFT_STATUS=MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=true
- SANITY_CHECK=PASS
- SANITY_DETAIL=broken-state routing is explicit
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-14/vsigma_operator_brief.md -Encoding UTF8

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
- data/processed/today/2026-06-14/vsigma_daily_execution_board.md
- data/processed/today/2026-06-14/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-14/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-14/vsigma_automation_health.md
- data/processed/today/2026-06-14/vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.
- Historical drift notifies only on material operator changes: action level, final decision, risk, or active candidates.
- Alert routing is diagnostic only; this script writes the route but does not send comments or external notifications.

## Calibration / Shadow Governance
- calibration_shadow_status: UNAVAILABLE
- shadow_active_candidates: 0
- shadow_high_priority: 0
- shadow_metrics: none
- shadow_decisions: none
- promotion_readiness: UNAVAILABLE
- promotion_candidates: 0
- promotion_decisions: none
- learning_sanity_status: WARN
- learning_sanity_counts: EMPTY_NO_FALLBACK=7
- learning_sanity_severity: WARN=7
- calibration_auto_apply: NO
- production_change: NO

### Calibration Sources
- shadow_queue: data/processed/today/2026-06-14/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-06-14/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-06-14/vsigma_learning_chain_output_sanity.csv
