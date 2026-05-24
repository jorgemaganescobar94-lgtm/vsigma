# vSIGMA Daily Controller Status - 2026-05-23

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NO_CHANGE']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | 1 | V7_PRELOCK_UNAVAILABLE | PRICE_THIN_SECONDARY_ONLY |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 2026-05-23T13:01:36+00:00 | -1421.3 | 2026-05-23T11:31:36+00:00 | PRELOCK_NO_CHANGE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392205.0 | Huesca | Castellón | OVER_2_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1392205.0 | Huesca | Castellón | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1392205.0 | Huesca | Castellón | OVER_2_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V6_API_PREDICTIONS | 1545796.0 | Catanzaro | Monza | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392205.0 | Huesca | Castellón | OVER_2_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-23/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-23/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-23/daily_controller_status.md
