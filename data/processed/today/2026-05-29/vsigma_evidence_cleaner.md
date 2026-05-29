# vSIGMA Evidence Cleaner - 2026-05-29

## Executive Cleaner Summary
- generated_at: 2026-05-29T12:57:54+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 3
- severity_counts: P2=3
- action_counts: PRELOCK_REBUILD=3
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=3
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1535218 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1535314 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #3 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1545797 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-29 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.