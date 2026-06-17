# vSIGMA Evidence Action Router - 2026-06-17

## Executive Action Routing Summary
- generated_at: 2026-06-17T03:06:43+01:00
- executive_status: POST_RESULTS_PENDING
- routed_actions: 5
- route_decision_counts: REBUILD_AFTER_POST=3; WAIT_FOR_POST_RESULTS=1; PRELOCK_CONTEXT_MISSING=1
- gate_status_counts: DEPENDENCY_WAIT_POST=3; POST_RESULTS_REQUIRED=1; MANUAL_TIMING_REVIEW=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-17 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #2 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-17 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #3 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-17 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #4 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-17 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #5 | PRELOCK_CONTEXT_MISSING | fixture=1548054 | market=OVER_2_5 | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-17 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.