# vSIGMA Forced API Board Fixture Lineups Refresh - 2026-06-18

## Summary
- fixtures_reviewed: 1
- api_calls_planned: 1
- api_calls_executed: 1
- lineup_fixtures_found: 1
- lineup_fixtures_missing: 0
- starting_xi_rows: 22
- substitute_rows: 14
- api_status_counts: OK=36
- team_side_counts: home=19; away=17
- provider_counts: API-SPORTS_DIRECT=36
- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- auto_apply: NO
- production_change: NO

## Fixture Lineup Status
- AC Oulu vs Mariehamn | fixture_id=1495703 | status=OK | starters=22 | subs=14 | note=lineups fetched directly by fixture_id

## Starting XI Rows
- home | AC Oulu | 3-4-3 | #13 Miguel Santos | pos=G | grid=1:1
- home | AC Oulu | 3-4-3 | #2 Sami Sipola | pos=D | grid=2:3
- home | AC Oulu | 3-4-3 | #3 Alex Lietsa | pos=D | grid=2:2
- home | AC Oulu | 3-4-3 | #66 Juha Pirinen | pos=D | grid=2:1
- home | AC Oulu | 3-4-3 | #22 Tuomas Kaukua | pos=M | grid=3:4
- home | AC Oulu | 3-4-3 | #6 Julius Paananen | pos=M | grid=3:3
- home | AC Oulu | 3-4-3 | #21 Iiro Mendolin | pos=M | grid=3:2
- home | AC Oulu | 3-4-3 | #27 Elias Kallio | pos=M | grid=3:1
- home | AC Oulu | 3-4-3 | #11 Lamine Ghezali | pos=M | grid=4:3
- home | AC Oulu | 3-4-3 | #26 Julius Körkkö | pos=F | grid=4:2
- home | AC Oulu | 3-4-3 | #7 Rasmus Karjalainen | pos=M | grid=4:1
- away | Mariehamn | 4-3-1-2 | #1 Kevin Lund | pos=G | grid=1:1
- away | Mariehamn | 4-3-1-2 | #18 Adam Stroud | pos=M | grid=2:4
- away | Mariehamn | 4-3-1-2 | #38 Yeboah Amankwah | pos=D | grid=2:3
- away | Mariehamn | 4-3-1-2 | #2 Noah Nurmi | pos=D | grid=2:2
- away | Mariehamn | 4-3-1-2 | #31 Samson Ngulube | pos=D | grid=2:1
- away | Mariehamn | 4-3-1-2 | #28 Jiri Nissinen | pos=D | grid=3:3
- away | Mariehamn | 4-3-1-2 | #20 Emmanuel Patut | pos=M | grid=3:2
- away | Mariehamn | 4-3-1-2 | #10 Sebastian Dahlström | pos=M | grid=3:1
- away | Mariehamn | 4-3-1-2 | #16 Anttoni Huttunen | pos=M | grid=4:1
- away | Mariehamn | 4-3-1-2 | #11 Luke Pearce | pos=F | grid=5:2
- away | Mariehamn | 4-3-1-2 | #7 Adam Larsson | pos=F | grid=5:1

## Guardrails
- This is a direct API-Football lineup snapshot using canonical board fixture_id.
- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.
- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.
