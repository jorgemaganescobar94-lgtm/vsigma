# vSIGMA Daily Operator Brief - 2026-06-20

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | LIVE | First-read operator priority |
| Risk | MEDIUM | Operational risk after sanity + health gate |
| Alert | LOCAL_ONLY / LOW | Routing decision for operator notifications |
| Counts | active=0; live=1; closed=0; watch=0; no_bet=9 | Candidate distribution |
| Reason | 1 candidate(s) waiting for live validation window | Why this action level was selected |
| Final | WAIT_LIVE_WINDOW | sanity=PASS; waiting_live_window=1; manual live validator rerun required |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | LOCAL_ONLY | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | LOW | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | live-window watch exists but no material drift | Why this route was selected |
| Drift | NO_MATERIAL_CHANGE | Historical drift status |
| DriftNotify | false | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-06-20; action=LIVE; risk=MEDIUM; final=WAIT_LIVE_WINDOW; active=0 | data/processed/today/2026-06-20/vsigma_operator_brief.csv |
| Current | date=2026-06-20; action=LIVE; risk=MEDIUM; final=WAIT_LIVE_WINDOW; active=0 | current_build |
| Drift | NO_MATERIAL_CHANGE | tracked operator fields unchanged |
| Changed | none | Tracked fields: action/final/risk/active |
| Notify | false | true only on material operator drift |

## Executive Summary
- action_level: LIVE
- compact_final_decision: WAIT_LIVE_WINDOW
- risk_label: MEDIUM
- alert_route: LOCAL_ONLY
- alert_materiality: LOW
- alert_reason: live-window watch exists but no material drift
- drift_status: NO_MATERIAL_CHANGE
- drift_notify_required: false
- drift_changed_fields: none
- sanity_check: PASS | waiting_live_window=1; manual live validator rerun required
- operator_status: WAIT_LIVE_WINDOW
- primary_next_action: Wait for useful live window and rerun live trigger validator.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 1
- closed_or_missed: 0
- watch_only: 0
- no_bet: 9
- board_decisions: NO_BET=9; LIVE_ONLY=1
- recheck_decisions: CANCELLED_NO_BET=9; LIVE_ONLY_WAIT_TRIGGER=1
- live_triggers: TOO_EARLY=1
- alert_notify_required: true
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=LIVE
- RISK_LABEL=MEDIUM
- FINAL_DECISION=WAIT_LIVE_WINDOW
- ALERT_ROUTE=LOCAL_ONLY
- ALERT_MATERIALITY=LOW
- ALERT_REASON=live-window watch exists but no material drift
- DRIFT_STATUS=NO_MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=false
- SANITY_CHECK=PASS
- SANITY_DETAIL=waiting_live_window=1; manual live validator rerun required
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-20/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- #1 | LIVE_ONLY_WAIT_TRIGGER | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | window=TOO_EARLY | live=TOO_EARLY | match=NS | elapsed=0 | score=0-0 | reason=outside useful live window

## Closed / Window Missed
- none

## Watch Only
- none

## No Bet
- #2 | NO_BET | Ceara vs Botafogo SP | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #3 | NO_BET | Londrina vs Athletic Club | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #4 | NO_BET | Vila Nova vs Nautico Recife | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #5 | NO_BET | Banga vs FK Zalgiris Vilnius | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #6 | NO_BET | Panevėžys vs Šiauliai | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #7 | NO_BET | TransINVEST Vilnius vs Kauno Žalgiris | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #8 | NO_BET | Anápolis vs AO Itabaiana | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #9 | NO_BET | Botafogo PB vs Volta Redonda | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #10 | NO_BET | Santa Cruz vs Ypiranga-RS | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- window_counts: TOO_EARLY=1
- live_trigger_counts: TOO_EARLY=1
- #1 | window=TOO_EARLY | decision=TOO_EARLY | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1165.65 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Learning / Calibration
- no calibration signal

## Key Files
- data/processed/today/2026-06-20/vsigma_daily_execution_board.md
- data/processed/today/2026-06-20/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-20/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-20/vsigma_automation_health.md
- data/processed/today/2026-06-20/vsigma_issue_alert_status.md

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
- shadow_queue: data/processed/today/2026-06-20/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-06-20/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-06-20/vsigma_learning_chain_output_sanity.csv
