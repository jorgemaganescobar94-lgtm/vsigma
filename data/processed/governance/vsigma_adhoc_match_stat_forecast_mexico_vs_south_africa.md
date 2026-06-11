# vSIGMA Ad Hoc Full Match Projection - 2026-06-11

## Summary
- rows: 1
- stat_confidence: MEDIUM_HIGH
- auto_apply: NO
- production_change: NO

## Fixture
- fixture: Mexico vs South Africa
- XI: OFFICIAL_XI | source=API_OFFICIAL_LINEUPS | shapes=4-1-4-1/5-3-2
- result_forecast: HOME_OR_DRAW
- primary_score: 1-0
- scorelines: 1-0 / 1-1 / 2-0
- goal_profile: MODERATE_GOALS
- scenario: FAVORITE_CONTROL_GAME
- tempo: CONTROLLED

## Probability Layer
- 1X2: Mexico 67.2% | draw 21.6% | South Africa 11.2%
- BTTS yes: 38.3%
- Over 1.5: 66.9%
- Over 2.5: 40.4%
- Under 3.5: 79.9%
- Mexico clean sheet: 52.7%
- South Africa to score: 47.3%

## Expected Goals By Phase
- full_match_xG: Mexico 1.66 - 0.64 South Africa | total=2.3
- first_half_xG: Mexico 0.73 - 0.27 South Africa
- second_half_xG: Mexico 0.93 - 0.37 South Africa
- HT score forecast: 1-0
- first goal: Mexico | window=25-55

## Predicted Match Stats
- shots: Mexico 17 - 9 South Africa
- shots_on_target: Mexico 4 - 2 South Africa
- big_chances: Mexico 2 - 1 South Africa
- possession: Mexico 68% - 32% South Africa
- corners: Mexico 7 - 4 South Africa
- fouls: Mexico 12 - 17 South Africa
- yellow_cards: Mexico 2 - 2 South Africa
- saves: Mexico 1 - 3 South Africa
- pressure_index: Mexico 94.8 - 49.2 South Africa

## Branch Map
- base_branch: Home territorial control against compact away block.
- danger_branch: 0-0 after 60' or away transition/set-piece keeps draw alive.
- first_half: Home control, away compact; first goal value high; HT likely 0-0 or 1-0.
- second_half: If home scores first, game management; if 0-0 after 60', draw branch rises sharply.

## Market Logic Translation
- robust: Mexico or draw / under 3.5
- value_expression: Mexico DNB / Mexico team over 0.5
- do_not_overstretch: Avoid handicap/goleada unless early goal + sustained xG pressure confirms.

## Note
- Full match projection derived from ad hoc fixture forecast, official/estimated XI, market-implied probabilities and scenario logic. Diagnostic only; not a betting instruction.
