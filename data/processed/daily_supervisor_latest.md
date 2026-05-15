# vSIGMA Daily Supervisor Report - 2026-05-15

- Mode run: prelock-check
- Status: PASS
- Detail: NO_PRELOCK_DUE
- Next recommended action: WAIT_FOR_PRELOCK
- Next recommended command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-15 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- Logs path: C:\vsigma\automation_logs\supervisor
- Stale warnings: NONE
- Ledger update status: PRE_UPDATED
- Scheduled automation status: vSIGMA PRE Daily=NOT_REGISTERED; vSIGMA PRELOCK Check=NOT_REGISTERED; vSIGMA POST Daily=NOT_REGISTERED; vSIGMA POST Backup Yesterday=NOT_REGISTERED

## Commands Executed
| label | exit_code | status | log_path | command |
| --- | --- | --- | --- | --- |
| master_report | 0 | PASS | C:\vsigma\automation_logs\supervisor\2026-05-15_prelock_check_20260515T150204_master_report.log | C:\vsigma\.venv\Scripts\python.exe scripts/build_daily_competition_master_report.py --date 2026-05-15 --processed-dir C:\vsigma\data\processed --snapshot-dir C:\vsigma\data\processed\today\2026-05-15 |

## Current Plan
| fixture_id | league | home_team | away_team | market_primary | kickoff_time | minutes_to_kickoff | prelock_window_start | prelock_status | recommended_next_action | recommended_command |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544651 | Serie B | Bari | Sudtirol | OVER_1_5 | 2026-05-15T18:00:29.200000+00:00 | 238.43 | 2026-05-15T16:30:29.200000+00:00 | PENDING_OUTSIDE_WINDOW | WAIT_FOR_PRELOCK | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-15 --timezone Atlantic/Canary --mode prelock --window-minutes 90 |
