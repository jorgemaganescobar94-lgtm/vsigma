# vSIGMA Daily Operator Brief - 2026-06-20

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | WATCH | First-read operator priority |
| Risk | LOW | Operational risk after sanity + health gate |
| Alert | NO_ALERT / NONE | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=1; no_bet=9 | Candidate distribution |
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
| Previous | date=2026-06-20; action=WATCH; risk=LOW; final=WATCH_ONLY_NO_STAKE; active=0 | data/processed/today/2026-06-20/vsigma_operator_brief.csv |
| Current | date=2026-06-20; action=WATCH; risk=LOW; final=WATCH_ONLY_NO_STAKE; active=0 | current_build |
| Drift | NO_MATERIAL_CHANGE | tracked operator fields unchanged |
| Changed | none | Tracked fields: action/final/risk/active |
| Notify | false | true only on material operator drift |

## Executive Summary
- action_level: WATCH
- compact_final_decision: WATCH_ONLY_NO_STAKE
- risk_label: LOW
- alert_route: NO_ALERT
- alert_materiality: NONE
- alert_reason: watch-only state unchanged; no official action
- drift_status: NO_MATERIAL_CHANGE
- drift_notify_required: false
- drift_changed_fields: none
- sanity_check: PASS | watch_only=1; no official action; no active/live review
- operator_status: REVIEW
- primary_next_action: Open health/board/recheck summaries; no automatic action.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 1
- no_bet: 9
- board_decisions: NO_BET=9; LIVE_ONLY=1
- recheck_decisions: UNKNOWN
- live_triggers: none
- alert_notify_required: false
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=WATCH
- RISK_LABEL=LOW
- FINAL_DECISION=WATCH_ONLY_NO_STAKE
- ALERT_ROUTE=NO_ALERT
- ALERT_MATERIALITY=NONE
- ALERT_REASON=watch-only state unchanged; no official action
- DRIFT_STATUS=NO_MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=false
- SANITY_CHECK=PASS
- SANITY_DETAIL=watch_only=1; no official action; no active/live review
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-20/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- #1 | LIVE_ONLY | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=LIVE_CANDIDATE | conf=MEDIUM | score=28 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups

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
- no live trigger report or no live candidates

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
