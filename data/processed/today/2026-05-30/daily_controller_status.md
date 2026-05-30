# vSIGMA Daily Controller Status - 2026-05-30

## Step State
- PRE: DONE
- Pre-lock: ['DUE_NOW', 'PENDING_OUTSIDE_WINDOW']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: STALE_PRELOCK_EXCLUDED: 2026-05-29

## Next Operator Command
- Action: CHECK_STALE_OUTPUTS
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494185 | Allsvenskan | AIK Stockholm | Sirius | OVER_2_5 | 1 |
| 1492281 | Serie A | Bahia | Botafogo | OVER_2_5 | 2 |
| 1544371 | UEFA Champions League | Paris Saint Germain | Arsenal | OVER_1_5 | 3 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494185 | Allsvenskan | AIK Stockholm | Sirius | OVER_2_5 | 1 |
| 1492281 | Serie A | Bahia | Botafogo | OVER_2_5 | 2 |
| 1544371 | UEFA Champions League | Paris Saint Germain | Arsenal | OVER_1_5 | 3 |

## Candidate v7 Decisions
- Waiting: 1
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494185 | Allsvenskan | AIK Stockholm | Sirius | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |
| 1492281 | Serie A | Bahia | Botafogo | OVER_2_5 | 2 | PRICE_OK | PRICE_OK |
| 1544371 | UEFA Champions League | Paris Saint Germain | Arsenal | OVER_1_5 | 3 | V7_WAITING_FOR_PRELOCK | PRICE_NEEDS_PRELOCK_CONFIRMATION |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494185 | AIK Stockholm | Sirius | OVER_2_5 | 2026-05-30T13:01:02+00:00 | 58.33 | 2026-05-30T11:31:02+00:00 | DUE_NOW | CHECK_STALE_OUTPUTS |
| 1492281 | Bahia | Botafogo | OVER_2_5 | 2026-05-30T20:30:59.600000+00:00 | 508.29 | 2026-05-30T19:00:59.600000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |
| 1544371 | Paris Saint Germain | Arsenal | OVER_1_5 | 2026-05-30T16:01:02.600000+00:00 | 238.34 | 2026-05-30T14:31:02.600000+00:00 | PENDING_OUTSIDE_WINDOW | CHECK_STALE_OUTPUTS |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1494185.0 | AIK Stockholm | Sirius | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1492281.0 | Bahia | Botafogo | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| OFFICIAL_BASELINE | 1544371.0 | Paris Saint Germain | Arsenal | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494185.0 | AIK Stockholm | Sirius | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1492281.0 | Bahia | Botafogo | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544371.0 | Paris Saint Germain | Arsenal | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V4_O25_FIREWALL | 1494185.0 | AIK Stockholm | Sirius | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V4_O25_FIREWALL | 1492281.0 | Bahia | Botafogo | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1494185.0 | AIK Stockholm | Sirius | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1492281.0 | Bahia | Botafogo | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1544371.0 | Paris Saint Germain | Arsenal | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V6_API_PREDICTIONS | 1544371.0 | Paris Saint Germain | Arsenal | OVER_1_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1494185.0 | AIK Stockholm | Sirius | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1492281.0 | Bahia | Botafogo | OVER_2_5 | PRE | PRE_REGISTERED | PENDING | PENDING |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/daily_controller_status.md
