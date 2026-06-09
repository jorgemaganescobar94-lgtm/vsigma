# vSIGMA Evidence Action Router - 2026-06-09

## Executive Action Routing Summary
- generated_at: 2026-06-09T12:43:04+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- routed_actions: 6
- route_decision_counts: REBUILD_AFTER_POST=3; WAIT_FOR_POST_RESULTS=2; WAIT_FOR_PRELOCK_WINDOW=1
- gate_status_counts: DEPENDENCY_WAIT_POST=3; POST_RESULTS_REQUIRED=2; TIME_GATE_CLOSED=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_PRELOCK_WINDOW | fixture=1548054 | market=OVER_2_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-06-09T17:30:18+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-09 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.
- #2 | WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-09 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #3 | WAIT_FOR_POST_RESULTS | fixture=1548054 | market=OVER_2_5 | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-09 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #4 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-09 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #5 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-09 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #6 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-09 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.