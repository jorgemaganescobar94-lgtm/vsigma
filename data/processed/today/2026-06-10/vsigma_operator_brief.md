# vSIGMA Daily Operator Brief - 2026-06-10

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | WATCH | First-read operator priority |
| Risk | LOW_ALERT | Operational risk after sanity + health gate |
| Alert | NO_ALERT / NONE | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=1; no_bet=1 | Candidate distribution |
| Reason | 1 watch-only item(s); official stake remains blocked | Why this action level was selected |
| Final | WATCH_ONLY_NO_STAKE | sanity=PASS; watch_only=1; no official action; no active/live review |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | NO_ALERT | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | NONE | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | watch-only state unchanged; no official action | Why this route was selected |
| Drift | NO_MATERIAL_CHANGE | Historical drift status |
| DriftNotify | false | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-06-10; action=WATCH; risk=LOW_ALERT; final=WATCH_ONLY_NO_STAKE; active=0 | data/processed/today/2026-06-10/vsigma_operator_brief.csv |
| Current | date=2026-06-10; action=WATCH; risk=LOW_ALERT; final=WATCH_ONLY_NO_STAKE; active=0 | current_build |
| Drift | NO_MATERIAL_CHANGE | tracked operator fields unchanged |
| Changed | none | Tracked fields: action/final/risk/active |
| Notify | false | true only on material operator drift |

## Executive Summary
- action_level: WATCH
- compact_final_decision: WATCH_ONLY_NO_STAKE
- risk_label: LOW_ALERT
- alert_route: NO_ALERT
- alert_materiality: NONE
- alert_reason: watch-only state unchanged; no official action
- drift_status: NO_MATERIAL_CHANGE
- drift_notify_required: false
- drift_changed_fields: none
- sanity_check: PASS | watch_only=1; no official action; no active/live review
- operator_status: OK
- primary_next_action: No operator action required.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 1
- no_bet: 1
- board_decisions: LIVE_ONLY=1; NO_BET=1
- recheck_decisions: none
- live_triggers: none
- alert_notify_required: true
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=WATCH
- RISK_LABEL=LOW_ALERT
- FINAL_DECISION=WATCH_ONLY_NO_STAKE
- ALERT_ROUTE=NO_ALERT
- ALERT_MATERIALITY=NONE
- ALERT_REASON=watch-only state unchanged; no official action
- DRIFT_STATUS=NO_MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=false
- SANITY_CHECK=PASS
- SANITY_DETAIL=watch_only=1; no official action; no active/live review
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-10/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- #1 | LIVE_ONLY | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=LIVE_CANDIDATE | conf=MEDIUM | score=17 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups

## No Bet
- #2 | NO_BET | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- no live trigger report or no live candidates

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

## Calibration / Shadow Governance
- calibration_shadow_status: STABLE_OR_NO_PATCH
- shadow_active_candidates: 0
- shadow_high_priority: 0
- shadow_metrics: none
- shadow_decisions: REJECT_LOW_SAMPLE=1
- promotion_readiness: NO_PROMOTION
- promotion_candidates: 0
- promotion_decisions: WAIT_MORE_SAMPLE=1
- learning_sanity_status: PASS
- learning_sanity_counts: PASS=7
- learning_sanity_severity: OK=7
- calibration_auto_apply: NO
- production_change: NO

### Calibration Sources
- shadow_queue: data/processed/today/2026-06-10/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-06-10/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-06-10/vsigma_learning_chain_output_sanity.csv
