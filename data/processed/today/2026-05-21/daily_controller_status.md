# vSIGMA Daily Controller Status - 2026-05-21

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW', 'DUE_NOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-05-20

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-21 --timezone Atlantic/Canary --mode status`

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
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |
| 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 3 | PRICE_OK | PRICE_OK |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | 2026-05-21T16:31:07.400000+00:00 | 1047.93 | 2026-05-21T15:01:07.400000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | 2026-05-21T00:31:14.600000+00:00 | 88.05 | 2026-05-20T23:01:14.600000+00:00 | DUE_NOW | CHECK_STALE_OUTPUTS |
| 1535208 | Gremio | Palestino | UNDER_3_5 | 2026-05-21T00:01:09.800000+00:00 | 57.97 | 2026-05-20T22:31:09.800000+00:00 | DUE_NOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1545410.0 | Brondby | FC Copenhagen | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_controller_status.md
