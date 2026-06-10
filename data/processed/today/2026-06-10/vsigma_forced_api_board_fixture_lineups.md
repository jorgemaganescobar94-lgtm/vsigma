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
- home | Malaga | 4-2-3-1 | #1 Alfonso Herrero | pos=G | grid=1:1
- home | Malaga | 4-2-3-1 | #3 Carlos Puga | pos=D | grid=2:4
- home | Malaga | 4-2-3-1 | #16 Diego Murillo | pos=D | grid=2:3
- home | Malaga | 4-2-3-1 | #20 Javi Montero | pos=D | grid=2:2
- home | Malaga | 4-2-3-1 | #31 Rafa Garrido | pos=D | grid=2:1
- home | Malaga | 4-2-3-1 | #23 Izan Merino | pos=M | grid=3:2
- home | Malaga | 4-2-3-1 | #22 Dani Lorenzo | pos=M | grid=3:1
- home | Malaga | 4-2-3-1 | #10 David Larrubia | pos=M | grid=4:3
- home | Malaga | 4-2-3-1 | #12 Carlos Dotor | pos=M | grid=4:2
- home | Malaga | 4-2-3-1 | #11 Joaquín Muñoz | pos=M | grid=4:1
- home | Malaga | 4-2-3-1 | #9 Chupete | pos=F | grid=5:1
- away | Las Palmas | 4-4-2 | #1 Dinko Horkaš | pos=G | grid=1:1
- away | Las Palmas | 4-4-2 | #2 Marvin Park | pos=D | grid=2:4
- away | Las Palmas | 4-4-2 | #4 Alex Suárez | pos=D | grid=2:3
- away | Las Palmas | 4-4-2 | #3 Mika Mármol | pos=D | grid=2:2
- away | Las Palmas | 4-4-2 | #5 Enrique Clemente | pos=D | grid=2:1
- away | Las Palmas | 4-4-2 | #18 Taisei Miyashiro | pos=M | grid=3:4
- away | Las Palmas | 4-4-2 | #16 Lorenzo Amatucci | pos=M | grid=3:3
- away | Las Palmas | 4-4-2 | #20 Kirian Rodríguez | pos=M | grid=3:2
- away | Las Palmas | 4-4-2 | #39 Estanis Pedrola | pos=M | grid=3:1
- away | Las Palmas | 4-4-2 | #21 Jonathan Viera | pos=F | grid=4:2
- away | Las Palmas | 4-4-2 | #10 Jesé Rodríguez | pos=F | grid=4:1
- home | Cape Town City | 4-4-2 | #47 Luca Diana-Oliaro | pos=G | grid=1:1
- home | Cape Town City | 4-4-2 | #19 Alifeyo Sibusiso Ziba | pos=D | grid=2:4
- home | Cape Town City | 4-4-2 | #48 Cayden Fortune | pos=D | grid=2:3
- home | Cape Town City | 4-4-2 | #25 Lorenzo Gordinho | pos=D | grid=2:2
- home | Cape Town City | 4-4-2 | #46 Bokang Telile | pos=D | grid=2:1
- home | Cape Town City | 4-4-2 | #10 Jaedin Rhodes | pos=M | grid=3:4
- home | Cape Town City | 4-4-2 | #51 Dhakier Lee | pos=M | grid=3:3
- home | Cape Town City | 4-4-2 | #55 Gabriel Amato | pos=M | grid=3:2
- home | Cape Town City | 4-4-2 | #33 Heaven Sereetsi | pos=M | grid=3:1
- home | Cape Town City | 4-4-2 | #9 Therlo Moosa | pos=F | grid=4:2
- home | Cape Town City | 4-4-2 | #7 Dženan Zajmović | pos=F | grid=4:1
- away | Magesi | 4-2-3-1 | #1 Elvis Chipezeze | pos=G | grid=1:1
- away | Magesi | 4-2-3-1 | #49 Diteboho Mofokeng | pos=D | grid=2:4
- away | Magesi | 4-2-3-1 | #4 Tshepo Makgoga | pos=D | grid=2:3
- away | Magesi | 4-2-3-1 | #5 Kgothatso Mariba | pos=M | grid=2:2
- away | Magesi | 4-2-3-1 | #8 John Mokone | pos=D | grid=2:1
- away | Magesi | 4-2-3-1 | #6 Samuel Darpoh | pos=M | grid=3:2
- away | Magesi | 4-2-3-1 | #21 Edmore Chirambadare | pos=F | grid=3:1
- away | Magesi | 4-2-3-1 | #50 Siyabonga Ndlozi | pos=D | grid=4:3
- away | Magesi | 4-2-3-1 | #10 Mcedi Vandala | pos=M | grid=4:2
- away | Magesi | 4-2-3-1 | #2 Godfrey Mashigo | pos=D | grid=4:1
- away | Magesi | 4-2-3-1 | #39 Sifiso Luthuli | pos=F | grid=5:1

## Guardrails
- This is a direct API-Football lineup snapshot using canonical board fixture_id.
- It is a prelock input only; it cannot create picks, stake, canonical board permission, or whitelist permission.
- If API returns no lineups, the system must keep NO_PREMATCH/LIVE_ONLY unless a manual approved override exists.
