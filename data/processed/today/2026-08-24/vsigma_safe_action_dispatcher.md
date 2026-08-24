# vSIGMA Safe Action Dispatcher - 2026-08-24

## Executive Dispatcher Summary
- generated_at: 2026-08-24T01:33:32+01:00
- executive_status: DISPATCH_REVIEW_ONLY
- dispatch_actions: 3
- dispatch_status_counts: MANUAL_TIMING_REVIEW_REQUIRED=3
- dispatch_allowed_counts: NO=3
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1547770 | market=OVER_1_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-08-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.
- #2 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1622620 | market=OVER_2_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-08-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.
- #3 | MANUAL_TIMING_REVIEW_REQUIRED | allowed=NO | fixture=1622621 | market=OVER_2_5 | phase=manual_timing_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-08-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Daily run plan lacks timing context; operator must inspect before dispatch.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.