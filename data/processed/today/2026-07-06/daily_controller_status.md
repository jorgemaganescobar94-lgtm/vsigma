# vSIGMA Daily Controller Status - 2026-07-06

## Step State
- PRE: DONE
- Pre-lock: ['KICKOFF_PASSED']
- POST: SETTLED
- Ledger: POST_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: ALL_SETTLED
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-06 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494197 | Allsvenskan | BK Hacken | Djurgardens IF | OVER_2_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494197 | Allsvenskan | BK Hacken | Djurgardens IF | OVER_2_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494197 | Allsvenskan | BK Hacken | Djurgardens IF | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494197 | BK Hacken | Djurgardens IF | OVER_2_5 | 2026-07-06T17:00:25.400000+00:00 | -1053.1 | 2026-07-06T15:30:25.400000+00:00 | KICKOFF_PASSED | ALL_SETTLED |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1494197.0 | BK Hacken | Djurgardens IF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.57 |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494197.0 | BK Hacken | Djurgardens IF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.57 |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1494197.0 | BK Hacken | Djurgardens IF | OVER_1_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.18 |
| CANDIDATE_V5_PLAYER_IMPACT | 1494197.0 | BK Hacken | Djurgardens IF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.57 |
| CANDIDATE_V6_API_PREDICTIONS |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1494197.0 | BK Hacken | Djurgardens IF | OVER_2_5 | POST | SETTLED | RESULT_AVAILABLE | WIN | 0.57 |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-06/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-06/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-06/daily_controller_status.md
