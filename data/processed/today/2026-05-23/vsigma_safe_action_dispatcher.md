# vSIGMA Safe Action Dispatcher - 2026-05-23

## Executive Dispatcher Summary
- generated_at: 2026-05-23T08:59:04+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- dispatch_actions: 11
- dispatch_status_counts: WAIT_POST_DEPENDENCY=7; WAIT_TIME_GATE=2; WAIT_POST_RESULTS=1; MANUAL_TIMING_REVIEW_REQUIRED=1
- dispatch_allowed_counts: NO=11
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_TIME_GATE | allowed=NO | fixture=1494177 | market=OVER_2_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.
- #2 | WAIT_TIME_GATE | allowed=NO | fixture=1544652 | market=OVER_1_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.
- #3 | WAIT_POST_RESULTS | allowed=NO | fixture=N/A | market=UNKNOWN | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #4 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #5 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #6 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #7 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=1494177 | market=OVER_2_5 | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #8 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=1494177 | market=OVER_2_5 | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #9 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=1544652 | market=OVER_1_5 | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #10 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=1544652 | market=OVER_1_5 | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #11 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1545405 | market=OVER_2_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.