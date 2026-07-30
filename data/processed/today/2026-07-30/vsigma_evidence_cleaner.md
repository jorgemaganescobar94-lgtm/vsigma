# vSIGMA Evidence Cleaner - 2026-07-30

## Executive Cleaner Summary
- generated_at: 2026-07-30T01:59:46+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 4
- severity_counts: P2=4
- action_counts: PRELOCK_REBUILD=4
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=4
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1492307 | market=OVER_1_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-30 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #2 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1494217 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-30 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #3 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1494709 | market=AWAY_WIN | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-30 --timezone Atlantic/Canary --mode prelock --window-minutes 90`
- #4 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1494711 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-07-30 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.