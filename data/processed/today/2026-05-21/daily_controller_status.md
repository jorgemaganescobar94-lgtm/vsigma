# vSIGMA Daily Controller Status - 2026-05-21

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE']
- POST: PENDING
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-21 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 1 |
| 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 2 |
| 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 1 |
| 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 2 |
| 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 3 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |
| 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 2 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 3 | PRICE_OK | PRICE_OK |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | 2026-05-21T16:31:08.400000+00:00 | 335.69 | 2026-05-21T15:01:08.400000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 2026-05-21T00:31:15+00:00 | -624.2 | 2026-05-20T23:01:15+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1535208 | Gremio | Palestino | UNDER_3_5 | 2026-05-21T00:01:10.800000+00:00 | -654.27 | 2026-05-20T22:31:10.800000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| OFFICIAL_BASELINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535208.0 | Gremio | Palestino | UNDER_3_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1545410.0 | Brondby | FC Copenhagen | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V4_O25_FIREWALL | 1535208.0 | Gremio | Palestino | UNDER_3_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V5_PLAYER_IMPACT | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 1535208.0 | Gremio | Palestino | UNDER_3_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V6_API_PREDICTIONS | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V6_API_PREDICTIONS | 1535208.0 | Gremio | Palestino | UNDER_3_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.36 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.36 |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_controller_status.md
