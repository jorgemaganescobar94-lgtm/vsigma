# vSIGMA Daily Operator Brief - 2026-06-20

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | LIVE | First-read operator priority |
| Risk | MEDIUM | Operational risk after sanity + health gate |
| Alert | GITHUB_ISSUE_COMMENT / MEDIUM | Routing decision for operator notifications |
| Counts | active=0; live=1; closed=0; watch=0; no_bet=9 | Candidate distribution |
| Reason | 1 candidate(s) waiting for live validation window | Why this action level was selected |
| Final | WAIT_LIVE_WINDOW | sanity=PASS; waiting_live_window=1; manual live validator rerun required |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | GITHUB_ISSUE_COMMENT | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | MEDIUM | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | live-window state changed materially | Why this route was selected |
| Drift | MATERIAL_CHANGE | Historical drift status |
| DriftNotify | true | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-06-20; action=WATCH; risk=LOW; final=WATCH_ONLY_NO_STAKE; active=0 | data/processed/today/2026-06-20/vsigma_operator_brief.csv |
| Current | date=2026-06-20; action=LIVE; risk=MEDIUM; final=WAIT_LIVE_WINDOW; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: WATCH -> LIVE; final_decision: WATCH_ONLY_NO_STAKE -> WAIT_LIVE_WINDOW; risk_label: LOW -> MEDIUM |
| Changed | action_level,final_decision,risk_label | Tracked fields: action/final/risk/active |
| Notify | true | true only on material operator drift |

## Executive Summary
- action_level: LIVE
- compact_final_decision: WAIT_LIVE_WINDOW
- risk_label: MEDIUM
- alert_route: GITHUB_ISSUE_COMMENT
- alert_materiality: MEDIUM
- alert_reason: live-window state changed materially
- drift_status: MATERIAL_CHANGE
- drift_notify_required: true
- drift_changed_fields: action_level,final_decision,risk_label
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
- live_triggers: none
- alert_notify_required: false
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=LIVE
- RISK_LABEL=MEDIUM
- FINAL_DECISION=WAIT_LIVE_WINDOW
- ALERT_ROUTE=GITHUB_ISSUE_COMMENT
- ALERT_MATERIALITY=MEDIUM
- ALERT_REASON=live-window state changed materially
- DRIFT_STATUS=MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=true
- SANITY_CHECK=PASS
- SANITY_DETAIL=waiting_live_window=1; manual live validator rerun required
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-06-20/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- #1 | LIVE_ONLY_WAIT_TRIGGER | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | window=UNKNOWN | live=UNKNOWN | reason=prematch serious stake blocked

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
