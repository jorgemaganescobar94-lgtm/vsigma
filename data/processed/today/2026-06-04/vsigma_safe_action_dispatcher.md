# vSIGMA Safe Action Dispatcher - 2026-06-04

## Executive Dispatcher Summary
- generated_at: 2026-06-04T12:35:19+01:00
- executive_status: WAITING_FOR_POST_RESULTS
- dispatch_actions: 4
- dispatch_status_counts: WAIT_POST_DEPENDENCY=3; WAIT_POST_RESULTS=1
- dispatch_allowed_counts: NO=4
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_POST_RESULTS | allowed=NO | fixture=N/A | market=UNKNOWN | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-04 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #2 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-04 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #3 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-04 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #4 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-04 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.