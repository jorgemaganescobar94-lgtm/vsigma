# vSIGMA Daily Controller Status - 2026-05-31

## Step State
- PRE: DONE
- Pre-lock: ['PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-05-30

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-31 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1492282 | Serie A | RB Bragantino | Internacional | OVER_1_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1392226 | Segunda División | Leganes | Mirandes | OVER_1_5 | 1 |
| 1492282 | Serie A | RB Bragantino | Internacional | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 2
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392226 | Segunda División | Leganes | Mirandes | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_THIN_SECONDARY_ONLY |
| 1492282 | Serie A | RB Bragantino | Internacional | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1492282 | RB Bragantino | Internacional | OVER_1_5 | 2026-05-31T14:01:13.200000+00:00 | 852.61 | 2026-05-31T12:31:13.200000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1392226 | Leganes | Mirandes | OVER_1_5 | 2026-05-31T19:01:16.800000+00:00 | 1152.67 | 2026-05-31T17:31:16.800000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1492282.0 | RB Bragantino | Internacional | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392226.0 | Leganes | Mirandes | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1492282.0 | RB Bragantino | Internacional | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1392226.0 | Leganes | Mirandes | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1492282.0 | RB Bragantino | Internacional | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1392226.0 | Leganes | Mirandes | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1492282.0 | RB Bragantino | Internacional | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1392226.0 | Leganes | Mirandes | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1492282.0 | RB Bragantino | Internacional | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392226.0 | Leganes | Mirandes | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1492282.0 | RB Bragantino | Internacional | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-31/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-31/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-31/daily_controller_status.md
