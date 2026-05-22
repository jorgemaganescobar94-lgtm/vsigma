# vSIGMA Evidence Cleaner - 2026-05-22

## Executive Cleaner Summary
- generated_at: 2026-05-22T14:21:02+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 11
- severity_counts: P3=7; P2=4
- action_counts: REBUILD_LEARNING=7; PRELOCK_REBUILD=3; POST_RESULT_LABELING=1
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=3; NO_SIGNAL=3; UNKNOWN_RISK=3; UNRESOLVED_LEDGER_ROWS=1; UNKNOWN_MARKET=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1494177 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1544652 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #3 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1545405 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #4 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=N/A | market=UNKNOWN | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-22 --timezone Atlantic/Canary --mode post`
- #5 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`
- #6 | P3 | NO_SIGNAL | fixture=1494177 | market=OVER_2_5 | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`
- #7 | P3 | NO_SIGNAL | fixture=1544652 | market=OVER_1_5 | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`
- #8 | P3 | UNKNOWN_MARKET | fixture=N/A | market=UNKNOWN | field=market_primary | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`
- #9 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`
- #10 | P3 | UNKNOWN_RISK | fixture=1494177 | market=OVER_2_5 | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`
- #11 | P3 | UNKNOWN_RISK | fixture=1544652 | market=OVER_1_5 | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-22 --timezone Atlantic/Canary`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.