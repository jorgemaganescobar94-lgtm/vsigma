# vSIGMA Daily Controller Status - 2026-05-19

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-05-18

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-19 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544951 | Serie B | Monza | Juve Stabia | OVER_1_5 | 1 |
| 1535300 | CONMEBOL Libertadores | Coquimbo Unido | Deportes Tolima | OVER_1_5 | 2 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544951 | Serie B | Monza | Juve Stabia | OVER_1_5 | 1 |
| 1535300 | CONMEBOL Libertadores | Coquimbo Unido | Deportes Tolima | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 2
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1544951 | Serie B | Monza | Juve Stabia | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_THIN_SECONDARY_ONLY |
| 1535300 | CONMEBOL Libertadores | Coquimbo Unido | Deportes Tolima | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544951 | Monza | Juve Stabia | OVER_1_5 | 2026-05-19T18:00:54.400000+00:00 | 430.98 | 2026-05-19T16:30:54.400000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1535300 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | 2026-05-19T22:00:58+00:00 | 671.04 | 2026-05-19T20:30:58+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1544951.0 | Monza | Juve Stabia | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535300.0 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544951.0 | Monza | Juve Stabia | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535300.0 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1544951.0 | Monza | Juve Stabia | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535300.0 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1544951.0 | Monza | Juve Stabia | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535300.0 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1544951.0 | Monza | Juve Stabia | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535300.0 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544951.0 | Monza | Juve Stabia | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535300.0 | Coquimbo Unido | Deportes Tolima | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-19/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-19/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-19/daily_controller_status.md
