# vSIGMA Forced API Lineup Bridge to Board - 2026-06-11

## Summary
- board_rows_reviewed: 2
- lineup_confirmed_rows: 2
- lineup_missing_rows: 0
- board_rows_written: 2
- bridge_status_counts: LINEUPS_CONFIRMED_BY_FORCED_API=2
- bridge_action_counts: CLEAR_LINEUPS_INACTIVE_WARNING_KEEP_EXECUTION_LOCK=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Use bridged copy for prelock review/repricing. Do not create picks or stake without separate governed promotion.
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Malaga vs Las Palmas | status=LINEUPS_CONFIRMED_BY_FORCED_API | starters=22 (11-11) | formations=4-2-3-1 / 4-4-2 | decision=NO_BET->NO_BET | permission=NO->NO | action=CLEAR_LINEUPS_INACTIVE_WARNING_KEEP_EXECUTION_LOCK
- Cape Town City vs Magesi | status=LINEUPS_CONFIRMED_BY_FORCED_API | starters=22 (11-11) | formations=4-4-2 / 4-2-3-1 | decision=NO_BET->NO_BET | permission=NO->NO | action=CLEAR_LINEUPS_INACTIVE_WARNING_KEEP_EXECUTION_LOCK

## Guardrails
- This bridge only converts confirmed API lineup snapshots into a coverage signal.
- It does not create picks, stake, canonical board permission, whitelist permission, or automatic execution.
- The canonical board remains locked unless a later governed prelock resolver explicitly promotes it.
