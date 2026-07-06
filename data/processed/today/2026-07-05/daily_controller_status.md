# vSIGMA Daily Controller Status - 2026-07-05

## Step State
- PRE: DONE
- Pre-lock: ['KICKOFF_PASSED']
- POST: SETTLED
- Ledger: MISSING_FOR_DATE
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: ALL_SETTLED
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-05 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494195 | Allsvenskan | IF Elfsborg | Hammarby FF | OVER_2_5 | 1 |

## Candidate v2 Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank |
| --- | --- | --- | --- | --- | --- |
| 1494195 | Allsvenskan | IF Elfsborg | Hammarby FF | OVER_2_5 | 1 |

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | candidate_v7_execution_status | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494195 | Allsvenskan | IF Elfsborg | Hammarby FF | OVER_2_5 | 1 | PRICE_OK | PRICE_OK |

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494195 | IF Elfsborg | Hammarby FF | OVER_2_5 | 2026-07-05T14:30:41+00:00 | -1273.75 | 2026-07-05T13:00:41+00:00 | KICKOFF_PASSED | ALL_SETTLED |

## Ledger State
_No rows._

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-05/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-05/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-07-05/daily_controller_status.md
