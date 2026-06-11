# vSIGMA Ad Hoc Team Style + Player Impact - 2026-06-11

## Summary
- fixture_found: YES
- team_rows: 2
- player_rows: 22
- home_xi_strength: 66.0
- away_xi_strength: 67.4
- xi_edge: -1.4
- auto_apply: NO
- production_change: NO

## Team Style
### Mexico (home)
- shape: 4-1-4-1
- sample: 6
- avg_possession: 54.3%
- avg_shots: 11.8 | avg_sot: 4.0 | avg_corners: 5.0
- avg_fouls: 10.2 | avg_yellows: 1.3
- goals_for/against: 1.7 / 0.3
- tempo: MEDIUM
- attack_style: CONTROL_ATTACK
- defense_style: MID_BLOCK
- set_piece_weight: MEDIUM | transition_weight: MEDIUM

### South Africa (away)
- shape: 5-3-2
- sample: 6
- avg_possession: 62.4%
- avg_shots: 11.8 | avg_sot: 3.4 | avg_corners: 3.8
- avg_fouls: 10.2 | avg_yellows: 2.5
- goals_for/against: 0.7 / 1.2
- tempo: MEDIUM
- attack_style: CONTROL_ATTACK
- defense_style: COMPACT_LOW_BLOCK
- set_piece_weight: HIGH | transition_weight: LOW

## Player Impact Scores
### Mexico (home)
- Raúl Rangel | pos=G | role=GOALKEEPER | api_pos=G | grid=1:1 | score=70.4 | atk=5 def=84 ctl=24 sp=5 | label=GOALKEEPER_STABILITY
- Raúl Jiménez | pos=F | role=STRIKER | api_pos=F | grid=5:1 | score=70.0 | atk=88 def=19 ctl=42 sp=44 | label=PRIMARY_ATTACK_THREAT
- Álvaro Fidalgo | pos=M | role=INTERIOR | api_pos=M | grid=4:2 | score=69.6 | atk=52 def=51 ctl=92 sp=50 | label=CONTROL_HUB
- Brian Gutiérrez | pos=M | role=INTERIOR | api_pos=M | grid=4:3 | score=67.7 | atk=52 def=51 ctl=87 sp=47 | label=CONTROL_HUB
- Erik Lira | pos=M | role=DEFENSIVE_MIDFIELD | api_pos=M | grid=3:1 | score=66.7 | atk=47 def=57 ctl=85 sp=47 | label=PIVOT_SCREEN
- César Montes | pos=D | role=CENTER_BACK | api_pos=D | grid=2:3 | score=64.7 | atk=17 def=85 ctl=45 sp=49 | label=CENTER_BACK_ANCHOR
- Johan Vásquez | pos=D | role=CENTER_BACK | api_pos=D | grid=2:2 | score=64.7 | atk=17 def=85 ctl=45 sp=49 | label=CENTER_BACK_ANCHOR
- Roberto Alvarado | pos=M | role=WIDE_MIDFIELD | api_pos=M | grid=4:4 | score=64.6 | atk=56 def=50 ctl=76 sp=47 | label=WIDE_BALANCE
- Julián Quiñones | pos=M | role=WIDE_MIDFIELD | api_pos=M | grid=4:1 | score=64.6 | atk=56 def=50 ctl=76 sp=47 | label=WIDE_BALANCE
- Israel Reyes | pos=D | role=FULL_BACK | api_pos=D | grid=2:4 | score=61.5 | atk=25 def=76 ctl=47 sp=43 | label=FULL_BACK_WIDTH
- Jesús Gallardo | pos=D | role=FULL_BACK | api_pos=D | grid=2:1 | score=61.5 | atk=25 def=76 ctl=47 sp=43 | label=FULL_BACK_WIDTH

### South Africa (away)
- Ronwen Williams | pos=G | role=GOALKEEPER | api_pos=G | grid=1:1 | score=72.4 | atk=5 def=88 ctl=24 sp=5 | label=GOALKEEPER_STABILITY
- Iqraam Rayners | pos=F | role=STRIKER_PAIR | api_pos=F | grid=4:2 | score=69.4 | atk=86 def=24 ctl=43 sp=44 | label=PRIMARY_ATTACK_THREAT
- Lyle Foster | pos=F | role=STRIKER_PAIR | api_pos=F | grid=4:1 | score=69.4 | atk=86 def=24 ctl=43 sp=44 | label=PRIMARY_ATTACK_THREAT
- Nkosinathi Sibisi | pos=D | role=CENTER_BACK | api_pos=D | grid=2:4 | score=68.0 | atk=17 def=93 ctl=45 sp=51 | label=CENTER_BACK_ANCHOR
- Mbekezeli Mbokazi | pos=D | role=CENTER_BACK | api_pos=D | grid=2:2 | score=68.0 | atk=17 def=93 ctl=45 sp=51 | label=CENTER_BACK_ANCHOR
- Teboho Mokoena | pos=M | role=CENTRAL_MIDFIELD | api_pos=M | grid=3:3 | score=67.3 | atk=50 def=56 ctl=85 sp=49 | label=CONTROL_HUB
- Ime Okon | pos=D | role=CENTER_BACK | api_pos=D | grid=2:3 | score=66.2 | atk=17 def=89 ctl=45 sp=49 | label=CENTER_BACK_ANCHOR
- Siphephelo Sithole | pos=M | role=CENTRAL_MIDFIELD | api_pos=M | grid=3:2 | score=65.4 | atk=50 def=56 ctl=80 sp=46 | label=CONTROL_HUB
- Jayden Adams | pos=M | role=CENTRAL_MIDFIELD | api_pos=M | grid=3:1 | score=65.4 | atk=50 def=56 ctl=80 sp=46 | label=CONTROL_HUB
- Khuliso Mudau | pos=D | role=WING_BACK | api_pos=D | grid=2:5 | score=65.1 | atk=28 def=84 ctl=47 sp=46 | label=WING_BACK_TWO_WAY
- Aubrey Modiba | pos=D | role=WING_BACK | api_pos=D | grid=2:1 | score=65.1 | atk=28 def=84 ctl=47 sp=46 | label=WING_BACK_TWO_WAY

## Interpretation
- Player scores are functional match-impact ratings, not market values.
- Role resolution uses API position + API grid + formation when available; otherwise it falls back to formation/order.
