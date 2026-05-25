# vSIGMA Safe Action Dispatcher - 2026-05-25

## Executive Dispatcher Summary
- generated_at: 2026-05-25T13:49:56+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- dispatch_actions: 1
- dispatch_status_counts: WAIT_TIME_GATE=1
- dispatch_allowed_counts: NO=1
- auto_run: NO
- production_change: NO

## Dispatch Queue
- #1 | WAIT_TIME_GATE | allowed=NO | fixture=1545418 | market=OVER_1_5 | phase=wait_prelock_window | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-25 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=PRELOCK time gate is not open yet.

## Guardrails
- This dispatcher never auto-runs commands.
- MANUAL_ONLY means the route is eligible for human-triggered execution, not automatic execution.
- NO means the command is blocked by timing, dependency, missing context, or safety state.
- No production model behavior is changed.