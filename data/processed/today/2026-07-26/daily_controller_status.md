# vSIGMA Daily Controller Status - 2026-07-26

## Step State
- PRE: DONE
- Pre-lock: ['KICKOFF_PASSED']
- POST: SETTLED
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: ALL_SETTLED
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-26 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494217 | Allsvenskan | IF Brommapojkarna | Hammarby FF | OVER_2_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494217 | Allsvenskan | IF Brommapojkarna | Hammarby FF | OVER_2_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 1
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494217 | Allsvenskan | IF Brommapojkarna | Hammarby FF | OVER_2_5 | 1 | V7_SECONDARY_ONLY | PRICE_THIN_SECONDARY_ONLY |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494217 | IF Brommapojkarna | Hammarby FF | OVER_2_5 | 2026-07-26T12:01:29+00:00 | -1369.58 | 2026-07-26T10:31:29+00:00 | KICKOFF_PASSED | ALL_SETTLED |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1494217.0 | IF Brommapojkarna | Hammarby FF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494217.0 | IF Brommapojkarna | Hammarby FF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1494217.0 | IF Brommapojkarna | Hammarby FF | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.17 |
| CANDIDATE_V5_PLAYER_IMPACT | 1494217.0 | IF Brommapojkarna | Hammarby FF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | LOSS | -1.0 |
| CANDIDATE_V6_API_PREDICTIONS |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V7_PRICE_DISCIPLINE |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-26/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-26/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-26/daily_controller_status.md
