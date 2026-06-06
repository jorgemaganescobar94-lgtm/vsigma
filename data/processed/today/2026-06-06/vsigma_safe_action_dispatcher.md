# vSIGMA Safe Action Dispatcher - 2026-06-06

## Executive Dispatcher Summary
- generated_at: 2026-06-06T10:13:27+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- dispatch_actions: 6
- dispatch_status_counts: WAIT_POST_DEPENDENCY=3; WAIT_POST_RESULTS=2; WAIT_TIME_GATE=1
- dispatch_allowed_counts: NO=6
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_TIME_GATE | allowed=NO | fixture=1548052 | market=OVER_2_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-06 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.
- #2 | WAIT_POST_RESULTS | allowed=NO | fixture=N/A | market=UNKNOWN | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-06 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #3 | WAIT_POST_RESULTS | allowed=NO | fixture=1548052 | market=OVER_2_5 | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-06 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #4 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-06 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #5 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-06 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #6 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-06 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.