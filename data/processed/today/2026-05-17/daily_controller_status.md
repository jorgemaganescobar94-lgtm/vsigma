# vSIGMA Daily Controller Status - 2026-05-17

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: WAIT_FOR_PRELOCK
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-17 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544950 | Serie B | Catanzaro | Palermo | OVER_1_5 | 1 |
| 1492260 | Serie A | Atletico Paranaense | Flamengo | OVER_1_5 | 2 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544950 | Serie B | Catanzaro | Palermo | OVER_1_5 | 1 |
| 1492260 | Serie A | Atletico Paranaense | Flamengo | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 2
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1544950 | Serie B | Catanzaro | Palermo | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1492260 | Serie A | Atletico Paranaense | Flamengo | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544950 | Catanzaro | Palermo | OVER_1_5 | 2026-05-17T18:04:26.800000+00:00 | 370.93 | 2026-05-17T16:34:26.800000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |
| 1492260 | Atletico Paranaense | Flamengo | OVER_1_5 | 2026-05-17T22:34:22.600000+00:00 | 640.86 | 2026-05-17T21:04:22.600000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1544950.0 | Catanzaro | Palermo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1492260.0 | Atletico Paranaense | Flamengo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544950.0 | Catanzaro | Palermo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1492260.0 | Atletico Paranaense | Flamengo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1544950.0 | Catanzaro | Palermo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1492260.0 | Atletico Paranaense | Flamengo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1544950.0 | Catanzaro | Palermo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1492260.0 | Atletico Paranaense | Flamengo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1544950.0 | Catanzaro | Palermo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1492260.0 | Atletico Paranaense | Flamengo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544950.0 | Catanzaro | Palermo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1492260.0 | Atletico Paranaense | Flamengo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/daily_controller_status.md
