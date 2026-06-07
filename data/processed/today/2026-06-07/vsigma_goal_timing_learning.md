# vSIGMA Goal Timing Learning - 2026-06-07

## Summary
- goal_timing_rows: 2
- goal_timing_data_status_counts: NO_GOAL_TIMING_DATA=2
- goal_timing_profile_counts: DIAGNOSTIC_NO_GOAL_TIMING_LEARNING=1; GOAL_TIMING_DATA_MISSING=1
- goal_timing_learning_label_counts: DIAGNOSTIC_NOT_REAL_FIXTURE=1; NO_TIMING_SIGNAL=1
- timing_evidence_level_counts: NONE=1; LOW=1
- manual_review_required_counts: NO=2
- auto_apply: NO
- production_change: NO

## Goal Timing Rows
- DIAGNOSTIC_NO_GOAL_TIMING_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- GOAL_TIMING_DATA_MISSING | Castellón vs Almeria | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA

## Guardrails
- This goal timing report is advisory only and never changes picks, stake, live gates, or weights.
- Missing event data is not treated as a model failure by itself.
- Early/late goal labels require causal review before any lesson is accepted.
- No automatic entry timing, live, source registry, or production changes are created here.
