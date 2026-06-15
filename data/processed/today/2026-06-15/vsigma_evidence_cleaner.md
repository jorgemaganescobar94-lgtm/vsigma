# vSIGMA Evidence Cleaner - 2026-06-15

## Executive Cleaner Summary
- generated_at: 2026-06-15T03:03:06+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 5
- severity_counts: P3=3; P2=2
- action_counts: REBUILD_LEARNING=3; PRELOCK_REBUILD=1; POST_RESULT_LABELING=1
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=1; UNRESOLVED_LEDGER_ROWS=1; NO_SIGNAL=1; UNKNOWN_MARKET=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1548054 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-15 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=N/A | market=UNKNOWN | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-15 --timezone Atlantic/Canary --mode post`
- #3 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-15 --timezone Atlantic/Canary`
- #4 | P3 | UNKNOWN_MARKET | fixture=N/A | market=UNKNOWN | field=market_primary | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-15 --timezone Atlantic/Canary`
- #5 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-15 --timezone Atlantic/Canary`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.