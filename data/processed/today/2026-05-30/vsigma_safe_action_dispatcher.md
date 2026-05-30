# vSIGMA Safe Action Dispatcher - 2026-05-30

## Executive Dispatcher Summary
- generated_at: 2026-05-30T09:42:56+01:00
- executive_status: WAITING_FOR_POST_RESULTS
- dispatch_actions: 7
- dispatch_status_counts: WAIT_POST_RESULTS=4; WAIT_POST_DEPENDENCY=3
- dispatch_allowed_counts: NO=7
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_POST_RESULTS | allowed=NO | fixture=N/A | market=UNKNOWN | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #2 | WAIT_POST_RESULTS | allowed=NO | fixture=1535218 | market=OVER_1_5 | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #3 | WAIT_POST_RESULTS | allowed=NO | fixture=1535314 | market=OVER_1_5 | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #4 | WAIT_POST_RESULTS | allowed=NO | fixture=1545409 | market=OVER_1_5 | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #5 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #6 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #7 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.