# vSIGMA Daily Controller Status - 2026-06-09

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-09 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1548054 | Segunda División | Almeria | Castellón | OVER_2_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1548054 | Segunda División | Almeria | Castellón | OVER_2_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1548054 | Segunda División | Almeria | Castellón | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1548054 | Almeria | Castellón | OVER_2_5 | 2026-06-09T19:00:18+00:00 | -1391.86 | 2026-06-09T17:30:18+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1548055.0 | Malaga | Las Palmas | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1548055.0 | Malaga | Las Palmas | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1548055.0 | Malaga | Las Palmas | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V6_API_PREDICTIONS | 1548055.0 | Malaga | Las Palmas | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/daily_controller_status.md
