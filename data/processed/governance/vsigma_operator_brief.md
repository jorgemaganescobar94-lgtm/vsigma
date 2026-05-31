# vSIGMA Daily Operator Brief - 2026-05-31

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | LIVE | First-read operator priority |
| Risk | MEDIUM | Operational risk after sanity + health gate |
| Alert | GITHUB_ISSUE_COMMENT / MEDIUM | Routing decision for operator notifications |
| Counts | active=0; live=2; closed=2; watch=9; no_bet=11 | Candidate distribution |
| Reason | 2 candidate(s) waiting for live validation window | Why this action level was selected |
| Final | WAIT_LIVE_WINDOW | sanity=PASS; waiting_live_window=2; manual live validator rerun required |

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
| Previous | date=2026-05-31; action=BROKEN; risk=HIGH; final=SYSTEM_FIX_REQUIRED; active=0 | data/processed/today/2026-05-31/vsigma_operator_brief.csv |
| Current | date=2026-05-31; action=LIVE; risk=MEDIUM; final=WAIT_LIVE_WINDOW; active=0 | current_build |
| Drift | MATERIAL_CHANGE | action_level: BROKEN -> LIVE; final_decision: SYSTEM_FIX_REQUIRED -> WAIT_LIVE_WINDOW; risk_label: HIGH -> MEDIUM |
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
- sanity_check: PASS | waiting_live_window=2; manual live validator rerun required
- operator_status: WAIT_LIVE_WINDOW
- primary_next_action: Wait for useful live window and rerun live trigger validator.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 2
- closed_or_missed: 2
- watch_only: 9
- no_bet: 11
- board_decisions: NO_BET=10; STAT_WATCH_ONLY=5; NO_BET_OR_WATCH=5; LIVE_ONLY=4
- recheck_decisions: CANCELLED_NO_BET=11; STAT_WATCH_ONLY=5; LIVE_ONLY_WAIT_TRIGGER=4; NO_BET_OR_WATCH=4
- live_triggers: TOO_EARLY=2; MATCH_FINISHED=2
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
- SANITY_DETAIL=waiting_live_window=2; manual live validator rerun required
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-05-31/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- #1 | LIVE_ONLY_WAIT_TRIGGER | Cordoba vs Huesca | market=OVER_1_5_SUPPORTED | window=TOO_EARLY | live=TOO_EARLY | match=NS | elapsed=0 | score=0-0 | reason=outside useful live window
- #4 | LIVE_ONLY_WAIT_TRIGGER | Vasco DA Gama vs Atletico-MG | market=BTTS_YES_REVIEW | window=TOO_EARLY | live=TOO_EARLY | match=NS | elapsed=0 | score=0-0 | reason=outside useful live window

## Closed / Window Missed
- #2 | LIVE_ONLY_WAIT_TRIGGER | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | window=MATCH_FINISHED | live=MATCH_FINISHED | match=FT | elapsed=90.0 | score=3-1 | reason=match already final
- #3 | LIVE_ONLY_WAIT_TRIGGER | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | window=MATCH_FINISHED | live=MATCH_FINISHED | match=FT | elapsed=90.0 | score=1-0 | reason=match already final

## Watch Only
- #5 | STAT_WATCH_ONLY | Leganes vs Mirandes | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WATCHLIST | conf=MEDIUM | score=53 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #6 | STAT_WATCH_ONLY | Zaragoza vs Malaga | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WATCHLIST | conf=MEDIUM | score=53 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #7 | STAT_WATCH_ONLY | Vasteras SK FK vs IFK Goteborg | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WATCHLIST | conf=MEDIUM | score=37 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups; new availability downgrade
- #8 | STAT_WATCH_ONLY | Racing Santander vs Cadiz | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WATCHLIST | conf=MEDIUM | score=32 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #9 | STAT_WATCH_ONLY | Castellón vs Eibar | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WATCHLIST | conf=MEDIUM | score=31 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #10 | NO_BET_OR_WATCH | BK Hacken vs Hammarby FF | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=21 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups; new availability…
- #11 | NO_BET_OR_WATCH | Degerfors IF vs IF Brommapojkarna | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=18 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #13 | NO_BET_OR_WATCH | Gent vs Genk | market=CORNERS_OVER_8_5_REVIEW | alt=CORNERS_OVER_9_5_AGGRESSIVE | bucket=WEAK_WATCH | conf=MEDIUM | score=1 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #14 | NO_BET_OR_WATCH | Palmeiras vs Chapecoense-sc | market=CORNERS_OVER_8_5_REVIEW | alt=CORNERS_OVER_9_5_AGGRESSIVE | bucket=WEAK_WATCH | conf=LOW | score=-26 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; low forecast confidence; bad or incomplete lineups; new availability downgrade

## No Bet
- #12 | NO_BET | Burgos vs FC Andorra | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=BLOCKED | conf=MEDIUM | score=18 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #15 | NO_BET | Deportivo La Coruna vs Las Palmas | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=MEDIUM | score=-10 | cancel=default no bet; bad or incomplete lineups
- #16 | NO_BET | Ceara vs Operario-PR | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #17 | NO_BET | Londrina vs Vila Nova | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #18 | NO_BET | São Bernardo vs Novorizontino | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #19 | NO_BET | AC Oulu vs FF Jaro | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #20 | NO_BET | Kauno Žalgiris vs FK Zalgiris Vilnius | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #21 | NO_BET | Anápolis vs Maranhão | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #22 | NO_BET | Guarani Campinas vs Amazonas | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #23 | NO_BET | Inter De Limeira vs Ypiranga-RS | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #24 | NO_BET | Santa Cruz vs Ferroviária | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- window_counts: TOO_EARLY=2; MATCH_FINISHED=2
- live_trigger_counts: TOO_EARLY=2; MATCH_FINISHED=2
- #1 | window=TOO_EARLY | decision=TOO_EARLY | Cordoba vs Huesca | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=633.49 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window
- #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=333.43 | score=3-1 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=483.51 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #4 | window=TOO_EARLY | decision=TOO_EARLY | Vasco DA Gama vs Atletico-MG | market=BTTS_YES_REVIEW | status=NS | min=0 | mtko=633.42 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Learning / Calibration
- no calibration signal

## Key Files
- data/processed/today/2026-05-31/vsigma_daily_execution_board.md
- data/processed/today/2026-05-31/vsigma_prelock_live_recheck.md
- data/processed/today/2026-05-31/vsigma_live_trigger_validator.md
- data/processed/today/2026-05-31/vsigma_automation_health.md
- data/processed/today/2026-05-31/vsigma_issue_alert_status.md

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
- shadow_queue: data/processed/today/2026-05-31/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-05-31/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-05-31/vsigma_learning_chain_output_sanity.csv
