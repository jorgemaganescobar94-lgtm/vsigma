# vSIGMA Healthcheck Report - 2026-06-08

- Global health status: WARNING
- Generated at: 2026-06-08T13:51:43.596400+01:00
- Mode: full
- HEALTHY: 24
- WARNING: 4
- NEEDS_ATTENTION: 0
- BROKEN: 0
- NOT_RUN_YET: 9
- First recovery command: `.\.venv\Scripts\python.exe scripts\update_immutable_daily_ledger.py --date 2026-06-08 --stage PRE`

## Critical Warnings
| check_name | status | detail | recovery_command |
| --- | --- | --- | --- |
| ledger_target_date_rows | WARNING | ledger has no rows for target date | .\.venv\Scripts\python.exe scripts\update_immutable_daily_ledger.py --date 2026-06-08 --stage PRE |
| freshness_report | WARNING | validation report missing | .\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-06-08 |
| candidate_isolation_report | WARNING | validation report missing | .\.venv\Scripts\python.exe scripts\validate_candidate_isolation.py --date 2026-06-08 |
| recent_automation_logs | WARNING | supervisor log directory missing | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode status |

## All Checks
| check_name | status | detail | recovery_command | evidence_path |
| --- | --- | --- | --- | --- |
| project_root_exists | HEALTHY | project root present |  | /home/runner/work/vsigma/vsigma |
| venv_python_exists | HEALTHY | cloud runner python active; local .venv not required: /opt/hostedtoolcache/Python/3.11.15/x64/bin/python |  | /opt/hostedtoolcache/Python/3.11.15/x64/bin/python |
| data_raw_exists | HEALTHY | data/raw present | Create data\raw or run the raw data fetch pipeline. | /home/runner/work/vsigma/vsigma/data/raw |
| data_processed_exists | HEALTHY | data/processed present | Create data\processed or run the PRE pipeline. | /home/runner/work/vsigma/vsigma/data/processed |
| required_script:scripts/run_daily_competition_controller.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/run_daily_competition_controller.py |
| required_script:scripts/run_daily_competition_supervisor.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/run_daily_competition_supervisor.py |
| required_script:scripts/run_today_prelock_orchestrator.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/run_today_prelock_orchestrator.py |
| required_script:scripts/run_today_post_results_pipeline.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/run_today_post_results_pipeline.py |
| required_script:scripts/update_immutable_daily_ledger.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/update_immutable_daily_ledger.py |
| required_script:scripts/build_daily_competition_master_report.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/build_daily_competition_master_report.py |
| required_script:scripts/build_promotion_threshold_governance.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/build_promotion_threshold_governance.py |
| required_script:scripts/validate_daily_output_freshness.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/validate_daily_output_freshness.py |
| required_script:scripts/validate_candidate_isolation.py | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/validate_candidate_isolation.py |
| required_script:scripts/register_vsigma_windows_tasks.ps1 | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/register_vsigma_windows_tasks.ps1 |
| required_script:scripts/unregister_vsigma_windows_tasks.ps1 | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/scripts/unregister_vsigma_windows_tasks.ps1 |
| api_config_available | HEALTHY | API configuration detected without exposing secrets | Set API_FOOTBALL_KEY, APISPORTS_KEY, RAPIDAPI_KEY, or X_RAPIDAPI_KEY in .env/environment. | /home/runner/work/vsigma/vsigma/.env |
| today_snapshot_folder | HEALTHY | today snapshot folder present | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-08 |
| official_baseline_output | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv |
| candidate_output:CANDIDATE_V2 | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v2_competition_top.csv |
| candidate_output:CANDIDATE_V7 | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v7_competition_top.csv |
| candidate_output:CANDIDATE_V7_SHORTLIST | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v7_competition_shortlist.csv |
| candidate_output:CANDIDATE_V4 | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v4_competition_top.csv |
| candidate_output:CANDIDATE_V5 | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v5_competition_top.csv |
| candidate_output:CANDIDATE_V6 | NOT_RUN_YET | output not available yet | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v6_competition_top.csv |
| daily_master_report | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-08/daily_competition_master_report.md |
| immutable_ledger_exists | HEALTHY | ledger present with 174 row(s) |  | /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv |
| ledger_target_date_rows | WARNING | ledger has no rows for target date | .\.venv\Scripts\python.exe scripts\update_immutable_daily_ledger.py --date 2026-06-08 --stage PRE | /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv |
| ledger_duplicate_ids | HEALTHY | no duplicate ledger_id values for target date |  | /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv |
| freshness_report | WARNING | validation report missing | .\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-06-08 | /home/runner/work/vsigma/vsigma/data/processed/vsigma_daily_freshness_report.csv |
| candidate_isolation_report | WARNING | validation report missing | .\.venv\Scripts\python.exe scripts\validate_candidate_isolation.py --date 2026-06-08 | /home/runner/work/vsigma/vsigma/data/processed/vsigma_candidate_isolation_report.csv |
| prelock_freshness | HEALTHY | prelock output present and empty for NO_BET/unavailable state |  | /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-08/vsigma_today_prelock_comparison.csv |
| post_results_status | NOT_RUN_YET | post not required yet or NO_BET official output |  | /home/runner/work/vsigma/vsigma/data/processed/today_post_results_report.csv |
| supervisor_latest_report | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/data/processed/daily_supervisor_latest.md |
| windows_task_registration | NOT_RUN_YET | task registration check unavailable outside Windows | powershell.exe -NoProfile -ExecutionPolicy Bypass -File /home/runner/work/vsigma/vsigma/scripts/register_vsigma_windows_tasks.ps1 |  |
| recent_automation_logs | WARNING | supervisor log directory missing | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-08 --timezone Atlantic/Canary --mode status | /home/runner/work/vsigma/vsigma/automation_logs/supervisor |
| disk_space | HEALTHY | free disk space acceptable: 15.98 GB |  |  |
| healthcheck_mode | HEALTHY | full mode completed all quick checks plus environment diagnostics |  |  |
