# vSIGMA Evidence Action Router - 2026-05-25

## Executive Action Routing Summary
- generated_at: 2026-05-25T13:48:19+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- routed_actions: 1
- route_decision_counts: WAIT_FOR_PRELOCK_WINDOW=1
- gate_status_counts: TIME_GATE_CLOSED=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_PRELOCK_WINDOW | fixture=1545418 | market=OVER_1_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-05-25T17:01:02.600000+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-25 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.