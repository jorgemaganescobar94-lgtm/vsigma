# vSIGMA Evidence Action Router - 2026-05-30

## Executive Action Routing Summary
- generated_at: 2026-05-30T09:42:09+01:00
- executive_status: POST_RESULTS_PENDING
- routed_actions: 7
- route_decision_counts: WAIT_FOR_POST_RESULTS=4; REBUILD_AFTER_POST=3
- gate_status_counts: POST_RESULTS_REQUIRED=4; DEPENDENCY_WAIT_POST=3
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #2 | WAIT_FOR_POST_RESULTS | fixture=1535218 | market=OVER_1_5 | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #3 | WAIT_FOR_POST_RESULTS | fixture=1535314 | market=OVER_1_5 | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #4 | WAIT_FOR_POST_RESULTS | fixture=1545409 | market=OVER_1_5 | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #5 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #6 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #7 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.