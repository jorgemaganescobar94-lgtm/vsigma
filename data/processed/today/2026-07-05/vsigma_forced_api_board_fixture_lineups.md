# vSIGMA Forced API Board Fixture Lineups Refresh - 2026-07-05

## Summary
- fixtures_reviewed: 1
- api_calls_planned: 2
- api_calls_executed: 2
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
- Degerfors IF vs Malmo FF | fixture_id=1494194 | status=OK | starters=22 | subs=18 | note=lineups fetched directly by fixture_id

## Starting XI Rows
- home | Degerfors IF | 4-4-2 | #38 Matvei Igonen | pos=G | grid=1:1
- home | Degerfors IF | 4-4-2 | #6 Daniel Sundgren | pos=D | grid=2:4
- home | Degerfors IF | 4-4-2 | #7 Sebastian Ohlsson | pos=D | grid=2:3
- home | Degerfors IF | 4-4-2 | #16 Sebastian Ohlsson | pos=D | grid=2:2
- home | Degerfors IF | 4-4-2 | #18 Samba Diatara | pos=D | grid=2:1
- home | Degerfors IF | 4-4-2 | #22 Nahom Girmai | pos=M | grid=3:4
- home | Degerfors IF | 4-4-2 | #8 Bilal Hussein | pos=M | grid=3:3
- home | Degerfors IF | 4-4-2 | #4 Kazper Karlsson | pos=M | grid=3:2
- home | Degerfors IF | 4-4-2 | #20 Elias Barsoum | pos=M | grid=3:1
- home | Degerfors IF | 4-4-2 | #17 Arman Taranis | pos=F | grid=4:2
- home | Degerfors IF | 4-4-2 | #14 Ludvig Fritzson | pos=F | grid=4:1
- away | Malmo FF | 3-4-2-1 | #1 Robin Olsen | pos=G | grid=1:1
- away | Malmo FF | 3-4-2-1 | #5 Andrej Đurić | pos=D | grid=2:3
- away | Malmo FF | 3-4-2-1 | #7 Otto Rosengren | pos=D | grid=2:2
- away | Malmo FF | 3-4-2-1 | #44 Malte Palsson | pos=D | grid=2:1
- away | Malmo FF | 3-4-2-1 | #17 Jens Stryger Larsen | pos=M | grid=3:4
- away | Malmo FF | 3-4-2-1 | #40 Kenan Busuladžić | pos=M | grid=3:3
- away | Malmo FF | 3-4-2-1 | #37 Adrian Skogmar | pos=M | grid=3:2
- away | Malmo FF | 3-4-2-1 | #23 Noah Åstrand John | pos=M | grid=3:1
- away | Malmo FF | 3-4-2-1 | #29 Sead Hakšabanović | pos=F | grid=4:2
- away | Malmo FF | 3-4-2-1 | #24 Oscar Sjostrand | pos=F | grid=4:1
- away | Malmo FF | 3-4-2-1 | #20 Erik Botheim | pos=F | grid=5:1

## Guardrails
- This is a direct API-Football lineup snapshot using canonical board fixture_id.
- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.
- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.
