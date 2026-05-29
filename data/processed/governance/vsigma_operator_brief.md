# vSIGMA Daily Operator Brief - 2026-05-29

## Compact Top Summary
| Field | Value | Meaning |
|---|---|---|
| Action | BROKEN | First-read operator priority |
| Risk | HIGH | Operational risk after sanity + health gate |
| Alert | CRITICAL_STOP / CRITICAL | Routing decision for operator notifications |
| Counts | active=0; live=0; closed=0; watch=12; no_bet=8 | Candidate distribution |
| Reason | system fault blocks market usage | Why this action level was selected |
| Final | SYSTEM_FIX_REQUIRED | sanity=PASS; broken-state routing is explicit |

## Alert Routing
| Field | Value | Meaning |
|---|---|---|
| Route | CRITICAL_STOP | NO_ALERT / LOCAL_ONLY / GITHUB_ISSUE_COMMENT / CRITICAL_STOP |
| Materiality | CRITICAL | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| Reason | sanity failure or broken system state blocks operator usage | Why this route was selected |
| Drift | NO_MATERIAL_CHANGE | Historical drift status |
| DriftNotify | false | Raw material drift notification flag |

## Historical Drift Check
| Field | Value | Meaning |
|---|---|---|
| Previous | date=2026-05-29; action=BROKEN; risk=HIGH; final=SYSTEM_FIX_REQUIRED; active=0 | data/processed/today/2026-05-29/vsigma_operator_brief.csv |
| Current | date=2026-05-29; action=BROKEN; risk=HIGH; final=SYSTEM_FIX_REQUIRED; active=0 | current_build |
| Drift | NO_MATERIAL_CHANGE | tracked operator fields unchanged |
| Changed | none | Tracked fields: action/final/risk/active |
| Notify | false | true only on material operator drift |

## Executive Summary
- action_level: BROKEN
- compact_final_decision: SYSTEM_FIX_REQUIRED
- risk_label: HIGH
- alert_route: CRITICAL_STOP
- alert_materiality: CRITICAL
- alert_reason: sanity failure or broken system state blocks operator usage
- drift_status: NO_MATERIAL_CHANGE
- drift_notify_required: false
- drift_changed_fields: none
- sanity_check: PASS | broken-state routing is explicit
- operator_status: BROKEN
- primary_next_action: Fix missing/broken workflow input before using any market signal.
- health_status: BROKEN
- active_candidates: 0
- waiting_live_window: 0
- closed_or_missed: 0
- watch_only: 12
- no_bet: 8
- board_decisions: NO_BET_OR_WATCH=10; NO_BET=8; LIVE_ONLY=1; STAT_WATCH_ONLY=1
- recheck_decisions: none
- live_triggers: none
- alert_notify_required: UNKNOWN
- auto_apply: NO
- production_change: NO

## Operator Priority
- ACTION_LEVEL=BROKEN
- RISK_LABEL=HIGH
- FINAL_DECISION=SYSTEM_FIX_REQUIRED
- ALERT_ROUTE=CRITICAL_STOP
- ALERT_MATERIALITY=CRITICAL
- ALERT_REASON=sanity failure or broken system state blocks operator usage
- DRIFT_STATUS=NO_MATERIAL_CHANGE
- DRIFT_NOTIFY_REQUIRED=false
- SANITY_CHECK=PASS
- SANITY_DETAIL=broken-state routing is explicit
- WINDOWS_READ=UTF8 | Get-Content data/processed/today/2026-05-29/vsigma_operator_brief.md -Encoding UTF8

## Active Review
- none

## Waiting Live Window
- none

## Closed / Window Missed
- none

## Watch Only
- #1 | LIVE_ONLY | Monza vs Catanzaro | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=LIVE_CANDIDATE | conf=MEDIUM | score=17 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=bad or incomplete lineups
- #2 | STAT_WATCH_ONLY | Valerenga vs Kristiansund BK | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WATCHLIST | conf=MEDIUM | score=48 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=no portfolio/context confirmation; bad or incomplete lineups
- #3 | NO_BET_OR_WATCH | Fredrikstad vs Start | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=23 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #4 | NO_BET_OR_WATCH | Orgryte IS vs IF Elfsborg | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=18 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #5 | NO_BET_OR_WATCH | Aalesund vs Ham-Kam | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | bucket=WEAK_WATCH | conf=MEDIUM | score=16 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #6 | NO_BET_OR_WATCH | Tigre vs Alianza Atletico | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=MEDIUM | score=2 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #7 | NO_BET_OR_WATCH | Rosenborg vs Bodo/Glimt | market=CORNERS_OVER_8_5_REVIEW | alt=CORNERS_OVER_9_5_AGGRESSIVE | bucket=WEAK_WATCH | conf=MEDIUM | score=-1 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #8 | NO_BET_OR_WATCH | Cruzeiro vs Barcelona SC | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | bucket=WEAK_WATCH | conf=MEDIUM | score=-2 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #9 | NO_BET_OR_WATCH | Boca Juniors vs U. Catolica | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | bucket=WEAK_WATCH | conf=MEDIUM | score=-4 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #10 | NO_BET_OR_WATCH | Nice vs Saint Etienne | market=UNDER_3_5_REVIEW | alt=NO_GOALS_AGGRESSION | bucket=WEAK_WATCH | conf=MEDIUM | score=-6 | live=live control: low SoT, low big chances, stable defensive structure | cancel=default no bet; bad or incomplete lineups; new availability downgrade
- #11 | NO_BET_OR_WATCH | Brann vs Sarpsborg 08 FF | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=LOW | score=-20 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; low forecast confidence; bad or incomplete lineups; new availability downgrade
- #12 | NO_BET_OR_WATCH | KFUM Oslo vs Tromso | market=BTTS_YES_REVIEW | alt=OVER_1_5_REVIEW | bucket=WEAK_WATCH | conf=LOW | score=-32 | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; low forecast confidence; bad or incomplete lineups; new availability downgrade

## No Bet
- #13 | NO_BET | America de Cali vs Macara | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=MEDIUM | score=-4 | cancel=default no bet; bad or incomplete lineups
- #14 | NO_BET | El Mokawloon vs Future FC | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #15 | NO_BET | Ghazl El Mehalla vs Haras El Hodood | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #16 | NO_BET | Masr vs Kahraba Ismailia | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #17 | NO_BET | National Bank of Egypt vs Al Ittihad | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #18 | NO_BET | FK Trakai vs Suduva Marijampole | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #19 | NO_BET | TransINVEST Vilnius vs Hegelmann Litauen | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence
- #20 | NO_BET | Cde Juventud Italiana vs Tecnico Universitario | market=NO_CLEAR_STAT_MARKET | bucket=BLOCKED | conf=LOW | score=-42 | cancel=default no bet; low forecast confidence

## Live Trigger Status
- no live trigger report or no live candidates

## Learning / Calibration
- no calibration signal

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
- shadow_queue: data/processed/today/2026-05-29/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/today/2026-05-29/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-05-29/vsigma_learning_chain_output_sanity.csv
