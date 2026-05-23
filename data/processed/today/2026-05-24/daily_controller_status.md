# vSIGMA Daily Controller Status - 2026-05-24

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW', 'DUE_NOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-05-23

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 1 |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 2 |
| 1492273 | Serie A | Flamengo | Palmeiras | OVER_1_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 1 |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 2 |
| 1492273 | Serie A | Flamengo | Palmeiras | OVER_1_5 | 3 |

## Candidate v7 Decisions
- Waiting: 2
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |
| 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 2 | PRICE_OK | PRICE_OK |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 3 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1492273 | Serie A | Flamengo | Palmeiras | OVER_1_5 | 4 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | 2026-05-24T16:33:24.600000+00:00 | 1002.99 | 2026-05-24T15:03:24.600000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1545796 | Catanzaro | Monza | OVER_1_5 | 2026-05-24T18:03:21+00:00 | 1092.93 | 2026-05-24T16:33:21+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1492273 | Flamengo | Palmeiras | OVER_1_5 | 2026-05-24T00:03:12.600000+00:00 | 12.79 | 2026-05-23T22:33:12.600000+00:00 | DUE_NOW | CHECK_STALE_OUTPUTS |
| 1392205 | Huesca | Castellón | OVER_2_5 | 2026-05-24T16:33:25.800000+00:00 | 1003.01 | 2026-05-24T15:03:25.800000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392207.0 | Sporting Gijon | Almeria | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392205.0 | Huesca | Castellón | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1392205.0 | Huesca | Castellón | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1392205.0 | Huesca | Castellón | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392205.0 | Huesca | Castellón | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_controller_status.md
