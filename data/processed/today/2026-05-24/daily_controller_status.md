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
| 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 1 |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 2 |
| 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 3 |

## Candidate v7 Decisions
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |
| 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 2 | PRICE_OK | PRICE_OK |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 3 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 4 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | 2026-05-24T16:33:21.600000+00:00 | 507.02 | 2026-05-24T15:03:21.600000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1545796 | Catanzaro | Monza | OVER_1_5 | 2026-05-24T18:03:18+00:00 | 596.96 | 2026-05-24T16:33:18+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 2026-05-24T05:03:14.400000+00:00 | -183.1 | 2026-05-24T03:33:14.400000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1392205 | Huesca | Castellón | OVER_2_5 | 2026-05-24T16:33:23.400000+00:00 | 507.05 | 2026-05-24T15:03:23.400000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392207.0 | Sporting Gijon | Almeria | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392205.0 | Huesca | Castellón | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1392205.0 | Huesca | Castellón | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1392205.0 | Huesca | Castellón | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392205.0 | Huesca | Castellón | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| CANDIDATE_V5_PLAYER_IMPACT | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |
| CANDIDATE_V6_API_PREDICTIONS | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.48 |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_controller_status.md
