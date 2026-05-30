# vSIGMA Evidence Cleaner - 2026-05-30

## Executive Cleaner Summary
- generated_at: 2026-05-30T09:42:00+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 7
- severity_counts: P2=4; P3=3
- action_counts: POST_RESULT_LABELING=4; REBUILD_LEARNING=3
- source_issue_counts: UNRESOLVED_LEDGER_ROWS=4; NO_SIGNAL=1; UNKNOWN_MARKET=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=N/A | market=UNKNOWN | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post`
- #2 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1535218 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post`
- #3 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1535314 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post`
- #4 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=1545409 | market=OVER_1_5 | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-30 --timezone Atlantic/Canary --mode post`
- #5 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary`
- #6 | P3 | UNKNOWN_MARKET | fixture=N/A | market=UNKNOWN | field=market_primary | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary`
- #7 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-30 --timezone Atlantic/Canary`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.