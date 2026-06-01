# vSIGMA Evidence Cleaner - 2026-06-01

## Executive Cleaner Summary
- generated_at: 2026-06-01T20:27:29+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 8
- severity_counts: P2=5; P3=3
- action_counts: PRELOCK_REBUILD=4; REBUILD_LEARNING=3; POST_RESULT_LABELING=1
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=4; UNRESOLVED_LEDGER_ROWS=1; NO_SIGNAL=1; UNKNOWN_MARKET=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1392217 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-01 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1392220 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-01 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #3 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1492282 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-01 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #4 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1492289 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-01 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #5 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=N/A | market=UNKNOWN | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-01 --timezone Atlantic/Canary --mode post`
- #6 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-01 --timezone Atlantic/Canary`
- #7 | P3 | UNKNOWN_MARKET | fixture=N/A | market=UNKNOWN | field=market_primary | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-01 --timezone Atlantic/Canary`
- #8 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-06-01 --timezone Atlantic/Canary`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.