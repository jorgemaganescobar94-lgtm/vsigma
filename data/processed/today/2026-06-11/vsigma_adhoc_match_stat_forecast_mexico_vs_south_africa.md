# vSIGMA Ad Hoc Full Match Projection - 2026-06-11

## Summary
- rows: 1
- stat_confidence: MEDIUM_HIGH
- impact_weighting_status: PLAYER_IMPACT_WEIGHTED
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

## Player Impact Weighting
- status: PLAYER_IMPACT_WEIGHTED
- XI strength: Mexico 66.6 - 67.4 South Africa | edge=-0.8
- attack_index: Mexico 64.8 - 86.0 South Africa
- defense_index: Mexico 77.2 - 88.5 South Africa
- control_index: Mexico 88.0 - 81.7 South Africa
- set_piece_index: Mexico 42.8 - 43.4 South Africa
- draw_risk_index: 69.5
- goal_suppression_index: 69.8
- adjustment_note: Forecast adjusted by XI strength, role-resolved player impact and team style.

## Probability Layer
- raw 1X2: Mexico 67.0% | draw 21.6% | South Africa 11.4%
- adjusted 1X2: Mexico 63.7% | draw 24.2% | South Africa 12.1%
- BTTS yes: 36.8%
- Over 1.5: 62.6%
- Over 2.5: 35.6%
- Under 3.5: 83.5%
- Mexico clean sheet: 52.2%
- South Africa to score: 47.8%

## Expected Goals By Phase
- raw_xG: Mexico 1.66 - 0.64 South Africa
- adjusted full_match_xG: Mexico 1.47 - 0.65 South Africa | total=2.12
- first_half_xG: Mexico 0.65 - 0.27 South Africa
- second_half_xG: Mexico 0.82 - 0.38 South Africa
- HT score forecast: 0-0 / 1-0
- first goal: Mexico | window=25-55

## Predicted Match Stats
- shots: Mexico 16 - 9 South Africa
- shots_on_target: Mexico 4 - 2 South Africa
- big_chances: Mexico 2 - 1 South Africa
- possession: Mexico 70% - 30% South Africa
- corners: Mexico 7 - 4 South Africa
- fouls: Mexico 12 - 17 South Africa
- yellow_cards: Mexico 2 - 2 South Africa
- saves: Mexico 1 - 3 South Africa
- pressure_index: Mexico 93.5 - 48.5 South Africa

## Branch Map
- base_branch: Home territorial control against compact away block.
- danger_branch: 0-0 after 60' or away transition/set-piece keeps draw alive. Player-impact layer raises draw risk due to away defensive structure/XI balance.
- first_half: Home control, away compact; first goal value high; HT likely 0-0 or 1-0.
- second_half: If home scores first, game management; if 0-0 after 60', draw branch rises sharply.

## Market Logic Translation
- robust: Mexico or draw / under 3.5
- value_expression: Mexico DNB / Mexico team over 0.5
- do_not_overstretch: Avoid handicap/goleada; player-impact layer suppresses blowout path unless early goal + sustained xG pressure confirms.

## Note
- Full match projection derived from ad hoc fixture forecast, official/estimated XI, market-implied probabilities, team style and player-impact weighting. Diagnostic only; not a betting instruction.
