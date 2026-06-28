# vSIGMA Forced API Board Fixture Lineups Refresh - 2026-06-28

## Summary
- fixtures_reviewed: 1
- api_calls_planned: 1
- api_calls_executed: 1
- lineup_fixtures_found: 0
- lineup_fixtures_missing: 1
- starting_xi_rows: 0
- substitute_rows: 0
- api_status_counts: API_ERROR=1
- team_side_counts: none=1
- provider_counts: API-SPORTS_DIRECT=1
- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- auto_apply: NO
- production_change: NO

## Fixture Lineup Status
- NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | fixture_id=DIAGNOSTIC_EMPTY_BY_PROMOTION_GATE | status=API_ERROR | starters=0 | subs=0 | note=API-SPORTS_DIRECT API errors: {'fixture': 'The Fixture field must contain an integer.'}

## Starting XI Rows
- none.

## Guardrails
- This is a direct API-Football lineup snapshot using canonical board fixture_id.
- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.
- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.
