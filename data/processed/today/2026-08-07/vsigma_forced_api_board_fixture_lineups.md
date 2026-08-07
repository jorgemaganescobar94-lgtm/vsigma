# vSIGMA Forced API Board Fixture Lineups Refresh - 2026-08-07

## Summary
- fixtures_reviewed: 1
- api_calls_planned: 1
- api_calls_executed: 1
- lineup_fixtures_found: 1
- lineup_fixtures_missing: 0
- starting_xi_rows: 22
- substitute_rows: 18
- api_status_counts: OK=40
- team_side_counts: home=20; away=20
- provider_counts: API-SPORTS_DIRECT=40
- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- auto_apply: NO
- production_change: NO

## Fixture Lineup Status
- Dundee Utd vs Rangers | fixture_id=1556628 | status=OK | starters=22 | subs=18 | note=lineups fetched directly by fixture_id

## Starting XI Rows
- home | Dundee Utd | 4-3-3 | #1 Jack James Walton | pos=G | grid=1:1
- home | Dundee Utd | 4-3-3 | #23 Joshua Rawlins | pos=D | grid=2:4
- home | Dundee Utd | 4-3-3 | #3 Bert Esselink | pos=D | grid=2:3
- home | Dundee Utd | 4-3-3 | #18 Michael Forbes | pos=D | grid=2:2
- home | Dundee Utd | 4-3-3 | #11 William Ferry | pos=D | grid=2:1
- home | Dundee Utd | 4-3-3 | #5 Vicko Ševelj | pos=M | grid=3:3
- home | Dundee Utd | 4-3-3 | #10 Dylan Tait | pos=M | grid=3:2
- home | Dundee Utd | 4-3-3 | #12 Emmanuel Agyei | pos=M | grid=3:1
- home | Dundee Utd | 4-3-3 | #21 Jesse Randall | pos=F | grid=4:3
- home | Dundee Utd | 4-3-3 | #15 Lachlan Rose | pos=F | grid=4:2
- home | Dundee Utd | 4-3-3 | #9 Zachary Sapsford | pos=F | grid=4:1
- away | Rangers | 4-2-3-1 | #1 Ivor Pandur | pos=G | grid=1:1
- away | Rangers | 4-2-3-1 | #21 Dujon Sterling | pos=D | grid=2:4
- away | Rangers | 4-2-3-1 | #4 Ben Godfrey | pos=D | grid=2:3
- away | Rangers | 4-2-3-1 | #37 Emmanuel Fernandez | pos=D | grid=2:2
- away | Rangers | 4-2-3-1 | #25 Tuur Rommens | pos=D | grid=2:1
- away | Rangers | 4-2-3-1 | #10 Mohammed Diomande | pos=M | grid=3:2
- away | Rangers | 4-2-3-1 | #14 Cameron Devlin | pos=M | grid=3:1
- away | Rangers | 4-2-3-1 | #20 Ryan Don Naderi | pos=M | grid=4:3
- away | Rangers | 4-2-3-1 | #11 Thelo Aasgaard | pos=M | grid=4:2
- away | Rangers | 4-2-3-1 | #23 Djeidi Gassama | pos=M | grid=4:1
- away | Rangers | 4-2-3-1 | #7 Lawrence Shankland | pos=F | grid=5:1

## Guardrails
- This is a direct API-Football lineup snapshot using canonical board fixture_id.
- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.
- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.
