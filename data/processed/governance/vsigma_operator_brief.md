# vSIGMA Daily Operator Brief - 2026-05-28

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | LIVE | First-read operator priority |
| Risk | MEDIUM | Operational risk after sanity + health gate |
| Alert | GITHUB_ISSUE_COMMENT / MEDIUM | Routing decision for operator notifications |
| Counts | active=0; live=1; closed=0; watch=2; no_bet=0 | Candidate distribution |
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
| Previous | date=2026-05-28; action=WATCH; risk=LOW_ALERT; final=WATCH_ONLY_NO_STAKE; active=0 | data/processed/today/2026-05-28/vsigma_operator_brief.csv |
| Current | date=2026-05-28; action=LIVE; risk=MEDIUM; final=WAIT_LIVE_WINDOW; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: WATCH -> LIVE; final_decision: WATCH_ONLY_NO_STAKE -> WAIT_LIVE_WINDOW; risk_label: LOW_ALERT -> MEDIUM |
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
- watch_only: 2
- no_bet: 0
- board_decisions: NO_BET_OR_WATCH=2; LIVE_ONLY=1
- recheck_decisions: NO_BET_OR_WATCH=2; LIVE_ONLY_WAIT_TRIGGER=1
- live_triggers: WAIT_MORE_MINUTES=1
- alert_notify_required: true
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
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-05-28/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- #1 | LIVE_ONLY_WAIT_TRIGGER | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | window=IN_LIVE_WINDOW | live=WAIT_MORE_MINUTES | match=1H | elapsed=14.0 | score=1-0 | reason=partial signal only

## Closed / Window Missed
- none

## Watch Only
- #2 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=MEDIUM | score=2 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #3 | NO_BET_OR_WATCH | Casa Pia vs Torreense | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=LOW | score=-22 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; low forecast confidence

## No Bet
- none

## Live Trigger Status
- #1 | window=IN_LIVE_WINDOW | decision=WAIT_MORE_MINUTES | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | status=1H | min=14.0 | mtko=196.53 | score=1-0 | shots=5.0 | SoT=2.0 | corners=0 | signal=3 | reason=partial signal only

## Learning / Calibration
- no calibration signal

## Key Files
- data/processed/today/2026-05-28/vsigma_daily_execution_board.md
- data/processed/today/2026-05-28/vsigma_prelock_live_recheck.md
- data/processed/today/2026-05-28/vsigma_live_trigger_validator.md
- data/processed/today/2026-05-28/vsigma_automation_health.md
- data/processed/today/2026-05-28/vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
- Use PowerShell -Encoding UTF8 when reading local Markdown files on Windows.
- Historical drift notifies only on material operator changes: action level, final decision, risk, or active candidates.
- Alert routing is diagnostic only; this script writes the route but does not send comments or external notifications.
