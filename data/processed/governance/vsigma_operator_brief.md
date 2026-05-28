# vSIGMA Daily Operator Brief - 2026-05-28

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | WATCH | First-read operator priority |
| Risk | LOW_ALERT | Operational risk after sanity + health gate |
| Alert | LOCAL_ONLY / LOW | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=8; no_bet=4 | Candidate distribution |
| Reason | 8 watch-only item(s); official stake remains blocked | Why this action level was selected |
| Final | WATCH_ONLY_NO_STAKE | sanity=PASS; watch_only=8; no official action; no active/live review |

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
| Previous | date=2026-05-28; action=UNKNOWN; risk=UNKNOWN; final=UNKNOWN; active=0 | data/processed/today/2026-05-28/vsigma_operator_brief.csv |
| Current | date=2026-05-28; action=WATCH; risk=LOW_ALERT; final=WATCH_ONLY_NO_STAKE; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: UNKNOWN -> WATCH; final_decision: UNKNOWN -> WATCH_ONLY_NO_STAKE; risk_label: UNKNOWN -> LOW_ALERT |
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
- sanity_check: PASS | watch_only=8; no official action; no active/live review
- operator_status: OK
- primary_next_action: No operator action required.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 8
- no_bet: 4
- board_decisions: NO_BET_OR_WATCH=7; NO_BET=4; LIVE_ONLY=1
- recheck_decisions: none
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
- SANITY_DETAIL=watch_only=8; no official action; no active/live review
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-05-28/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- #1 | LIVE_ONLY | Palmeiras vs Junior | market=CORNERS_OVER_8_5_REVIEW | alt=CORNERS_OVER_9_5_AGGRESSIVE | bucket=LIVE_CANDIDATE | conf=MEDIUM | score=5 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #2 | NO_BET_OR_WATCH | River Plate vs Blooming | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=26 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #3 | NO_BET_OR_WATCH | RB Bragantino vs Carabobo FC | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=23 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #4 | NO_BET_OR_WATCH | Corinthians vs Platense | market=BTTS_YES_REVIEW | alt=OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=6 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #5 | NO_BET_OR_WATCH | Cerro Porteno vs Sporting Cristal | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=MEDIUM | score=2 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #6 | NO_BET_OR_WATCH | Fluminense vs Deportivo La Guaira | market=BTTS_YES_REVIEW | alt=OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=-2 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #7 | NO_BET_OR_WATCH | Penarol vs Santa Fe | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | bucket=WEAK_WATCH | conf=MEDIUM | score=-10 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #8 | NO_BET_OR_WATCH | Casa Pia vs Torreense | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=LOW | score=-34 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; low forecast confidence; bad or incomplete lineups

## No Bet
- #9 | NO_BET | Bolívar vs Independ. Rivadavia | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=MEDIUM | score=-24 | cancel=default no bet; bad or incomplete lineups
- #10 | NO_BET | El Geish vs Wadi Degla | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #11 | NO_BET | Ismaily SC vs Pharco | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #12 | NO_BET | Petrojet vs El Gouna FC | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- no live trigger report or no live candidates

## Learning / Calibration
- calibration_status_counts: CALIBRATION_OK=3; MODEL_OVER_ESTIMATING=3
- total_cards | rows=6 | hit_rate=0.833 | avg_error=1.50 | bias=OVER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=8 | hit_rate=0.625 | avg_error=2.62 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_fouls | rows=9 | hit_rate=0.667 | avg_error=7.78 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_goals | rows=9 | hit_rate=0.556 | avg_error=0.86 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=9 | hit_rate=0.778 | avg_error=4.56 | bias=OVER_ESTIMATE | status=CALIBRATION_OK
- total_sot | rows=8 | hit_rate=1.000 | avg_error=1.50 | bias=BALANCED_OR_ON_RANGE | status=CALIBRATION_OK

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
