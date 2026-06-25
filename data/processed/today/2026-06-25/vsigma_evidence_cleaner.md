# vSIGMA Evidence Cleaner - 2026-06-25

## Executive Cleaner Summary
- generated_at: 2026-06-25T02:35:16+01:00
- executive_status: P2_EVIDENCE_CLEANING_REQUIRED
- cleaner_actions: 1
- severity_counts: P2=1
- action_counts: PRELOCK_REBUILD=1
- source_issue_counts: PRELOCK_CONFIRMATION_REQUIRED=1
- auto_fix: NO
- production_change: NO

## Prioritized Cleaning Plan
- #1 | P2 | PRELOCK_CONFIRMATION_REQUIRED | fixture=1548054 | market=OVER_2_5 | field=lineup_activation_state | action=PRELOCK_REBUILD | command=`.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-06-25 --timezone Atlantic/Canary --mode prelock --window-minutes 90`

## Guardrails
- No auto-fix is applied.
- No production model behavior is changed.
- This report only tells the operator or next automation what should be cleaned first.