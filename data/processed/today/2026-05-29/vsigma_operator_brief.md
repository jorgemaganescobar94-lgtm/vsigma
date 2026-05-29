# vSIGMA Daily Operator Brief - 2026-05-29

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | WATCH | First-read operator priority |
| Risk | LOW_ALERT | Operational risk after sanity + health gate |
| Alert | LOCAL_ONLY / LOW | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=1; no_bet=1 | Candidate distribution |
| Reason | 1 watch-only item(s); official stake remains blocked | Why this action level was selected |
| Final | WATCH_ONLY_NO_STAKE | sanity=PASS; watch_only=1; no official action; no active/live review |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | LOCAL_ONLY | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | LOW | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | watch-only state changed materially; no stake permission | Why this route was selected |
| Drift | MATERIAL_CHANGE | Historical drift status |
| DriftNotify | true | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-05-29; action=BROKEN; risk=HIGH; final=SYSTEM_FIX_REQUIRED; active=0 | data/processed/today/2026-05-29/vsigma_operator_brief.csv |
| Current | date=2026-05-29; action=WATCH; risk=LOW_ALERT; final=WATCH_ONLY_NO_STAKE; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: BROKEN -> WATCH; final_decision: SYSTEM_FIX_REQUIRED -> WATCH_ONLY_NO_STAKE; risk_label: HIGH -> LOW_ALERT |
| Changed | action_level,final_decision,risk_label | Tracked fields: action/final/risk/active |
| Notify | true | true only on material operator drift |

## Executive Summary
- action_level: WATCH
- compact_final_decision: WATCH_ONLY_NO_STAKE
- risk_label: LOW_ALERT
- alert_route: LOCAL_ONLY
- alert_materiality: LOW
- alert_reason: watch-only state changed materially; no stake permission
- drift_status: MATERIAL_CHANGE
- drift_notify_required: true
- drift_changed_fields: action_level,final_decision,risk_label
- sanity_check: PASS | watch_only=1; no official action; no active/live review
- operator_status: OK
- primary_next_action: No operator action required.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 1
- no_bet: 1
- board_decisions: NO_BET_OR_WATCH=1; NO_BET=1
- recheck_decisions: NO_BET_OR_WATCH=1; CANCELLED_NO_BET=1
- live_triggers: none
- alert_notify_required: true
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=WATCH
- RISK_LABEL=LOW_ALERT
- FINAL_DECISION=WATCH_ONLY_NO_STAKE
- ALERT_ROUTE=LOCAL_ONLY
- ALERT_MATERIALITY=LOW
- ALERT_REASON=watch-only state changed materially; no stake permission
- DRIFT_STATUS=MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=true
- SANITY_CHECK=PASS
- SANITY_DETAIL=watch_only=1; no official action; no active/live review
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-05-29/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- #1 | NO_BET_OR_WATCH | Nice vs Saint Etienne | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=MEDIUM | score=-12 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; bad or incomplete lineups; new availability downgrade

## No Bet
- #2 | NO_BET | Cde Juventud Italiana vs Tecnico Universitario | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- no live trigger report or no live candidates

## Learning / Calibration
- calibration_status_counts: CALIBRATION_OK=2; MODEL_UNDER_ESTIMATING=2; MODEL_OVER_ESTIMATING=2
- total_cards | rows=5 | hit_rate=0.800 | avg_error=1.60 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=6 | hit_rate=0.500 | avg_error=2.83 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING
- total_fouls | rows=6 | hit_rate=0.500 | avg_error=5.33 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_goals | rows=7 | hit_rate=0.429 | avg_error=1.22 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=6 | hit_rate=0.833 | avg_error=4.83 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_sot | rows=6 | hit_rate=0.500 | avg_error=2.67 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING

## Key Files
- data/processed/today/2026-05-29/vsigma_daily_execution_board.md
- data/processed/today/2026-05-29/vsigma_prelock_live_recheck.md
- data/processed/today/2026-05-29/vsigma_live_trigger_validator.md
- data/processed/today/2026-05-29/vsigma_automation_health.md
- data/processed/today/2026-05-29/vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.
- Historical drift notifies only on material operator changes: action level, final decision, risk, or active candidates.
- Alert routing is diagnostic only; this script writes the route but does not send comments or external notifications.

## Calibration / Shadow Governance
- calibration_shadow_status: ACTIVE
- shadow_active_candidates: 4
- shadow_high_priority: 4
- shadow_metrics: total_corners,total_fouls,total_goals,total_sot
- shadow_decisions: PROMOTE_TO_SHADOW_TEST=4; NO_PATCH_STABLE=2
- promotion_readiness: KEEP_SHADOW_TEST
- promotion_candidates: 0
- promotion_decisions: KEEP_SHADOW_TEST=4; NO_PROMOTION_STABLE=2
- learning_sanity_status: PASS
- learning_sanity_counts: PASS=7
- learning_sanity_severity: OK=7
- calibration_auto_apply: NO
- production_change: NO

### Calibration Sources
- shadow_queue: data/processed/today/2026-05-29/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-05-29/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-05-29/vsigma_learning_chain_output_sanity.csv
