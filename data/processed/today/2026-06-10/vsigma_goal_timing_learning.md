# vSIGMA Goal Timing Learning - 2026-06-10

## Summary
- goal_timing_rows: 8
- goal_timing_data_status_counts: NO_GOAL_TIMING_DATA=8
- goal_timing_profile_counts: GOAL_TIMING_DATA_MISSING=7; DIAGNOSTIC_NO_GOAL_TIMING_LEARNING=1
- goal_timing_learning_label_counts: NO_TIMING_SIGNAL=7; DIAGNOSTIC_NOT_REAL_FIXTURE=1
- timing_evidence_level_counts: LOW=7; NONE=1
- manual_review_required_counts: NO=8
- auto_apply: NO
- production_change: NO

## Goal Timing Rows
- DIAGNOSTIC_NO_GOAL_TIMING_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- GOAL_TIMING_DATA_MISSING | Las Palmas vs Malaga | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Almeria vs Castellón | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Almeria vs Castellón | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Nautico Recife vs Fortaleza EC | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Ponte Preta vs Cuiaba | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Malaga vs Las Palmas | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Cape Town City vs Magesi | first_goal=NA team=UNKNOWN | 0-0HT=NO early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA

## Guardrails
- This goal timing report is advisory only and never changes picks, stake, live gates, or weights.
- Missing event data is not treated as a model failure by itself.
- Early/late goal labels require causal review before any lesson is accepted.
- No automatic entry timing, live, source registry, or production changes are created here.
