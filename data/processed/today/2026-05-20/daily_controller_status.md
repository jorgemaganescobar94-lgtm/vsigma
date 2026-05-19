# vSIGMA Daily Controller Status - 2026-05-20

## Step State
- PRE: DONE
- Pre-lock: ['DUE_NOW', 'PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-05-19

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-20 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1535312 | CONMEBOL Libertadores | Santa Fe | Platense | OVER_1_5 | 1 |
| 1494229 | Allsvenskan | Gais | Hammarby FF | OVER_2_5 | 2 |
| 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1535312 | CONMEBOL Libertadores | Santa Fe | Platense | OVER_1_5 | 1 |
| 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 2
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1535312 | CONMEBOL Libertadores | Santa Fe | Platense | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535312 | Santa Fe | Platense | OVER_1_5 | 2026-05-20T00:01:06+00:00 | 15.54 | 2026-05-19T22:31:06+00:00 | DUE_NOW | CHECK_STALE_OUTPUTS |
| 1494229 | Gais | Hammarby FF | OVER_2_5 | 2026-05-20T17:01:04.800000+00:00 | 1035.52 | 2026-05-20T15:31:04.800000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 2026-05-20T19:01:04.800000+00:00 | 1155.52 | 2026-05-20T17:31:04.800000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1494229.0 | Gais | Hammarby FF | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_controller_status.md
