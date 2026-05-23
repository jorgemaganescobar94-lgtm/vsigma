# vSIGMA Daily Controller Status - 2026-05-23

## Step State
- PRE: DONE
- Pre-lock: ['PRELOCK_NOT_AVAILABLE']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: RUN_POST_AFTER_FINISH
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1504822 | J1 League | Kashima | FC Tokyo | OVER_1_5 | 1 |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | 2 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1504822 | J1 League | Kashima | FC Tokyo | OVER_1_5 | 1 |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | 2 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 2
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1504822 | J1 League | Kashima | FC Tokyo | OVER_1_5 | 1 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | 2 | V7_PRELOCK_UNAVAILABLE | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1504822 | Kashima | FC Tokyo | OVER_1_5 | 2026-05-23T08:31:50.600000+00:00 | 41.85 | 2026-05-23T07:01:50.600000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |
| 1494182 | Kalmar FF | Degerfors IF | OVER_1_5 | 2026-05-23T13:01:51.200000+00:00 | 311.86 | 2026-05-23T11:31:51.200000+00:00 | PRELOCK_NOT_AVAILABLE | RUN_POST_AFTER_FINISH |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1504822.0 | Kashima | FC Tokyo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1494182.0 | Kalmar FF | Degerfors IF | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-23/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-23/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-23/daily_controller_status.md
