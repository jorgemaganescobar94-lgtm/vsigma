# vSIGMA Daily Controller Status - 2026-05-20

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE']
- POST: PENDING
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-20 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 1
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | 1 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 2026-05-20T19:00:40+00:00 | 107.89 | 2026-05-20T17:30:40+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535312.0 | Santa Fe | Platense | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.6 |
| OFFICIAL_BASELINE | 1494229.0 | Gais | Hammarby FF | OVER_2_5 | POST | PENDING | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535312.0 | Santa Fe | Platense | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.6 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1535312.0 | Santa Fe | Platense | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.6 |
| CANDIDATE_V4_O25_FIREWALL | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535312.0 | Santa Fe | Platense | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.6 |
| CANDIDATE_V5_PLAYER_IMPACT | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535312.0 | Santa Fe | Platense | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.6 |
| CANDIDATE_V6_API_PREDICTIONS | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535312.0 | Santa Fe | Platense | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1544596.0 | SC Freiburg | Aston Villa | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_controller_status.md
