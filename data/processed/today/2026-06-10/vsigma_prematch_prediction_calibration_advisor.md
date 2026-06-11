# vSIGMA Prematch Prediction Calibration Advisor - 2026-06-10

## Summary
- advice_rows: 12
- watch_rows: 4
- caution_rows: 2
- hold_rows: 6
- next_action: Review calibration advice only; keep auto_apply disabled until sample is large enough.
- auto_apply: NO
- production_change: NO

## Advice
- HOLD | ALL / ALL | focus=sample_size | sample=2 | rate=2 | OBSERVE_MORE | Sample below 5; do not change weights yet.
- WATCH | ALL / ALL | focus=result_family | sample=2 | rate=100.0 | KEEP_RESULT_FAMILY_SIGNAL | Result-family prediction is currently strong; keep monitoring.
- WATCH | ALL / ALL | focus=score_neighbor | sample=2 | rate=100.0 | PRIORITIZE_SCORE_NEIGHBOR_OVER_EXACT | Neighbor score is more stable than exact score.
- WATCH | ALL / ALL | focus=goals_2plus | sample=2 | rate=100.0 | KEEP_2PLUS_GOALS_SIGNAL | 2+ goals signal is strong in current sample.
- CAUTION | ALL / ALL | focus=goals_3plus | sample=2 | rate=0.0 | REQUIRE_STRONGER_EVIDENCE_FOR_3PLUS | 3+ goals conversion is weak; avoid aggressive goal inflation.
- WATCH | ALL / ALL | focus=both_scored | sample=2 | rate=100.0 | KEEP_BTTS_AS_SUPPORTING_SIGNAL | Both-scored signal is strong as a supporting prediction layer.
- HOLD | RECENT / LAST_20 | focus=sample_size | sample=2 | rate=2 | OBSERVE_MORE | Sample below 5; do not change weights yet.
- HOLD | RECENT / LAST_50 | focus=sample_size | sample=2 | rate=2 | OBSERVE_MORE | Sample below 5; do not change weights yet.
- HOLD | PREDICTED_RESULT / AWAY_OR_DRAW | focus=sample_size | sample=2 | rate=2 | OBSERVE_MORE | Sample below 5; do not change weights yet.
- HOLD | GOAL_PROFILE / HIGH_GOALS | focus=sample_size | sample=1 | rate=1 | OBSERVE_MORE | Sample below 5; do not change weights yet.
- CAUTION | GOAL_PROFILE / HIGH_GOALS | focus=high_goals_aggression | sample=1 | rate=0.0 | DOWNGRADE_HIGH_GOALS_TO_OPEN_GOALS_REVIEW | High-goal profile is over-aggressive versus realized goal profile / 3+ goals.
- HOLD | GOAL_PROFILE / MODERATE_GOALS | focus=sample_size | sample=1 | rate=1 | OBSERVE_MORE | Sample below 5; do not change weights yet.
