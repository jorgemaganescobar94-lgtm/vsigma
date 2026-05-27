# vSIGMA Daily Operator Brief - 2026-05-27

## Executive Summary
- operator_status: WAIT_LIVE_WINDOW
- primary_next_action: Wait for useful live window and rerun live trigger validator.
- health_status: ATTENTION
- active_candidates: 0
- waiting_live_window: 2
- closed_or_missed: 2
- board_decisions: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; NO_BET=4; PRELOCK_REVIEW_LOW_STAKE=2; LIVE_ONLY=2
- recheck_decisions: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- live_triggers: MATCH_FINISHED=2; TOO_EARLY=2
- alert_notify_required: false
- auto_apply: NO
- production_change: NO

## Active Review Candidates
- none

## Waiting Live Window
- LIVE_ONLY_WAIT_TRIGGER | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | window=TOO_EARLY | live_decision=TOO_EARLY
- LIVE_ONLY_WAIT_TRIGGER | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | window=TOO_EARLY | live_decision=TOO_EARLY

## Closed / Window Missed
- READY_LOW_STAKE_REVIEW | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | window=MATCH_FINISHED | live_decision=MATCH_FINISHED
- READY_LOW_STAKE_REVIEW | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | window=MATCH_FINISHED | live_decision=MATCH_FINISHED

## Live Trigger Status
- window_counts: MATCH_FINISHED=2; TOO_EARLY=2
- live_trigger_counts: MATCH_FINISHED=2; TOO_EARLY=2
- #1 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.52 | score=3-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.53 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | window=TOO_EARLY | decision=TOO_EARLY | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1120.49 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window
- #4 | window=TOO_EARLY | decision=TOO_EARLY | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1300.47 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Blocked / Watch Only
- final_decision_counts: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; NO_BET=4; PRELOCK_REVIEW_LOW_STAKE=2; LIVE_ONLY=2
- #9 | NO_BET_OR_WATCH | Estudiantes L.P. vs Independiente Medellin | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | stake=NO_STAKE_OR_SYMBOLIC | score=18 | conf=HIGH | bucket=WEAK_WATCH | stats=goals 1.69-2.69 | shots 20-29 | SoT 6-10 | corners 7-12 | cards 4-8 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation
- #10 | NO_BET_OR_WATCH | Independiente del Valle vs Rosario Central | market=OVER_1_5_SUPPORTED | alt=BTTS_OR_OVER_1_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | score=18 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 2.05-3.45 | shots 22-33 | SoT 6-11 | corners 8-14 | cards 3-7 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; no portfolio/context confirmation; bad or incomplete lineups
- #11 | NO_BET_OR_WATCH | Vasco DA Gama vs Barracas Central | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | stake=NO_STAKE_OR_SYMBOLIC | score=-2 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 1.56-2.69 | shots 22-33 | SoT 7-13 | corners 8-14 | cards 3-7 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #12 | NO_BET_OR_WATCH | Atletico-MG vs Puerto Cabello | market=CARDS_OVER_3_5_REVIEW | alt=CARDS_OVER_4_5_AGGRESSIVE | stake=NO_STAKE_OR_SYMBOLIC | score=-10 | conf=MEDIUM | bucket=WEAK_WATCH | stats=goals 2.02-3.61 | shots 21-33 | SoT 5-11 | corners 6-12 | cards 3-8 | prelock=none | live=live tempo: early shots, SoT threat, box entries, pressure and no dead 0-0 rhythm | cancel=default no bet; bad or incomplete lineups
- #13 | NO_BET | Santos vs Deportivo Cuenca | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=10 | conf=HIGH | bucket=BLOCKED | stats=goals 1.84-2.91 | shots 23-33 | SoT 6-11 | corners 8-13 | cards 3-7 | prelock=none | live=none | cancel=default no bet; no portfolio/context confirmation
- #14 | NO_BET | San Lorenzo vs Deportivo Recoleta | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=10 | conf=HIGH | bucket=BLOCKED | stats=goals 1.43-2.32 | shots 21-30 | SoT 6-10 | corners 7-12 | cards 2-6 | prelock=none | live=none | cancel=default no bet; no portfolio/context confirmation
- #15 | NO_BET | Cienciano vs Juventud | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-18 | conf=MEDIUM | bucket=BLOCKED | stats=goals 1.78-3.22 | shots 20-32 | SoT 6-12 | corners 7-14 | cards 1-4 | prelock=none | live=none | cancel=default no bet; bad or incomplete lineups
- #16 | NO_BET | Cuniburo vs Orense SC | market=NO_CLEAR_STAT_MARKET | alt=NONE | stake=NO_STAKE | score=-42 | conf=LOW | bucket=BLOCKED | stats=goals 1.58-3.12 | shots 17-29 | SoT 5-11 | corners 6-13 | cards 2-6 | prelock=none | live=none | cancel=default no bet; low forecast confidence
- recheck_decision_counts: STAT_WATCH_ONLY=4; NO_BET_OR_WATCH=4; CANCELLED_NO_BET=4; READY_LOW_STAKE_REVIEW=2; LIVE_ONLY_WAIT_TRIGGER=2
- #9 | NO_BET_OR_WATCH | Estudiantes L.P. vs Independiente Medellin | market=CARDS_OVER_3_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state
- #10 | NO_BET_OR_WATCH | Independiente del Valle vs Rosario Central | market=OVER_1_5_SUPPORTED | stake=NO_STAKE_OR_SYMBOLIC | lineup= | min=NA | availability= | next=watch only | note=weak watch state

## Learning / Calibration
- calibration_status_counts: MODEL_OVER_ESTIMATING=3; MODEL_UNDER_ESTIMATING=2; CALIBRATION_OK=1
- total_cards | rows=4 | hit_rate=0.750 | avg_error=1.75 | bias=UNDER_ESTIMATE | status=CALIBRATION_OK
- total_corners | rows=6 | hit_rate=0.667 | avg_error=2.50 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_fouls | rows=6 | hit_rate=0.667 | avg_error=4.17 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING
- total_goals | rows=6 | hit_rate=0.167 | avg_error=1.34 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_shots | rows=6 | hit_rate=0.500 | avg_error=7.33 | bias=OVER_ESTIMATE | status=MODEL_OVER_ESTIMATING
- total_sot | rows=6 | hit_rate=0.333 | avg_error=3.50 | bias=UNDER_ESTIMATE | status=MODEL_UNDER_ESTIMATING

## Key Files
- data/processed/today/2026-05-27/vsigma_daily_execution_board.md
- data/processed/today/2026-05-27/vsigma_prelock_live_recheck.md
- data/processed/today/2026-05-27/vsigma_live_trigger_validator.md
- data/processed/today/2026-05-27/vsigma_automation_health.md
- data/processed/today/2026-05-27/vsigma_issue_alert_status.md

## Guardrails
- Brief is diagnostic only; it does not execute bets.
- Manual review remains mandatory for every market.
