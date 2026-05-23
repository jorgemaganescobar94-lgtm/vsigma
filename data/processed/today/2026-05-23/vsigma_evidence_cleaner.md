# vSIGMA Evidence Cleaner - 2026-05-23

## Executive Cleaner Summary
- generated_at: 2026-05-23T08:58:33+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 14
- severity_counts: P2=9; P3=5
- action_counts: POST_RESULT_LABELING=5; REBUILD_LEARNING=5; PRELOCK_REBUILD=4
- source_issue_counts: UNRESOLVED_LEDGER_ROWS=5; PRELOCK_CONFIRMATION_REQUIRED=4; NO_SIGNAL=3; UNKNOWN_MARKET=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1378234 | market=AWAY_WIN | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1378237 | market=HOME_WIN | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #3 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1494182 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #4 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1504822 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #5 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=N/A | market=UNKNOWN | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`
- #6 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1494182 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`
- #7 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1494182.0 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`
- #8 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1504822 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`
- #9 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1504822.0 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-23 --timezone Atlantic/Canary --mode post`
- #10 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-23 --timezone Atlantic/Canary`
- #11 | P3 | NO_SIGNAL | fixture=1494182.0 | market=OVER_1_5 | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-23 --timezone Atlantic/Canary`
- #12 | P3 | NO_SIGNAL | fixture=1504822.0 | market=OVER_1_5 | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-23 --timezone Atlantic/Canary`
- #13 | P3 | UNKNOWN_MARKET | fixture=N/A | market=UNKNOWN | field=market_primary | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-23 --timezone Atlantic/Canary`
- #14 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-23 --timezone Atlantic/Canary`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.