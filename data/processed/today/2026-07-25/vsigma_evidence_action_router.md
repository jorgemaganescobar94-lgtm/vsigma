# vSIGMA Evidence Action Router - 2026-07-25

## Executive Action Routing Summary
- generated_at: 2026-07-25T02:13:46+01:00
- executive_status: ROUTED_REVIEW_ONLY
- routed_actions: 3
- route_decision_counts: PRELOCK_CONTEXT_MISSING=3
- gate_status_counts: MANUAL_TIMING_REVIEW=3
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | PRELOCK_CONTEXT_MISSING | fixture=1494212 | market=AWAY_WIN | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-25 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.
- #2 | PRELOCK_CONTEXT_MISSING | fixture=1494213 | market=BTTS_YES | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-25 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.
- #3 | PRELOCK_CONTEXT_MISSING | fixture=1507002 | market=HOME_WIN | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-25 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.