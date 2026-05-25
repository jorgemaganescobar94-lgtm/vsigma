# vSIGMA Daily Controller Status - 2026-05-24

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE', 'KICKOFF_PASSED']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode post`

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
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | 2026-05-24T16:32:34.600000+00:00 | -1420.04 | 2026-05-24T15:02:34.600000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1545796 | Catanzaro | Monza | OVER_1_5 | 2026-05-24T18:02:31+00:00 | -1330.1 | 2026-05-24T16:32:31+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1492276 | Remo | Atletico Paranaense | OVER_1_5 | 2026-05-24T19:02:26.800000+00:00 | -1270.17 | 2026-05-24T17:32:26.800000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1392205 | Huesca | Castellón | OVER_2_5 | 2026-05-24T16:32:35.800000+00:00 | -1420.02 | 2026-05-24T15:02:35.800000+00:00 | KICKOFF_PASSED | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V6_API_PREDICTIONS | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_controller_status.md
