# vSIGMA Evidence Action Router - 2026-05-28

## Executive Action Routing Summary
- generated_at: 2026-05-28T13:48:33+01:00
- executive_status: POST_RESULTS_PENDING
- routed_actions: 10
- route_decision_counts: WAIT_FOR_POST_RESULTS=5; REBUILD_AFTER_POST=3; PRELOCK_CONTEXT_MISSING=2
- gate_status_counts: POST_RESULTS_REQUIRED=5; DEPENDENCY_WAIT_POST=3; MANUAL_TIMING_REVIEW=2
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #2 | WAIT_FOR_POST_RESULTS | fixture=1535316 | market=OVER_1_5 | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #3 | WAIT_FOR_POST_RESULTS | fixture=1535327 | market=BTTS_YES | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #4 | WAIT_FOR_POST_RESULTS | fixture=1535327 | market=BTTS_YES | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #5 | WAIT_FOR_POST_RESULTS | fixture=1545404 | market=AWAY_WIN | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #6 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-28 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #7 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-28 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #8 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-28 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #9 | PRELOCK_CONTEXT_MISSING | fixture=1535315 | market=OVER_2_5 | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.
- #10 | PRELOCK_CONTEXT_MISSING | fixture=1535327 | market=BTTS_YES | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.