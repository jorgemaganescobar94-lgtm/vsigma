# vSIGMA Daily Controller Status - 2026-05-25

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE']
- POST: PENDING
- Ledger: PRELOCK_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-25 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | 1 |

## Candidate v7 Decisions
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | 2026-05-25T18:31:02.600000+00:00 | 382.52 | 2026-05-25T17:01:02.600000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | POST | PENDING | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/daily_controller_status.md
