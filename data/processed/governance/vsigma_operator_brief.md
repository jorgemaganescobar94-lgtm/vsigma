# vSIGMA Daily Operator Brief - 2026-06-21

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | NONE | First-read operator priority |
| Risk | NONE | Operational risk after sanity + health gate |
| Alert | LOCAL_ONLY / LOW | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=0; no_bet=11 | Candidate distribution |
| Reason | no active/live/watch action; no_bet=11 | Why this action level was selected |
| Final | NO_OPERATOR_ACTION | sanity=PASS; no active/live/watch action; no_bet=11; closed=0 |

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
| Previous | date=2026-06-21; action=UNKNOWN; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | data/processed/today/2026-06-21/vsigma_operator_brief.csv |
| Current | date=2026-06-21; action=NONE; risk=NONE; final=NO_OPERATOR_ACTION; active=0 | current_build |
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
- sanity_check: PASS | no active/live/watch action; no_bet=11; closed=0
- operator_status: REVIEW
- primary_next_action: Open health/board/recheck summaries; no automatic action.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 0
- no_bet: 11
- board_decisions: NO_BET=11
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
- SANITY_DETAIL=no active/live/watch action; no_bet=11; closed=0
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-21/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- none

## No Bet
- #1 | NO_BET | Avai vs Cuiaba | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #2 | NO_BET | CRB vs Fortaleza EC | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #3 | NO_BET | Goias vs Operario-PR | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #4 | NO_BET | São Bernardo vs Juventude | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #5 | NO_BET | Džiugas Telšiai vs Suduva Marijampole | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #6 | NO_BET | Barra vs Amazonas | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #7 | NO_BET | Brusque vs Floresta | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #8 | NO_BET | Caxias vs Maringá | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #9 | NO_BET | Ferroviária vs Inter De Limeira | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #10 | NO_BET | Ituano vs Figueirense | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #11 | NO_BET | Maranhão vs Paysandu | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- no live trigger report or no live candidates

## Learning / Calibration
- no calibration signal

## Key Files
- data/processed/today/2026-06-21/vsigma_daily_execution_board.md
- data/processed/today/2026-06-21/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-21/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-21/vsigma_automation_health.md
- data/processed/today/2026-06-21/vsigma_issue_alert_status.md

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
- learning_sanity_counts: EMPTY_NO_FALLBACK=6; PASS=1
- learning_sanity_severity: WARN=6; OK=1
- calibration_auto_apply: NO
- production_change: NO

### Calibration Sources
- shadow_queue: data/processed/today/2026-06-21/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-06-21/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-06-21/vsigma_learning_chain_output_sanity.csv
