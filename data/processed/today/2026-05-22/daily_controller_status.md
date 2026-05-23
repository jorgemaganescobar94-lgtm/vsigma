# vSIGMA Daily Controller Status - 2026-05-22

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE', 'PRELOCK_CONFIRMED']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544652 | Serie B | Sudtirol | Bari | OVER_1_5 | 1 |
| 1494177 | Allsvenskan | Djurgardens IF | IF Brommapojkarna | OVER_2_5 | 2 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544652 | Serie B | Sudtirol | Bari | OVER_1_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1544652 | Serie B | Sudtirol | Bari | OVER_1_5 | 1 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544652 | Sudtirol | Bari | OVER_1_5 | 2026-05-22T18:00:38.600000+00:00 | -1062.01 | 2026-05-22T16:30:38.600000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1494177 | Djurgardens IF | IF Brommapojkarna | OVER_2_5 | 2026-05-22T17:00:38.600000+00:00 | -1122.01 | 2026-05-22T15:30:38.600000+00:00 | PRELOCK_CONFIRMED | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V6_API_PREDICTIONS | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V6_API_PREDICTIONS | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-22/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-22/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-22/daily_controller_status.md
