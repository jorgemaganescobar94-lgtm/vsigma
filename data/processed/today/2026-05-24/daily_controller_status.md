# vSIGMA Daily Controller Status - 2026-05-24

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE', 'PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: WAIT_FOR_PRELOCK
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 1 |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 2 |
| 1492276 | Serie A | Remo | Atletico Paranaense | OVER_1_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 1 |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |
| 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 2 | PRICE_OK | PRICE_OK |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 3 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | 2026-05-24T16:32:34.600000+00:00 | 272.54 | 2026-05-24T15:02:34.600000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1545796 | Catanzaro | Monza | OVER_1_5 | 2026-05-24T18:02:31+00:00 | 362.48 | 2026-05-24T16:32:31+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1492276 | Remo | Atletico Paranaense | OVER_1_5 | 2026-05-24T19:02:26.800000+00:00 | 422.41 | 2026-05-24T17:32:26.800000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |
| 1392205 | Huesca | Castellón | OVER_2_5 | 2026-05-24T16:32:35.800000+00:00 | 272.56 | 2026-05-24T15:02:35.800000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392207.0 | Sporting Gijon | Almeria | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392205.0 | Huesca | Castellón | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1392205.0 | Huesca | Castellón | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1392205.0 | Huesca | Castellón | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392205.0 | Huesca | Castellón | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| CANDIDATE_V5_PLAYER_IMPACT | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| CANDIDATE_V6_API_PREDICTIONS | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| OFFICIAL_BASELINE | 1492276.0 | Remo | Atletico Paranaense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_controller_status.md
