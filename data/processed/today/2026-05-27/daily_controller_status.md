# vSIGMA Daily Controller Status - 2026-05-27

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE', 'PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: WAIT_FOR_PRELOCK
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-27 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544608 | UEFA Europa Conference League | Crystal Palace | Rayo Vallecano | OVER_1_5 | 1 |
| 1535322 | CONMEBOL Libertadores | Independiente del Valle | Rosario Central | OVER_1_5 | 2 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544608 | UEFA Europa Conference League | Crystal Palace | Rayo Vallecano | OVER_1_5 | 1 |
| 1535322 | CONMEBOL Libertadores | Independiente del Valle | Rosario Central | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1544608 | UEFA Europa Conference League | Crystal Palace | Rayo Vallecano | OVER_1_5 | 1 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1535322 | CONMEBOL Libertadores | Independiente del Valle | Rosario Central | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544608 | Crystal Palace | Rayo Vallecano | OVER_1_5 | 2026-05-27T19:00:35+00:00 | 46.18 | 2026-05-27T17:30:35+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1535322 | Independiente del Valle | Rosario Central | OVER_1_5 | 2026-05-27T22:00:35.600000+00:00 | 226.19 | 2026-05-27T20:30:35.600000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1544608.0 | Crystal Palace | Rayo Vallecano | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544608.0 | Crystal Palace | Rayo Vallecano | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1544608.0 | Crystal Palace | Rayo Vallecano | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1544608.0 | Crystal Palace | Rayo Vallecano | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1544608.0 | Crystal Palace | Rayo Vallecano | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544608.0 | Crystal Palace | Rayo Vallecano | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535322.0 | Independiente del Valle | Rosario Central | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535322.0 | Independiente del Valle | Rosario Central | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535322.0 | Independiente del Valle | Rosario Central | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535322.0 | Independiente del Valle | Rosario Central | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535322.0 | Independiente del Valle | Rosario Central | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535322.0 | Independiente del Valle | Rosario Central | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-27/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-27/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-27/daily_controller_status.md
