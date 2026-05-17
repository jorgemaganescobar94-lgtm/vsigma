# vSIGMA Daily Controller Status - 2026-05-16

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE']
- POST: PENDING
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-16 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1388609 | Bundesliga | SC Freiburg | RB Leipzig | OVER_2_5 | 1 |
| 1392194 | Segunda División | Granada CF | Burgos | OVER_1_5 | 2 |
| 1544949 | Serie B | Juve Stabia | Monza | OVER_1_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392194 | Segunda División | Granada CF | Burgos | OVER_1_5 | 1 |
| 1544949 | Serie B | Juve Stabia | Monza | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 2
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392194 | Segunda División | Granada CF | Burgos | OVER_1_5 | 1 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1544949 | Serie B | Juve Stabia | Monza | OVER_1_5 | 2 | V7_PRELOCK_UNAVAILABLE | PRICE_REJECTED |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1388609 | SC Freiburg | RB Leipzig | OVER_2_5 | 2026-05-16T13:33:09.200000+00:00 | -1324.32 | 2026-05-16T12:03:09.200000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1392194 | Granada CF | Burgos | OVER_1_5 | 2026-05-16T16:33:02+00:00 | -1144.44 | 2026-05-16T15:03:02+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1544949 | Juve Stabia | Monza | OVER_1_5 | 2026-05-16T18:03:00.800000+00:00 | -1054.46 | 2026-05-16T16:33:00.800000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392194.0 | Granada CF | Burgos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| OFFICIAL_BASELINE | 1544949.0 | Juve Stabia | Monza | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.55 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392194.0 | Granada CF | Burgos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544949.0 | Juve Stabia | Monza | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.55 |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1392194.0 | Granada CF | Burgos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V4_O25_FIREWALL | 1544949.0 | Juve Stabia | Monza | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.55 |
| CANDIDATE_V5_PLAYER_IMPACT | 1392194.0 | Granada CF | Burgos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 1544949.0 | Juve Stabia | Monza | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.55 |
| CANDIDATE_V6_API_PREDICTIONS | 1392194.0 | Granada CF | Burgos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V6_API_PREDICTIONS | 1544949.0 | Juve Stabia | Monza | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.55 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392194.0 | Granada CF | Burgos | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1388609.0 | SC Freiburg | RB Leipzig | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.52 |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/daily_controller_status.md
