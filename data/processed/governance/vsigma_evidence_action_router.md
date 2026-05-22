# vSIGMA Evidence Action Router - 2026-05-22

## Executive Action Routing Summary
- generated_at: 2026-05-22T14:34:35+01:00
- executive_status: WAITING_FOR_PRELOCK_WINDOW
- routed_actions: 11
- route_decision_counts: REBUILD_AFTER_POST=7; WAIT_FOR_PRELOCK_WINDOW=2; WAIT_FOR_POST_RESULTS=1; PRELOCK_CONTEXT_MISSING=1
- gate_status_counts: DEPENDENCY_WAIT_POST=7; TIME_GATE_CLOSED=2; POST_RESULTS_REQUIRED=1; MANUAL_TIMING_REVIEW=1
- auto_run: NO
- production_change: NO

## Routed Actions
- #1 | WAIT_FOR_PRELOCK_WINDOW | fixture=1494177 | market=OVER_2_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-05-22T15:30:36.600000+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.
- #2 | WAIT_FOR_PRELOCK_WINDOW | fixture=1544652 | market=OVER_1_5 | gate=TIME_GATE_CLOSED | phase=prelock_window_start=2026-05-22T16:30:37.200000+00:00 | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=Fixture is still outside the configured 90-minute PRELOCK window.
- #3 | WAIT_FOR_POST_RESULTS | fixture=N/A | market=UNKNOWN | gate=POST_RESULTS_REQUIRED | phase=post | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode post` | reason=Post-result labeling is only safe after matches are finished.
- #4 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #5 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #6 | REBUILD_AFTER_POST | fixture=N/A | market=UNKNOWN | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #7 | REBUILD_AFTER_POST | fixture=1494177 | market=OVER_2_5 | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #8 | REBUILD_AFTER_POST | fixture=1494177 | market=OVER_2_5 | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #9 | REBUILD_AFTER_POST | fixture=1544652 | market=OVER_1_5 | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #10 | REBUILD_AFTER_POST | fixture=1544652 | market=OVER_1_5 | gate=DEPENDENCY_WAIT_POST | phase=after_post_results | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary` | reason=Learning rebuild should follow post-result labeling to avoid preserving unresolved rows.
- #11 | PRELOCK_CONTEXT_MISSING | fixture=1545405 | market=OVER_2_5 | gate=MANUAL_TIMING_REVIEW | phase=prelock_context_review | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90` | reason=No daily_run_plan row found for this fixture; operator must inspect timing before execution.

## Guardrails
- No command is auto-run by this router.
- No production model behavior is changed.
- The router only determines safe timing/order for future operator or automation steps.