# vSIGMA Evidence Cleaner - 2026-05-24

## Executive Cleaner Summary
- generated_at: 2026-05-24T10:08:21+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 6
- severity_counts: P2=6
- action_counts: PRELOCK_REBUILD=6
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=6
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1379344 | market=BTTS_YES | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1392205 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #3 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1392207 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #4 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1504827 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #5 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1537007 | market=HOME_WIN | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #6 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1545796 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-24 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.