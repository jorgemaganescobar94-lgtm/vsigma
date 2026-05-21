# vSIGMA Daily Controller Status - 2026-05-21

## Step State
- PRE: DONE
- Pre-lock: ['NO_CURRENT_PICKS']
- POST: PENDING
- Ledger: PRELOCK_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: NO_BET_DAY
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-21 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
_No rows._

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
|  |  |  |  |  |  |  | NO_CURRENT_PICKS | NO_BET_DAY |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | LOSS | -1.0 |
| OFFICIAL_BASELINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1545410.0 | Brondby | FC Copenhagen | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V4_O25_FIREWALL | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V5_PLAYER_IMPACT | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V6_API_PREDICTIONS | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V6_API_PREDICTIONS | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK | PRELOCK_UPDATED | RESULT_AVAILABLE | WIN | 0.36 |
| OFFICIAL_BASELINE |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V5_PLAYER_IMPACT |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V6_API_PREDICTIONS |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V7_PRICE_DISCIPLINE |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_controller_status.md
