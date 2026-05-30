# vSIGMA Daily Controller Status - 2026-05-29

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NO_CHANGE']
- POST: PENDING
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | 1 |

## Candidate v7 Decisions
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | 1 | V7_WAITING_FOR_PRELOCK | PRICE_REJECTED |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545409 | Nice | Saint Etienne | OVER_1_5 | 2026-05-29T18:45:19.600000+00:00 | -1032.9 | 2026-05-29T17:15:19.600000+00:00 | PRELOCK_NO_CHANGE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| OFFICIAL_BASELINE | 1545409.0 | Nice | Saint Etienne | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.52 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545409.0 | Nice | Saint Etienne | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.52 |
| CANDIDATE_V4_O25_FIREWALL | 1545409.0 | Nice | Saint Etienne | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.52 |
| CANDIDATE_V5_PLAYER_IMPACT | 1545409.0 | Nice | Saint Etienne | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.52 |
| CANDIDATE_V6_API_PREDICTIONS | 1545409.0 | Nice | Saint Etienne | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.52 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545409.0 | Nice | Saint Etienne | OVER_1_5 | PRELOCK | PRELOCK_UPDATED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/daily_controller_status.md
