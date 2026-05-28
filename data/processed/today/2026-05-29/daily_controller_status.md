# vSIGMA Daily Controller Status - 2026-05-29

## Step State
- PRE: DONE
- Pre-lock: ['DUE_NOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_PRELOCK_NOW
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | 1 |
| 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | 2 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | 1 |
| 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 2
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | 2 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 2026-05-29T00:31:01.200000+00:00 | 85.16 | 2026-05-28T23:01:01.200000+00:00 | DUE_NOW | RUN_PRELOCK_NOW |
| 1535218 | America de Cali | Macara | OVER_1_5 | 2026-05-29T00:30:58.800000+00:00 | 85.12 | 2026-05-28T23:00:58.800000+00:00 | DUE_NOW | RUN_PRELOCK_NOW |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1535218.0 | America de Cali | Macara | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535218.0 | America de Cali | Macara | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1535218.0 | America de Cali | Macara | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1535218.0 | America de Cali | Macara | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1535218.0 | America de Cali | Macara | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535218.0 | America de Cali | Macara | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/daily_controller_status.md
