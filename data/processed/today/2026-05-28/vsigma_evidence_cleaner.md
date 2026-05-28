# vSIGMA Evidence Cleaner - 2026-05-28

## Executive Cleaner Summary
- generated_at: 2026-05-28T13:47:56+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 10
- severity_counts: P2=7; P3=3
- action_counts: POST_RESULT_LABELING=5; REBUILD_LEARNING=3; PRELOCK_REBUILD=2
- source_issue_counts: PENDING_MARKET_RESULTS=4; PRELOCK_CONFIRMATION_REQUIRED=2; UNRESOLVED_LEDGER_ROWS=1; NO_SIGNAL=1; UNKNOWN_MARKET=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PENDING_MARKET_RESULTS | fixture=1535316 | market=OVER_1_5 | field=primary_result | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post`
- #2 | P2 | PENDING_MARKET_RESULTS | fixture=1535327 | market=BTTS_YES | field=actionable_result | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post`
- #3 | P2 | PENDING_MARKET_RESULTS | fixture=1535327 | market=BTTS_YES | field=primary_result | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post`
- #4 | P2 | PENDING_MARKET_RESULTS | fixture=1545404 | market=AWAY_WIN | field=primary_result | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post`
- #5 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1535315 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #6 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1535327 | market=BTTS_YES | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #7 | P2 | UNRESOLVED_LEDGER_ROWS | fixture=N/A | market=UNKNOWN | field=result_status | action=POST_RESULT_LABELING | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-28 --timezone Atlantic/Canary --mode post`
- #8 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-28 --timezone Atlantic/Canary`
- #9 | P3 | UNKNOWN_MARKET | fixture=N/A | market=UNKNOWN | field=market_primary | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-28 --timezone Atlantic/Canary`
- #10 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | action=REBUILD_LEARNING | command=`.\.venv\Scripts\python.exe scripts\build_learning_ledger.py --date 2026-05-28 --timezone Atlantic/Canary`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.