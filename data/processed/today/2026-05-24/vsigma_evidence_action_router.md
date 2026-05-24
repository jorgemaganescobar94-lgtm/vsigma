# vSIGMA Evidence Action Router - 2026-05-24

## Executive Action Routing Summary
- generated_at: 2026-05-24T10:09:19+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- routed_actions: 6
- route_decision_counts: WAIT_FOR_PRELOCK_WINDOW=3; PRELOCK_CONTEXT_MISSING=2; PRELOCK_EXPIRED=1
- gate_status_counts: TIME_GATE_CLOSED=3; MANUAL_TIMING_REVIEW=2; TIME_GATE_EXPIRED=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_PRELOCK_WINDOW | fixture=1392205 | market=OVER_2_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-05-24T15:03:23.400000+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.
- #2 | WAIT_FOR_PRELOCK_WINDOW | fixture=1392207 | market=OVER_2_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-05-24T15:03:21.600000+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.
- #3 | WAIT_FOR_PRELOCK_WINDOW | fixture=1545796 | market=OVER_1_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-05-24T16:33:18+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.
- #4 | PRELOCK_CONTEXT_MISSING | fixture=1379344 | market=BTTS_YES | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.
- #5 | PRELOCK_CONTEXT_MISSING | fixture=1537007 | market=HOME_WIN | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.
- #6 | PRELOCK_EXPIRED | fixture=1504827 | market=OVER_1_5 | gate=TIME_GATE_EXPIRED | phase=post_or_no_action | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Kickoff has already passed; do not treat this as a predictive failure.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.