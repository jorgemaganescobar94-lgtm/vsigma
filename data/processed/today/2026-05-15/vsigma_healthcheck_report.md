# vSIGMA Healthcheck Report - 2026-05-15

- Global health status: WARNING
- Generated at: 2026-05-15T15:14:02.442494+01:00
- Mode: full
- HEALTHY: 34
- WARNING: 3
- NEEDS_ATTENTION: 0
- BROKEN: 0
- NOT_RUN_YET: 0
- First recovery command: `.\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-15`

## Critical Warnings
| check_name | status | detail | recovery_command |
| --- | --- | --- | --- |
| freshness_report | WARNING | validation report contains warning rows | .\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-15 |
| post_results_status | WARNING | post-results report missing while official picks exist | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-15 --timezone Atlantic/Canary --mode post |
| windows_task_registration | WARNING | vSIGMA PRE Daily=NOT_REGISTERED; vSIGMA PRELOCK Check=NOT_REGISTERED; vSIGMA POST Daily=NOT_REGISTERED; vSIGMA POST Backup Yesterday=NOT_REGISTERED | powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\vsigma\scripts\register_vsigma_windows_tasks.ps1 |

## All Checks
| check_name | status | detail | recovery_command | evidence_path |
| --- | --- | --- | --- | --- |
| project_root_exists | HEALTHY | project root present |  | C:\vsigma |
| venv_python_exists | HEALTHY | .venv Python present | Create or repair .venv, then install project requirements. | C:\vsigma\.venv\Scripts\python.exe |
| data_raw_exists | HEALTHY | data/raw present | Create data\raw or run the raw data fetch pipeline. | C:\vsigma\data\raw |
| data_processed_exists | HEALTHY | data/processed present | Create data\processed or run the PRE pipeline. | C:\vsigma\data\processed |
| required_script:scripts/run_daily_competition_controller.py | HEALTHY | present |  | C:\vsigma\scripts\run_daily_competition_controller.py |
| required_script:scripts/run_daily_competition_supervisor.py | HEALTHY | present |  | C:\vsigma\scripts\run_daily_competition_supervisor.py |
| required_script:scripts/run_today_prelock_orchestrator.py | HEALTHY | present |  | C:\vsigma\scripts\run_today_prelock_orchestrator.py |
| required_script:scripts/run_today_post_results_pipeline.py | HEALTHY | present |  | C:\vsigma\scripts\run_today_post_results_pipeline.py |
| required_script:scripts/update_immutable_daily_ledger.py | HEALTHY | present |  | C:\vsigma\scripts\update_immutable_daily_ledger.py |
| required_script:scripts/build_daily_competition_master_report.py | HEALTHY | present |  | C:\vsigma\scripts\build_daily_competition_master_report.py |
| required_script:scripts/build_promotion_threshold_governance.py | HEALTHY | present |  | C:\vsigma\scripts\build_promotion_threshold_governance.py |
| required_script:scripts/validate_daily_output_freshness.py | HEALTHY | present |  | C:\vsigma\scripts\validate_daily_output_freshness.py |
| required_script:scripts/validate_candidate_isolation.py | HEALTHY | present |  | C:\vsigma\scripts\validate_candidate_isolation.py |
| required_script:scripts/register_vsigma_windows_tasks.ps1 | HEALTHY | present |  | C:\vsigma\scripts\register_vsigma_windows_tasks.ps1 |
| required_script:scripts/unregister_vsigma_windows_tasks.ps1 | HEALTHY | present |  | C:\vsigma\scripts\unregister_vsigma_windows_tasks.ps1 |
| api_config_available | HEALTHY | API configuration detected without exposing secrets | Set API_FOOTBALL_KEY, APISPORTS_KEY, RAPIDAPI_KEY, or X_RAPIDAPI_KEY in .env/environment. | C:\vsigma\.env |
| today_snapshot_folder | HEALTHY | today snapshot folder present | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-15 --timezone Atlantic/Canary --mode pre | C:\vsigma\data\processed\today\2026-05-15 |
| official_baseline_output | HEALTHY | present with 1 row(s) |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_competition_top.csv |
| candidate_output:CANDIDATE_V2 | HEALTHY | present with 1 row(s) |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_candidate_v2_competition_top.csv |
| candidate_output:CANDIDATE_V7 | HEALTHY | empty output with headers is valid for NO_BET |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_candidate_v7_competition_top.csv |
| candidate_output:CANDIDATE_V7_SHORTLIST | HEALTHY | present with 1 row(s) |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_candidate_v7_competition_shortlist.csv |
| candidate_output:CANDIDATE_V4 | HEALTHY | present with 1 row(s) |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_candidate_v4_competition_top.csv |
| candidate_output:CANDIDATE_V5 | HEALTHY | present with 1 row(s) |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_candidate_v5_competition_top.csv |
| candidate_output:CANDIDATE_V6 | HEALTHY | present with 1 row(s) |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_candidate_v6_competition_top.csv |
| daily_master_report | HEALTHY | present |  | C:\vsigma\data\processed\today\2026-05-15\daily_competition_master_report.md |
| immutable_ledger_exists | HEALTHY | ledger present with 19 row(s) |  | C:\vsigma\data\processed\ledger\vsigma_immutable_daily_pick_ledger.csv |
| ledger_target_date_rows | HEALTHY | 7 row(s) for target date |  | C:\vsigma\data\processed\ledger\vsigma_immutable_daily_pick_ledger.csv |
| ledger_duplicate_ids | HEALTHY | no duplicate ledger_id values for target date |  | C:\vsigma\data\processed\ledger\vsigma_immutable_daily_pick_ledger.csv |
| freshness_report | WARNING | validation report contains warning rows | .\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-15 | C:\vsigma\data\processed\today\2026-05-15\vsigma_daily_freshness_report.csv |
| candidate_isolation_report | HEALTHY | validation report present without ERROR |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_candidate_isolation_report.csv |
| prelock_freshness | HEALTHY | prelock output present and empty for NO_BET/unavailable state |  | C:\vsigma\data\processed\today\2026-05-15\vsigma_today_prelock_comparison.csv |
| post_results_status | WARNING | post-results report missing while official picks exist | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-15 --timezone Atlantic/Canary --mode post | C:\vsigma\data\processed\today_post_results_report.csv |
| supervisor_latest_report | HEALTHY | present |  | C:\vsigma\data\processed\daily_supervisor_latest.md |
| windows_task_registration | WARNING | vSIGMA PRE Daily=NOT_REGISTERED; vSIGMA PRELOCK Check=NOT_REGISTERED; vSIGMA POST Daily=NOT_REGISTERED; vSIGMA POST Backup Yesterday=NOT_REGISTERED | powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\vsigma\scripts\register_vsigma_windows_tasks.ps1 |  |
| recent_automation_logs | HEALTHY | latest log: C:\vsigma\automation_logs\supervisor\2026-05-15_prelock_check_20260515T150204_master_report.log |  | C:\vsigma\automation_logs\supervisor\2026-05-15_prelock_check_20260515T150204_master_report.log |
| disk_space | HEALTHY | free disk space acceptable: 78.31 GB |  |  |
| healthcheck_mode | HEALTHY | full mode completed all quick checks plus environment diagnostics |  |  |
