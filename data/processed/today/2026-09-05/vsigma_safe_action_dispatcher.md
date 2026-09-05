# vSIGMA Safe Action Dispatcher - 2026-09-05

## Executive Dispatcher Summary
- generated_at: 2026-09-05T02:43:39+01:00
- executive_status: WAITING_FOR_POST_RESULTS
- dispatch_actions: 7
- dispatch_status_counts: WAIT_POST_DEPENDENCY=3; MANUAL_TIMING_REVIEW_REQUIRED=3; WAIT_POST_RESULTS=1
- dispatch_allowed_counts: NO=7
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_POST_RESULTS | allowed=NO | fixture=N/A | market=UNKNOWN | phase=post_results | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-09-05 --timezone Atlantic/Canary --mode post` | reason=Post-result command is not safe until fixtures are finished.
- #2 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-09-05 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #3 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-09-05 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #4 | WAIT_POST_DEPENDENCY | allowed=NO | fixture=N/A | market=UNKNOWN | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-09-05 --timezone Atlantic/Canary` | reason=Learning rebuild depends on post-result labeling first.
- #5 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1547770 | market=OVER_1_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-09-05 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.
- #6 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1622620 | market=OVER_2_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-09-05 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.
- #7 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1622621 | market=OVER_2_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-09-05 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.