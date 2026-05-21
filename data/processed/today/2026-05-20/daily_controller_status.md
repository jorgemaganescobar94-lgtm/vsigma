# vSIGMA Daily Controller Status - 2026-05-20

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NO_CHANGE']
- POST: SETTLED
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: ALL_SETTLED
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-20 --timezone Atlantic/Canary --mode status`

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
| 1544596 | SC Freiburg | Aston Villa | OVER_1_5 | 2026-05-20T19:00:26.600000+00:00 | -1592.28 | 2026-05-20T17:30:26.600000+00:00 | PRELOCK_NO_CHANGE | ALL_SETTLED |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-20/daily_controller_status.md
