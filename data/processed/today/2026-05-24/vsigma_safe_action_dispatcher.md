# vSIGMA Safe Action Dispatcher - 2026-05-24

## Executive Dispatcher Summary
- generated_at: 2026-05-24T10:09:38+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- dispatch_actions: 6
- dispatch_status_counts: WAIT_TIME_GATE=3; MANUAL_TIMING_REVIEW_REQUIRED=2; NO_DISPATCH_EXPIRED=1
- dispatch_allowed_counts: NO=6
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_TIME_GATE | allowed=NO | fixture=1392205 | market=OVER_2_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.
- #2 | WAIT_TIME_GATE | allowed=NO | fixture=1392207 | market=OVER_2_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.
- #3 | WAIT_TIME_GATE | allowed=NO | fixture=1545796 | market=OVER_1_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.
- #4 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1379344 | market=BTTS_YES | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.
- #5 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1537007 | market=HOME_WIN | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.
- #6 | NO_DISPATCH_EXPIRED | allowed=NO | fixture=1504827 | market=OVER_1_5 | phase=expired_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Prelock opportunity has expired; do not execute as if it were live.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.