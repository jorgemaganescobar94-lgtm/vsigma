# vSIGMA Prematch Calibration Rule Gate - 2026-06-10

## Summary
- rows: 12
- candidate_rows: 0
- blocked_sample_rows: 6
- blocked_history_rows: 0
- hold_rows: 6
- min_sample: 20
- min_repeat_days: 3
- next_action: No automatic rule changes; review candidates only after sample and history gates pass.
- auto_apply: NO
- production_change: NO

## Gate Rows
- HOLD_ONLY | ALL / ALL | focus=sample_size | sample=2 | repeat_days=1 | OBSERVE_MORE | Advisor requested observation only.
- BLOCKED_SAMPLE | ALL / ALL | focus=result_family | sample=2 | repeat_days=1 | KEEP_RESULT_FAMILY_SIGNAL | sample 2 below minimum 20.
- BLOCKED_SAMPLE | ALL / ALL | focus=score_neighbor | sample=2 | repeat_days=1 | PRIORITIZE_SCORE_NEIGHBOR_OVER_EXACT | sample 2 below minimum 20.
- BLOCKED_SAMPLE | ALL / ALL | focus=goals_2plus | sample=2 | repeat_days=1 | KEEP_2PLUS_GOALS_SIGNAL | sample 2 below minimum 20.
- BLOCKED_SAMPLE | ALL / ALL | focus=goals_3plus | sample=2 | repeat_days=1 | REQUIRE_STRONGER_EVIDENCE_FOR_3PLUS | sample 2 below minimum 20.
- BLOCKED_SAMPLE | ALL / ALL | focus=both_scored | sample=2 | repeat_days=1 | KEEP_BTTS_AS_SUPPORTING_SIGNAL | sample 2 below minimum 20.
- HOLD_ONLY | RECENT / LAST_20 | focus=sample_size | sample=2 | repeat_days=1 | OBSERVE_MORE | Advisor requested observation only.
- HOLD_ONLY | RECENT / LAST_50 | focus=sample_size | sample=2 | repeat_days=1 | OBSERVE_MORE | Advisor requested observation only.
- HOLD_ONLY | PREDICTED_RESULT / AWAY_OR_DRAW | focus=sample_size | sample=2 | repeat_days=1 | OBSERVE_MORE | Advisor requested observation only.
- HOLD_ONLY | GOAL_PROFILE / HIGH_GOALS | focus=sample_size | sample=1 | repeat_days=1 | OBSERVE_MORE | Advisor requested observation only.
- BLOCKED_SAMPLE | GOAL_PROFILE / HIGH_GOALS | focus=high_goals_aggression | sample=1 | repeat_days=1 | DOWNGRADE_HIGH_GOALS_TO_OPEN_GOALS_REVIEW | sample 1 below minimum 20.
- HOLD_ONLY | GOAL_PROFILE / MODERATE_GOALS | focus=sample_size | sample=1 | repeat_days=1 | OBSERVE_MORE | Advisor requested observation only.
