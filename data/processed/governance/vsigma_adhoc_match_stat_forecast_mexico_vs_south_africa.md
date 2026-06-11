# vSIGMA Ad Hoc Full Match Projection - 2026-06-11

## Summary
- rows: 1
- stat_confidence: MEDIUM_HIGH
- impact_weighting_status: PLAYER_IMPACT_WEIGHTED
- unit_weighting_status: UNIT_WEIGHTED_TEAM_INDEX
- auto_apply: NO
- production_change: NO

## Fixture
- fixture: Mexico vs South Africa
- XI: OFFICIAL_XI | source=API_OFFICIAL_LINEUPS | shapes=4-1-4-1/5-3-2
- result_forecast: HOME_OR_DRAW
- primary_score: 1-0
- scorelines_base: 1-0 / 1-1 / 2-0
- adjusted_goal_profile: LOW_TO_MODERATE_GOALS
- scenario: FAVORITE_CONTROL_GAME
- tempo: CONTROLLED

## Unit-Weighted Team Index
- status: UNIT_WEIGHTED_TEAM_INDEX
- XI strength: Mexico 66.6 - 67.4 South Africa | edge=-0.8
- unit_team_index: Mexico 68.7 - 65.6 South Africa | unit_edge=3.1
- raw_role_attack_index: Mexico 64.8 - 86.0 South Africa
- style_attack_index: Mexico 61.6 - 46.1 South Africa
- unit_weighted_attack_index: Mexico 65.7 - 55.0 South Africa
- unit_defense_index: Mexico 76.9 - 81.0 South Africa
- unit_control_index: Mexico 76.1 - 72.4 South Africa
- set_piece_index: Mexico 42.8 - 43.4 South Africa
- draw_risk_index: 64.4
- goal_suppression_index: 65.3
- adjustment_note: Forecast adjusted by unit-weighted team index: player roles + team production + style context.

## Probability Layer
- raw 1X2: Mexico 67.0% | draw 21.6% | South Africa 11.4%
- adjusted 1X2: Mexico 67.0% | draw 23.8% | South Africa 9.3%
- BTTS yes: 31.6%
- Over 1.5: 61.3%
- Over 2.5: 34.2%
- Under 3.5: 84.4%
- Mexico clean sheet: 60.0%
- South Africa to score: 40.0%

## Expected Goals By Phase
- raw_xG: Mexico 1.66 - 0.64 South Africa
- adjusted full_match_xG: Mexico 1.56 - 0.51 South Africa | total=2.07
- first_half_xG: Mexico 0.69 - 0.21 South Africa
- second_half_xG: Mexico 0.87 - 0.3 South Africa
- HT score forecast: 0-0 / 1-0
- first goal: Mexico | window=25-55

## Predicted Match Stats
- shots: Mexico 16 - 8 South Africa
- shots_on_target: Mexico 4 - 1 South Africa
- big_chances: Mexico 2 - 1 South Africa
- possession: Mexico 70% - 30% South Africa
- corners: Mexico 7 - 4 South Africa
- fouls: Mexico 12 - 17 South Africa
- yellow_cards: Mexico 2 - 2 South Africa
- saves: Mexico 0 - 3 South Africa
- pressure_index: Mexico 93.5 - 46.5 South Africa

## Branch Map
- base_branch: Home territorial control against compact away block.
- danger_branch: 0-0 after 60' or away transition/set-piece keeps draw alive.
- first_half: Home control, away compact; first goal value high; HT likely 0-0 or 1-0.
- second_half: If home scores first, game management; if 0-0 after 60', draw branch rises sharply.

## Market Logic Translation
- robust: Mexico or draw / under 3.5
- value_expression: Mexico DNB / Mexico team over 0.5
- do_not_overstretch: Avoid handicap/goleada; unit-weighted layer suppresses blowout path unless early goal + sustained xG pressure confirms.

## Note
- Full match projection derived from ad hoc fixture forecast, official/estimated XI, market-implied probabilities, team style and unit-weighted player-impact weighting. Diagnostic only; not a betting instruction.
