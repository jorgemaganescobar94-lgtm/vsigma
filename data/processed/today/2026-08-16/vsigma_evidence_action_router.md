# vSIGMA Evidence Action Router - 2026-08-16

## Executive Action Routing Summary
- generated_at: 2026-08-16T00:59:46+01:00
- executive_status: ROUTED_REVIEW_ONLY
- routed_actions: 1
- route_decision_counts: PRELOCK_CONTEXT_MISSING=1
- gate_status_counts: MANUAL_TIMING_REVIEW=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | PRELOCK_CONTEXT_MISSING | fixture=1607197 | market=OVER_1_5 | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-08-16 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.