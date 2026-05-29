# vSIGMA Evidence Action Router - 2026-05-29

## Executive Action Routing Summary
- generated_at: 2026-05-29T12:58:34+01:00
- executive_status: PRELOCK_ACTION_READY
- routed_actions: 3
- route_decision_counts: RUN_PRELOCK_NOW=2; PRELOCK_CONTEXT_MISSING=1
- gate_status_counts: TIME_GATE_OPEN=2; MANUAL_TIMING_REVIEW=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | RUN_PRELOCK_NOW | fixture=1535218 | market=OVER_1_5 | gate=TIME_GATE_OPEN | phase=prelock | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is inside the configured PRELOCK window or close enough for confirmation.
- #2 | RUN_PRELOCK_NOW | fixture=1535314 | market=OVER_1_5 | gate=TIME_GATE_OPEN | phase=prelock | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is inside the configured PRELOCK window or close enough for confirmation.
- #3 | PRELOCK_CONTEXT_MISSING | fixture=1545797 | market=OVER_2_5 | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.