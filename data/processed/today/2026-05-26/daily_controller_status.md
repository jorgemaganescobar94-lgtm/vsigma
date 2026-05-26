# vSIGMA Daily Controller Status - 2026-05-26

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: WAIT_FOR_PRELOCK
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-26 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1535324 | CONMEBOL Libertadores | LDU de Quito | Always Ready | UNDER_3_5 | 1 |

## Candidate v2 Picks
_No rows._

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
_No rows._

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535324 | LDU de Quito | Always Ready | UNDER_3_5 | 2026-05-26T22:00:24.600000+00:00 | 147.55 | 2026-05-26T20:30:24.600000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V5_PLAYER_IMPACT |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V6_API_PREDICTIONS |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V7_PRICE_DISCIPLINE |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| OFFICIAL_BASELINE | 1535324.0 | LDU de Quito | Always Ready | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/daily_controller_status.md
