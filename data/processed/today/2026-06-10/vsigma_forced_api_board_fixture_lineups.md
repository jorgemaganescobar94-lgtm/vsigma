# vSIGMA Forced API Board Fixture Lineups Refresh - 2026-06-10

## Summary
- fixtures_reviewed: 2
- api_calls_planned: 2
- api_calls_executed: 2
- lineup_fixtures_found: 2
- lineup_fixtures_missing: 0
- starting_xi_rows: 44
- substitute_rows: 42
- api_status_counts: OK=86
- team_side_counts: home=43; away=43
- provider_counts: API-SPORTS_DIRECT=86
- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- auto_apply: NO
- production_change: NO

## Fixture Lineup Status
- Malaga vs Las Palmas | fixture_id=1548055 | status=OK | starters=22 | subs=24 | note=lineups fetched directly by fixture_id
- Cape Town City vs Magesi | fixture_id=1546281 | status=OK | starters=22 | subs=18 | note=lineups fetched directly by fixture_id

## Starting XI Rows
- home | Malaga | 4-2-3-1 | #1 A. Herrero | pos=G | grid=1:1
- home | Malaga | 4-2-3-1 | #3 C. Puga | pos=D | grid=2:4
- home | Malaga | 4-2-3-1 | #16 D. Murillo | pos=D | grid=2:3
- home | Malaga | 4-2-3-1 | #20 J. Montero | pos=D | grid=2:2
- home | Malaga | 4-2-3-1 | #31 Rafita | pos=D | grid=2:1
- home | Malaga | 4-2-3-1 | #23 I. Merino | pos=M | grid=3:2
- home | Malaga | 4-2-3-1 | #22 D. Lorenzo | pos=M | grid=3:1
- home | Malaga | 4-2-3-1 | #10 D. Larrubia | pos=M | grid=4:3
- home | Malaga | 4-2-3-1 | #12 C. Dotor | pos=M | grid=4:2
- home | Malaga | 4-2-3-1 | #11 J. Munoz | pos=M | grid=4:1
- home | Malaga | 4-2-3-1 | #9 Chupe | pos=F | grid=5:1
- away | Las Palmas | 4-4-2 | #1 D. Horkas | pos=G | grid=1:1
- away | Las Palmas | 4-4-2 | #2 Marvin | pos=D | grid=2:4
- away | Las Palmas | 4-4-2 | #4 Alex Suarez | pos=D | grid=2:3
- away | Las Palmas | 4-4-2 | #3 M. Marmol | pos=D | grid=2:2
- away | Las Palmas | 4-4-2 | #5 E. Clemente | pos=D | grid=2:1
- away | Las Palmas | 4-4-2 | #18 T. Miyashiro | pos=M | grid=3:4
- away | Las Palmas | 4-4-2 | #16 L. Amatucci | pos=M | grid=3:3
- away | Las Palmas | 4-4-2 | #20 K. Rodriguez | pos=M | grid=3:2
- away | Las Palmas | 4-4-2 | #39 E. Pedrola | pos=M | grid=3:1
- away | Las Palmas | 4-4-2 | #21 J. Viera | pos=F | grid=4:2
- away | Las Palmas | 4-4-2 | #10 Jese | pos=F | grid=4:1
- home | Cape Town City | 4-4-2 | #47 L. Diana-Olario | pos=G | grid=1:1
- home | Cape Town City | 4-4-2 | #19 A. S. Ziba | pos=D | grid=2:4
- home | Cape Town City | 4-4-2 | #48 C. Fortune | pos=D | grid=2:3
- home | Cape Town City | 4-4-2 | #25 L. Gordinho | pos=D | grid=2:2
- home | Cape Town City | 4-4-2 | #46 B. Telile | pos=D | grid=2:1
- home | Cape Town City | 4-4-2 | #10 J. Rhodes | pos=M | grid=3:4
- home | Cape Town City | 4-4-2 | #51 D. Lee | pos=M | grid=3:3
- home | Cape Town City | 4-4-2 | #55 G. Amato | pos=M | grid=3:2
- home | Cape Town City | 4-4-2 | #33 H. Sereets | pos=M | grid=3:1
- home | Cape Town City | 4-4-2 | #9 T. Moosa | pos=F | grid=4:2
- home | Cape Town City | 4-4-2 | #7 D. Zajmovic | pos=F | grid=4:1
- away | Magesi | 4-2-3-1 | #1 E. Chipezeze | pos=G | grid=1:1
- away | Magesi | 4-2-3-1 | #49 D. Mofokeng | pos=D | grid=2:4
- away | Magesi | 4-2-3-1 | #4 T. Makgoga | pos= | grid=2:3
- away | Magesi | 4-2-3-1 | #5 K. Mariba | pos=M | grid=2:2
- away | Magesi | 4-2-3-1 | #8 J. M. Mokone | pos= | grid=2:1
- away | Magesi | 4-2-3-1 | #6 S. Darpoh | pos=M | grid=3:2
- away | Magesi | 4-2-3-1 | #21 E. Chirambadare | pos=F | grid=3:1
- away | Magesi | 4-2-3-1 | #50 S. Ndlozi | pos=D | grid=4:3
- away | Magesi | 4-2-3-1 | #10 M. Vandala | pos=M | grid=4:2
- away | Magesi | 4-2-3-1 | #2 T. Mashigo | pos= | grid=4:1
- away | Magesi | 4-2-3-1 | #39 S. Luthuli | pos=F | grid=5:1

## Guardrails
- This is a direct API-Football lineup snapshot using canonical board fixture_id.
- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.
- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.
