# vSIGMA Daily Controller Status - 2026-05-21

## Step State
- PRE: DONE
- Pre-lock: ['NO_CURRENT_PICKS']
- POST: PENDING
- Ledger: PRE_UPDATED
- Governance: AVAILABLE
- Stale warnings: NONE

## Next Operator Command
- Action: NO_BET_DAY
- Command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-21 --timezone Atlantic/Canary --mode status`

## Official Baseline Picks
_No rows._

## Candidate v2 Picks
_No rows._

## Candidate v7 Decisions
- Waiting: 0
- Confirmed: 0
- Rejected: 0
- Unavailable: 0
_No rows._

## Pre-Lock Timing
| fixture_id | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  | NO_CURRENT_PICKS | NO_BET_DAY |

## Ledger State
| experiment_id | fixture_id | home_team | away_team | market_primary | pipeline_stage | record_status | result_status | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  | PRE | NO_BET_RECORD |  |  |  |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1544652.0 | Sudtirol | Bari | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V4_O25_FIREWALL | 1544652.0 | Sudtirol | Bari | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V5_PLAYER_IMPACT | 1544652.0 | Sudtirol | Bari | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |
| CANDIDATE_V6_API_PREDICTIONS | 1544652.0 | Sudtirol | Bari | OVER_1_5 | POST | PENDING | UNMATCHED | UNMATCHED |  |

## Controller Outputs
- Plan CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.csv
- Plan MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_run_plan.md
- Status MD: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_controller_status.md
