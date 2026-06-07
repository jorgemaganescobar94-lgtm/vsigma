# vSIGMA Daily Controller Status - 2026-06-07

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-06-06

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-07 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1548053 | Segunda División | Las Palmas | Malaga | OVER_1_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1548053 | Segunda División | Las Palmas | Malaga | OVER_1_5 | 1 |

## Candidate v7 Decisions
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1548053 | Segunda División | Las Palmas | Malaga | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1548053 | Las Palmas | Malaga | OVER_1_5 | 2026-06-07T19:00:20.200000+00:00 | 619.71 | 2026-06-07T17:30:20.200000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1548053.0 | Las Palmas | Malaga | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1548053.0 | Las Palmas | Malaga | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1548053.0 | Las Palmas | Malaga | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1548053.0 | Las Palmas | Malaga | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1548053.0 | Las Palmas | Malaga | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1548053.0 | Las Palmas | Malaga | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-07/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-07/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-07/daily_controller_status.md
