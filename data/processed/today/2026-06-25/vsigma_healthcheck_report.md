# vSIGMA Healthcheck Report - 2026-06-25

- Global health status: WARNING
- Generated at: 2026-06-25T00:12:26.192163+01:00
- Mode: full
- HEALTHY: 31
- WARNING: 4
- NEEDS_ATTENTION: 0
- BROKEN: 0
- NOT_RUN_YET: 2
- First recovery command: `.\.venv\Scripts\python.exe scripts\build_daily_competition_master_report.py --date 2026-06-25`

## Critical Warnings
| check_name | status | detail | recovery_command |
| --- | --- | --- | --- |
| daily_master_report | WARNING | daily master report missing | .\.venv\Scripts\python.exe scripts\build_daily_competition_master_report.py --date 2026-06-25 |
| ledger_target_date_rows | WARNING | ledger has no rows for target date | .\.venv\Scripts\python.exe scripts\update_immutable_daily_ledger.py --date 2026-06-25 --stage PRE |
| freshness_report | WARNING | validation report contains warning rows | .\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-06-25 |
| recent_automation_logs | WARNING | supervisor log directory missing | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-24 --timezone Atlantic/Canary --mode status |

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
| today_snapshot_folder | HEALTHY | today snapshot folder present | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-25 --timezone Atlantic/Canary --mode pre | /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-25 |
| official_baseline_output | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv |
| candidate_output:CANDIDATE_V2 | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v2_competition_top.csv |
| candidate_output:CANDIDATE_V7 | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v7_competition_top.csv |
| candidate_output:CANDIDATE_V7_SHORTLIST | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v7_competition_shortlist.csv |
| candidate_output:CANDIDATE_V4 | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v4_competition_top.csv |
| candidate_output:CANDIDATE_V5 | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v5_competition_top.csv |
| candidate_output:CANDIDATE_V6 | HEALTHY | empty output with headers is valid for NO_BET |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_candidate_v6_competition_top.csv |
| daily_master_report | WARNING | daily master report missing | .\.venv\Scripts\python.exe scripts\build_daily_competition_master_report.py --date 2026-06-25 | /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-25/daily_competition_master_report.md |
| immutable_ledger_exists | HEALTHY | ledger present with 234 row(s) |  | /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv |
| ledger_target_date_rows | WARNING | ledger has no rows for target date | .\.venv\Scripts\python.exe scripts\update_immutable_daily_ledger.py --date 2026-06-25 --stage PRE | /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv |
| ledger_duplicate_ids | HEALTHY | no duplicate ledger_id values for target date |  | /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv |
| freshness_report | WARNING | validation report contains warning rows | .\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-06-25 | /home/runner/work/vsigma/vsigma/data/processed/vsigma_daily_freshness_report.csv |
| candidate_isolation_report | HEALTHY | validation report present without ERROR |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_candidate_isolation_report.csv |
| prelock_freshness | HEALTHY | prelock output present and empty for NO_BET/unavailable state |  | /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_prelock_comparison.csv |
| post_results_status | NOT_RUN_YET | post not required yet or NO_BET official output |  | /home/runner/work/vsigma/vsigma/data/processed/today_post_results_report.csv |
| supervisor_latest_report | HEALTHY | present |  | /home/runner/work/vsigma/vsigma/data/processed/daily_supervisor_latest.md |
| windows_task_registration | NOT_RUN_YET | task registration check unavailable outside Windows | powershell.exe -NoProfile -ExecutionPolicy Bypass -File /home/runner/work/vsigma/vsigma/scripts/register_vsigma_windows_tasks.ps1 |  |
| recent_automation_logs | WARNING | supervisor log directory missing | .\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-24 --timezone Atlantic/Canary --mode status | /home/runner/work/vsigma/vsigma/automation_logs/supervisor |
| disk_space | HEALTHY | free disk space acceptable: 88.16 GB |  |  |
| healthcheck_mode | HEALTHY | full mode completed all quick checks plus environment diagnostics |  |  |
